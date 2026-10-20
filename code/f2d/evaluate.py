"""Forecast errors and cost-free inventory KPIs (data_flow.md §8, research_questions.md RQ1–RQ3)."""
import numpy as np
import pandas as pd

from . import config


def naive_scales(Y, start, end):
    """Per-series mean |Δy| and mean Δy² of the one-step naive forecast over training weeks [start, end)."""
    d = np.diff(Y[:, :end], axis=1)
    d[np.arange(1, end)[None, :] <= start[:, None]] = np.nan
    with np.errstate(all="ignore"):
        return np.nanmean(np.abs(d), 1), np.nanmean(d ** 2, 1)


def forecast_metrics(Q, Dtrue, qs, h, s_abs, s_sq, groups):
    """Q [n, O, n_q], Dtrue [n, O]. Returns one row per group with SQL, RMSSE and coverage of each quantile.

    SQL   = mean pinball loss / (h · mean|Δy|)
    RMSSE = sqrt(mean (D − Q_0.5)² / (h² · mean Δy²))
    """
    qs = np.asarray(qs)
    ok = ~np.isnan(Dtrue)[:, :, None] & ~np.isnan(Q)
    e = Dtrue[:, :, None] - Q
    pin = np.where(ok, np.maximum(qs * e, (qs - 1) * e), np.nan)
    with np.errstate(all="ignore"):
        sql = np.nanmean(pin, axis=(1, 2)) / (h * s_abs)
        med = Q[:, :, list(qs).index(0.5)]
        rmsse = np.sqrt(np.nanmean((Dtrue - med) ** 2, 1) / (h ** 2 * s_sq))
        cov = np.nanmean(np.where(ok, Dtrue[:, :, None] <= Q, np.nan), 1)
    valid = (s_abs > 0) & np.isfinite(sql)
    rows = []
    for g, m in groups.items():
        m = m & valid
        r = dict(group=g, n_series=int(m.sum()), SQL=np.nanmean(sql[m]), RMSSE=np.nanmean(rmsse[m]))
        for k, q in enumerate(qs):
            r[f"cov_{q}"] = np.nanmean(cov[m, k])
        rows.append(r)
    return pd.DataFrame(rows)


def series_kpis(sim, D, H, warmup=config.WARMUP_WEEKS):
    """Per-series totals over the KPI weeks (after warm-up)."""
    w = slice(warmup, None)
    dem = D[:, w]
    oh = sim["on_hand_end"][:, w]
    # ex-post excess: on-hand above the realised demand of the next H weeks (weeks with a full window)
    W = D.shape[1]
    C = np.concatenate([np.zeros((D.shape[0], 1)), np.cumsum(D, 1)], 1)
    k = np.arange(warmup, W - H + 1) if W - H + 1 > warmup else np.arange(0)
    fut = C[:, k + H] - C[:, k] if len(k) else np.zeros((D.shape[0], 0))
    excess = np.maximum(sim["on_hand_end"][:, k] - fut, 0) if len(k) else np.zeros((D.shape[0], 0))
    return dict(
        demand=dem.sum(1), sales=sim["sales"][:, w].sum(1), lost=sim["lost"][:, w].sum(1),
        weeks=np.full(D.shape[0], dem.shape[1]), stockout_weeks=(sim["lost"][:, w] > 0).sum(1),
        demand_weeks=(dem > 0).sum(1), on_hand=oh.sum(1), liq=sim["liq"][:, w].sum(1),
        liq_weeks=(sim["liq"][:, w] > 0).sum(1), orders=sim["order"][:, w].sum(1),
        excess=excess.sum(1), excess_weeks=np.full(D.shape[0], excess.shape[1]),
        excess_demand=fut.sum(1) / max(H, 1),
    )


def _agg(t):
    """Pooled KPIs from per-series totals (dict of arrays restricted to a group)."""
    dem = t["demand"].sum()
    wks = t["weeks"].sum()
    mean_dem = dem / wks if wks else np.nan                 # mean weekly demand of the group
    ex_w = t["excess_weeks"].sum()
    return dict(
        fill_rate=t["sales"].sum() / dem if dem else np.nan,
        csl=1 - t["stockout_weeks"].sum() / wks,
        stockout_rate_demand_weeks=t["stockout_weeks"].sum() / max(t["demand_weeks"].sum(), 1),
        inventory_weeks=(t["on_hand"].sum() / wks) / mean_dem if mean_dem else np.nan,
        excess_weeks_of_demand=(t["excess"].sum() / ex_w) / mean_dem if ex_w and mean_dem else np.nan,
        liquidated_share=t["liq"].sum() / dem if dem else np.nan,
        liq_series_share=float((t["liq"] > 0).mean()),
    )


def kpi_table(tot, groups, n_boot=0, seed=config.SEED):
    """Aggregate per-series totals by group; optional bootstrap (over series) 95% CI of fill rate and
    inventory weeks."""
    rng = np.random.default_rng(seed)
    rows = []
    for g, m in groups.items():
        idx = np.flatnonzero(m)
        t = {k: v[idx] for k, v in tot.items()}
        r = dict(group=g, n_series=len(idx), **_agg(t))
        if n_boot and len(idx):
            fr, iw = [], []
            for _ in range(n_boot):
                bi = rng.integers(0, len(idx), len(idx))
                a = _agg({k: v[bi] for k, v in t.items()})
                fr.append(a["fill_rate"]); iw.append(a["inventory_weeks"])
            r["fill_rate_lo"], r["fill_rate_hi"] = np.nanpercentile(fr, [2.5, 97.5])
            r["inventory_weeks_lo"], r["inventory_weeks_hi"] = np.nanpercentile(iw, [2.5, 97.5])
        rows.append(r)
    return pd.DataFrame(rows)
