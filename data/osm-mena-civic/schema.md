# osm-mena-civic / mena-civic-amenities.csv

Node/way counts for three civic amenity types in Istanbul, Cairo, and Mumbai. Counted with the Overpass API (kumi.systems mirror, keyless), `out count` queries per city per amenity, 2026-09-10. City areas resolved via Nominatim relations, passed to Overpass as 3600000000-offset area IDs: Istanbul R223474 (İstanbul province, area 3600223474), Cairo R5466227 (Cairo Governorate, area 3605466227), Mumbai R7964375 + R7964376 (Mumbai Suburban District + Mumbai City District, areas 3607964375/3607964376).

## Columns
- `city` — Istanbul (Türkiye), Cairo (Egypt), or Mumbai (India); admin-boundary areas, not loose metro matches
- `theme` — `water fountains` (amenity=drinking_water), `public bookcases` (amenity=public_bookcase), or `bike repair stations` (amenity=bicycle_repair_station)
- `count` — features carrying that amenity tag inside the city area (nodes + ways)
- `osm_license` — Overpass copyright line, verbatim per row

## Boundary notes
- Task-suggested relation IDs R147965 (Istanbul), R192754 (Cairo), R288498 (Mumbai) all resolve to nothing in Nominatim. Verified replacements: Istanbul province is R223474 (admin_level 4), Cairo Governorate is R5466227 (admin_level 4), and Mumbai's city=relation R16173235 has no Overpass area, so counts use its two admin_level 5 district children (Mumbai Suburban R7964375, Mumbai City R7964376).
- Mumbai district totals cross-checked against a bbox count over the same ground: 71 drinking_water features in-bbox vs 67 in-area (bbox clips the harbor edge differently); bicycle_repair_station 3 in both.

## Example nodes
- Istanbul drinking_water: Siyavuşpaşa Çeşmesi (node 1026153699, 41.00094, 28.85205); Hatice Turhan Valide Sultan Çeşmesi (node 5221026261, 41.01596, 28.97298). Historic Ottoman fountains dominate the tag.
- Istanbul public_bookcase: one unnamed way (1063574471, 41.01081, 29.19228, Kadıköy side).
- Istanbul bicycle_repair_station: Yusuf Bisiklet (node 5300958421, 40.93658, 29.21433); Bike City (node 6961577861, 41.01809, 28.58917).
- Cairo drinking_water: شركة مياة الشرب (node 5129741229, 30.05361, 31.33394); فروت ستار (node 5735366721, 30.10098, 31.37579). No public_bookcase or bicycle_repair_station mapped anywhere in the governorate.
- Mumbai drinking_water: Durgadevi Saraf Pyau (node 12293013067, 19.06276, 72.90085); Ghanshyamdas Saraf Pyau (node 12298863511, 19.04035, 72.84696). The W1-W27 cluster sits around one building at 19.133, 72.915.
- Mumbai bicycle_repair_station: Sagar Cycle repair shop (node 6801919187, 19.12599, 72.91887); Welcome cycle mart (node 11445752109, 19.08554, 72.88265).

## Caveats
- Overpass mirror base timestamp 2026-07-28 (kumi.systems) — counts are a snapshot, OSM moves daily.
- Nodes + ways counted; relations ignored (none exist for these tags in the three areas).
- Cairo bookcase/repair counts of 0 are real results: nobody has mapped those amenities inside the Cairo Governorate boundary yet.
- Istanbul counts cover the full province, which reaches well past the built-up city into rural Marmara and Black Sea districts; its fountain count benefits from historic-fountain mapping enthusiasm.
