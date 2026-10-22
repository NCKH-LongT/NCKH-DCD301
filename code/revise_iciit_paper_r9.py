"""Seven-method combination and ablation (mentor's suggestion) on 08_final_submission/ICIIT2027_Paper_rev8.docx -> rev9
(must stay at 10 pages). Numbers from code/outputs/ensemble/ensemble_ablation.md; design fixed beforehand in
07_paper_draft/phase5_workflow.md, section 7.

Usage:
    python code/revise_iciit_paper_r9.py --src 08_final_submission/ICIIT2027_Paper_rev8.docx --out 08_final_submission/ICIIT2027_Paper_rev9.docx
"""
import argparse
import os
import sys

import docx

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from revise_iciit_paper_r7 import find, replace_in, set_text  # noqa: E402

S55A = ("The complementary VN1 results for LGB-Q and TSB-NB suggest testing their average, C2, the arithmetic mean of the "
        "two methods' quantiles. We chose these two inputs after inspecting their relative performance, so C2 is "
        "exploratory and post hoc. To test combination without that choice, we fixed a second design before running it: "
        "the mean (E7) and the median (E7-med) of all seven methods' quantiles, leave-one-out ablations of E7, and a "
        "prospective rule that applies the lowest-regret mean subset of one window to the next.")

S55B = ("At fill rate 0.92, C2 uses 5.9%, 10.5% and 7.1% less VN1 inventory than LGB-Q in the main, second and third "
        "windows and E7-med 7.6%, 8.2% and 7.1% less, with all bootstrap intervals excluding zero. On M5 both stay within "
        "1.6% of LGB-Q, whereas E7 needs up to 3.1% more and so misses our preset criterion. Every combination has a higher "
        "wQL than LGB-Q. Removing LGB-Q or HGB-Q from E7 raises its stock by 1.0–4.5%, removing ETS lowers it in all six "
        "runs, and the lowest-regret subset of every run contains LGB-Q and TSB-NB. The prospective rule saves 7.8–8.2% on "
        "VN1 in both transitions but needs 0.9% more on M5 in one. C2 also saves VN1 inventory at one- and four-week lead "
        "times (Section 5.8).")

REGRET = ("Among the combinations, E7-med has the smallest maximum regret under the paper's descriptive metric (excess "
          "stock relative to the best single method, averaged over attainable fill-rate targets in each dataset–window "
          "run): 0.3% across six runs, versus 0.9% for the post hoc C2, 3.4% for E7, 9.4% for LGB-Q, 9.5% for LGB-T, 11.4% "
          "for HGB-Q and 20.7% for TSB-NB. LGB-T does not reach the highest target levels. When a lost sale costs at most "
          "200 weeks of holding, C2's cost is within 3.1% of the cheapest single model in each run. At higher penalties the "
          "methods operate at τ = 0.99; LGB-Q then has the highest fill rate, and C2 can cost as much as 29% more. These "
          "figures describe the six evaluated runs, not expected deployment performance.")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--src", required=True)
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    d = docx.Document(a.src)

    set_text(find(d, "The complementary VN1 results for LGB-Q and TSB-NB"), S55A)
    set_text(find(d, "At fill rate 0.92, C2 uses 5.9%"), S55B)
    set_text(find(d, "The post hoc C2 has the smallest maximum regret"), REGRET)
    replace_in(d, "Toward deployment of C2.", "Toward deployment of C2. Because C2 is post hoc, its next evaluation",
               "Toward deployment. Because C2 is post hoc and E7-med was tested on only three windows per dataset, the "
               "next evaluation")
    replace_in(d, "Toward deployment.", "freeze its specification", "freeze the specification")

    replace_in(d, "The forecast with the lowest error is not necessarily",
               "Averaging the LGB-Q and TSB-NB quantiles reduces VN1 inventory by 6–11% relative to LGB-Q at a fill rate of "
               "0.92 and remains within 1.5% on M5. This combination was selected after inspection of the results and has "
               "not been independently validated, so our main evidence concerns the single methods.",
               "Averaging the LGB-Q and TSB-NB quantiles, a post hoc choice, reduces VN1 inventory by 6–11% relative to "
               "LGB-Q at a fill rate of 0.92 and remains within 1.5% on M5; a median of all seven methods, specified before "
               "testing, saves 7–8% on VN1 and stays within 1.6% on M5. Because these combinations lack an independent test "
               "period, our main evidence concerns the single methods.")
    replace_in(d, "We hold the inventory policy fixed",
               "Finally, we report an exploratory average of two forecast distributions. Its constituent methods were "
               "selected after seeing the initial results, so the combination is not an independently validated policy.",
               "Finally, we report an exploratory average of two forecast distributions, chosen after seeing the initial "
               "results, and a pre-specified combination and ablation of all seven methods.")
    replace_in(d, "The VN1 results do not identify a single leading method",
               "An equal-weight LGB-Q/TSB-NB quantile average reduces inventory by 6–11% relative to LGB-Q on VN1 at fill "
               "rate 0.92 and stays within 1.5% on M5. Because that pair was chosen after inspection of the results, this "
               "finding is exploratory and needs an independent evaluation; the conclusions about single methods above do "
               "not depend on it.",
               "An equal-weight LGB-Q/TSB-NB quantile average reduces inventory by 6–11% relative to LGB-Q on VN1 at fill "
               "rate 0.92 and stays within 1.5% on M5; a pre-specified median of all seven methods saves 7–8% on VN1 with "
               "the lowest maximum regret, but no combination clearly beats LGB-Q on M5. Without an independent test period "
               "these findings are exploratory; the conclusions about single methods above do not depend on them.")
    d.save(a.out)
    print("written", a.out)


if __name__ == "__main__":
    main()
