"""Shared loading for the P0–P1 robustness scripts (prospective_tau.py, bootstrap_robust.py, censoring_sensitivity.py).

load_window(dataset, offset) -> dict with the panel, selected series, test demand D [n, 26] and the cached h = 3 quantile
forecasts of the seven single methods plus C2 (mean of LGB-Q and TSB-NB) and E7-med (median of the seven).
"""
import os
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from combination import setup  # noqa: E402
from f2d import config, policy  # noqa: E402
from segment_eval import MODELS  # noqa: E402

H = config.DEFAULT["L"] + config.DEFAULT["R"]
WINDOWS = {"third": 52, "second": 26, "main": 0}
METHODS = MODELS + ["C2", "E7-med"]
LAB = {"empirical": "EMP", "tsb_nb": "TSB-NB", "ets": "ETS", "lgb_tweedie": "LGB-T", "lgb_conformal": "LGB-C",
       "hgb_quantile": "HGB-Q", "lgb_quantile": "LGB-Q", "C2": "C2", "E7-med": "E7-med"}
EVAL_W = slice(config.WARMUP_WEEKS, None)


def load_window(d, off):
    p, idx, test0, T = setup(d, off)
    D = np.nan_to_num(p["Y"][:, test0:T]).astype(np.float64)[idx]
    fc = os.path.join(config.CACHE, "forecasts", d + (f"_w{off}" if off else ""))
    Q = {m: np.load(os.path.join(fc, f"{m}_h{H}.npz"))["Q"][idx].astype(np.float64) for m in MODELS}
    Q["C2"] = (Q["lgb_quantile"] + Q["tsb_nb"]) / 2
    Q["E7-med"] = np.median([Q[m] for m in MODELS], 0)
    return dict(p=p, idx=idx, test0=test0, T=T, D=D, Q=Q)


def level(Qm, tau):
    """Order-up-to level for any τ in [0.5, 0.99]: linear interpolation between the cached quantiles."""
    qs = np.asarray(config.QUANTILES)
    tau = float(np.clip(tau, qs[0], qs[-1]))
    j = min(int(np.searchsorted(qs, tau, side="right")) - 1, len(qs) - 2)
    w = (tau - qs[j]) / (qs[j + 1] - qs[j])
    return (1 - w) * Qm[:, :, j] + w * Qm[:, :, j + 1]


def run(D, S):
    sim = policy.simulate(D, S, np.full_like(S, np.inf), config.DEFAULT["L"])
    return sim["sales"][:, EVAL_W], sim["on_hand_end"][:, EVAL_W]
