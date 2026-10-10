"""Assemble the section files of 07_paper_draft/ into one document (README step 11: write each section separately,
then merge). Writes 07_paper_draft/full_draft.md.

The per-file "> Draft ..." notes are dropped; source tags ([P03 p. 2], [R §4], [Nhận định nhóm], [Chưa kiểm chứng])
are kept for verification and must be removed for submission. References are taken from paper_outline.md §6.

Usage:
    python code/assemble_paper.py
"""
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
D = os.path.join(ROOT, "07_paper_draft")
ORDER = ["abstract.md", "introduction.md", "related_work.md", "methodology.md", "results.md", "discussion.md",
         "conclusion.md"]


def body(name):
    text = open(os.path.join(D, name), encoding="utf-8").read()
    lines = [ln for ln in text.splitlines() if not ln.startswith("> Draft")]
    return "\n".join(lines).strip() + "\n"


def main():
    outline = open(os.path.join(D, "paper_outline.md"), encoding="utf-8").read()
    title = re.search(r"\*\*Title:\*\* (.+)", outline).group(1).strip()
    refs = outline[outline.index("## 6. References"):outline.index("## 7. Open items")]
    refs = refs.replace("## 6. References (draft)", "# References")
    abstract = body("abstract.md").replace("# Abstract", "## Abstract")
    abstract = re.sub(r"\*\*Title:\*\*.*\n", "", abstract)
    parts = [f"# {title}", "",
             "> Assembled by `code/assemble_paper.py` from the section files. Internal source tags are kept for "
             "verification and must be removed before submission (`paper_outline.md`).", "",
             abstract]
    for name in ORDER[1:]:
        parts.append(body(name))
    parts.append(refs.strip() + "\n")
    parts.append(body("appendix.md"))
    out = "\n".join(parts)
    # image paths are relative to 07_paper_draft/, which is where the assembled file lives as well
    open(os.path.join(D, "full_draft.md"), "w", encoding="utf-8").write(out)
    words = len(re.findall(r"\w+", out))
    print(f"written 07_paper_draft/full_draft.md ({words:,} words incl. tables and appendix)")


if __name__ == "__main__":
    main()
