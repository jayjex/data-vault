# osm-africa-civic / africa-civic-amenities.csv

Node/way counts for three civic amenity types in Lagos, Nairobi, and Addis Ababa. Counted with the Overpass API (maps.mail.ru mirror, keyless, base timestamp 2026-09-08T19:24:39Z), `out count` queries per city per amenity, 2026-09-10. City areas resolved via Nominatim relations, passed to Overpass as 3600000000-offset area IDs: Lagos R3718182 (Lagos State, area 3603718182), Nairobi R3492709 (Nairobi County, area 3603492709), Addis Ababa R1707699 (city-state administration, area 3601707699).

## Columns
- `city` — Lagos (Nigeria), Nairobi (Kenya), or Addis Ababa (Ethiopia); admin-boundary areas, not loose metro matches
- `theme` — `water fountains` (amenity=drinking_water), `public bookcases` (amenity=public_bookcase), or `bike repair stations` (amenity=bicycle_repair_station)
- `count` — features carrying that amenity tag inside the city area (nodes + ways)
- `osm_license` — Overpass copyright line, verbatim per row

## Boundary notes
- Nominatim's top "Lagos" hit is a city place node (27565124); the area-filtered counts use Lagos State R3718182 (admin_level 4), whose built-up core matches the city. Nairobi County is R3492709 (admin_level 4) and covers the whole county, not the old city council boundary. Addis Ababa is a chartered city, so its R1707699 administration is the city itself.
- All three relations carry Overpass areas directly (no district-child fallback needed, unlike Mumbai in the MENA batch).

## Example nodes
- Lagos drinking_water: Clean Water (node 7376214198, 6.494245, 3.3885316) and a second Clean Water tap (node 7376214199, 6.4953821, 3.3881906). Most Lagos fountains sit in one branded "Clean Water" cluster around 6.494-6.495 N, 3.388 E.
- Nairobi drinking_water: Kibera Water & Sanitation Project (node 612007474, -1.3122261, 36.790174); unnamed tap (node 612007432, -1.3081789, 36.7859978). The bulk of the 2,174 are unnamed tap points, with a dense Kibera cluster around -1.31, 36.79.
- Nairobi bicycle_repair_station: gitonga bicycle services (node 12243521973, -1.3111768, 36.8686335) — the county's only mapped stand, a bike shop.
- Addis Ababa drinking_water: Esa bling (node 6665462785, 8.8386084, 38.818319); Minch water filters (node 10800986807, 8.9584987, 38.7314722). Only 5 drinking-water features exist in the whole city.

## Cross-checks
- A parallel count run on the kumi.systems mirror (base timestamp 2026-05-06, four months staler) matched 8 of 9 numbers exactly: Lagos 60/0/0 and Addis 5/0/0 identical, Nairobi bicycle_repair_station 1. Nairobi drinking_water was 2,173 on the staler base vs 2,174 here — one edit in the gap between the two mirrors.

## Caveats
- Overpass mirror base timestamp 2026-09-08T19:24:39Z (maps.mail.ru) — counts are a snapshot, OSM moves daily.
- Nodes + ways counted; relations ignored (none exist for these tags in the three areas).
- Zero bookcase and repair-stand counts are real results: no public_bookcase is mapped anywhere in the three boundaries, and bicycle_repair_station appears only once (Nairobi).
- All three boundaries are admin_level 4 units that reach past the built-up core (Lagos State includes Epe, Ikorodu, and Badagry; Nairobi County covers the full pre-2010 county), so counts are province-wide rather than downtown-only.
- Nairobi's 2,174 is the largest single-city drinking-water count in the catalog's OSM civic series (Tokyo 2,163, Madrid 2,058), driven by community water-point mapping projects rather than decorative fountains.
