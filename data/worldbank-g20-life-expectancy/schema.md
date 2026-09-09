# World Bank Life Expectancy, G20 Countries + EU27, 1960-2024 — schema

Source: World Bank API v2, indicator SP.DYN.LE00.IN (Life expectancy at birth, total
years), WDI series, retrieved 2026-09-10. Source license CC BY 4.0; this pack stays
CC BY 4.0. Entity list: the 19 national G20 members plus the European Union aggregate
(ISO3 EUU, EU27 grouping), same as the SP.POP.TOTL and SP.RUR.TOTL.ZS sibling packs.
Missing-value convention: years where the World Bank reports no value are dropped
from the CSV. The WDI series for these 20 entities runs 1960-2024 (no 2025 value
published yet), 65 observations per entity, 1,300 rows total.

## g20-life-expectancy.csv (long format, 1300 rows)
| column | type | meaning |
|---|---|---|
| entity | text | World Bank country name (e.g. "Korea, Rep.", "Turkiye", "European Union") |
| iso3 | text | World Bank ISO3 code (EUU = EU27 aggregate) |
| year | int | observation year, 1960-2024 |
| life_expectancy_years | float | life expectancy at birth in years (SP.DYN.LE00.IN), rounded to 2 decimals from the API's full precision |

## g20-life-expectancy-2024.csv (20 rows)
Latest observation per entity, sorted by life expectancy descending. All rows are
year 2024.

## Normalization
- Values parsed from the API JSON and rounded to 2 decimal places; the underlying
  WDI series itself is an annual estimate, so the two decimals carry no extra
  precision. No imputation; gaps would be dropped, and none occur in this window.
- Entity names kept verbatim from the World Bank ("Korea, Rep.", "Turkiye",
  "Russian Federation").
- One row per entity-year; every entity has a full 1960-2024 run (65 values).

## Caveats
- The series runs through 2024, not 2025: WDI publishes life expectancy with a
  longer lag than the population counts, and no 2025 value existed at retrieval.
- SP.DYN.LE00.IN is the total-population (both sexes) series. The World Bank also
  publishes SP.DYN.LE00.FE.IN and SP.DYN.LE00.MA.IN separately; those are not in
  this pack.
- The 2020-2021 rows carry the COVID-19 mortality shock in most members; year-over
  -year comparisons across that window are not comparable to normal years.
- EU27 aggregate (EUU) is not a country; exclude it when ranking national members.
- 2024 observations reflect the WDI database update of 2026-07-13 and can be revised.
