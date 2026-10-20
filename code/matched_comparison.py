"""B2b — do the M5 / VN1 conclusions converge once the two datasets have the same composition of series?

The datasets differ in the kind of series they contain (dataset_shift.py). Instead of altering the data, the
series of one dataset are re-weighted so that the distribution of their pre-test features matches the other
dataset (inverse-propensity weighting with the "M5 or VN1?" classifier, out-of-fold probabilities):
    VN1 → M5 :  w_i = (1 − p_i) / p_i      for VN1 series     (p_i = P(VN1 | features))
    M5 → VN1 :  w_i = p_i / (1 − p_i)      for M5 series
Weights are clipped at their 99th percentile and normalised to mean 1. Reported per test window:
    balance      standardised mean difference of every feature before / after weighting, effective sample size
    inventory    frontier rank and inventory needed at fill 0.92 / 0.94 from weighted totals (7 methods, no TSB-P)
    accuracy     weighted share of series on which LGB-Q has a lower SQL than TSB-NB (h = 3, 13), weighted wQL
Only cached forecasts are used. Writes code/outputs/matched_comparison.md and .csv.

Usage:
    python code/matched_comparison.py
"""
import os
import sys

import numpy as np
import pandas as pd
from sklearn.ensemble import HistGradientBoostingClassifier
from sklearn.model_selection import StratifiedKFold, cross_val_predict

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from analyze_results import frontier_rank  # noqa: E402
from equal_fill_ci import totals  # noqa: E402
from f2d import config  # noqa: E402
from f2d.series_features import SHARED  # noqa: E402

MODELS = ["empirical", "tsb_nb", "ets", "lgb_tweedie", "lgb_conformal", "hgb_quantile", "lgb_quantile"]
TARGETS = (0.90, 0.92, 0.94, 0.96, 0.98)
OFFSETS = (0, 26, 52)
CLIP_PCT = 99


def needed(tot, w):
    dem = (w * tot["demand"]).sum()
    rows = {}
    for m in MODELS:
        f_ = np.array([(w * tot[m, t, "sales"]).sum() / dem for t in config.TAU_GRID])
        i_ = np.array([(w * tot[m, t, "onhand"]).sum() / dem for t in config.TAU_GRID])
        f_ = np.maximum.accumulate(f_)
        rows[m] = {t: (np.interp(t, f_, i_) if f_.min() <= t <= f_.max() else np.nan) for t in TARGETS}
    return pd.DataFrame(rows).T


def smd(a, b, wa, wb):
    """Standardised mean difference of a feature between two weighted samples (NaNs ignored)."""
    oa, ob = np.isfinite(a), np.isfinite(b)
    ma, mb = np.average(a[oa], weights=wa[oa]), np.average(b[ob], weights=wb[ob])
    sd = np.sqrt((np.var(a[oa]) + np.var(b[ob])) / 2)
    return (mb - ma) / sd if sd > 0 else np.nan


def main():
    out, bal, acc = [], [], []
    for off in OFFSETS:
        win = f"w{off}" if off else "main"
        sfx = f"_w{off}" if off else ""
        F = {d: pd.read_parquet(os.path.join(config.CACHE, f"series_features_{d}_{win}.parquet")) for d in ("M5", "VN1")}
        S = {d: pd.read_parquet(os.path.join(config.CACHE, f"series_metrics_{d}{sfx}.parquet")) for d in ("M5", "VN1")}
        X = pd.concat([F["M5"][SHARED], F["VN1"][SHARED]], ignore_index=True).to_numpy(float)
        y = np.r_[np.zeros(len(F["M5"])), np.ones(len(F["VN1"]))]
        clf = HistGradientBoostingClassifier(max_iter=200, learning_rate=0.1, class_weight="balanced", random_state=config.SEED)
        p = cross_val_predict(clf, X, y, cv=StratifiedKFold(5, shuffle=True, random_state=config.SEED), method="predict_proba")[:, 1]
        p = np.clip(p, 1e-3, 1 - 1e-3)
        pm, pv = p[y == 0], p[y == 1]

        def norm(w):
            w = np.minimum(w, np.percentile(w, CLIP_PCT))
            return w / w.mean()
        W = {("M5", "original"): np.ones(len(pm)), ("VN1", "original"): np.ones(len(pv)),
             ("VN1", "reweighted to M5"): norm((1 - pv) / pv), ("M5", "reweighted to VN1"): norm(pm / (1 - pm))}
        T = {d: totals(d, off, MODELS) for d in ("M5", "VN1")}
        for d in ("M5", "VN1"):
            assert len(T[d]["demand"]) == len(F[d]) == len(S[d]), "series order mismatch"

        # balance
        for c in SHARED:
            a, b = F["M5"][c].to_numpy(float), F["VN1"][c].to_numpy(float)
            bal.append(dict(window=win, feature=c, SMD_original=smd(a, b, W["M5", "original"], W["VN1", "original"]),
                            SMD_VN1_to_M5=smd(a, b, W["M5", "original"], W["VN1", "reweighted to M5"]),
                            SMD_M5_to_VN1=smd(a, b, W["M5", "reweighted to VN1"], W["VN1", "original"])))
        for (d, name), w in W.items():
            t = needed(T[d], w)
            fr = frontier_rank(t)
            ess = w.sum() ** 2 / (w ** 2).sum()
            for m in MODELS:
                out.append(dict(window=win, dataset=d, weighting=name, model=m, frontier_rank=fr[m], ess=ess, n=len(w),
                                **{f"inv_{k:.2f}": t.loc[m, k] for k in TARGETS}))
            s = S[d]
            r = dict(window=win, dataset=d, weighting=name, ess=ess)
            for h in (3, 13):
                a, b = s[f"lgb_quantile|SQL_h{h}"].to_numpy(float), s[f"tsb_nb|SQL_h{h}"].to_numpy(float)
                ok = np.isfinite(a) & np.isfinite(b)
                r[f"lgbq_better_h{h}"] = np.average((a < b)[ok], weights=w[ok])
            acc.append(r)
    out, bal, acc = pd.DataFrame(out), pd.DataFrame(bal), pd.DataFrame(acc)
    out.to_csv(os.path.join(config.OUTPUTS, "matched_comparison.csv"), index=False)

    order = [("M5", "original"), ("VN1", "reweighted to M5"), ("VN1", "original"), ("M5", "reweighted to VN1")]
    lines = ["# B2b — Composition-matched comparison of M5 and VN1 (generated by code/matched_comparison.py)", "",
             "Series are re-weighted (inverse propensity, 9 shared pre-test features) so that one dataset has the feature "
             "distribution of the other. 7 methods (TSB-P excluded). Frontier rank: 1 = least inventory over fill targets "
             "0.90–0.98.", "",
             "## 1. Does the weighting balance the features? (standardised mean difference VN1 − M5; |SMD| < 0.1 = balanced)", ""]
    b0 = bal[bal.window == "main"].drop(columns="window")
    lines += [b0.round(2).to_markdown(index=False), "",
              "Mean |SMD| over the 9 features: " + "; ".join(
                  f"{w}: original {g.SMD_original.abs().mean():.2f}, VN1→M5 {g.SMD_VN1_to_M5.abs().mean():.2f}, "
                  f"M5→VN1 {g.SMD_M5_to_VN1.abs().mean():.2f}" for w, g in bal.groupby("window", sort=False)), ""]
    lines += ["## 2. Frontier rank by method", ""]
    for win in [f"w{o}" if o else "main" for o in OFFSETS]:
        g = out[out.window == win]
        t = pd.DataFrame({f"{d} {n}": g[(g.dataset == d) & (g.weighting == n)].set_index("model").frontier_rank for d, n in order})
        ess = {f"{d} {n}": g[(g.dataset == d) & (g.weighting == n)].ess.iloc[0] for d, n in order}
        lines += [f"### Window {win}", "", t.loc[MODELS].round(2).to_markdown(), "",
                  "Effective sample size: " + "; ".join(f"{k}: {v:,.0f}" for k, v in ess.items()), ""]
    lines += ["## 3. Inventory needed at fill rate 0.92 and 0.94: LGB-Q vs TSB-NB vs LGB-T", "",
              "Δ = I_method / I_LGB-Q − 1 (positive = LGB-Q needs less). “—” = target not reached.", "",
              "| window | dataset, weighting | LGB-Q @0.92 | TSB-NB Δ @0.92 | LGB-T Δ @0.92 | LGB-Q @0.94 | TSB-NB Δ @0.94 | LGB-T Δ @0.94 | leader (frontier rank) |",
              "|---|---|---|---|---|---|---|---|---|"]

    def d_(a, b):
        return "—" if not (np.isfinite(a) and np.isfinite(b)) else f"{100 * (a / b - 1):+.1f}%"
    for win in [f"w{o}" if o else "main" for o in OFFSETS]:
        for d, n in order:
            g = out[(out.window == win) & (out.dataset == d) & (out.weighting == n)].set_index("model")
            q, tn, lt = g.loc["lgb_quantile"], g.loc["tsb_nb"], g.loc["lgb_tweedie"]
            lead = g.frontier_rank.idxmin()
            f = lambda v: "—" if not np.isfinite(v) else f"{v:.2f}"
            lines.append(f"| {win} | {d}, {n} | {f(q['inv_0.92'])} | {d_(tn['inv_0.92'], q['inv_0.92'])} | {d_(lt['inv_0.92'], q['inv_0.92'])} | "
                         f"{f(q['inv_0.94'])} | {d_(tn['inv_0.94'], q['inv_0.94'])} | {d_(lt['inv_0.94'], q['inv_0.94'])} | "
                         f"{lead} ({g.frontier_rank.min():.2f}) |")
    lines += ["", "## 4. Accuracy per series: weighted share of series where LGB-Q has a lower SQL than TSB-NB", "",
              acc.assign(lgbq_better_h3=(100 * acc.lgbq_better_h3).round(1), lgbq_better_h13=(100 * acc.lgbq_better_h13).round(1),
                         ess=acc.ess.round(0)).to_markdown(index=False), ""]
    with open(os.path.join(config.OUTPUTS, "matched_comparison.md"), "w", encoding="utf-8") as fh:
        fh.write("\n".join(lines))
    print("written code/outputs/matched_comparison.md")


if __name__ == "__main__":
    main()
