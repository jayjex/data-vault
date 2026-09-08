# osm-latam-civic / latam-civic-amenities.csv

Node counts for three civic amenity types in São Paulo, Buenos Aires, and Mexico City. Counted with Overpass API (kumi.systems mirror, keyless), `out count` queries per city per amenity, 2026-09-10. City areas resolved via Nominatim relation IDs: São Paulo R298285 (municipality of São Paulo, area 3600298285), Buenos Aires R3082668 (Ciudad Autónoma de Buenos Aires, area 3600308268), Mexico City R1376330 (Ciudad de México, area 36001376330).

## Columns
- `city` — Sao Paulo, Buenos Aires, or Mexico City (admin area, not metro-area loose matches)
- `theme` — human-readable label: `water fountains` (amenity=drinking_water), `public bookcases` (amenity=public_bookcase), `bike repair stations` (amenity=bicycle_repair_station)
- `count` — node count in the city area (ways/relations ignored)
- `osm_license` — the Overpass response license line, verbatim in every row

## Example nodes (spot-checking, pulled from a 2026-09-08 Overpass query)
- São Paulo drinking_water: "Bebedouro SABESP" at -23.64127, -46.69177
- Buenos Aires drinking_water: "Drinking fountain" at -34.57200, -58.41412
- Buenos Aires public_bookcase: "Biblioteca comunitaria" at -34.67267, -58.46850
- Buenos Aires bicycle_repair_station: "Bicicletería Paraná" at -34.60746, -58.41870
- Mexico City drinking_water: "Tanque Lázaro Cárdenas" at 19.42770, -99.25515
- Mexico City bicycle_repair_station: "Taller de bicis" at 19.41435, -99.16915
- São Paulo public_bookcase: 4 nodes, unnamed (none named in the sample pull)

## Caveats
- Overpass mirror base timestamps ranged 2026-05-06 to 2026-07-24 across the nine queries (kumi serves replicas at different snapshot depths) — counts are a snapshot, OSM moves daily.
- Nodes only. Some amenities are mapped as ways (rare for these three tags).
- Mexico City public_bookcase = 0 is a real result: nobody has mapped one in the Ciudad de México boundary yet.
- Counts are area-filtered on exact administrative boundaries; a bbox would include neighboring municipalities.
