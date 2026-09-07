# SEO report: what is fair market rent (HUD FMR explained) — 2026-09-10

Task: SEO 1 PAGE — data-vault. Page: guides/hud-fair-market-rent-explained.html. Keyword: "what is fair market rent" / "hud fair market rent explained". Evergreen definition angle: FMR = 40th percentile (not median), how HUD computes it, FMR vs actual rent, why vouchers use FMR, SAFMR vs metro-wide, FY effective dates.

## What was done

- Read no-ai-slop SKILL.md first; page written to house voice, checked against banned words/patterns (script scan, 0 hits).
- New page `guides/hud-fair-market-rent-explained.html` (commit bb926da):
  - Sections: short answer; 40th percentile vs median (QHWRA 1998, PL 105-276, first applied FY2001; HUD 50th percentile estimates as separate huduser.gov product); how HUD computes it (ACS base, recent-mover tuning, inflation, annual workbooks) + FY cycle dates (FY2026 through Sep 30 2026, FY2027 workbooks Aug 26/31 2026, effective Oct 1 2026, median 2BR +3.30%); FMR vs actual rent (percentile/basis/timing/geography; ACS median; ZORI 1,962 vs FMR median 1,150); voucher rationale (24 CFR 982.505 90-110% band, 40% move-in cap); SAFMR vs metro-wide (Dallas 2012 demo, Nov 2016 rule, intra-MSA spread 76437 = 1,090 vs 79536 = 1,460).
  - Real CSV number: ZIP 76437 row verbatim from data/hud-fmr-2026/sample.csv (`76437,METRO10180M10180,metro,"Abilene, TX MSA",TX,850,880,1090,1420,1710`), 2BR 1,090 → band 981-1,199; FY2027 1,150 → band 1,035-1,265. Band math assert-checked.
  - All claims sourced from HUD docs (huduser.gov pages/files already cited site-wide) and our own parsed CSVs. No invented stats.
  - NO PRICE: 0 dollar signs (assert-checked). No self-AI reference. journal/STATUS/Getly/matchbook-labs untouched.
- JSON-LD: Article + BreadcrumbList + FAQPage(4), all json.loads-validated. FAQ visible text == JSON-LD verbatim (script-compared, 4/4).
- sitemap.xml: 127 → 128 URLs, new entry lastmod 2026-09-10 (minidom valid, no duplicate locs).
- llms.txt: +1 guide line under ## Guides (after FMR vs Actual Rent line).
- Cross-links two-way:
  - new page → guides/hud-fmr-data-downloads.html (computes-it section + get-data section) and guides/hud-fmr-2027.html (FY cycle section + get-data section)
  - hud-fmr-data-downloads.html → new page (Excel/CSV/MCP section closing para)
  - hud-fmr-2027.html → new page (Where to get the FY2027 data section)
- Other cross-links from new page: hud-fmr-history.html, safmr-vs-fmr.html, hud-fmr-small-areas.html, hud-fmr-safmr-list.html, fmr-vs-rent-actuals.html, hud-fmr-vs-census-rent.html, hud-fmr-vs-zillow-rent.html, fmr-payment-standard.html, hud-payment-standard.html, datasets/hud-fmr-2026.html, sample.csv.

## Verification

- Local: all three edited/created pages 200 on python http.server; HTMLParser parse ok.
- Push: 7336342..bb926da main -> main.
- Live (2026-09-10, jayjex.github.io/data-vault):
  - page 200
  - 3 JSON-LD blocks parse, types Article/BreadcrumbList/FAQPage
  - FAQ 4/4 verbatim match live
  - verbatim CSV row present live, no $ live
  - sitemap.xml 200, 128 locs, new URL present
  - llms.txt 200, guide line live
  - backlinks live on both target pages (1 link each)

## Constraints

- Untouched: journal, STATUS, Getly API, matchbook-labs. Cost: $0 (GitHub Pages, no APIs called beyond public huduser.gov-derived CSVs already in repo).
