"""Reading-order fixes (rev20 -> rev21; 10 pages). No numbers change.

A  Conclusion: one paragraph answers RQ1, the next RQ2 (finding first, evidence after).
B  Abstract: "three statistical and four gradient-boosting approaches" and "bootstrap confidence intervals"; the N-HiTS
   sentence moves out of the abstract (the result stays in Section 5.8) to keep it under 250 words.
C  Introduction opens with the conflict between accuracy rankings and inventory decisions.

Usage:
    python code/revise_iciit_paper_r21.py --src 08_final_submission/ICIIT2027_Paper_rev20.docx --out 08_final_submission/ICIIT2027_Paper_rev21.docx
"""
import argparse
import os
import sys

import docx

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from revise_iciit_paper_r7 import find, replace_in, set_text  # noqa: E402

INTRO = ("Forecasting benchmarks rank models by predictive error, but retailers choose forecasts to support inventory "
         "decisions, and the two rankings need not agree. An order based on the expected value of demand cannot describe "
         "the risk of a stockout: insufficient inventory loses sales, while excess stock incurs holding costs and may later "
         "be liquidated. Forecast quantiles allow an order-up-to level to be set for a chosen service target [3], but "
         "whether they are statistically accurate is a separate question from how much stock their use requires.")

RQ1 = ("For RQ1, rankings by accuracy and by inventory agree on M5 but not on VN1. Under the weekly order-up-to policy "
       "tested here, LGB-Q has the lowest volume-weighted quantile loss on M5 and needs 3–11% less inventory than the "
       "statistical and point-based alternatives at a realised fill rate of 0.94 in all three windows, across the "
       "lead-time checks and four LightGBM configurations. On VN1 no single method leads across periods, and neither "
       "demand classes, clusters nor pre-test warehouse features select one reliably in advance.")

RQ2 = ("For RQ2, the results expose a gap between retrospective inventory efficiency and prospective reliability. At "
       "matched realised fill, a pre-specified median of all seven methods needs 7–8% less VN1 inventory than LGB-Q, and "
       "the post hoc LGB-Q/TSB-NB average 6–11%, while both stay within 1.6% on M5. Neither advantage is confirmed under "
       "past-only τ calibration, full-policy cluster bootstraps or the independent footwear panel, so LGB-Q remains the "
       "dependable default; the conclusions about single methods do not depend on the combinations.")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--src", required=True)
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    d = docx.Document(a.src)

    set_text(find(d, "An order based on the expected value of demand"), INTRO)
    set_text(find(d, "On RQ1: under the weekly order-up-to policy"), RQ1)
    set_text(find(d, "On VN1, by contrast, no single method leads"), RQ2)

    ab = "The forecast with the lowest error is not necessarily"
    replace_in(d, ab, "seven probabilistic methods—three statistical and four gradient-boosting—",
               "seven probabilistic forecasting methods—three statistical and four gradient-boosting approaches—")
    replace_in(d, ab, "with bootstrap intervals.", "with bootstrap confidence intervals.")
    replace_in(d, ab, " The N-HiTS baseline leads no inventory comparison.", "")
    d.save(a.out)
    print("written", a.out, "| abstract words:", len(find(d, ab).text.split()))


if __name__ == "__main__":
    main()
