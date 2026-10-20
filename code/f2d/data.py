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
    # drop incomplete Walmart weeks (d_1940-d_1941 form a 2-day week 11618)
    full = cal.groupby("wm_yr_wk")["d"].transform("size") == 7
    dcols = [d for d, f in zip(dcols, full) if f]
    cal = cal[full.to_numpy()].copy()
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
    prices = prices[prices["wm_yr_wk"].isin(wk_ids)]            # sell_prices also covers the 28 hidden days after d_1941
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


def load_vnf():
    """Vietnam footwear retail chain (Vietnam Datathon 2023, Kaggle tienanh2003/sales-and-inventory-snapshot-data),
    case study. Series = style-colour (mold_code + color) × whole chain, retail channel ("Bán lẻ"), weekly.

    Week codes are year + ISO week of the transaction date's year, which mislabels the year-boundary days:
    202153 holds 1–2 Jan 2022 (a 2-day remnant of ISO week 2021-W52) and is dropped; 202352 holds 1 Jan 2023
    (ISO week 2022-W52) and is merged into 202252. Week 202331 contains only 31 Jul 2023 and is dropped.
    Returns (negative quantities) are excluded from demand. Price = weekly net unit price (net revenue / units),
    forward-filled; per-series median unit net price and unit cost are kept in attrs for the money-based analysis.
    Requires data/cache/vn_sales.parquet (created by code/profile_datasets.py from the raw Excel files).
    """
    path = os.path.join(config.CACHE, "vn_sales.parquet")
    if not os.path.exists(path):
        raise FileNotFoundError("run code/profile_datasets.py first to build data/cache/vn_sales.parquet")
    s = pd.read_parquet(path, columns=["week", "distribution_channel", "sold_quantity", "cost_price", "net_price",
                                       "product_id"])
    s = s[(s.distribution_channel == "Bán lẻ") & (s.sold_quantity > 0)].copy()
    pm = pd.read_excel(os.path.join(config.VNF_DIR, "MasterData", "Productmaster.xlsx"), engine="calamine",
                       usecols=["product_id", "mold_code", "color", "product_group"]).drop_duplicates("product_id")
    s = s.merge(pm, on="product_id", how="inner")
    s["week"] = s["week"].replace({202352: 202252})
    s = s[(s.week != 202153) & (s.week != 202331)]
    s["series_id"] = s["mold_code"].astype(str) + "_" + s["color"].astype(str)
    g = s.groupby(["series_id", "week"]).agg(q=("sold_quantity", "sum"), rev=("net_price", "sum"),
                                              cost=("cost_price", "sum")).reset_index()
    wk = np.sort(g.week.unique())
    weeks = pd.DatetimeIndex([pd.Timestamp.fromisocalendar(int(w) // 100, int(w) % 100, 1) for w in wk])
    assert (np.diff(weeks.values).astype("timedelta64[D]").astype(int) == 7).all(), "weekly grid has gaps"
    ids = np.sort(g.series_id.unique())
    r = pd.Series(np.arange(len(ids)), index=ids).loc[g.series_id].to_numpy()
    c = pd.Series(np.arange(len(wk)), index=wk).loc[g.week].to_numpy()
    Y = np.zeros((len(ids), len(wk)), np.float32)
    Y[r, c] = g.q.to_numpy()
    P = np.full(Y.shape, np.nan, np.float32)
    P[r, c] = (g.rev / g.q).to_numpy()
    Pobs = ~np.isnan(P)
    start = (Y > 0).argmax(1).astype(np.int32)
    Y[np.arange(Y.shape[1])[None, :] < start[:, None]] = np.nan
    P = _ffill_rows(P)
    unit = g.assign(price=g.rev / g.q, ucost=g.cost / g.q).groupby("series_id")[["price", "ucost"]].median().loc[ids]
    grp = s.drop_duplicates("series_id").set_index("series_id")["product_group"].loc[ids]
    attrs = pd.DataFrame({"series_id": ids, "product_group": grp.to_numpy(), "unit_price": unit.price.to_numpy(),
                          "unit_cost": unit.ucost.to_numpy()})
    return dict(Y=Y, P=P, Pobs=Pobs, weeks=weeks, start=start, attrs=attrs,
                events=np.zeros((len(weeks), 0), np.float32), event_names=[], name="VNF")


def truncate(panel, T):
    """Keep the first T weeks (a panel that ends T weeks after its start), e.g. for an earlier test window."""
    q = dict(panel)
    for k in ("Y", "P", "Pobs"):
        q[k] = panel[k][:, :T]
    q["weeks"] = panel["weeks"][:T]
    q["events"] = panel["events"][:T]
    return q


def load(name):
    return {"M5": load_m5, "VN1": load_vn1, "VNF": load_vnf}[name.upper()]()
