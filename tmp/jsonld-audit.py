#!/usr/bin/env python3
"""data-vault JSON-LD audit: parse all ld+json blocks in 170 html, check required props per type."""
import json, re, sys
from pathlib import Path

ROOT = Path("/home/uwuki/money-mission/data-vault")

REQUIRED = {
    "Article": ["headline", "datePublished", "author"],
    "Dataset": ["name", "description", "license", "distribution"],
    "DataCatalog": ["name", "description"],  # extra: catalog page
    "FAQPage": ["mainEntity"],
    "BreadcrumbList": ["itemListElement"],
    "WebSite": ["name", "url"],
}
# soft-warn (recommended, not hard-required by brief)
SOFT = {"Dataset": ["url", "creator", "keywords", "dateModified", "isAccessibleForFree"]}

def find_html():
    files = sorted(p for p in ROOT.rglob("*.html") if "tmp" not in p.parts and "state" not in p.parts)
    return files

def extract_blocks(text):
    out = []
    for m in re.finditer(r'<script[^>]*type=["\']application/ld\+json["\'][^>]*>(.*?)</script>', text, re.S | re.I):
        out.append(m.group(1))
    return out

parse_errors = []   # (file, idx, err)
type_counts = {}
missing_hard = []   # (file, type, prop)
missing_soft = []   # (file, type, prop)
empty_vals = []     # (file, type, prop) — present but empty

files = find_html()
for f in files:
    rel = f.relative_to(ROOT)
    text = f.read_text(encoding="utf-8", errors="replace")
    blocks = extract_blocks(text)
    if not blocks:
        parse_errors.append((str(rel), None, "NO ld+json block"))
        continue
    for i, raw in enumerate(blocks):
        try:
            data = json.loads(raw)
        except json.JSONDecodeError as e:
            parse_errors.append((str(rel), i, f"JSON error: {e} @ line {e.lineno} col {e.colno}"))
            continue
        # normalize to list of nodes
        nodes = data if isinstance(data, list) else [data]
        for node in nodes:
            if not isinstance(node, dict) or "@type" not in node:
                continue
            t = node["@type"]
            if isinstance(t, list):
                tl = t
            else:
                tl = [t]
            for tt in tl:
                type_counts[tt] = type_counts.get(tt, 0) + 1
                for prop in REQUIRED.get(tt, []):
                    v = node.get(prop)
                    if v is None:
                        missing_hard.append((str(rel), tt, prop))
                    elif isinstance(v, str) and not v.strip():
                        empty_vals.append((str(rel), tt, prop))
                    elif isinstance(v, list) and not v:
                        empty_vals.append((str(rel), tt, prop))
                for prop in SOFT.get(tt, []):
                    if node.get(prop) in (None, "", []):
                        missing_soft.append((str(rel), tt, prop))

print(f"files scanned: {len(files)}")
print(f"\n=== TYPE COUNTS ===")
for t, c in sorted(type_counts.items(), key=lambda x: -x[1]):
    print(f"  {t}: {c}")

print(f"\n=== PARSE ERRORS ({len(parse_errors)}) ===")
for e in parse_errors:
    print(f"  {e[0]} block#{e[1]}: {e[2]}")

print(f"\n=== MISSING REQUIRED ({len(missing_hard)}) ===")
for e in missing_hard:
    print(f"  {e[0]} [{e[1]}] missing {e[2]}")

print(f"\n=== PRESENT BUT EMPTY ({len(empty_vals)}) ===")
for e in empty_vals:
    print(f"  {e[0]} [{e[1]}] empty {e[2]}")

print(f"\n=== SOFT MISSING (recommended) ({len(missing_soft)}) ===")
for e in missing_soft:
    print(f"  {e[0]} [{e[1]}] missing {e[2]}")
