"""Combination of all seven methods and ablation (mentor's suggestion; design fixed beforehand in
07_paper_draft/phase5_workflow.md, section 7).

Uses the cached h = 3 forecasts of the seven single methods; default policy (L = 2, no liquidation); M5 and VN1,
windows main / second (w26) / third (w52). Combinations average the members' quantiles (quantile averaging; the median
variant takes the per-quantile median), which keeps the quantiles ordered.
    E7       mean of the seven methods (primary)
    E7-med   median of the seven methods
    E7−m     leave-one-out ablation, for each method m
    STAT3, GBM4, DQ2, C2   family combinations and the earlier pair
    all 127 subsets (mean): best subset per run = retrospective upper bound, not deployable
    prospective subset: the subset with the lowest regret in one window, applied unchanged to the next
Reported: wQL; inventory relative to LGB-Q at fill 0.92 / 0.94 with 95% bootstrap CIs (200 resamples of series);
regret = excess inventory over the best of the seven single methods, mean over the reached fill targets 0.90–0.98.
Writes code/outputs/ensemble/ensemble_ablation.md and .csv files.

Usage:
    python code/ensemble_ablation.py
"""
import itertools
import os
import sys
import time

import numpy as np
import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from combination import setup, wql  # noqa: E402
from equal_fill_ci import totals  # noqa: E402
from f2d import config, policy  # noqa: E402
from f2d.features import Builder  # noqa: E402
from segment_eval import MODELS, TARGETS, curve, inv_at  # noqa: E402

WINDOWS = {"third": 52, "second": 26, "main": 0}
TRANSITIONS = [("third", "second"), ("second", "main")]
EVAL = (0.92, 0.94)
N_BOOT = 200
H = config.DEFAULT["L"] + config.DEFAULT["R"]
LAB = {"empirical": "EMP", "tsb_nb": "TSB-NB", "ets": "ETS", "lgb_tweedie": "LGB-T", "lgb_conformal": "LGB-C",
       "hgb_quantile": "HGB-Q", "lgb_quantile": "LGB-Q"}
NAMED = {"E7": tuple(MODELS), "STAT3": ("empirical", "ets", "tsb_nb"),
         "GBM4": ("lgb_tweedie", "lgb_conformal", "hgb_quantile", "lgb_quantile"),
         "DQ2": ("hgb_quantile", "lgb_quantile"), "C2": ("lgb_quantile", "tsb_nb")}
for _m in MODELS:
    NAMED["E7−" + LAB[_m]] = tuple(x for x in MODELS if x != _m)
SUBSETS = [s for k in range(1, 8) for s in itertools.combinations(MODELS, k)]


def name_of(s):
    for k, v in NAMED.items():
        if set(v) == set(s):
            return k
    return "+".join(LAB[m] for m in s)


def simulate(tot, key, Q, D):
    L = config.DEFAULT["L"]
    w = slice(config.WARMUP_WEEKS, None)
    qs = list(config.QUANTILES)
    for tau in config.TAU_GRID:
        S = Q[:, :, qs.index(tau)]
        sim = policy.simulate(D, S, np.full_like(S, np.inf), L)
        tot[key, tau, "sales"] = sim["sales"][:, w].sum(1)
        tot[key, tau, "onhand"] = sim["on_hand_end"][:, w].sum(1)


def need_of(tot, key, n):
    c = curve(tot, np.array([key] * n))
    return np.array([inv_at(*c, t) for t in TARGETS])


def regret(need, best):
    r = need / best - 1
    return np.nanmean(r) if np.isfinite(r).any() else np.nan


def delta_ci(tot, key, n, boots):
    c, cr = curve(tot, np.array([key] * n)), curve(tot, np.array(["lgb_quantile"] * n))
    bc = [curve(tot, np.array([key] * n), b) for b in boots]
    br = [curve(tot, np.array(["lgb_quantile"] * n), b) for b in boots]
    out = {}
    for tg in EVAL:
        v, r = inv_at(*c, tg), inv_at(*cr, tg)
        x = np.array([inv_at(*bc[k], tg) / inv_at(*br[k], tg) - 1 for k in range(len(boots))])
        ok = np.isfinite(x)
        out[f"d_{tg:.2f}"] = v / r - 1 if np.isfinite(v) and np.isfinite(r) else np.nan
        out[f"lo_{tg:.2f}"], out[f"hi_{tg:.2f}"] = (np.percentile(x[ok], [2.5, 97.5]) if ok.mean() >= 0.95
                                                    else (np.nan, np.nan))
    return out


def main():
    rng = np.random.default_rng(config.SEED)
    out = os.path.join(config.OUTPUTS, "ensemble")
    os.makedirs(out, exist_ok=True)
    named_rows, subset_rows, runs, prev_best = [], [], {}, {}
    for d in ("M5", "VN1"):
        for wname, off in WINDOWS.items():
            t0 = time.time()
            p, idx, test0, T = setup(d, off)
            n = len(idx)
            tot = totals(d, off, MODELS)
            D = np.nan_to_num(p["Y"][:, test0:T]).astype(np.float64)[idx]
            fc = os.path.join(config.CACHE, "forecasts", d + (f"_w{off}" if off else ""))
            Q = {m: np.load(os.path.join(fc, f"{m}_h{H}.npz"))["Q"][idx].astype(np.float64) for m in MODELS}
            b = Builder(p)
            Dt = np.stack([b.target(o, H) for o in range(test0, T)], 1)[idx]
            qs = list(config.QUANTILES)
            single = {m: need_of(tot, m, n) for m in MODELS}
            best = np.nanmin(np.vstack(list(single.values())), 0)
            # all 127 mean subsets (singles included as subsets of size 1)
            for s in SUBSETS:
                key = "S:" + "+".join(s)
                if len(s) == 1:
                    nd = single[s[0]]
                else:
                    simulate(tot, key, np.mean([Q[m] for m in s], 0), D)
                    nd = need_of(tot, key, n)
                subset_rows.append(dict(dataset=d, window=wname, subset=name_of(s), size=len(s), key=key,
                                        regret=regret(nd, best), **{f"inv_{t:.2f}": v for t, v in zip(TARGETS, nd)}))
            # median of seven
            simulate(tot, "E7-med", np.median([Q[m] for m in MODELS], 0), D)
            boots = [rng.integers(0, n, n) for _ in range(N_BOOT)]
            # keep only what is needed later: singles, named combinations, this run's best subset (selected for the
            # next window) and the subset selected in the previous window
            here = [r for r in subset_rows if r["dataset"] == d and r["window"] == wname]
            best_key = min(here, key=lambda r: r["regret"] if np.isfinite(r["regret"]) else np.inf)["key"]
            keep = set(MODELS) | {"E7-med"} | {"S:" + "+".join(x for x in MODELS if x in v) for v in NAMED.values()}
            keep |= {best_key, prev_best.get(d, "")}
            prev_best[d] = best_key
            tot = {k: v for k, v in tot.items() if not isinstance(k, tuple) or k[0] in keep}
            runs[d, wname] = dict(tot=tot, n=n, boots=boots, best=best)
            for nm in list(NAMED) + ["E7-med"]:
                if nm == "E7-med":
                    key, Qc = "E7-med", np.median([Q[m] for m in MODELS], 0)
                else:
                    key, Qc = "S:" + "+".join(s for s in MODELS if s in NAMED[nm]), np.mean([Q[m] for m in NAMED[nm]], 0)
                nd = need_of(tot, key, n)
                row = dict(dataset=d, window=wname, method=nm, wql=wql(Qc, Dt, qs), regret=regret(nd, best))
                if nm in ("E7", "E7-med", "C2", "STAT3", "GBM4", "DQ2"):
                    row.update(delta_ci(tot, key, n, boots))
                else:
                    c, cr = curve(tot, np.array([key] * n)), curve(tot, np.array(["lgb_quantile"] * n))
                    for tg in EVAL:
                        v, r = inv_at(*c, tg), inv_at(*cr, tg)
                        row[f"d_{tg:.2f}"] = v / r - 1 if np.isfinite(v) and np.isfinite(r) else np.nan
                named_rows.append(row)
            for m in MODELS:
                named_rows.append(dict(dataset=d, window=wname, method=LAB[m], wql=wql(Q[m], Dt, qs),
                                       regret=regret(single[m], best)))
            print(d, wname, f"n={n:,} done in {time.time() - t0:.0f}s", flush=True)
    named, subs = pd.DataFrame(named_rows), pd.DataFrame(subset_rows)
    # prospective subset selection
    pros = []
    for d in ("M5", "VN1"):
        for src, dst in TRANSITIONS:
            s = subs[(subs.dataset == d) & (subs.window == src)].sort_values("regret").iloc[0]
            r = runs[d, dst]
            t = subs[(subs.dataset == d) & (subs.window == dst) & (subs.key == s.key)].iloc[0]
            oracle = subs[(subs.dataset == d) & (subs.window == dst)].sort_values("regret").iloc[0]
            pros.append(dict(dataset=d, transition=f"{src} → {dst}", selected=s.subset, source_regret=s.regret,
                             target_regret=t.regret, oracle_subset=oracle.subset, oracle_regret=oracle.regret,
                             **delta_ci(r["tot"], s.key, r["n"], r["boots"])))
    pros = pd.DataFrame(pros)
    named.to_csv(os.path.join(out, "ensemble_named.csv"), index=False)
    subs.drop(columns="key").to_csv(os.path.join(out, "ensemble_subsets.csv"), index=False)
    pros.to_csv(os.path.join(out, "ensemble_prospective.csv"), index=False)
    write_md(named, subs, pros, out)


def pct(v):
    return "—" if not np.isfinite(v) else f"{100 * v:+.1f}"


def cell(r, tg):
    v, lo, hi = r.get(f"d_{tg:.2f}", np.nan), r.get(f"lo_{tg:.2f}", np.nan), r.get(f"hi_{tg:.2f}", np.nan)
    if not np.isfinite(v):
        return "—"
    return pct(v) + (f" [{pct(lo)}, {pct(hi)}]" if np.isfinite(lo) else "")


def write_md(named, subs, pros, out):
    order = [("M5", w) for w in ("main", "second", "third")] + [("VN1", w) for w in ("main", "second", "third")]
    L = ["# Combination of the seven methods and ablation (generated by code/ensemble_ablation.py)", "",
         "Design and decision criteria fixed beforehand: 07_paper_draft/phase5_workflow.md, section 7. h = 3, L = 2, no "
         "liquidation. Δ = inventory / LGB-Q inventory − 1 in % (negative = less stock than LGB-Q), 95% bootstrap CI over "
         "series. Regret = excess over the best of the seven single methods, mean over reached fill targets 0.90–0.98.", ""]
    main_m = ["E7", "E7-med", "C2", "STAT3", "GBM4", "DQ2"]
    L += ["## 1. Inventory relative to LGB-Q", "", "| dataset | window | method | fill 0.92 | fill 0.94 | wQL |", "|---|---|---|---|---|---|"]
    for d, w in order:
        g = named[(named.dataset == d) & (named.window == w)].set_index("method")
        L.append(f"| {d} | {w} | LGB-Q | ref | ref | {g.loc['LGB-Q', 'wql']:.4f} |")
        for m in main_m:
            r = g.loc[m]
            L.append(f"| {d} | {w} | {m} | {cell(r, 0.92)} | {cell(r, 0.94)} | {r['wql']:.4f} |")
    piv = named.pivot_table(index="method", columns=["dataset", "window"], values="regret")
    piv["max"] = piv.max(1)
    piv = (100 * piv).round(1).sort_values("max")
    L += ["", "## 2. Regret (%) per run and maximum over the six runs", "", piv.to_markdown(), ""]
    L += ["## 3. Leave-one-out ablation: inventory of E7 − m relative to E7 at fill 0.92 (%)", "",
          "Positive = removing m needs more stock (m helps the combination); negative = the combination is better without m.", ""]
    rows = []
    for m in MODELS:
        nm = "E7−" + LAB[m]
        rr = {"removed": LAB[m]}
        for d, w in order:
            g = named[(named.dataset == d) & (named.window == w)].set_index("method")
            a, e = g.loc[nm, "d_0.92"], g.loc["E7", "d_0.92"]
            rr[f"{d} {w}"] = round(100 * ((1 + a) / (1 + e) - 1), 1) if np.isfinite(a) and np.isfinite(e) else np.nan
        rows.append(rr)
    L += [pd.DataFrame(rows).set_index("removed").to_markdown(), ""]
    L += ["## 4. Best of all 127 mean subsets per run (retrospective, not deployable)", "",
          "| dataset | window | best subset | regret % | E7 regret % | LGB-Q regret % |", "|---|---|---|---|---|---|"]
    for d, w in order:
        g = subs[(subs.dataset == d) & (subs.window == w)].sort_values("regret")
        e7 = g[g.subset == "E7"].regret.iloc[0]
        lq = g[g.subset == "LGB-Q"].regret.iloc[0]
        L.append(f"| {d} | {w} | {g.iloc[0].subset} | {100 * g.iloc[0].regret:.1f} | {100 * e7:.1f} | {100 * lq:.1f} |")
    L += ["", "## 5. Prospective subset selection (lowest regret in the earlier window, applied to the next)", "",
          "| dataset | transition | selected subset | regret in source % | regret in target % | Δ vs LGB-Q fill 0.92 | Δ vs LGB-Q fill 0.94 | best subset in target (hindsight) |",
          "|---|---|---|---|---|---|---|---|"]
    for _, r in pros.iterrows():
        L.append(f"| {r.dataset} | {r.transition} | {r.selected} | {100 * r.source_regret:.1f} | {100 * r.target_regret:.1f} | "
                 f"{cell(r, 0.92)} | {cell(r, 0.94)} | {r.oracle_subset} ({100 * r.oracle_regret:.1f}) |")
    with open(os.path.join(out, "ensemble_ablation.md"), "w", encoding="utf-8") as fh:
        fh.write("\n".join(L) + "\n")
    print("written", os.path.join(out, "ensemble_ablation.md"))


if __name__ == "__main__":
    main()
