"""Feature builder (data_flow.md, section 5).

A row is (series i, origin o): the decision is taken at the start of week o using weeks < o only.
The target is the total demand of weeks o … o+h−1, D_h = Σ Y[i, o:o+h].

Level features (lags, rolling means/stds) are divided by a per-row scale s = mean weekly demand of the
last 52 active weeks (floored at 0.1), so one global model sees series of very different volume on a
common footing; the scale itself is kept as a feature and the quantile model is trained on D_h / s
(the pinball loss is scale-equivariant, so predictions are multiplied back by s).
"""
import numpy as np
import pandas as pd

LAGS = (1, 2, 3, 4, 8, 13, 26, 52)
WINDOWS = (4, 13, 26)
SCALE_WEEKS = 52
SCALE_FLOOR = 0.1


class Builder:
    def __init__(self, panel):
        self.p = panel
        Y = panel["Y"]
        self.n, self.T = Y.shape
        act = ~np.isnan(Y)
        Y0 = np.nan_to_num(Y)
        z = np.zeros((self.n, 1), np.float64)
        self.C = np.concatenate([z, np.cumsum(Y0, 1, dtype=np.float64)], 1)          # C[:, t] = Σ Y[:, :t]
        self.C2 = np.concatenate([z, np.cumsum(Y0.astype(np.float64) ** 2, 1)], 1)
        self.A = np.concatenate([z, np.cumsum(act, 1, dtype=np.float64)], 1)
        self.NZ = np.concatenate([z, np.cumsum(Y0 > 0, 1, dtype=np.float64)], 1)
        idx = np.where(Y0 > 0, np.arange(self.T)[None, :], -1)
        self.last_sale = np.maximum.accumulate(idx, axis=1)
        self.Y = Y
        self.start = panel["start"]

        attrs = panel["attrs"]
        if panel["name"] == "M5":
            self.static_names = ["dept_id", "cat_id", "store_id", "state_id"]
            state = attrs["state_id"].to_numpy()
            names = panel["event_names"]
            self.ev_event = panel["events"][:, names.index("n_event")]
            snap = np.stack([panel["events"][:, names.index(f"snap_{s}")] for s in ("CA", "TX", "WI")], 1)
            self.ev_snap = snap[:, pd.Index(["CA", "TX", "WI"]).get_indexer(state)].T      # [n, T]
        else:
            # VN1 Client/Warehouse are anonymous codes with 46/328 levels; as LightGBM categoricals they
            # overfit and produced exploding quantiles (code/README.md, "Design notes"), so they are not used.
            self.static_names = []
            self.ev_event = None
        self.static = np.stack([pd.factorize(attrs[c])[0] for c in self.static_names] or [np.zeros(self.n)],
                               1).astype(np.float32)[:, :len(self.static_names)]
        self.week0 = pd.Timestamp(panel["weeks"][0])

    # ---- helpers -------------------------------------------------------------------------------
    def window_sum(self, M, a, b):
        """Σ over weeks [a, b) (a, b clipped to the panel)."""
        a, b = max(a, 0), min(max(b, 0), self.T)
        return M[:, b] - M[:, a] if b > a else np.zeros(self.n)

    def target(self, o, h):
        if o + h > self.T:
            return np.full(self.n, np.nan)
        d = self.C[:, o + h] - self.C[:, o]
        return np.where(self.start < o + h, d, np.nan)

    def since_sale(self, o):
        """Weeks since the last positive sale before week o (o − start if the series never sold)."""
        ls = self.last_sale[:, o - 1]
        return np.where(ls >= 0, o - 1 - ls, o - self.start)

    def scale(self, o):
        cnt = self.window_sum(self.A, o - SCALE_WEEKS, o)
        s = self.window_sum(self.C, o - SCALE_WEEKS, o) / np.maximum(cnt, 1)
        return np.maximum(np.where(cnt > 0, s, 1.0), SCALE_FLOOR)

    @property
    def names(self):
        n = [f"lag_{k}" for k in LAGS] + [f"mean_{w}" for w in WINDOWS] + [f"std_{w}" for w in WINDOWS]
        n += ["zero_share_13", "weeks_since_sale", "week_of_year", "month"]
        if self.ev_event is not None:
            n += ["n_event", "snap_days"]
        n += ["price", "price_change_4"]
        # No "price_observed" flag for VN1: prices are only reported in weeks with sales, so the flag
        # duplicates lag_1 > 0 in training, and Phase 2 has no prices at all, which would set it to 0
        # for every series in the second test block (train/test shift).
        return n + self.static_names + ["scale"]

    @property
    def categorical(self):
        return self.static_names

    # ---- one origin -----------------------------------------------------------------------------
    def row(self, o, h):
        """Features of all series at origin o for a target of h weeks. Returns X [n, F], scale [n]."""
        s = self.scale(o)
        cols = []
        for k in LAGS:
            cols.append(self.Y[:, o - k] / s if o - k >= 0 else np.full(self.n, np.nan))
        for w in WINDOWS:
            cnt = self.window_sum(self.A, o - w, o)
            m = self.window_sum(self.C, o - w, o) / np.where(cnt > 0, cnt, np.nan)
            cols.append(m / s)
        for w in WINDOWS:
            cnt = self.window_sum(self.A, o - w, o)
            m = self.window_sum(self.C, o - w, o) / np.where(cnt > 0, cnt, np.nan)
            m2 = self.window_sum(self.C2, o - w, o) / np.where(cnt > 0, cnt, np.nan)
            cols.append(np.sqrt(np.maximum(m2 - m ** 2, 0)) / s)
        cnt = self.window_sum(self.A, o - 13, o)
        cols.append(1 - self.window_sum(self.NZ, o - 13, o) / np.where(cnt > 0, cnt, np.nan))
        ls = self.last_sale[:, o - 1]
        cols.append(np.where(ls >= 0, o - 1 - ls, o - self.start).astype(np.float64))
        wk = self.week0 + pd.Timedelta(weeks=o)
        cols.append(np.full(self.n, wk.isocalendar().week, np.float64))
        cols.append(np.full(self.n, wk.month, np.float64))
        if self.ev_event is not None:
            a, b = o, min(o + h, self.T)
            cols.append(np.full(self.n, self.ev_event[a:b].sum(), np.float64))
            cols.append(self.ev_snap[:, a:b].sum(1).astype(np.float64))
        P = self.p["P"]
        cols.append(P[:, o - 1])
        with np.errstate(divide="ignore", invalid="ignore"):
            cols.append(P[:, o - 1] / P[:, o - 5] - 1 if o >= 5 else np.full(self.n, np.nan))
        X = np.column_stack(cols + [self.static, s[:, None]]).astype(np.float32)
        return X, s

    def rows(self, origins, h, series=None, need_target=False, min_history=13):
        """Stack rows for several origins. Keeps series with ≥ min_history active weeks before o."""
        Xs, S, D, I, O = [], [], [], [], []
        sel = np.ones(self.n, bool) if series is None else series
        for o in origins:
            X, s = self.row(o, h)
            keep = sel & (o - self.start >= min_history)
            d = self.target(o, h)
            if need_target:
                keep &= ~np.isnan(d)
            idx = np.flatnonzero(keep)
            Xs.append(X[idx]); S.append(s[idx]); D.append(d[idx]); I.append(idx); O.append(np.full(len(idx), o))
        return (np.concatenate(Xs), np.concatenate(S), np.concatenate(D),
                np.concatenate(I), np.concatenate(O))
