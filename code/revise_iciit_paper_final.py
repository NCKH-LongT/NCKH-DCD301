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
    # second set of cuts: the tables kept whole and moved below their first mention leave less room
    cut("Censored demand. Both datasets record sales",
        "Censoring could also be handled in training, treating flagged weeks as missing or right-censored with an "
        "expectation–maximisation step or a censored likelihood [28], censored quantile regression [29] or a survival "
        "model of the time between sales; we leave this to future work.",
        "Censoring could also be handled in training, with a censored likelihood [28] or censored quantile regression "
        "[29]; we leave this to future work.")
    cut("Adaptive updating.",
        "More frequent or warm-started refits, recency weighting or re-tuning could reduce that lag but were not tested.",
        "More frequent refits or recency weighting could reduce that lag but were not tested.")
    cut("Limitations. Recorded sales stand in for demand",
        "Nabil et al. [27] forecast spare-part demand with a two-stage LightGBM/XGBoost model (an occurrence classifier "
        "times a size regressor) and set stock with a normal safety factor; a quantile version of this design is not "
        "tested here.",
        "A quantile version of the two-stage occurrence-times-size LightGBM/XGBoost model of Nabil et al. [27] is not "
        "tested here.")
    keep_tables_together(d)
    move_figure_after(d, "The stable-demand VN1 group favours")
    move_table_after(d, "Table 1:", "Independent panel.")
    move_table_after(d, "Table 4:", "The stable-demand VN1 group favours")
    move_table_after(d, "Table 7:", "On VN1, the retrospective demand split")
    d.save(a.out)
    print("written", a.out, "|", names.text, "|", aff.text, "|", mail.text)


def move_figure_after(d, anchor_start):
    """Float Figure 1 (image paragraph + caption) to the end of Section 5.2 so that it does not leave half a page empty
    once tables are kept together."""
    from docx.oxml.ns import qn
    cap = [p for p in d.paragraphs if p.style.name == "FigureCaption"]
    assert len(cap) == 1
    img = cap[0]._p.getprevious()
    assert list(img.iter(qn("w:drawing"))), "no image paragraph before the figure caption"
    anchor = [p for p in d.paragraphs if p.text.startswith(anchor_start)]
    assert len(anchor) == 1
    anchor[0]._p.addnext(img)
    img.addnext(cap[0]._p)


def move_table_after(d, caption_start, anchor_start):
    """Move a table (caption, table and the empty paragraph after it) to follow another paragraph of the same section."""
    from docx.oxml.ns import qn
    cap = [p for p in d.paragraphs if p.text.startswith(caption_start)]
    anchor = [p for p in d.paragraphs if p.text.startswith(anchor_start)]
    assert len(cap) == 1 and len(anchor) == 1
    tbl = cap[0]._p.getnext()
    assert tbl.tag == qn("w:tbl")
    block = [cap[0]._p, tbl]
    nxt = tbl.getnext()
    if nxt is not None and nxt.tag == qn("w:p") and not "".join(x.text or "" for x in nxt.iter(qn("w:t"))).strip():
        block.append(nxt)
    prev = anchor[0]._p
    for el in block:
        prev.addnext(el)
        prev = el


def keep_tables_together(d):
    """Short tables never split across pages: rows cannot break, every row is kept with the next, the caption above
    each table is kept with it. Long tables (> 15 rows) may break between rows; their first row is a header row that
    Word repeats on the next page, and the caption stays with the header."""
    from docx.oxml import OxmlElement
    from docx.oxml.ns import qn
    for t in d.tables:
        rows = t.rows
        long_table = len(rows) > 15          # may break across pages, with its header row repeated
        for k, row in enumerate(rows):
            trPr = row._tr.get_or_add_trPr()
            for tag in ("w:cantSplit",) + (("w:tblHeader",) if k == 0 else ()):
                if trPr.find(qn(tag)) is None:
                    trPr.append(OxmlElement(tag))
            if k < len(rows) - 1 and (not long_table or k == 0):
                for p_el in row._tr.iter(qn("w:p")):          # every paragraph, merged cells included
                    docx.text.paragraph.Paragraph(p_el, None).paragraph_format.keep_with_next = True
        prev = t._tbl.getprevious()
        while prev is not None and prev.tag == qn("w:p") and not "".join(x.text or "" for x in prev.iter(qn("w:t"))).strip():
            prev = prev.getprevious()
        if prev is not None and prev.tag == qn("w:p"):
            docx.text.paragraph.Paragraph(prev, None).paragraph_format.keep_with_next = True


if __name__ == "__main__":
    main()
