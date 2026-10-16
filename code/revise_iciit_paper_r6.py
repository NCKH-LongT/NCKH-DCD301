"""Second review round (16/10/2026) on the user's manuscript 08_final_submission/ICIIT2027_Paper_Updated_Title.docx.

Reviewer requests: (1) discuss lost-sales censoring of demand; (2) give an explicit formula for the break-even
salvage ratio s*; (3) discuss online/adaptive learning for LGB-Q on fast-growing e-commerce series; (4) a deployment
and independent-validation path for C2. The input file is never modified.

Usage:
    python code/revise_iciit_paper_r6.py --src 08_final_submission/ICIIT2027_Paper_Updated_Title.docx --out 08_final_submission/ICIIT2027_Paper_rev6.docx
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


def clone_after(p, text):
    el = copy.deepcopy(p._p)
    p._p.addnext(el)
    q = docx.text.paragraph.Paragraph(el, p._parent)
    set_text(q, text)
    return q


# (2) explicit s* -- matches code/liquidation_breakeven.py
SSTAR = ("Liquidation. For each policy we simulate each series twice from the same starting stock, with and without "
         "liquidation, and write Δ for the difference between the two runs over the test window. With unit cost "
         "normalised to 1, ΔO is the change in units ordered, ΔS the change in units sold, ΔI the change in inventory "
         "(unit-weeks), ΔE the change in the end-of-horizon position (on-hand plus on-order units, valued at cost) and Q "
         "the number of units liquidated. With weekly holding rate h (annual rate / 52) and gross margin m (selling price "
         "(1 + m) times cost), liquidating at salvage ratio s is at least as profitable as holding when "
         "s·Q + (1 + m)·ΔS − ΔO − h·ΔI + ΔE ≥ 0. The break-even salvage ratio is therefore "
         "s* = [ΔO − ΔE + h·ΔI − (1 + m)·ΔS] / Q. "
         "A value s* < 1 means that liquidating below cost still pays off; s* > 1 means that liquidation pays off only if "
         "stock can be sold above cost. Valuing the end position at cost favours holding, so the reported s* is an upper "
         "bound. Calculations cover annual holding costs of 10–40% and gross margins of 30–100%. Neither actual salvage "
         "prices nor inventory costs are observed in these datasets.")

# (3) adaptive learning
ADAPT = ("Adaptive updating. Between refits, the global models are re-applied every week to the newest lags and rolling "
         "statistics, so their forecasts follow recent demand; their parameters, however, are re-estimated only every 13 "
         "weeks, with fixed hyper-parameters. On fast-growing VN1 series this can leave the learned mapping one block "
         "behind a level shift. More frequent refits, online or warm-started updating of the boosted trees, weighting "
         "recent observations more heavily, or re-tuning hyper-parameters at each refit could reduce that lag. The VN1 "
         "sensitivity to tree size (Section 5.8) suggests that configuration matters there. These options were not tested. "
         "They also carry a risk: neither the growth classifier above nor learned combination weights (reported in the "
         "repository) outperformed simpler fixed choices, so added adaptivity should be validated out of sample before it is "
         "adopted.")

# (4) deployment and validation path for C2
DEPLOY = ("Toward deployment of C2. Because C2 was chosen after inspecting these results, its next evaluation should be "
          "prospective. First, freeze its specification: the two members, equal weights, the quantile grid, the policy "
          "and the evaluation metrics (inventory at fill rates 0.90–0.98 and regret). Then apply it, unchanged, to periods "
          "after the end of the current data and to retail datasets not used here. In a company, C2 can first run in "
          "shadow mode next to the current method, comparing realised fill rate and inventory for several review cycles "
          "before any switch. Two guardrails follow from our results: use LGB-Q instead when lost sales cost more than "
          "about 200 weeks of holding, and monitor the empirical coverage of the upper quantiles, where TSB-NB "
          "under-covers. The public repository fixes the code and settings needed for such replications.")

# (1) censoring
CENSOR = ("Censored demand. Both datasets record sales, not demand: in any week with a stockout, recorded sales equal the "
          "available stock and understate demand. Neither dataset includes on-hand records, so these weeks cannot be "
          "identified, and some zero-sales weeks may reflect stockouts rather than absent demand. Censoring affects both "
          "training and evaluation. The models learn from truncated observations, which tends to bias their quantiles "
          "downward for items that often ran out. The simulation also treats recorded sales as demand, so lost sales during "
          "historical stockouts are invisible and fill rates are likely overstated for every method. Because all methods "
          "share the same data and simulation, the comparison between methods is likely less affected than absolute "
          "levels, but the bias need not be equal across methods or demand classes: censoring may, for example, make "
          "intermittent series appear sparser. Data with stock-availability records would allow censored weeks to be "
          "flagged or demand to be reconstructed before training, and would test whether our rankings survive.")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--src", required=True)
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    d = docx.Document(a.src)

    set_text(find(d, "Liquidation. We compute the break-even salvage ratio s*"), SSTAR)

    p = find(d, "None of the policies has a consistent economic advantage")
    t = p.text
    old = "These figures are required salvage thresholds from the cost model, not measured resale revenues or realised profits."
    assert old in t
    set_text(p, t.replace(old, "These figures are upper-bound thresholds from the cost model of Section 3.4, not measured "
                               "resale revenues or realised profits."))

    clone_after(find(d, "On VN1, the retrospective demand split helps describe"), ADAPT)
    clone_after(find(d, "C2 has the smallest maximum regret"), DEPLOY)
    lim = find(d, "Limitations. Recorded sales stand in for demand")
    el = copy.deepcopy(lim._p)
    lim._p.addprevious(el)
    set_text(docx.text.paragraph.Paragraph(el, lim._parent), CENSOR)
    t = lim.text
    old = "Recorded sales stand in for demand, so historical stockouts are unknown."
    assert old in t
    set_text(lim, t.replace(old, "Recorded sales stand in for demand (see above)."))
    d.save(a.out)
    print("written", a.out)


if __name__ == "__main__":
    main()
