# eurostat-unemployment-monthly / unemployment-rate-monthly.csv

Monthly harmonised unemployment rates from Eurostat table `une_rt_m` ("Unemployment by sex and age - monthly data"), pulled 2026-09-10 via the dissemination API (JSON-stat 2.0, keyless). Seasonally adjusted (s_adj `SA`), unit `PC_ACT` = percentage of the labour force (ILO definition), age band `TOTAL` (16 to 74 years). 7,641 rows. Monthly companion to the annual pack in `data/eurostat/unemployment/` (une_rt_a).

## Coverage
- Geos (9): EU-27 aggregate and 8 countries: DE, EL, ES, FR, IT, NL, PL, SE. The euro area aggregate (EA20) is absent from une_rt_m on the API - the request returns an empty cube - so it appears only in the annual dataset.
- Sex (3): T (Total), F (Females), M (Males)
- Months: 2003-01 through 2026-07 (283 months). Complete grid: 9 geos x 283 months x 3 sexes = 7,641 rows, no gaps.
- Source dataset last updated 2026-09-04.

## Columns
- `month` — reference month, `YYYY-MM`, 2003-01 to 2026-07
- `geo` — `EU27` or ISO 2-letter country code (EU27_2020 renamed to EU27 as in the other eurostat-* tables here)
- `sex` — T / F / M
- `age` — always `TOTAL` (the 16-74 age band); kept as a column so the file joins 1:1 with the annual CSV's schema
- `value` — unemployment rate, percent of the labour force, seasonally adjusted
- `geo_label` — Eurostat's label for the geo code
- `sex_label` — Total / Females / Males
- `age_label` — Eurostat's label for the age band

## Reading the numbers
- Latest month (2026-07, total): EU-27 6.1%, Spain 10.0% highest of the nine geos, Poland 3.4% lowest. Females above males in 6 of 9 geos that month (EU27 6.3 vs 5.9).
- Extremes in the file: Greece total 28.3% in 2013-07 is the max; the floor is 2.4%. Spain's peak came earlier (26.4% in 2013-02), Poland's in 2003-08 (20.0%).
- EU-27 trend: 9.8% in 2003-01, crisis peak 11.7% in 2013-05, 6.1% in 2026-07.
- Sanity range used at build: all values within 0-40 (SA monthly rates stay well inside; the annual pack's youth columns are the ones that exceed it).

## Caveats
- Seasonally adjusted (`SA`) only. Eurostat also publishes non-adjusted (`NSA`) and trend-cycle (`TC`) series in this table; this CSV carries the SA slice so months compare directly.
- LFS harmonised series; member-state definitions follow the ILO standard, so cross-country comparisons are Eurostat-consistent, not survey-identical.
- The last monthly figures get revised by member states; a rerun of the ETL a month later can shift the 2026 values slightly.
- Break-in-series (b) and low-reliability (u) flags exist in Eurostat's TSV export but JSON-stat carries bare numbers, so this CSV has no flag column. Flag detail on the databrowser page for une_rt_m.
- une_rt_m codes the total age band `TOTAL` (16-74) while the annual headline is `Y15-74`; both are the working-age total under the ILO definition, labelled differently by the source.
