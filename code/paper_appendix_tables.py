"""Generate Appendix tables A1-A5 of the paper draft from code/outputs.

Writes 07_paper_draft/_appendix_tables.md, which is pasted into 07_paper_draft/appendix.md.

Usage:
    python code/paper_appendix_tables.py
"""
import os
import numpy as np
import pandas as pd

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "code", "outputs")
LAB = {"empirical": "EMP", "tsb": "TSB-P", "tsb_nb": "TSB-NB", "ets": "ETS", "lgb_tweedie": "LGB-T",
       "lgb_conformal": "LGB-C", "hgb_quantile": "HGB-Q", "lgb_quantile": "LGB-Q", "chronos2": "Chronos-2"}
ORDER = ["empirical", "tsb", "tsb_nb", "ets", "lgb_tweedie", "lgb_conformal", "hgb_quantile", "lgb_quantile"]
T = (0.90, 0.92, 0.94, 0.96, 0.98)
WIN = [("Main", "equal_fill_ci.csv"), ("Second", "equal_fill_ci_w26.csv"), ("Third", "equal_fill_ci_w52.csv")]


def f(x, d=2):
    return "—" if not np.isfinite(x) else f"{x:.{d}f}"


L = []
# A1 default-scenario KPIs
L += ["## A1. Inventory KPIs at the default scenario (τ = 0.9, no liquidation), main window", "",
      "Fill rate, CSL, stockout rate (stockout weeks / weeks with demand) and inventory (weeks of demand); 95% bootstrap CIs over series (200 resamples). Source: `code/outputs/<D>/kpi.csv`.", ""]
for D in ["M5", "VN1"]:
    k = pd.read_csv(os.path.join(OUT, D, "kpi.csv"))
    k = k[(k.policy == "none") & (k.tau == 0.9) & (k.L == 2) & (k.H == 13) & (k.q_liq == 0.95) & (k.k == 26) & (k.group == "all")]
    k = k.drop_duplicates("model").set_index("model")
    L += [f"**{D}**", "", "| Method | Fill rate [CI] | CSL | Stockout rate | Inventory [CI] |", "|---|---|---|---|---|"]
    for m in ORDER:
        r = k.loc[m]
        L.append(f"| {LAB[m]} | {r.fill_rate:.3f} [{r.fill_rate_lo:.3f}, {r.fill_rate_hi:.3f}] | {r.csl:.3f} | "
                 f"{r.stockout_rate_demand_weeks:.3f} | {r.inventory_weeks:.2f} [{r.inventory_weeks_lo:.2f}, {r.inventory_weeks_hi:.2f}] |")
    L.append("")

# A2 Tweedie fix
tw = pd.read_csv(os.path.join(ROOT, "06_experiment_results", "tables", "tweedie_fix_before_after.csv"))
L += ["## A2. LightGBM-Tweedie trained on unscaled vs. scaled target", "",
      "Source: `06_experiment_results/tables/tweedie_fix_before_after.csv` ([R §1.1]).", "",
      tw.to_markdown(index=False, floatfmt=".3f"), ""]

# A3 per-quantile loss
pq = pd.read_csv(os.path.join(OUT, "per_quantile_loss.csv"))
L += ["## A3. Scaled pinball loss by quantile (h = 3), intermittent series", "",
      "Mean and median over series of the per-series scaled pinball loss, and share of series where LGB-Q has a strictly lower loss than TSB-NB. Source: `code/outputs/per_quantile_loss.csv`.", "",
      "| Data | Window | q | Mean LGB-Q | Mean TSB-NB | Median LGB-Q | Median TSB-NB | LGB-Q lower (%) |", "|---|---|---|---|---|---|---|---|"]
wn = {"main": "Main", "w26": "Second", "w52": "Third"}
for D in ["VN1", "M5", "VNF"]:
    x = pq[(pq.dataset == D) & (pq.group == "intermittent")]
    for _, r in x.iterrows():
        L.append(f"| {D} | {wn[r.window]} | {r.q:g} | {r.mean_lgb_quantile:.3f} | {r.mean_tsb_nb:.3f} | {r.median_lgb_quantile:.3f} | "
                 f"{r.median_tsb_nb:.3f} | {100 * r.lgbq_better_than_tsbnb_share:.1f} |")
L.append("")

# A4 inventory needed by class and window (units)
L += ["## A4. Inventory (weeks of demand) needed to reach a fill rate, by window and demand class", "",
      "Point estimates, linear interpolation along the τ curve (τ ∈ [0.5, 0.99]); \"—\" = target not reached. Source: `code/outputs/equal_fill_ci*.csv` (identical to `comparison*.md`).", ""]
for wname, fn in WIN:
    d = pd.read_csv(os.path.join(OUT, fn))
    for D, groups in [("M5", ["all"]), ("VN1", ["all", "smooth", "erratic", "intermittent", "lumpy"])]:
        for g in groups:
            y = d[(d.dataset == D) & (d.kpi == "units") & (d.group == g)].set_index("model")
            if not len(y):
                continue
            L += [f"**{D}, {wname} window, {g}** (n = {int(y.n_series.iloc[0]):,})", "",
                  "| Method | " + " | ".join(f"{t:.2f}" for t in T) + " | Frontier rank |", "|---|" + "---|" * (len(T) + 1)]
            for m in ORDER:
                r = y.loc[m]
                L.append(f"| {LAB[m]} | " + " | ".join(f(r[f'inv_{t:.2f}']) for t in T) + f" | {f(r.frontier_rank, 2)} |")
            L.append("")

# A5 value-weighted CIs
L += ["## A5. Value-weighted inventory at fill rate 0.94 with bootstrap CIs", "",
      "As Table 5, with units weighted by the weekly selling price. Δ = I_method / I_LGB-Q − 1 (%). Source: `code/outputs/equal_fill_ci*.csv`.", "",
      "| Dataset | Window | LGB-Q inventory | Frontier rank | P(best) | HGB-Q | LGB-T | LGB-C | TSB-NB | ETS |", "|---|---|---|---|---|---|---|---|---|---|"]


def cell(r):
    v, lo, hi = r["rel_0.94"], r["rel_0.94_lo"], r["rel_0.94_hi"]
    if not np.isfinite(v):
        return "—"
    s = f"{100 * v:+.1f}"
    return s + (f" [{100 * lo:+.1f}, {100 * hi:+.1f}]" if np.isfinite(lo) else "")


for D in ["M5", "VN1"]:
    for wname, fn in WIN:
        d = pd.read_csv(os.path.join(OUT, fn))
        y = d[(d.dataset == D) & (d.kpi == "value") & (d.group == "all")].set_index("model")
        q = y.loc["lgb_quantile"]
        L.append(f"| {D} | {wname} | {q['inv_0.94']:.2f} [{q['inv_0.94_lo']:.2f}, {q['inv_0.94_hi']:.2f}] | {q.frontier_rank:.2f} | "
                 f"{q.best_frontier_share:.2f} | " + " | ".join(cell(y.loc[m]) for m in ["hgb_quantile", "lgb_tweedie", "lgb_conformal", "tsb_nb", "ets"]) + " |")
L.append("")
open(os.path.join(ROOT, "07_paper_draft", "_appendix_tables.md"), "w", encoding="utf-8").write("\n".join(L))
print("ok", len(L))
