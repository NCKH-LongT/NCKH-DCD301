"""Decision Engine and multi-period lost-sales inventory simulator (system_architecture.md §4, data_flow.md §7).

Timeline of test week k (origin o = first test week + k), vectorised over series:
    1. receive the order placed L weeks ago;
    2. review (every R = 1 week) with the forecast made at o from weeks < o:
         IP = on-hand + on-order
         liquidate  x = min(max(IP − T_liq, 0), on-hand)            (T_liq = ∞ for "no liquidation")
         order      q = 0 if x > 0 else max(S − IP, 0)             (S = order-up-to level)
    3. demand of week o arrives; sales = min(on-hand, demand); the rest is lost.
Levels are rounded up to whole units. Initial on-hand = S of the first review, nothing on order.
"""
import numpy as np

ACTIONS = np.array(["HOLD", "ORDER", "LIQUIDATE"])


def simulate(D, S, T_liq, L):
    """D, S, T_liq: [n, W] demand, order-up-to level, liquidation threshold (np.inf = none)."""
    n, W = D.shape
    S = np.ceil(S)
    T_liq = np.ceil(T_liq)
    on_hand = S[:, 0].copy()
    pipe = np.zeros((n, W + L + 1))
    out = {k: np.zeros((n, W)) for k in ("on_hand_end", "sales", "lost", "liq", "order", "ip", "action")}
    for k in range(W):
        on_hand += pipe[:, k]
        ip = on_hand + pipe[:, k + 1: k + L + 1].sum(1) if L > 0 else on_hand.copy()
        liq = np.minimum(np.maximum(ip - T_liq[:, k], 0), on_hand)
        on_hand -= liq
        ip -= liq
        order = np.where(liq > 0, 0.0, np.maximum(S[:, k] - ip, 0))
        pipe[:, k + L] += order
        sales = np.minimum(on_hand, D[:, k])
        on_hand -= sales
        out["on_hand_end"][:, k] = on_hand
        out["sales"][:, k] = sales
        out["lost"][:, k] = D[:, k] - sales
        out["liq"][:, k] = liq
        out["order"][:, k] = order
        out["ip"][:, k] = ip
        out["action"][:, k] = np.where(liq > 0, 2, np.where(order > 0, 1, 0))
    return out


def stockout_risk(Q, qs, ip):
    """P(D_{L+R} > IP) for one review week. Q: [m, n_q] sorted quantiles, ip: [m].

    The CDF is interpolated linearly through (0, 0) — or (0, q_min) when Q_{q_min} = 0 — and the points
    (Q_q, q); above the highest quantile it is set to 1, so the risk there is reported as 0."""
    qs = np.asarray(qs, float)
    risk = np.full(len(ip), np.nan)
    for i in range(len(ip)):
        x = Q[i]
        if not np.all(np.isfinite(x)):
            continue
        fp = np.r_[0.0 if x[0] > 0 else qs[0], qs]
        risk[i] = 1 - np.interp(ip[i], np.r_[0.0, x], fp, right=1.0)
    return risk


def deadstock(S, since_sale, N):
    """Dead-stock rule: a series without any sale in the last N weeks (since_sale >= N, known at the review)
    liquidates all on-hand stock and is not replenished until it sells again.

    S, since_sale: [n, W]. Returns (S_eff, T_liq) for simulate()."""
    dead = since_sale >= N
    return np.where(dead, 0.0, S), np.where(dead, 0.0, np.inf)
