# World Bank Rural Population Share, G20 Countries + EU27, 1960-2025 — schema

Source: World Bank API v2, indicator SP.RUR.TOTL.ZS (Rural population, % of total
population), WDI series, retrieved 2026-09-10. Source license CC BY 4.0; this pack
stays CC BY 4.0. Entity list: the 19 national G20 members plus the European Union
aggregate (ISO3 EUU, EU27 grouping), same as the SP.POP.TOTL sibling pack.
Missing-value convention: years where the World Bank reports no value are dropped
from the CSV (none in the 1960-2025 window for these 20 entities).

## g20-rural-population.csv (long format, 1320 rows)
| column | type | meaning |
|---|---|---|
| entity | text | World Bank country name (e.g. "Korea, Rep.", "Turkiye", "European Union") |
| iso3 | text | World Bank ISO3 code (EUU = EU27 aggregate) |
| year | int | observation year, 1960-2025 |
| rural_pct | float | rural population as percent of total population (SP.RUR.TOTL.ZS), verbatim API precision, not rounded |

## g20-rural-2025.csv (20 rows)
Latest observation per entity, sorted by rural share descending. All rows are year 2025.

## Normalization
- Values parsed from the API JSON and kept as floats at the API's own precision;
  no rounding, no imputation. Percent shares, not absolute counts.
- Entity names kept verbatim from the World Bank ("Korea, Rep.", "Turkiye",
  "Russian Federation").
- One row per entity-year; every entity has a full 1960-2025 run (66 values).

## Caveats
- The indicator is a share of total population. To get rural headcounts, multiply
  by SP.POP.TOTL (available in the sibling worldbank-g20-population pack).
- The World Bank defines "rural" per each country's own census definition, so the
  threshold is not harmonized across countries; comparisons are directionally
  solid, single-point differences between countries are not.
- EU27 aggregate (EUU) is not a country; exclude it when averaging national members.
- 2025 observations reflect the WDI database update of 2026-07-13 and can be revised.
