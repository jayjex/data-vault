# World Bank Population, G20 Countries + EU27, 1960-2025 — schema

Source: World Bank API v2, indicator SP.POP.TOTL (Population, total), WDI series,
retrieved 2026-09-10. Source license CC BY 4.0; this pack stays CC BY 4.0.
Entity list: the 19 national G20 members plus the European Union aggregate (ISO3 EUU,
EU27 grouping). Missing-value convention: years where the World Bank reports no value
are dropped from the CSV (none in the 1960-2025 window for these 20 entities).

## g20-population.csv (long format, 1320 rows)
| column | type | meaning |
|---|---|---|
| entity | text | World Bank country name (e.g. "Korea, Rep.", "Turkiye", "European Union") |
| iso3 | text | World Bank ISO3 code (EUU = EU27 aggregate) |
| year | int | observation year, 1960-2025 |
| population | int | total population, persons (SP.POP.TOTL) |

## g20-population-2025.csv (20 rows)
Latest observation per entity, sorted by population descending. All rows are year 2025.

## Normalization
- Values parsed from the API JSON and cast to int; no rounding, no imputation.
- Entity names kept verbatim from the World Bank ("Korea, Rep.", "Turkiye",
  "Russian Federation").
- One row per entity-year; every entity has a full 1960-2025 run (66 values).

## Caveats
- EU27 aggregate (EUU) is not a country; exclude it when summing national members.
- South Africa's series ends at the World Bank's latest WDI update (2025); the
  retrieval date is stamped above.
- 2025 observations reflect World Bank estimates as of the WDI database update of
  2026-07-13 and can be revised.
