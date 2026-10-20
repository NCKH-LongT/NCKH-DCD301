"""Learned vs equal combination weight (the "forecast combination puzzle" at the decision level).

C_w = w · Q(LGB-Q) + (1 − w) · Q(TSB-NB), w ∈ {0, 0.1, …, 1}; C2 is w = 0.5. For each dataset:
  1. sensitivity: inventory needed at fill 0.90 / 0.92 / 0.94 relative to LGB-Q for every w and window;
  2. learned weight: w is chosen on the training window(s) to minimise the mean inventory needed at fill
     0.90–0.94 (relative to LGB-Q), then applied unchanged to the next window, with the same three transitions as
     growth_rule.py (third → second, second → main, third + second → main); compared with C2 and with LGB-Q,
     with 95% bootstrap CIs over series.
Writes code/outputs/combination_weights.md and .csv.

Usage:
    python code/combination_weights.py
"""
import os
import sys

import numpy as np
import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from combination import setup  # noqa: E402
from f2d import config, policy  # noqa: E402
from segment_eval import curve, inv_at  # noqa: E402

WINDOWS = {"third": 52, "second": 26, "main": 0}
TRANSITIONS = [(("third",), "second"), (("second",), "main"), (("third", "second"), "main")]
WEIGHTS = tuple(np.round(np.arange(0, 1.01, 0.1), 1))
EVAL = (0.90, 0.92, 0.94)
N_BOOT = 200
H = 3


def totals_for(d, off):
    """Per-series totals over the τ grid for every weight w (keys 'w0.0' … 'w1.0'); w1.0 = LGB-Q, w0.0 = TSB-NB."""
    p, idx, test0, T = setup(d, off)
    L = config.DEFAULT["L"]
    D = np.nan_to_num(p["Y"][:, test0:T]).astype(np.float64)[idx]
    w_ = slice(config.WARMUP_WEEKS, None)
    fc = os.path.join(config.CACHE, "forecasts", d + (f"_w{off}" if off else ""))
    A = np.load(os.path.join(fc, f"lgb_quantile_h{H}.npz"))["Q"][idx]
    B = np.load(os.path.join(fc, f"tsb_nb_h{H}.npz"))["Q"][idx]
    qs = list(config.QUANTILES)
    tot = {"demand": D[:, w_].sum(1)}
    for w in WEIGHTS:
        Q = w * A + (1 - w) * B
        for tau in config.TAU_GRID:
            S = Q[:, :, qs.index(tau)]
            sim = policy.simulate(D, S, np.full_like(S, np.inf), L)
            tot[f"w{w}", tau, "sales"] = sim["sales"][:, w_].sum(1)
            tot[f"w{w}", tau, "onhand"] = sim["on_hand_end"][:, w_].sum(1)
    return tot


def rel(tot, w, idx=None):
    """Inventory needed relative to LGB-Q (w = 1) at the EVAL targets."""
    n = len(tot["demand"])
    a, b = curve(tot, np.array([f"w{w}"] * n), idx), curve(tot, np.array(["w1.0"] * n), idx)
    return np.array([inv_at(*a, t) / inv_at(*b, t) - 1 for t in EVAL])


def main():
    rng = np.random.default_rng(config.SEED)
    sens, learn = [], []
    for d in ("M5", "VN1"):
        tots = {}
        for wname, off in WINDOWS.items():
            tots[wname] = totals_for(d, off)
            for w in WEIGHTS:
                r = rel(tots[wname], w)
                sens.append(dict(dataset=d, window=wname, w=w, **{f"rel_{t:.2f}": v for t, v in zip(EVAL, r)}))
            print(d, wname, "simulated", flush=True)
        for train, test in TRANSITIONS:
            score = {w: np.nanmean([np.nanmean(rel(tots[tw], w)) for tw in train]) for w in WEIGHTS}
            w_star = min(score, key=lambda k: (np.inf if np.isnan(score[k]) else score[k]))
            tt = tots[test]
            n = len(tt["demand"])
            boots = [rng.integers(0, n, n) for _ in range(N_BOOT)]
            row = dict(dataset=d, transition=" + ".join(train) + " → " + test, learned_w=w_star)
            for lab, w in (("learned", w_star), ("C2", 0.5)):
                point = rel(tt, w)
                bs = np.array([rel(tt, w, b) for b in boots])
                for k, t in enumerate(EVAL):
                    ok = np.isfinite(bs[:, k])
                    row[f"{lab}_{t:.2f}"] = point[k]
                    row[f"{lab}_{t:.2f}_lo"], row[f"{lab}_{t:.2f}_hi"] = (np.percentile(bs[ok, k], [2.5, 97.5]) if ok.mean() >= 0.95
                                                                          else (np.nan, np.nan))
            # learned vs C2 directly
            a = np.array([[inv_at(*curve(tt, np.array([f"w{w_star}"] * n), b), t) / inv_at(*curve(tt, np.array(["w0.5"] * n), b), t) - 1
                           for t in EVAL] for b in boots])
            p0 = [inv_at(*curve(tt, np.array([f"w{w_star}"] * n)), t) / inv_at(*curve(tt, np.array(["w0.5"] * n)), t) - 1 for t in EVAL]
            for k, t in enumerate(EVAL):
                ok = np.isfinite(a[:, k])
                row[f"learned_vs_C2_{t:.2f}"] = p0[k]
                row[f"learned_vs_C2_{t:.2f}_lo"], row[f"learned_vs_C2_{t:.2f}_hi"] = (np.percentile(a[ok, k], [2.5, 97.5]) if ok.mean() >= 0.95
                                                                                      else (np.nan, np.nan))
            learn.append(row)
            print(d, row["transition"], "learned w =", w_star, flush=True)
    sens, learn = pd.DataFrame(sens), pd.DataFrame(learn)
    sens.to_csv(os.path.join(config.OUTPUTS, "combination_weights_sensitivity.csv"), index=False)
    learn.to_csv(os.path.join(config.OUTPUTS, "combination_weights.csv"), index=False)

    def cell(r, key):
        v, lo, hi = r[key], r.get(key + "_lo", np.nan), r.get(key + "_hi", np.nan)
        if not np.isfinite(v):
            return "—"
        return f"{100 * v:+.1f}" + (f" [{100 * lo:+.1f}, {100 * hi:+.1f}]" if np.isfinite(lo) else "")
    lines = ["# Learned vs equal combination weight (generated by code/combination_weights.py)", "",
             "C_w = w · LGB-Q + (1 − w) · TSB-NB (quantile averaging); C2 = w 0.5. h = 3, L = 2, no liquidation. "
             "Δ in % with 95% bootstrap CI over series.", "",
             "## 1. Learned weight applied to the next window", "",
             "| dataset | transition | learned w | learned vs LGB-Q, fill 0.92 | C2 vs LGB-Q, fill 0.92 | learned vs C2, 0.90 | learned vs C2, 0.92 | learned vs C2, 0.94 |",
             "|---|---|---|---|---|---|---|---|"]
    for _, r in learn.iterrows():
        lines.append(f"| {r.dataset} | {r.transition} | {r.learned_w:.1f} | {cell(r, 'learned_0.92')} | {cell(r, 'C2_0.92')} | "
                     f"{cell(r, 'learned_vs_C2_0.90')} | {cell(r, 'learned_vs_C2_0.92')} | {cell(r, 'learned_vs_C2_0.94')} |")
    lines += ["", "## 2. Sensitivity: inventory relative to LGB-Q at fill 0.92 (%) for every weight w", ""]
    piv = (100 * sens.pivot_table(index=["dataset", "window"], columns="w", values="rel_0.92")).round(1)
    lines += [piv.to_markdown(), ""]
    with open(os.path.join(config.OUTPUTS, "combination_weights.md"), "w", encoding="utf-8") as fh:
        fh.write("\n".join(lines))
    print("written code/outputs/combination_weights.md")


if __name__ == "__main__":
    main()
