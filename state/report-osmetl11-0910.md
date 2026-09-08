# data-vault ETL batch 11 — World Bank G20 population (2026-09-10)

Lane: data-vault ETL batch 11 (etl11). etl10 (Airbnb 8 cities, commit 19335bf) sudah landed sebelum batch mulai — zero file conflict (beda slug, beda entry catalog; sisa diff working tree milik lane fresto/storelinkfix, tidak disentuh).

## Keputusan kandidat
1. **World Bank SP.POP.TOTL, G20 + EU27** — DIPILIH. Satu call API keyless, 1,320 rows JSON bersih, 20/20 entitas full run 1960-2025, license CC BY 4.0 jelas.
2. OpenFoodFacts category counts — tidak dibutuhkan (kandidat 1 jalan mulus, probe tidak dilakukan).
3. Wikidata SPARQL universities ASEAN — tidak dibutuhkan (alasan sama).

## Dataset baru
`data/worldbank-g20-population/` (1,320 rows long format, 4 kolom, ~39 KB total):
- `g20-population.csv` — long format entity,iso3,year,population; 20 entitas (19 negara G20 + EUU EU27 aggregate) × 66 tahun, values verbatim dari API (int cast saja, no rounding/imputation).
- `g20-population-2025.csv` — 20 rows latest-year per entity, sorted population desc.
- `sample.csv` 20 rows (Argentina 1960-1979) + `sample.json` {slug, name, columns[], row_count, records[]} — sample == long[:20] script-checked.
- `schema.md` — dictionary + normalization + caveats.
- `etl-stats.json` — angka untuk halaman/report (bukan bagian pack publik? ikut ter-commit di folder; ringan).

ETL: `tools/etl-wb-g20-population.py` (stdlib, rerunnable; source JSON disimpan `tmp/etl-wb-g20/wb-pop.json`). Source URL: api.worldbank.org/v2 indicator SP.POP.TOTL, date=1960:2025, per_page=20000, retrieved 2026-09-10, WDI lastupdated 2026-07-13.

## Angka (script-checked)
- 2025: India 1,463,865,525 > China 1,406,585,000; crossover India lewat China di 2021 (dari data sendiri).
- EU27 (EUU) 451,127,411 rank 3; 19 negara nasional sum = 4,744,611,663; Australia terkecil 27,614,411.
- 6/20 entitas sudah lewat puncaknya: RUS 1992, JPN 2010, ITA 2014, KOR 2020, CHN 2021 (1,412,360,000), DEU 2024.
- Growth 1960→2025: Saudi Arabia 15.18x tercepat, lalu South Africa 3.94x, Mexico 3.59x.

## Halaman + indeks
- `datasets/worldbank-g20-population.html`: Dataset JSON-LD (license CC BY 4.0, isAccessibleForFree, 5 DataDownloads, isBasedOn = API URL), tabel 2025 20 rows == g20-population-2025.csv (script-checked), files list ukuran aktual, cross-link eurostat-unemployment + eurostat-house-prices + license guide + portfolio. No-ai-slop skill diaplikasikan (0 banned words, 0 em dash, semua angka dari CSV). No self-AI-reference. No price.
- catalog.json: +entry setelah eurostat-unemployment (20→21 datasets), full_data.status "free" (source CC BY 4.0, no Getly pack).
- sitemap.xml: +1 URL (159→160), disisipkan setelah airbnb-eight-cities, minidom valid, 0 dup.
- llms.txt: +1 dataset section setelah eurostat-unemployment.
- datasets/index.html: +1 section "World Bank series", lead di-update (3 Eurostat tables + 1 World Bank series).
- datasets/eurostat-unemployment.html: +1 cross-link sentence ke halaman baru (btn-note).

## Biaya
$0. Keyless HTTP dari api.worldbank.org, no API berbayar, no Zenodo (license source sudah CC BY 4.0; DOI bisa menyusul kalau diminta).
