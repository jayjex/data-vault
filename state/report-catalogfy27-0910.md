# Catalog report — FY2027 entry — 2026-09-10

Close mcp-listings-4 open item: catalog.json had no hud-fmr-2027, so list_datasets/get_dataset_info missed FY27.

## What changed

- catalog.json: new `hud-fmr-2027` entry after hud-fmr-2026, same field set as FY26 (slug, name, niche, tags, description, stats, sample, extra_files, full_data, license, page — verified programmatically, zero field diff). stats: 51,871 rows / 3 tables / 10 columns / updated FY2027. Description states effective Oct 1 2026. last_built 2026-09-09 → 2026-09-10.
- Sample files added: `data/hud-fmr-2027/sample.csv` (first 22 rows, FY26 format), `sample.json` (same {slug, name, columns, row_count, records} shape), `state-summary.csv` (complete 52-row aggregate).
- Commit bc313f9 (only catalog.json + 3 data files), pushed to main.

## Decisions

- DOI: FY26 pattern has no DOI field, so per instruction the Zenodo DOI stayed out. It's already on the guide page and in dataset-mcp's README/dictionary.
- sha256: no sha256 field in the catalog pattern; hashes live in the dataset-mcp manifest and surface through get_dataset_info's full_query.files merge. Verified both: cached hud-fmr-by-zip-2027.csv hashes to 3f94c5e98da5…, hud-state-summary-2027.csv to 97a5c5a50ddd…, both match manifest data-v1.
- full_data: no FY27 Getly product exists yet, so the entry uses the store-page URL plus a note (FY2027 pack in prep; full files free via query_dataset("hud-fmr-2027") / data-v1 release). Same pattern as the printable-engineering-bundle entry.
- page: datasets/hud-fmr-2027.html doesn't exist, so the entry points to the live guide page guides/hud-fmr-2027.html instead of a 404.
- FY26 entry says columns: 11 for a 10-column CSV; FY27 entry uses the real count (10). FY26 left untouched.

## Verification

- JSON parses; FY27 entry field set matches FY26 exactly.
- query_dataset simulation on the cached release file: 51,871 rows, state=TX → 3,244 matched (first zip 76437, 2BR 1150), state=CA → 2,605.
- Live 200 after push: catalog.json, sample.csv, sample.json, state-summary.csv. Live catalog lists 7 datasets including hud-fmr-2027.
- Live manifest (raw.githubusercontent main) serves hud-fmr-2027; release-fallback manifest.json also 200.

## Smoke (no server restart)

Live server untouched. dataset-mcp fetches catalog + manifest at runtime with a 10-minute cache, so no restart is needed. Fresh local `node index.js` instance against the same live URLs:

- list_datasets: 7 datasets, hud-fmr-2027 full_query available (51,871 rows).
- get_dataset_info("hud-fmr-2027"): catalog entry merged with manifest, default_file hud-fmr-by-zip-2027.csv, 4 files, sha256 3f94c5e98da5.
- query_dataset(state=TX, limit 2): 51,871 rows, 3,244 matched, sha256 verified.

Running MCP clients pick up the entry on their next catalog refresh (10-min TTL).
