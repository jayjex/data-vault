# catalog + sitemap sync check — 2026-09-10

## 1. catalog page links → sitemap (7/7 PASS)

| slug | page | file | in sitemap |
|---|---|---|---|
| nfl-games | /datasets/nfl-games.html | Y | Y (2026-09-10) |
| hud-fmr-2026 | /datasets/hud-fmr-2026.html | Y | Y (2026-09-10) |
| hud-fmr-2027 | /guides/hud-fmr-2027.html | Y | Y (2026-09-10) |
| airbnb-six-cities | /datasets/airbnb-six-cities.html | Y | Y (2026-09-10) |
| earn-bounties | /datasets/earn-bounties.html | Y | Y (2026-09-09) |
| scraper-pack | /datasets/scraper-pack.html | Y | Y (2026-09-07) |
| printable-engineering-bundle | /datasets/printable-engineering-bundle.html | Y | Y (2026-09-09) |

## 2. landing pages on disk (7/7 EXIST)

All 6 /datasets/*.html + /guides/hud-fmr-2027.html present. Zero catalog → 404. No fix needed.

Note: hud-fmr-2027 intentionally points to /guides/ (FY2027 first-mover page, commit 45bf702), not /datasets/. Consistent.

## 3. listing pages

- No datasets/index.html exists (none needed, none broken).
- index.html links all 6 dataset pages, but NOT guides/hud-fmr-2027.html (guide surface, not dataset listing — OK).
- free-datasets-for-ai-agents.html links 5 of 6 dataset pages (missing printable-engineering-bundle — fine, that dataset belongs to the printables funnel; it IS listed on free-printables-index.html, printable-index-roundup.html, index.html).
- sitemap: 131 URLs, 0 dupes, minidom-parses clean.

## 4. broken internal links

Checked href/src in all 7 catalog pages + 4 root listing pages, resolved relative → repo path. Broken count: 0. No fix, no commit.

## Verdict

Catalog ↔ sitemap ↔ disk fully in sync. No action taken. Untouched: journal/STATUS/Getly API/matchbook-labs.
