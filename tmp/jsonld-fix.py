#!/usr/bin/env python3
"""Fix missing JSON-LD props on 15 priority data-vault pages.
license: CC BY 4.0 URL where source is CC BY 4.0 (nflverse, Inside Airbnb);
CreativeWork embed for proprietary packs (no canonical URL exists).
dateModified: factual values from catalog.json stats.updated (FY2027 metro page = git creation date).
"""
import re
from pathlib import Path

ROOT = Path("/home/uwuki/money-mission/data-vault")

CCBY = '"license": "https://creativecommons.org/licenses/by/4.0/", '

LICENSE_URL = {
    "datasets/nfl-games.html": CCBY,
    "datasets/airbnb-six-cities.html": CCBY,
    "datasets/earn-bounties.html": '"license": {"@type": "CreativeWork", "name": "Superteam Earn Bounties pack license", "description": "Personal and commercial use. No resale of the files as-is."}, ',
    "datasets/scraper-pack.html": '"license": {"@type": "CreativeWork", "name": "Web Scraping Script Pack license", "description": "Personal and commercial use."}, ',
    "guides/nfl-scores-dataset.html": CCBY,
}

DATEMOD = {
    "datasets/nfl-games.html": "2026-09-06",
    "datasets/airbnb-six-cities.html": "2026-08-10",
    "datasets/airbnb-eight-cities.html": "2026-06-24",
    "datasets/earn-bounties.html": "2026-09-04",
    "datasets/scraper-pack.html": "2026-09-07",
    "datasets/worldbank-g20-rural.html": "2026-07-13",
    "datasets/worldbank-g20-population.html": "2026-07-13",
    "datasets/worldbank-g20-life-expectancy.html": "2026-07-13",
    "datasets/hud-fmr-county-2026.html": "2026-09-10",
    "datasets/hud-fmr-metro-2027.html": "2026-09-09",
    "datasets/eurostat-house-prices.html": "2026-07-02",
    "datasets/eurostat-rents.html": "2026-02-06",
}

LD_RE = re.compile(r'(<script[^>]*type=["\']application/ld\+json["\'][^>]*>)(.*?)(</script>)', re.S | re.I)

def dataset_nodes(block):
    """Yield (start, end) spans of Dataset nodes inside a block."""
    for m in re.finditer(r'\{"@context": "https://schema\.org", "@type": "Dataset".*?\}(?=\s*[,}\]])|(?<=\{"@type": "Dataset")', block):
        pass
    # simpler: find '{"@type": "Dataset"' occurrences and their enclosing object bounds
    spans = []
    idx = 0
    while True:
        i = block.find('"@type": "Dataset"', idx)
        if i == -1:
            break
        # walk back to object start '{'
        s = block.rfind("{", 0, i)
        # walk forward matching braces
        depth = 0
        e = s
        while e < len(block):
            c = block[e]
            if c == '{':
                depth += 1
            elif c == '}':
                depth -= 1
                if depth == 0:
                    e += 1
                    break
            e += 1
        spans.append((s, e))
        idx = e
    return spans

touched = []
for rel in sorted(set(list(LICENSE_URL) + list(DATEMOD))):
    p = ROOT / rel
    t = p.read_text()
    changed = []
    def repl(m):
        head, body, tail = m.group(1), m.group(2), m.group(3)
        b = body
        if rel in LICENSE_URL and '"license"' not in b:
            # insert after isAccessibleForFree (or after url if missing)
            if '"isAccessibleForFree": true,' in b:
                b = b.replace('"isAccessibleForFree": true, ', '"isAccessibleForFree": true, ' + LICENSE_URL[rel], 1)
                changed.append("license")
        if rel in DATEMOD and '"dateModified"' not in b:
            # insert after url (existing pattern: url, dateModified, keywords)
            um = re.search(r'("url": "https://jayjex\.github\.io/data-vault/[^"]*", )', b)
            if um:
                b = b.replace(um.group(1), um.group(1) + f'"dateModified": "{DATEMOD[rel]}", ', 1)
                changed.append("dateModified")
        if b != body:
            changed.append("block")
        return head + b + tail
    t2 = LD_RE.sub(repl, t)
    if changed:
        p.write_text(t2)
        touched.append((rel, [c for c in changed if c in ("license", "dateModified")]))

for rel, what in touched:
    print(rel, "->", ",".join(what))
print(f"\n{len(touched)} pages touched")
