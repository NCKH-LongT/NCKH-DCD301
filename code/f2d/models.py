"""Forecasting models (ai_model_integration.md, sections 2-3).

Every model returns quantiles of the total demand D_h = Σ Y[o : o+h] for each series and test origin:
    Q  float32 [n_series, n_origins, n_quantiles]   (NaN for series outside the evaluation set)

Origins o are the test weeks; a forecast at o uses weeks < o only. Model parameters are refitted every
BLOCK_WEEKS at the block cutoff c (the first test week of the block) using targets fully observed before c;
between cutoffs the statistical models update their state every week, the ML models are re-applied to
the newest features.
"""
import time

import lightgbm as lgb
import numpy as np
from scipy import stats

from . import config
from .features import Builder

HISTORY_WEEKS = 104      # empirical baseline: window of past h-week totals
TRAIN_ORIGINS = 104      # ML models: number of training origins before each cutoff
MAX_TRAIN_ROWS = 3_000_000
WARM_WEEKS = 13          # statistical models: in-sample weeks skipped when choosing parameters


def block_cutoffs(origins):
    t0 = origins[0]
    return {o: t0 + config.BLOCK_WEEKS * ((o - t0) // config.BLOCK_WEEKS) for o in origins}


def _sort(Q):
    Q = np.maximum(Q, 0)
    return np.sort(Q, axis=-1)


# ------------------------------------------------------------------------------------------------
# Empirical (seasonal naive) baseline
# ------------------------------------------------------------------------------------------------
def empirical(b: Builder, origins, h, qs, series):
    Q = np.full((b.n, len(origins), len(qs)), np.nan, np.float32)
    idx = np.flatnonzero(series)
    st = b.start[idx]
    for j, o in enumerate(origins):
        t = np.arange(max(o - HISTORY_WEEKS, 0), o - h + 1)
        R = b.C[idx][:, t + h] - b.C[idx][:, t]
        R[t[None, :] < st[:, None]] = np.nan
        with np.errstate(all="ignore"):
            q = np.nanquantile(R, qs, axis=1).T
        Q[idx, j] = np.nan_to_num(q)
    return _sort(Q)


# ------------------------------------------------------------------------------------------------
# TSB and ETS(A,N,N): vectorised exponential smoothing, parameters chosen per series on a grid
# ------------------------------------------------------------------------------------------------
TSB_GRID = [(ad, ap) for ad in (0.05, 0.1, 0.2, 0.3) for ap in (0.05, 0.1, 0.2, 0.3)]
SES_GRID = [0.02, 0.05, 0.1, 0.2, 0.3, 0.5]


def _init_stats(Y0, act, start, c):
    """Initial level / demand size / probability from the training weeks [start, c)."""
    t = np.arange(Y0.shape[1])[None, :]
    win = act & (t < c)
    n = win.sum(1)
    pos = win & (Y0 > 0)
    level = np.where(win, Y0, 0).sum(1) / np.maximum(n, 1)
    size = np.where(pos, Y0, 0).sum(1) / np.maximum(pos.sum(1), 1)
    prob = pos.sum(1) / np.maximum(n, 1)
    return level, np.where(size > 0, size, 1.0), prob


def _grid_sse(kind, Y0, act, start, params, init, c):
    """Run the smoother for every grid value over weeks < c; in-sample one-step SSE over [start+WARM, c)."""
    n = Y0.shape[0]
    K = len(params)
    if kind == "tsb":
        ad, ap = params[:, 0][None, :], params[:, 1][None, :]
        z = np.repeat(init[1][:, None], K, 1)
        p = np.repeat(init[2][:, None], K, 1)
    else:
        a = np.asarray(params)[None, :]
        l = np.repeat(init[0][:, None], K, 1)
    sse = np.zeros((n, K))
    for t in range(c):
        f = p * z if kind == "tsb" else l
        y = Y0[:, t][:, None]
        on = act[:, t][:, None]
        use = on & (t >= start[:, None] + WARM_WEEKS)
        sse += np.where(use, y - f, 0.0) ** 2
        if kind == "tsb":
            pos = y > 0
            p = np.where(on, p + ap * (pos - p), p)
            z = np.where(on & pos, z + ad * (y - z), z)
        else:
            l = np.where(on, l + a * (y - l), l)
    return sse


def _smooth_model(kind, b: Builder, origins, h, qs, series):
    Y0 = np.nan_to_num(b.Y).astype(np.float64)
    act = ~np.isnan(b.Y)
    Q = np.full((b.n, len(origins), len(qs)), np.nan, np.float32)
    cut = block_cutoffs(origins)
    grid = np.array(TSB_GRID if kind == "tsb" else SES_GRID, np.float64)
    rows = np.flatnonzero(series)
    for c in sorted(set(cut.values())):
        orig = [o for o in origins if cut[o] == c]
        init = _init_stats(Y0, act, b.start, c)
        par = grid[_grid_sse(kind, Y0, act, b.start, grid, init, c).argmin(1)]
        sse1, cnt1, rec = _run_per_series(kind, Y0, act, b.start, par, init, c, orig)
        if kind == "ets":
            mse = sse1 / np.maximum(cnt1, 1)
            sigma = np.sqrt(mse)
            w = (1 + par[:, None] * np.arange(h)[None, :]) ** 2          # Var of an h-week total under ANN
            sd = sigma * np.sqrt(w.sum(1))
        for o in orig:
            j = origins.index(o)
            f = rec[o]
            if kind == "tsb":
                lam = h * f
                q = stats.poisson.ppf(np.array(qs)[None, :], np.maximum(lam, 1e-9)[:, None])
            else:
                q = h * f[:, None] + stats.norm.ppf(np.array(qs))[None, :] * sd[:, None]
            Q[rows, j] = q[rows]
    return _sort(Q)


def _run_per_series(kind, Y0, act, start, par, init, c, record):
    """Run with each series' own parameters; record the one-step mean forecast at each origin in record."""
    n = Y0.shape[0]
    if kind == "tsb":
        ad, ap = par[:, 0], par[:, 1]
        z, p = init[1].copy(), init[2].copy()
    else:
        a = par
        l = init[0].copy()
    sse = np.zeros(n); cnt = np.zeros(n)
    rec = {o: None for o in record}
    for t in range(max(record) + 1):
        f = p * z if kind == "tsb" else l
        if t in rec:
            rec[t] = f.copy()
            if t == max(record):
                break
        y = Y0[:, t]
        on = act[:, t]
        if t < c:
            use = on & (t >= start + WARM_WEEKS)
            e = np.where(use, y - f, 0.0)
            sse += e ** 2; cnt += use
        if kind == "tsb":
            pos = y > 0
            p = np.where(on, p + ap * (pos - p), p)
            z = np.where(on & pos, z + ad * (y - z), z)
        else:
            l = np.where(on, l + a * (y - l), l)
    return sse, cnt, rec


def tsb(b, origins, h, qs, series):
    return _smooth_model("tsb", b, origins, h, qs, series)


def tsb_nb(b: Builder, origins, h, qs, series):
    """TSB mean with a negative binomial predictive distribution of the h-week total.

    Weekly demand is modelled as Bernoulli(p) occurrence × size with mean z and variance var_z (sample
    variance of the positive weeks before the cutoff). For the h-week total:
        mean = h·p·z,   var = h·(p·(var_z + z²) − (p·z)²)
    The total is mapped to a negative binomial with that mean and variance (Poisson when var ≤ mean).
    """
    Y0 = np.nan_to_num(b.Y).astype(np.float64)
    act = ~np.isnan(b.Y)
    Q = np.full((b.n, len(origins), len(qs)), np.nan, np.float32)
    cut = block_cutoffs(origins)
    grid = np.array(TSB_GRID, np.float64)
    rows = np.flatnonzero(series)
    qa = np.array(qs)[None, :]
    t = np.arange(b.T)[None, :]
    for c in sorted(set(cut.values())):
        orig = [o for o in origins if cut[o] == c]
        init = _init_stats(Y0, act, b.start, c)
        par = grid[_grid_sse("tsb", Y0, act, b.start, grid, init, c).argmin(1)]
        pos = act & (t < c) & (Y0 > 0)
        npos = pos.sum(1)
        m1 = np.where(pos, Y0, 0).sum(1) / np.maximum(npos, 1)
        var_z = np.where(npos > 1, np.where(pos, Y0 ** 2, 0).sum(1) / np.maximum(npos, 1) - m1 ** 2, 0.0)
        var_z = np.maximum(var_z, 0)
        # one run that records both the occurrence probability and the size at each origin
        ad, ap = par[:, 0], par[:, 1]
        z, p = init[1].copy(), init[2].copy()
        rec = {}
        for tt in range(max(orig) + 1):
            if tt in orig:
                rec[tt] = (p.copy(), z.copy())
            y = Y0[:, tt]
            on = act[:, tt]
            ps = y > 0
            p = np.where(on, p + ap * (ps - p), p)
            z = np.where(on & ps, z + ad * (y - z), z)
        for o in orig:
            j = origins.index(o)
            pp, zz = rec[o]
            mean = h * pp * zz
            var = h * (pp * (var_z + zz ** 2) - (pp * zz) ** 2)
            mean = np.maximum(mean, 1e-9)
            over = var > mean * (1 + 1e-6)
            r_nb = np.where(over, mean ** 2 / np.maximum(var - mean, 1e-12), 1.0)
            p_nb = np.where(over, mean / np.maximum(var, 1e-12), 0.5)
            q_nb = stats.nbinom.ppf(qa, r_nb[:, None], p_nb[:, None])
            q_po = stats.poisson.ppf(qa, mean[:, None])
            q = np.where(over[:, None], q_nb, q_po)
            Q[rows, j] = q[rows]
    return _sort(Q)


def ets(b, origins, h, qs, series):
    return _smooth_model("ets", b, origins, h, qs, series)


# ------------------------------------------------------------------------------------------------
# LightGBM: quantile regression (main model) and Tweedie + normal safety stock (ablation)
# ------------------------------------------------------------------------------------------------
LGB_PARAMS = dict(learning_rate=0.05, num_leaves=63, min_data_in_leaf=200, feature_fraction=0.8,
                  bagging_fraction=0.8, bagging_freq=1, lambda_l2=1.0, max_bin=255, verbose=-1,
                  num_threads=0, seed=config.SEED)
NUM_ROUNDS = 1000
TARGET_CLIP_PCT = 99.9   # winsorise the scaled quantile target D_h / s (series reviving after long zero runs)
EARLY_STOP = 50


def _train_valid(b: Builder, c, h, series, rng):
    last = c - h                                     # last origin whose target ends before c
    valid_o = list(range(last - config.VALID_WEEKS + 1, last + 1))
    train_o = list(range(max(last - config.VALID_WEEKS - TRAIN_ORIGINS + 1, 1), last - config.VALID_WEEKS + 1))
    Xt, St, Dt, It, _ = b.rows(train_o, h, series, need_target=True)
    if len(Dt) > MAX_TRAIN_ROWS:
        k = np.sort(rng.choice(len(Dt), MAX_TRAIN_ROWS, replace=False))
        Xt, St, Dt, It = Xt[k], St[k], Dt[k], It[k]
    Xv, Sv, Dv, Iv, _ = b.rows(valid_o, h, series, need_target=True)
    return (Xt, St, Dt, It), (Xv, Sv, Dv, Iv)


def _fit(params, Xt, yt, Xv, yv, b):
    cat = [b.names.index(c) for c in b.categorical]
    dt = lgb.Dataset(Xt, yt, feature_name=b.names, categorical_feature=cat, free_raw_data=False)
    dv = lgb.Dataset(Xv, yv, reference=dt)
    return lgb.train(params, dt, NUM_ROUNDS, valid_sets=[dv],
                     callbacks=[lgb.early_stopping(EARLY_STOP, verbose=False)])


def _lgb_model(kind, b: Builder, origins, h, qs, series, log=print):
    Q = np.full((b.n, len(origins), len(qs)), np.nan, np.float32)
    cut = block_cutoffs(origins)
    rng = np.random.default_rng(config.SEED)
    for c in sorted(set(cut.values())):
        orig = [o for o in origins if cut[o] == c]
        t0 = time.time()
        (Xt, St, Dt, It), (Xv, Sv, Dv, Iv) = _train_valid(b, c, h, series, rng)
        Xp, Sp, _, Ip, Op = b.rows(orig, h, series, min_history=0)
        jp = np.searchsorted(origins, Op)
        log(f"    block cutoff {c}: train {len(Dt):,} rows, valid {len(Dv):,}, predict {len(Ip):,}")
        if kind == "lgb_quantile":
            cap = np.percentile(Dt / St, TARGET_CLIP_PCT)
            yt, yv = np.minimum(Dt / St, cap), np.minimum(Dv / Sv, cap)
            for k, q in enumerate(qs):
                m = _fit({**LGB_PARAMS, "objective": "quantile", "alpha": q}, Xt, yt, Xv, yv, b)
                Q[Ip, jp, k] = m.predict(Xp, num_iteration=m.best_iteration) * Sp
                log(f"      q={q}: {m.best_iteration} rounds ({time.time() - t0:.0f}s)")
        else:
            m = _fit({**LGB_PARAMS, "objective": "tweedie", "tweedie_variance_power": 1.1}, Xt, Dt, Xv, Dv, b)
            mu_v = m.predict(Xv, num_iteration=m.best_iteration)
            # σ per series from validation residuals of the h-week total
            sq = np.bincount(Iv, (Dv - mu_v) ** 2, b.n)
            nv = np.bincount(Iv, minlength=b.n)
            sigma = np.sqrt(sq / np.maximum(nv, 1))
            mu = m.predict(Xp, num_iteration=m.best_iteration)
            sig = np.where(nv[Ip] > 0, sigma[Ip], np.sqrt(np.maximum(mu, 0)))
            z = stats.norm.ppf(np.array(qs))
            Q[Ip, jp] = mu[:, None] + sig[:, None] * z[None, :]
            log(f"      tweedie: {m.best_iteration} rounds ({time.time() - t0:.0f}s)")
    return _sort(Q)


def lgb_quantile(b, origins, h, qs, series, log=print):
    return _lgb_model("lgb_quantile", b, origins, h, qs, series, log)


def lgb_tweedie(b, origins, h, qs, series, log=print):
    return _lgb_model("lgb_tweedie", b, origins, h, qs, series, log)


# ------------------------------------------------------------------------------------------------
# Additional ML baselines (no deep learning; ai_model_integration.md, section 3)
# ------------------------------------------------------------------------------------------------
HGB_MAX_TRAIN_ROWS = 300_000     # HistGradientBoosting is much slower than LightGBM: train on a random subsample


def lgb_conformal(b: Builder, origins, h, qs, series, log=print):
    """LightGBM-Tweedie point forecast + split-conformal quantiles.

    Residuals of the validation origins are divided by the series scale s and pooled per ADI–CV² class
    (classes computed on the weeks before the cutoff). Quantile q of a forecast = μ + s · F⁻¹_class(q).
    """
    from .classify import classify as _classify
    Q = np.full((b.n, len(origins), len(qs)), np.nan, np.float32)
    cut = block_cutoffs(origins)
    rng = np.random.default_rng(config.SEED)
    for c in sorted(set(cut.values())):
        orig = [o for o in origins if cut[o] == c]
        t0 = time.time()
        (Xt, St, Dt, It), (Xv, Sv, Dv, Iv) = _train_valid(b, c, h, series, rng)
        Xp, Sp, _, Ip, Op = b.rows(orig, h, series, min_history=0)
        jp = np.searchsorted(origins, Op)
        m = _fit({**LGB_PARAMS, "objective": "tweedie", "tweedie_variance_power": 1.1}, Xt, Dt, Xv, Dv, b)
        cls, _, _ = _classify(b.Y, b.start, c)
        r = (Dv - m.predict(Xv, num_iteration=m.best_iteration)) / Sv
        mu = m.predict(Xp, num_iteration=m.best_iteration)
        q_all = np.quantile(r, qs)
        for g in np.unique(cls[Ip]):
            rv = r[cls[Iv] == g]
            qg = np.quantile(rv, qs) if len(rv) >= 200 else q_all
            sel = cls[Ip] == g
            Q[Ip[sel], jp[sel]] = mu[sel][:, None] + Sp[sel][:, None] * qg[None, :]
        log(f"    block cutoff {c}: conformal on {len(r):,} validation residuals ({time.time() - t0:.0f}s)")
    return _sort(Q)


def hgb_quantile(b: Builder, origins, h, qs, series, log=print):
    """scikit-learn HistGradientBoostingRegressor(loss='quantile') on the same scaled target as lgb_quantile."""
    from sklearn.ensemble import HistGradientBoostingRegressor
    Q = np.full((b.n, len(origins), len(qs)), np.nan, np.float32)
    cut = block_cutoffs(origins)
    rng = np.random.default_rng(config.SEED)
    cat = np.array([n in b.categorical for n in b.names])
    for c in sorted(set(cut.values())):
        orig = [o for o in origins if cut[o] == c]
        t0 = time.time()
        (Xt, St, Dt, It), _ = _train_valid(b, c, h, series, rng)
        if len(Dt) > HGB_MAX_TRAIN_ROWS:
            k = np.sort(rng.choice(len(Dt), HGB_MAX_TRAIN_ROWS, replace=False))
            Xt, St, Dt = Xt[k], St[k], Dt[k]
        Xp, Sp, _, Ip, Op = b.rows(orig, h, series, min_history=0)
        jp = np.searchsorted(origins, Op)
        y = Dt / St
        y = np.minimum(y, np.percentile(y, TARGET_CLIP_PCT))
        log(f"    block cutoff {c}: train {len(y):,} rows, predict {len(Ip):,}")
        for k, q in enumerate(qs):
            m = HistGradientBoostingRegressor(loss="quantile", quantile=q, learning_rate=0.1, max_iter=300,
                                              max_leaf_nodes=63, min_samples_leaf=200, l2_regularization=1.0,
                                              categorical_features=cat if cat.any() else None,
                                              early_stopping=True, validation_fraction=0.1, n_iter_no_change=30,
                                              random_state=config.SEED)
            m.fit(Xt, y)
            Q[Ip, jp, k] = m.predict(Xp) * Sp
            log(f"      q={q}: {m.n_iter_} iterations ({time.time() - t0:.0f}s)")
    return _sort(Q)


MODELS = {"empirical": empirical, "tsb": tsb, "tsb_nb": tsb_nb, "ets": ets, "lgb_tweedie": lgb_tweedie,
          "lgb_conformal": lgb_conformal, "hgb_quantile": hgb_quantile, "lgb_quantile": lgb_quantile}
