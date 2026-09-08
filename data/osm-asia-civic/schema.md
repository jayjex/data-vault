# osm-asia-civic / counts-2026-09.csv

Node counts for three civic amenity types in Tokyo, Jakarta, Seoul. Counted with Overpass API (kumi.systems + maps.mail.ru mirrors), `out count` queries per city per amenity, 2026-09-10. City areas resolved via Nominatim relation IDs: Tokyo R3601543125 (Tokyo Metropolis, area 3601543125), Jakarta R6362934 (Daerah Khusus Ibukota Jakarta, area 3606362934), Seoul R2297418 (Seoul Special City, area 3602297418).

## Columns
- `city` — Tokyo, Jakarta, or Seoul (admin area, not metro-area loose matches)
- `amenity` — `drinking_water`, `public_bookcase`, or `bicycle_repair_station`
- `total` — node count in the city area (ways/relations ignored)
- `tags` — example `name` tag from a real node in that city+amenity (empty = unnamed nodes)
- `lat`, `lon` — example node coordinates (Jakarta public_bookcase row: city center placeholder, count is 0 so no node exists)
- `source` — data origin

## Caveats
- Overpass mirror base timestamps 2026-07-24 (kumi) — counts are a snapshot, OSM moves daily.
- Nodes only. Some amenities are mapped as ways (rare for these three tags).
- Jakarta public_bookcase = 0 is a real result: nobody has mapped one yet in the Jakarta relation boundary.
