"""Method selection by predicted demand growth (extension for the journal version).

Idea (from demand_shift_analysis.py): a statistical model is more economical for series whose demand stays stable,
a quantile model for series whose demand grows. Growth is unknown at decision time, so it is predicted.

Protocol, per dataset and per transition (training window → next window); nothing of the next window is used
before it is evaluated:
  1. Label the series of the training window by realised growth (test demand > 1.5 × the previous 26 weeks).
  2. Fit a classifier on the pre-test features of the training window (9 shared features).
  3. On the training window choose A = most inventory-efficient method for the growing stratum, B = the same for
     the other series, and the threshold θ on the out-of-fold growth probability that minimises the inventory of
     the composite policy (A if p ≥ θ else B) at fill rate 0.92.
  4. Apply classifier, A, B and θ to the next window; compare the composite policy with always using LGB-Q at
     equal fill rate, with bootstrap confidence intervals over series.
Also reported: the out-of-sample AUC of the growth classifier, and an oracle that knows the realised stratum.
Writes code/outputs/growth_rule.md and .csv.

Usage:
    python code/growth_rule.py
"""
import os
import sys

import numpy as np
import pandas as pd
from sklearn.ensemble import HistGradientBoostingClassifier
from sklearn.metrics import roc_auc_score
from sklearn.model_selection import StratifiedKFold, cross_val_predict

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from equal_fill_ci import totals  # noqa: E402
from f2d import classify, config, data  # noqa: E402
from f2d.series_features import SHARED  # noqa: E402
from segment_eval import MODELS, curve, group_leader, inv_at  # noqa: E402

WINDOWS = {"w52": 52, "w26": 26, "main": 0}
TRANSITIONS = [(("w52",), "w26"), (("w26",), "main"), (("w52", "w26"), "main")]
SELECT_TARGET = 0.92
EVAL_TARGETS = (0.90, 0.92, 0.94)
SHARES = (0.05, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7)       # candidate shares of series sent to the growth method
N_BOOT = 200
GROW = 1.5


def realised_growth(name, offset):
    """Boolean per evaluated series (same order as totals()): test demand > 1.5 × demand of the previous 26 weeks."""
    p = data.load(name)
    if offset:
        p = data.truncate(p, p["Y"].shape[1] - offset)
    Y = p["Y"]
    T = Y.shape[1]
    test0 = T - config.TEST_WEEKS
    sel = p["start"] <= test0 - config.VALID_WEEKS
    cls, _, _ = classify.classify(Y, p["start"], test0)
    sel &= cls != "none"
    Y0 = np.nan_to_num(Y)[sel]
    prev = Y0[:, test0 - 26:test0].sum(1)
    test = Y0[:, test0 + config.WARMUP_WEEKS:T].sum(1) * 26 / (config.TEST_WEEKS - config.WARMUP_WEEKS)
    ratio = np.where(prev > 0, test / np.maximum(prev, 1e-9), np.where(test > 0, np.inf, 1.0))
    return ratio > GROW


def clf():
    return HistGradientBoostingClassifier(max_iter=200, learning_rate=0.1, random_state=config.SEED)


def composite(tot, p, theta, A, B):
    return np.where(p >= theta, A, B)


def main():
    rng = np.random.default_rng(config.SEED)
    res, info, sens = [], [], []
    for d in ("M5", "VN1"):
        W = {}
        for w, off in WINDOWS.items():
            F = pd.read_parquet(os.path.join(config.CACHE, f"series_features_{d}_{w}.parquet"))
            tot = totals(d, off, MODELS)
            g = realised_growth(d, off)
            assert len(F) == len(g) == len(tot["demand"])
            W[w] = (F[SHARED].to_numpy(float), g, tot)
            print(d, w, "loaded; growing share", round(g.mean(), 3), flush=True)
        for train, test in TRANSITIONS:
            # ---- learn on the training window(s)
            oof, choice = [], []
            for w in train:
                X, g, tot = W[w]
                p = cross_val_predict(clf(), X, g, cv=StratifiedKFold(5, shuffle=True, random_state=config.SEED),
                                      method="predict_proba")[:, 1]
                oof.append((w, p))
            # A and B from realised strata of the (last) training window; θ by composite inventory on all training windows
            Xl, gl, totl = W[train[-1]]
            A = group_leader(totl, gl)[0] or "lgb_quantile"
            B = group_leader(totl, ~gl)[0] or "lgb_quantile"
            best = (np.inf, None)
            for share in SHARES:
                cost = 0.0
                for w, p in oof:
                    theta = np.quantile(p, 1 - share)
                    f, i = curve(W[w][2], composite(W[w][2], p, theta, A, B))
                    v = inv_at(f, i, SELECT_TARGET)
                    cost += v if np.isfinite(v) else np.inf
                if cost < best[0]:
                    best = (cost, share)
            share = best[1] if best[1] is not None else 0.3
            single = group_leader(totl, np.ones(len(gl), bool))[0]
            model = clf().fit(np.vstack([W[w][0] for w in train]), np.concatenate([W[w][1] for w in train]))
            # ---- apply to the next window
            Xt, gt, tott = W[test]
            pt = model.predict_proba(Xt)[:, 1]
            theta = np.quantile(pt, 1 - share)
            auc = roc_auc_score(gt, pt)
            n = len(gt)
            rules = {"always LGB-Q": np.array(["lgb_quantile"] * n),
                     "always TSB-NB": np.array(["tsb_nb"] * n),
                     "best single method of the training window": np.array([single] * n),
                     "growth rule (predicted)": composite(tott, pt, theta, A, B),
                     "oracle (realised growth, not usable)": np.where(gt, A, B)}
            curves = {r: curve(tott, m) for r, m in rules.items()}
            boots = [rng.integers(0, n, n) for _ in range(N_BOOT)]
            bc = {r: [curve(tott, m, b) for b in boots] for r, m in rules.items()}
            tr = " + ".join(train) + " → " + test
            info.append(dict(dataset=d, transition=tr, growth_method=A, stable_method=B, share_to_growth_method=share,
                             best_single=single, auc_next_window=auc, growing_share_next=gt.mean(),
                             flagged_growing_precision=gt[pt >= theta].mean(), recall=(gt & (pt >= theta)).sum() / gt.sum()))
            # sensitivity: the same classifier and methods with every candidate share (not used for selection)
            ref92 = inv_at(*curves["always LGB-Q"], SELECT_TARGET)
            srow = dict(dataset=d, transition=tr, A=A, B=B, chosen_share=f"{share:.2f}")
            for sh in SHARES:
                v = inv_at(*curve(tott, composite(tott, pt, np.quantile(pt, 1 - sh), A, B)), SELECT_TARGET)
                srow[f"share {sh:.2f}"] = 100 * (v / ref92 - 1) if np.isfinite(v) else np.nan
            sens.append(srow)
            for r in rules:
                row = dict(dataset=d, transition=tr, rule=r)
                for tg in EVAL_TARGETS:
                    v, ref = inv_at(*curves[r], tg), inv_at(*curves["always LGB-Q"], tg)
                    rel = np.array([inv_at(*bc[r][k], tg) / inv_at(*bc["always LGB-Q"][k], tg) - 1 for k in range(N_BOOT)])
                    ok = np.isfinite(rel)
                    row[f"inv_{tg:.2f}"] = v
                    row[f"rel_{tg:.2f}"] = v / ref - 1 if np.isfinite(v) and np.isfinite(ref) else np.nan
                    row[f"lo_{tg:.2f}"], row[f"hi_{tg:.2f}"] = (np.percentile(rel[ok], [2.5, 97.5]) if ok.mean() >= 0.95 else (np.nan, np.nan))
                res.append(row)
            print(d, tr, "done: A =", A, "B =", B, "share =", share, "AUC =", round(auc, 3), flush=True)
    res, info = pd.DataFrame(res), pd.DataFrame(info)
    res.to_csv(os.path.join(config.OUTPUTS, "growth_rule.csv"), index=False)

    def cell(r, tg):
        v, rel, lo, hi = r[f"inv_{tg:.2f}"], r[f"rel_{tg:.2f}"], r[f"lo_{tg:.2f}"], r[f"hi_{tg:.2f}"]
        if not np.isfinite(v):
            return "—"
        return f"{v:.2f} ({100 * rel:+.1f}%" + (f" [{100 * lo:+.1f}, {100 * hi:+.1f}])" if np.isfinite(lo) else ")")
    lines = ["# Method selection by predicted demand growth (generated by code/growth_rule.py)", "",
             "Growing = test demand > 1.5 × demand of the previous 26 weeks. The classifier, the two methods (A for predicted "
             "growth, B otherwise) and the share of series sent to A are all learned on the training window(s).", "",
             "## 1. What was learned, and how well growth is predicted in the next window", "",
             info.round(3).to_markdown(index=False), "",
             "## 2. Inventory (weeks of demand) at equal fill rate in the next window",
             "", "In brackets: difference to always using LGB-Q with a 95% bootstrap CI over series (negative = less inventory).", ""]
    for (d, tr), g in res.groupby(["dataset", "transition"], sort=False):
        lines += [f"### {d}, {tr}", "", "| rule | fill 0.90 | fill 0.92 | fill 0.94 |", "|---|---|---|---|"]
        lines += [f"| {r.rule} | {cell(r, 0.90)} | {cell(r, 0.92)} | {cell(r, 0.94)} |" for _, r in g.iterrows()]
        lines.append("")
    lines += ["## 3. Sensitivity to the share of series sent to the growth method (next window, fill rate 0.92)", "",
              "Difference to always using LGB-Q in %, point estimates. The share actually selected on the training window is "
              "in the column chosen_share; the other columns show what every other share would have given.", "",
              pd.DataFrame(sens).round(1).to_markdown(index=False), ""]
    with open(os.path.join(config.OUTPUTS, "growth_rule.md"), "w", encoding="utf-8") as fh:
        fh.write("\n".join(lines))
    print("written code/outputs/growth_rule.md")


if __name__ == "__main__":
    main()
