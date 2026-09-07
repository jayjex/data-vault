# State — SEO 1 page: NFL vs college football data sources (2026-09-10)

Repo: jayjex/data-vault (main). No AI self-reference on any page touched. No dollar signs anywhere on the new page (NO PRICE rule).

## Page
- New: `guides/nfl-vs-college-football-data.html` — "NFL vs College Football Statistics: Data Sources Compared"
- Keywords targeted: "nfl vs college football statistics" (H1, title, breadcrumb, og), "college football data sources" (H2, body)
- Angle: data source comparison, NFL (nflverse, 7,548 games, CC BY 4.0, community-maintained = cleaner for analysis) vs NCAA side (CFBD API, Sports Reference CFB, NCAA stats portal, plus ESPN CFB site API as the quick-scores route)
- Master table: source | coverage | format | license | free tier (5 rows). Second table: structural differences NFL vs CFB (league structure, schedules, postseason, stats sourcing, naming, machine-readable history). Third table: which source for which job.
- Positive section: why NFL data is cleaner (one schema, one issuer, one license, open QA via nflverse community)

## Fact discipline (all verbatim from live checks / provider docs, same-day 2026-09-10)
- CFBD keyless call → 401; body pasted verbatim: `{"message":"Unauthorized. Did you forget to add \"Bearer \" before your key? Go to CollegeFootballData.com to register for your free API key..."}`
- CFBD terms read at collegefootballdata.com/terms: free key, Bearer on every request, tiers = shared quota pool, one subscription covers CFBD+CBBD, commercial use in-app allowed, redistribution prohibited, attribution appreciated not required, no SLA. Operator: Rad Sports Analytics LLC.
- CFBD Python client `cfbd` snippet from official CFBD blog (blog.collegefootballdata.com), not invented.
- Sports Reference: curl to /cfb/ → 403 Access Denied (Akamai). data_use.html read: no automated access without permission, no competing data store, no AI-training use, custom extracts at a five-figure minimum (stated without a currency symbol to honor NO PRICE), facts-not-copyrighted counterweight noted.
- NCAA stats portal: curl → 403 Access Denied; browser-side load confirmed via reader fetch; official + school-reported + HTML-only stated.
- ESPN CFB site API: scoreboard 200 with 25 events; teams 200 returning 50 teams across divisions, first team "Amherst Mammoths" (Division III) — used as concrete evidence there is no documented classification filter.
- No invented stats. Numbers used: 7,548 rows (own pack, nflverse games.csv), 7,182 home-site games (own prior analysis), 32 clubs, "more than 130" top-division schools (deliberately conservative), 25 events / 50 teams / 403/401 codes (live same-day).

## SEO requirements checklist
- JSON-LD: Article + BreadcrumbList + FAQPage(3) — all 3 blocks json.loads-validated
- FAQ visible == JSON-LD: 3/3 verbatim match after tag-stripping (script-compared)
- NO PRICE: 0 dollar signs on page (assert-checked)
- sitemap.xml: 126 → 127 URLs, new entry lastmod 2026-09-10, minidom-validated, no dup locs
- llms.txt: +1 guide line under Guides (after nfl-data-apis line)
- Cross-links 2-way:
  - new → nfl-data-apis.html (byline + ESPN section + verdict) and new → public-data-apis-list.html (ESPN section)
  - nfl-data-apis.html → new (verdict paragraph in quick answer)
  - public-data-apis-list.html → new ("Where to go next" section)
- Banned-word scan: clean (delve/leverage/robust/etc all absent); 0 em dashes; active voice; no throat-clearing
- No touching journal/STATUS/Getly API/matchbook-labs

## Files changed
- guides/nfl-vs-college-football-data.html (new)
- guides/nfl-data-apis.html (1 link added)
- guides/public-data-apis-list.html (1 link added)
- sitemap.xml (+1 url)
- llms.txt (+1 line)

## Verification
- Local: JSON-LD parse, FAQ mirror, tag balance, canonical URL, keyword presence — all pass (script in session log)
- Live: to be checked post-push (HTTP 200 on the deployed URL)

## Cost
- $0. Research via free fetches + curl; no paid APIs.
