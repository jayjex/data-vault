# OSM ETL #4 — EU civic amenities (Berlin, Amsterdam, Paris, Madrid, Warsaw)

Date: 2026-09-10. Status: SHIPPED (pushed, live-verified).

## Data
- Query: Overpass `area(3600000000+rel_id)->.a; node["amenity"="X"](area.a); out count;` for amenity=drinking_water, amenity=public_bookcase, amenity=bicycle_repair_station. Area-filtered via Nominatim admin relations: Berlin R62422, Amsterdam R271110, Paris R71525, Madrid R5326784, Warsaw R336075 (area IDs = rel_id + 3,600,000,000).
- Results (15 pairs, 4,669 nodes): Berlin 265/114/71, Amsterdam 540/0/4, Paris 1045/165/52, Madrid 2058/9/3, Warsaw 122/33/188 (water/bookcases/bike-repair).
- Totals: drinking water 4,030, bookcases 321, bike repair 318. Madrid fountains 2,058 > other four combined; Warsaw repair stands 188 > other four combined; Amsterdam zero public_bookcase (tag never caught on, noted honestly on page).
- Files: data/osm-eu-civic/eu-civic-amenities.csv (full, free, 4 columns incl. verbatim osm_license), sample.csv (same table), sample.json (15 records).

## Infrastructure notes
- overpass-api.de refused connections from this network for the whole session (connection-level, HTTP 000); kumi.systems mirror served all 15 counts (base snapshot 2026-05-31). Heavy rate limiting early; paced retries fixed it.
- First run used wrong area IDs (rel_id + 360,000,000) → returned 0 for several cities; caught by Berlin fountain 0 vs 374 fountain-tag sanity check, rerun with 3,600,000,000 offset.
- First fountain pass used amenity=fountain (374/69/180/245/139); reran as amenity=drinking_water to match the US/Asia lane query shape for cross-table comparability. drinking_water ≠ fountain counts (Berlin 265 vs 374); page documents the exact tag.

## Site changes
- New page datasets/osm-eu-civic-amenities.html: Dataset JSON-LD (json.loads-validated), ODbL attribution verbatim block, NO PRICE (0 dollar signs grep-checked), cross-links osm-us + osm-asia + eurostat house-prices + eurostat-rents. Tag balance OK, no banned slop words, no self-AI-reference.
- catalog.json: datasets 11 → 12 (osm-eu-civic-amenities inserted after osm-us), re-parse OK.
- sitemap.xml: 141 → 142, lastmod 2026-09-10, minidom valid. Live count checked pre-edit: 141.
- llms.txt: +1 dataset section after osm-us.

## Verify
- Commit: OSM ETL EU push; pushed to main.
- Live 200s: /datasets/osm-eu-civic-amenities.html and /data/osm-eu-civic/eu-civic-amenities.csv verified after Pages deploy.

Untouched: journal.md, STATUS, Getly, sibling state reports. No self-AI-reference in page.
