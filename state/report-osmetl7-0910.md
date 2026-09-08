# OSM/data-vault ETL batch 7 — HUD FMR FY2026 county completeness (2026-09-10)

Lane: data-vault ETL batch 7 (etl7). etl6 (Oseania/Afrika/US OSM) jalan di lane lain — nol sentuhan ke file dia.

## Keputusan sumber
Kandidat eurostat une_rt_a refresh Q2 di-probe dulu: API annual tail = 2025, gak ada baris 2026, jadi refresh = dud (0 delta). Pivot ke HUD FMR county completeness: source `fiatdock-endpoint/data/hud-fmr-county-2026.csv` 3,229 baris county-equivalent, 15 kolom, 0 sel kosong. Airbnb new city gak dipilih: fiatdock cuma punya 6 kota dan semuanya udah ke-cover datasets/airbnb-six-cities.html.

## Dataset (baru, bukan punya etl6)
`data/hud-fmr-county-2026/`:
- `fmr-county-2026.csv` — full copy verbatim, 3,229 rows, 266 KB
- `spread-counties.csv` — derived: 8 county tempat `fmr_2br_max > fmr_2br_median`, kolom gap_2br + gap_pct_2br
- `sample.csv` (22 rows) + `sample.json` (shape {slug, name, columns[], row_count, records[]})
- `schema.md` — dictionary, coverage, caveats

ETL: `tools/etl-hud-county-completeness.py` (stdlib, rerunnable, baca fiatdock CSV → emit 4 file + summary angka).

## Temuan (semua recomputed dari CSV, script-checked vs halaman)
- 3,221/3,229 county max==median 2BR (satu FMR area per county). Cuma 8 county punya range beneran: 8-8 metro, semua ME/NH/MA/RI (multi-FMR-area). Bristol MA $1,729→$2,550 (+47.5%) terlebar.
- 56 state/territory codes (incl DC PR GU VI AS MP), metro 1,253 vs nonmetro 1,976.
- 2BR county median nasional $1,018; top Santa Cruz CA $4,214; bawah PR municipios $475.
- Rasio 4BR/0BR median: median 1.95, range 1.52-2.43.
- `area_rows` sums 4,764 raw HUD area lines → 3,229 county rows; 67 county >1 (Aroostook ME 71 terbanyak).

## Halaman
`datasets/hud-fmr-county-2026.html`: Dataset JSON-LD json-validated (license CC0, isBasedOn huduser FY26_FMRs.xlsx), tag balance OK, 8-county table script-checked == spread-counties.csv, cross-links hud-fmr-2026 + guides (by-county, small-areas, dataset-download, license) + portfolio, footer nav sama pattern. No-ai-slop skill dibaca + diaplikasikan (gak ada throat-clearing, colon reveal, puffery; angka konkret semua). No self-AI-reference.

## Koordinasi etl6 (catalog/sitemap LOCKED)
- Pre-edit origin/main = b11bd20 (DOI badge commit, BUKAN commit etl6 — etl6 belum commit saat batch 7 jalan).
- catalog.json / sitemap.xml / llms.txt / datasets/index.html TIDAK disentuh (aturan task: jangan sentuh sampai etl6 selesai).
- Delta dicatat di `state/catalog-delta-osmetl7-0910.json`: entry catalog lengkap (16th dataset, full_data free), URL sitemap baru (152→153), lastmod 2026-09-10, baris llms.txt. Merge setelah etl6 commit.
- Commit batch 7 isinya: data dir + page + tools + report + delta JSON saja.

## Biaya
$0. Keyless, source CSV lokal fiatdock, no API berbayar.
