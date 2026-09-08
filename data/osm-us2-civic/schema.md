# Schema — OpenStreetMap Civic Amenities, New York-Chicago-Seattle, 2026-09

Node/way/relation counts for three civic amenity types in New York City, Chicago, and Seattle. Counted with the Overpass API (maps.mail.ru mirror, keyless, base timestamp 2026-09-08T21:00:20Z), `out count` queries per city per amenity, 2026-09-10. City areas are exact administrative relations verified through the OSM API 0.6 tags (name, boundary, admin_level, population), then passed to Overpass as 3600000000-offset area IDs: New York City R175905 (City of New York, admin_level 5, area 3600175905), Chicago R122604 (City of Chicago, admin_level 8, area 3600122604), Seattle R237385 (City of Seattle, admin_level 8, place=city, area 3600237385).

## Columns

- `city` — city name, one of New York City, Chicago, Seattle
- `theme` — amenity type, one of `drinking water` (amenity=drinking_water), `public toilets` (amenity=toilets), `benches` (amenity=bench)
- `count` — number of OpenStreetMap features (nodes + ways + relations) carrying that amenity tag inside the city boundary
- `osm_license` — ODbL license line, verbatim per row

## Overpass query form

```
[out:json][timeout:120];
area(3600175905)->.a;
nwr["amenity"="drinking_water"](area.a); out count;
nwr["amenity"="toilets"](area.a); out count;
nwr["amenity"="bench"](area.a); out count;
```

## Boundary verification

The batch brief suggested R2552842 (New York), R129221 (Chicago), and R858925 (Seattle). All three failed OSM API tag verification and were discarded:

- R2552842 — Лозинська сільська рада, a historic boundary of a village council in Ukraine.
- R129221 — Dunkerton, Iowa, an admin_level 8 city of 842 people.
- R858925 — no tags returned.

The relations above were resolved by Nominatim search and re-verified against OSM API tags (boundary=administrative, admin_level, official_name "City of New York", Wikidata Q60/Q1297/Q5083, populations 8,467,513 / 2,746,388 / 737,015).

## Example features

- New York City: drinking water node 765239335 (Riverbank State Park), toilets node 5148538491 (operator NYC Parks), bench node 3906837660 (Andrew Haswell Green Bench).
- Chicago: drinking water node 3744841486 (Vienna Drinking Fountain, Hans Muhr), toilets node 13283985947 and way 163779333 (Hamlin Comfort Station, both operator Chicago Park District), bench node 4410755216 (C-Bench).
- Seattle: drinking water node 419519151 (fountain=bubbler, unnamed), toilets node 632283737 (Miller Community Center, operator Seattle Parks and Recreation, wheelchair=yes), bench node 1950322167 (Anthony Q. Harris Memorial Bench).

## Mirror cross-check

A parallel count run on the overpass-api.de mirror (base timestamps 2026-09-08T21:00:20Z to 21:02:20Z) matched all 9 of 9 numbers exactly: New York 1531/774/18991, Chicago 252/301/1905, Seattle 193/231/3446.

## Caveats

- Counts include nodes, ways, and relations (`nwr`), since fountains attach to ways, toilet facilities are often mapped as building ways, and one New York bench is a relation.
- Overpass mirror base timestamp 2026-09-08T21:00:20Z (maps.mail.ru); counts are a snapshot, OSM moves daily.
- New York's bench count (18,991) leads the whole series; park benches in NYC are mapped densely, and the count includes park, transit, and street seats. Comparisons across cities still reflect mapping effort as much as ground truth.
- Chicago toilets skew toward Chicago Park District comfort stations mapped as building ways; Seattle toilet nodes carry wheelchair and changing-table attributes from Parks and Recreation surveys.
- This dataset covers the same three cities as the earlier US civic amenities dataset (data/osm-civic, bounding-box counts of drinking water, public bookcases, and bicycle repair stations); the query shape, themes, and boundaries differ, so the tables do not merge row for row.
