"""Load M5 and VN1 into a common weekly panel.

A panel is a dict with
    Y      float32 [n_series, n_weeks]  observed weekly sales (>= 0, NaN before series start)
    P      float32 [n_series, n_weeks]  weekly price (forward-filled within series; NaN if unknown)
    Pobs   bool    [n_series, n_weeks]  True where the price was actually observed
    weeks  DatetimeIndex                week start dates
    start  int32   [n_series]           index of the first active week of each series
    attrs  DataFrame                    one row per series (series_id + static categorical attributes)
    events float32 [n_weeks, n_ev]      calendar covariates known in advance (may have 0 columns)
"""
import os

import numpy as np
import pandas as pd

from . import config


def _ffill_rows(a):
    """Forward-fill NaNs along axis 1 (per series)."""
    mask = np.isnan(a)
    idx = np.where(~mask, np.arange(a.shape[1]), 0)
    np.maximum.accumulate(idx, axis=1, out=idx)
    out = a[np.arange(a.shape[0])[:, None], idx]
    out[np.cumsum(~mask, axis=1) == 0] = np.nan
    return out


def load_m5():
    cache = os.path.join(config.CACHE, "panel_m5.npz")
    sales = pd.read_csv(os.path.join(config.M5_DIR, "sales_train_evaluation.csv"))
    cal = pd.read_csv(os.path.join(config.M5_DIR, "calendar.csv"))
    attrs = sales[["id", "item_id", "dept_id", "cat_id", "store_id", "state_id"]].rename(columns={"id": "series_id"})
    if os.path.exists(cache):
        z = np.load(cache, allow_pickle=True)
        return dict(Y=z["Y"], P=z["P"], Pobs=z["Pobs"], weeks=pd.DatetimeIndex(z["weeks"]), start=z["start"],
                    attrs=attrs, events=z["events"], event_names=list(z["event_names"]), name="M5")
    dcols = [c for c in sales.columns if c.startswith("d_")]
    cal = cal.iloc[: len(dcols)].copy()
    wk_ids, inv = np.unique(cal["wm_yr_wk"].to_numpy(), return_inverse=True)
    Yd = sales[dcols].to_numpy(dtype=np.float32)
    Y = np.stack([Yd[:, inv == j].sum(1) for j in range(len(wk_ids))], axis=1)
    weeks = pd.to_datetime(cal.groupby("wm_yr_wk")["date"].min().loc[wk_ids].to_numpy())

    # weekly calendar covariates: number of events and SNAP days in the series' own state
    cal["n_event"] = cal[["event_name_1", "event_name_2"]].notna().sum(1)
    ev = cal.groupby("wm_yr_wk").agg(n_event=("n_event", "sum"), snap_CA=("snap_CA", "sum"),
                                     snap_TX=("snap_TX", "sum"), snap_WI=("snap_WI", "sum")).loc[wk_ids]

    prices = pd.read_csv(os.path.join(config.M5_DIR, "sell_prices.csv"))
    prices["series_id"] = prices["item_id"] + "_" + prices["store_id"] + "_evaluation"
    row = pd.Series(np.arange(len(attrs)), index=attrs["series_id"])
    col = pd.Series(np.arange(len(wk_ids)), index=wk_ids)
    P = np.full(Y.shape, np.nan, dtype=np.float32)
    P[row.loc[prices["series_id"]].to_numpy(), col.loc[prices["wm_yr_wk"]].to_numpy()] = prices["sell_price"].to_numpy()
    Pobs = ~np.isnan(P)
    # series start = first week with a listed price (product on shelf); fall back to first sale
    has_p = Pobs.any(1)
    start = np.where(has_p, Pobs.argmax(1), (Y > 0).argmax(1)).astype(np.int32)
    P = _ffill_rows(P)
    Y = Y.astype(np.float32)
    Y[np.arange(Y.shape[1])[None, :] < start[:, None]] = np.nan

    events = ev[["n_event", "snap_CA", "snap_TX", "snap_WI"]].to_numpy(dtype=np.float32)
    os.makedirs(config.CACHE, exist_ok=True)
    np.savez_compressed(cache, Y=Y, P=P, Pobs=Pobs, weeks=weeks.to_numpy(), start=start,
                        events=events, event_names=np.array(list(ev.columns)))
    return dict(Y=Y, P=P, Pobs=Pobs, weeks=weeks, start=start, attrs=attrs, events=events,
                event_names=list(ev.columns), name="M5")


def load_vn1():
    keys = ["Client", "Warehouse", "Product"]
    S = pd.concat([pd.read_csv(os.path.join(config.VN1_DIR, f"Phase {p} - Sales.csv")).set_index(keys) for p in (0, 1, 2)], axis=1)
    Pr = pd.concat([pd.read_csv(os.path.join(config.VN1_DIR, f"Phase {p} - Price.csv")).set_index(keys) for p in (0, 1)], axis=1)
    Pr = Pr.reindex(index=S.index, columns=S.columns)          # Phase 2 prices are not provided
    weeks = pd.to_datetime(S.columns)
    Y = S.to_numpy(dtype=np.float32).clip(min=0)
    P = Pr.to_numpy(dtype=np.float32)
    Pobs = ~np.isnan(P)
    start = (Y > 0).argmax(1).astype(np.int32)                  # first positive sale
    Y[np.arange(Y.shape[1])[None, :] < start[:, None]] = np.nan
    P = _ffill_rows(P)
    attrs = S.index.to_frame(index=False)
    attrs.insert(0, "series_id", attrs["Client"].astype(str) + "_" + attrs["Warehouse"].astype(str) + "_" + attrs["Product"].astype(str))
    attrs["client_wh"] = attrs["Client"].astype(str) + "_" + attrs["Warehouse"].astype(str)
    return dict(Y=Y, P=P, Pobs=Pobs, weeks=weeks, start=start, attrs=attrs,
                events=np.zeros((len(weeks), 0), np.float32), event_names=[], name="VN1")


def load(name):
    return {"M5": load_m5, "VN1": load_vn1}[name.upper()]()
