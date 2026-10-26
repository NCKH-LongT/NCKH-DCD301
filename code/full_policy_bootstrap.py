"""Full-policy cluster bootstrap of Table 7 (design: phase5_workflow.md, section 10, item 2).

The earlier intervals of Table 7 resampled clusters with the τ paths of the original sample held fixed. Here every
bootstrap replicate reruns the whole past-only policy: clusters are resampled (M5 items, VN1 warehouses, footwear
styles), the portfolio fill F_t is recomputed on the weighted sample, the weekly τ path
    τ_{t+1} = clip(τ_t + 0.5 · (0.92 − F_t), 0.5, 0.99)
is recalculated, and inventory is simulated again with it. Forecasts, policy (lost sales, L = 2), warm-up and τ_0 are
those of rev18 (τ_0 from code/outputs/robustness/prospective_tau.csv; τ_0 = target on the footwear panel). All methods
use the same replicate weights, so differences are paired. Replicate 0 is the original sample and must reproduce
Table 7. Replicates are simulated in batches as an [n series × batch] array.

Reported per case × method: achieved fill, inventory (weeks of demand), window violation (fill < target − 0.005),
Δ fill and Δ inventory vs LGB-Q with 95% percentile intervals from 2,000 replicates, and the same intervals from the
first 1,000 replicates as a stability check. Writes code/outputs/robustness/full_policy_bootstrap.{md,csv} and the
replicate-level file full_policy_bootstrap_reps.csv.gz. One checkpoint per case under robustness/fpb_parts/.

Usage:
    python code/full_policy_bootstrap.py
"""
import os
import sys
import time

import numpy as np
import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from f2d import config  # noqa: E402
from robust_common import LAB, WINDOWS, load_window  # noqa: E402

TARGET = 0.92
ETA = 0.5
N_REP = 2000
BATCH = 50
METHODS = ["lgb_quantile", "hgb_quantile", "tsb_nb", "C2", "E7-med"]
CASES = [("M5", "third", "second"), ("M5", "second", "main"), ("VN1", "third", "second"), ("VN1", "second", "main"),
         ("VNF", None, "main")]
CLUSTER = {"M5": "item_id", "VN1": "client_wh"}
QS = np.asarray(config.QUANTILES)
WU = config.WARMUP_WEEKS
L = config.DEFAULT["L"]


def simulate_batch(D, Qm, Wt, tau0):
    """D [n, W] demand, Qm [n, W, 5] quantiles, Wt [n, B] replicate weights, tau0 scalar.
    Returns per replicate: fill, inventory (weeks of demand) over the evaluation weeks, and the τ paths [W, B]."""
    n, W = D.shape
    B = Wt.shape[1]
    tau = np.full(B, tau0)
    ring = np.zeros((L + 1, n, B))
    taus = np.zeros((W, B))
    cs = np.zeros(B)
    cd = np.zeros(B)
    es = np.zeros(B)
    eo = np.zeros(B)
    ed = np.zeros(B)
    on_hand = None
    rows = np.arange(n)[:, None]
    for k in range(W):
        taus[k] = tau
        t = np.clip(tau, QS[0], QS[-1])
        j = np.minimum(np.searchsorted(QS, t, side="right") - 1, len(QS) - 2)
        w = (t - QS[j]) / (QS[j + 1] - QS[j])
        Qk = Qm[:, k, :]
        S = np.ceil((1 - w) * Qk[rows, j[None, :]] + w * Qk[rows, j[None, :] + 1])
        if on_hand is None:
            on_hand = S.copy()
        slot = k % (L + 1)
        on_hand += ring[slot]
        ring[slot] = 0
        ip = on_hand + ring.sum(0)
        order = np.maximum(S - ip, 0)
        ring[(k + L) % (L + 1)] += order
        sales = np.minimum(on_hand, D[:, k][:, None])
        on_hand -= sales
        ws = (Wt * sales).sum(0)
        wd = (Wt * D[:, k][:, None]).sum(0)
        cs += ws
        cd += wd
        if k >= WU:
            es += ws
            ed += wd
            eo += (Wt * on_hand).sum(0)
        tau = np.where(cd > 0, np.clip(tau + ETA * (TARGET - cs / np.maximum(cd, 1e-12)), QS[0], QS[-1]), tau)
    return es / ed, eo / ed, taus


def cluster_of(w, d):
    a = w["p"]["attrs"].iloc[w["idx"]].reset_index(drop=True)
    key = a["series_id"].str.split("_").str[0] if d == "VNF" else a[CLUSTER[d]]
    return pd.factorize(key)[0]


def run_case(d, src, dst, tau0s, seed):
    w = load_window(d, WINDOWS[dst] if d != "VNF" else 0)
    D = w["D"]
    grp = cluster_of(w, d)
    G = grp.max() + 1
    rng = np.random.default_rng(seed)
    counts = np.vstack([np.ones(G)] + [np.bincount(rng.integers(0, G, G), minlength=G) for _ in range(N_REP)])
    out = {m: {"fill": [], "inv": [], "tau_end": []} for m in METHODS}
    for b0 in range(0, len(counts), BATCH):
        Wt = counts[b0:b0 + BATCH][:, grp].T.astype(float)
        for m in METHODS:
            f, i, taus = simulate_batch(D, w["Q"][m], Wt, tau0s[m])
            out[m]["fill"].append(f)
            out[m]["inv"].append(i)
            out[m]["tau_end"].append(taus[-1])
    reps = []
    for m in METHODS:
        for key in out[m]:
            out[m][key] = np.concatenate(out[m][key])
        reps.append(pd.DataFrame({"dataset": d, "transition": f"{src} → {dst}" if src else "main (τ0 = target)",
                                  "method": LAB[m], "rep": np.arange(len(counts)), **out[m]}))
    return pd.concat(reps, ignore_index=True), G


def summarise(reps):
    rows = []
    for (d, tr), g in reps.groupby(["dataset", "transition"], sort=False):
        ref = g[g.method == "LGB-Q"].set_index("rep")
        for m, gm in g.groupby("method", sort=False):
            x = gm.set_index("rep")
            dfill = x.fill - ref.fill
            dinv = x.inv / ref.inv - 1
            boot = x.index > 0
            r = dict(dataset=d, transition=tr, method=m, fill=x.fill[0], inv=x.inv[0],
                     violation=bool(x.fill[0] < TARGET - 0.005), violation_share=float((x.fill[boot] < TARGET - 0.005).mean()),
                     d_fill=dfill[0], d_inv=dinv[0])
            for tag, sel in (("", boot), ("_1k", boot & (x.index <= 1000))):
                r[f"dfill_lo{tag}"], r[f"dfill_hi{tag}"] = np.percentile(dfill[sel], [2.5, 97.5])
                r[f"dinv_lo{tag}"], r[f"dinv_hi{tag}"] = np.percentile(dinv[sel], [2.5, 97.5])
            rows.append(r)
    return pd.DataFrame(rows)


def main():
    out = os.path.join(config.OUTPUTS, "robustness")
    parts = os.path.join(out, "fpb_parts")
    os.makedirs(parts, exist_ok=True)
    pt = pd.read_csv(os.path.join(out, "prospective_tau.csv"))
    inv_lab = {v: k for k, v in LAB.items()}
    clusters = {}
    for k, (d, src, dst) in enumerate(CASES):
        fn = os.path.join(parts, f"{d}_{src}_{dst}.csv.gz")
        if os.path.exists(fn):
            print(d, src, dst, "already done", flush=True)
            continue
        t0 = time.time()
        if d == "VNF":
            tau0s = {m: TARGET for m in METHODS}
        else:
            g = pt[(pt.dataset == d) & (pt.transition == f"{src} → {dst}") & (pt.target == TARGET)]
            tau0s = {inv_lab[r.method]: r.tau for r in g.itertuples()}
        reps, G = run_case(d, src, dst, tau0s, [config.SEED, k])
        reps.to_csv(fn, index=False)
        print(d, src, "→", dst, f"clusters {G}, {N_REP} replicates in {time.time() - t0:.0f}s", flush=True)
    reps = pd.concat([pd.read_csv(os.path.join(parts, f"{d}_{s}_{t}.csv.gz")) for d, s, t in CASES], ignore_index=True)
    reps.to_csv(os.path.join(out, "full_policy_bootstrap_reps.csv.gz"), index=False)
    res = summarise(reps)
    # comparison with the fixed-trajectory intervals and point values of rev18 (rolling_calibration.csv)
    rc = pd.read_csv(os.path.join(out, "rolling_calibration.csv"))
    rc = rc[(rc.eta == 0.5) & (rc.target == TARGET)][["dataset", "transition", "method", "fill", "d_inv", "lo", "hi"]]
    res = res.merge(rc.rename(columns={"fill": "fill_rev18", "d_inv": "d_inv_rev18", "lo": "fixed_lo", "hi": "fixed_hi"}),
                    on=["dataset", "transition", "method"], how="left")
    res.to_csv(os.path.join(out, "full_policy_bootstrap.csv"), index=False)
    pc = lambda v: "—" if not np.isfinite(v) else f"{100 * v:+.1f}"
    L_ = ["# Full-policy cluster bootstrap of Table 7 (generated by code/full_policy_bootstrap.py)", "",
          f"Design: phase5_workflow.md, section 10. Target fill {TARGET}; τ path recomputed in every replicate ({N_REP} "
          "replicates, paired across methods; clusters: M5 items, VN1 warehouses, footwear styles). Point values = original "
          "sample (must equal rev18). Intervals: 95% percentile; '1k' = first 1,000 replicates; 'fixed' = rev18 intervals "
          "with τ paths held fixed. viol share = share of replicates whose achieved fill is below target − 0.005.", "",
          "| case | method | fill (rev18) | viol share | Δ fill pt [CI] | ΔI % [full-policy CI] | ΔI CI 1k | ΔI CI fixed (rev18) |",
          "|---|---|---|---|---|---|---|---|"]
    for _, r in res.iterrows():
        if r.method == "LGB-Q":
            L_.append(f"| {r.dataset} {r.transition} | LGB-Q | {r.fill:.3f} ({r.fill_rev18:.3f}) | {100 * r.violation_share:.0f}% | ref | "
                      f"inv {r.inv:.2f} wk | | |")
            continue
        L_.append(f"| {r.dataset} {r.transition} | {r.method} | {r.fill:.3f} ({r.fill_rev18:.3f}) | {100 * r.violation_share:.0f}% | "
                  f"{pc(r.d_fill)} [{pc(r.dfill_lo)}, {pc(r.dfill_hi)}] | {pc(r.d_inv)} [{pc(r.dinv_lo)}, {pc(r.dinv_hi)}] | "
                  f"[{pc(r.dinv_lo_1k)}, {pc(r.dinv_hi_1k)}] | [{pc(r.fixed_lo)}, {pc(r.fixed_hi)}] |")
    dev = (res.fill - res.fill_rev18).abs().max()
    L_ += ["", f"Largest |fill(original) − fill(rev18)| = {dev:.2e} (reproduction check)."]
    with open(os.path.join(out, "full_policy_bootstrap.md"), "w", encoding="utf-8") as fh:
        fh.write("\n".join(L_) + "\n")
    print("written full_policy_bootstrap.md; max fill deviation from rev18", dev)


if __name__ == "__main__":
    main()
