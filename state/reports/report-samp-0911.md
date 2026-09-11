# DV Sample-First Audit 2026-09-11

Scope: every sample/data file path advertised in catalog.json (all string fields walked: sample.csv, sample.json, extra_files, mcp) + products.html hrefs. Complements report-dvlinks-0911.md (that one covered html hrefs only; catalog sample links were not in its scope).

## Method

1. Parsed catalog.json (26 datasets), recursive walk of every string value; kept URLs matching .csv/.json/.pdf/.zip under jayjex.github.io/data-vault/ → 76 unique local paths.
2. products.html href extraction → only catalog.json, no direct sample links (cards link catalog per sample-first design).
3. Filesystem existence check against data-vault/ repo layout.
4. Live spot-check: 5 GETs (curl, discard body, 20s timeout each).

## Results

| Check | Count | Missing/Broken |
|---|---|---|
| catalog.json paths extracted | 76 | — |
| Files exist on disk | 76 | 0 missing |
| products.html sample hrefs | 1 (catalog.json) | 0 |
| Live spot-check (5 URLs) | 5 | 0 (all 200) |

Live spot-check:

| URL | Status | Content-Type |
|---|---|---|
| data/nfl-games/sample.csv | 200 | text/csv; charset=utf-8 |
| data/osm-civic/sample.json | 200 | application/json; charset=utf-8 |
| data/hud-fmr-2027/sample.csv | 200 | text/csv; charset=utf-8 |
| data/airbnb-six-cities/sample.csv | 200 | text/csv; charset=utf-8 |
| data/eurostat/rents/sample.json | 200 | application/json; charset=utf-8 |

## Notes

- Full-dataset files (full_data, e.g. hud-fmr-by-zip-2027/fmr-by-zip-2027.csv, osm-*/civic-amenities.csv) are all present too — extras and samples alike, 76/76.
- No pdf/zip in catalog; all links are csv/json. No dangling sample.* promises: every dataset with a sample block resolves.
- html pages under agents/ + datasets/ reference a handful of sample.json paths directly (embedded listing); spot-verified 4 of them on disk, all present.

## Fixes applied

None needed. Missing count 0 (≤5 threshold would have triggered repair; nothing to repair).

## Budget

5 HTTP GETs (limit 5), $0, no sleeps.
