"""Per-series statistical tests between forecasting methods (evaluation_metrics.md §5).

For every evaluated series the script recomputes, from the cached forecasts:
    SQL at h = L+R and h = H            (same definition as evaluate.forecast_metrics)
    fill rate and inventory (weeks of demand) of the default scenario without liquidation
and then, per dataset × demand class × metric:
    Friedman test over the 8 methods (complete cases) + mean ranks and the Nemenyi critical difference
    Wilcoxon signed-rank test of each method against lgb_quantile, Holm-adjusted, with the median paired
    difference and the share of series where lgb_quantile is better / worse.

Writes code/outputs/<DATASET>/stat_tests.csv, code/outputs/stat_tests.md and the per-series metrics to
data/cache/series_metrics_<DATASET>.parquet.

Usage:
    python code/stat_tests.py
"""
import os
import sys

import numpy as np
import pandas as pd
from scipy import stats

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from f2d import classify, config, data, evaluate, policy  # noqa: E402
from f2d.features import Builder  # noqa: E402

MODELS = ["empirical", "tsb", "tsb_nb", "ets", "lgb_tweedie", "lgb_conformal", "hgb_quantile", "lgb_quantile"]
REF = "lgb_quantile"
CLASSES = ["all", "smooth", "erratic", "intermittent", "lumpy"]
ALPHA = 0.05
# metric -> True if lower is better
METRICS = {"SQL_h3": True, "SQL_h13": True, "fill_rate": False, "inventory_weeks": True}


def series_sql(Q, Dtrue, qs, h, s_abs):
    qs = np.asarray(qs)
    ok = ~np.isnan(Dtrue)[:, :, None] & ~np.isnan(Q)
    e = Dtrue[:, :, None] - Q
    pin = np.where(ok, np.maximum(qs * e, (qs - 1) * e), np.nan)
    with np.errstate(all="ignore"):
        sql = np.nanmean(pin, axis=(1, 2)) / (h * s_abs)
    return np.where((s_abs > 0) & np.isfinite(sql), sql, np.nan)


def per_series(name):
    d = config.DEFAULT
    R, L, tau, H = d["R"], d["L"], d["tau"], d["H"]
    p = data.load(name)
    Y = p["Y"]
    n, T = Y.shape
    test0 = T - config.TEST_WEEKS
    origins = list(range(test0, T))
    sel = p["start"] <= test0 - config.VALID_WEEKS
    cls, _, _ = classify.classify(Y, p["start"], test0)
    sel &= cls != "none"
    idx = np.flatnonzero(sel)
    b = Builder(p)
    qs = list(config.QUANTILES)
    s_abs, _ = evaluate.naive_scales(Y, p["start"], test0)
    D = np.nan_to_num(Y[:, test0:T]).astype(np.float64)[idx]
    fc = os.path.join(config.CACHE, "forecasts", name)
    out = pd.DataFrame({"series_id": p["attrs"]["series_id"].to_numpy()[idx], "demand_class": cls[idx]})
    w = slice(config.WARMUP_WEEKS, None)
    for m in MODELS:
        for h in (L + R, H):
            Q = np.load(os.path.join(fc, f"{m}_h{h}.npz"))["Q"]
            Dt = np.stack([b.target(o, h) for o in origins], 1)
            out[f"{m}|SQL_h{h}"] = series_sql(Q, Dt, qs, h, s_abs)[idx]
        S = np.load(os.path.join(fc, f"{m}_h{L + R}.npz"))["Q"][idx][:, :, qs.index(tau)]
        sim = policy.simulate(D, S, np.full_like(S, np.inf), L)
        dem = D[:, w].sum(1)
        with np.errstate(all="ignore"):
            out[f"{m}|fill_rate"] = np.where(dem > 0, sim["sales"][:, w].sum(1) / dem, np.nan)
            out[f"{m}|inventory_weeks"] = np.where(dem > 0, sim["on_hand_end"][:, w].sum(1) / dem, np.nan)
    return out


def holm(p):
    p = np.asarray(p, float)
    o = np.argsort(p)
    adj = np.empty_like(p)
    run = 0.0
    for r, i in enumerate(o):
        run = max(run, min(1.0, (len(p) - r) * p[i]))
        adj[i] = run
    return adj


def tests(df, name):
    rows = []
    q_crit = stats.studentized_range.ppf(1 - ALPHA, len(MODELS), np.inf) / np.sqrt(2)
    for metric, lower in METRICS.items():
        X = df[[f"{m}|{metric}" for m in MODELS]].to_numpy()
        for g in CLASSES:
            mask = np.ones(len(df), bool) if g == "all" else (df.demand_class == g).to_numpy()
            Xg = X[mask]
            Xg = Xg[np.isfinite(Xg).all(1)]
            N = len(Xg)
            if N < 10:
                continue
            fr = stats.friedmanchisquare(*Xg.T)
            ranks = stats.rankdata(Xg if lower else -Xg, axis=1).mean(0)
            cd = q_crit * np.sqrt(len(MODELS) * (len(MODELS) + 1) / (6 * N))
            ref = Xg[:, MODELS.index(REF)]
            pw = []
            for j, m in enumerate(MODELS):
                if m == REF:
                    pw.append((np.nan, 0.0, np.nan, np.nan))
                    continue
                diff = Xg[:, j] - ref
                better = np.mean(diff > 0) if lower else np.mean(diff < 0)       # REF better
                worse = np.mean(diff < 0) if lower else np.mean(diff > 0)
                p_w = stats.wilcoxon(Xg[:, j], ref).pvalue if np.any(diff != 0) else 1.0
                pw.append((p_w, np.median(diff), better, worse))
            p_adj = holm([x[0] for x in pw if not np.isnan(x[0])])
            k = 0
            for j, m in enumerate(MODELS):
                r = dict(dataset=name, metric=metric, group=g, n_series=N, friedman_chi2=fr.statistic,
                         friedman_p=fr.pvalue, nemenyi_cd=cd, model=m, mean_rank=ranks[j],
                         rank_gap_vs_ref=ranks[j] - ranks[MODELS.index(REF)],
                         median_diff_vs_ref=pw[j][1], ref_better_share=pw[j][2], ref_worse_share=pw[j][3],
                         wilcoxon_p=pw[j][0], wilcoxon_p_holm=np.nan)
                if m != REF:
                    r["wilcoxon_p_holm"] = p_adj[k]
                    k += 1
                rows.append(r)
    return pd.DataFrame(rows)


def fmt_p(p):
    return "—" if not np.isfinite(p) else ("<0,001" if p < 1e-3 else f"{p:.3f}".replace(".", ","))


def main():
    lines = ["# Per-series statistical tests (generated by code/stat_tests.py)", "",
             f"Friedman test over {len(MODELS)} methods on complete cases; Nemenyi critical difference CD at α = {ALPHA}; "
             f"Wilcoxon signed-rank vs {REF}, Holm-adjusted. 'ref better' = share of series where {REF} is strictly better.",
             "Fill rate and inventory: default scenario (τ = 0.9, L = 2), no liquidation, series with demand in the KPI weeks.", ""]
    for name in ("M5", "VN1"):
        print(f"{name}: per-series metrics ...")
        df = per_series(name)
        df.to_parquet(os.path.join(config.CACHE, f"series_metrics_{name}.parquet"), index=False)
        t = tests(df, name)
        t.to_csv(os.path.join(config.OUTPUTS, name, "stat_tests.csv"), index=False)
        lines += [f"## {name}", ""]
        for metric in METRICS:
            tm = t[t.metric == metric]
            head = tm.groupby("group").first().loc[[g for g in CLASSES if g in tm.group.unique()]]
            lines += [f"### {metric}", "", "| group | N | Friedman χ² | p | Nemenyi CD |", "|---|---|---|---|---|"]
            for g, r in head.iterrows():
                lines.append(f"| {g} | {r.n_series:,} | {r.friedman_chi2:,.0f} | {fmt_p(r.friedman_p)} | {r.nemenyi_cd:.3f} |")
            lines += ["", "Mean rank (lower = better) by group; in brackets: Holm-adjusted Wilcoxon p vs lgb_quantile", ""]
            piv = tm.pivot(index="model", columns="group", values="mean_rank").loc[MODELS, head.index]
            pp = tm.pivot(index="model", columns="group", values="wilcoxon_p_holm").loc[MODELS, head.index]
            lines += ["| model | " + " | ".join(head.index) + " |", "|---" * (len(head.index) + 1) + "|"]
            for m in MODELS:
                cells = [f"{piv.loc[m, g]:.2f}" + ("" if m == REF else f" ({fmt_p(pp.loc[m, g])})") for g in head.index]
                lines.append(f"| {m} | " + " | ".join(cells) + " |")
            ta = tm[(tm.group == "all") & (tm.model != REF)]
            lines += ["", f"All series, vs {REF}: median paired difference (method − ref), share of series where ref is better / worse", "",
                      "| model | median diff | ref better | ref worse |", "|---|---|---|---|"]
            for _, r in ta.iterrows():
                lines.append(f"| {r.model} | {r.median_diff_vs_ref:.4f} | {r.ref_better_share:.3f} | {r.ref_worse_share:.3f} |")
            lines.append("")
    with open(os.path.join(config.OUTPUTS, "stat_tests.md"), "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print("written code/outputs/stat_tests.md")


if __name__ == "__main__":
    main()
