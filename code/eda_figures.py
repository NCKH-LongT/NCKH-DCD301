"""Exploratory figures of M5 and VN1 for the presentation (Vietnamese labels).

Every figure uses the evaluated series of run_pipeline.py (≥ 13 weeks of history before the test period, at least
one sale) and, unless stated, features computed on the weeks before the main test period.
    eda_1_sales_over_time.png      total weekly sales, with the three 26-week test windows shaded
    eda_2_demand_classes.png       share of series in each ADI–CV² class
    eda_3_feature_distributions.png distributions of six series features, M5 vs VN1
    eda_4_adi_cv2.png              ADI–CV² scatter with the class thresholds
    eda_5_growth_by_window.png     demand change between the 26 weeks before a test window and the window itself
    eda_6_correlation.png          Spearman correlation of the series features
Writes code/outputs/eda/*.png and eda_summary.md (the numbers quoted in the figures).

Usage:
    python code/eda_figures.py
"""
import os
import sys

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy import stats

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from f2d import classify, config, data  # noqa: E402

OUT = os.path.join(config.OUTPUTS, "eda")
# Validated categorical palette (dataviz skill, default instance): slot 1 blue, 2 orange, 3 aqua.
C1, C2, C3 = "#2a78d6", "#eb6834", "#1baf7a"
COLOR = {"M5": C1, "VN1": C2}
INK, INK2, GRID, SURFACE = "#0b0b0b", "#52514e", "#e4e3df", "#fcfcfb"
DIV_LO, DIV_MID, DIV_HI = "#2a78d6", "#f0efec", "#e34948"
WINDOWS = {0: "chính", 26: "thứ hai", 52: "thứ ba"}
CLASS_VI = {"smooth": "smooth\n(đều)", "erratic": "erratic\n(thất thường)",
            "intermittent": "intermittent\n(gián đoạn)", "lumpy": "lumpy\n(gián đoạn,\nthất thường)"}

plt.rcParams.update({
    "font.family": "DejaVu Sans", "font.size": 10, "axes.edgecolor": GRID, "axes.labelcolor": INK2,
    "axes.titlecolor": INK, "axes.titleweight": "bold", "axes.titlesize": 11, "xtick.color": INK2,
    "ytick.color": INK2, "axes.grid": True, "grid.color": GRID, "grid.linewidth": 0.6, "axes.axisbelow": True,
    "figure.facecolor": SURFACE, "axes.facecolor": SURFACE, "savefig.facecolor": SURFACE, "legend.frameon": False,
    "axes.spines.top": False, "axes.spines.right": False, "lines.linewidth": 2,
})


def evaluated(p, offset=0):
    """Selection, classes and test start of one window (as in run_pipeline.py)."""
    if offset:
        p = data.truncate(p, p["Y"].shape[1] - offset)
    Y = p["Y"].astype(np.float64)
    T = Y.shape[1]
    test0 = T - config.TEST_WEEKS
    sel = p["start"] <= test0 - config.VALID_WEEKS
    cls, adi, cv2 = classify.classify(Y, p["start"], test0)
    sel &= cls != "none"
    return p, Y, test0, sel, cls, adi, cv2


def features(p, Y, test0, sel, adi, cv2):
    """Per-series features on the weeks before test0 (evaluated series only)."""
    start = p["start"].astype(int)
    t = np.arange(Y.shape[1])[None, :]
    hist = (t >= start[:, None]) & (t < test0)
    Y0 = np.nan_to_num(Y)
    n_act = hist.sum(1)
    mean = (Y0 * hist).sum(1) / np.maximum(n_act, 1)
    zero = ((Y0 == 0) & hist).sum(1) / np.maximum(n_act, 1)
    last = np.where((Y0 > 0) & hist, t, -1).max(1)
    since = np.where(last >= 0, test0 - 1 - last, n_act)
    prev = (Y0[:, test0 - 26:test0]).sum(1)
    older = (Y0[:, test0 - 52:test0 - 26]).sum(1)
    with np.errstate(divide="ignore", invalid="ignore"):
        trend = np.log2((prev + 1) / (older + 1))
    f = pd.DataFrame({"mean_week": mean, "zero_share": zero, "adi": adi, "cv2": cv2, "hist_len": n_act,
                      "since_sale": since, "trend_26": trend})
    return f[sel].reset_index(drop=True)


def kde_line(ax, x, color, label, lo, hi, log=False, ls="-"):
    x = np.asarray(x, float)
    x = x[np.isfinite(x)]
    if log:
        x = np.log10(x[x > 0])
        lo, hi = np.log10(lo), np.log10(hi)
    x = np.clip(x, lo, hi)
    g = np.linspace(lo, hi, 300)
    k = stats.gaussian_kde(x, bw_method=0.15)(g)
    gx = 10 ** g if log else g
    ax.fill_between(gx, k, color=color, alpha=0.18, linewidth=0)
    ax.plot(gx, k, color=color, label=label, ls=ls)
    if log:
        ax.set_xscale("log")


def fig_sales(panels, summary):
    fig, axes = plt.subplots(2, 1, figsize=(11, 6.2))
    for ax, (name, p) in zip(axes, panels.items()):
        Y = p["Y"]
        T = Y.shape[1]
        tot = np.nansum(Y, 0)
        wk = pd.DatetimeIndex(p["weeks"])
        for off, lab in WINDOWS.items():
            a, b = T - off - config.TEST_WEEKS, T - off
            ax.axvspan(wk[a], wk[b - 1], color=COLOR[name], alpha=0.10, linewidth=0)
            ax.text(wk[a + (b - a) // 2], 1.0, f"cửa sổ\n{lab}", transform=ax.get_xaxis_transform(), ha="center",
                    va="top", fontsize=8.5, color=INK2)
        ax.plot(wk, tot / 1e3, color=COLOR[name])
        ax.set_title(f"{name}: tổng doanh số mỗi tuần (nghìn đơn vị)", loc="left")
        ax.set_ylim(0, tot.max() / 1e3 * 1.3)
        ax.set_ylabel("nghìn đơn vị / tuần")
        summary.append(f"- {name}: {Y.shape[0]:,} chuỗi × {T} tuần ({wk[0].date()} → {wk[-1].date()}); "
                       f"tổng tuần cao nhất {tot.max():,.0f}, thấp nhất {tot[tot > 0].min():,.0f}")
    fig.text(0.01, 0.005, "Vùng tô màu: ba cửa sổ kiểm thử, mỗi cửa sổ 26 tuần (mô hình chỉ dùng dữ liệu trước cửa sổ).",
             fontsize=8.5, color=INK2)
    fig.tight_layout(rect=(0, 0.02, 1, 1))
    fig.savefig(os.path.join(OUT, "eda_1_sales_over_time.png"), dpi=200)
    plt.close(fig)


def fig_classes(ev, summary):
    share = {d: pd.Series(e["cls"][e["sel"]]).value_counts(normalize=True).reindex(classify.CLASSES).fillna(0)
             for d, e in ev.items()}
    fig, ax = plt.subplots(figsize=(9, 4.6))
    x = np.arange(len(classify.CLASSES))
    w = 0.38
    for k, (d, s) in enumerate(share.items()):
        xs = x + (k - 0.5) * (w + 0.02)
        ax.bar(xs, s.to_numpy() * 100, width=w, color=COLOR[d], label=f"{d} ({int(ev[d]['sel'].sum()):,} chuỗi)")
        for xi, v in zip(xs, s.to_numpy()):
            ax.text(xi, v * 100 + 1, f"{100 * v:.0f}%", ha="center", va="bottom", fontsize=9, color=INK)
    ax.set_xticks(x, [CLASS_VI[c] for c in classify.CLASSES])
    ax.set_ylabel("% số chuỗi")
    ax.set_ylim(0, max(s.max() for s in share.values()) * 100 + 10)
    ax.set_title("Phân loại nhu cầu ADI–CV² (giai đoạn trước cửa sổ chính)", loc="left")
    ax.legend(loc="upper right")
    ax.grid(axis="x", visible=False)
    fig.tight_layout()
    fig.savefig(os.path.join(OUT, "eda_2_demand_classes.png"), dpi=200)
    plt.close(fig)
    summary.append("")
    summary.append("| Nhóm | " + " | ".join(share) + " |")
    summary.append("|---|" + "---|" * len(share))
    for c in classify.CLASSES:
        summary.append(f"| {c} | " + " | ".join(f"{100 * share[d][c]:.1f}%" for d in share) + " |")


SPEC = [  # column, title, x label, lo, hi, log
    ("mean_week", "Mức bán trung bình mỗi tuần", "đơn vị / tuần (thang log)", 0.01, 1000, True),
    ("zero_share", "Tỷ lệ tuần không bán được", "tỷ lệ tuần bán = 0", 0, 1, False),
    ("adi", "ADI: khoảng cách giữa hai lần bán", "tuần (thang log)", 1, 60, True),
    ("cv2", "CV²: độ dao động lượng bán", "CV² (thang log)", 0.01, 10, True),
    ("hist_len", "Độ dài lịch sử", "số tuần", 0, 260, False),
    ("trend_26", "Xu hướng 26 tuần gần nhất", "log₂(26 tuần gần / 26 tuần trước)", -4, 4, False),
]


def fig_features(feat, summary):
    fig, axes = plt.subplots(2, 3, figsize=(13, 7))
    for ax, (col, title, xl, lo, hi, log) in zip(axes.ravel(), SPEC):
        for d, f in feat.items():
            kde_line(ax, f[col], COLOR[d], d, lo, hi, log, ls="-" if d == "M5" else "--")
        ax.set_title(title, loc="left")
        ax.set_xlabel(xl)
        ax.set_ylabel("mật độ")
        ax.set_yticklabels([])
        if col in ("adi", "cv2"):
            cut = config.ADI_CUT if col == "adi" else config.CV2_CUT
            ax.axvline(cut, color=INK2, lw=1, ls=":")
            ax.text(cut, 0.97, " ngưỡng " + ("4/3" if col == "adi" else "0,5"), transform=ax.get_xaxis_transform(), fontsize=8, color=INK2,
                    va="top")
    axes[0, 0].legend(loc="upper left")
    fig.suptitle("So sánh phân phối đặc trưng chuỗi: M5 (cửa hàng) và VN1 (thương mại điện tử)", x=0.01, ha="left",
                 fontweight="bold", color=INK)
    fig.tight_layout()
    fig.savefig(os.path.join(OUT, "eda_3_feature_distributions.png"), dpi=200)
    plt.close(fig)
    summary += ["", "| Đặc trưng (trung vị) | " + " | ".join(feat) + " | KS |", "|---|" + "---|" * (len(feat) + 1)]
    for col, title, *_ in SPEC:
        a, b = (feat[d][col].replace([np.inf, -np.inf], np.nan).dropna() for d in feat)
        summary.append(f"| {title} | {a.median():.3g} | {b.median():.3g} | {stats.ks_2samp(a, b).statistic:.2f} |")


def fig_adi_cv2(feat):
    fig, axes = plt.subplots(1, 2, figsize=(12, 5), sharey=True)
    rng = np.random.default_rng(config.SEED)
    for ax, (d, f) in zip(axes, feat.items()):
        s = f.iloc[rng.choice(len(f), min(6000, len(f)), replace=False)]
        ax.scatter(np.clip(s.adi, 1, 100), np.clip(s.cv2, 1e-3, 30), s=4, color=COLOR[d], alpha=0.25, linewidths=0)
        ax.axhspan(6e-4, 1.6e-3, color=GRID, alpha=0.5, linewidth=0)
        ax.text(1.02, 1.8e-3, f"CV² = 0 ({100 * np.mean(f.cv2 <= 1e-3):.0f}% số chuỗi: mỗi lần bán đúng một lượng)",
                fontsize=8, color=INK2, va="bottom")
        ax.set_xscale("log")
        ax.set_yscale("log")
        ax.axvline(config.ADI_CUT, color=INK2, lw=1, ls=":")
        ax.axhline(config.CV2_CUT, color=INK2, lw=1, ls=":")
        ax.set_ylim(6e-4, 40)
        for x, y, t in [(1.05, 0.02, "smooth"), (1.05, 15, "erratic"), (8, 0.02, "intermittent"),
                        (8, 15, "lumpy")]:
            ax.text(x, y, t, fontsize=9, color=INK, fontweight="bold")
        ax.set_xlabel("ADI (tuần, thang log)")
        ax.set_title(f"{d}: {len(f):,} chuỗi (vẽ ngẫu nhiên {len(s):,})", loc="left")
    axes[0].set_ylabel("CV² (thang log)")
    fig.suptitle("Bản đồ ADI–CV²: đường chấm là ngưỡng phân loại (ADI = 4/3, CV² = 0,5)", x=0.01, ha="left",
                 fontweight="bold", color=INK)
    fig.tight_layout()
    fig.savefig(os.path.join(OUT, "eda_4_adi_cv2.png"), dpi=200)
    plt.close(fig)


def fig_growth(panels, summary):
    fig, axes = plt.subplots(1, 3, figsize=(14, 4.6), sharey=True)
    summary += ["", "| Dataset | Cửa sổ | Chuỗi tăng > 1,5× | Chuỗi giảm < 0,67× | Trung vị log₂ thay đổi |",
                "|---|---|---|---|---|"]
    for ax, (off, lab) in zip(axes, WINDOWS.items()):
        for name, p0 in panels.items():
            p, Y, test0, sel, *_ = evaluated(p0, off)
            Y0 = np.nan_to_num(Y)
            prev = Y0[:, test0 - 26:test0].sum(1)[sel]
            test = Y0[:, test0:].sum(1)[sel]
            g = np.log2((test + 1) / (prev + 1))
            up, down = np.mean(test > 1.5 * prev), np.mean(test < prev / 1.5)
            kde_line(ax, g, COLOR[name], f"{name}: tăng >1,5× {up:.0%}, giảm >1,5× {down:.0%}", -4, 4,
                     ls="-" if name == "M5" else "--")
            summary.append(f"| {name} | {lab} | {up:.1%} | {down:.1%} | {np.median(g):+.2f} |")
        ax.set_title(f"Cửa sổ {lab}", loc="left")
        ax.set_xlabel("log₂(nhu cầu trong cửa sổ / 26 tuần trước)\n← giảm        tăng →")
        ax.set_yticklabels([])
        ax.legend(loc="upper left", fontsize=8.5)
    top = max(l.get_ydata().max() for ax in axes for l in ax.get_lines())
    for ax in axes:
        ax.set_ylim(0, top * 1.45)
        ax.axvline(0, ymax=1 / 1.45, color=INK2, lw=1)
    axes[0].set_ylabel("mật độ")
    fig.suptitle("Nhu cầu thay đổi thế nào khi bước vào cửa sổ kiểm thử (distribution shift theo thời gian)",
                 x=0.01, ha="left", fontweight="bold", color=INK)
    fig.text(0.01, 0.005, "Mỗi đường là phân phối trên các chuỗi. Giá trị ngoài ±4 (thay đổi hơn 16 lần) được dồn về hai "
             "biên, nên có gờ nhỏ ở hai đầu.", fontsize=8.5, color=INK2)
    fig.tight_layout(rect=(0, 0.03, 1, 1))
    fig.savefig(os.path.join(OUT, "eda_5_growth_by_window.png"), dpi=200)
    plt.close(fig)


def fig_corr(feat):
    from matplotlib.colors import LinearSegmentedColormap
    cmap = LinearSegmentedColormap.from_list("div", [DIV_LO, DIV_MID, DIV_HI])
    # ADI is a function of the zero share (ADI = 1 / (1 − zero share)), so it is replaced by weeks since the last sale
    cols = ["mean_week", "zero_share", "since_sale", "cv2", "hist_len", "trend_26"]
    names = ["mức bán", "tỷ lệ\ntuần = 0", "tuần từ lần\nbán cuối", "CV²", "độ dài\nlịch sử", "xu hướng"]
    fig, axes = plt.subplots(1, 2, figsize=(12, 5.2))
    for ax, (d, f) in zip(axes, feat.items()):
        r = f[cols].replace([np.inf, -np.inf], np.nan).corr(method="spearman").to_numpy()
        im = ax.imshow(r, cmap=cmap, vmin=-1, vmax=1)
        ax.set_xticks(range(len(cols)), [n.replace("\n", " ") for n in names], fontsize=8.5, rotation=35, ha="right")
        ax.set_yticks(range(len(cols)), names, fontsize=8.5)
        ax.grid(False)
        for i in range(len(cols)):
            for j in range(len(cols)):
                ax.text(j, i, f"{r[i, j]:.2f}", ha="center", va="center", fontsize=8.5,
                        color="white" if abs(r[i, j]) > 0.6 else INK)
        ax.set_title(d, loc="left")
    fig.colorbar(im, ax=axes, shrink=0.8, label="tương quan Spearman")
    fig.suptitle("Tương quan giữa các đặc trưng chuỗi (trước cửa sổ chính)", x=0.01, ha="left", fontweight="bold",
                 color=INK)
    fig.savefig(os.path.join(OUT, "eda_6_correlation.png"), dpi=200, bbox_inches="tight")
    plt.close(fig)


def main():
    os.makedirs(OUT, exist_ok=True)
    panels = {d: data.load(d) for d in ("M5", "VN1")}
    ev, feat = {}, {}
    for d, p in panels.items():
        q, Y, test0, sel, cls, adi, cv2 = evaluated(p)
        ev[d] = dict(sel=sel, cls=cls)
        feat[d] = features(q, Y, test0, sel, adi, cv2)
        print(f"{d}: {int(sel.sum()):,} evaluated series", flush=True)
    summary = ["# Số liệu trong các biểu đồ EDA (generated by code/eda_figures.py)", "", "## Dữ liệu", ""]
    fig_sales(panels, summary)
    summary += ["", "## Phân loại ADI–CV² (cửa sổ chính)"]
    fig_classes(ev, summary)
    summary += ["", "## Đặc trưng chuỗi (cửa sổ chính)"]
    fig_features(feat, summary)
    fig_adi_cv2(feat)
    summary += ["", "## Thay đổi nhu cầu khi vào cửa sổ kiểm thử"]
    fig_growth(panels, summary)
    fig_corr(feat)
    with open(os.path.join(OUT, "eda_summary.md"), "w", encoding="utf-8") as f:
        f.write("\n".join(summary) + "\n")
    print("written", OUT)


if __name__ == "__main__":
    main()
