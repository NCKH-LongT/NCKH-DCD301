"""Censoring check for the seven-method combinations (follow-up to censoring_rank_check.py, which covered C2 only).

Same detector (censoring_check.flag_weeks), same three evaluations and the same α values as censoring_rank_check.py:
    base     all eligible series, recorded sales as demand
    clean    only series without a suspected stock-out week in the test window
    imputed  suspected weeks set to max(sales, the series' mean weekly sales before the test period)
Methods: the seven single methods, C2, E7 (mean of seven) and E7-med (median of seven). Cached h = 3 forecasts,
default policy (L = 2, no liquidation). Reported: Δ vs LGB-Q at fill 0.92 / 0.94 with 95% bootstrap CIs (200
resamples of series) and regret over the best of the seven single methods (mean over reached targets 0.90–0.98).
Writes code/outputs/censoring/censoring_rank_check_e7.md and .csv.

Usage:
    python code/censoring_rank_check_e7.py
"""
import os
import sys

import numpy as np
import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from censoring_check import flag_weeks  # noqa: E402
from censoring_rank_check import ALPHAS, EVAL, H, N_BOOT, WINDOWS, simulate_all  # noqa: E402
from f2d import classify, config, data  # noqa: E402
from segment_eval import MODELS, TARGETS, curve, inv_at  # noqa: E402

COMBOS = ["C2", "E7", "E7-med"]
LAB = {"empirical": "EMP", "tsb_nb": "TSB-NB", "ets": "ETS", "lgb_tweedie": "LGB-T", "lgb_conformal": "LGB-C",
       "hgb_quantile": "HGB-Q", "lgb_quantile": "LGB-Q", "C2": "C2", "E7": "E7", "E7-med": "E7-med"}


def evaluate(tot, n, idx, rng, label):
    methods = MODELS + COMBOS
    curves = {m: curve(tot, np.array([m] * n), idx) for m in methods}
    need = pd.DataFrame({m: [inv_at(*curves[m], t) for t in TARGETS] for m in methods}, index=TARGETS)
    best = need[MODELS].min(axis=1)
    m_idx = np.arange(n) if idx is None else idx
    boots = [rng.choice(m_idx, len(m_idx), replace=True) for _ in range(N_BOOT)]
    bc = {m: [curve(tot, np.array([m] * n), b) for b in boots] for m in ["lgb_quantile"] + COMBOS}
    rows = []
    for m in methods:
        r = dict(eval=label, method=LAB[m], n_series=len(m_idx), regret=(need[m] / best - 1).mean(skipna=True))
        if m in COMBOS:
            for tg in EVAL:
                v, ref = inv_at(*curves[m], tg), inv_at(*curves["lgb_quantile"], tg)
                x = np.array([inv_at(*bc[m][k], tg) / inv_at(*bc["lgb_quantile"][k], tg) - 1 for k in range(N_BOOT)])
                ok = np.isfinite(x)
                r[f"d_{tg:.2f}"] = v / ref - 1 if np.isfinite(v) and np.isfinite(ref) else np.nan
                r[f"lo_{tg:.2f}"], r[f"hi_{tg:.2f}"] = (np.percentile(x[ok], [2.5, 97.5]) if ok.mean() >= 0.95
                                                        else (np.nan, np.nan))
        rows.append(r)
    return rows


def main():
    rng = np.random.default_rng(config.SEED)
    rows = []
    for d in ("M5", "VN1"):
        base_panel = data.load(d)
        for wname, off in WINDOWS.items():
            p = data.truncate(base_panel, base_panel["Y"].shape[1] - off) if off else base_panel
            Y = p["Y"].astype(np.float64)
            T = Y.shape[1]
            test0 = T - config.TEST_WEEKS
            start = p["start"].astype(int)
            sel = start <= test0 - config.VALID_WEEKS
            cls, _, _ = classify.classify(Y, p["start"], test0)
            sel &= cls != "none"
            idx = np.flatnonzero(sel)
            n = len(idx)
            D = np.nan_to_num(Y[:, test0:T])[idx]
            t = np.arange(T)[None, :]
            hist = (t >= start[:, None]) & (t < test0)
            rate = ((np.nan_to_num(Y) * hist).sum(1) / np.maximum(hist.sum(1), 1))[idx]
            fc = os.path.join(config.CACHE, "forecasts", d + (f"_w{off}" if off else ""))
            Q = {m: np.load(os.path.join(fc, f"{m}_h{H}.npz"))["Q"][idx] for m in MODELS}
            Q["C2"] = (Q["lgb_quantile"] + Q["tsb_nb"]) / 2
            Q["E7"] = np.mean([Q[m] for m in MODELS], 0)
            Q["E7-med"] = np.median([Q[m] for m in MODELS], 0)
            tot = simulate_all(Q, D)
            for r in evaluate(tot, n, None, rng, "base"):
                rows.append(dict(dataset=d, window=wname, alpha=np.nan, **r))
            for alpha in ALPHAS:
                F, _ = flag_weeks(Y, start, test0, alpha)
                Ft = F[idx][:, test0:T]
                clean = np.flatnonzero(~Ft.any(1))
                for r in evaluate(tot, n, clean, rng, "clean"):
                    rows.append(dict(dataset=d, window=wname, alpha=alpha, **r))
                tot_imp = simulate_all(Q, np.where(Ft, np.maximum(D, rate[:, None]), D))
                for r in evaluate(tot_imp, n, None, rng, "imputed"):
                    rows.append(dict(dataset=d, window=wname, alpha=alpha, **r))
                print(d, wname, "alpha", alpha, f"clean {len(clean):,}/{n:,}", flush=True)
    res = pd.DataFrame(rows)
    out = os.path.join(config.OUTPUTS, "censoring")
    res.to_csv(os.path.join(out, "censoring_rank_check_e7.csv"), index=False)

    def cell(r, tg):
        v, lo, hi = r.get(f"d_{tg:.2f}", np.nan), r.get(f"lo_{tg:.2f}", np.nan), r.get(f"hi_{tg:.2f}", np.nan)
        if not np.isfinite(v):
            return "—"
        return f"{100 * v:+.1f}" + (f" [{100 * lo:+.1f}, {100 * hi:+.1f}]" if np.isfinite(lo) else "")
    L = ["# Suspected stock-outs and the seven-method combinations (generated by code/censoring_rank_check_e7.py)", "",
         "Same detector and evaluations as censoring_rank_check.md. Δ vs LGB-Q in % with 95% bootstrap CI "
         "(negative = less stock than LGB-Q). Regret over the best of the seven single methods.", ""]
    for alpha in ALPHAS:
        sub = res[(res.alpha == alpha) | res.alpha.isna()]
        L += [f"## α = {alpha}", "", "### Δ vs LGB-Q (%)", "", "| dataset | window | eval | method | fill 0.92 | fill 0.94 |",
              "|---|---|---|---|---|---|"]
        for _, r in sub[sub.method.isin(COMBOS)].iterrows():
            L.append(f"| {r.dataset} | {r.window} | {r['eval']} | {r.method} | {cell(r, 0.92)} | {cell(r, 0.94)} |")
        piv = sub.pivot_table(index="method", columns="eval", values="regret", aggfunc="max")
        L += ["", "### Maximum regret over the six runs (%)", "", (100 * piv).round(1).sort_values("base").to_markdown(), ""]
    with open(os.path.join(out, "censoring_rank_check_e7.md"), "w", encoding="utf-8") as fh:
        fh.write("\n".join(L))
    print("written code/outputs/censoring/censoring_rank_check_e7.md")


if __name__ == "__main__":
    main()
