"""Ranking reversal between TSB-NB and LGB-Q on VN1, by warehouse (design: phase5_workflow.md, section 10, item 3).

Outcome per warehouse (client × warehouse with ≥ 20 eligible series): y = log(I_TSB-NB / I_LGB-Q), the inventory needed
for fill 0.92 within the warehouse (curve over the τ grid, default policy). y < 0 means TSB-NB needs less stock.
Predictors use only data before the test window (cached series features): medians over the warehouse's series of
recent growth (recent_ratio_13), 26-week trend, log ADI, CV², zero-week share, history length and log mean demand,
plus log number of series. Analyses:
    1. per window: Spearman correlation of y with each predictor (sign stability across the three windows);
    2. standardised OLS on the earlier window, prediction on the next (third → second, second → main, third+second →
       main): Spearman ρ between predicted and realised y, with a permutation p-value (2,000 permutations);
    3. decision value: in the target window, use TSB-NB in warehouses with predicted y < 0 and LGB-Q elsewhere;
       inventory at portfolio fill 0.92 relative to LGB-Q everywhere (retrospective oracle by warehouse for reference).
Test-window demand is never used as a predictor. Writes code/outputs/robustness/ranking_reversal.{md,csv}.

Usage:
    python code/ranking_reversal.py
"""
import os
import sys

import numpy as np
import pandas as pd
from scipy.stats import spearmanr

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from f2d import config  # noqa: E402
from robust_common import load_window, run  # noqa: E402
from segment_eval import inv_at  # noqa: E402

WINDOWS = [("third", 52, "w52"), ("second", 26, "w26"), ("main", 0, "main")]
METHODS = ("tsb_nb", "lgb_quantile")
TARGET = 0.92
MIN_SERIES = 20
QS = list(config.QUANTILES)
FEATS = ["recent_ratio_13", "trend_26", "log_adi", "cv2", "zero_share", "hist_len", "log_mean", "log_n"]


def window_data(off, tag):
    w = load_window("VN1", off)
    D = w["D"]
    attrs = w["p"]["attrs"].iloc[w["idx"]].reset_index(drop=True)
    sf = pd.read_parquet(os.path.join(config.CACHE, f"series_features_VN1_{tag}.parquet")).set_index("series_id")
    sf = sf.loc[attrs.series_id].reset_index(drop=True)
    dem = D[:, config.WARMUP_WEEKS:].sum(1)
    tot = {}
    for m in METHODS:
        for t in config.TAU_GRID:
            s, o = run(D, w["Q"][m][:, :, QS.index(t)])
            tot[m, t] = (s.sum(1), o.sum(1))
    wh = pd.factorize(attrs.client_wh)[0]
    return dict(attrs=attrs, sf=sf, dem=dem, tot=tot, wh=wh, whname=attrs.client_wh.to_numpy())


def curve_inv(tot, m, mask, dem):
    dd = dem[mask].sum()
    if dd <= 0:
        return np.nan
    f = np.maximum.accumulate(np.array([tot[m, t][0][mask].sum() / dd for t in config.TAU_GRID]))
    i = np.array([tot[m, t][1][mask].sum() / dd for t in config.TAU_GRID])
    return inv_at(f, i, TARGET)


def warehouse_table(W):
    rows = []
    for name in np.unique(W["whname"]):
        mask = W["whname"] == name
        if mask.sum() < MIN_SERIES:
            continue
        it, iq = curve_inv(W["tot"], "tsb_nb", mask, W["dem"]), curve_inv(W["tot"], "lgb_quantile", mask, W["dem"])
        sf = W["sf"][mask]
        rows.append(dict(warehouse=name, n=int(mask.sum()), y=np.log(it / iq) if np.isfinite(it) and np.isfinite(iq) else np.nan,
                         recent_ratio_13=sf.recent_ratio_13.median(), trend_26=sf.trend_26.median(),
                         log_adi=np.log(sf.adi).median(), cv2=sf.cv2.median(), zero_share=sf.zero_share.median(),
                         hist_len=sf.hist_len.median(), log_mean=sf.log_mean.median(), log_n=np.log(mask.sum())))
    return pd.DataFrame(rows)


def fit(train):
    tr = train.dropna(subset=["y"] + FEATS)
    mu, sd = tr[FEATS].mean(), tr[FEATS].std().replace(0, 1)
    X = np.c_[np.ones(len(tr)), ((tr[FEATS] - mu) / sd).to_numpy()]
    beta = np.linalg.lstsq(X, tr.y.to_numpy(), rcond=None)[0]
    return beta, mu, sd


def predict(model, df):
    beta, mu, sd = model
    X = np.c_[np.ones(len(df)), ((df[FEATS].fillna(mu) - mu) / sd).to_numpy()]
    return X @ beta


def portfolio_inv(W, use_tsb):
    """Inventory at portfolio fill 0.92 when the series of the warehouses in use_tsb use TSB-NB, the rest LGB-Q."""
    tsb = np.isin(W["whname"], list(use_tsb))
    dd = W["dem"].sum()
    f, i = [], []
    for t in config.TAU_GRID:
        s = np.where(tsb, W["tot"]["tsb_nb", t][0], W["tot"]["lgb_quantile", t][0]).sum()
        o = np.where(tsb, W["tot"]["tsb_nb", t][1], W["tot"]["lgb_quantile", t][1]).sum()
        f.append(s / dd), i.append(o / dd)
    return inv_at(np.maximum.accumulate(np.array(f)), np.array(i), TARGET)


def main():
    rng = np.random.default_rng(config.SEED)
    out = os.path.join(config.OUTPUTS, "robustness")
    Wd, T = {}, {}
    for name, off, tag in WINDOWS:
        Wd[name] = window_data(off, tag)
        T[name] = warehouse_table(Wd[name]).assign(window=name)
        print(name, "warehouses", len(T[name]), "with outcome", int(T[name].y.notna().sum()), flush=True)
    allw = pd.concat(T.values(), ignore_index=True)
    allw.to_csv(os.path.join(out, "ranking_reversal.csv"), index=False)

    L = ["# Ranking reversal between TSB-NB and LGB-Q on VN1, by warehouse (generated by code/ranking_reversal.py)", "",
         f"Outcome y = log(inventory TSB-NB / inventory LGB-Q) at fill {TARGET} within a warehouse (≥ {MIN_SERIES} series); "
         "y < 0: TSB-NB needs less stock. Predictors: pre-test medians only.", "",
         "## 1. Outcome and univariate associations (Spearman ρ of y with each predictor)", "",
         "| window | warehouses with y | share y < 0 | median y | " + " | ".join(FEATS) + " |",
         "|---|---|---|---|" + "---|" * len(FEATS)]
    for name, _, _ in WINDOWS:
        t = T[name].dropna(subset=["y"])
        rhos = [spearmanr(t[f], t.y, nan_policy="omit")[0] for f in FEATS]
        L.append(f"| {name} | {len(t)} | {100 * (t.y < 0).mean():.0f}% | {t.y.median():+.3f} | " +
                 " | ".join(f"{r:+.2f}" for r in rhos) + " |")
    L += ["", "## 2–3. Out-of-window prediction and decision value", "",
          "| fit on → test on | Spearman ρ (pred, y) | permutation p | warehouses assigned TSB-NB | inventory vs always LGB-Q | oracle by warehouse |",
          "|---|---|---|---|---|---|"]
    rows = []
    for train_names, test in ((["third"], "second"), (["second"], "main"), (["third", "second"], "main")):
        model = fit(pd.concat([T[n] for n in train_names]))
        te = T[test].copy()
        te["pred"] = predict(model, te)
        ok = te.dropna(subset=["y"])
        rho = spearmanr(ok.pred, ok.y)[0]
        perm = np.array([spearmanr(rng.permutation(ok.pred.to_numpy()), ok.y)[0] for _ in range(2000)])
        p = float((np.abs(perm) >= abs(rho)).mean())
        base = portfolio_inv(Wd[test], [])
        chosen = set(te.loc[te.pred < 0, "warehouse"])
        rule = portfolio_inv(Wd[test], chosen) / base - 1
        oracle = portfolio_inv(Wd[test], set(ok.loc[ok.y < 0, "warehouse"])) / base - 1
        lab = " + ".join(train_names) + " → " + test
        rows.append(dict(fit=lab, rho=rho, p=p, n_tsb=len(chosen), n=len(te), rule=rule, oracle=oracle))
        L.append(f"| {lab} | {rho:+.2f} | {p:.3f} | {len(chosen)} of {len(te)} | {100 * rule:+.1f}% | {100 * oracle:+.1f}% |")
    pd.DataFrame(rows).to_csv(os.path.join(out, "ranking_reversal_oos.csv"), index=False)
    L += ["", "Negative inventory change = the rule needs less stock than LGB-Q everywhere at portfolio fill 0.92. The oracle "
          "uses each warehouse's realised y in the test window and is not deployable."]
    with open(os.path.join(out, "ranking_reversal.md"), "w", encoding="utf-8") as fh:
        fh.write("\n".join(L) + "\n")
    print("written ranking_reversal.md")


if __name__ == "__main__":
    main()
