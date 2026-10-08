"""Imports C:\\Users\\matti\\affiliate-marketing\\content\\*.md into _posts/ as Jekyll posts.

Re-runnable: it overwrites posts it created before (same filename) and leaves others alone.
  python import_posts.py [YYYY-MM-DD]     # post date, default today

For each source post it: builds Jekyll front matter (title from the H1, description from the
meta description), drops the H1 (the layout prints the title), and rewrites generator
placeholders like "[AFFILIATE LINK: matched betting service]" to
<mark class="aff">[AFFILIATE_LINK_ODDSMONKEY]</mark> so they are obvious on the page.
"""
import datetime as dt
import re
import sys
from pathlib import Path

SRC = Path(r"C:\Users\matti\affiliate-marketing\content")
DEST = Path(__file__).parent / "_posts"

# generator placeholder text (lower-case) -> token. Edit if you regenerate posts with other placeholders.
LINKS = {
    "matched betting service": "ODDSMONKEY",
    "matched betting training platform": "PROFITACCUMULATOR",
    "prop firm name": "WISE",
    "ai writing assistant": "AI_WRITING_TOOL",
    "property crm software": "PROPERTY_CRM",
}


def token_for(label: str) -> str:
    key = label.strip().lower()
    return LINKS.get(key) or re.sub(r"[^A-Z0-9]+", "_", label.upper()).strip("_")


def convert(text: str) -> tuple[dict, str]:
    m = re.match(r"---\n(.*?)\n---\n", text, re.S)
    fm = {}
    if m:
        for line in m.group(1).splitlines():
            k, _, v = line.partition(":")
            fm[k.strip()] = v.strip().strip('"')
        text = text[m.end():]
    h1 = re.search(r"^# (.+)$", text, re.M)
    fm["title"] = h1.group(1).strip() if h1 else fm.get("keyword", "Untitled")
    if h1:
        text = text[:h1.start()] + text[h1.end():]
    # the layout prints its own disclosure above the post, so drop the generator's duplicate line
    text = re.sub(r"^\*Affiliate disclosure:.*\*\s*$", "", text, flags=re.M)
    text = re.sub(
        r"\[AFFILIATE LINK:\s*([^\]]+)\]",
        lambda mm: f'<mark class="aff">[AFFILIATE_LINK_{token_for(mm.group(1))}]</mark>',
        text,
    )
    return fm, text.strip() + "\n"


def main() -> None:
    date = sys.argv[1] if len(sys.argv) > 1 else dt.date.today().isoformat()
    DEST.mkdir(exist_ok=True)
    for src in sorted(SRC.glob("*.md")):
        fm, body = convert(src.read_text(encoding="utf-8"))
        esc = lambda s: s.replace("\\", "\\\\").replace('"', '\\"')
        front = (
            "---\n"
            "layout: post\n"
            f'title: "{esc(fm["title"])}"\n'
            f'description: "{esc(fm.get("meta_description", ""))}"\n'
            f'topic: {fm.get("topic", "")}\n'
            f'keyword: "{esc(fm.get("keyword", ""))}"\n'
            f"date: {date} 09:00:00 +0100\n"
            "---\n\n"
        )
        out = DEST / f"{date}-{src.stem}.md"
        out.write_text(front + body, encoding="utf-8")
        tokens = sorted(set(re.findall(r"\[AFFILIATE_LINK_[A-Z0-9_]+\]", body)))
        print(f"{src.name} -> _posts/{out.name}   placeholders: {', '.join(tokens) or 'none'}")


if __name__ == "__main__":
    main()
