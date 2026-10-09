"""Bootstrap confidence intervals for inventory at equal fill rate, in units and in value (results.md §11, item 1).

For every method the default-scenario policy (L = 2, R = 1, no liquidation) is simulated at each τ of the grid from
the cached forecasts. Per series we keep the totals of demand, sales and end-of-week on-hand over the KPI weeks,
both in units and valued at the weekly selling price (price of the same week, forward-filled; series without any
price are excluded from the value KPIs). For each bootstrap resample of series (B = 200, seed 2026) the trade-off
curve of every method is rebuilt and the inventory (weeks of demand) needed to reach each fill target is
interpolated exactly as in analyze_results.py. Reported per dataset × class × target:
    inventory needed (point estimate and 95% CI) for every method;
    relative difference of each method vs lgb_quantile, (I_m / I_lgbq − 1), with 95% CI and the share of
    resamples where lgb_quantile needs less inventory;
    frontier rank of every method and the share of resamples in which each method has the best frontier rank.
Writes code/outputs/equal_fill_ci[_wN][_suffix].csv and .md.

Usage:
    python code/equal_fill_ci.py
    python code/equal_fill_ci.py --offset 26
    python code/equal_fill_ci.py --models ...,chronos2 --out-suffix c2
"""
import argparse
import os
import sys

import numpy as np
import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from analyze_results import TARGETS, frontier_rank  # noqa: E402
from f2d import classify, config, data, policy  # noqa: E402

MODELS = ["empirical", "tsb", "tsb_nb", "ets", "lgb_tweedie", "lgb_conformal", "hgb_quantile", "lgb_quantile"]
REF = "lgb_quantile"
CLASSES = ["all", "smooth", "erratic", "intermittent", "lumpy"]
B = 200


def totals(name, offset, models):
    """Per-series totals [n_sel] for demand and, per (model, τ), sales and on-hand; units and value."""
    d = config.DEFAULT
    L = d["L"]
    h = L + d["R"]
    p = data.load(name)
    if offset:
        p = data.truncate(p, p["Y"].shape[1] - offset)
    Y = p["Y"]
    T = Y.shape[1]
    test0 = T - config.TEST_WEEKS
    sel = p["start"] <= test0 - config.VALID_WEEKS
    cls, _, _ = classify.classify(Y, p["start"], test0)
    sel &= cls != "none"
    idx = np.flatnonzero(sel)
    D = np.nan_to_num(Y[:, test0:T]).astype(np.float64)[idx]
    P = p["P"][idx, test0:T].astype(np.float64)
    has_p = np.isfinite(P).all(1)
    P = np.nan_to_num(P)
    w = slice(config.WARMUP_WEEKS, None)
    out = {"class": cls[idx], "has_price": has_p,
           "demand": D[:, w].sum(1), "demand_v": (D * P)[:, w].sum(1)}
    fc = os.path.join(config.CACHE, "forecasts", name + (f"_w{offset}" if offset else ""))
    qs = list(config.QUANTILES)
    for m in models:
        Q = np.load(os.path.join(fc, f"{m}_h{h}.npz"))["Q"][idx]
        for tau in config.TAU_GRID:
            S = Q[:, :, qs.index(tau)]
            sim = policy.simulate(D, S, np.full_like(S, np.inf), L)
            out[m, tau, "sales"] = sim["sales"][:, w].sum(1)
            out[m, tau, "onhand"] = sim["on_hand_end"][:, w].sum(1)
            out[m, tau, "sales_v"] = (sim["sales"] * P)[:, w].sum(1)
            out[m, tau, "onhand_v"] = (sim["on_hand_end"] * P)[:, w].sum(1)
    return out


def needed(fill, inv):
    """fill, inv: [models, τ] -> inventory needed at each target [models, targets] (NaN outside the curve)."""
    R = np.full((fill.shape[0], len(TARGETS)), np.nan)
    for i in range(fill.shape[0]):
        f_ = np.maximum.accumulate(fill[i])
        for j, t in enumerate(TARGETS):
            if f_.min() <= t <= f_.max():
                R[i, j] = np.interp(t, f_, inv[i])
    return R


def analyse(tot, models, value):
    taus = list(config.TAU_GRID)
    sfx = "_v" if value else ""
    base = tot["has_price"] if value else np.ones(len(tot["class"]), bool)
    rng = np.random.default_rng(config.SEED)
    rows = []
    for g in CLASSES:
        m_g = base & ((tot["class"] == g) if g != "all" else True)
        ii = np.flatnonzero(m_g)
        if len(ii) < 20:
            continue
        # stack per-series columns: demand, then (sales, onhand) for every model × τ
        cols = [tot["demand" + sfx][ii]]
        for m in models:
            for tau in taus:
                cols += [tot[m, tau, "sales" + sfx][ii], tot[m, tau, "onhand" + sfx][ii]]
        X = np.stack(cols, 1)                                            # [n_g, 1 + 2·M·K]
        W = np.vstack([np.ones(len(ii))] + [rng.multinomial(len(ii), np.full(len(ii), 1 / len(ii))) for _ in range(B)])
        S = W @ X                                                        # [1 + B, cols]; row 0 = point estimate
        dem = S[:, 0]
        SO = S[:, 1:].reshape(len(W), len(models), len(taus), 2)
        fill = SO[..., 0] / dem[:, None, None]
        inv = SO[..., 1] / dem[:, None, None]                            # weeks of demand (equal weeks per series)
        Need = np.stack([needed(fill[b], inv[b]) for b in range(len(W))])  # [1 + B, M, targets]
        ref = models.index(REF)
        fr = np.stack([frontier_rank(pd.DataFrame(Need[b], index=models)).to_numpy() for b in range(len(W))])
        best = (fr[1:] == np.nanmin(fr[1:], axis=1, keepdims=True)).mean(0)
        for k, m in enumerate(models):
            r = dict(kpi="value" if value else "units", group=g, n_series=len(ii), model=m,
                     frontier_rank=fr[0, k], frontier_rank_lo=np.nanpercentile(fr[1:, k], 2.5),
                     frontier_rank_hi=np.nanpercentile(fr[1:, k], 97.5), best_frontier_share=best[k])
            for j, t in enumerate(TARGETS):
                v = Need[:, k, j]
                r[f"inv_{t:.2f}"] = v[0]
                with np.errstate(all="ignore"):
                    r[f"inv_{t:.2f}_lo"], r[f"inv_{t:.2f}_hi"] = np.nanpercentile(v[1:], [2.5, 97.5]) if np.isfinite(v[1:]).any() else (np.nan, np.nan)
                    rel = Need[:, k, j] / Need[:, ref, j] - 1
                    ok = np.isfinite(rel[1:])
                r[f"rel_{t:.2f}"] = rel[0]
                r[f"rel_{t:.2f}_lo"], r[f"rel_{t:.2f}_hi"] = (np.nanpercentile(rel[1:], [2.5, 97.5]) if ok.mean() >= 0.95
                                                              else (np.nan, np.nan))
                r[f"ref_less_{t:.2f}"] = np.mean(rel[1:][ok] > 0) if ok.any() else np.nan
                r[f"reached_share_{t:.2f}"] = np.isfinite(v[1:]).mean()
            rows.append(r)
    return pd.DataFrame(rows)


def fmt(x, lo, hi, pct=False):
    if not np.isfinite(x):
        return "—"
    s = f"{100 * x:+.1f}%" if pct else f"{x:.2f}"
    if np.isfinite(lo) and np.isfinite(hi):
        s += f" [{100 * lo:+.1f}, {100 * hi:+.1f}]" if pct else f" [{lo:.2f}, {hi:.2f}]"
    return s


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--offset", type=int, default=0)
    ap.add_argument("--models", default=",".join(MODELS))
    ap.add_argument("--out-suffix", default="")
    ap.add_argument("--datasets", default="M5,VN1")
    a = ap.parse_args()
    models = a.models.split(",")
    sfx = (f"_w{a.offset}" if a.offset else "") + (f"_{a.out_suffix}" if a.out_suffix else "")
    res = []
    for name in a.datasets.split(","):
        print(f"{name}: simulating τ grid ...", flush=True)
        tot = totals(name, a.offset, models)
        for value in (False, True):
            t = analyse(tot, models, value)
            t.insert(0, "dataset", name)
            res.append(t)
    res = pd.concat(res, ignore_index=True)
    res.to_csv(os.path.join(config.OUTPUTS, f"equal_fill_ci{sfx}.csv"), index=False)
    lines = [f"# Inventory at equal fill rate with bootstrap 95% CIs{(' — window ' + sfx.strip('_')) if sfx else ''} "
             "(generated by code/equal_fill_ci.py)", "",
             f"Default scenario (L = 2, no liquidation), τ ∈ {list(config.TAU_GRID)}; {B} bootstrap resamples of series "
             f"(seed {config.SEED}). 'units' = weeks of demand in units; 'value' = the same KPIs weighted by the weekly "
             f"selling price (series without price excluded). Δ vs {REF} = I_method / I_{REF} − 1 (positive = "
             f"{REF} needs less); CI shown only if the target is reached in ≥ 95% of resamples.", ""]
    for (dname, kpi), t in res.groupby(["dataset", "kpi"], sort=False):
        for g, tg in t.groupby("group", sort=False):
            lines += [f"## {dname} — {kpi} — {g} (n = {int(tg.n_series.iloc[0]):,})", "",
                      "| method | frontier rank [95% CI] | P(best) | " + " | ".join(f"Δ at fill {x:.2f}" for x in TARGETS) + " |",
                      "|---|---|---|" + "---|" * len(TARGETS)]
            for _, r in tg.iterrows():
                cells = [fmt(r[f"rel_{x:.2f}"], r[f"rel_{x:.2f}_lo"], r[f"rel_{x:.2f}_hi"], pct=True) if r.model != REF
                         else fmt(r[f"inv_{x:.2f}"], r[f"inv_{x:.2f}_lo"], r[f"inv_{x:.2f}_hi"]) for x in TARGETS]
                lines.append(f"| {r.model} | {r.frontier_rank:.1f} [{r.frontier_rank_lo:.1f}, {r.frontier_rank_hi:.1f}] | "
                             f"{r.best_frontier_share:.2f} | " + " | ".join(cells) + " |")
            lines += ["", f"Row {REF}: inventory needed (weeks of demand) [95% CI]; other rows: Δ vs {REF}.", ""]
    with open(os.path.join(config.OUTPUTS, f"equal_fill_ci{sfx}.md"), "w", encoding="utf-8") as fh:
        fh.write("\n".join(lines))
    print(f"written code/outputs/equal_fill_ci{sfx}.md")


if __name__ == "__main__":
    main()
