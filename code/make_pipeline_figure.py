"""Figure 1 of the journal draft: the forecast-to-decision pipeline.

Writes 07_paper_draft/figures/fig_pipeline.png (300 dpi) and .pdf.

Usage:
    python code/make_pipeline_figure.py
"""
import os

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "07_paper_draft", "figures")

STAGES = [
    ("Data", "M5 (30,490 series)\nVN1 (15,053 series)\nweekly panels,\nall series kept"),
    ("Forecasts", "8 methods + 2 combinations\nquantiles 0.5–0.99 of the\nh-week total (h = 3, 13)\n26 weekly origins,\nrefit every 13 weeks"),
    ("Decision layer", "order-up-to $S = Q_\\tau(D_{L+1})$\nlost sales, L = 1 / 2 / 4\nliquidation: none, quantile,\nfixed, dead13"),
    ("Trade-off curves", "simulate τ ∈ {0.5, …, 0.99}\nfill rate vs inventory\n(weeks of demand)"),
    ("Evaluation", "inventory at equal fill rate\nfrontier rank, regret\nbootstrap CIs (200)\ncost view C(r), break-even s*"),
]
ROBUST = "Repeated on 3 test windows (offset 0 / 26 / 52 weeks), 3 lead times, 4 hyper-parameter settings"


def main():
    os.makedirs(OUT, exist_ok=True)
    fig, ax = plt.subplots(figsize=(11, 2.9))
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 26)
    ax.axis("off")
    w, gap, y, hgt = 16.6, 3.5, 8, 17
    x = 1.0
    centers = []
    for title, body in STAGES:
        ax.add_patch(FancyBboxPatch((x, y), w, hgt, boxstyle="round,pad=0.3,rounding_size=1.2",
                                    linewidth=1.0, edgecolor="#3b4a6b", facecolor="#eef2f8"))
        ax.text(x + w / 2, y + hgt - 2.6, title, ha="center", va="center", fontsize=10, fontweight="bold", color="#1f2a44")
        ax.text(x + w / 2, y + (hgt - 4.0) / 2 + 0.3, body, ha="center", va="center", fontsize=7.6, color="#1f2a44", linespacing=1.35)
        centers.append(x + w / 2)
        x += w + gap
    for i in range(len(STAGES) - 1):
        x0 = 1.0 + (i + 1) * w + i * gap + 0.5
        ax.add_patch(FancyArrowPatch((x0, y + hgt / 2), (x0 + gap - 0.8, y + hgt / 2), arrowstyle="-|>",
                                     mutation_scale=12, linewidth=1.2, color="#3b4a6b"))
    ax.add_patch(FancyBboxPatch((1.0, 1.2), 98, 4.6, boxstyle="round,pad=0.2,rounding_size=1.0",
                                linewidth=0.8, edgecolor="#8a6d1f", facecolor="#fbf4e1"))
    ax.text(50, 3.5, ROBUST, ha="center", va="center", fontsize=8.2, color="#5a4510")
    fig.tight_layout()
    for ext in ("png", "pdf"):
        fig.savefig(os.path.join(OUT, f"fig_pipeline.{ext}"), dpi=300, bbox_inches="tight")
    print("written 07_paper_draft/figures/fig_pipeline.png/.pdf")


if __name__ == "__main__":
    main()
