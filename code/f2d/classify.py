"""ADI–CV² demand classes (data_flow.md, section 4)."""
import numpy as np

from . import config

CLASSES = ("smooth", "erratic", "intermittent", "lumpy")


def adi_cv2(Y, start, end):
    """ADI and CV² of each series over weeks [start_i, end).

    ADI = active weeks / weeks with a sale; CV² = (std / mean)² of the positive weeks (ddof = 0).
    """
    t = np.arange(Y.shape[1])[None, :]
    win = (t >= start[:, None]) & (t < end)
    y = np.where(win, np.nan_to_num(Y), 0.0)
    pos = y > 0
    n_act = win.sum(1)
    nnz = pos.sum(1)
    with np.errstate(divide="ignore", invalid="ignore"):
        adi = n_act / nnz
        mean = y.sum(1) / nnz
        var = (y ** 2).sum(1) / nnz - mean ** 2
        cv2 = var / mean ** 2
    return adi, cv2, nnz


def classify(Y, start, end):
    adi, cv2, nnz = adi_cv2(Y, start, end)
    cls = np.where(adi < config.ADI_CUT, np.where(cv2 < config.CV2_CUT, "smooth", "erratic"),
                   np.where(cv2 < config.CV2_CUT, "intermittent", "lumpy"))
    cls = np.where(nnz > 0, cls, "none")
    return cls, adi, cv2
