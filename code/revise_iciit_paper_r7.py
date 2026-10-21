"""Third review round (21/10/2026) on 08_final_submission/ICIIT2027_Paper_rev6.docx -> rev7 (must stay at 10 pages).

R1  C2 flagged as post hoc wherever it is summarised.
R2  Censored demand: results of censoring_check.py (teammate) and censoring_rank_check.py.
R3  Computational cost vs inventory efficiency (teammate's 06_experiment_results/phase4_compute_cost.md, checked
    against the logs).
R4  How to use s* in practice.
Plus one sentence on the two-stage LightGBM study (Nabil et al. 2026) and compensating cuts.

Usage:
    python code/revise_iciit_paper_r7.py --src 08_final_submission/ICIIT2027_Paper_rev6.docx --out 08_final_submission/ICIIT2027_Paper_rev7.docx
"""
import argparse
import copy

import docx


def find(doc, start):
    hits = [p for p in doc.paragraphs if p.text.strip().startswith(start)]
    assert len(hits) == 1, f"{len(hits)} paragraphs start with {start!r}"
    return hits[0]


def set_text(p, text):
    p.runs[0].text = text
    for r in p.runs[1:]:
        r._r.getparent().remove(r._r)


def replace_in(doc, start, old, new):
    p = find(doc, start)
    assert old in p.text, (start, old[:50])
    set_text(p, p.text.replace(old, new))


def clone_after(p, text):
    el = copy.deepcopy(p._p)
    p._p.addnext(el)
    q = docx.text.paragraph.Paragraph(el, p._parent)
    set_text(q, text)
    return q


CENSOR = ("Censored demand. Both datasets record sales, not demand, and contain no on-hand records. A sales-only detector "
          "that flags zero runs between two sales whose probability under the series' sale frequency p is below 1% "
          "((1 − p)^k < 0.01) marks 7.4–9.0% of M5 and 6.1–6.9% of VN1 test weeks as suspected stockouts, about twice as "
          "often in intermittent and lumpy as in smooth series; because genuine pauses in demand are also flagged, these "
          "are upper bounds. Restricting the evaluation to the 72–82% of series without flagged weeks leaves the leading "
          "method of every window and C2's lowest maximum regret unchanged. A stricter scenario imputes each series' mean "
          "weekly sales in every flagged week. TSB-NB, whose occurrence probability falls during zero runs, then needs "
          "17–27% more inventory than LGB-Q on M5 at fill rate 0.92; the leading method changes in three of six windows, "
          "always to a closely ranked method; and C2's maximum regret rises to 9.8%, although it still needs 6.9–10.7% less "
          "inventory than LGB-Q on VN1. Censoring thus matters most for TSB-NB and for the post hoc case for C2 on "
          "brick-and-mortar data; stock-availability records would be needed to settle it.")

COST = ("Computational cost. All methods except Chronos-2 forecast one 26-week window in minutes on the laptop CPU: about "
        "1–2 minutes for TSB-NB, 10–21 minutes for LGB-Q on M5 (five quantile models per refit) and about 7 minutes for "
        "N-HiTS. Zero-shot Chronos-2 [22] needs no training, but its CPU inference took 5.4 hours per M5 window and 32–45 "
        "minutes per VN1 window, while needing 14.7% more inventory than LGB-Q on M5 and 1.2–48.1% more on VN1 at fill rate "
        "0.92. For weekly review, computation does not constrain the statistical and boosting methods, and the costlier "
        "zero-shot model did not buy inventory efficiency here; it ran without fine-tuning or covariates.")

SSTAR_USE = (" In practice the rule is direct: liquidate only if the expected recovery ratio r on the secondary market "
             "(salvage price divided by unit cost) exceeds s*. With the VN1 quantile-rule thresholds of 0.91–1.21, a channel "
             "that recovers 60% of cost would not justify liquidation within 26 weeks, whereas one that recovers about unit "
             "cost could. Obsolescence, scarce storage space or a longer horizon would lower s* and are not modelled here.")

ADAPT = ("Adaptive updating. The global models use the newest lags every week, but their parameters are re-estimated only "
         "every 13 weeks with fixed hyper-parameters, which can leave them one block behind a level shift on fast-growing "
         "VN1 series. More frequent or warm-started refits, heavier weights on recent observations, or re-tuning at each "
         "refit could reduce that lag; the VN1 sensitivity to tree size (Section 5.8) suggests configuration matters. We "
         "did not test these options, and neither the growth classifier nor learned combination weights (repository) "
         "beat simpler fixed choices, so added adaptivity needs out-of-sample validation.")

DEPLOY = ("Toward deployment of C2. Because C2 is post hoc, its next evaluation should be prospective: freeze its "
          "specification (members, equal weights, quantile grid, policy and metrics), apply it unchanged to later periods "
          "and to other retail datasets, and, in a company, run it in shadow mode beside the current method for several "
          "review cycles before any switch. Two guardrails follow from our results: use LGB-Q when lost sales cost more "
          "than about 200 weeks of holding, and monitor upper-quantile coverage, where TSB-NB under-covers.")

HPARAM = ("Hyperparameters. For h = 3 in the main window, we refitted LGB-Q and LGB-T with small (15 leaves), large (255 "
          "leaves) and regularised (31 leaves, minimum 500 samples per leaf, L2 penalty 10) trees. On M5, LGB-Q needs "
          "4.7–6.8% less inventory than LGB-T and 7.5–11.0% less than TSB-NB at fill rate 0.92 under all four "
          "configurations, and its own inventory changes by less than 3%. The VN1 ranking persists for three settings; with "
          "small trees, LGB-Q's advantage over TSB-NB is no longer resolved and LGB-T uses 8.9% less inventory than LGB-Q.")

NABIL = (" Nabil et al. [27] forecast spare-part demand with a two-stage LightGBM/XGBoost model (an occurrence classifier "
         "times a size regressor) and set stock with a normal safety factor; a quantile version of this design is not "
         "tested here.")
REF27 = ("[27]  O. M. Nabil, N. H. Afia, and T. Ismail. 2026. Intermittent demand forecasting for spare parts using "
         "classification/regression models of machine learning and deep learning. Ain Shams Engineering Journal 17, "
         "104445. https://doi.org/10.1016/j.asej.2026.104445")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--src", required=True)
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    d = docx.Document(a.src)

    # R1 – post hoc wherever C2 is summarised
    replace_in(d, "Lead time. We repeated the equal-fill comparisons", "For VN1, C2 uses", "For VN1, the post hoc C2 uses")
    replace_in(d, "Neural baseline. We evaluated", "Including N-HiTS leaves C2's maximum regret at 0.9%.",
               "Including N-HiTS leaves the post hoc C2's maximum regret at 0.9%.")
    replace_in(d, "C2 has the smallest maximum regret", "C2 has the smallest maximum regret", "The post hoc C2 has the smallest maximum regret")
    replace_in(d, "An additional combination, C2, averages", "An additional combination, C2, averages",
               "An additional combination, C2, specified post hoc after inspecting the results, averages")

    # R2 – censoring
    set_text(find(d, "Censored demand. Both datasets record sales"), CENSOR)
    replace_in(d, "Limitations. Recorded sales stand in for demand", "Recorded sales stand in for demand (see above).",
               "Recorded sales stand in for demand, and stockouts are only inferred (see above).")

    # R3 – computational cost, after the neural baseline
    clone_after(find(d, "Neural baseline. We evaluated"), COST)

    # R4 – using s*
    p = find(d, "None of the policies has a consistent economic advantage")
    set_text(p, p.text + SSTAR_USE)

    # two-stage LightGBM reference (cited last, in Limitations, so reference order follows first citation)
    replace_in(d, "Limitations. Recorded sales stand in for demand",
               "Chronos-2 [22] is evaluated separately in the repository;", "Chronos-2 [22] was run zero-shot only;")
    p = find(d, "Limitations. Recorded sales stand in for demand")
    set_text(p, p.text + NABIL)
    clone_after(find(d, "[26]  C. Challu"), REF27)

    # compensating cuts
    set_text(find(d, "Adaptive updating. Between refits"), ADAPT)
    set_text(find(d, "Toward deployment of C2."), DEPLOY)
    set_text(find(d, "Hyperparameters. For h = 3 in the main window"), HPARAM)
    replace_in(d, "Nemenyi critical difference (α = 0.05)",
               " Mean series-level ranks at h = 13: M5—LGB-Q 3.45 / 3.43 / 3.50, HGB-Q 3.38 / 3.45 / 3.50, TSB-NB 4.16 / 4.04 / 4.05; VN1—LGB-Q 4.02 / 3.48 / 3.85, HGB-Q 3.85 / 3.46 / 3.57, TSB-NB 2.92 / 2.99 / 3.37.",
               " At h = 13, TSB-NB has the best mean VN1 rank in every window (2.92 / 2.99 / 3.37).")
    replace_in(d, "Neural baseline. We evaluated",
               " Its wQL lies between LGB-Q and TSB-NB in all six runs (M5: 0.078 / 0.083 / 0.089; VN1: 0.107 / 0.079 / 0.104); empirical coverage of the 0.99-quantile is 0.986–0.992.",
               " Its wQL lies between LGB-Q and TSB-NB in all six runs, and its 0.99-quantile coverage is 0.986–0.992.")
    replace_in(d, "We next ask whether information available before a window",
               " Among K-means and mixture candidates, predefined criteria select a three-component Gaussian mixture labelled regular, fading and sparse. Refits are similar (adjusted Rand index 0.94), but the clusters overlap substantially (silhouette 0.21).",
               " Predefined criteria select a three-component Gaussian mixture (regular, fading, sparse) that is stable across refits (adjusted Rand index 0.94) but overlapping (silhouette 0.21).")
    d.save(a.out)
    print("written", a.out)


if __name__ == "__main__":
    main()
