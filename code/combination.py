"""Quantile combination as a hedge between the two VN1 leaders (extension; Petropoulos et al. 2019 find combinations best).

On VN1 the most inventory-efficient method alternates between LGB-Q and TSB-NB across test windows, and the
growth-prediction rule (growth_rule.py) is unstable. A combination needs no prediction: each quantile is the
arithmetic mean of the methods' quantiles (quantile averaging). Specified before looking at the results:
    C2 = mean(LGB-Q, TSB-NB)                primary
    C3 = mean(LGB-Q, HGB-Q, TSB-NB)         secondary
For every dataset × window (main, second = w26, third = w52) and h = 3, the default policy (L = 2, no
liquidation) is simulated over the τ grid. Reported:
    accuracy: wQL of the combinations and of their members;
    inventory needed at fill 0.90 / 0.92 / 0.94, relative to LGB-Q and to TSB-NB, with 95% bootstrap CIs over series;
    regret: excess inventory over the best of the seven single methods in the run, averaged over the fill targets
    0.90–0.98 the method reaches (the definition used in the paper); maximum over the six runs.
Writes code/outputs/combination.md and .csv.

Usage:
    python code/combination.py
"""
import os
import sys

import numpy as np
import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from equal_fill_ci import totals  # noqa: E402
from f2d import classify, config, data, policy  # noqa: E402
from f2d.features import Builder  # noqa: E402
from segment_eval import MODELS, TARGETS, curve, inv_at  # noqa: E402

WINDOWS = {"main": 0, "second": 26, "third": 52}
COMBOS = {"C2": ("lgb_quantile", "tsb_nb"), "C3": ("lgb_quantile", "hgb_quantile", "tsb_nb")}
EVAL = (0.90, 0.92, 0.94)
N_BOOT = 200
H = config.DEFAULT["L"] + config.DEFAULT["R"]
LAB = {"empirical": "EMP", "tsb_nb": "TSB-NB", "ets": "ETS", "lgb_tweedie": "LGB-T", "lgb_conformal": "LGB-C",
       "hgb_quantile": "HGB-Q", "lgb_quantile": "LGB-Q", "C2": "C2", "C3": "C3"}


def setup(name, offset):
    p = data.load(name)
    if offset:
        p = data.truncate(p, p["Y"].shape[1] - offset)
    Y = p["Y"]
    T = Y.shape[1]
    test0 = T - config.TEST_WEEKS
    sel = p["start"] <= test0 - config.VALID_WEEKS
    cls, _, _ = classify.classify(Y, p["start"], test0)
    sel &= cls != "none"
    return p, np.flatnonzero(sel), test0, T


def wql(Q, Dt, qs):
    e = Dt[:, :, None] - Q
    ok = ~np.isnan(Dt)[:, :, None] & ~np.isnan(Q)
    pin = np.where(ok, np.maximum(np.asarray(qs) * e, (np.asarray(qs) - 1) * e), 0.0)
    return pin.sum() / (len(qs) * np.nansum(np.where(ok.any(2), Dt, np.nan)))


def add_combos(tot, p, name, offset, idx, test0, T):
    """Simulate the combinations exactly as equal_fill_ci.totals simulates single methods; return their forecasts."""
    L = config.DEFAULT["L"]
    D = np.nan_to_num(p["Y"][:, test0:T]).astype(np.float64)[idx]
    w = slice(config.WARMUP_WEEKS, None)
    fc = os.path.join(config.CACHE, "forecasts", name + (f"_w{offset}" if offset else ""))
    qs = list(config.QUANTILES)
    Qs = {m: np.load(os.path.join(fc, f"{m}_h{H}.npz"))["Q"] for m in {m for c in COMBOS.values() for m in c}}
    for c, members in COMBOS.items():
        Qs[c] = np.mean([Qs[m] for m in members], axis=0)
        for tau in config.TAU_GRID:
            S = Qs[c][idx][:, :, qs.index(tau)]
            sim = policy.simulate(D, S, np.full_like(S, np.inf), L)
            tot[c, tau, "sales"] = sim["sales"][:, w].sum(1)
            tot[c, tau, "onhand"] = sim["on_hand_end"][:, w].sum(1)
    return Qs


def main():
    rng = np.random.default_rng(config.SEED)
    allm = MODELS + list(COMBOS)
    res, reg, acc = [], [], []
    for d in ("M5", "VN1"):
        for wname, off in WINDOWS.items():
            p, idx, test0, T = setup(d, off)
            tot = totals(d, off, MODELS)
            Qs = add_combos(tot, p, d, off, idx, test0, T)
            b = Builder(p)
            Dt = np.stack([b.target(o, H) for o in range(test0, T)], 1)[idx]
            qs = list(config.QUANTILES)
            acc.append(dict(dataset=d, window=wname, **{LAB[m]: wql(Qs[m][idx], Dt, qs) for m in Qs}))
            n = len(idx)
            curves = {m: curve(tot, np.array([m] * n)) for m in allm}
            need = pd.DataFrame({m: [inv_at(*curves[m], t) for t in TARGETS] for m in allm}, index=TARGETS)
            best = need[MODELS].min(axis=1)
            for m in allm:
                r = need[m] / best - 1
                reg.append(dict(dataset=d, window=wname, method=LAB[m], regret=r.mean(skipna=True),
                                targets_reached=int(r.notna().sum())))
            boots = [rng.integers(0, n, n) for _ in range(N_BOOT)]
            bc = {m: [curve(tot, np.array([m] * n), bi) for bi in boots] for m in ("lgb_quantile", "tsb_nb", "C2", "C3")}
            for m in ("tsb_nb", "C2", "C3"):
                row = dict(dataset=d, window=wname, method=LAB[m])
                for ref in ("lgb_quantile", "tsb_nb"):
                    if ref == m:
                        continue
                    for tg in EVAL:
                        v, rv = inv_at(*curves[m], tg), inv_at(*curves[ref], tg)
                        rel = np.array([inv_at(*bc[m][k], tg) / inv_at(*bc[ref][k], tg) - 1 for k in range(N_BOOT)])
                        ok = np.isfinite(rel)
                        key = f"vs_{LAB[ref]}_{tg:.2f}"
                        row[key] = v / rv - 1 if np.isfinite(v) and np.isfinite(rv) else np.nan
                        row[key + "_lo"], row[key + "_hi"] = (np.percentile(rel[ok], [2.5, 97.5]) if ok.mean() >= 0.95
                                                              else (np.nan, np.nan))
                res.append(row)
            for tg in EVAL:
                res.append(dict(dataset=d, window=wname, method="LGB-Q inventory", **{f"inv_{tg:.2f}": inv_at(*curves["lgb_quantile"], tg)}))
            print(d, wname, "done", flush=True)
    res, reg, acc = pd.DataFrame(res), pd.DataFrame(reg), pd.DataFrame(acc)
    res.to_csv(os.path.join(config.OUTPUTS, "combination.csv"), index=False)
    reg.to_csv(os.path.join(config.OUTPUTS, "combination_regret.csv"), index=False)

    def cell(r, key):
        v, lo, hi = r.get(key, np.nan), r.get(key + "_lo", np.nan), r.get(key + "_hi", np.nan)
        if not np.isfinite(v):
            return "—"
        return f"{100 * v:+.1f}" + (f" [{100 * lo:+.1f}, {100 * hi:+.1f}]" if np.isfinite(lo) else "")
    lines = ["# Quantile combination (generated by code/combination.py)", "",
             "C2 = mean of the LGB-Q and TSB-NB quantiles (primary); C3 = mean of LGB-Q, HGB-Q and TSB-NB (secondary). "
             "h = 3, L = 2, no liquidation. Δ in % with 95% bootstrap CI over series (negative = less inventory than the "
             "reference); '—' = fill target not reached.", "",
             "## 1. Accuracy (wQL, lower is better)", "", acc.round(4).to_markdown(index=False), "",
             "## 2. Inventory at equal fill rate", ""]
    for ref in ("LGB-Q", "TSB-NB"):
        lines += [f"### Relative to {ref}", "", "| dataset | window | method | fill 0.90 | fill 0.92 | fill 0.94 |", "|---|---|---|---|---|---|"]
        for _, r in res[res.method.isin(["TSB-NB", "C2", "C3"])].iterrows():
            if r.method == ref:
                continue
            lines.append(f"| {r.dataset} | {r.window} | {r.method} | " + " | ".join(cell(r, f"vs_{ref}_{tg:.2f}") for tg in EVAL) + " |")
        lines.append("")
    piv = reg.pivot_table(index="method", columns=["dataset", "window"], values="regret")
    piv["max"] = piv.max(axis=1)
    piv = (100 * piv).round(1).sort_values("max")
    reach = reg.pivot_table(index="method", columns=["dataset", "window"], values="targets_reached")
    lines += ["## 3. Regret (% excess inventory over the best of the seven single methods, mean over reached targets 0.90–0.98)", "",
              piv.to_markdown(), "", "Fill targets reached (of 5):", "", reach.to_markdown(), ""]
    with open(os.path.join(config.OUTPUTS, "combination.md"), "w", encoding="utf-8") as fh:
        fh.write("\n".join(lines))
    print("written code/outputs/combination.md")


if __name__ == "__main__":
    main()
