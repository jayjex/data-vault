# HUD Fair Market Rents FY2027 by ZIP Code — schema

Source: FY2027 Fair Market Rent ZIP-level file, 51,871 rows parsed from
FY27_FMRs.xlsx plus the FY2027 small-area FMR file (FY27_safmrs.xlsx), rates
effective October 1, 2026. The copy here is byte-identical to the parsed file,
sha256-checked at build time. No new download, no re-derivation, no edits:
every cell matches the source parse. License: public domain (US government
data, HUD FY2027 Fair Market Rent release).

## fmr-by-zip-2027.csv (51,871 rows)
| column | type | meaning |
|---|---|---|
| zip | text | 5-digit ZIP code, leading zeros preserved (3,000 unique ZIPs start with 0) |
| hud_area_code | text | HUD FMR area code (e.g. METRO10180M10180, NCNTY72923N72923) |
| metro | text | `metro` or `nonmetro` flag for the row |
| area_name | text | HUD area name, verbatim, may contain commas (quoted) |
| state | text | two-letter state or territory code, 52 total |
| fmr_0br ... fmr_4br | int | FY2027 fair market rent in dollars for studios through 4 bedrooms |

## Coverage
- 38,601 unique ZIP codes across 51,871 rows: 10,093 ZIPs appear in
  more than one HUD area, because metro and nonmetro coverage split the same
  ZIP between areas. Max rows per single ZIP: 6 (ZIPs 40351, 40601, 40962, 47240, 68823).
- 27,288 metro rows vs 24,583 nonmetro rows; 2,600 distinct
  area codes (649 metro, 1951 nonmetro).
- Largest states by row count: TX 3,244, CA 2,605, PA 2,576, NY 2,397, IL 1,939, then MO 1,908, OH 1,884, IA 1,718, MI 1,556, FL 1,552. The top ten together carry
  21,379 of the 51,871 rows.

## Integrity checks at build time (all pass)
- 51,871 rows, uniform 10 columns, header identical to the FY2026 schema.
- 0 malformed ZIP fields (every value 5 digits).
- 0 empty, zero, or non-numeric FMR cells across 5 bedroom sizes.
- 0 duplicate (zip, hud_area_code) keys.
- 0 rows where fmr_4br < fmr_2br.
- Copy sha256 equals source sha256.

## Distribution reference (2BR)
Min 520 (00669, Aguadilla, PR MSA), p25 1020, median
1190, p75 1590, max 5260 (95060,
Santa Cruz-Watsonville, CA MSA). State-level 2BR medians run from California 2600
down to Puerto Rico 610.

## Caveats
- Multi-area ZIPs are HUD's design, not duplication: one ZIP can carry both a
  metro and a nonmetro row, or split between small-area county groups. Dedup
  on (zip, hud_area_code) or filter on `metro` before per-ZIP lookups.
- ZIP rows are small-area FMRs where HUD publishes them and metro/nonmetro
  area rents elsewhere; the `metro` flag tells you which. Rows of one area
  share the same rent values.
- HUD can revise FY2027 rents mid-cycle; the FY2026 file stays the baseline
  for anything dated before October 1, 2026.
