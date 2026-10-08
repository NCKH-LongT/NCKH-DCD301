"""End-to-end benchmark: panel → classes → forecasts → Decision Engine → simulation → KPIs.

Outputs (code/outputs/<DATASET>/):
    classes.csv            ADI, CV², demand class of every evaluated series
    forecast_metrics.csv   SQL, RMSSE, coverage by model × horizon × demand class
    kpi.csv                inventory KPIs by model × policy × scenario × demand class
    summary.md             default-scenario tables
Forecasts are cached in data/cache/forecasts/<DATASET>/<model>_h<h>.npz (delete to recompute).

Usage:
    python code/run_pipeline.py --dataset VN1
    python code/run_pipeline.py --dataset M5 --grid full --boot 200
    python code/run_pipeline.py --dataset M5 --stores CA_1 --models empirical,tsb      # quick run
"""
import argparse
import os
import sys
import time
import warnings

warnings.filterwarnings("ignore", category=RuntimeWarning)

import numpy as np
import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from f2d import classify, config, data, evaluate, models, policy  # noqa: E402
from f2d.features import Builder  # noqa: E402

ALL_MODELS = ["empirical", "tsb", "tsb_nb", "ets", "lgb_tweedie", "lgb_conformal", "hgb_quantile", "lgb_quantile"]
R = config.DEFAULT["R"]


def scenarios(grid):
    """One-at-a-time grid around the default scenario (data_flow.md §7)."""
    d = config.DEFAULT
    base = dict(tau=d["tau"], L=d["L"], H=d["H"], q_liq=d["q_liq"], k=d["k_fixed"])
    out = []
    vary = {"tau": [d["tau"]], "L": [d["L"]], "H": [d["H"]], "q_liq": [d["q_liq"]], "k": [d["k_fixed"]]}
    if grid == "full":
        vary = {"tau": [0.8, 0.9, 0.95], "L": [1, 2, 4], "H": [8, 13, 26], "q_liq": [0.9, 0.95, 0.99], "k": [13, 26, 52]}
    for key, vals in vary.items():
        for v in vals:
            s = {**base, key: v}
            if s not in out:
                out.append(s)
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dataset", required=True, choices=["M5", "VN1"])
    ap.add_argument("--models", default=",".join(ALL_MODELS))
    ap.add_argument("--grid", default="default", choices=["default", "full"])
    ap.add_argument("--boot", type=int, default=0, help="bootstrap resamples for KPI CIs")
    ap.add_argument("--stores", default="", help="M5 only: comma-separated store_id subset")
    ap.add_argument("--tag", default="", help="suffix of the output folder")
    ap.add_argument("--default-only-models", default="hgb_quantile",
                    help="models forecast only at the default horizons (L+R, H) even with --grid full")
    a = ap.parse_args()
    names = a.models.split(",")
    t_all = time.time()

    p = data.load(a.dataset)
    Y = p["Y"]
    n, T = Y.shape
    test0 = T - config.TEST_WEEKS
    origins = list(range(test0, T))
    sel = p["start"] <= test0 - config.VALID_WEEKS
    if a.stores:
        sel &= p["attrs"]["store_id"].isin(a.stores.split(",")).to_numpy()
    cls, adi, cv2 = classify.classify(Y, p["start"], test0)
    sel &= cls != "none"
    print(f"{a.dataset}: {n:,} series x {T} weeks; test weeks {p['weeks'][test0].date()} .. {p['weeks'][-1].date()}; "
          f"evaluated series {sel.sum():,}")

    out_dir = os.path.join(config.OUTPUTS, a.dataset + (f"_{a.tag}" if a.tag else ""))
    fc_dir = os.path.join(config.CACHE, "forecasts", a.dataset + (f"_{a.tag}" if a.tag else ""))
    os.makedirs(out_dir, exist_ok=True)
    os.makedirs(fc_dir, exist_ok=True)
    pd.DataFrame({"series_id": p["attrs"]["series_id"], "start_week": p["start"], "ADI": adi, "CV2": cv2,
                  "demand_class": cls})[sel].to_csv(os.path.join(out_dir, "classes.csv"), index=False)
    groups = {"all": sel, **{c: sel & (cls == c) for c in classify.CLASSES}}
    print("  classes:", {g: int(m.sum()) for g, m in groups.items()})

    scen = scenarios(a.grid)
    horizons = sorted({s["L"] + R for s in scen} | {s["H"] for s in scen})
    default_h = [config.DEFAULT["L"] + R, config.DEFAULT["H"]]
    light = set(filter(None, a.default_only_models.split(",")))
    b = Builder(p)
    qs = list(config.QUANTILES)

    # ---- forecasts ------------------------------------------------------------------------------
    F = {}
    fm_rows = []
    s_abs, s_sq = evaluate.naive_scales(Y, p["start"], test0)
    for m in names:
        for h in (default_h if m in light else horizons):
            path = os.path.join(fc_dir, f"{m}_h{h}.npz")
            if os.path.exists(path):
                Q = np.load(path)["Q"]
            else:
                t0 = time.time()
                print(f"  forecasting {m}, h={h} ...")
                Q = models.MODELS[m](b, origins, h, qs, sel)
                np.savez_compressed(path, Q=Q)
                print(f"    done in {time.time() - t0:.0f}s")
            F[m, h] = Q
            Dt = np.stack([b.target(o, h) for o in origins], 1)
            fm = evaluate.forecast_metrics(Q, Dt, qs, h, s_abs, s_sq, groups)
            fm.insert(0, "horizon", h)
            fm.insert(0, "model", m)
            fm_rows.append(fm)
    fm = pd.concat(fm_rows, ignore_index=True)
    fm.to_csv(os.path.join(out_dir, "forecast_metrics.csv"), index=False)

    # ---- decision engine + simulation -------------------------------------------------------------
    D = np.nan_to_num(Y[:, test0:T]).astype(np.float64)
    avg26 = np.stack([b.window_sum(b.C, o - 26, o) / np.maximum(b.window_sum(b.A, o - 26, o), 1) for o in origins], 1)
    idx = np.flatnonzero(sel)
    sub = {g: m[idx] for g, m in groups.items()}
    kpi_rows = []
    for m in names:
        for s in scen:
            if (m, s["L"] + R) not in F or (m, s["H"]) not in F:
                continue
            S = F[m, s["L"] + R][idx][:, :, qs.index(s["tau"])]
            pols = {"none": np.full_like(S, np.inf),
                    "quantile": F[m, s["H"]][idx][:, :, qs.index(s["q_liq"])],
                    "fixed": s["k"] * avg26[idx]}
            for pol, thr in pols.items():
                sim = policy.simulate(D[idx], S, thr, s["L"])
                tot = evaluate.series_kpis(sim, D[idx], s["H"])
                k = evaluate.kpi_table(tot, sub, n_boot=a.boot)
                for c, v in [("model", m), ("policy", pol), *[(kk, s[kk]) for kk in ("tau", "L", "H", "q_liq", "k")]][::-1]:
                    k.insert(0, c, v)
                kpi_rows.append(k)
    kpi = pd.concat(kpi_rows, ignore_index=True)
    kpi.to_csv(os.path.join(out_dir, "kpi.csv"), index=False)

    write_summary(out_dir, a, fm, kpi, groups, sel, p, test0)
    print(f"finished in {time.time() - t_all:.0f}s -> {out_dir}")


def write_summary(out_dir, a, fm, kpi, groups, sel, p, test0):
    d = config.DEFAULT
    is_def = ((kpi.tau == d["tau"]) & (kpi.L == d["L"]) & (kpi.H == d["H"]) & (kpi.q_liq == d["q_liq"])
              & (kpi.k == d["k_fixed"]))
    lines = [f"# {a.dataset} benchmark summary (generated by code/run_pipeline.py)", "",
             f"- Evaluated series: {int(sel.sum()):,}; test weeks: {p['weeks'][test0].date()} … {p['weeks'][-1].date()} "
             f"({config.TEST_WEEKS} weeks, first {config.WARMUP_WEEKS} are warm-up)",
             f"- Default scenario: R={d['R']}, L={d['L']}, τ={d['tau']}, H={d['H']}, q_L={d['q_liq']}, k={d['k_fixed']}",
             "- Demand classes: " + ", ".join(f"{g} {int(m.sum()):,}" for g, m in groups.items()), "",
             "## Forecast accuracy (all series)", ""]
    t = fm[fm.group == "all"].drop(columns="group").round(3)
    lines += [t.to_markdown(index=False), "", "## Forecast accuracy by demand class (SQL, h = L+R)", ""]
    h_lr = d["L"] + d["R"]
    t = fm[fm.horizon == h_lr].pivot(index="model", columns="group", values="SQL").round(3)
    lines += [t.to_markdown(), "", "## Inventory KPIs, default scenario, no liquidation (all series)", ""]
    cols = ["model", "fill_rate", "csl", "inventory_weeks", "excess_weeks_of_demand"]
    cols += [c for c in kpi.columns if c.endswith(("_lo", "_hi"))]
    t = kpi[is_def & (kpi.policy == "none") & (kpi.group == "all")][cols].round(3)
    lines += [t.to_markdown(index=False), "", "## Fill rate by demand class, default scenario, no liquidation", ""]
    t = kpi[is_def & (kpi.policy == "none")].pivot(index="model", columns="group", values="fill_rate").round(3)
    lines += [t.to_markdown(), "", "## Liquidation policies, default scenario (all series)", ""]
    t = kpi[is_def & (kpi.group == "all")][["model", "policy", "fill_rate", "csl", "inventory_weeks",
                                            "excess_weeks_of_demand", "liquidated_share", "liq_series_share"]].round(4)
    lines += [t.to_markdown(index=False), ""]
    with open(os.path.join(out_dir, "summary.md"), "w", encoding="utf-8") as f:
        f.write("\n".join(lines))


if __name__ == "__main__":
    main()
