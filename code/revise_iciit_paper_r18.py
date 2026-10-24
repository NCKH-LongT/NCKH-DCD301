"""Consistency fixes from the full read of rev17 (rev17 -> rev18; 10 pages).

1  Conclusion no longer says there is no independent test period (the footwear panel is one).
2  Censored demand: the threshold × imputation summary moves before the paragraph's closing judgement.
3  Section 5.5 labels the prospective-subset saving as measured at matched realised fill.
4  Related Work mentions the independent third panel.

Usage:
    python code/revise_iciit_paper_r18.py --src 08_final_submission/ICIIT2027_Paper_rev17.docx --out 08_final_submission/ICIIT2027_Paper_rev18.docx
"""
import argparse
import os
import sys

import docx

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from revise_iciit_paper_r7 import find, replace_in, set_text  # noqa: E402

GRID = ("Across detector thresholds of 0.001–0.1 and imputing half the mean, the mean or the mean positive sales, TSB-NB "
        "needs 11.8–34.2% more inventory than LGB-Q on M5, while E7-med needs 1.4–7.2% (M5) and 8.2–15.9% (VN1) less and "
        "keeps a maximum regret of at most 1.6%.")
CLOSE = "Censoring thus matters most for TSB-NB and for the post hoc case for C2 on brick-and-mortar data;"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--src", required=True)
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    d = docx.Document(a.src)

    replace_in(d, "The VN1 results do not identify a single leading method",
               "Without an independent test period these findings are exploratory;",
               "These combination findings are exploratory;")

    p = find(d, "Censored demand. Both datasets record sales")
    t = p.text
    assert GRID in t and CLOSE in t and t.index(GRID) > t.index(CLOSE)
    t = t.replace(" " + GRID, "").replace(CLOSE, GRID + " " + CLOSE)
    set_text(p, t)

    replace_in(d, "At fill rate 0.92, C2 uses 5.9%",
               "The prospective rule saves 7.8–8.2% on VN1 in both transitions but needs 0.9% more on M5 in one.",
               "At matched realised fill, the prospective rule saves 7.8–8.2% on VN1 in both transitions but needs 0.9% more "
               "on M5 in one.")
    replace_in(d, "We retain eligible series across demand classes",
               "use two retail settings and three test windows,",
               "use two retail settings with three test windows plus an independent third panel,")
    d.save(a.out)
    print("written", a.out)


if __name__ == "__main__":
    main()
