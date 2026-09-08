# osm-oceania-civic / oceania-civic-amenities.csv

Node/way counts for three civic amenity types in Sydney, Melbourne, and Auckland. Counted with the Overpass API (maps.mail.ru mirror, keyless, base timestamp 2026-09-08T20:07:04Z), `out count` queries per city per amenity, 2026-09-10. City areas resolved via Nominatim relations, passed to Overpass as 3600000000-offset area IDs: Sydney R5750005 (area 3605750005), Melbourne R2404870 (City of Melbourne, area 3602404870), Auckland R2094141 (area 3602094141).

## Columns
- `city` — Sydney (NSW, Australia), Melbourne (VIC, Australia), or Auckland (New Zealand); admin-boundary areas, not loose metro matches
- `theme` — `drinking water` (amenity=drinking_water), `public toilets` (amenity=toilets), or `benches` (amenity=bench)
- `count` — features carrying that amenity tag inside the city area (nodes + ways)
- `osm_license` — Overpass copyright line, verbatim per row

## Boundary notes
- Sydney R5750005 is the OSM `place=city` boundary relation for the metropolitan area (population tag 5,219,674), not the much smaller Council of the City of Sydney local-government area (R1251066). Nominatim's top "Sydney" hit is this same R5750005, so the metro boundary is what the counts cover.
- Melbourne uses R2404870, the City of Melbourne local government area (admin_level 6, ~37 km² core municipality). It does not reach the outer suburbs, so Melbourne counts cover the CBD and inner city only (the lowest per-city counts in this table are a boundary artifact as much as a mapping gap).
- Auckland R2094141 is the Auckland unitary authority (admin_level 4), covering the whole Auckland region including rural north and south.
- An earlier task brief suggested Sydney R7003490; that relation is a suburb in Rzeszów, Poland (Baranówka), discarded after verification. All three boundaries here were re-verified through the OSM API before counting.

## Example nodes
- Sydney toilets: Public Toilet Cook Park (node 15179265, Bayside Council operator, changing table, wheelchair designated). Sydney's toilet mapping is dense and attributes operators (city councils keep the data current), and many nodes link to the national toilet map (toiletmap.gov.au).
- Sydney drinking_water: unnamed `tap` nodes dominate (node 2135532822, node 2144956494); a dog fountain is tagged `tap (for dogs)` (node 2178006854).
- Sydney bench: Mrs Macquarie's Chair (node 13887214, the famous harbour-headland bench); bus-stop style names like Ben Boyd Rd at Yeo St (node 512739556).
- Melbourne drinking_water: Temperance Fountain (node 2975190811) and the Samuel Maucer memorial drinking fountain (node 6014207961), heritage fountains and a Melbourne specialty.
- Melbourne toilets: Toilet 124 (node 305075011) and Public Urinals (node 368131639).
- Auckland drinking_water: St Heliers Memorial Fountain (node 2061341156), Collins Drinking Fountain (node 2611965390), Waiariki (node 7998091383, te reo Māori for warm spring).
- Auckland toilets: Cornwall Park Archery (node 1357198229); Auckland also maps toilets as ways, e.g. Kohimarama Beach Changing Rooms and Toilets (way 128209733).

## Cross-checks
- A parallel count run on the overpass-api.de mirror (base timestamp 2026-09-08T20:19:04Z) matched all 9 of 9 numbers exactly: Sydney 2479/2501/13573, Melbourne 355/142/1845, Auckland 428/992/4916.
- A third run on overpass.kumi.systems was abandoned: the mirror throttled heavily (timeouts on most calls) and its area store was months stale (a naive Sydney bench query on kumi returned 0, refuted immediately by the other two mirrors).

## Caveats
- Overpass mirror base timestamp 2026-09-08T20:07:04Z (maps.mail.ru); counts are a snapshot, OSM moves daily.
- Nodes + ways counted; relations ignored (none exist for these tags in the three areas).
- Melbourne's small counts reflect the City of Melbourne municipal boundary (37 km²), not greater Melbourne. Per-area density comparisons with Sydney (metro) and Auckland (unitary) need that asymmetry in mind.
- Bench counts sit on a different scale than the bookcase/repair-station themes of earlier batches: benches are one of the most-mapped amenities in OSM at all (Sydney 13,573 is the largest single count in the catalog's OSM civic series), so cross-region comparisons should stay within a theme.
- The three boundaries differ in kind (metro place boundary, LGA, unitary authority), chosen per city for what "the city" means locally; all three are relation-level areas with full Overpass area support.
