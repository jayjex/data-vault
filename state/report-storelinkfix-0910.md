# Store link fix — 2026-09-10

Old store `mtmw06l2` (store 09036907) archived. New store live: https://www.getly.store/store/matchbook-labs-mtrfh66f

## What was replaced

- `getly.store/store/mtmw06l2` + `store/matchbook-labs-mtmw06l2` (157 links, 41 files) → `www.getly.store/store/matchbook-labs-mtrfh66f`
- No truncated `store/matchbook"` variants found in repo (printable-engineering-bundle.html had full old slug, now fixed).

## Product links

Republished in new store (26 products) — swapped to new IDs:

| old | new |
|---|---|
| airbnb-...-mtpkvxdf | ...-mtrfuvf3 (12 uses) |
| nfl-betting-...-mtpl017h | ...-mtrfvdt7 (26) |
| superteam-earn-...-mtmy11ny | ...-mtrfumk0 (12) |
| web-scraping-...-mtn8em7k | ...-mtrfwfcd (10) |
| web3-remote-jobs-...-mtp4jzje | ...-mtrfw6qk (1) |

Not in new store (not in sitemap, direct slug 404) → now link to store page:

- `usa-rent-benchmark-...-mtqsf1xm` (~40 uses, HUD FMR pages, catalog.json, llms.txt)
- `case-files-60-detective-logic-puzzles-...-mtqnxm7f` (1 use, free-printables-index.html)

## Files touched

136 tracked files: 132 HTML + catalog.json + llms.txt + README.md + tools/gen-roundup.py (generator script updated too, so regen won't reintroduce stale links). Untouched: state/ reports, journal.

## Verification

- All 6 unique live getly.store URLs in HTML verified HTTP 200 via curl.
- No stale IDs (mtmw06l2/mtpkvxdf/mtpl017h/mtmy11ny/mtn8em7k/mtp4jzje/mtqsf1xm/mtqnxm7f) remain in tracked files.

## Commit

- `99857e3` pushed to main (jayjex/data-vault), 136 files, +287/-287.
