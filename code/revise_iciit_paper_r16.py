"""rev15 -> rev16 (must stay at 10 pages).

P0  Method description of the independent footwear panel (provenance, preprocessing, train/test, independence,
    reproducibility limits) in Section 3.1; facts from f2d/data.py:load_vnf and the loaded panel.
P1  Contributions rewritten around ranking instability and the gap between retrospective inventory efficiency and
    prospective reliability; the combination is no longer presented as a successful solution.
P1  New Table 7: target fill, achieved fill, inventory and cluster-bootstrap intervals together under the past-only
    τ rule (η = 0.5, target 0.92), read from code/outputs/robustness/rolling_calibration.csv.
Compensating cuts in Sections 5.8 and 6 keep the paper at 10 pages.

Usage:
    python code/revise_iciit_paper_r16.py --src 08_final_submission/ICIIT2027_Paper_rev15.docx --out 08_final_submission/ICIIT2027_Paper_rev16.docx
"""
import argparse
import copy
import os
import sys

import docx
import pandas as pd
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.shared import Inches, Pt
from docx.text.paragraph import Paragraph

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from revise_iciit_paper_r7 import clone_after, find, replace_in, set_text  # noqa: E402

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

VNF = ("Independent panel. To check the combinations on data not used to specify them, we add the retail-channel sales of "
       "a Vietnamese footwear chain, public on Kaggle (tienanh2003/sales-and-inventory-snapshot-data). Units sold are "
       "aggregated to 1,001 style–colour series for the whole chain over 82 weeks (January 2022 to July 2023); returns are "
       "excluded, and three partial year-boundary or end weeks are dropped or merged. With the eligibility rule above, 909 "
       "series enter one 26-week test window starting 30 January 2023; 31.7% of their pre-test weeks have no sales. "
       "Forecasts use the same pipeline, 21 features, refit schedule and policy. The short history allows only one window, "
       "the chain's month-end stock snapshots are not used, and single-method results on this panel existed before, but "
       "were not used for, specifying the combinations.")

ROBUST = ("Prospective τ, resampling and a third dataset. Choosing each method's τ on the previous window puts every method "
          "except EMP within 0.8 points of the target fill on M5, where LGB-T, LGB-C, TSB-NB and ETS then need 3.8–14.2% "
          "more inventory than LGB-Q. On VN1 the realised fill misses the target by up to 4.6 points for LGB-Q, HGB-Q, C2 "
          "and E7-med; updating τ every week by half the gap between the target and the fill realised so far reduces the "
          "miss to 2.4 points, above our one-point criterion. Table 7 reports achieved fill and inventory together under "
          "this past-only rule; we read an inventory difference as a saving only where fills differ by less than 0.5 "
          "points. In that sense E7-med never needs significantly less stock than LGB-Q on VN1 or on the footwear panel, "
          "and C2 does so once. Resampling items, stores or blocks of weeks leaves every M5 interval claim intact, whereas "
          "warehouse- or client-level resampling leaves only the second-window VN1 savings significant.")

CAPTION = ("Table 7. Past-only service calibration at target fill 0.92 (τ updated weekly, η = 0.5). Fill = achieved fill "
           "rate; ΔI = inventory relative to LGB-Q (%) with 95% cluster-bootstrap intervals (M5 items, VN1 warehouses, "
           "footwear styles). LGB-Q rows give inventory in weeks of demand. ΔI is a saving only where fills are close.")

BULLETS = [
    "•  Ranking instability across settings and periods. Accuracy and inventory rankings agree on M5, where LGB-Q needs "
    "3–11% less stock than the point-forecast, conformal, TSB-NB and exponential-smoothing alternatives in every window, "
    "but not on VN1, where the leading method changes between windows.",
    "•  Limits of prospective method selection. Pre-test demand classes, clusters and the previous window's leader do not "
    "reliably identify the best method, and reweighting VN1 to M5's feature distribution leaves the VN1 findings unchanged.",
    "•  Retrospective efficiency versus prospective reliability. Savings measured at matched realised fill need not "
    "survive deployment-style evaluation: with service calibrated from past weeks only, warehouse-level resampling and "
    "an independent footwear panel, the 7–8% VN1 saving of a pre-specified seven-method median disappears, whereas the "
    "M5 ranking holds. With τ chosen on the previous window, the direct quantile learners stay closest to the target fill.",
]

COLS = [("M5", "third → second", "M5 3→2"), ("M5", "second → main", "M5 2→main"), ("VN1", "third → second", "VN1 3→2"),
        ("VN1", "second → main", "VN1 2→main"), ("VNF", "main (τ0 = target)", "Footwear")]
ROWS = ["LGB-Q", "HGB-Q", "TSB-NB", "C2", "E7-med"]


def build_table(d, anchor_p, cap_proto, tbl_proto):
    r = pd.read_csv(os.path.join(ROOT, "code", "outputs", "robustness", "rolling_calibration.csv"))
    r = r[(r.eta == 0.5) & (r.target == 0.92)]
    cap = clone_after(anchor_p, CAPTION)
    cap.style = cap_proto.style
    t = d.add_table(rows=2 + len(ROWS), cols=1 + 2 * len(COLS))
    t._tbl.remove(t._tbl.tblPr)
    t._tbl.insert(0, copy.deepcopy(tbl_proto._tbl.tblPr))
    t.alignment = WD_TABLE_ALIGNMENT.CENTER

    def put(cell, text, bold=False):
        p = cell.paragraphs[0]
        p.style = d.styles["CellText"]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        for k, line in enumerate(text.split("\n")):
            run = p.add_run(line)
            run.font.size = Pt(7)
            run.bold = bold
            if k < len(text.split("\n")) - 1:
                run.add_break()

    put(t.cell(0, 0), "Method", True)
    t.cell(0, 0).merge(t.cell(1, 0))
    for j, (_, _, lab) in enumerate(COLS):
        a, b = t.cell(0, 1 + 2 * j), t.cell(0, 2 + 2 * j)
        put(a, lab, True)
        a.merge(b)
        put(t.cell(1, 1 + 2 * j), "Fill", True)
        put(t.cell(1, 2 + 2 * j), "ΔI %", True)
    for i, m in enumerate(ROWS):
        put(t.cell(2 + i, 0), m)
        for j, (ds, tr, _) in enumerate(COLS):
            row = r[(r.dataset == ds) & (r.transition == tr) & (r.method == m)].iloc[0]
            put(t.cell(2 + i, 1 + 2 * j), f"{row.fill:.3f}")
            if m == "LGB-Q":
                put(t.cell(2 + i, 2 + 2 * j), f"{row.inv:.2f} wk")
            else:
                sign = lambda v: f"{100 * v:+.1f}".replace("-", "−")
                put(t.cell(2 + i, 2 + 2 * j), f"{sign(row.d_inv)}\n[{sign(row.lo)},{sign(row.hi)}]")
    widths = [Inches(0.6)] + [Inches(0.45), Inches(0.79)] * len(COLS)
    t.autofit = False
    for row in t.rows:
        for c, w in zip(row.cells, widths):
            c.width = w
    # Word takes column widths from tblGrid and needs a fixed layout to respect them
    for gc, w in zip(t._tbl.tblGrid.findall(qn("w:gridCol")), widths):
        gc.set(qn("w:w"), str(int(w.inches * 1440)))
    pr = t._tbl.tblPr
    for el in pr.findall(qn("w:tblLayout")):
        pr.remove(el)
    lay = OxmlElement("w:tblLayout")
    lay.set(qn("w:type"), "fixed")
    pr.append(lay)
    cap._p.addnext(t._tbl)
    return t


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--src", required=True)
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    d = docx.Document(a.src)

    # P0 – independent panel in Section 3.1
    clone_after(find(d, "A single processing pipeline handles both panels."), VNF)

    # P1 – contributions and the related-work sentence
    old = [p for p in d.paragraphs if p.text.startswith("•  ")]
    assert len(old) == 4
    for p, text in zip(old[:3], BULLETS):
        set_text(p, text)
    replace_in(d, "We retain eligible series across demand classes",
               "and a pre-specified combination of the compared methods.",
               "and a check of whether retrospective inventory savings survive deployment-style evaluation.")

    # P1 – Table 7 after the rewritten robustness paragraph
    rob = find(d, "Prospective τ, resampling and a third dataset.")
    set_text(rob, ROBUST)
    cap_proto = find(d, "Table 6.")
    build_table(d, rob, cap_proto, d.tables[5])

    # compensating cuts
    set_text(find(d, "Lead time. We repeated the equal-fill comparisons"),
             "Lead time. At lead times of one and four weeks in every window (HGB-Q omitted), LGB-Q needs less inventory "
             "on M5 than LGB-T, LGB-C, TSB-NB and ETS in all nine window–lead-time runs (2.5–14.8% at fill rate 0.94). On "
             "VN1 the post hoc C2 uses 3.2–10.9% less inventory than LGB-Q at fill rate 0.92 in all nine runs, with "
             "intervals excluding zero in seven; its maximum regret over the 18 runs is 2.0%, against 12.6% for LGB-Q.")
    set_text(find(d, "Computational cost. All methods except Chronos-2"),
             "Computational cost. Except Chronos-2, every method forecasts a 26-week window within minutes on the laptop "
             "CPU (TSB-NB 1–2, LGB-Q on M5 10–21, N-HiTS about 7). Zero-shot Chronos-2 [22] needs no training, but its "
             "inference took 5.4 hours per M5 window and 32–45 minutes per VN1 window, while needing 14.7% (M5) and "
             "1.2–48.1% (VN1) more inventory than LGB-Q at fill rate 0.92; it ran without fine-tuning or covariates.")
    set_text(find(d, "Hyperparameters. For h = 3 in the main window"),
             "Hyperparameters. Refitting LGB-Q and LGB-T for h = 3 in the main window with small (15 leaves), large (255) "
             "and regularised (31 leaves, at least 500 samples per leaf, L2 penalty 10) trees leaves LGB-Q 4.7–6.8% below "
             "LGB-T and 7.5–11.0% below TSB-NB in inventory on M5 at fill rate 0.92, with its own inventory changing by "
             "less than 3%. The VN1 ranking persists for three settings; with small trees LGB-T uses 8.9% less inventory "
             "than LGB-Q.")
    replace_in(d, "We tested whether specific differences between M5 and VN1", " Further implementation details are in the "
               "repository.", "")
    replace_in(d, "Neural baseline. We evaluated",
               " Its wQL lies between LGB-Q and TSB-NB in all six runs, and its 0.99-quantile coverage is 0.986–0.992.", "")
    set_text(find(d, "How the quantiles are constructed also matters."),
             "How the quantiles are constructed also matters: on M5 at fill rate 0.94, LGB-T and LGB-C need 3.3–8.2% more "
             "inventory than directly estimated LightGBM quantiles. Residual-based quantiles in [7] and empirical quantiles "
             "in [23] may explain part of the disagreement with those studies, which do not isolate this effect.")
    replace_in(d, "Among the combinations, E7-med has the smallest maximum regret",
               " LGB-T does not reach the highest target levels.", "")
    replace_in(d, "Among the combinations, E7-med has the smallest maximum regret",
               "At higher penalties the methods operate at τ = 0.99; LGB-Q then has the highest fill rate, and C2 can cost as "
               "much as 29% more.", "At higher penalties LGB-Q is cheapest.")
    set_text(find(d, "Toward deployment."),
             "Toward deployment. Because neither combination passed the prospective checks of Section 5.8, LGB-Q is the safer "
             "default. A combination should be frozen and run in shadow mode beside it for several review cycles, with LGB-Q "
             "preferred when lost sales cost more than about 200 weeks of holding and upper-quantile coverage monitored, "
             "where TSB-NB under-covers.")
    replace_in(d, "Censored demand. Both datasets record sales",
               "Censoring could also be handled in training rather than only in evaluation: flagged weeks could be treated as "
               "missing or right-censored observations and estimated with an expectation–maximisation step or a censored "
               "likelihood, as in lost-sales demand estimation [28], with censored quantile regression [29] for the quantile "
               "learners, or with a survival model of the time between sales. We leave such models to future work.",
               "Censoring could also be handled in training, treating flagged weeks as missing or right-censored with an "
               "expectation–maximisation step or a censored likelihood [28], censored quantile regression [29] or a survival "
               "model of the time between sales; we leave this to future work.")
    replace_in(d, "Neural baseline. We evaluated",
               "Because we did not test architectures such as DeepAR or PatchTST, this CPU-budgeted baseline is not "
               "evidence about deep-learning methods as a class.",
               "It is a CPU-budgeted baseline, not evidence about deep learning as a class.")
    replace_in(d, "Among the combinations, E7-med has the smallest maximum regret",
               "(excess stock relative to the best single method, averaged over attainable fill-rate targets in each "
               "dataset–window run)", "(excess stock over the best single method, averaged over attainable targets)")
    replace_in(d, "Quantile liquidation reduces inventory on VN1",
               "Useful next tests would apply the quantile combination to new periods and retail datasets, select models "
               "using only information available before the forecast date, extend the liquidation horizon and compare more "
               "forecasting architectures under the same stock policy.",
               "Useful next tests would use stock-availability records, longer liquidation horizons and more forecasting "
               "architectures under the same stock policy.")
    d.save(a.out)
    print("written", a.out)


if __name__ == "__main__":
    main()
