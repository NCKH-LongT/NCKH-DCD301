"""Three fixes from the self-review of rev10 (08_final_submission/ICIIT2027_Paper_rev10.docx -> rev11; 10 pages).

1  Section 3.1 cited Section 5.7 for the AUC of 0.91, which 5.7 does not report (code/outputs/dataset_shift.md does).
2  The last sentence of Related Work now matches the contribution list (it omitted the combination).
3  The first contribution names the alternatives LGB-Q beats by 3–11% (HGB-Q is within 0.2–1.4%).

Usage:
    python code/revise_iciit_paper_r11.py --src 08_final_submission/ICIIT2027_Paper_rev10.docx --out 08_final_submission/ICIIT2027_Paper_rev11.docx
"""
import argparse
import os
import sys

import docx

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from revise_iciit_paper_r7 import replace_in  # noqa: E402


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--src", required=True)
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    d = docx.Document(a.src)
    replace_in(d, "A single processing pipeline handles both panels.",
               "identifies the dataset with an AUC of 0.91 (Section 5.7).",
               "identifies the dataset with an AUC of 0.91 (repository); Section 5.7 tests whether such differences "
               "explain the results.")
    replace_in(d, "We retain eligible series across demand classes",
               "the contribution here is the comparison across datasets, periods and decision settings.",
               "our contributions are the comparison across datasets, periods and decision settings and a pre-specified "
               "combination of the compared methods.")
    replace_in(d, "•  Evidence across settings and periods.",
               "LGB-Q needs 3–11% less stock than the alternatives in every window,",
               "LGB-Q needs 3–11% less stock than the point-forecast, conformal, TSB-NB and exponential-smoothing "
               "alternatives in every window,")
    d.save(a.out)
    print("written", a.out)


if __name__ == "__main__":
    main()
