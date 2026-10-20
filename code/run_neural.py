"""Deep-learning baseline: N-HiTS (neuralforecast) with a multi-quantile loss, same protocol as the other methods.

Target. Like every method in f2d/models.py, the model forecasts the quantiles of the h-week total
D_h(o) = Y[o] + … + Y[o+h−1] at each test origin o, using weeks < o only. The weekly series is turned into the
series of forward h-week sums Z[t] = Y[t] + … + Y[t+h−1]; at origin o the last fully observed value is Z[o−h],
so D_h(o) = Z[o] is the h-th step of an h-step-ahead forecast of Z. Quantiles are therefore forecast directly
for the total (the quantile of a sum is not the sum of quantiles).

Protocol. Test period = last 26 weeks (two 13-week blocks). At each block cutoff c the model is trained on the Z
values observed before c (Z[t] for t ≤ c − h) of the evaluated series, then applied without refitting at every
origin of the block, with the history extended up to that origin. Univariate model (no price or calendar
covariates), fixed hyper-parameters, one seed. Output in the cache format used by every evaluation script:
    data/cache/forecasts/<DATASET>[_w<offset>]/nhits_h<h>.npz   with  Q float32 [n_series, 26, 5]
(NaN for series outside the evaluation set), so that e.g.
    python code/equal_fill_ci.py --models empirical,tsb_nb,ets,lgb_tweedie,lgb_conformal,hgb_quantile,lgb_quantile,nhits --out-suffix nn

Must be run with the interpreter that has neuralforecast installed, e.g.
    D:/venvs/nf/Scripts/python.exe code/run_neural.py --dataset VN1 --offset 0 --h 3
    D:/venvs/nf/Scripts/python.exe code/run_neural.py --dataset VN1 --offset 0 --h 3 --quick     # smoke test
"""
import argparse
import logging
import os
import sys
import time
import warnings

warnings.filterwarnings("ignore")
logging.getLogger("pytorch_lightning").setLevel(logging.ERROR)
logging.getLogger("lightning.pytorch").setLevel(logging.ERROR)
os.environ.setdefault("PYTORCH_ENABLE_MPS_FALLBACK", "1")

import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from f2d import classify, config, data  # noqa: E402

INPUT_SIZE = 52          # weeks of Z history fed to the network
MAX_STEPS = 1500         # training steps per block (fixed, no early stopping)
QUICK_STEPS = 50


def forward_sums(Y, h):
    """Z[:, t] = Y[:, t] + … + Y[:, t+h−1] (NaN where any week is unobserved or beyond the panel)."""
    n, T = Y.shape
    Z = np.full((n, T), np.nan, np.float64)
    for t in range(T - h + 1):
        Z[:, t] = Y[:, t:t + h].sum(1)          # NaN propagates if a week is before the series start
    return Z


def long_frame(Z, rows, last):
    """Long data frame (unique_id, ds, y) with Z[:, t] for t ≤ last[i] (per series), NaN dropped."""
    parts = []
    for k, i in enumerate(rows):
        z = Z[i, : last[k] + 1]
        t = np.flatnonzero(~np.isnan(z))
        if len(t):
            parts.append(pd.DataFrame({"unique_id": i, "ds": t, "y": z[t]}))
    return pd.concat(parts, ignore_index=True)


def make_model(h, qs, steps, seed):
    from neuralforecast.losses.pytorch import MQLoss
    from neuralforecast.models import NHITS
    return NHITS(h=h, input_size=INPUT_SIZE, loss=MQLoss(quantiles=list(qs)), max_steps=steps,
                 scaler_type="standard", start_padding_enabled=True, batch_size=256, windows_batch_size=1024,
                 random_seed=seed, enable_progress_bar=False, logger=False, enable_model_summary=False,
                 accelerator="cpu")


def quantile_columns(pred, qs):
    """Map the prediction columns of the MQLoss output to the quantile order of qs."""
    cols = [c for c in pred.columns if c not in ("unique_id", "ds", "cutoff")]
    # neuralforecast names quantile outputs 'NHITS-median', 'NHITS-lo-x', 'NHITS-hi-x' or 'NHITS_ql0.9'
    out = []
    for q in qs:
        cand = [c for c in cols if c.endswith(f"ql{q}") or c.endswith(f"_ql{q}")]
        if not cand:
            if q == 0.5:
                cand = [c for c in cols if c.endswith("median")]
            else:
                lvl = abs(2 * q - 1) * 100
                side = "hi" if q > 0.5 else "lo"
                cand = [c for c in cols if f"-{side}-" in c and abs(float(c.rsplit("-", 1)[1]) - lvl) < 1e-6]
        if len(cand) != 1:
            raise RuntimeError(f"cannot find the column of quantile {q} among {cols}")
        out.append(cand[0])
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dataset", required=True, choices=["M5", "VN1"])
    ap.add_argument("--offset", type=int, default=0, help="0 = main window, 26 = second, 52 = third")
    ap.add_argument("--h", type=int, default=3)
    ap.add_argument("--quick", action="store_true", help="smoke test: few steps, 300 series, not saved to the cache")
    a = ap.parse_args()
    from neuralforecast import NeuralForecast

    p = data.load(a.dataset)
    if a.offset:
        p = data.truncate(p, p["Y"].shape[1] - a.offset)
    Y = p["Y"].astype(np.float64)
    T = Y.shape[1]
    test0 = T - config.TEST_WEEKS
    origins = list(range(test0, T))
    sel = p["start"] <= test0 - config.VALID_WEEKS
    cls, _, _ = classify.classify(Y, p["start"], test0)
    sel &= cls != "none"
    rows = np.flatnonzero(sel)
    if a.quick:
        rows = np.random.default_rng(config.SEED).choice(rows, size=min(300, len(rows)), replace=False)
    print(f"fingerprint {a.dataset} w{a.offset}: {Y.shape[0]} series x {T} weeks, evaluated {int(sel.sum())}, "
          f"total sales of evaluated series {np.nansum(Y[sel]):.0f}", flush=True)
    qs = list(config.QUANTILES)
    h = a.h
    Z = forward_sums(Y, h)
    Q = np.full((Y.shape[0], len(origins), len(qs)), np.nan, np.float32)
    steps = QUICK_STEPS if a.quick else MAX_STEPS
    t_all = time.time()
    for c in range(test0, T, config.BLOCK_WEEKS):
        t0 = time.time()
        train = long_frame(Z, rows, np.full(len(rows), c - h))
        nf = NeuralForecast(models=[make_model(h, qs, steps, config.SEED)], freq=1)
        nf.fit(df=train)
        print(f"{a.dataset} w{a.offset} h{h} cutoff {c}: trained on {len(train):,} rows in {time.time() - t0:.0f}s", flush=True)
        for o in range(c, min(c + config.BLOCK_WEEKS, T)):
            hist = long_frame(Z, rows, np.full(len(rows), o - h))
            pred = nf.predict(df=hist)
            if "unique_id" not in pred.columns:
                pred = pred.reset_index()
            cols = quantile_columns(pred, qs)
            last = pred.sort_values("ds").groupby("unique_id").tail(1).set_index("unique_id")   # step h = Z[o]
            v = np.sort(np.maximum(last[cols].to_numpy(np.float64), 0), axis=1)
            Q[last.index.to_numpy(int), origins.index(o)] = v
        print(f"    origins {c}-{min(c + config.BLOCK_WEEKS, T) - 1} predicted ({time.time() - t0:.0f}s in block)", flush=True)
    miss = np.isnan(Q[rows]).any(axis=(1, 2)).mean()
    print(f"done in {time.time() - t_all:.0f}s; series with missing forecasts: {100 * miss:.2f}%", flush=True)
    if a.quick:
        Dt = np.stack([Z[rows, o] for o in origins], 1)
        cover = {q: np.nanmean(Dt <= Q[rows][:, :, k]) for k, q in enumerate(qs)}
        print("quick check, empirical coverage per quantile:", {q: round(v, 3) for q, v in cover.items()})
        return
    out = os.path.join(config.CACHE, "forecasts", a.dataset + (f"_w{a.offset}" if a.offset else ""))
    os.makedirs(out, exist_ok=True)
    np.savez_compressed(os.path.join(out, f"nhits_h{h}.npz"), Q=Q)
    print("written", os.path.join(out, f"nhits_h{h}.npz"))


if __name__ == "__main__":
    main()
