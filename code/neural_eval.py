"""Evaluate the N-HiTS baseline (run_neural.py) against the seven methods and the combination C2.

Uses every dataset × window for which code/outputs/neural/<D>_w<offset>_nhits_h3.npz exists (copied to the
forecast cache if needed). For each run (h = 3, L = 2, no liquidation):
    accuracy: wQL and empirical coverage of each quantile;
    inventory needed at fill 0.90 / 0.92 / 0.94 relative to LGB-Q, with 95% bootstrap CIs over series;
    frontier rank among the eight single methods;
    regret: excess inventory over the best of the eight single methods, averaged over the reached targets
    0.90–0.98; maximum over the available runs (also for C2).
Writes code/outputs/neural_eval.md and .csv.

Usage:
    python code/neural_eval.py
"""
import os
import shutil
import sys

import numpy as np
import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from analyze_results import frontier_rank  # noqa: E402
from combination import add_combos, setup, wql  # noqa: E402
from equal_fill_ci import totals  # noqa: E402
from f2d import config  # noqa: E402
from f2d.features import Builder  # noqa: E402
from segment_eval import MODELS, TARGETS, curve, inv_at  # noqa: E402

SINGLE = MODELS + ["nhits"]
WINDOWS = {"main": 0, "second": 26, "third": 52}
EVAL = (0.90, 0.92, 0.94)
N_BOOT = 200
H = 3
LAB = {"empirical": "EMP", "tsb_nb": "TSB-NB", "ets": "ETS", "lgb_tweedie": "LGB-T", "lgb_conformal": "LGB-C",
       "hgb_quantile": "HGB-Q", "lgb_quantile": "LGB-Q", "nhits": "N-HiTS", "C2": "C2", "C3": "C3"}
NEURAL = os.path.join(config.ROOT, "code", "outputs", "neural")


def ensure_cache(d, off):
    src = os.path.join(NEURAL, f"{d}_w{off}_nhits_h{H}.npz")
    if not os.path.exists(src):
        return False
    dst_dir = os.path.join(config.CACHE, "forecasts", d + (f"_w{off}" if off else ""))
    dst = os.path.join(dst_dir, f"nhits_h{H}.npz")
    if not os.path.exists(dst):
        os.makedirs(dst_dir, exist_ok=True)
        shutil.copyfile(src, dst)
    return True


def main():
    rng = np.random.default_rng(config.SEED)
    acc, rel, reg, fr = [], [], [], []
    for d in ("M5", "VN1"):
        for wname, off in WINDOWS.items():
            if not ensure_cache(d, off):
                continue
            p, idx, test0, T = setup(d, off)
            tot = totals(d, off, SINGLE)
            Qs = add_combos(tot, p, d, off, idx, test0, T)
            fc = os.path.join(config.CACHE, "forecasts", d + (f"_w{off}" if off else ""))
            Qs["nhits"] = np.load(os.path.join(fc, f"nhits_h{H}.npz"))["Q"]
            b = Builder(p)
            Dt = np.stack([b.target(o, H) for o in range(test0, T)], 1)[idx]
            qs = list(config.QUANTILES)
            for m in ("nhits", "lgb_quantile", "hgb_quantile", "tsb_nb", "C2"):
                Q = Qs[m][idx]
                ok = ~np.isnan(Dt)
                acc.append(dict(dataset=d, window=wname, method=LAB[m], wQL=wql(Q, Dt, qs),
                                **{f"cover_{q}": float(np.mean((Dt <= Q[:, :, k])[ok])) for k, q in enumerate(qs)}))
            n = len(idx)
            allm = SINGLE + ["C2"]
            curves = {m: curve(tot, np.array([m] * n)) for m in allm}
            need = pd.DataFrame({m: [inv_at(*curves[m], t) for t in TARGETS] for m in allm}, index=TARGETS)
            ranks = frontier_rank(need[SINGLE].T)
            for m in SINGLE:
                fr.append(dict(dataset=d, window=wname, method=LAB[m], frontier_rank=ranks[m]))
            best = need[SINGLE].min(axis=1)
            for m in allm:
                r = need[m] / best - 1
                reg.append(dict(dataset=d, window=wname, method=LAB[m], regret=r.mean(skipna=True),
                                targets_reached=int(r.notna().sum())))
            boots = [rng.integers(0, n, n) for _ in range(N_BOOT)]
            bc = {m: [curve(tot, np.array([m] * n), bi) for bi in boots] for m in ("lgb_quantile", "nhits", "tsb_nb", "C2")}
            for m in ("nhits", "tsb_nb", "C2"):
                row = dict(dataset=d, window=wname, method=LAB[m])
                for tg in EVAL:
                    v, ref = inv_at(*curves[m], tg), inv_at(*curves["lgb_quantile"], tg)
                    x = np.array([inv_at(*bc[m][k], tg) / inv_at(*bc["lgb_quantile"][k], tg) - 1 for k in range(N_BOOT)])
                    okb = np.isfinite(x)
                    row[f"d_{tg:.2f}"] = v / ref - 1 if np.isfinite(v) and np.isfinite(ref) else np.nan
                    row[f"lo_{tg:.2f}"], row[f"hi_{tg:.2f}"] = (np.percentile(x[okb], [2.5, 97.5]) if okb.mean() >= 0.95
                                                                else (np.nan, np.nan))
                rel.append(row)
            print(d, wname, "evaluated", flush=True)
    acc, rel, reg, fr = map(pd.DataFrame, (acc, rel, reg, fr))
    rel.to_csv(os.path.join(config.OUTPUTS, "neural_eval.csv"), index=False)
    reg.to_csv(os.path.join(config.OUTPUTS, "neural_eval_regret.csv"), index=False)

    def cell(r, tg):
        v, lo, hi = r[f"d_{tg:.2f}"], r[f"lo_{tg:.2f}"], r[f"hi_{tg:.2f}"]
        if not np.isfinite(v):
            return "—"
        return f"{100 * v:+.1f}" + (f" [{100 * lo:+.1f}, {100 * hi:+.1f}]" if np.isfinite(lo) else "")
    lines = ["# N-HiTS baseline (generated by code/neural_eval.py)", "",
             "h = 3, L = 2, no liquidation. Runs available: " + ", ".join(sorted({f"{a} {b}" for a, b in zip(acc.dataset, acc.window)})) + ".",
             "", "## 1. Accuracy (wQL) and empirical coverage of each quantile", "",
             acc.round(4).to_markdown(index=False), "",
             "## 2. Inventory at equal fill rate relative to LGB-Q (%, 95% bootstrap CI; positive = LGB-Q needs less)", "",
             "| dataset | window | method | fill 0.90 | fill 0.92 | fill 0.94 |", "|---|---|---|---|---|---|"]
    lines += [f"| {r.dataset} | {r.window} | {r.method} | " + " | ".join(cell(r, tg) for tg in EVAL) + " |" for _, r in rel.iterrows()]
    lines += ["", "## 3. Frontier rank among the eight single methods (1 = least inventory)", "",
              fr.pivot_table(index="method", columns=["dataset", "window"], values="frontier_rank").round(1).to_markdown(), ""]
    piv = reg.pivot_table(index="method", columns=["dataset", "window"], values="regret")
    piv["max"] = piv.max(axis=1)
    lines += ["## 4. Regret (% excess over the best of the eight single methods; mean over reached targets 0.90–0.98)", "",
              (100 * piv).round(1).sort_values("max").to_markdown(), "",
              "Fill targets reached (of 5):", "",
              reg.pivot_table(index="method", columns=["dataset", "window"], values="targets_reached").to_markdown(), ""]
    with open(os.path.join(config.OUTPUTS, "neural_eval.md"), "w", encoding="utf-8") as fh:
        fh.write("\n".join(lines))
    print("written code/outputs/neural_eval.md")


if __name__ == "__main__":
    main()
