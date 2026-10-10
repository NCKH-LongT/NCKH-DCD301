"""Draw the benchmark pipeline figure of the paper (Figure 1).

Writes 06_experiment_results/figures/fig_pipeline.png.

Usage:
    python code/make_pipeline_figure.py
"""
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "06_experiment_results", "figures", "fig_pipeline.png")

BOXES = [  # (x, y, width, height, title, body, colour)
    (0.02, 0.56, 0.17, 0.34, "Weekly panel", "M5 (30,490 series)\nVN1 (15,053 series)\nVNF case study (1,001)", "#e8eef7"),
    (0.22, 0.56, 0.17, 0.34, "Demand classes", "ADI–CV²\nsmooth / erratic /\nintermittent / lumpy", "#e8eef7"),
    (0.42, 0.56, 0.17, 0.34, "Features", "lags, rolling stats,\nzero share, price,\ncalendar, scale s", "#e8eef7"),
    (0.62, 0.56, 0.36, 0.34, "Probabilistic forecasts", "quantiles q ∈ {0.5, 0.8, 0.9, 0.95, 0.99}\nof D_{L+R} and D_H, at every weekly origin\n8 methods (4 statistical, 4 boosting)\n+ Chronos-2 (zero-shot, Section 5.8)", "#fdf0e0"),
    (0.62, 0.08, 0.36, 0.36, "Decision layer (transparent rules)", "ORDER up to S = Q_τ(D_{L+R})\nLIQUIDATE above T_liq:\nquantile Q_{q_L}(D_H) / fixed k weeks /\ndead-stock 13 or 26 weeks; else HOLD", "#e6f4ea"),
    (0.32, 0.08, 0.26, 0.36, "Lost-sales simulation", "26 weeks, lead time L,\nreview R = 1 week,\n4 warm-up weeks\n(three test windows)", "#e6f4ea"),
    (0.02, 0.08, 0.26, 0.36, "Cost-free evaluation", "fill rate, stockouts, weeks of\ninventory; trade-off curves,\nfrontier rank, bootstrap CIs;\nbreak-even salvage ratio s*", "#f3e8f7"),
]


def main():
    fig, ax = plt.subplots(figsize=(11, 4.6))
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")
    centers = []
    for x, y, w, h, title, body, col in BOXES:
        ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.008,rounding_size=0.015",
                                    fc=col, ec="#555555", lw=1.0))
        ax.text(x + w / 2, y + h - 0.055, title, ha="center", va="top", fontsize=10, fontweight="bold")
        ax.text(x + w / 2, y + h / 2 - 0.05, body, ha="center", va="center", fontsize=8.3, linespacing=1.35)
        centers.append((x, y, w, h))

    def arrow(p, q):
        ax.add_patch(FancyArrowPatch(p, q, arrowstyle="-|>", mutation_scale=14, lw=1.2, color="#333333"))

    # top row left to right
    for i in range(3):
        x, y, w, h = centers[i]
        x2, y2, w2, h2 = centers[i + 1]
        arrow((x + w + 0.003, y + h / 2), (x2 - 0.003, y2 + h2 / 2))
    # forecasts down to decision layer
    x, y, w, h = centers[3]
    x2, y2, w2, h2 = centers[4]
    arrow((x + w / 2, y - 0.005), (x2 + w2 / 2, y2 + h2 + 0.005))
    # bottom row right to left
    for i in (4, 5):
        x, y, w, h = centers[i]
        x2, y2, w2, h2 = centers[i + 1]
        arrow((x - 0.003, y + h / 2), (x2 + w2 + 0.003, y2 + h2 / 2))
    fig.tight_layout()
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    fig.savefig(OUT, dpi=200)
    print("written", OUT)


if __name__ == "__main__":
    main()
