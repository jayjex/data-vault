# airbnb-eight-cities: schema and coverage

Inside Airbnb summary listings for 8 US cities not covered by airbnb-six-cities.
Snapshot dates June 2026, pulled from insideairbnb.com get-the-data
(visualisations/listings.csv files), normalized to the same 12-column schema as
airbnb-six-cities. Source data: Inside Airbnb, CC BY 4.0.

## Files

| file | rows | notes |
|---|---|---|
| cities-index.csv | 8 | one row per city: city, snapshot_date, rows, file, median_price_usd, room_type_mix |
| airbnb-boston.csv | 4,414 | Boston, MA, snapshot 2026-06-15 |
| airbnb-chicago.csv | 8,704 | Chicago, IL, snapshot 2026-06-24 |
| airbnb-los-angeles.csv | 43,932 | Los Angeles, CA, snapshot 2026-06-15 |
| airbnb-new-orleans.csv | 7,254 | New Orleans, LA, snapshot 2026-06-16 |
| airbnb-portland.csv | 4,210 | Portland, OR, snapshot 2026-06-15 |
| airbnb-san-francisco.csv | 7,422 | San Francisco, CA, snapshot 2026-06-14 |
| airbnb-seattle.csv | 7,814 | Seattle, WA, snapshot 2026-06-15 |
| airbnb-washington-dc.csv | 6,996 | Washington, DC, snapshot 2026-06-24 |
| sample.csv | 20 | first 20 Boston rows, verbatim from airbnb-boston.csv |
| sample.json | 20 | {slug, name, columns[], row_count, records[]} |

Total: 90,746 rows.

## Columns (12, same order as airbnb-six-cities)

| column | type | notes |
|---|---|---|
| id | int | Inside Airbnb listing id |
| name | text | listing title, verbatim |
| neighbourhood | text | source neighbourhood label (city-specific: Boston/Chicago/DC use neighborhood names, LA/SF use city-defined zones) |
| latitude | float | Inside Airbnb blurs coordinates to roughly the block level; precision varies by row (about 4-7 decimals) |
| longitude | float | same blur as latitude |
| room_type | enum | Entire home/apt, Private room, Hotel room, Shared room |
| price | float | nightly USD, empty when the source has no price |
| minimum_nights | int | |
| availability_365 | int | nights available in the next 365 days at snapshot |
| number_of_reviews | int | lifetime count at snapshot |
| reviews_per_month | float | empty when number_of_reviews = 0 |
| last_review | date | empty when no reviews |

## Normalization from source

Source visualisations/listings.csv carries 19+ columns (host_id, host_profile_id,
host_name, neighbourhood_group, calculated_host_listings_count,
number_of_reviews_ltm, license). This dataset drops all of them: no host fields
ship, matching the six-city pack. Nothing else is edited; prices stay as the
source numbers.

## Coverage notes

- 90,746 listings across 8 cities; the six-city pack has 90,169 across its 6, so the two packs are nearly equal in size.
- Los Angeles is the largest single-city file in either pack (43,932 rows, ahead of New York City's 30,234 in the six-city pack); Portland is the smallest here (4,210).
- Combined nightly median across the 8 cities: USD 226 (price-bearing rows only). City medians: Boston 279, Seattle 281, San Francisco 252, Los Angeles 224, Washington DC 221, Chicago 223, New Orleans 192, Portland 160.
- 11,594 of 90,746 rows (13%) carry no price; medians and mixes above count only price-bearing rows where noted.
- Room mix across 8 cities: Entire home/apt 67,526 (74%), Private room 21,402 (24%), Hotel room 1,371 (2%), Shared room 447 (0%).
- neighbourhood_group was dropped because it is empty for every city in this set.

## Caveats

- Snapshots are point-in-time: counts and prices drift with every Inside Airbnb release. Snapshot dates are per row in cities-index.csv.
- San Francisco's max price (99,999) and several 20,000+ outliers are source artifacts, not edited out.
- neighbourhood labels are not normalized across cities; compare within a city, not across.
- Median, not mean: nightly prices are heavy-tailed; the mean would overstate typical rates.
