"""Tables of the 10-page paper (v3, seven methods), generated from the result files so that no number is retyped.

Writes 07_paper_draft/v3_tables.md. Sources: *_m7 outputs (seven methods), demand_shift.csv, segment_eval.csv,
matched_comparison.csv, kpi.csv / breakeven.csv of the standard runs (liquidation, LGB-Q rows), *_nop and *_sf
outputs (comparability checks, if present), *_c2m7 outputs (appendix, Chronos-2 on VN1 and VNF).

Usage:
    python code/paper_tables_v3.py
"""
import os
import sys

import numpy as np
import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from f2d import config  # noqa: E402

O = config.OUTPUTS
LAB = {"empirical": "EMP", "tsb_nb": "TSB-NB", "ets": "ETS", "lgb_tweedie": "LGB-T", "lgb_conformal": "LGB-C",
       "hgb_quantile": "HGB-Q", "lgb_quantile": "LGB-Q", "chronos2": "Chronos-2", "tsb": "TSB-P"}
M7 = ["empirical", "tsb_nb", "ets", "lgb_tweedie", "lgb_conformal", "hgb_quantile", "lgb_quantile"]
WIN = [("main", ""), ("second", "_w26"), ("third", "_w52")]
D = config.DEFAULT


def rd(*p):
    return pd.read_csv(os.path.join(O, *p))


def pct(x, lo=None, hi=None):
    if not np.isfinite(x):
        return "—"
    s = f"{100 * x:+.1f}"
    return s + (f" [{100 * lo:+.1f}, {100 * hi:+.1f}]" if lo is not None and np.isfinite(lo) else "")


def t_accuracy():
    ra = rd("robust_accuracy_m7.csv")
    L = ["**Table 2.** Forecast accuracy, all series, h = 3. wQL = volume-weighted quantile loss; median = median per-series "
         "scaled quantile loss; rank = mean per-series rank among the seven methods (CD = Nemenyi critical difference). "
         "Three test windows: main / second / third. Lower is better.", "",
         "| Method | M5 wQL | M5 median | M5 rank | VN1 wQL | VN1 median | VN1 rank |", "|---|---|---|---|---|---|---|"]
    st = {(d, w): rd(d + s + "_m7", "stat_tests.csv") for d in ("M5", "VN1") for w, s in WIN}
    wn = {"main": "main", "second": "w26", "third": "w52"}
    for m in M7:
        row = [LAB[m]]
        for d in ("M5", "VN1"):
            for col in ("wQL", "median_SQL"):
                v = [ra[(ra.dataset == d) & (ra.window == wn[w]) & (ra.h == 3) & (ra.group == "all") & (ra.model == m)][col].iloc[0] for w, _ in WIN]
                row.append(" / ".join(f"{x:.3f}" for x in v))
            v = []
            for w, _ in WIN:
                s = st[d, w]
                v.append(s[(s.metric == "SQL_h3") & (s.group == "all") & (s.model == m)].mean_rank.iloc[0])
            row.append(" / ".join(f"{x:.2f}" for x in v))
        L.append("| " + " | ".join(row) + " |")
    cds = {d: " / ".join(f"{st[d, w][(st[d, w].metric == 'SQL_h3') & (st[d, w].group == 'all')].nemenyi_cd.iloc[0]:.3f}" for w, _ in WIN) for d in ("M5", "VN1")}
    L += ["", f"CD (α = 0.05): M5 {cds['M5']}; VN1 {cds['VN1']}.", ""]
    # h = 13 ranks, compact
    L += ["Mean per-series rank at h = 13 (main / second / third): " + "; ".join(
        f"{d}: " + ", ".join(f"{LAB[m]} " + " / ".join(
            f"{st[d, w][(st[d, w].metric == 'SQL_h13') & (st[d, w].group == 'all') & (st[d, w].model == m)].mean_rank.iloc[0]:.2f}" for w, _ in WIN)
            for m in ("lgb_quantile", "hgb_quantile", "tsb_nb")) for d in ("M5", "VN1")) + ".", ""]
    return L


def t_inventory():
    L = ["**Table 3.** Inventory (weeks of demand) needed for a fill rate of 0.94, all series, with 95% bootstrap CIs over "
         "series. Frontier rank = mean rank of the inventory needed over fill targets 0.90–0.98 among seven methods; "
         "P(best) = share of resamples in which LGB-Q has the best frontier rank. Δ = I_method / I_LGB-Q − 1 in % "
         "(positive = LGB-Q needs less); “—” = fill rate 0.94 not reached.", "",
         "| Dataset | Window | LGB-Q inventory | Frontier rank | P(best) | HGB-Q Δ | LGB-T Δ | LGB-C Δ | TSB-NB Δ | ETS Δ |", "|---|---|---|---|---|---|---|---|---|---|"]
    for d in ("M5", "VN1"):
        for w, s in WIN:
            c = rd(f"equal_fill_ci{s}_m7.csv")
            c = c[(c.dataset == d) & (c.kpi == "units") & (c.group == "all")].set_index("model")
            q = c.loc["lgb_quantile"]
            row = [d, w, f"{q['inv_0.94']:.2f} [{q['inv_0.94_lo']:.2f}, {q['inv_0.94_hi']:.2f}]", f"{q.frontier_rank:.2f}", f"{q.best_frontier_share:.2f}"]
            for m in ("hgb_quantile", "lgb_tweedie", "lgb_conformal", "tsb_nb", "ets"):
                r = c.loc[m]
                row.append(pct(r["rel_0.94"], r["rel_0.94_lo"], r["rel_0.94_hi"]))
            L.append("| " + " | ".join(row) + " |")
    L.append("")
    # class-level frontier ranks
    L += ["**Table 4.** Frontier rank by ADI–CV² class (main / second / third window; 1 = least inventory; n/a = no method "
          "reaches fill rate 0.90).", "", "| Method | M5 all | M5 smooth | M5 erratic | M5 intermittent | M5 lumpy | VN1 all | VN1 smooth | VN1 erratic | VN1 intermittent | VN1 lumpy |",
          "|---|" + "---|" * 10]
    C = {w: rd(f"equal_fill_ci{s}_m7.csv") for w, s in WIN}
    for m in M7:
        row = [LAB[m]]
        for d in ("M5", "VN1"):
            for g in ("all", "smooth", "erratic", "intermittent", "lumpy"):
                v = []
                for w, _ in WIN:
                    c = C[w]
                    x = c[(c.dataset == d) & (c.kpi == "units") & (c.group == g) & (c.model == m)].frontier_rank.iloc[0]
                    v.append("n/a" if not np.isfinite(x) else f"{x:.1f}")
                row.append(" / ".join(v))
        L.append("| " + " | ".join(row) + " |")
    L.append("")
    return L


def t_shift():
    s = rd("demand_shift.csv")
    wn = {"main": "main", "second": "w26", "third": "w52"}
    L = ["**Table 5.** Ex-post split of the series by the change of their demand (test period vs the 26 weeks before it): "
         "stable 0.67–1.5×, growing > 1.5×. Share of test demand of the growing series, and inventory needed at fill rate "
         "0.92: Δ = I_TSB-NB / I_LGB-Q − 1 (positive = LGB-Q needs less; “TSB-NB fails” = TSB-NB does not reach 0.92).", "",
         "| Dataset | Window | Growing: share of demand | Stable series: Δ | Growing series: Δ | All series: Δ |", "|---|---|---|---|---|---|"]
    for d in ("M5", "VN1"):
        for w, _ in WIN:
            g = s[(s.dataset == d) & (s.window == wn[w])]

            def delta(st):
                x = g[g.stratum == st].set_index("model")["inv_0.92"]
                a, b = x["lgb_quantile"], x["tsb_nb"]
                if np.isfinite(a) and not np.isfinite(b):
                    return "TSB-NB fails"
                return pct(b / a - 1) + "%" if np.isfinite(a) and np.isfinite(b) else "—"
            sh = g[g.stratum == "growing"].demand_share.iloc[0]
            L.append(f"| {d} | {w} | {100 * sh:.1f}% | {delta('stable')} | {delta('growing')} | {delta('all')} |")
    L.append("")
    return L


def t_rules():
    r = rd("segment_eval.csv")
    L = ["**Table 6.** Selection rules learned on one window and applied to the next: inventory needed at fill rate 0.94 "
         "relative to always using LGB-Q (%, 95% bootstrap CI; negative = less inventory).", "",
         "| Rule | M5 third → second | M5 second → main | VN1 third → second | VN1 second → main |", "|---|---|---|---|---|"]
    order = ["always TSB-NB", "best single method of previous window", "rule by ADI–CV² class", "rule by segment",
             "rule by class × segment", "oracle by segment (not usable)"]
    tr = [("M5", "w52 → w26"), ("M5", "w26 → main"), ("VN1", "w52 → w26"), ("VN1", "w26 → main")]
    for o in order:
        row = [o]
        for d, t in tr:
            x = r[(r.dataset == d) & (r.transition == t) & (r.rule == o)].iloc[0]
            row.append(pct(x["rel_0.94"], x["lo_0.94"], x["hi_0.94"]))
        L.append("| " + " | ".join(row) + " |")
    L.append("")
    return L


def t_liq():
    L = ["**Table 7.** Liquidation policies with LGB-Q forecasts, default scenario, all series (main / second / third "
         "window). Inventory change and fill-rate change relative to no liquidation; stockout = change of the stockout "
         "rate on weeks with demand; s* = break-even salvage ratio (upper bound), range over holding cost 10–40%/year × "
         "margin 30–100% and the four ML models.", "",
         "| Dataset | Policy | % of demand liquidated | Inventory change | Fill rate change (pp) | Stockout rate change | s* range |", "|---|---|---|---|---|---|---|"]
    for d in ("M5", "VN1"):
        K = {w: rd(d + s, "kpi.csv") for w, s in WIN}
        B = {w: rd(d + s, "breakeven.csv") for w, s in WIN}
        for pol in ("quantile", "fixed", "dead13"):
            liq, inv, fill, so, lo, hi = [], [], [], [], [], []
            for w, _ in WIN:
                k = K[w]
                k = k[(k.model == "lgb_quantile") & (k.group == "all") & (k.tau == D["tau"]) & (k.L == D["L"]) & (k.H == D["H"])
                      & (k.q_liq == D["q_liq"]) & (k.k == D["k_fixed"])].set_index("policy")
                a, b = k.loc["none"], k.loc[pol]
                liq.append(f"{100 * b.liquidated_share:.2f}")
                inv.append(f"{100 * (b.inventory_weeks / a.inventory_weeks - 1):+.1f}%")
                fill.append(f"{100 * (b.fill_rate - a.fill_rate):+.2f}")
                so.append(f"{100 * (b.stockout_rate_demand_weeks / a.stockout_rate_demand_weeks - 1):+.0f}%")
                bb = B[w]
                bb = bb[(bb.policy == pol) & (bb.group == "all") & bb.model.isin(["lgb_quantile", "hgb_quantile", "lgb_tweedie", "lgb_conformal"])]
                up = [c for c in bb.columns if c.startswith("s_star_h")]
                units = bb.liquidated_units.min()
                lo.append(bb[up].min().min())
                hi.append(bb[up].max().max())
                small = units < 2000
            srange = " / ".join(f"{a:.2f}–{b:.2f}" for a, b in zip(lo, hi))
            if d == "M5" and pol == "quantile":
                srange = "unstable (few units)"
            L.append(f"| {d} | {pol} | {' / '.join(liq)} | {' / '.join(inv)} | {' / '.join(fill)} | {' / '.join(so)} | {srange} |")
    L.append("")
    return L


def t_checks():
    L = ["**Table 8.** Comparability checks.", ""]
    mc = rd("matched_comparison.csv")
    L += ["(a) Composition matching: frontier leader and Δ = I_TSB-NB / I_LGB-Q − 1 at fill rate 0.92 (main / second / third).", "",
          "| Sample | Leader | Δ TSB-NB vs LGB-Q |", "|---|---|---|"]
    for d, wt, name in (("M5", "original", "M5"), ("VN1", "reweighted to M5", "VN1 re-weighted to the M5 composition"), ("VN1", "original", "VN1")):
        lead, dl = [], []
        for w in ("main", "w26", "w52"):
            g = mc[(mc.dataset == d) & (mc.weighting == wt) & (mc.window == w)].set_index("model")
            lead.append(LAB[g.frontier_rank.idxmin()])
            a, b = g.loc["lgb_quantile", "inv_0.92"], g.loc["tsb_nb", "inv_0.92"]
            dl.append(pct(b / a - 1) + "%")
        L.append(f"| {name} | {' / '.join(lead)} | {' / '.join(dl)} |")
    L.append("")
    for tag, title, d in (("nop", "(b) VN1 without the price features", "VN1"), ("sf", "(c) M5 with the 21 shared features only", "M5")):
        rows = []
        for w, s in WIN:
            f0, f1 = os.path.join(O, f"equal_fill_ci{s}_m7.csv"), os.path.join(O, f"equal_fill_ci{s}_{tag}.csv")
            if not os.path.exists(f1):
                rows.append(f"| {w} | pending | pending | pending | pending |")
                continue
            a, b = pd.read_csv(f0), pd.read_csv(f1)
            a = a[(a.dataset == d) & (a.kpi == "units") & (a.group == "all")].set_index("model")
            b = b[(b.dataset == d) & (b.kpi == "units") & (b.group == "all") & b.model.isin(M7)].set_index("model")
            # frontier ranks of the ablation file were computed with TSB-P present: report inventory, which does not depend on it
            fa = rd(d + s, "forecast_metrics.csv")
            fb = rd(d + s + "_" + tag, "forecast_metrics.csv")
            sq = lambda f: f[(f.model == "lgb_quantile") & (f.horizon == 3) & (f.group == "all")].SQL.iloc[0]
            pp = lambda v: "not reached" if not np.isfinite(v) else pct(v) + "%"
            rows.append(f"| {w} | {a.loc['lgb_quantile', 'inv_0.94']:.2f} → {b.loc['lgb_quantile', 'inv_0.94']:.2f} | "
                        f"{pp(a.loc['tsb_nb', 'rel_0.94'])} → {pp(b.loc['tsb_nb', 'rel_0.94'])} | "
                        f"{pp(a.loc['lgb_tweedie', 'rel_0.94'])} → {pp(b.loc['lgb_tweedie', 'rel_0.94'])} | {sq(fa):.3f} → {sq(fb):.3f} |")
        L += [title + ": standard → ablation.", "", "| Window | LGB-Q inventory at fill 0.94 | Δ TSB-NB | Δ LGB-T | LGB-Q mean SQL (h = 3) |", "|---|---|---|---|---|"] + rows + [""]
    return L


def t_chronos():
    L = ["**Table A1 (appendix).** Chronos-2 (zero-shot, univariate) against the seven-method benchmark, h = 3. Rank = mean "
         "per-series SQL rank among 8 methods; Δ = I_Chronos-2 / I_LGB-Q − 1 at equal fill rate with 95% bootstrap CI.", "",
         "| Data, window | Mean SQL Chronos-2 / LGB-Q | Per-series rank Chronos-2 / LGB-Q | LGB-Q better on | Frontier rank Chronos-2 / LGB-Q | Δ at fill 0.90 | Δ at fill 0.94 |",
         "|---|---|---|---|---|---|---|"]
    runs = [("VN1", "main", "", "equal_fill_ci_c2m7.csv", "VN1_c2m7"), ("VN1", "second", "_w26", "equal_fill_ci_w26_c2m7.csv", "VN1_w26_c2m7"),
            ("VN1", "third", "_w52", "equal_fill_ci_w52_c2m7.csv", "VN1_w52_c2m7"), ("VNF", "single", "", "equal_fill_ci_VNF_c2m7.csv", "VNF_c2m7")]
    for d, w, s, ef, sd in runs:
        if not os.path.exists(os.path.join(O, ef)) or not os.path.exists(os.path.join(O, sd, "stat_tests.csv")):
            L.append(f"| {d}, {w} | pending | | | | | |")
            continue
        c = rd(ef)
        c = c[(c.dataset == d) & (c.kpi == "units") & (c.group == "all")].set_index("model")
        t = rd(sd, "stat_tests.csv")
        t = t[(t.metric == "SQL_h3") & (t.group == "all")].set_index("model")
        fm_dir = d + s + "_c2" if d == "VN1" else "VNF"
        fm = rd(fm_dir, "forecast_metrics.csv")
        sq = lambda m: fm[(fm.model == m) & (fm.horizon == 3) & (fm.group == "all")].SQL.iloc[0]
        ch = c.loc["chronos2"]
        L.append(f"| {d}, {w} | {sq('chronos2'):.3f} / {sq('lgb_quantile'):.3f} | {t.mean_rank['chronos2']:.2f} / {t.mean_rank['lgb_quantile']:.2f} | "
                 f"{100 * t.ref_better_share['chronos2']:.1f}% | {ch.frontier_rank:.2f} / {c.loc['lgb_quantile'].frontier_rank:.2f} | "
                 f"{pct(ch['rel_0.90'], ch['rel_0.90_lo'], ch['rel_0.90_hi'])} | {pct(ch['rel_0.94'], ch['rel_0.94_lo'], ch['rel_0.94_hi'])} |")
    L.append("")
    return L


def main():
    L = ["# Tables for the 10-page paper (v3, seven methods) — generated by code/paper_tables_v3.py", "",
         "Do not edit by hand: rerun the script. Method labels: " + ", ".join(f"{v} = {k}" for k, v in LAB.items() if k in M7) + ".", ""]
    for f in (t_accuracy, t_inventory, t_shift, t_rules, t_liq, t_checks, t_chronos):
        L += f()
    out = os.path.join(config.ROOT, "07_paper_draft", "v3_tables.md")
    with open(out, "w", encoding="utf-8") as fh:
        fh.write("\n".join(L))
    print("written", out)


if __name__ == "__main__":
    main()
