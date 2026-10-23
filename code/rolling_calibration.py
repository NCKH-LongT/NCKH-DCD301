"""P0 rolling τ calibration and P1 independent validation on VNF (design: phase5_workflow.md, section 9).

Rolling calibration: inside the target window τ is updated after every week from observed outcomes only,
    τ_{k+1} = clip(τ_k + η · (target − F_k), 0.5, 0.99),   F_k = portfolio fill from the window start to week k,
with the same lost-sales order-up-to dynamics as f2d.policy.simulate (no liquidation, L = 2). τ_0 = τ* chosen on the
previous window (code/outputs/robustness/prospective_tau.csv) for M5 and VN1; τ_0 = target on VNF. η = 0.5 is the
primary setting, 0.25 and 1.0 are sensitivity checks; η = 0 reproduces the static τ*.
Reported on the 22 evaluation weeks: fill, |fill − target|, window violation (fill < target − 0.005), share of weeks
whose trailing 4-week fill is below target, inventory, Δ inventory vs LGB-Q with 95% cluster-bootstrap intervals
(τ paths held fixed; clusters: M5 item, VN1 warehouse, VNF style).
VNF also gets the paper's equal-fill comparison with series and style-cluster bootstraps (1,000 resamples).
Writes code/outputs/robustness/rolling_calibration.md / .csv and vnf_validation.md / .csv.

Usage:
    python code/rolling_calibration.py
"""
import os
import sys

import numpy as np
import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from f2d import config  # noqa: E402
from robust_common import LAB, METHODS, WINDOWS, load_window, run  # noqa: E402

TARGETS = (0.92, 0.94)
ETAS = (0.5, 0.25, 1.0, 0.0)
TRANSITIONS = [("third", "second"), ("second", "main")]
CLUSTER = {"M5": "item_id", "VN1": "client_wh", "VNF": "style"}
N_BOOT = 1000
QS = np.asarray(config.QUANTILES)
WU = config.WARMUP_WEEKS


def level_col(Qm, tau, k):
    tau = float(np.clip(tau, QS[0], QS[-1]))
    j = min(int(np.searchsorted(QS, tau, side="right")) - 1, len(QS) - 2)
    w = (tau - QS[j]) / (QS[j + 1] - QS[j])
    return (1 - w) * Qm[:, k, j] + w * Qm[:, k, j + 1]


def simulate_rolling(D, Qm, tau0, target, eta, L=config.DEFAULT["L"]):
    n, W = D.shape
    tau = tau0
    on_hand = np.ceil(level_col(Qm, tau, 0))
    pipe = np.zeros((n, W + L + 1))
    sales_w, onh_w, taus = np.zeros((n, W)), np.zeros((n, W)), []
    cs = cd = 0.0
    for k in range(W):
        taus.append(tau)
        S = np.ceil(level_col(Qm, tau, k))
        on_hand += pipe[:, k]
        ip = on_hand + pipe[:, k + 1: k + L + 1].sum(1)
        order = np.maximum(S - ip, 0)
        pipe[:, k + L] += order
        sales = np.minimum(on_hand, D[:, k])
        on_hand -= sales
        sales_w[:, k], onh_w[:, k] = sales, on_hand
        cs += sales.sum()
        cd += D[:, k].sum()
        if cd > 0:
            tau = float(np.clip(tau + eta * (target - cs / cd), QS[0], QS[-1]))
    return sales_w, onh_w, np.array(taus)


def metrics(D, s, o, target):
    De, se, oe = D[:, WU:], s[:, WU:], o[:, WU:]
    fill = se.sum() / De.sum()
    wk_d, wk_s = De.sum(0), se.sum(0)
    trail = np.array([wk_s[max(0, k - 3):k + 1].sum() / max(wk_d[max(0, k - 3):k + 1].sum(), 1e-9) for k in range(len(wk_d))])
    return dict(fill=fill, abs_err=abs(fill - target), window_violation=fill < target - 0.005,
                weeks_below=(trail < target).mean(), inv=oe.sum() / De.sum())


def cluster_ids(w, d):
    a = w["p"]["attrs"].iloc[w["idx"]].reset_index(drop=True)
    key = a["series_id"].str.split("_").str[0] if d == "VNF" else a[CLUSTER[d]]
    return pd.factorize(key)[0]


def boot_ratio(onh_m, onh_r, grp, rng):
    G = grp.max() + 1
    a, b = np.bincount(grp, weights=onh_m, minlength=G), np.bincount(grp, weights=onh_r, minlength=G)
    C = np.stack([np.bincount(rng.integers(0, G, G), minlength=G) for _ in range(N_BOOT)]).astype(float)
    x = (C @ a) / (C @ b) - 1
    return np.percentile(x, [2.5, 97.5])


def rolling_rows(d, tr, w_dst, tau0s, rng, grp):
    rows = []
    D = w_dst["D"]
    for target in TARGETS:
        for eta in ETAS:
            res = {}
            for m in METHODS:
                s, o, taus = simulate_rolling(D, w_dst["Q"][m], tau0s[m, target], target, eta)
                res[m] = (s, o, taus, metrics(D, s, o, target))
            ref = res["lgb_quantile"]
            for m in METHODS:
                s, o, taus, mt = res[m]
                r = dict(dataset=d, transition=tr, target=target, eta=eta, method=LAB[m], tau0=tau0s[m, target],
                         tau_end=taus[-1], **mt, d_fill=mt["fill"] - ref[3]["fill"], d_inv=mt["inv"] / ref[3]["inv"] - 1)
                if eta == 0.5 and m != "lgb_quantile":
                    r["lo"], r["hi"] = boot_ratio(o[:, WU:].sum(1), ref[1][:, WU:].sum(1), grp, rng)
                rows.append(r)
    return rows


def vnf_equal_fill(w, grp, rng):
    """Paper metric on VNF: inventory at equal realised fill, series and style-cluster bootstraps."""
    D = w["D"]
    dem = D[:, WU:].sum(1)
    tot = {}
    for m in METHODS:
        for t in config.TAU_GRID:
            s, o = run(D, w["Q"][m][:, :, list(QS).index(t)])
            tot[m, t] = (s.sum(1), o.sum(1))

    def curve(wts, m):
        dd = wts @ dem
        f = np.maximum.accumulate(np.array([(wts @ tot[m, t][0]) / dd for t in config.TAU_GRID]))
        i = np.array([(wts @ tot[m, t][1]) / dd for t in config.TAU_GRID])
        return f, i

    def inv_at(f, i, tg):
        return np.interp(tg, f, i) if f.min() <= tg <= f.max() else np.nan
    n = len(dem)
    ones = np.ones(n)
    rows = []
    G = grp.max() + 1
    draws = {"series": [np.bincount(rng.integers(0, n, n), minlength=n) for _ in range(N_BOOT)],
             "cluster:style": [np.bincount(rng.integers(0, G, G), minlength=G)[grp] for _ in range(N_BOOT)]}
    for m in METHODS:
        for tg in TARGETS:
            v, r = inv_at(*curve(ones, m), tg), inv_at(*curve(ones, "lgb_quantile"), tg)
            row = dict(method=LAB[m], target=tg, d=v / r - 1 if np.isfinite(v) and np.isfinite(r) else np.nan)
            if m in ("C2", "E7-med", "tsb_nb", "hgb_quantile"):
                for name, ws in draws.items():
                    x = np.array([inv_at(*curve(wt, m), tg) / inv_at(*curve(wt, "lgb_quantile"), tg) - 1 for wt in ws])
                    ok = np.isfinite(x)
                    row[name] = tuple(np.percentile(x[ok], [2.5, 97.5])) if ok.mean() >= 0.95 else (np.nan, np.nan)
            rows.append(row)
    return pd.DataFrame(rows)


def main():
    rng = np.random.default_rng(config.SEED)
    out = os.path.join(config.OUTPUTS, "robustness")
    pt = pd.read_csv(os.path.join(out, "prospective_tau.csv"))
    inv_lab = {v: k for k, v in LAB.items()}
    parts = os.path.join(out, "rolling_parts")
    os.makedirs(parts, exist_ok=True)
    # one checkpoint file per (dataset, transition): a crashed run resumes where it stopped
    for d in ("M5", "VN1"):
        for src, dst in TRANSITIONS:
            tr = f"{src} → {dst}"
            fn = os.path.join(parts, f"{d}_{src}_{dst}.csv")
            if os.path.exists(fn):
                print(d, tr, "already done", flush=True)
                continue
            w = load_window(d, WINDOWS[dst])          # only the target window is needed (τ0 comes from the csv)
            g = pt[(pt.dataset == d) & (pt.transition == tr)]
            tau0s = {(inv_lab[r.method], r.target): r.tau for r in g.itertuples()}
            pd.DataFrame(rolling_rows(d, tr, w, tau0s, np.random.default_rng([config.SEED, len(d), len(src)]),
                                      cluster_ids(w, d))).to_csv(fn, index=False)
            del w
            print(d, tr, "done", flush=True)
    wv = load_window("VNF", 0)
    gv = cluster_ids(wv, "VNF")
    fn = os.path.join(parts, "VNF_main.csv")
    if not os.path.exists(fn):
        pd.DataFrame(rolling_rows("VNF", "main (τ0 = target)", wv, {(m, t): t for m in METHODS for t in TARGETS},
                                  np.random.default_rng([config.SEED, 3]), gv)).to_csv(fn, index=False)
    order = [f"{d}_{s}_{t}.csv" for d in ("M5", "VN1") for s, t in TRANSITIONS] + ["VNF_main.csv"]
    res = pd.concat([pd.read_csv(os.path.join(parts, x)) for x in order], ignore_index=True)
    res.to_csv(os.path.join(out, "rolling_calibration.csv"), index=False)
    ef = vnf_equal_fill(wv, gv, rng)
    ef.to_csv(os.path.join(out, "vnf_validation.csv"), index=False)
    print("VNF done", flush=True)

    ci = lambda r: "" if not np.isfinite(r.get("lo", np.nan)) else f" [{100 * r['lo']:+.1f}, {100 * r['hi']:+.1f}]"
    L = ["# Rolling τ calibration (generated by code/rolling_calibration.py)", "",
         "Design: phase5_workflow.md, section 9. η = 0.5 primary; η = 0 = static τ chosen on the previous window. "
         "viol = window fill below target − 0.005; wk<t = share of evaluation weeks with trailing 4-week fill below target. "
         "Δ inv vs LGB-Q with 95% cluster-bootstrap interval (M5 item, VN1 warehouse, VNF style), τ paths fixed.", ""]
    for (d, tr, tg), g in res.groupby(["dataset", "transition", "target"], sort=False):
        L += [f"## {d} · {tr} · target {tg}", "", "| method | η | τ0 → τ end | fill | |err| | viol | wk<t | inv | Δ fill | Δ inv vs LGB-Q |",
              "|---|---|---|---|---|---|---|---|---|---|"]
        for _, r in g[g.eta.isin([0.5, 0.0])].sort_values(["eta", "method"], ascending=[False, True]).iterrows():
            L.append(f"| {r.method} | {r.eta} | {r.tau0:.3f} → {r.tau_end:.3f} | {r.fill:.3f} | {100 * r.abs_err:.1f} pt | "
                     f"{'yes' if r.window_violation else 'no'} | {100 * r.weeks_below:.0f}% | {r.inv:.2f} | {100 * r.d_fill:+.1f} pt | "
                     f"{100 * r.d_inv:+.1f}%{ci(r)} |")
        L.append("")
    sens = res[res.method.isin(["LGB-Q", "HGB-Q", "C2", "E7-med"])].groupby(["dataset", "eta"]).abs_err.max().unstack()
    L += ["## Largest |fill − target| (points) of LGB-Q, HGB-Q, C2, E7-med by η", "", (100 * sens).round(1).to_markdown(), ""]
    with open(os.path.join(out, "rolling_calibration.md"), "w", encoding="utf-8") as fh:
        fh.write("\n".join(L))
    V = ["# Independent validation on VNF (generated by code/rolling_calibration.py)", "",
         "Frozen specifications (E7-med = median, C2 = mean of LGB-Q and TSB-NB). Inventory at equal realised fill, "
         "Δ vs LGB-Q in %, 95% bootstraps (1,000) over series and over styles.", "",
         "| method | fill | Δ vs LGB-Q | series CI | style-cluster CI |", "|---|---|---|---|---|"]
    fmt = lambda c: "—" if not isinstance(c, tuple) or not np.isfinite(c[0]) else f"[{100 * c[0]:+.1f}, {100 * c[1]:+.1f}]"
    for _, r in ef.iterrows():
        V.append(f"| {r.method} | {r.target} | {'—' if not np.isfinite(r.d) else f'{100 * r.d:+.1f}%'} | "
                 f"{fmt(r.get('series'))} | {fmt(r.get('cluster:style'))} |")
    with open(os.path.join(out, "vnf_validation.md"), "w", encoding="utf-8") as fh:
        fh.write("\n".join(V) + "\n")
    print("written rolling_calibration.md and vnf_validation.md")


if __name__ == "__main__":
    main()
