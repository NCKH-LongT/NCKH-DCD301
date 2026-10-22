"""Censoring check for E7-med added to the Censored demand paragraph (rev11 -> rev12; 10 pages).
Numbers (α = 0.01, as in the paper's detector) from code/outputs/censoring/censoring_rank_check_e7.md.

Usage:
    python code/revise_iciit_paper_r12.py --src 08_final_submission/ICIIT2027_Paper_rev11.docx --out 08_final_submission/ICIIT2027_Paper_rev12.docx
"""
import argparse
import os
import sys

import docx

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from revise_iciit_paper_r7 import replace_in  # noqa: E402

OLD = "although it still needs 6.9–10.7% less inventory than LGB-Q on VN1."
NEW = (OLD + " The pre-specified E7-med is less sensitive: its maximum regret is 0.1% on the clean subset and −2.2% under "
       "imputation, where it needs 2.9–5.6% less M5 and 9.5–14.7% less VN1 inventory than LGB-Q at fill rate 0.92.")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--src", required=True)
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    d = docx.Document(a.src)
    replace_in(d, "Censored demand. Both datasets record sales", OLD, NEW)
    d.save(a.out)
    print("written", a.out)


if __name__ == "__main__":
    main()
