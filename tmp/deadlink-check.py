#!/usr/bin/env python3
"""deadlink-check.py — local dead-link audit for the data-vault Pages checkout.

0 HTTP, 0 API. Buy links on the site are checked against the storefront truth
on disk: money-mission state/portfolio.json (live rows + fourthwall_url),
tmp/catalogfull-getly.json (Getly active dump), state/sellapp/store-status.md
(SellApp offers marked PUBLIC live) and state/zenodo-dois.json (DOI ledger).
Internal hrefs are checked against files in the checkout.
Exit 0 = nothing unresolved; exit 1 + list of offenders.

    DV_SITE=/home/uwuki/data-vault python3 tmp/deadlink-check.py
"""
import json
import os
import re
import sys
from pathlib import Path
from urllib.parse import urldefrag, urlparse

SITE = Path(os.environ.get('DV_SITE') or '/home/uwuki/data-vault')
ROOT = Path(os.environ.get('MM_ROOT') or '/home/uwuki/money-mission')
PAGES = ['catalog.html', 'products.html', 'index.html', 'portfolio.html',
         'free-printables-index.html', 'free-datasets-for-ai-agents.html', 'printable-index-roundup.html',
         'christmas-gift-planning-hub.html']
PREVIEW = ['datasets/occupation-wages.html', 'agents/agent-skills-vol1.html', 'printables/planner-2027.html']
# informational external hosts (citations, licenses) - not storefront state
HOST_SKIP = {'creativecommons.org', 'www.onetcenter.org', 'www.bls.gov', 'zenodo.org', 'openai.com',
             'developers.openai.com', 'www.anthropic.com', 'www.federalreserve.gov', 'worldbank.org',
             'data.worldbank.org', 'ec.europa.eu', 'europa.eu', 'www.hud.gov', 'www.sec.gov',
             'docs.python.org', 'git-scm.com', 'www.ietf.org', 'tools.ietf.org', 'schema.org',
             'www.w3.org', 'json-schema.org', 'web.archive.org', 'www.rfc-editor.org',
             'modelcontextprotocol.io', 'github.blog', 'www.reddit.com', 'reddit.com',
             'superteam.fun', 'www.superteam.fun', 'makerworld.com', 'www.thingiverse.com', '_printables', 'insider.one', 'sui.io', 'aptos.dev',
             'docs.solana.com', 'solana.com', 'www.npr.org', 'rapin.dev', 'www.crunchbase.com'}
HOST_SKIP |= {h[4:] if h.startswith('www.') else h for h in list(HOST_SKIP)}

rows = json.loads((ROOT / 'state' / 'portfolio.json').read_text())['products']

known, pending = set(), set()
for r in rows:
    st = r['status']
    fw = r.get('fourthwall_url')
    url = r.get('url')
    live = (st == 'LIVE-FOURTHWALL'
            or (st == 'LIVE-GETLY' and ('pending_review' not in (r.get('reason') or '').lower() or fw))
            or (st == 'PENDING-REVIEW-GETLY' and fw))
    if live:
        for u in (fw, url):
            if u:
                known.add(u.rstrip('/'))
    else:
        for u in (fw, url):
            if u:
                pending.add(u.rstrip('/'))

dump = json.loads((ROOT / 'tmp' / 'catalogfull-getly.json').read_text())['data']['items']
for i in dump:
    if i.get('status') == 'active' and i.get('slug'):
        known.add(f"https://www.getly.store/product/{i['slug']}".rstrip('/'))

for line in (ROOT / 'state' / 'sellapp' / 'store-status.md').read_text().splitlines():
    m = re.match(r'\|\s*(\d{6})\s*\|\s*([a-z0-9-]+)\s*\|\s*\$[\d.]+\s*\|\s*PUBLIC live', line)
    if m:
        known.add('https://datavaultdesk.sell.app/product/' + m.group(2))

dois = {v['doi'] for v in json.loads((ROOT / 'state' / 'zenodo-dois.json').read_text()).values()
        if isinstance(v, dict) and v.get('doi')}

bad = []
pages = PAGES + [p for p in PREVIEW if p not in PAGES]
for page in pages + [p for p in PREVIEW if p not in pages]:
    p = SITE / page
    if not p.exists():
        bad.append(f'{page}: page missing')
        continue
    text = p.read_text()
    for href in re.findall(r'href="([^"]+)"', text):
        href = urldefrag(href)[0]
        if not href or href.startswith(('mailto:', 'tel:', '#', 'javascript:')):
            continue
        u = urlparse(href)
        if u.scheme:
            host, path = u.netloc, u.path
            if host == 'doi.org':
                doi = path[len('/'):]
                if doi not in dois:
                    bad.append(f'{page}: DOI not in zenodo ledger: {href}')
                continue
            if host == 'schema.org' or path.startswith('/schema.org'):
                continue
            if host == 'jayjex.github.io':
                if not path.startswith('/data-vault/'):
                    continue  # other Pages site (matchbook-labs), not this checkout
                rel = path[len('/data-vault/'):].lstrip('/')
                tgt = (SITE / rel)
                ok = (tgt / 'index.html').exists() if rel.endswith('/') else (tgt.exists() or (tgt / 'index.html').exists())
                if not ok:
                    bad.append(f'{page}: self-link has no file: {href}')
                continue
            if host in ('github.com', 'www.getly.store') and path in ('/jayjex', '/jayjex/', '/store/matchbook-labs-mtrfh66f'):
                continue
            if host in ('www.getly.store', 'jayjex-shop.fourthwall.com', 'datavaultdesk.sell.app', 'jayjex.gumroad.com'):
                h = href.rstrip('/')
                if h in known:
                    continue
                if h in pending:
                    bad.append(f'{page}: buy link to a NOT-LIVE row: {href}')
                else:
                    bad.append(f'{page}: buy link matches no live row: {href}')
                continue
            if host in ('fonts.googleapis.com', 'fonts.gstatic.com', 'www.w3.org', 'json-schema.org', 'schema.org'):
                continue
            root = host.split(':')[0]
            if root in HOST_SKIP or '.'.join(root.split('.')[-2:]) in {'googleapis.com', 'google.com', 'github.io'}:
                continue
            bad.append(f'{page}: unhandled external host: {href}')
            continue
        # relative
        if href.startswith('/data-vault/'):
            tgt = SITE / href[len('/data-vault/'):]
            ok = (tgt / 'index.html').exists() if str(href).endswith('/') else (tgt.exists() or (tgt / 'index.html').exists())
            if not ok:
                bad.append(f'{page}: broken Pages-root link {href}')
            continue
        if href.startswith('/'):
            bad.append(f'{page}: site-root link outside /data-vault/: {href}')
            continue
        # relative
        rel = href[2:] if href.startswith('./') else href
        base = p.parent if not href.startswith('/') else SITE
        tgt = (base / rel).resolve()
        if rel.startswith('/'):
            tgt = SITE / rel.lstrip('/')
        if rel.endswith('/'):
            ok = (tgt / 'index.html').exists()
        else:
            ok = tgt.exists() or (tgt / 'index.html').exists()
        if not ok:
            bad.append(f'{page}: broken internal link {href}')

text = (SITE / 'catalog.html').read_text()
n_cards = text.count('<article class="card"')
n_buy = len(re.findall(r'<p class="btn-note">Buy on \w+: <a href="', text))
if n_cards != n_buy:
    bad.append(f'catalog.html: {n_buy} buy links for {n_cards} cards')
coming = re.search(r'<ul class="come">(.*?)</ul>', text, re.S)
if coming and '<a ' in coming.group(1):
    bad.append('catalog.html: link inside coming-this-week list')
for prev in PREVIEW:
    t = (SITE / prev).read_text()
    if re.search(r'<a[^>]*aria-disabled="true"', t) or re.search(r'aria-disabled="true"[^>]*href=', t):
        bad.append(f'{prev}: disabled button carries href')
    if 'aria-disabled="true">Coming soon<' not in t:
        bad.append(f'{prev}: Coming-soon pattern missing')
    if re.search(r'Buy on (Getly|Fourthwall)|/product/', t):
        bad.append(f'{prev}: preview page carries a buy link')
for page in pages:
    t = (SITE / page).read_text()
    if 'SLUGPENDING' in t:
        bad.append(f'{page}: SLUGPENDING placeholder left in page')

print(f'pages: {len(pages)} | live urls known: {len(known)} | DOI ledger: {len(dois)} | cards {n_cards} | buy links {n_buy}')
if bad:
    print('DEAD / INVALID:')
    for b in bad:
        print('  -', b)
    sys.exit(1)
print('OK: 0 dead link')
