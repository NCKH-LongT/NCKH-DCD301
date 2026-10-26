"""Calibrated wording about the combinations (rev21 -> rev22; 10 pages). No numbers change.

A  Conclusion: the retrospective advantages do not generalise consistently; C2 keeps one significant prospective
   VN1 saving (Table 7: −7.4%, CI −15.3% to −1.9%, fills 0.907 vs 0.908); LGB-Q is the more defensible reference.
B  Abstract: on the footwear panel neither combination shows a statistically significant advantage over LGB-Q
   (instead of "LGB-Q again needs the least stock").
C  Contributions: achieved fill is reported beside the prospective comparisons (Table 3 uses matched fill).
Also: contribution 2 "disappears" -> "is not confirmed"; deployment paragraph "passed the prospective checks" ->
"showed a reliable advantage in" (the pre-set criterion applied to E7-med only).

Usage:
    python code/revise_iciit_paper_r22.py --src 08_final_submission/ICIIT2027_Paper_rev21.docx --out 08_final_submission/ICIIT2027_Paper_rev22.docx
"""
import argparse
import os
import sys

import docx

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from revise_iciit_paper_r7 import find, replace_in  # noqa: E402

CONCL = ("These retrospective advantages do not generalise consistently under past-only service calibration, full-policy "
         "cluster bootstrapping and independent footwear validation. Although C2 retains a significant inventory "
         "advantage in one prospective VN1 comparison, neither combination demonstrates a reliable benefit across "
         "settings. LGB-Q therefore remains the more defensible reference method under the tested policy.")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--src", required=True)
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    d = docx.Document(a.src)

    replace_in(d, "For RQ2, the results expose a gap",
               "Neither advantage is confirmed under past-only τ calibration, full-policy cluster bootstraps or the "
               "independent footwear panel, so LGB-Q remains the dependable default; the conclusions about single methods "
               "do not depend on the combinations.", CONCL)

    ab = "The forecast with the lowest error is not necessarily"
    replace_in(d, ab, "is not confirmed on an independent footwear dataset, where LGB-Q again needs the least stock.",
               "is not confirmed on an independent footwear dataset, where neither combination demonstrates a "
               "statistically significant inventory advantage over LGB-Q.")

    replace_in(d, "•  Retrospective savings are not prospective evidence",
               "achieved fill is reported beside every inventory comparison.",
               "prospective inventory comparisons report achieved fill alongside stock requirements.")
    replace_in(d, "•  Retrospective savings are not prospective evidence",
               "at matched realised fill disappears under", "at matched realised fill is not confirmed under")
    replace_in(d, "Toward deployment.", "Because neither combination passed the prospective checks of Section 5.8,",
               "Because neither combination showed a reliable advantage in Section 5.8,")
    replace_in(d, "Censored demand. Both datasets record sales",
               "Censoring thus matters most for TSB-NB and for the post hoc case for C2 on brick-and-mortar data; "
               "stock-availability records would be needed to settle it.",
               "Stock-availability records would be needed to settle these effects.")
    replace_in(d, "Limitations. Recorded sales stand in for demand",
               " Findings may differ for other retailers or inventory policies.", "")
    d.save(a.out)
    print("written", a.out, "| abstract words:", len(find(d, ab).text.split()))


if __name__ == "__main__":
    main()
