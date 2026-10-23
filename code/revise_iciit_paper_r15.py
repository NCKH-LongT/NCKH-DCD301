"""Past-only τ calibration and independent VNF validation (design: phase5_workflow.md, section 9) in rev14 -> rev15
(must stay at 10 pages). Neither pre-set criterion was met, so the combination claims are reduced as the design
prescribes. Numbers from code/outputs/robustness/rolling_calibration.md and vnf_validation.md.

Usage:
    python code/revise_iciit_paper_r15.py --src 08_final_submission/ICIIT2027_Paper_rev14.docx --out 08_final_submission/ICIIT2027_Paper_rev15.docx
"""
import argparse
import os
import sys

import docx

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from revise_iciit_paper_r7 import find, replace_in, set_text  # noqa: E402

ROBUST = ("Prospective τ, resampling and a third dataset. Choosing each method's τ on the previous window puts every method "
          "except EMP within 0.8 points of the target fill on M5, where LGB-Q, HGB-Q, C2 and E7-med then need inventory "
          "within 2% of one another and LGB-T, LGB-C, TSB-NB and ETS 3.8–14.2% more. On VN1 the realised fill misses the "
          "target by up to 4.6 points for these four methods; updating τ every week by half the gap between the target and "
          "the fill realised so far reduces the miss to 2.4 points, still above our one-point criterion. With service matched "
          "this way, E7-med never needs less VN1 stock than LGB-Q at comparable fill with a warehouse-level interval "
          "excluding zero, C2 does so once, and TSB-NB needs 28–42% more in three of four cases. Resampling items, stores or "
          "blocks of weeks leaves every M5 interval claim intact, whereas warehouse- or client-level resampling leaves only "
          "the second-window VN1 savings significant. On an independent panel not used to design either combination (909 "
          "style–colour series of a Vietnamese footwear chain, one 26-week window), LGB-Q needs the least inventory at equal "
          "fill; E7-med needs 2.4% more at fill 0.92 (style-level interval −1.0% to +5.8%) and C2 0.3% more.")

ADAPT = ("Adaptive updating. Parameters are re-estimated only every 13 weeks with fixed hyperparameters, which can leave the "
         "global models a block behind level shifts on fast-growing VN1 series. More frequent or warm-started refits, "
         "recency weighting or re-tuning could reduce that lag but were not tested.")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--src", required=True)
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    d = docx.Document(a.src)

    set_text(find(d, "Prospective τ and resampling."), ROBUST)
    set_text(find(d, "Adaptive updating."), ADAPT)

    replace_in(d, "The forecast with the lowest error is not necessarily",
               "A median of all seven methods' quantiles, specified before testing, needs 7–8% less VN1 inventory than LGB-Q "
               "at a fill rate of 0.92 and stays within 1.6% on M5; a post hoc average of LGB-Q and TSB-NB saves 6–11%. "
               "These VN1 savings lose significance when warehouses are resampled, and without an independent test period "
               "the combinations remain exploratory.",
               "A median of all seven methods' quantiles, specified before testing, needs 7–8% less VN1 inventory than LGB-Q "
               "at a fill rate of 0.92, but the saving loses significance when warehouses are resampled, does not persist "
               "when τ is calibrated from past weeks only, and is not confirmed on an independent footwear dataset, where "
               "LGB-Q again needs the least stock.")
    set_text(find(d, "•  A pre-specified combination with ablation."),
             "•  A pre-specified combination tested prospectively. The median of the seven methods' quantiles needs 7–8% "
             "less VN1 inventory than LGB-Q at equal realised fill, and the ablation shows that the direct quantile learners "
             "contribute most, but the saving does not survive warehouse-level resampling, past-only τ calibration or an "
             "independent third dataset. An earlier average of two methods (C2) is reported as post hoc.")
    replace_in(d, "The VN1 results do not identify a single leading method",
               "a pre-specified median of all seven methods saves 7–8% on VN1 with the lowest maximum regret, but no "
               "combination clearly beats LGB-Q on M5, and warehouse-level resampling leaves only the second-window savings "
               "significant.",
               "a pre-specified median of all seven methods saves 7–8% on VN1 with the lowest maximum regret, but the saving "
               "does not survive warehouse-level resampling, past-only τ calibration or an independent footwear dataset, so "
               "LGB-Q remains the dependable default.")
    replace_in(d, "Toward deployment.",
               "Because C2 is post hoc and E7-med was tested on only three windows per dataset, the next evaluation should "
               "be prospective:",
               "Because C2 is post hoc and E7-med did not pass the prospective checks of Section 5.8, any further evaluation "
               "should also be prospective:")
    d.save(a.out)
    print("written", a.out, "| abstract words:", len(find(d, "The forecast with the lowest error").text.split()))


if __name__ == "__main__":
    main()
