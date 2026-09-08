#!/usr/bin/env python3
"""Generate printable-index-roundup.html: 223 free printables sorted into 4 use cases."""
import re, json, html as H

SRC = "free-printables-index.html"
OUT = "printable-index-roundup.html"
BASE = "https://jayjex.github.io/data-vault"

raw = open(SRC).read()
cards = re.findall(r'<article class="card" data-niche="([a-z]+)">.*?<h2><a href="([^"]+)">(.*?)</a></h2>', raw, re.S)
assert len(cards) == 223, f"expected 223 cards, got {len(cards)}"
assert len({u for _, u, _ in cards}) == 223, "duplicate urls"

SECTIONS = [
    ("uc-budget", "Budget & money packs", [
        ("Budget & money tracking", "budget"),
        ("Freelance & small business", "business"),
        ("Crypto & web3", "crypto"),
    ]),
    ("uc-move", "Moving & home packs", [
        ("Home, moving & rentals", "home"),
        ("Travel & expat paperwork", "travel"),
    ]),
    ("uc-study", "Study, career & planning packs", [
        ("Kids & school", "kids"),
        ("Planners & habits", "planner"),
        ("Jobs & interviews", "career"),
        ("Study, exams & health logs", "study"),
        ("Content, social & PKM", "content"),
    ]),
    ("uc-worksheet", "Worksheet & activity packs", [
        ("Puzzles, games & draft boards", "puzzles"),
        ("Weddings, holidays & parties", "events"),
        ("Kitchen & meal planning", "food"),
        ("Dogs & pets", "pets"),
        ("Garden & homestead", "garden"),
        ("Free data samples", "data"),
    ]),
]

INTROS = {
    "uc-budget": "Envelope budgets, debt payoff trackers, bill and subscription logs, freelance invoices and expense sheets, crypto and wallet records. Use these when money leaks and you want one page that shows where it went.",
    "uc-move": "Move-in and move-out checklists, rental walkthroughs, cleaning schedules, home maintenance logs, expat document organizers. Built for the weeks when boxes are stacked and the landlord is waiting.",
    "uc-study": "Homework and exam schedules, habit and routine trackers, job application and interview sheets, content calendars and second-brain checklists. Print a fresh copy each week instead of rebuilding a spreadsheet.",
    "uc-worksheet": "Kindergarten worksheets, mazes and word searches, holiday party checklists, meal planners, dog training logs, garden records. The print-and-go shelf: hand one to a kid, a guest or yourself.",
}

CTAS = {
    "uc-budget": ('Want packs instead of single sheets? The <a href="datasets/printable-engineering-bundle.html">printable engineering bundle</a> collects the full packs in one download, and the <a href="https://www.getly.store/store/matchbook-labs-mtrfh66f" rel="noopener">Getly store</a> sells each pack separately.',),
    "uc-move": ('Moving this month? Start with the move-in inspection checklist, keep the move-out cleaning checklist for the last day, and grab the <a href="datasets/printable-engineering-bundle.html">full packs in the printable engineering bundle</a> when the free pages run out of rows.',),
    "uc-study": ('Pick one sheet per habit, print a stack on Sunday, and bin the app that keeps nagging you. The <a href="printables/free-printable-templates.html">PDF templates hub</a> sorts these same sheets by topic.',),
    "uc-worksheet": ('Print the kindergarten worksheets for the weekend and keep the maze stack for rainy days. Every sheet prints free, and the <a href="datasets/printable-engineering-bundle.html">printable engineering bundle</a> holds the full packs with answer keys.',),
}

def clean_title(t):
    prev = None
    for _ in range(4):
        if t == prev:
            break
        prev = t
        t = H.unescape(t)
    t = t.replace("\u2014", "-").replace("\u2013", "-")
    t = re.sub(r"\s+", " ", t).strip()
    return t

by_niche = {}
for niche, url, title in cards:
    by_niche.setdefault(niche, []).append((clean_title(title), url))

order_in_index = [n for n, _, _ in cards]
def niche_order(niches):
    return sorted(niches, key=lambda n: order_in_index.index(next(c[0] for c in cards if c[0] == n)))

items = []          # (position, name, url) across page
sec_meta = []
for sid, label, groups in SECTIONS:
    count = sum(len(by_niche[n]) for _, n in groups)
    sec_meta.append((sid, label, groups, count))

for sid, label, groups, count in sec_meta:
    for gname, niche in groups:
        for title, url in by_niche[niche]:
            items.append((len(items) + 1, title, url))
assert len(items) == 223, f"total {len(items)}"

jsonld = {
    "@context": "https://schema.org",
    "@type": "ItemList",
    "name": "Free printable packs by use case",
    "description": "223 free printable packs sorted by use case: budget and money tracking, moving and home, study and career planning, and printable worksheets and activities.",
    "url": f"{BASE}/printable-index-roundup.html",
    "numberOfItems": 223,
    "itemListElement": [
        {"@type": "ListItem", "position": p, "name": n, "url": u} for p, n, u in items
    ],
}
jsonld_str = json.dumps(jsonld, ensure_ascii=False, separators=(",", ":"))

p = []
w = p.append
w('<!DOCTYPE html>')
w('<html lang="en">')
w('<head>')
w('<meta charset="utf-8">')
w('<meta name="viewport" content="width=device-width, initial-scale=1">')
w('<title>Free Printable Packs by Use Case: budget, moving, study and worksheets | Data Vault</title>')
w('<meta name="description" content="223 free printable packs sorted by use case: budget and bill trackers, moving and rental checklists, study and career planners, and printable worksheets. Every sheet prints free.">')
w(f'<link rel="canonical" href="{BASE}/printable-index-roundup.html">')
w('<meta property="og:type" content="website">')
w('<meta property="og:site_name" content="Data Vault">')
w('<meta property="og:title" content="Free Printable Packs by Use Case: budget, moving, study and worksheets">')
w('<meta property="og:description" content="223 free printables sorted by the job you are doing: money tracking, moving house, study and work, and worksheets for kids. Free to print.">')
w(f'<meta property="og:url" content="{BASE}/printable-index-roundup.html">')
w('<meta name="twitter:card" content="summary">')
w(f'<script type="application/ld+json">{jsonld_str}</script>')
w('<link rel="stylesheet" href="./assets/style.css">')
w('<style>')
w('h3.niche-h{font-family:var(--mono);font-size:.78rem;letter-spacing:.1em;text-transform:uppercase;color:var(--muted);margin:30px 0 8px}')
w('h3.niche-h b{color:var(--text)}')
w('ul.packlist{list-style:none;padding:0;margin:0 0 6px}')
w('ul.packlist li{padding:7px 0;border-bottom:1px solid var(--line);font-size:.95rem;max-width:46rem}')
w('ul.packlist a{text-decoration:none;color:var(--text)}')
w('ul.packlist a:hover{color:var(--accent);text-decoration:underline}')
w('p.cta{max-width:46rem;color:var(--muted);font-size:.95rem;margin:14px 0 0}')
w('</style>')
w('</head>')
w('<body>')
w('<a class="skip" href="#main">Skip to content</a>')
w('<header class="site"><div class="wrap">')
w('<a class="brand" href="index.html">data<span class="u">&middot;</span>vault<span class="cursor">_</span></a>')
w('<nav aria-label="Site">')
w('  <a href="index.html">Catalog</a>')
w('  <a href="free-printables-index.html">Free printables</a>')
w('  <a href="printables/free-printable-templates.html">PDF templates</a>')
w('  <a href="agents/">For agents</a>')
w('  <a href="https://www.getly.store/store/matchbook-labs-mtrfh66f" rel="noopener">Store</a>')
w('</nav>')
w('</div></header>')
w('<main id="main" class="wrap page">')
w('  <a class="crumb" href="index.html">&larr; Catalog</a>')
w('  <h1>Free printable packs by use case</h1>')
w('  <div class="stats" style="margin-bottom:26px"><span class="stat"><b>223</b> free printables</span><span class="stat"><b>4</b> use cases</span><span class="stat">print cost <b>free</b></span></div>')
w('  <p>The <a href="free-printables-index.html">free printables index</a> lists every sheet by topic. This page sorts the same 223 printables by the job you are doing: tracking money, moving house, studying or working, and printing worksheets. Every link opens the live page on the Matchbook Labs funnel, you print the free version, and the same page offers the bigger pack when you want more rows, pages or answer keys.</p>')
w('  <p>Sorting by category instead of job? The <a href="printables/free-printable-templates.html">free printable PDF templates hub</a> keeps the 16 topic groups, and the <a href="datasets/printable-engineering-bundle.html">printable engineering bundle</a> collects the packs in one download.</p>')
w('  <nav aria-label="Use cases" style="margin:10px 0 4px"><p style="max-width:46rem;font-family:var(--mono);font-size:.85rem">Jump to: <a href="#uc-budget">budget &amp; money</a> &middot; <a href="#uc-move">moving &amp; home</a> &middot; <a href="#uc-study">study, career &amp; planning</a> &middot; <a href="#uc-worksheet">worksheets &amp; activities</a></p></nav>')

for (sid, label, groups, count) in sec_meta:
    w(f'  <section aria-labelledby="{sid}">')
    w(f'    <h2 class="kicker" id="{sid}">{label} <span class="count">({count})</span></h2>')
    w(f'    <p class="group-intro">{INTROS[sid]}</p>')
    for gname, niche in groups:
        rows = by_niche[niche]
        w(f'    <h3 class="niche-h" id="{sid}-{niche}">{H.escape(gname)} <b>({len(rows)})</b></h3>')
        w('    <ul class="packlist">')
        for title, url in rows:
            w(f'      <li><a href="{url}">{H.escape(title)}</a></li>')
        w('    </ul>')
    w(f'    <p class="cta">{CTAS[sid][0]}</p>')
    w('  </section>')

w('</main>')
w('')
w('<footer><div class="wrap">')
w('<div>Data Vault is a Matchbook Labs project. <a class="mono" href="https://github.com/jayjex" rel="noopener">github.com/jayjex</a></div>')
w('<div class="mono"><a href="guides/how-we-sell-public-data.html">How we sell public datasets</a></div>')
w('<div class="mono">Samples CC BY 4.0 &middot; full packs licensed per purchase &middot; <a href="catalog.json">catalog.json</a></div>')
w('</div></footer>')
w('</body>')
w('</html>')

open(OUT, "w").write("\n".join(p) + "\n")
print(f"wrote {OUT}: {len(items)} links, sections: {[(s[1], s[3]) for s in sec_meta]}")
