# OSM ETL #3 — Asia civic amenities (Tokyo / Jakarta / Seoul) — 2026-09-10

## Result
- Counts (nodes per city boundary, Overpass `out count`):
  - Tokyo: drinking_water 2,163 · public_bookcase 3 · bicycle_repair_station 25
  - Jakarta: drinking_water 38 · public_bookcase 0 · bicycle_repair_station 1
  - Seoul: drinking_water 253 · public_bookcase 1 · bicycle_repair_station 5
  - Total 2,489 nodes. Jakarta bookcase = 0 is a real count, not missing data.
- Files: `data/osm-asia-civic/counts-2026-09.csv` (9 rows, full + free), `sample.csv`, `sample.json`, `schema.md`.
- Page: `datasets/osm-asia-civic-amenities.html` — Dataset JSON-LD (json.loads-validated), ODbL verbatim attribution, 0 dollar signs, cross-links to `osm-us-civic-amenities.html` + `osm-eu-civic-amenities.html` (worker pages, resolve once their pushes land).
- catalog.json 9→10 · sitemap 139→140 (minidom valid) · llms.txt +1 dataset block.

## Method / gotchas
- overpass-api.de TCP-refused from this box. Used keyless mirrors: kumi.systems + maps.mail.ru (base snapshot 2026-07-24). Some `out tags` probes hit dispatcher busy → retry loop.
- Area names alone return dozens of wrong Tokyo areas (stations, parks). Fixed: Nominatim relation lookups, area id = 3600000000 + relation id — Tokyo R1543125, Jakarta R6362934, Seoul R2297418.
- Counts queried in parallel per city; sample rows via `out 5` for the example tags/coords columns.

## Ship
- Commit `1f6ab73` on main (targeted: 8 files, only my lane; no journal/STATUS touched). Pushed 61ef6f8..1f6ab73.
- Live verify (Pages deployed): page/data/catalog/sitemap all 200, live sitemap = 140 urls, live catalog = 10 entries.

## Not done / handoff
- Cross-link targets (US/EU pages) belong to other workers — did not touch their files or sitemap entries.
