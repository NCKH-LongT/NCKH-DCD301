"""Apply the reviewer-driven revisions to the user's edited ICIIT manuscript (08_final_submission/ICIIT2027_Paper.docx).

The input file is never modified; the result is written to a new file. Each change replaces the text of a
paragraph identified by its opening words (so the edit fails loudly if the manuscript changes), or inserts a new
paragraph cloned from a neighbouring one so that the user's styles are kept.

Usage:
    python code/revise_iciit_paper.py --src 08_final_submission/ICIIT2027_Paper.docx --out 08_final_submission/ICIIT2027_Paper_rev1.docx [--leadtime code/outputs/leadtime_all_windows.json]
"""
import argparse
import copy
import json

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


ABS1 = ("Public retail forecasting benchmarks rank methods by forecast error, although forecasts determine replenishment "
        "quantities. We compare seven probabilistic forecasting methods (three statistical, four gradient-boosting) under one "
        "order-up-to policy with optional liquidation, on all eligible series of M5 (physical retail) and VN1 (multi-vendor "
        "e-commerce) over three 26-week test windows. Without cost data, methods are compared by the inventory needed to reach "
        "the same realised fill rate, with bootstrap confidence intervals.")
ABS2 = ("On M5, LightGBM quantile regression (LGB-Q) is the most accurate method and needs 3–11% less inventory than point "
        "forecasts with safety stock, conformal quantiles, TSB-NB and exponential smoothing at a fill rate of 0.94, in every "
        "window{lt_abs} and under four hyper-parameter settings. On VN1 the best method varies by window: TSB-NB needs 13–16% "
        "less inventory on stable-demand series but under-serves growing ones, and neither ADI–CV² classes nor an unsupervised "
        "segmentation anticipates which series will grow. A post hoc equal-weight average of LGB-Q and TSB-NB quantiles needs "
        "6–11% less inventory than LGB-Q on VN1 at a fill rate of 0.92, stays within 1.5% on M5 and has the smallest "
        "worst-case regret (0.9% vs 9.4%), pending independent validation. A univariate N-HiTS baseline leads in no run. "
        "Quantile-based liquidation costs at most 0.02 percentage points of fill rate but shows no economic benefit within 26 "
        "weeks under the assumed costs.")

HP = ("Hyper-parameters. We refitted LGB-Q and LGB-T (h = 3, main window) under three alternative LightGBM settings: small "
      "trees (15 leaves, at least 100 samples per leaf), large trees (255 leaves, at least 50) and a regularised setting "
      "(31 leaves, at least 500, L2 penalty 10). On M5, LGB-Q requires 4.7–6.8% less inventory than LGB-T and 7.5–11.0% less "
      "than TSB-NB at a fill rate of 0.92 under all four settings, with every interval above zero, and its own inventory "
      "varies by less than 3% across settings. On VN1, the conclusions of Section 5.2 hold under three of the four settings. "
      "With small trees, LGB-Q no longer requires significantly less inventory than TSB-NB, LGB-T needs 8.9% less inventory "
      "than LGB-Q at a fill rate of 0.92, and LGB-Q itself needs 6.3% more inventory at 0.94 than with the default setting.")
NN = ("Neural baseline. Outside the seven-method benchmark, we ran a univariate N-HiTS network [26] with a multi-quantile "
      "loss under the same protocol: direct quantiles of h-week totals, refits every 13 weeks and fixed hyper-parameters. Its "
      "wQL lies between those of LGB-Q and TSB-NB in every run (M5: 0.078, 0.083, 0.089; VN1: 0.107, 0.079, 0.104), and its "
      "upper quantiles are well calibrated (empirical coverage of the 0.99 quantile 0.986–0.992). It is not the most "
      "inventory-efficient method in any run: on M5 it requires 2.6–10.0% more inventory than LGB-Q at fill rates 0.90–0.94, "
      "and on VN1 its frontier rank among eight single methods is 2.8–4.4. With N-HiTS included, C2 keeps the lowest maximum "
      "regret (0.9%). We did not evaluate further neural architectures such as DeepAR or PatchTST; with a CPU-only budget, "
      "N-HiTS serves as one representative global neural forecaster, not as an upper bound for deep learning.")
REF26 = ("[26]  C. Challu, K. G. Olivares, B. N. Oreshkin, F. Garza, M. Mergenthaler-Canseco, and A. Dubrawski. 2023. N-HiTS: "
         "Neural hierarchical interpolation for time series forecasting. In Proceedings of the AAAI Conference on Artificial "
         "Intelligence 37, 6. https://doi.org/10.1609/aaai.v37i6.25854")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--src", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--leadtime", default=None, help="JSON with the all-window lead-time sentences")
    a = ap.parse_args()
    lt = json.load(open(a.leadtime, encoding="utf-8")) if a.leadtime else None
    d = docx.Document(a.src)

    # 1. abstract in two paragraphs
    p = find(d, "Public retail forecasting benchmarks primarily")
    set_text(p, ABS1)
    clone_after(p, ABS2.format(lt_abs=lt["abstract"] if lt else ""))

    # 2. hyper-parameters are fixed -> point to the sensitivity analysis
    p = find(d, "Section 5.5 additionally examines C2")
    t = p.text
    old = "Hyperparameters are held fixed; the models are not tuned for these experiments."
    assert old in t
    set_text(p, t.replace(old, "Hyperparameters are held fixed and not tuned; Section 5.8 reports their sensitivity."))

    # 3. contributions: mention the robustness checks and the neural baseline
    p = find(d, "We evaluate probabilistic forecasting methods by simulating")
    t = p.text
    old = "(3) repeats the experiments across three 26-week windows per dataset;"
    assert old in t
    set_text(p, t.replace(old, "(3) repeats the experiments across three 26-week windows per dataset and checks hyper-parameters, "
                               "lead times and a neural baseline;"))

    # 4. new Section 5.8 after 5.7
    h57 = find(d, "5.7  Sensitivity to dataset differences")
    body57 = find(d, "We examine three potential sources of dataset-specific results")
    h58 = copy.deepcopy(h57._p)
    body57._p.addnext(h58)
    h58p = docx.text.paragraph.Paragraph(h58, body57._parent)
    set_text(h58p, "5.8  Robustness checks and a neural baseline")
    q = clone_after(h58p, HP)
    # the heading clone carries heading style; the body paragraphs must be cloned from a body paragraph
    q._p.getparent().remove(q._p)
    b1 = copy.deepcopy(body57._p)
    h58.addnext(b1)
    b1p = docx.text.paragraph.Paragraph(b1, body57._parent)
    set_text(b1p, HP)
    last = b1p
    if lt:
        last = clone_after(last, lt["section"])
    clone_after(last, NN)

    # 5. lead-time sentence in 5.5 and the limitations
    p = find(d, "At a realised fill rate of 0.92, C2 requires")
    t = p.text
    old = ("With one- and four-week lead times in the VN1 main window, C2 requires 4.1% and 5.4% less inventory than LGB-Q, "
           "respectively, at a fill rate of 0.94. These lead-time checks do not extend to the other test windows.")
    assert old in t
    set_text(p, t.replace(old, lt["c2"] if lt else "With one- and four-week lead times in the VN1 main window, C2 requires "
                                                     "4.1% and 5.4% less inventory than LGB-Q, respectively, at a fill rate of 0.94 (Section 5.8)."))
    p = find(d, "Limitations. Recorded sales proxy demand")
    t = p.text
    old1 = ("Hyperparameters are not tuned, although the reported M5 comparisons persist under four LightGBM settings. "
            "Lead times of one and four weeks were examined only in the main window.")
    assert old1 in t
    new1 = ("Hyperparameters are not tuned; the M5 comparisons persist under four LightGBM settings and the VN1 comparisons "
            "under three of four (Section 5.8). " + (lt["limitation"] if lt else
            "Lead times of one and four weeks were examined only in the main window."))
    t = t.replace(old1, new1)
    old2 = "this result is not part of the seven-method main benchmark."
    assert old2 in t
    t = t.replace(old2, "this result and the N-HiTS baseline (Section 5.8) are not part of the seven-method main benchmark.")
    set_text(p, t)

    # 0. authors (order as given by the first author)
    set_text(find(d, "[AUTHOR NAMES TO BE ADDED]"), "Bùi Anh Duy, Khổng Trần Gia Huy, Nguyễn Thị Cẩm Hương, Trương Long")
    set_text(find(d, "[Affiliation, city, country, e-mail"),
             "FPT University, Ho Chi Minh City, Vietnam · anhduy290605@gmail.com, huyktgse180313@fpt.edu.vn, "
             "huongntc2@fpt.edu.vn, longt5@fpt.edu.vn")
    p = find(d, "ACM Reference Format:")
    assert "[Author names to be added]" in p.text
    set_text(p, p.text.replace("[Author names to be added]", "Bùi Anh Duy, Khổng Trần Gia Huy, Nguyễn Thị Cẩm Hương, and Trương Long"))

    # 6a. code link
    p = find(d, "Each dataset is evaluated on its final 26 weeks")
    t = p.text
    assert "[link to be added]" in t
    set_text(p, t.replace("[link to be added]", "https://github.com/anhduyBA/forecast-to-decision-benchmark"))

    # 6. reference [26]
    clone_after(find(d, "[25]  M. Z. Babai"), REF26)
    d.save(a.out)
    print("written", a.out)


if __name__ == "__main__":
    main()
