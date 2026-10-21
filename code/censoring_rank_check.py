"""Do suspected stock-outs change the method rankings? (reviewer item 2, follow-up to censoring_check.py)

Uses flag_weeks() of censoring_check.py (suspected stock-out weeks, from sales only) and the cached h = 3 forecasts of
the seven methods plus C2 (mean of the LGB-Q and TSB-NB quantiles). Default policy (L = 2, no liquidation). Per
dataset × window (main, second, third) and α ∈ {0.01, 0.05}, three evaluations are compared:
    base    all eligible series, recorded sales as demand (the paper's setting)
    clean   (a) only series without any suspected stock-out week in the test window
    imputed (b) all series; in suspected weeks of the test window, demand is replaced by the series' mean weekly sales
            before the test period, and the policy is simulated again with the same forecasts
Reported: inventory needed at fill 0.90–0.98, frontier rank, leading single method, regret (excess over the best of
the seven single methods, mean over reached targets) and Δ vs LGB-Q at fill 0.92 / 0.94 with 95% bootstrap CIs.
Decision criteria fixed before running: rankings "hold" if the leading single method of each window is unchanged and
C2 keeps the lowest maximum regret.
Writes code/outputs/censoring/censoring_rank_check.md and .csv.

Usage:
    python code/censoring_rank_check.py
"""
import os
import sys

import numpy as np
import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from analyze_results import frontier_rank  # noqa: E402
from censoring_check import flag_weeks  # noqa: E402
from f2d import classify, config, data, policy  # noqa: E402
from segment_eval import MODELS, TARGETS, curve, inv_at  # noqa: E402

WINDOWS = {"main": 0, "second": 26, "third": 52}
ALPHAS = (0.01, 0.05)
EVAL = (0.92, 0.94)
N_BOOT = 200
H = 3
LAB = {"empirical": "EMP", "tsb_nb": "TSB-NB", "ets": "ETS", "lgb_tweedie": "LGB-T", "lgb_conformal": "LGB-C",
       "hgb_quantile": "HGB-Q", "lgb_quantile": "LGB-Q", "C2": "C2"}


def simulate_all(Q, D):
    L = config.DEFAULT["L"]
    w = slice(config.WARMUP_WEEKS, None)
    qs = list(config.QUANTILES)
    tot = {"demand": D[:, w].sum(1)}
    for m, q in Q.items():
        for tau in config.TAU_GRID:
            S = q[:, :, qs.index(tau)]
            sim = policy.simulate(D, S, np.full_like(S, np.inf), L)
            tot[m, tau, "sales"] = sim["sales"][:, w].sum(1)
            tot[m, tau, "onhand"] = sim["on_hand_end"][:, w].sum(1)
    return tot


def evaluate(tot, n, idx, rng, label):
    methods = MODELS + ["C2"]
    curves = {m: curve(tot, np.array([m] * n), idx) for m in methods}
    need = pd.DataFrame({m: [inv_at(*curves[m], t) for t in TARGETS] for m in methods}, index=TARGETS)
    fr = frontier_rank(need[MODELS].T)
    leader = fr.idxmin()
    best = need[MODELS].min(axis=1)
    m_idx = np.arange(n) if idx is None else idx
    boots = [rng.choice(m_idx, len(m_idx), replace=True) for _ in range(N_BOOT)]
    bc = {m: [curve(tot, np.array([m] * n), b) for b in boots] for m in ("lgb_quantile", "tsb_nb", "lgb_tweedie", "C2")}
    rows = []
    for m in methods:
        rg = need[m] / best - 1
        r = dict(eval=label, method=LAB[m], n_series=len(m_idx), regret=rg.mean(skipna=True),
                 frontier_rank=fr.get(m, np.nan), leader=LAB[leader])
        if m in bc and m != "lgb_quantile":
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
            tot = simulate_all(Q, D)
            for r in evaluate(tot, n, None, rng, "base"):
                rows.append(dict(dataset=d, window=wname, alpha=np.nan, **r))
            for alpha in ALPHAS:
                F, _ = flag_weeks(Y, start, test0, alpha)
                Ft = F[idx][:, test0:T]
                clean = np.flatnonzero(~Ft.any(1))
                for r in evaluate(tot, n, clean, rng, "clean"):
                    rows.append(dict(dataset=d, window=wname, alpha=alpha, **r))
                Dimp = np.where(Ft, np.maximum(D, rate[:, None]), D)
                tot_imp = simulate_all(Q, Dimp)
                for r in evaluate(tot_imp, n, None, rng, "imputed"):
                    rows.append(dict(dataset=d, window=wname, alpha=alpha, **r))
                print(d, wname, "alpha", alpha, f"clean series {len(clean):,}/{n:,}; flagged test weeks {Ft.mean():.3f}", flush=True)
    res = pd.DataFrame(rows)
    out = os.path.join(config.OUTPUTS, "censoring")
    os.makedirs(out, exist_ok=True)
    res.to_csv(os.path.join(out, "censoring_rank_check.csv"), index=False)

    def cell(r, tg):
        v, lo, hi = r.get(f"d_{tg:.2f}", np.nan), r.get(f"lo_{tg:.2f}", np.nan), r.get(f"hi_{tg:.2f}", np.nan)
        if not np.isfinite(v):
            return "—"
        return f"{100 * v:+.1f}" + (f" [{100 * lo:+.1f}, {100 * hi:+.1f}]" if np.isfinite(lo) else "")
    lines = ["# Do suspected stock-outs change the rankings? (generated by code/censoring_rank_check.py)", "",
             "base = all eligible series, recorded sales as demand; clean = only series without suspected stock-out weeks "
             "in the test window; imputed = suspected weeks set to the series' mean weekly sales before the test period. "
             "Same cached forecasts throughout. Δ vs LGB-Q in % with 95% bootstrap CI (positive = LGB-Q needs less).", ""]
    for alpha in ALPHAS:
        sub = res[(res.alpha == alpha) | res.alpha.isna()]
        lines += [f"## α = {alpha}", "", "### Leading single method (frontier rank) and number of series", "",
                  "| dataset | window | base | clean | imputed | clean series |", "|---|---|---|---|---|---|"]
        for (d, w), g in sub.groupby(["dataset", "window"], sort=False):
            lead = {e: g[g["eval"] == e].leader.iloc[0] for e in ("base", "clean", "imputed")}
            ncl = int(g[(g["eval"] == "clean")].n_series.iloc[0])
            nb = int(g[(g["eval"] == "base")].n_series.iloc[0])
            lines.append(f"| {d} | {w} | {lead['base']} | {lead['clean']} | {lead['imputed']} | {ncl:,} of {nb:,} |")
        lines += ["", "### Δ vs LGB-Q (%)", "", "| dataset | window | eval | method | fill 0.92 | fill 0.94 |", "|---|---|---|---|---|---|"]
        for _, r in sub[sub.method.isin(["TSB-NB", "LGB-T", "C2"])].iterrows():
            lines.append(f"| {r.dataset} | {r.window} | {r['eval']} | {r.method} | {cell(r, 0.92)} | {cell(r, 0.94)} |")
        piv = sub.pivot_table(index="method", columns="eval", values="regret", aggfunc="max")
        lines += ["", "### Maximum regret over the six runs (%)", "", (100 * piv).round(1).sort_values("base").to_markdown(), ""]
    with open(os.path.join(out, "censoring_rank_check.md"), "w", encoding="utf-8") as fh:
        fh.write("\n".join(lines))
    print("written code/outputs/censoring/censoring_rank_check.md")


if __name__ == "__main__":
    main()
