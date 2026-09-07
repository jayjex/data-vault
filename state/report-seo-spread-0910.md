# SEO report: NFL point spread history page — 2026-09-10

Task: 1-page SEO build, guides/nfl-spread-history.html, keywords "nfl point spread history" / "nfl spread data". Angle: spread analysis from games.csv (7,548 rows, 1999-2026, betting lines included; source file money-mission/artifacts/products/nfl-dataset/games.csv). Repo jayjex/data-vault, main. Cost: $0. No contact with journal/, STATUS, Getly API, matchbook-labs.

## Numbers computed verbatim from games.csv (python, re-run 2026-09-10)

- Scope: 7,548 rows. spread_line present on 7,388 (all played + 112 scheduled 2026 rows with early numbers). Played-with-line-and-score: 7,276 (1999-2025). 31 pick'ems (spread_line = 0). 15 ties among played rows.
- Average closing spread by era (abs line, all 7,388 rows): 1999-2003 = 5.30 (1,311); 2004-2008 = 5.49 (1,335); 2009-2013 = 5.50 (1,335); 2014-2018 = 5.11 (1,335); 2019-2023 = 5.44 (1,390); 2024-2026 = 4.95 (682; 2024-25 played only = 5.12). All-time 5.33, median 4.0, per-season max 2009 = 6.54, min full season 2016 = 4.63.
- Home favorite %: played games 4,731/7,276 = 65.0% positive spread_line, away favored 2,514 (34.6%), 31 pick'ems (0.4%). Including 112 scheduled 2026 rows: 4,806/7,388 = 65.1%. Avg line when home favored 5.82, away favored 4.47; mean signed line +2.24 (tracks HFA guide's +2.39 scoring gap).
- Spread accuracy (favorite covers, computed row-by-row; favorite side on pick'ems read from moneyline): favorite 3,464 covers, 3,617 fails, 195 pushes → 48.9% of 7,081 decided (raw 47.4% of 7,276). Alternative pick'em handling (score-only) = 3,473 covers, 49.0%, stated in page + FAQ. Push count 195 reconciles exactly with shipped season-summaries.csv (sum of spread_push_count column). Per shipped season-summaries: best favorite season 2005 = 58.8%, worst 2006 = 43.6%.
- Biggest spreads all-time (full census of all 9 lines >= 20; top-5 = first five rows): 2013-10-13 JAX 19 @ DEN 35, DEN -27, fail; 2007-11-25 PHI 28 @ NE 31, NE -24, fail; 2007-12-23 MIA 7 @ NE 28, NE -22, fail; 2019-09-22 MIA 6 @ DAL 31, DAL -22, cover; 2007-12-16 NYJ 10 @ NE 20, NE -20.5, fail. Behind: IND 2011, NYJ 2019 (-20.5 fail), HOU@ARI 2021 (-20.5 cover), NYJ@KC 2020 (-20 cover). Favorites 3-6 ATS on the nine.
- Biggest upsets by spread (dog wins outright): MIA 27 @ NE 24 (NE -17.5, 2019-12-29) and NYJ 23 @ LA 20 (LA -17.5, 2020-12-20), then BUF 27 @ MIN 6 (MIN -16.5, 2018). Five at 14.5, two at 14, incl. HOU 24 @ PIT 6 (2002, +14) and CLE 16 @ PIT 15 (1999, +14.5). Expansion teams = 2 of the 9 biggest upsets.
- Sign convention verified two ways: sample rows (spread_line -4 = MIN favored @ ATL) and moneyline cross-check (5,315 agree, 87 conflicts all at pick'em-ish -1/+100 territory where moneyline is too thin to signal favorite; page uses spread_line, not moneyline).

## Page spec compliance

- JSON-LD: Article + BreadcrumbList + FAQPage(3), all json.loads-validated.
- FAQ visible text == JSON-LD answer text, script-compared: exact match, all 3.
- NO PRICE: 0 dollar signs on page, script-counted.
- sitemap.xml: +1 url (129 → 130, script-counted), lastmod 2026-09-10, inserted next to nfl-spreads-history.html.
- llms.txt: +1 entry after NFL Spread History CSV line (now 186 lines), same style as neighbors.
- Cross-links 2 arah: new page → nfl-home-field-advantage.html (byline + HFA section) and → nfl-data-apis.html (byline + Get-the-data section). Reverse: nfl-home-field-advantage.html cover section now links new page; nfl-data-apis.html closing paragraph links new page alongside HFA.
- Live verify: python http.server on repo root, curl 200 on new page, both cross-linked pages, sitemap.xml, llms.txt.
- NO karangan: every number on the page re-derived from games.csv this session; pick'em favorite tie-break and 2026-schedule caveat disclosed in-page.

## Files

- New: guides/nfl-spread-history.html
- Modified: sitemap.xml (+1 url), llms.txt (+1 entry), guides/nfl-home-field-advantage.html (1 outbound link), guides/nfl-data-apis.html (1 outbound link)
- Commit: targeted add of the 5 files only; journal/, state/ of other tasks, and other untracked files untouched.

## Guardrails

- Untouched: journal/, STATUS, Getly API, matchbook-labs.
- No AI self-reference on page or report.
- no-ai-slop check run on page copy: banned-word scan clean, 0 em dashes, no throat-clearing openers, colon reveals, or summary endings; numbers carry the prose.
