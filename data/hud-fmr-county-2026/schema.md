# schema.md — HUD FMR FY2026 by County: completeness & spread

Source: US Department of Housing and Urban Development, FY2026 Fair Market Rent
release, county-level file (one row per county equivalent). US government data,
public domain. Pulled and parsed 2026-09-10.

## Files

- `fmr-county-2026.csv` — full copy, 3,229 rows, verbatim source columns (see below).
- `spread-counties.csv` — the 8 counties where `fmr_2br_max` > `fmr_2br_median`, with derived `gap_2br`, `gap_pct_2br`.
- `sample.csv` / `sample.json` — first 22 rows, verbatim.

## Columns (fmr-county-2026.csv)

| column | meaning |
|---|---|
| state | 2-letter USPS code (52 values incl. DC, PR, GU, VI, AS, MP) |
| state_name | full state/territory name |
| county | county or county-equivalent name |
| metro | `metro` (1,253 rows) or `nonmetro` (1,976 rows) |
| fmr_0br_median .. fmr_4br_median | HUD county median FMR in USD for that bedroom size |
| fmr_0br_max .. fmr_4br_max | HUD county maximum FMR in USD for that bedroom size |
| area_rows | number of FMR area rows the county covers in HUD's raw ZIP-level file (1 = the whole county is one FMR area) |

## Coverage

- 3,229 county-equivalents across 56 states/territories. CA 58, TX 254 counties; AS and MP contribute 1 each.
- 0 empty cells in any rent column. Every county has all five bedroom sizes, median and max.
- No duplicate state+county pairs.

## Derivation notes / caveats

- All numbers come from the source file. `gap_2br` and `gap_pct_2br` in
  spread-counties.csv are computed as `fmr_2br_max - fmr_2br_median` and the
  percentage equivalent; nothing else is derived.
- When `area_rows = 1`, HUD publishes a single rent per bedroom size for the
  county, so max equals median. 3,221 of 3,229 counties are in this case.
- The 8 exceptions (all `metro`, all in ME/NH/MA/RI) are counties split into
  multiple FMR areas, where HUD publishes a range. Bristol County MA spans the
  widest gap: 2BR median $1,729 vs max $2,550 (+47.5%).
- Median/max here are HUD's county aggregates, not percentiles we computed.
- `area_rows` sums to 4,764 across the file; that is the count of raw HUD area
  lines these 3,229 county rows aggregate. The 67 counties with `area_rows > 1`
  are where HUD keeps separate rent points inside one county.
