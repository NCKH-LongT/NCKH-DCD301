"""Small clarity fixes from the review of rev19 (rev19 -> rev20; 10 pages).

1  Conclusion answers RQ1 and RQ2 explicitly.
2  Abstract: the stable-demand result is marked as retrospective (groups use test-window demand).
3  Section 5.8: the warehouse/client resampling sentence refers to the matched-fill comparisons, not Table 7.

Usage:
    python code/revise_iciit_paper_r20.py --src 08_final_submission/ICIIT2027_Paper_rev19.docx --out 08_final_submission/ICIIT2027_Paper_rev20.docx
"""
import argparse
import os
import sys

import docx

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from revise_iciit_paper_r7 import find, replace_in  # noqa: E402


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--src", required=True)
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    d = docx.Document(a.src)

    replace_in(d, "Under the weekly order-up-to policy tested here",
               "Under the weekly order-up-to policy tested here, LGB-Q",
               "On RQ1: under the weekly order-up-to policy tested here, LGB-Q")
    replace_in(d, "The VN1 results do not identify a single leading method",
               "The VN1 results do not identify a single leading method across periods.",
               "On VN1, by contrast, no single method leads across periods.")
    replace_in(d, "On VN1, by contrast, no single method leads across periods.",
               "a pre-specified median of all seven methods saves 7–8% on VN1",
               "on RQ2, a pre-specified median of all seven methods saves 7–8% on VN1")

    replace_in(d, "The forecast with the lowest error is not necessarily",
               "TSB-NB needs 13–16% less inventory for stable-demand series",
               "TSB-NB needs 13–16% less inventory for series that turn out to be stable")

    for old, new in (("three statistical approaches and four gradient-boosting variants", "three statistical and four gradient-boosting"),
                     ("we compare stock requirements at equal realised fill rates with bootstrap confidence intervals.",
                      "we compare stock at equal realised fill rates with bootstrap intervals."),
                     ("this holds across the tested lead times", "this holds across tested lead times")):
        replace_in(d, "The forecast with the lowest error is not necessarily", old, new)

    replace_in(d, "Prospective τ, resampling and a third dataset.",
               "whereas warehouse- or client-level resampling leaves only the second-window VN1 savings significant.",
               "whereas for the matched-fill comparisons warehouse- or client-level resampling leaves only the "
               "second-window VN1 savings significant.")
    d.save(a.out)
    print("written", a.out, "| abstract words:", len(find(d, "The forecast with the lowest error").text.split()))


if __name__ == "__main__":
    main()
