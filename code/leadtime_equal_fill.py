"""Lead-time sensitivity at equal fill rate (reviewer point; Theodorou et al. 2025 find that the lead time matters).

The main comparison uses L = 2 weeks (R = 1). Here the default policy (no liquidation) is simulated for L = 1, 2, 4
over the τ grid, using the cached forecasts of the main window for the matching horizon h = L + 1 (h = 2, 3, 5).
HGB-Q has no cached forecasts at h = 2 and 5 and is left out. The quantile combination C2 = mean(LGB-Q, TSB-NB)
(combination.py) is included. Reported per dataset and lead time:
    inventory needed by LGB-Q at fill 0.90 / 0.92 / 0.94;
    Δ = I_method / I_LGB-Q − 1 with 95% bootstrap CIs over series (200 resamples);
    regret: excess inventory over the best single method, averaged over the reached targets 0.90–0.98.
Writes code/outputs/leadtime_equal_fill.md and .csv.

Usage:
    python code/leadtime_equal_fill.py
"""
import os
import sys

import numpy as np
import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from f2d import classify, config, data, policy  # noqa: E402
from segment_eval import TARGETS, curve, inv_at  # noqa: E402

SINGLE = ["empirical", "tsb_nb", "ets", "lgb_tweedie", "lgb_conformal", "lgb_quantile"]
LAB = {"empirical": "EMP", "tsb_nb": "TSB-NB", "ets": "ETS", "lgb_tweedie": "LGB-T", "lgb_conformal": "LGB-C",
       "lgb_quantile": "LGB-Q", "C2": "C2"}
LEADS = (1, 2, 4)
WIN = {0: "main", 26: "second", 52: "third"}
EVAL = (0.90, 0.92, 0.94)
N_BOOT = 200


def run(name, L, rng, offset=0):
    R = config.DEFAULT["R"]
    h = L + R
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
    w = slice(config.WARMUP_WEEKS, None)
    fc = os.path.join(config.CACHE, "forecasts", name + (f"_w{offset}" if offset else ""))
    qs = list(config.QUANTILES)
    Q = {m: np.load(os.path.join(fc, f"{m}_h{h}.npz"))["Q"][idx] for m in SINGLE}
    Q["C2"] = (Q["lgb_quantile"] + Q["tsb_nb"]) / 2
    tot = {"demand": D[:, w].sum(1)}
    for m, q in Q.items():
        for tau in config.TAU_GRID:
            S = q[:, :, qs.index(tau)]
            sim = policy.simulate(D, S, np.full_like(S, np.inf), L)
            tot[m, tau, "sales"] = sim["sales"][:, w].sum(1)
            tot[m, tau, "onhand"] = sim["on_hand_end"][:, w].sum(1)
    n = len(idx)
    methods = list(Q)
    curves = {m: curve(tot, np.array([m] * n)) for m in methods}
    need = pd.DataFrame({m: [inv_at(*curves[m], t) for t in TARGETS] for m in methods}, index=TARGETS)
    best = need[SINGLE].min(axis=1)
    boots = [rng.integers(0, n, n) for _ in range(N_BOOT)]
    bc = {m: [curve(tot, np.array([m] * n), b) for b in boots] for m in methods}
    rows = []
    for m in methods:
        rg = need[m] / best - 1
        r = dict(dataset=name, window=WIN[offset], L=L, method=LAB[m], regret=rg.mean(skipna=True), targets_reached=int(rg.notna().sum()))
        for tg in EVAL:
            v, ref = inv_at(*curves[m], tg), inv_at(*curves["lgb_quantile"], tg)
            r[f"inv_{tg:.2f}"] = v
            if m == "lgb_quantile":
                continue
            rel = np.array([inv_at(*bc[m][k], tg) / inv_at(*bc["lgb_quantile"][k], tg) - 1 for k in range(N_BOOT)])
            ok = np.isfinite(rel)
            r[f"d_{tg:.2f}"] = v / ref - 1 if np.isfinite(v) and np.isfinite(ref) else np.nan
            r[f"lo_{tg:.2f}"], r[f"hi_{tg:.2f}"] = (np.percentile(rel[ok], [2.5, 97.5]) if ok.mean() >= 0.95 else (np.nan, np.nan))
        rows.append(r)
    return rows


def main():
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("--offsets", default="0")
    ap.add_argument("--datasets", default="M5,VN1")
    ap.add_argument("--suffix", default=None)
    a = ap.parse_args()
    offsets = [int(x) for x in a.offsets.split(",")]
    sfx = a.suffix if a.suffix is not None else ("" if offsets == [0] else "_all_windows")
    rng = np.random.default_rng(config.SEED)
    rows = []
    for d in a.datasets.split(","):
        for off in offsets:
            for L in LEADS:
                rows += run(d, L, rng, off)
                print(d, WIN[off], "L =", L, "done", flush=True)
    res = pd.DataFrame(rows)
    res.to_csv(os.path.join(config.OUTPUTS, f"leadtime_equal_fill{sfx}.csv"), index=False)

    def cell(r, tg):
        if r.method == "LGB-Q":
            v = r[f"inv_{tg:.2f}"]
            return "—" if not np.isfinite(v) else f"{v:.2f} wk"
        v, lo, hi = r[f"d_{tg:.2f}"], r[f"lo_{tg:.2f}"], r[f"hi_{tg:.2f}"]
        if not np.isfinite(v):
            return "—"
        return f"{100 * v:+.1f}" + (f" [{100 * lo:+.1f}, {100 * hi:+.1f}]" if np.isfinite(lo) else "")
    lines = ["# Lead-time sensitivity at equal fill rate, windows " + ", ".join(WIN[o] for o in offsets) + " (generated by code/leadtime_equal_fill.py)", "",
             "R = 1, no liquidation, forecasts for h = L + 1. Row LGB-Q: inventory needed (weeks of demand). Other rows: "
             "Δ vs LGB-Q in % with 95% bootstrap CI over series (positive = LGB-Q needs less). '—' = target not reached. "
             "HGB-Q not included (no forecasts at h = 2 and 5). C2 = mean of the LGB-Q and TSB-NB quantiles.", ""]
    for (d, w, L), g in res.groupby(["dataset", "window", "L"], sort=False):
        lines += [f"## {d}, {w} window, L = {L}", "", "| method | fill 0.90 | fill 0.92 | fill 0.94 | regret % | targets reached |", "|---|---|---|---|---|---|"]
        for _, r in g.iterrows():
            lines.append(f"| {r.method} | " + " | ".join(cell(r, tg) for tg in EVAL) + f" | {100 * r.regret:.1f} | {r.targets_reached} |")
        lines.append("")
    piv = (100 * res.pivot_table(index="method", columns=["dataset", "window", "L"], values="regret")).round(1)
    piv["max"] = piv.max(axis=1)
    lines += ["## Regret summary (% excess over the best single method; max over all dataset × window × lead-time runs)", "",
              piv.sort_values("max").to_markdown(), ""]
    with open(os.path.join(config.OUTPUTS, f"leadtime_equal_fill{sfx}.md"), "w", encoding="utf-8") as fh:
        fh.write("\n".join(lines))
    print(f"written code/outputs/leadtime_equal_fill{sfx}.md")


if __name__ == "__main__":
    main()
