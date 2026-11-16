#!/usr/bin/env python3
"""Build a book-style Markdown/LaTeX source from the public essay."""
from __future__ import annotations

import re
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SRC = ROOT.parent / "README.md"


def main() -> None:
    s = SRC.read_text(encoding="utf-8")

    # Keep the opening address; drop the web title/blockquote.
    intro_start = s.index("如果你读到这里")
    zero = s.index("## 0.")
    intro = s[intro_start:zero].strip()

    rest = s[zero:]
    rest = re.sub(r"^## 0\.\s*.*$", "# 先把“下一个黄仁勋”放下", rest, count=1, flags=re.M)
    chapter_map = {
        "## 1.": "# 逆周期的本质",
        "## 2.": "# 七种逆周期平台资产",
        "## 3.": "# 七条逆周期崛起路径",
        "## 4.": "# AI 冲击下的特殊逆周期",
        "## 5.": "# 24 个月逆周期 Playbook",
        "## 6.": "# 对照：两种策略",
        "## 7.": "# 失败模式",
        "## 8.": "# 最后的条件清单",
    }
    lines = []
    for line in rest.splitlines():
        for prefix, title in chapter_map.items():
            if line.startswith(prefix):
                line = title
                break
        lines.append(line)
    rest = "\n".join(lines)

    # Insert the opening address after the first chapter heading.
    rest = rest.replace(
        "# 先把“下一个黄仁勋”放下",
        "# 先把“下一个黄仁勋”放下\n\n" + intro,
        1,
    )

    # Section numbering is redundant in a book.
    rest = re.sub(r"^### \d+\.\d+\s+", "## ", rest, flags=re.M)
    rest = re.sub(r"^### (路径[一二三四五六七]：)", r"## \1", rest, flags=re.M)

    # Drop the web colophon; it lives on the copyright page.
    cut = rest.rfind("\n---\n")
    if cut != -1 and "本文为公开版" in rest[cut:]:
        rest = rest[:cut]

    book_md = rest.strip() + "\n"
    # Ensure lists that follow a colon are parsed as lists, not inline text.
    lines = book_md.splitlines()
    normalized = []
    for line in lines:
        if normalized and normalized[-1].rstrip().endswith("：") and re.match(r"^(\d+\.|-)\s", line):
            normalized.append("")
        normalized.append(line)
    book_md = "\n".join(normalized) + "\n"
    (ROOT / "book.md").write_text(book_md, encoding="utf-8")

    subprocess.run(
        ["pandoc", "book.md", "-f", "markdown+pipe_tables", "-t", "latex",
         "--top-level-division=chapter", "-o", "content.tex"],
        cwd=ROOT, check=True,
    )

    print("wrote book.md and content.tex")
    for line in book_md.splitlines():
        if line.startswith("#"):
            print(line)


if __name__ == "__main__":
    main()
