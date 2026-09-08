# eurostat-unemployment / unemployment-rate.csv

Annual harmonised unemployment rates from Eurostat table `une_rt_a` ("Unemployment by sex and age - annual data"), pulled 2026-09-10 via the dissemination API (JSON-stat 2.0, keyless). One unit slice: `PC_ACT` = percentage of the labour force (ILO definition). 3,768 rows.

## Coverage
- Geos (10): EU-27 aggregate, euro area EA20, and 8 countries: DE, EL, ES, FR, IT, NL, PL, SE
- Sex (3): T (Total), F (Females), M (Males)
- Age (7): Y15-74 (headline), Y15-24, Y15-29, Y20-64, Y25-54, Y25-74, Y55-74
- Years: 2003-2025. Not every combination exists - aggregates (EU27/EA20) start 2005, NL starts 2009, some series break in later. Missing cells are simply absent rows.
- Source dataset last updated 2026-06-11.

## Columns
- `year` — reference year, 2003-2025
- `geo` — `EU27`, `EA20`, or ISO 2-letter country code (EU27_2020 renamed to EU27 as in the other eurostat-* tables here)
- `sex` — T / F / M
- `age` — age band code
- `value` — unemployment rate, percent of the labour force
- `geo_label` — Eurostat's label for the geo code
- `sex_label` — Total / Females / Males
- `age_label` — Eurostat's label for the age band

## Reading the numbers
- 2025 headline (Y15-74, Total): EU-27 6.0%, euro area 6.4%; Spain 10.5% highest of the eight countries, Poland 3.1% lowest. NL 3.9% (was 8.2% in 2013).
- Extremes in the file: Greece youth (Y15-24) 64.6% in 2013 is the max overall; the floor is 1.5% (male Y55-74 rates in tight markets).
- Sanity ranges used at build: total Y15-74 within 0-40, all bands within 0-70 (youth crisis rates legitimately exceed 40).

## Caveats
- LFS harmonised series; member-state definitions follow the ILO standard, so cross-country comparisons are Eurostat-consistent, not survey-identical.
- Annual data is not seasonally adjusted (annual rates don't need it).
- Break-in-series (b) and low-reliability (u) flags exist in Eurostat's TSV export but JSON-stat carries bare numbers, so this CSV has no flag column. Full flag detail on the databrowser page for une_rt_a.
- EU27/EA20 aggregates start 2005 because they are built from national series that all need to exist.
- Youngest band Y15-24 for a few countries in early years is missing for the same reason.
