"""P0–P1 robustness results (design: phase5_workflow.md, section 8) in rev13 -> rev14 (must stay at 10 pages).
Numbers from code/outputs/robustness/prospective_tau.md, robustness/bootstrap_robust.md and
censoring/censoring_sensitivity.md. The VN1 interval claims are qualified because warehouse- and client-level
resampling widens them.

Usage:
    python code/revise_iciit_paper_r14.py --src 08_final_submission/ICIIT2027_Paper_rev13.docx --out 08_final_submission/ICIIT2027_Paper_rev14.docx
"""
import argparse
import os
import sys

import docx

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from revise_iciit_paper_r7 import clone_after, find, replace_in  # noqa: E402

ROBUST = ("Prospective τ and resampling. Choosing each method's τ on the previous window and applying it unchanged to the "
          "next puts every method except EMP within 0.8 points of the target fill on M5; LGB-Q, HGB-Q, C2 and E7-med then "
          "need inventory within 2% of one another, and LGB-T, LGB-C, TSB-NB and ETS 3.8–14.2% more. On VN1 the realised "
          "fill misses the target by 0.7–2.4 points for LGB-Q and HGB-Q and by 2.4–5.9 points for the other methods, so the "
          "combinations overshoot with 15–35% more stock in one transition and undershoot with 18–27% less in the other. "
          "Resampling items, stores or blocks of weeks leaves every M5 interval claim intact. On VN1, resampling warehouses "
          "or clients widens the intervals, and only the second-window savings of C2 (and of E7-med for warehouses) remain "
          "significant.")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--src", required=True)
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    d = docx.Document(a.src)

    # new robustness paragraph after computational cost (Section 5.8)
    clone_after(find(d, "Computational cost. All methods except Chronos-2"), ROBUST)

    # Section 5.5: qualify the interval claim
    replace_in(d, "At fill rate 0.92, C2 uses 5.9%", "with all bootstrap intervals excluding zero.",
               "with all series-bootstrap intervals excluding zero (but see Section 5.8).")

    # censoring: sensitivity grid; shorter closing sentence
    replace_in(d, "Censored demand. Both datasets record sales",
               "Because the flags are uncertain, such models would need on-hand records or a sensitivity analysis over the "
               "flagging threshold; we leave them to future work.",
               "We leave such models to future work. Across detector thresholds of 0.001–0.1 and imputing half the mean, the "
               "mean or the mean positive sales, TSB-NB needs 11.8–34.2% more inventory than LGB-Q on M5, while E7-med needs "
               "1.4–7.2% (M5) and 8.2–15.9% (VN1) less and keeps a maximum regret of at most 1.6%.")

    # abstract, contribution, conclusion, limitations
    replace_in(d, "The forecast with the lowest error is not necessarily",
               "Without an independent test period, these combinations remain exploratory.",
               "These VN1 savings lose significance when warehouses are resampled, and without an independent test period "
               "the combinations remain exploratory.")
    replace_in(d, "•  A pre-specified combination with ablation.",
               "but gives no gain on M5;",
               "but gives no gain on M5 and its VN1 saving is not robust to warehouse-level resampling;")
    replace_in(d, "The VN1 results do not identify a single leading method",
               "but no combination clearly beats LGB-Q on M5.",
               "but no combination clearly beats LGB-Q on M5, and warehouse-level resampling leaves only the second-window "
               "savings significant.")
    replace_in(d, "Limitations. Recorded sales stand in for demand",
               "Bootstrap intervals resample series rather than time periods, and each dataset supplies only three "
               "evaluation windows.",
               "Series-level intervals are too narrow on VN1, where warehouse- and client-level resampling widens them "
               "(Section 5.8), and each dataset supplies only three evaluation windows.")
    d.save(a.out)
    print("written", a.out)


if __name__ == "__main__":
    main()
