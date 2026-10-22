"""P0-2: do the paper's "interval excludes zero" claims survive cluster and block bootstraps?
(design: phase5_workflow.md, section 8)

For each dataset × window, the policy is simulated once per method × τ grid point. Resampling units:
    series        each series (the paper's bootstrap; reference)
    cluster       M5: item (3,049) and store (10, few clusters — reported only); VN1: warehouse (328) and client (46)
    week-block    circular blocks of 4 of the 22 evaluation weeks, all series kept
1,000 resamples each. For every resample the inventory–fill curve is rebuilt and the inventory at fill 0.92 / 0.94 is
interpolated; Δ = I_method / I_LGB-Q − 1. Claims checked are those stated with intervals in the paper.
Writes code/outputs/robustness/bootstrap_robust.md and .csv.

Usage:
    python code/bootstrap_robust.py
"""
import os
import sys

import numpy as np
import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from f2d import config  # noqa: E402
from robust_common import LAB, METHODS, WINDOWS, load_window, run  # noqa: E402

N_BOOT = 1000
BLOCK = 4
CLUSTERS = {"M5": ["item_id", "store_id"], "VN1": ["client_wh", "Client"]}
QS = list(config.QUANTILES)
# (dataset, window or None = all, method, fill, expected sign of Δ vs LGB-Q)
CLAIMS = ([("M5", None, m, 0.94, +1) for m in ("lgb_tweedie", "lgb_conformal", "tsb_nb", "ets")] +
          [("VN1", "second", m, 0.94, -1) for m in ("tsb_nb", "lgb_tweedie", "lgb_conformal")] +
          [("VN1", None, m, 0.92, -1) for m in ("E7-med", "C2")])


def inv_at_many(F, I, target):
    """F, I: [B, n_tau] -> inventory at target per row (NaN if not reached)."""
    F = np.maximum.accumulate(F, axis=1)
    out = np.full(F.shape[0], np.nan)
    for b in range(F.shape[0]):
        if F[b, 0] <= target <= F[b, -1]:
            out[b] = np.interp(target, F[b], I[b])
    return out


def resample(units_sales, units_onh, units_dem, draws):
    """units_*: [U, K] (K = methods × τ) and [U]; draws: [B, U] counts. Returns fill and inventory [B, K]."""
    dem = draws @ units_dem
    return (draws @ units_sales) / dem[:, None], (draws @ units_onh) / dem[:, None]


def counts(rng, U, B, chunk=None):
    return np.stack([np.bincount(rng.integers(0, U, U), minlength=U) for _ in range(B)]).astype(np.float64)


def block_counts(rng, W, B):
    nb = int(np.ceil(W / BLOCK))
    C = np.zeros((B, W))
    for b in range(B):
        for s in rng.integers(0, W, nb):
            for k in range(BLOCK):
                C[b, (s + k) % W] += 1
    return C * W / (nb * BLOCK)


def main():
    rng = np.random.default_rng(config.SEED)
    out = os.path.join(config.OUTPUTS, "robustness")
    os.makedirs(out, exist_ok=True)
    rows = []
    for d in ("M5", "VN1"):
        for wname, off in WINDOWS.items():
            w = load_window(d, off)
            D = w["D"]
            keys = [(m, t) for m in METHODS for t in config.TAU_GRID]
            n, Wn = D.shape[0], D[:, config.WARMUP_WEEKS:].shape[1]
            ser_s, ser_o = np.zeros((n, len(keys))), np.zeros((n, len(keys)))
            wk_s, wk_o = np.zeros((Wn, len(keys))), np.zeros((Wn, len(keys)))
            for k, (m, t) in enumerate(keys):
                s, o = run(D, w["Q"][m][:, :, QS.index(t)])
                ser_s[:, k], ser_o[:, k] = s.sum(1), o.sum(1)
                wk_s[:, k], wk_o[:, k] = s.sum(0), o.sum(0)
            dem_ser, dem_wk = D[:, config.WARMUP_WEEKS:].sum(1), D[:, config.WARMUP_WEEKS:].sum(0)
            attrs = w["p"]["attrs"].iloc[w["idx"]].reset_index(drop=True)
            schemes = {"series": None}
            for c in CLUSTERS[d]:
                schemes["cluster:" + c] = pd.factorize(attrs[c])[0]
            schemes["week-block"] = "weeks"
            for name, grp in schemes.items():
                if grp is None:
                    Fs, Is = [], []
                    for _ in range(N_BOOT // 100):
                        C = counts(rng, n, 100)
                        f, i = resample(ser_s, ser_o, dem_ser, C)
                        Fs.append(f), Is.append(i)
                    F, I = np.vstack(Fs), np.vstack(Is)
                elif isinstance(grp, str):
                    F, I = resample(wk_s, wk_o, dem_wk, block_counts(rng, Wn, N_BOOT))
                else:
                    G = grp.max() + 1
                    agg = lambda A: np.vstack([np.bincount(grp, weights=A[:, k], minlength=G) for k in range(A.shape[1])]).T
                    cs, co, cd = agg(ser_s), agg(ser_o), np.bincount(grp, weights=dem_ser, minlength=G)
                    F, I = resample(cs, co, cd, counts(rng, G, N_BOOT))
                nt = len(config.TAU_GRID)
                for (cd_, cw, m, fill, sign) in CLAIMS:
                    if cd_ != d or (cw is not None and cw != wname):
                        continue
                    km, kr = METHODS.index(m) * nt, METHODS.index("lgb_quantile") * nt
                    a = inv_at_many(F[:, km:km + nt], I[:, km:km + nt], fill)
                    r = inv_at_many(F[:, kr:kr + nt], I[:, kr:kr + nt], fill)
                    x = a / r - 1
                    ok = np.isfinite(x)
                    lo, hi = (np.percentile(x[ok], [2.5, 97.5]) if ok.mean() >= 0.95 else (np.nan, np.nan))
                    rows.append(dict(dataset=d, window=wname, method=LAB[m], fill=fill, scheme=name,
                                     n_units=(n if grp is None else Wn if isinstance(grp, str) else int(grp.max() + 1)),
                                     lo=lo, hi=hi, reached_share=ok.mean(),
                                     holds=bool(np.isfinite(lo) and (lo > 0 if sign > 0 else hi < 0))))
            print(d, wname, "done", flush=True)
    res = pd.DataFrame(rows)
    res.to_csv(os.path.join(out, "bootstrap_robust.csv"), index=False)
    L = ["# Cluster and block bootstraps of the paper's interval claims (generated by code/bootstrap_robust.py)", "",
         f"{N_BOOT} resamples per scheme. Δ = I_method / I_LGB-Q − 1 (%), 95% percentile interval. 'holds' = interval "
         "excludes zero in the claimed direction. Store-level clusters on M5 (10) are too few for reliable intervals.", ""]
    piv = res.assign(ci=[("—" if not np.isfinite(r.lo) else f"[{100 * r.lo:+.1f}, {100 * r.hi:+.1f}]") + (" ✓" if r.holds else " ✗")
                         for r in res.itertuples()])
    for (d, m, fill), g in piv.groupby(["dataset", "method", "fill"], sort=False):
        t = g.pivot(index="window", columns="scheme", values="ci").reindex(["main", "second", "third"]).dropna(how="all")
        L += [f"## {d} · {m} vs LGB-Q · fill {fill}", "", t.to_markdown(), ""]
    summ = res.groupby("scheme").holds.agg(["sum", "count"])
    L += ["## Claims holding per scheme", "", summ.to_markdown(), ""]
    with open(os.path.join(out, "bootstrap_robust.md"), "w", encoding="utf-8") as fh:
        fh.write("\n".join(L))
    print("written", os.path.join(out, "bootstrap_robust.md"))


if __name__ == "__main__":
    main()
