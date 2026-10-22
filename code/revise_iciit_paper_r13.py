"""Three fixes from the review of rev12 (rev12 -> rev13; 10 pages).

1  Table 1 and Figure 1 are now cited in the text.
2  The seven-method combinations (E7, E7-med) are introduced in Section 3.2, next to C2.
3  Abstract shortened from 269 to under 250 words; numbers unchanged.

Usage:
    python code/revise_iciit_paper_r13.py --src 08_final_submission/ICIIT2027_Paper_rev12.docx --out 08_final_submission/ICIIT2027_Paper_rev13.docx
"""
import argparse
import os
import sys

import docx

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from revise_iciit_paper_r7 import find, replace_in, set_text  # noqa: E402

ABSTRACT = (
    "The forecast with the lowest error is not necessarily the forecast that supports the lowest inventory. We test this "
    "using seven probabilistic methods—three statistical approaches and four gradient-boosting variants—in a weekly "
    "order-up-to simulation with optional liquidation, on all eligible series from M5 (physical stores) and VN1 "
    "(multi-vendor e-commerce) over three 26-week windows per dataset. Because inventory costs are unobserved, we compare "
    "stock requirements at equal realised fill rates with bootstrap confidence intervals. On M5, LightGBM quantile "
    "regression (LGB-Q) has the lowest volume-weighted quantile loss and, at a fill rate of 0.94, needs 3–11% less "
    "inventory than the safety-stock, conformal, TSB-NB and exponential-smoothing alternatives in each window; this holds "
    "across the tested lead times and LightGBM settings. VN1 ranks the methods differently in different windows: TSB-NB "
    "needs 13–16% less inventory for stable-demand series but fails to reach a fill rate of 0.92 on growing-demand series "
    "in two windows, and neither ADI–CV² classes nor clusters consistently identify the right method in advance. A median "
    "of all seven methods' quantiles, specified before testing, needs 7–8% less VN1 inventory than LGB-Q at a fill rate of "
    "0.92 and stays within 1.6% on M5; a post hoc average of LGB-Q and TSB-NB saves 6–11%. Without an independent test "
    "period, these combinations remain exploratory. The N-HiTS baseline leads no inventory comparison. Quantile-based "
    "liquidation changes fill rate by at most 0.02 percentage points but shows no consistent economic advantage over 26 "
    "weeks under the assumed costs.")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--src", required=True)
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    d = docx.Document(a.src)

    # 1 – cite Table 1 and Figure 1
    replace_in(d, "A single processing pipeline handles both panels.",
               "Their demand characteristics are nonetheless distinct:",
               "Their demand characteristics are nonetheless distinct (Table 1):")
    replace_in(d, "M5. LGB-Q ranks first on the inventory frontier",
               "M5. LGB-Q ranks first on the inventory frontier in all",
               "M5. LGB-Q ranks first on the inventory frontier (Figure 1) in all")

    # 2 – introduce E7 and E7-med in Section 3.2
    replace_in(d, "An additional combination, C2, specified post hoc",
               "averages the corresponding LGB-Q and TSB-NB quantiles (Section 5.5).",
               "averages the corresponding LGB-Q and TSB-NB quantiles (Section 5.5). That section also evaluates two "
               "combinations of all seven methods fixed before they were run: the mean (E7) and the median (E7-med) of "
               "their quantiles.")

    # 3 – shorter abstract
    p = find(d, "The forecast with the lowest error is not necessarily")
    set_text(p, ABSTRACT)
    print("abstract words:", len(ABSTRACT.split()))
    d.save(a.out)
    print("written", a.out)


if __name__ == "__main__":
    main()
