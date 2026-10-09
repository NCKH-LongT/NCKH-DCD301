"""RQ3: break-even salvage ratio of liquidation, and series-level inventory distribution.

For each model and liquidation rule (quantile, fixed) the lost-sales simulation is run with and without
liquidation from the same starting stock (default scenario). Over the whole test horizon (warm-up included,
so both runs start from the same state), all quantities in units valued at unit cost c = 1:

    Δ = (with liquidation) − (no liquidation)
    s* = [ΔOrders − ΔEndPosition + h·ΔInventoryUnitWeeks − (1 + m)·ΔSales] / LiquidatedUnits

s* is the minimum salvage value (as a fraction of unit cost) at which liquidating is at least as profitable as
holding. h = weekly holding cost rate (annual rate / 52), m = gross margin (price = (1 + m)·cost). End position
(on-hand + on order) is valued either (a) at cost — favourable to holding, gives an upper bound of s* — or
(b) at the same salvage ratio s, i.e. leftover stock is eventually cleared too — gives a lower bound:
    s*_b = [ΔOrders + h·ΔInventoryUnitWeeks − (1 + m)·ΔSales] / (LiquidatedUnits + ΔEndPosition).
s* < 0 means liquidating pays off even at zero salvage; s* > 1 means it
only pays off when stock can be sold above cost.

For the Vietnam footwear case study (--dataset VNF) the panel carries each series' median unit cost c_i and unit net
price p_i, so s* is also computed with the actual costs and prices (salvage as a fraction of cost, summed over series):
    s*_actual = [Σ c·ΔOrders − Σ c·ΔEndPosition + h·Σ c·ΔInventoryUnitWeeks − Σ p·ΔSales] / Σ c·LiquidatedUnits
(columns s_star_actual_h<rate>; upper bound, end position valued at cost).

Writes code/outputs/<DATASET>/breakeven.csv and series_inventory.csv.

Usage:
    python code/liquidation_breakeven.py --dataset VN1
"""
import argparse
import os
import sys

import numpy as np
import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from f2d import classify, config, data, policy  # noqa: E402
from f2d.features import Builder  # noqa: E402

ANNUAL_HOLDING = (0.10, 0.25, 0.40)
MARGINS = (0.3, 0.5, 1.0)
MODELS = ["empirical", "tsb", "tsb_nb", "ets", "lgb_tweedie", "lgb_conformal", "hgb_quantile", "lgb_quantile", "chronos2"]


def end_position(sim, L):
    W = sim["order"].shape[1]
    on_order = sim["order"][:, max(W - L, 0):].sum(1) if L > 0 else 0.0
    return sim["on_hand_end"][:, -1] + on_order


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dataset", required=True, choices=["M5", "VN1", "VNF"])
    a = ap.parse_args()
    d = config.DEFAULT
    R, L, tau, H, ql, kf = d["R"], d["L"], d["tau"], d["H"], d["q_liq"], d["k_fixed"]

    p = data.load(a.dataset)
    Y = p["Y"]
    n, T = Y.shape
    test0 = T - config.TEST_WEEKS
    origins = list(range(test0, T))
    sel = p["start"] <= test0 - config.VALID_WEEKS
    cls, _, _ = classify.classify(Y, p["start"], test0)
    sel &= cls != "none"
    idx = np.flatnonzero(sel)
    groups = {"all": np.ones(len(idx), bool), **{c: cls[idx] == c for c in classify.CLASSES}}
    b = Builder(p)
    qs = list(config.QUANTILES)
    D = np.nan_to_num(Y[:, test0:T]).astype(np.float64)[idx]
    avg26 = np.stack([b.window_sum(b.C, o - 26, o) / np.maximum(b.window_sum(b.A, o - 26, o), 1) for o in origins], 1)[idx]
    since = np.stack([b.since_sale(o) for o in origins], 1)[idx]
    fc = os.path.join(config.CACHE, "forecasts", a.dataset)
    actual = "unit_cost" in p["attrs"].columns
    if actual:
        uc = p["attrs"]["unit_cost"].to_numpy(float)[idx]
        up = p["attrs"]["unit_price"].to_numpy(float)[idx]

    rows, inv_rows = [], []
    for m in MODELS:
        f_lr = os.path.join(fc, f"{m}_h{L + R}.npz")
        f_h = os.path.join(fc, f"{m}_h{H}.npz")
        if not (os.path.exists(f_lr) and os.path.exists(f_h)):
            print(f"  skip {m}: forecasts not cached")
            continue
        S = np.load(f_lr)["Q"][idx][:, :, qs.index(tau)]
        thr = {"quantile": (S, np.load(f_h)["Q"][idx][:, :, qs.index(ql)]), "fixed": (S, kf * avg26),
               **{f"dead{N}": policy.deadstock(S, since, N) for N in config.DEAD_WEEKS}}
        base = policy.simulate(D, S, np.full_like(S, np.inf), L)

        # series-level weeks of supply (KPI weeks), no liquidation
        w = slice(config.WARMUP_WEEKS, None)
        md = D[:, w].mean(1)
        wos = np.where(md > 0, base["on_hand_end"][:, w].mean(1) / md, np.nan)
        for g, msk in groups.items():
            v = wos[msk]
            inv_rows.append(dict(model=m, group=g, median_weeks_of_supply=np.nanmedian(v),
                                 p75=np.nanpercentile(v, 75), p90=np.nanpercentile(v, 90),
                                 zero_demand_series_share=float(np.mean(md[msk] == 0))))

        for pol, (S_pol, T_liq) in thr.items():
            liq = policy.simulate(D, S_pol, T_liq, L)
            d_orders = liq["order"].sum(1) - base["order"].sum(1)
            d_end = end_position(liq, L) - end_position(base, L)
            d_inv = liq["on_hand_end"].sum(1) - base["on_hand_end"].sum(1)
            d_sales = liq["sales"].sum(1) - base["sales"].sum(1)
            X = liq["liq"].sum(1)
            for g, msk in groups.items():
                Xg = X[msk].sum()
                r = dict(model=m, policy=pol, group=g, liquidated_units=Xg,
                         liquidated_share_of_demand=Xg / max(D[msk].sum(), 1),
                         d_orders=d_orders[msk].sum(), d_end_position=d_end[msk].sum(),
                         d_inventory_unit_weeks=d_inv[msk].sum(), d_sales=d_sales[msk].sum())
                disposed = Xg + r["d_end_position"]          # units removed for good (liquidated minus re-bought at the end)
                for hy in ANNUAL_HOLDING:
                    for mg in MARGINS:
                        base_num = r["d_orders"] + (hy / 52) * r["d_inventory_unit_weeks"] - (1 + mg) * r["d_sales"]
                        tag = f"h{int(hy * 100)}_m{int(mg * 100)}"
                        # (a) end position valued at cost  -> upper bound of s*
                        r[f"s_star_{tag}"] = (base_num - r["d_end_position"]) / Xg if Xg > 0 else np.nan
                        # (b) end position eventually salvaged at the same ratio s -> lower bound of s*
                        r[f"s_star_endsalv_{tag}"] = base_num / disposed if disposed > 0 else np.nan
                if actual:
                    cX = (uc * X)[msk].sum()
                    r["liquidated_cost_value"] = cX
                    for hy in ANNUAL_HOLDING:
                        num = ((uc * d_orders)[msk].sum() - (uc * d_end)[msk].sum()
                               + (hy / 52) * (uc * d_inv)[msk].sum() - (up * d_sales)[msk].sum())
                        r[f"s_star_actual_h{int(hy * 100)}"] = num / cX if cX > 0 else np.nan
                rows.append(r)

    out = os.path.join(config.OUTPUTS, a.dataset)
    os.makedirs(out, exist_ok=True)
    be = pd.DataFrame(rows)
    be.to_csv(os.path.join(out, "breakeven.csv"), index=False)
    inv = pd.DataFrame(inv_rows)
    inv.to_csv(os.path.join(out, "series_inventory.csv"), index=False)
    show = ["model", "policy", "group", "liquidated_share_of_demand", "d_sales", "s_star_h25_m50", "s_star_endsalv_h25_m50"]
    print(be[be.group == "all"][show].round(3).to_string(index=False))
    print()
    print(inv[inv.group == "all"].round(2).to_string(index=False))


if __name__ == "__main__":
    main()
