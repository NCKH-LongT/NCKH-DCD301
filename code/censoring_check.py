"""How much of the recorded demand may be censored by stock-outs? (reviewer comment, ICIIT revision item 2).

The benchmark uses sales as demand, so weeks with a stock-out record a sale of zero (or a too-low sale). The
datasets have no stock records, so stock-outs cannot be observed; this script estimates how often they are
plausible from the sales alone and where they concentrate.

Detector (per series, no stock data). A zero run is a maximal run of k ≥ 2 consecutive zero-sale weeks with a
positive sale both before and after it (so leading zeros, end-of-life and the end of the panel are excluded). Let p
be the share of weeks with a sale in the series' history before the test period. If sales were independent with
that frequency, a run of k zeros would occur with probability (1 − p)^k; the run is flagged as a suspected stock-out
when (1 − p)^k < α (default α = 0.01, also 0.05 and 0.001). p includes the runs themselves, which lowers p and makes
the detector conservative. The detector also flags genuine demand pauses (e.g. seasonal items), so the shares are
an upper-bound indication, not a measurement.

Reported for every dataset × test window (main, w26, w52), for the history before the test period and for the
26-week test period separately, overall and by ADI–CV² class (classes as in run_pipeline.py):
    series_share        share of evaluated series with at least one suspected run
    week_share          share of active series-weeks inside suspected runs
    hidden_demand_share demand that would have been sold in those weeks at the series' mean weekly rate before the
                        test period, as a share of recorded sales (a rough size of the censoring)
Series selection is the one of run_pipeline.py (≥ 13 weeks of history before the test period, at least one sale).

Writes code/outputs/censoring_check.csv and censoring_check.md.

Usage:
    python code/censoring_check.py
    python code/censoring_check.py --datasets M5 --offsets 0
"""
import argparse
import os
import sys

import numpy as np
import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from f2d import classify, config, data  # noqa: E402

ALPHAS = (0.05, 0.01, 0.001)
MAIN_ALPHA = 0.01
WINDOWS = {0: "main", 26: "second", 52: "third"}
GROUPS = ("all",) + classify.CLASSES


def interior_zero_runs(y):
    """(start, length) of the zero runs of y that have a positive value before and after them."""
    pos = np.flatnonzero(y > 0)
    if len(pos) < 2:
        return np.empty(0, int), np.empty(0, int)
    gap = np.diff(pos) - 1                     # zeros between consecutive sales
    k = gap > 0
    return pos[:-1][k] + 1, gap[k]


def flag_weeks(Y, start, test0, alpha):
    """Boolean [n, T]: week inside a suspected stock-out run. Also returns p (sale frequency before test0)."""
    n, T = Y.shape
    Y0 = np.nan_to_num(Y)
    t = np.arange(T)[None, :]
    hist = (t >= start[:, None]) & (t < test0)
    p = ((Y0 > 0) & hist).sum(1) / np.maximum(hist.sum(1), 1)
    F = np.zeros((n, T), bool)
    with np.errstate(divide="ignore"):
        log_q = np.log1p(-np.minimum(p, 1 - 1e-12))   # log(1 − p)
    for i in range(n):
        if p[i] <= 0:
            continue
        s0, k = interior_zero_runs(Y0[i, start[i]:])
        if not len(k):
            continue
        sus = (k >= 2) & (k * log_q[i] < np.log(alpha))
        for a, b in zip(s0[sus], k[sus]):
            F[i, start[i] + a: start[i] + a + b] = True
    return F, p


def summarise(Y, F, start, test0, sel, cls, rate):
    """Rows of the three shares by period × group."""
    T = Y.shape[1]
    t = np.arange(T)[None, :]
    act = ~np.isnan(Y)
    Y0 = np.nan_to_num(Y)
    periods = {"history": (t >= start[:, None]) & (t < test0), "test": (t >= test0) & act}
    rows = []
    for per, M in periods.items():
        M = M & act
        for g in GROUPS:
            m = sel if g == "all" else sel & (cls == g)
            if not m.any():
                continue
            Fm, Mm = F[m] & M[m], M[m]
            sales = (Y0[m] * Mm).sum()
            rows.append(dict(period=per, group=g, n_series=int(m.sum()),
                             series_share=float(Fm.any(1).mean()),
                             week_share=float(Fm.sum() / max(Mm.sum(), 1)),
                             hidden_demand_share=float((Fm.sum(1) * rate[m]).sum() / max(sales, 1e-9))))
    return rows


def run(name, offset):
    p = data.load(name)
    if offset:
        p = data.truncate(p, p["Y"].shape[1] - offset)
    Y = p["Y"].astype(np.float64)
    T = Y.shape[1]
    test0 = T - config.TEST_WEEKS
    start = p["start"].astype(int)
    sel = start <= test0 - config.VALID_WEEKS
    cls, _, _ = classify.classify(Y, p["start"], test0)
    sel &= cls != "none"
    # mean weekly demand before the test period (used to size the hidden demand)
    t = np.arange(T)[None, :]
    hist = (t >= start[:, None]) & (t < test0)
    rate = (np.nan_to_num(Y) * hist).sum(1) / np.maximum(hist.sum(1), 1)
    out = []
    for alpha in ALPHAS:
        F, _ = flag_weeks(Y, start, test0, alpha)
        for r in summarise(Y, F, start, test0, sel, cls, rate):
            out.append(dict(dataset=name, window=WINDOWS.get(offset, f"w{offset}"), alpha=alpha, **r))
    print(f"{name} {WINDOWS.get(offset, offset)}: {int(sel.sum()):,} series", flush=True)
    return out


def pct(x):
    return f"{100 * x:.1f}%"


def write_md(df, path):
    m = df[df.alpha == MAIN_ALPHA]
    lines = ["# Suspected stock-outs in the sales data (generated by code/censoring_check.py)", "",
             "Sales are used as demand. A zero run (k ≥ 2 zero weeks between two sales) is flagged as a suspected "
             f"stock-out when (1 − p)^k < α, p = share of weeks with a sale before the test period; α = {MAIN_ALPHA} "
             "unless stated. The detector also flags genuine pauses in demand, so the shares are an upper-bound "
             "indication, not a measurement.", "",
             "- **series**: share of evaluated series with at least one suspected run",
             "- **weeks**: share of active series-weeks inside suspected runs",
             "- **hidden demand**: demand those weeks would carry at the series' mean weekly rate before the test "
             "period, as a share of recorded sales", ""]
    lines += ["## 1. All series, by dataset, window and period", ""]
    a = m[m.group == "all"]
    t = a.assign(series=a.series_share.map(pct), weeks=a.week_share.map(pct),
                 hidden_demand=a.hidden_demand_share.map(pct))[
        ["dataset", "window", "period", "n_series", "series", "weeks", "hidden_demand"]]
    lines += [t.to_markdown(index=False), ""]
    lines += ["## 2. By ADI–CV² class, test period", ""]
    for d in df.dataset.unique():
        s = m[(m.dataset == d) & (m.period == "test") & (m.group != "all")]
        piv = s.pivot(index="group", columns="window", values="week_share").reindex(classify.CLASSES)
        piv = piv[[w for w in WINDOWS.values() if w in piv.columns]].map(pct)
        hd = s.pivot(index="group", columns="window", values="hidden_demand_share").reindex(classify.CLASSES)
        hd = hd[[w for w in WINDOWS.values() if w in hd.columns]].map(pct)
        lines += [f"### {d}: share of weeks inside suspected runs", "", piv.to_markdown(), "",
                  f"### {d}: hidden demand as a share of recorded sales", "", hd.to_markdown(), ""]
    lines += ["## 3. Sensitivity to α (all series, main window)", ""]
    s = df[(df.group == "all") & (df.window == "main")]
    piv = s.pivot_table(index=["dataset", "period"], columns="alpha", values="week_share")
    lines += ["Share of weeks inside suspected runs:", "", piv.map(pct).to_markdown(), ""]
    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--datasets", default="M5,VN1")
    ap.add_argument("--offsets", default="0,26,52")
    a = ap.parse_args()
    rows = []
    for d in a.datasets.split(","):
        for o in (int(x) for x in a.offsets.split(",")):
            rows += run(d, o)
    df = pd.DataFrame(rows)
    os.makedirs(config.OUTPUTS, exist_ok=True)
    df.to_csv(os.path.join(config.OUTPUTS, "censoring_check.csv"), index=False)
    write_md(df, os.path.join(config.OUTPUTS, "censoring_check.md"))
    print("written", os.path.join(config.OUTPUTS, "censoring_check.md"))


if __name__ == "__main__":
    main()
