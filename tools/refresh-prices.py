#!/usr/bin/env python3
"""Refresh every price cell in data-vault/products.html from state/portfolio.json.

products.html is hand-maintained since the fw-posters wave (gen-products.py aborts
on 'missing from GROUPS: artifacts/products/fw-posters' and would drop the hand-written
New this week rail), so the 0912 sale band never reached the page. This script walks
each <article class="card">, resolves its buy link back to a portfolio row and rewrites
<b>$N</b> price from that row's price_cents — the same source both site generators use.
Cards whose link is the Getly store (staged rail cards) are skipped: no live price yet.
"""
import json
import pathlib
import re
import sys

PORT = pathlib.Path('/home/uwuki/money-mission/state/portfolio.json')
DUMP = pathlib.Path('/home/uwuki/money-mission/tmp/getly-list-0912-fresh-dvsample.json')
PAGE = pathlib.Path('/home/uwuki/data-vault/products.html')

rows = json.loads(PORT.read_text())['products']
by_url = {}
for r in rows:
    for u in (r.get('url'), r.get('fourthwall_url')):
        if u:
            by_url.setdefault(u.rstrip('/'), r)

# Dual-rail precedence, same rule as both generators: an active dump slug is the
# card's buy link even when the row's `url` field still points at Fourthwall.
dump = json.loads(DUMP.read_text())['data']['items']
by_id = {r.get('getly_id'): r for r in rows if r.get('getly_id')}
for i in dump:
    r = by_id.get(i['id'])
    if r and i.get('status') == 'active' and i.get('slug'):
        by_url.setdefault(f"https://www.getly.store/product/{i['slug']}", r)

text = PAGE.read_text()
parts = text.split('<article class="card">')
out = [parts[0]]
changed, skipped = [], []
for seg in parts[1:]:
    m = re.search(r'href="([^"]+)"', seg)
    if not m:
        skipped.append('no-link')
        out.append(seg)
        continue
    row = by_url.get(m.group(1).rstrip('/'))
    if row is None:
        skipped.append(m.group(1))
        out.append(seg)
        continue
    cents = row['price_cents']
    want = 'free' if not cents else f'${cents // 100}'
    pm = re.search(r'<span class="stat"><b>([^<]+)</b> price</span>', seg)
    if pm is None:
        sys.exit(f'no price cell for {row["folder"]}')
    have = pm.group(1)
    if have != want:
        seg = seg.replace(pm.group(0), pm.group(0).replace(f'<b>{have}</b>', f'<b>{want}</b>'), 1)
        changed.append((row['folder'], have, want))
    out.append(seg)
PAGE.write_text('<article class="card">'.join(out))
print(f'cards: {len(parts) - 1} | price cells rewritten: {len(changed)} | skipped: {skipped}')
for c in changed:
    print('  ', *c)
