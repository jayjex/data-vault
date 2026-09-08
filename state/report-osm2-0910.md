# OSM ETL #2 — US civic amenities (NYC, LA, Chicago, Austin, Seattle)

Date: 2026-09-10. Status: SHIPPED (pushed, live-verified).

## Data
- Query: Overpass `nwr(bbox)[amenity=X]; out count;` for amenity=drinking_water, amenity=public_bookcase, amenity=bicycle_repair_station over city bounding boxes.
- Results (15 pairs, 4,000 elements): NYC 1599/221/31, LA 450/148/44, Chicago 298/103/40, Austin 265/35/28, Seattle 213/497/28 (water/bookcases/bike-repair).
- Totals: water fountains 2,825, bookcases 1,004, bike repair 171. Seattle bookcases 497 = ~half the five-city total; NYC fountains 1,599 = more than other four combined.
- Files: data/osm-civic/us-civic-amenities.csv (full, free), sample.csv, sample.json.

## Infrastructure notes
- overpass-api.de main instance refused connections from this network at start; kumi.systems mirror served most counts (base snapshot 2026-05-31), main instance recovered later and served Seattle bike-repair (28) + first Seattle/bookcase-LA retries. Heavy rate limiting: several retries with sleeps. osm.ch returned suspicious 0 for Seattle → not trusted, discarded.
- Bounding boxes used (not Nominatim relation areas): NYC 40.49,-74.27,40.92,-73.68; LA 33.70,-118.67,34.34,-118.16; Chicago 41.64,-87.94,42.02,-87.52; Austin 30.10,-97.94,30.63,-97.52; Seattle 47.48,-122.46,47.74,-122.22.

## Site changes
- New page datasets/osm-us-civic-amenities.html: Dataset JSON-LD (json.loads-validated), ODbL attribution verbatim block, NO PRICE (0 dollar signs), cross-links osm-asia + eurostat house-prices/rents. Tag balance OK, no banned slop words.
- Asia page (OSM ETL #3, already committed by sibling) links back to this page; link now resolves.
- catalog.json: datasets 10 → 11 (osm-us-civic-amenities inserted after osm-asia), re-parse OK.
- sitemap.xml: 140 → 141 (race resolved: OSM ETL #3 committed Asia mid-flight; stash -u + pull --rebase brought it in, then bumped). Live check pre-edit: 139 (Pages hadn't redeployed Asia yet).
- llms.txt: +1 dataset section.

## Verify
- Commit: OSM ETL US push; pushed to main.
- Live 200s: /datasets/osm-us-civic-amenities.html and /data/osm-civic/us-civic-amenities.csv verified after Pages deploy.

Untouched: journal.md, STATUS, Getly, openstreetmap-etl EU files. No self-AI-reference in page.
