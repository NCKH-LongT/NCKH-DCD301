"""Final file with the author block in the format the authors supplied (rev22 -> ICIIT2027_Paper.docx; 10 pages).

Format (from the sample the authors gave): names given-name first without diacritics (full syllable reversal, as in
"Binh Thuan Truong" for Trương Thuận Bình), superscript affiliation numbers, "and" before the last author, * on the
corresponding author; one line per affiliation starting with its superscript number; a last line with the
corresponding author's e-mail in a monospaced face. The ACM reference line uses the same names. Text otherwise
identical to rev22.

Usage:
    python code/revise_iciit_paper_final.py --src 08_final_submission/ICIIT2027_Paper_rev22.docx --out 08_final_submission/ICIIT2027_Paper.docx
"""
import argparse
import copy
import re

import docx

AUTHORS = [("Duy Anh Bui", "1"), ("Huy Gia Tran Khong", "1"), ("Huong Cam Thi Nguyen", "1"), ("Long Truong", "1*")]
AFFILIATIONS = [("1", "Faculty of Software Engineering, FPT University, Ho Chi Minh City, Vietnam")]
CORRESPONDING_EMAIL = "longt5@fpt.edu.vn"
OLD_REF_NAMES = "Bùi Anh Duy, Khổng Trần Gia Huy, Nguyễn Thị Cẩm Hương, and Trương Long."
NEW_REF_NAMES = "Duy Anh Bui, Huy Gia Tran Khong, Huong Cam Thi Nguyen, and Long Truong."


def rebuild(p, parts, font=None):
    """parts: list of (text, superscript). New runs copy the formatting of the paragraph's first run."""
    proto = copy.deepcopy(p.runs[0]._r)
    for r in list(p.runs):
        r._r.getparent().remove(r._r)
    for text, sup in parts:
        el = copy.deepcopy(proto)
        p._p.append(el)
        run = docx.text.run.Run(el, p)
        run.text = text
        run.font.superscript = True if sup else None
        if font:
            run.font.name = font
            run._r.get_or_add_rPr().get_or_add_rFonts().set(docx.oxml.ns.qn("w:hAnsi"), font)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--src", required=True)
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    d = docx.Document(a.src)
    names, aff = d.paragraphs[1], d.paragraphs[2]
    assert names.text.startswith("Bùi Anh Duy") and aff.text.startswith("FPT University")

    parts = []
    for k, (n, mark) in enumerate(AUTHORS):
        if k == len(AUTHORS) - 1:
            parts.append(("and ", False))
        parts.append((n, False))
        parts.append((mark, True))
        if k < len(AUTHORS) - 1:
            parts.append((", ", False))
    rebuild(names, parts)

    # one paragraph per affiliation, then the corresponding author's e-mail
    num, text = AFFILIATIONS[0]
    rebuild(aff, [(num, True), (" " + text, False)])
    last = aff
    for num, text in AFFILIATIONS[1:]:
        el = copy.deepcopy(aff._p)
        last._p.addnext(el)
        last = docx.text.paragraph.Paragraph(el, aff._parent)
        rebuild(last, [(num, True), (" " + text, False)])
    el = copy.deepcopy(aff._p)
    last._p.addnext(el)
    mail = docx.text.paragraph.Paragraph(el, aff._parent)
    rebuild(mail, [(CORRESPONDING_EMAIL, False)], font="Courier New")

    ref = [p for p in d.paragraphs if p.text.startswith("ACM Reference Format:")]
    assert len(ref) == 1 and OLD_REF_NAMES in ref[0].text
    for r in ref[0].runs:
        if OLD_REF_NAMES in r.text:
            r.text = r.text.replace(OLD_REF_NAMES, NEW_REF_NAMES)
            break
    else:
        raise SystemExit("reference names are split across runs; not changed")

    # ACM conventions (acmart template): reference line with venue, dates and length; "Table 1:" / "Figure 1:" captions
    old_venue = "(ICIIT 2027). ACM, New York, NY, USA."
    new_venue = "(ICIIT 2027), March 4–7, 2027, Ho Chi Minh City, Vietnam. ACM, New York, NY, USA, 10 pages."
    r = [r for r in ref[0].runs if old_venue in r.text]
    assert len(r) == 1
    r[0].text = r[0].text.replace(old_venue, new_venue)
    n_cap = 0
    for p in d.paragraphs:
        m = re.match(r"^(Table|Figure) (\d+)\.", p.text)
        if m and p.style.name in ("TableCaption", "FigureCaption"):
            first = p.runs[0]
            assert first.text.startswith(m.group(0))
            first.text = first.text.replace(m.group(0), f"{m.group(1)} {m.group(2)}:", 1)
            n_cap += 1
    assert n_cap == 8, n_cap

    # compensating cuts for the longer reference line (10 pages)
    def cut(start, old, new):
        p = [p for p in d.paragraphs if p.text.startswith(start)]
        assert len(p) == 1 and len(p[0].runs) == 1 and old in p[0].text, start
        p[0].runs[0].text = p[0].text.replace(old, new)
    cut("On VN1, the retrospective demand split",
        " Theodorou et al. [7] similarly find cases in which forecast accuracy and inventory cost favour different methods, "
        "though under different service and cost settings.", "")
    cut("Neural baseline. We evaluated",
        "It predicts quantiles of cumulative h-week demand with a multi-quantile loss, is refitted every 13 weeks and uses "
        "fixed hyperparameters.",
        "It predicts h-week demand quantiles and is refitted every 13 weeks with fixed hyperparameters.")
    cut("Toward deployment.",
        "A candidate should be frozen and run in shadow mode beside it for several review cycles, with achieved fill and "
        "upper-quantile coverage monitored, where TSB-NB under-covers.",
        "A frozen candidate should first run in shadow mode beside it, with achieved fill and upper-quantile coverage "
        "monitored.")
    cut("Limitations. Recorded sales stand in for demand", " Chronos-2 [22] ran zero-shot only.", "")
    cut("Quantile liquidation reduces inventory on VN1",
        "Quantile liquidation reduces inventory on VN1 while changing fill rate by at most 0.02 percentage points. Its "
        "economic value is not established under the assumed costs over 26 weeks. Useful next tests would use "
        "stock-availability records, longer liquidation horizons and more forecasting architectures under the same stock "
        "policy.",
        "Quantile liquidation reduces VN1 inventory at a fill-rate cost of at most 0.02 points, but its economic value is "
        "not established under the assumed costs; stock-availability records and longer horizons are the next tests.")
    d.save(a.out)
    print("written", a.out, "|", names.text, "|", aff.text, "|", mail.text)


if __name__ == "__main__":
    main()
