# HUD Fair Market Rents FY2027, Top-50 Metro Areas — schema

Source: FY2027 Fair Market Rent ZIP-level file (51,871 ZIP rows parsed from
FY27_FMRs.xlsx plus the FY2027 small-area FMR file, effective October 1, 2026),
already published in the hud-fmr-2027 pack. The metro rows here are recomputed
from that file, not copied from any HUD summary. No new download. License:
public domain (US government data). The full FY2027 FMR list has 649 metro FMR
areas; this pack keeps the 50 with the most ZIP codes, which together cover
10,143 of the 27,288 metro-assigned ZIPs.

## fmr-metro-2027.csv (50 rows)
| column | type | meaning |
|---|---|---|
| metro_code | text | HUD metro FMR area code (e.g. METRO35620MM5600) |
| metro_name | text | HUD area name, verbatim (e.g. "New York, NY HUD Metro FMR Area") |
| state | text | two-letter state or territory code |
| zip_count | int | FY2027 ZIP rows inside the area |
| fmr_0br_median ... fmr_4br_median | int | median FY2027 FMR in dollars across the area's ZIPs, per bedroom size |

## Selection and aggregation
- Rows with the ZIP-level `metro` flag only; nonmetro and county-level
  small-area rows are excluded.
- One area = one hud_area_code. Each code has exactly one name and one state
  in the source file, checked at build time (asserted).
- Per area and bedroom size, the value is the integer median of the ZIP FMRs
  (statistics.median of ints; when the ZIP count is even the two middle values
  are averaged then floored by int()). Areas are ranked by zip_count
  descending, tie-broken by metro_code, and the top 50 are kept.

## most-expensive-2br.csv (50 rows)
Same columns. The 50 areas with the highest fmr_2br_median across all 649
metro areas, sorted by fmr_2br_median descending, tie-broken by metro_code.
Only 12 of these 50 overlap with the ZIP-coverage top 50, so the two files
answer different questions.

## Caveats
- The aggregate is a median across the area's ZIPs, which weights every ZIP
  equally. It is not a ZIP-count-weighted average and not the official 40th
  percentile FMR HUD publishes at the area level.
- Puerto Rico areas (state PR) are in the source and were eligible for both
  rankings; none made the ZIP-coverage top 50.
- Rates are effective October 1, 2026 and reflect the FY2027 files HUD
  published in 2026; HUD can revise them mid-cycle.
