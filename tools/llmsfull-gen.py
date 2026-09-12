#!/usr/bin/env python3
"""Generate llms-full.txt: core pages of data-vault as clean markdown for LLM ingestion.

Selection: README + 10 most-referenced dataset pages + 3 newest guides + 14-DOI catalog block.
Content converted verbatim from existing pages (tables, numbers, source links intact).
Rerun after page updates: python3 tools/llmsfull-gen.py
"""
import datetime
import json
import os
import re
import sys
from html.parser import HTMLParser
from urllib.parse import urljoin

BASE = "https://jayjex.github.io/data-vault/"
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# 10 most-referenced dataset pages (inbound refs across llms.txt + guides + hub pages)
DATASETS = [
    "hud-fmr-2026",            # 71 refs
    "nfl-games",               # 42
    "airbnb-six-cities",       # 32
    "hud-fmr-2027",            # 28
    "hud-fmr-by-zip-2027",     # 18
    "earn-bounties",           # 16
    "hud-fmr-county-2026",     # 15
    "scraper-pack",            # 13
    "hud-fmr-metro-2027",      # 10
    "worldbank-g20-population",  # 9
]
# 3 newest guides by last commit
GUIDES = [
    "hsa-vs-fsa-2026-limits-run-out",  # 2026-09-12 21:20
    "zip-prefix-geography",            # 2026-09-11 03:49
    "worldwide-civic-amenities-map",   # 2026-09-11 03:49
]

DOI_IDS = ["22643177", "22643149", "22643189", "22649503", "22665145", "22665925",
           "22666640", "22667164", "22667477", "22667657", "22676080", "22697115",
           "22706557", "22707493"]


def slugify(t):
    t = t.strip().lower()
    t = re.sub(r"[^\w\s-]", "", t)
    return re.sub(r"[\s]+", "-", t)


class PageParser(HTMLParser):
    """Convert the <main> block of one HTML page into markdown blocks.

    Blocks: ("txt", text) | ("pre", fenced) | ("li", "- item" or "1. item")
    Inline: links -> [text](url), b/strong -> **, em/i -> *, code -> `, tables -> pipe rows.
    """

    BLOCK_SKIP_TAGS = {"script", "style", "svg", "select", "button", "img", "input", "iframe"}
    CLASS_SKIP = {"skip", "crumb", "cursor", "toc"}

    def __init__(self, page_url):
        super().__init__(convert_charrefs=True)
        self.page_url = page_url
        self.blocks = []
        self.cur = []          # list of (text, href|None) segments
        self.in_main = False
        self.skip_depth = 0
        self.href = None
        self.code_depth = 0
        self.pre = False
        self.table = None
        self.row = None
        self.cell = None
        self.div_class = None
        self.h1 = None
        self.lists = []        # stack: "ul" | "ol" | "li"
        self.ol_counts = []    # parallel counter for ol depth

    # ---------- helpers ----------
    def seg(self, text):
        return (text, self.href if self.href else None)

    def out(self, text):
        s = self.seg(text)
        if self.cell is not None:
            self.cell.append(s)
        else:
            self.cur.append(s)

    def render(self, segs):
        parts = []
        i = 0
        while i < len(segs):
            text, href = segs[i]
            if href:
                j = i
                buf = []
                while j < len(segs) and segs[j][1] == href:
                    buf.append(segs[j][0])
                    j += 1
                label = "".join(buf).strip()
                if label:
                    parts.append(f"[{label}]({href})")
                else:
                    parts.append(f"<{href}>")
                i = j
            else:
                parts.append(text)
                i += 1
        return "".join(parts)

    def flush(self):
        if self.cell is not None:
            return
        if not self.cur:
            return
        text = self.render(self.cur).strip()
        self.cur = []
        if text:
            self.blocks.append(("txt", text))

    def resolve(self, href):
        if not href:
            return None
        href = href.strip()
        if href.startswith(("mailto:", "javascript:", "#")):
            return None
        if href.startswith(("http://", "https://")):
            return href
        return urljoin(self.page_url, href)

    # ---------- start tags ----------
    def handle_starttag(self, tag, attrs):
        if tag == "main":
            self.in_main = True
            return
        if not self.in_main:
            return
        a = dict(attrs)
        cls = a.get("class", "")

        if self.skip_depth:
            if tag not in ("br", "hr"):
                self.skip_depth += 1
            return

        if tag in self.BLOCK_SKIP_TAGS or any(c in cls.split() for c in self.CLASS_SKIP):
            self.skip_depth = 1
            return

        if tag == "a":
            self.href = self.resolve(a.get("href")) or ""
            return

        if tag == "code":
            self.code_depth += 1
            if not self.pre:
                self.out("`")
            return

        if tag == "pre":
            self.flush()
            self.pre = True
            return

        if tag in ("h1", "h2", "h3", "h4"):
            self.flush()
            return

        if tag == "div":
            if "stats" in cls.split():
                self.flush()
                self.div_class = "stats"
                return
            if "btnrow" in cls.split():
                self.flush()
                self.div_class = "btnrow"
                self.cur = [("- ", None)]
                return
            self.flush()
            return

        if tag == "table":
            self.flush()
            self.table = {"rows": [], "in_head": False}
            return

        if tag == "span":
            if self.div_class == "stats":
                if self.cur:
                    self.cur.append((" · ", None))
                return
            if "sz" in cls.split() and self.lists and self.cell is None:
                self.out(" · ")
                return
            return

        if self.table is not None:
            if tag == "thead":
                self.table["in_head"] = True
            elif tag == "tbody":
                self.table["in_head"] = False
            elif tag == "tr":
                self.row = []
            elif tag in ("td", "th"):
                self.cell = []
            return

        if tag in ("ul", "ol"):
            self.flush()
            self.lists.append(tag)
            self.ol_counts.append(0 if tag == "ol" else None)
            return

        if tag == "li":
            self.flush()
            return

        if tag in ("p", "section", "blockquote", "figure"):
            if self.cur:
                self.flush()
            return

        if tag in ("b", "strong"):
            self.out("**")
            return
        if tag in ("i", "em"):
            self.out("*")
            return
        if tag == "br":
            self.out(" ")
            return
        if tag == "hr":
            self.flush()
            self.blocks.append(("txt", "---"))
            return

    # ---------- end tags ----------
    def handle_endtag(self, tag):
        if not self.in_main:
            return

        if self.skip_depth:
            if tag not in ("br", "hr"):
                self.skip_depth -= 1
            return

        if tag == "main":
            self.in_main = False
            self.flush()
            return

        if tag == "a":
            self.href = None
            return

        if tag == "code":
            self.code_depth = max(0, self.code_depth - 1)
            if not self.pre:
                self.out("`")
            return

        if tag in ("b", "strong"):
            self.out("**")
            return
        if tag in ("i", "em"):
            self.out("*")
            return

        if tag == "pre":
            self.pre = False
            text = self.render(self.cur).strip("\n")
            self.cur = []
            if text.strip():
                self.blocks.append(("pre", "```\n" + text.rstrip() + "\n```"))
            return

        if tag in ("h1", "h2", "h3", "h4"):
            text = self.render(self.cur).strip()
            self.cur = []
            text = re.sub(r"\*+", "", text).strip()
            if tag == "h1":
                self.h1 = text
            else:
                level = {"h2": "###", "h3": "####", "h4": "#####"}.get(tag, "###")
                if text:
                    self.blocks.append(("txt", f"{level} {text}"))
            return

        if tag == "span" and self.div_class == "stats":
            return

        if tag == "span":
            return

        if tag == "div":
            if self.div_class == "stats":
                text = self.render(self.cur)
                text = re.sub(r"\s+", " ", text).strip()
                self.cur = []
                self.div_class = None
                if text:
                    self.blocks.append(("txt", text))
                return
            if self.div_class == "btnrow":
                text = self.render(self.cur)
                self.cur = []
                self.div_class = None
                text = re.sub(r"[ \t]*\n[ \t]*", " ", text)
                text = re.sub(r"\s+", " ", text).strip()
                if text:
                    if not text.startswith("- "):
                        text = "- " + text
                    self.blocks.append(("li", text))
                return
            self.flush()
            return

        if tag in ("td", "th") and self.cell is not None:
            text = self.render(self.cell).strip()
            text = re.sub(r"\s+", " ", text)
            self.row.append(text.replace("|", "\\|"))
            self.cell = None
            return

        if tag == "tr" and self.row is not None and self.table is not None:
            self.table["rows"].append((self.row, self.table["in_head"]))
            self.row = None
            return

        if tag == "table" and self.table is not None:
            rows = self.table["rows"]
            self.table = None
            if not rows:
                return
            head = None
            body = []
            for r, is_head in rows:
                if is_head and head is None:
                    head = r
                else:
                    body.append(r)
            if head is None:
                head = body.pop(0) if body else [""]
            width = max([len(head)] + [len(r) for r in body])
            head = head + [""] * (width - len(head))
            lines = ["| " + " | ".join(head) + " |",
                     "|" + "|".join([" --- "] * width) + "|"]
            for r in body:
                r = r + [""] * (width - len(r))
                lines.append("| " + " | ".join(r) + " |")
            self.blocks.append(("txt", "\n".join(lines)))
            return

        if tag in ("thead", "tbody"):
            return

        if tag in ("ul", "ol"):
            self.flush()
            if self.lists and self.lists[-1] in ("ul", "ol"):
                self.lists.pop()
            if self.ol_counts and self.ol_counts[-1] is None:
                self.ol_counts.pop()
                self.ol_counts.append(None) if False else None
            # pop matching counter
            if self.ol_counts:
                # find top matching list; ol end pops its counter
                if tag == "ol":
                    for k in range(len(self.ol_counts) - 1, -1, -1):
                        if self.ol_counts[k] is not None:
                            del self.ol_counts[k]
                            break
                else:
                    for k in range(len(self.ol_counts) - 1, -1, -1):
                        if self.ol_counts[k] is None:
                            del self.ol_counts[k]
                            break
            return

        if tag == "li":
            text = self.render(self.cur)
            self.cur = []
            marker = "- "
            # find enclosing list type
            for k in range(len(self.lists) - 1, -1, -1):
                if self.lists[k] == "li":
                    continue
                if self.lists[k] == "ol":
                    if k < len(self.ol_counts) and self.ol_counts[k] is not None:
                        self.ol_counts[k] += 1
                        marker = f"{self.ol_counts[k]}. "
                break
            body = text.strip()
            body = re.sub(r"[ \t]*\n[ \t]*", " ", body)
            if body:
                self.blocks.append(("li", marker + body))
            if self.lists and self.lists[-1] == "li":
                self.lists.pop()
            return

        if tag in ("p", "section", "blockquote", "figure"):
            self.flush()
            return

    # ---------- data ----------
    def handle_data(self, data):
        if not self.in_main or self.skip_depth:
            return
        self.out(data)

    # ---------- final markdown ----------
    def markdown(self):
        out = []
        for kind, content in self.blocks:
            if kind == "li":
                if out and out[-1].startswith(("- ", "1. ", "2. ", "3. ", "4. ", "5. ", "6. ", "7. ", "8. ", "9. ")):
                    out[-1] += "\n" + content
                else:
                    out.append(content)
            else:
                out.append(content)
        return "\n\n".join(out)


def convert_page(relpath):
    path = os.path.join(ROOT, relpath)
    url = BASE + relpath
    html_text = open(path, encoding="utf-8").read()
    p = PageParser(url)
    p.feed(html_text)
    p.close()
    md = p.markdown().strip()
    # header dedup: drop content's first line if it duplicates the section title
    nl = md.find("\n")
    first = md if nl == -1 else md[:nl]
    if first.lstrip("#").strip().lower() == (p.h1 or "").lower():
        md = md[nl + 1:].strip() if nl != -1 else ""
    return p.h1, url, md


def doi_section(llms_txt):
    doi_lines = [ln for ln in llms_txt.splitlines()
                 if ln.startswith(("Dataset DOIs", "FY2027 HUD FMR DOI")) and "zenodo.22" in ln]
    parts = []
    if doi_lines:
        parts.append("\n\n".join(doi_lines))
        parts.append("")
        parts.append("DOI to pack mapping (pack names from the dataset index above):")
    for rec in DOI_IDS:
        block = None
        for b in llms_txt.split("### ")[1:]:
            head = b.splitlines()[0].strip()
            if (f"zenodo.{rec}" in b or f"/records/{rec}" in b) and "###" not in b:
                block = head
                break
        if block:
            parts.append(f"- https://doi.org/10.5281/zenodo.{rec} — {block}")
        elif rec == "22706557":
            # housing pack has no llms.txt dataset section (Getly product, no sample dir)
            parts.append("- https://doi.org/10.5281/zenodo.22706557 — US Housing Affordability Pack: HUD Fair Market Rents by ZIP, County and Metro plus Eurostat Unemployment and Price Indices, 68,209 Rows (Getly pack; the FY2027 ZIP file serves free from the hud-fmr-by-zip-2027 dataset page)")
    body = "\n".join(parts).strip()
    return f"Dataset DOIs (14 packs with permanent citable DOIs on Zenodo):\n\n{body}"


def build():
    llms_txt = open(os.path.join(ROOT, "llms.txt"), encoding="utf-8").read()
    catalog = json.load(open(os.path.join(ROOT, "catalog.json")))
    desc = catalog["description"]

    sections = []

    readme = open(os.path.join(ROOT, "README.md"), encoding="utf-8").read().strip()
    # absolutize relative links inside README for standalone-file context
    readme = re.sub(r"\]\((?!https?://|#|mailto:)([^)]+)\)",
                    lambda m: "](" + urljoin(BASE, m.group(1)) + ")", readme)
    sections.append(("README", "https://github.com/jayjex/data-vault", readme))

    for slug in DATASETS:
        h1, url, md = convert_page(os.path.join("datasets", slug + ".html"))
        title = h1 or slug
        sections.append((f"{title} ({slug})", url, md))

    for g in GUIDES:
        h1, url, md = convert_page(os.path.join("guides", g + ".html"))
        title = h1 or g
        sections.append((f"Guide: {title}", url, md))

    sections.append(("Dataset DOIs — Zenodo DOI catalog (14 DOIs)", "https://doi.org/",
                     doi_section(llms_txt)))

    out = []
    out.append("# Data Vault — llms-full.txt")
    out.append("")
    out.append(f"> {desc}")
    out.append("")
    out.append(f"Index (llms.txt): {BASE}llms.txt")
    out.append(f"Catalog (start here): {BASE}catalog.json")
    out.append(f"Base URL: {BASE}")
    out.append(f"Generated: {datetime.date.today().isoformat()}")
    out.append("Scope: README + 10 most-referenced dataset pages + 3 newest guides + 14-DOI catalog block, "
               "converted to markdown. Tables and numbers are verbatim from the live pages; each section lists "
               "its canonical source URL. Full guide set: https://jayjex.github.io/data-vault/guides/ · "
               "Full dataset set: https://jayjex.github.io/data-vault/datasets/")
    out.append("")
    out.append("## Contents")
    for title, url, md in sections:
        out.append(f"- [{title}](#{slugify(title)})")
    out.append("")
    out.append("---")
    for title, url, md in sections:
        out.append("")
        out.append(f"## {title}")
        out.append("")
        out.append(f"Source: {url}")
        out.append("")
        out.append(md.strip())
    text = "\n".join(out).rstrip() + "\n"

    dest = os.path.join(ROOT, "llms-full.txt")
    with open(dest, "w", encoding="utf-8") as f:
        f.write(text)
    size = os.path.getsize(dest)
    print(f"llms-full.txt written: {size} bytes ({size/1024:.1f} KB), {len(sections)} sections")
    if size > 512 * 1024:
        print("ERROR: exceeds 512KB target", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    build()
