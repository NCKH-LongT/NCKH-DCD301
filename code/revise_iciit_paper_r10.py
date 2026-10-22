"""Introduction ends with an explicit list of contributions (08_final_submission/ICIIT2027_Paper_rev9.docx -> rev10;
must stay at 10 pages). Every claim restates a result already reported in Sections 5-6.

Usage:
    python code/revise_iciit_paper_r10.py --src 08_final_submission/ICIIT2027_Paper_rev9.docx --out 08_final_submission/ICIIT2027_Paper_rev10.docx
"""
import argparse
import os
import sys

import docx
from docx.shared import Pt

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from revise_iciit_paper_r7 import clone_after, find, set_text  # noqa: E402

LEAD = ("We hold the inventory policy fixed and vary only its demand forecasts. Seven methods are evaluated on every "
        "eligible series in M5 and VN1, with weekly decisions simulated over three 26-week windows per dataset and "
        "inventory compared at matched realised fill rates. Our contributions are as follows.")

BULLETS = [
    "Evidence across settings and periods. Accuracy and inventory rankings agree on M5, where LGB-Q needs 3–11% less "
    "stock than the alternatives in every window, but not on VN1, where the leading method changes between windows.",
    "Limits of prospective method selection. Pre-test demand classes, clusters and the previous window's leader do not "
    "reliably identify the best method, and reweighting VN1 to M5's feature distribution leaves the VN1 findings unchanged.",
    "A pre-specified combination with ablation. The median of the seven methods' quantiles needs 7–8% less VN1 inventory "
    "than LGB-Q and has the lowest maximum regret (0.3%), but gives no gain on M5; the ablation shows that the direct "
    "quantile learners contribute most and that adding ETS hurts. An earlier average of two methods (C2) is reported as "
    "post hoc.",
    "Decision guidance and robustness. A break-even salvage ratio states when liquidation pays, and checks on lead time, "
    "hyperparameters, censored demand and computing cost show which findings are stable. Code and results are public.",
]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--src", required=True)
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    d = docx.Document(a.src)
    p = find(d, "We hold the inventory policy fixed")
    set_text(p, LEAD)
    prev = p
    for text in BULLETS:
        q = clone_after(prev, "•  " + text)
        q.paragraph_format.left_indent = Pt(14)
        q.paragraph_format.first_line_indent = Pt(-10)
        prev = q
    d.save(a.out)
    print("written", a.out)


if __name__ == "__main__":
    main()
