"""Per-quantile scaled pinball loss by demand class, h = L + R = 3 (check of the §5.4 reading in results.md).

For each series: mean over test origins of the pinball loss at quantile q, scaled by h · mean|Δy| as in SQL
(evaluate.forecast_metrics). Reports, per dataset × window × class × q, the mean and median over series and the
share of series where lgb_quantile has a lower loss than tsb_nb. Writes code/outputs/per_quantile_loss.csv.

Usage:
    python code/per_quantile_loss.py
"""
import os
import sys

import numpy as np
import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from f2d import classify, config, data, evaluate  # noqa: E402
from f2d.features import Builder  # noqa: E402

MODELS = ["tsb", "tsb_nb", "hgb_quantile", "lgb_quantile"]
CLASSES = ["all", "smooth", "erratic", "intermittent", "lumpy"]


def run(name, offset, h):
    p = data.load(name)
    if offset:
        p = data.truncate(p, p["Y"].shape[1] - offset)
    Y = p["Y"]
    T = Y.shape[1]
    test0 = T - config.TEST_WEEKS
    origins = list(range(test0, T))
    sel = p["start"] <= test0 - config.VALID_WEEKS
    cls, _, _ = classify.classify(Y, p["start"], test0)
    sel &= cls != "none"
    idx = np.flatnonzero(sel)
    s_abs, _ = evaluate.naive_scales(Y, p["start"], test0)
    b = Builder(p)
    qs = np.asarray(config.QUANTILES)
    Dt = np.stack([b.target(o, h) for o in origins], 1)
    fc = os.path.join(config.CACHE, "forecasts", name + (f"_w{offset}" if offset else ""))
    loss = {}
    for m in MODELS:
        Q = np.load(os.path.join(fc, f"{m}_h{h}.npz"))["Q"]
        e = Dt[:, :, None] - Q
        ok = ~np.isnan(Dt)[:, :, None] & ~np.isnan(Q)
        pin = np.where(ok, np.maximum(qs * e, (qs - 1) * e), np.nan)
        with np.errstate(all="ignore"):
            l = np.nanmean(pin, axis=1) / (h * s_abs[:, None])          # series × quantile
        l[~((s_abs > 0)[:, None] & np.isfinite(l))] = np.nan
        loss[m] = l[idx]
    c = cls[idx]
    rows = []
    for g in CLASSES:
        mask = np.ones(len(c), bool) if g == "all" else c == g
        for j, q in enumerate(qs):
            r = dict(dataset=name, window=f"w{offset}" if offset else "main", h=h, group=g, q=q)
            for m in MODELS:
                v = loss[m][mask, j]
                r[f"mean_{m}"] = np.nanmean(v)
                r[f"median_{m}"] = np.nanmedian(v)
            a, t = loss["lgb_quantile"][mask, j], loss["tsb_nb"][mask, j]
            ok2 = np.isfinite(a) & np.isfinite(t)
            r["n_series"] = int(ok2.sum())
            r["lgbq_better_than_tsbnb_share"] = np.mean(a[ok2] < t[ok2])
            rows.append(r)
    return pd.DataFrame(rows)


def main():
    h = config.DEFAULT["L"] + config.DEFAULT["R"]
    out = pd.concat([run("M5", 0, h), run("VN1", 0, h), run("M5", 26, h), run("VN1", 26, h)])
    path = os.path.join(config.OUTPUTS, "per_quantile_loss.csv")
    out.to_csv(path, index=False)
    cols = ["dataset", "window", "group", "q", "mean_lgb_quantile", "mean_tsb_nb", "median_lgb_quantile",
            "median_tsb_nb", "lgbq_better_than_tsbnb_share"]
    pd.set_option("display.width", 250, "display.max_rows", 500)
    print(out[cols].round(3).to_string(index=False))
    print("written:", path)


if __name__ == "__main__":
    main()
