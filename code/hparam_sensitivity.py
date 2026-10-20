"""Hyper-parameter sensitivity of the main comparison (reviewer point: no model is tuned).

LGB-Q and LGB-T are refitted for the replenishment horizon (h = 3) under alternative LightGBM settings, on the main
test window. For each setting the script reports the accuracy of both models and the inventory needed at equal
fill rate, with bootstrap confidence intervals over series for
    Δ(LGB-T)   = I_LGB-T / I_LGB-Q − 1     same setting for both models (point forecast + safety stock vs quantiles)
    Δ(TSB-NB)  = I_TSB-NB / I_LGB-Q − 1    TSB-NB has no such hyper-parameters (cached forecast)
    Δ(default) = I_LGB-Q(setting) / I_LGB-Q(default) − 1
Forecasts are cached in data/cache/forecasts/<DATASET>_hp_<setting>/. Writes code/outputs/hparam_sensitivity.md/.csv.

Usage:
    python code/hparam_sensitivity.py --datasets VN1,M5
"""
import argparse
import os
import sys
import time
import warnings

warnings.filterwarnings("ignore")
import numpy as np
import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from f2d import classify, config, data, models, policy  # noqa: E402
from f2d.features import Builder  # noqa: E402

SETTINGS = {
    "default": {},                                                              # lr 0.05, 63 leaves, ≥200 per leaf, λ2 = 1
    "small_trees": dict(num_leaves=15, min_data_in_leaf=100),
    "large_trees": dict(num_leaves=255, min_data_in_leaf=50),
    "regularised": dict(num_leaves=31, min_data_in_leaf=500, lambda_l2=10.0, feature_fraction=0.6),
}
TARGETS = (0.90, 0.92, 0.94, 0.96)
N_BOOT = 200
H = config.DEFAULT["L"] + config.DEFAULT["R"]


def totals_of(Q, D, qs, L):
    w = slice(config.WARMUP_WEEKS, None)
    out = {}
    for tau in config.TAU_GRID:
        S = Q[:, :, qs.index(tau)]
        sim = policy.simulate(D, S, np.full_like(S, np.inf), L)
        out[tau] = (sim["sales"][:, w].sum(1), sim["on_hand_end"][:, w].sum(1))
    return out


def inv_at(tot, dem, target, idx=None):
    sl = slice(None) if idx is None else idx
    d = dem[sl].sum()
    f = np.maximum.accumulate(np.array([tot[t][0][sl].sum() / d for t in config.TAU_GRID]))
    i = np.array([tot[t][1][sl].sum() / d for t in config.TAU_GRID])
    return np.interp(target, f, i) if f.min() <= target <= f.max() else np.nan


def wql(Q, Dt, qs):
    e = Dt[:, :, None] - Q
    ok = ~np.isnan(Dt)[:, :, None] & ~np.isnan(Q)
    pin = np.where(ok, np.maximum(np.asarray(qs) * e, (np.asarray(qs) - 1) * e), 0.0)
    return pin.sum() / (len(qs) * np.nansum(np.where(ok.any(2), Dt, np.nan)))


def run(name):
    p = data.load(name)
    Y = p["Y"]
    T = Y.shape[1]
    test0 = T - config.TEST_WEEKS
    origins = list(range(test0, T))
    sel = p["start"] <= test0 - config.VALID_WEEKS
    cls, _, _ = classify.classify(Y, p["start"], test0)
    sel &= cls != "none"
    idx = np.flatnonzero(sel)
    b = Builder(p)
    qs = list(config.QUANTILES)
    L = config.DEFAULT["L"]
    D = np.nan_to_num(Y[:, test0:T]).astype(np.float64)[idx]
    dem = D[:, config.WARMUP_WEEKS:].sum(1)
    Dt = np.stack([b.target(o, H) for o in origins], 1)[idx]
    std = os.path.join(config.CACHE, "forecasts", name)
    tsb = totals_of(np.load(os.path.join(std, f"tsb_nb_h{H}.npz"))["Q"][idx], D, qs, L)
    base = dict(models.LGB_PARAMS)
    rng = np.random.default_rng(config.SEED)
    boots = [rng.integers(0, len(idx), len(idx)) for _ in range(N_BOOT)]
    rows, ref = [], None
    for sname, over in SETTINGS.items():
        fc = std if sname == "default" else os.path.join(config.CACHE, "forecasts", f"{name}_hp_{sname}")
        os.makedirs(fc, exist_ok=True)
        Q = {}
        for m in ("lgb_quantile", "lgb_tweedie"):
            path = os.path.join(fc, f"{m}_h{H}.npz")
            if os.path.exists(path):
                Q[m] = np.load(path)["Q"]
            else:
                models.LGB_PARAMS = {**base, **over}
                t0 = time.time()
                print(f"{name} {sname}: fitting {m} ...", flush=True)
                Q[m] = models.MODELS[m](b, origins, H, qs, sel, log=lambda *a, **k: None)
                np.savez_compressed(path, Q=Q[m])
                print(f"    done in {time.time() - t0:.0f}s", flush=True)
                models.LGB_PARAMS = base
        tq, tt = totals_of(Q["lgb_quantile"][idx], D, qs, L), totals_of(Q["lgb_tweedie"][idx], D, qs, L)
        if sname == "default":
            ref = tq
        r = dict(dataset=name, setting=sname, **{k: v for k, v in over.items()},
                 wQL_LGBQ=wql(Q["lgb_quantile"][idx], Dt, qs), wQL_LGBT=wql(Q["lgb_tweedie"][idx], Dt, qs))
        for tg in TARGETS:
            a = inv_at(tq, dem, tg)
            r[f"inv_LGBQ_{tg:.2f}"] = a
            for lab, other, num_first in (("LGBT", tt, True), ("TSBNB", tsb, True), ("default", ref, False)):
                x = inv_at(other, dem, tg)
                point = (x / a - 1) if num_first else (a / x - 1)
                bs = []
                for bi in boots:
                    aa, xx = inv_at(tq, dem, tg, bi), inv_at(other, dem, tg, bi)
                    bs.append((xx / aa - 1) if num_first else (aa / xx - 1))
                bs = np.array(bs)
                okb = np.isfinite(bs)
                r[f"d_{lab}_{tg:.2f}"] = point
                r[f"lo_{lab}_{tg:.2f}"], r[f"hi_{lab}_{tg:.2f}"] = (np.percentile(bs[okb], [2.5, 97.5]) if okb.mean() >= 0.95
                                                                   else (np.nan, np.nan))
        rows.append(r)
    return pd.DataFrame(rows)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--datasets", default="VN1,M5")
    a = ap.parse_args()
    out = pd.concat([run(d) for d in a.datasets.split(",")], ignore_index=True)
    out.to_csv(os.path.join(config.OUTPUTS, "hparam_sensitivity.csv"), index=False)

    def c(r, lab, tg):
        v, lo, hi = r[f"d_{lab}_{tg:.2f}"], r[f"lo_{lab}_{tg:.2f}"], r[f"hi_{lab}_{tg:.2f}"]
        if not np.isfinite(v):
            return "—"
        return f"{100 * v:+.1f}" + (f" [{100 * lo:+.1f}, {100 * hi:+.1f}]" if np.isfinite(lo) else "")
    lines = ["# Hyper-parameter sensitivity, main window, h = 3 (generated by code/hparam_sensitivity.py)", "",
             "LightGBM settings: default = learning rate 0.05, 63 leaves, ≥ 200 samples per leaf, λ2 = 1, feature fraction 0.8; "
             + "; ".join(f"{k} = {v}" for k, v in SETTINGS.items() if v) + ".",
             "Δ in % with 95% bootstrap CI over series. Δ LGB-T and Δ TSB-NB: positive = LGB-Q (same setting) needs less "
             "inventory. Δ vs default: negative = this setting needs less inventory than the default LGB-Q.", ""]
    for tg in (0.92, 0.94):
        lines += [f"## Fill rate {tg:.2f}", "", "| dataset | setting | wQL LGB-Q | wQL LGB-T | LGB-Q inventory | Δ LGB-T | Δ TSB-NB | Δ vs default LGB-Q |",
                  "|---|---|---|---|---|---|---|---|"]
        for _, r in out.iterrows():
            lines.append(f"| {r.dataset} | {r.setting} | {r.wQL_LGBQ:.4f} | {r.wQL_LGBT:.4f} | {r[f'inv_LGBQ_{tg:.2f}']:.3f} | "
                         f"{c(r, 'LGBT', tg)} | {c(r, 'TSBNB', tg)} | {c(r, 'default', tg)} |")
        lines.append("")
    with open(os.path.join(config.OUTPUTS, "hparam_sensitivity.md"), "w", encoding="utf-8") as fh:
        fh.write("\n".join(lines))
    print("written code/outputs/hparam_sensitivity.md")


if __name__ == "__main__":
    main()
