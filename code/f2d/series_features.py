"""Per-series descriptive features computed from the history before a cut-off week (phase 2: B1–B4).

Every feature uses weeks [start_i, cutoff) only, so the table can be used for ex-ante segmentation without
leaking the test period. `start` can be overridden to compare series-start definitions between datasets.
"""
import numpy as np
import pandas as pd

FEATURES = ["log_mean", "log_size", "adi", "cv2", "zero_share", "since_sale", "hist_len", "trend_26",
            "recent_ratio_13", "acf_52", "max_share", "peak_ratio_52", "price_cv"]
# features that do not depend on dataset-specific information (prices, length of the panel). max_share is left
# out because it shrinks mechanically with the length of the history; peak_ratio_52 uses a fixed 52-week window.
SHARED = ["log_mean", "log_size", "adi", "cv2", "zero_share", "since_sale", "trend_26", "recent_ratio_13", "peak_ratio_52"]
EPS = 0.1


def series_features(panel, cutoff, start=None):
    """DataFrame [n_series × FEATURES] from weeks [start, cutoff). Series without a sale before the cut-off
    get NaN in the demand features."""
    Y = np.nan_to_num(panel["Y"][:, :cutoff]).astype(np.float64)
    P = panel["P"][:, :cutoff].astype(np.float64)
    st = (panel["start"] if start is None else start).astype(np.int64)
    n = Y.shape[0]
    t = np.arange(cutoff)[None, :]
    act = t >= st[:, None]
    Y = np.where(act, Y, 0.0)
    n_act = act.sum(1)
    pos = Y > 0
    nnz = pos.sum(1)
    tot = Y.sum(1)
    with np.errstate(all="ignore"):
        mean = tot / n_act
        size = tot / nnz
        var_size = (Y ** 2).sum(1) / nnz - size ** 2
        cv2 = var_size / size ** 2
        adi = n_act / nnz
        idx = np.where(pos, t, -1).max(1)
        since = np.where(idx >= 0, cutoff - 1 - idx, np.nan)

        def win_mean(a, b):
            w = act & (t >= a) & (t < b)
            c = w.sum(1)
            return np.where(c > 0, np.where(w, Y, 0).sum(1) / np.maximum(c, 1), np.nan)

        m_last26, m_prev26 = win_mean(cutoff - 26, cutoff), win_mean(cutoff - 52, cutoff - 26)
        trend = np.log((m_last26 + EPS) / (m_prev26 + EPS))
        recent = np.log((win_mean(cutoff - 13, cutoff) + EPS) / (mean + EPS))
        # seasonal autocorrelation at lag 52 over the last 104 weeks (needs 104 active weeks)
        acf = np.full(n, np.nan)
        if cutoff >= 104:
            a, b = Y[:, cutoff - 52:cutoff], Y[:, cutoff - 104:cutoff - 52]
            ok = n_act >= 104
            ac, bc = a - a.mean(1, keepdims=True), b - b.mean(1, keepdims=True)
            den = np.sqrt((ac ** 2).sum(1) * (bc ** 2).sum(1))
            acf = np.where(ok & (den > 0), (ac * bc).sum(1) / np.where(den > 0, den, 1), np.nan)
        max_share = Y.max(1) / tot
        # largest week of the last 52 weeks relative to the mean positive sale of the same weeks (bulk-order signal)
        w52 = act & (t >= cutoff - 52)
        y52 = np.where(w52, Y, 0.0)
        n52 = (y52 > 0).sum(1)
        peak = np.where(n52 > 0, np.log(y52.max(1) / np.where(n52 > 0, y52.sum(1) / np.maximum(n52, 1), 1)), np.nan)
        Pm = np.where(act & np.isfinite(P), P, np.nan)
        price_cv = np.nanstd(Pm, 1) / np.nanmean(Pm, 1)
    f = pd.DataFrame({
        "log_mean": np.log1p(mean), "log_size": np.log1p(size), "adi": adi, "cv2": cv2,
        "zero_share": 1 - nnz / np.maximum(n_act, 1), "since_sale": since, "hist_len": n_act.astype(float),
        "trend_26": trend, "recent_ratio_13": recent, "acf_52": acf, "max_share": max_share, "peak_ratio_52": peak,
        "price_cv": price_cv})
    f.loc[nnz == 0, [c for c in FEATURES if c not in ("hist_len",)]] = np.nan
    return f[FEATURES]
