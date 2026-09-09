# data-vault ETL batch 14 — World Bank G20 life expectancy (2026-09-10)

Lane: data-vault ETL batch 14 (etl14, dataset #24). etl13 (Eurostat monthly unemployment, commit 069f948) landed sebelum batch mulai — zero file conflict (beda slug, beda entry catalog; sisa diff working tree milik lane lain, tidak disentuh).

## Keputusan kandidat
1. **World Bank SP.DYN.LE00.IN life expectancy, G20 + EU27** — DIPILIH. Probe dulu sebelum commit: satu call API keyless, hidup (bukan 0 rows): 1,300 rows untuk 20 entitas, 1960-2024, 65 observasi/entity tanpa gap, license CC BY 4.0. Trio natural dengan worldbank-g20-population (SP.POP.TOTL) + worldbank-g20-rural (SP.RUR.TOTL.ZS), API dan entity list sama persis, join on entity-year.
2. OWID CO2 per capita — tidak diprobe (kandidat 1 jalan, danOWID CSV lebih berat dari satu call WB API).
3. FAO food price index + WB Gini — tidak diprobe (alasan sama).

## Dataset baru
`data/worldbank-g20-life-expectancy/` (1,300 rows long format, 4 kolom, ~35 KB total):
- `g20-life-expectancy.csv` — long format entity,iso3,year,life_expectancy_years; 20 entitas (19 negara G20 + EUU EU27 aggregate) × 65 tahun (1960-2024), values 2dp dari API (round(v,2); series WDI annual estimate, rounding buang 0 presisi berguna), no imputation.
- `g20-life-expectancy-2024.csv` — 20 rows latest-year per entity, sorted life expectancy desc.
- `sample.csv` 20 rows (Argentina 1960-1979) + `sample.json` {slug, name, columns[], row_count, records[]} — script-checked == long[:20].
- `schema.md` — dictionary + normalization + caveats (termasuk caveat 2020-2021 COVID shock + kenapa series berhenti di 2024).
- `etl-stats.json` — angka untuk halaman/report.

ETL: `tools/etl-wb-g20-life-expectancy.py` (stdlib, rerunnable; source JSON disimpan `tmp/etl-wb-le/wb-le.json`). Source URL: api.worldbank.org/v2 indicator SP.DYN.LE00.IN, date=1960:2025, per_page=20000, retrieved 2026-09-10, WDI lastupdated 2026-07-13. Series berhenti di 2024 karena WDI belum publish 2025 life expectancy (lag lebih panjang dari population counts) — ditulis jelas di schema + halaman.

Gotcha ETL: fetch country=all returns ~265 entity termasuk aggregates — filter G20 iso3 harus diterapkan saat build records, bukan saat stats (bug pertama: records tanpa filter → leaders terisi MCO/ISL/FRO; ketangkap karena KeyError 'JPN' di stats, fix + rerun clean).

## Angka (script-checked, recompute fresh)
- 2024: Japan 84.04 #1 — sudah 53 tahun berturut-turut (sejak 1972); Canada memimpin 1960-1971 (12 tahun) sebelum itu. Lalu Italy 83.95, Korea 83.63, Australia 83.05, France 82.98.
- Bottom 2024: South Africa 66.31 (record high utk negaranya), Indonesia 71.29, India 72.23. Spread top-bottom 17.7 tahun.
- Gain 1960→2024: China +44.60 (33.42 → 78.02) terbesar; 33.42 itu = nilai terendah di seluruh file. Saudi Arabia +33.67 (45.31 start), Korea +29.83 (53.80 start).
- Paling lambat: Russia +5.91, trough 64.47 di 1994, baru lewat level 1960-nya (67.53) di 2007. USA +9.12: 78.79 (2019) → dip 76.33 (2021) → 78.89 (2024) baru balik di atas level 2019 di 2024.
- 14/20 entitas set record high di 2024; 6 yang tidak peak-nya 2019-2022: Germany/Canada/Turkiye 2019, Japan 2020, Australia 2021, China 2022 → baseline pre-2020 yang benar utk 6 entitas itu.

## Halaman + indeks
- `datasets/worldbank-g20-life-expectancy.html`: Dataset JSON-LD (license CC BY 4.0, isAccessibleForFree, 5 DataDownloads, isBasedOn = API URL), tabel 2024 20 rows == g20-life-expectancy-2024.csv (script-checked), files list ukuran aktual, cross-link population + rural + milestones/rural guides + license guide + portfolio. No-ai-slop diaplikasikan (0 banned words, 0 em dash, 0 `$`, semua angka dari CSV). No self-AI-reference. No price.
- catalog.json: +entry setelah worldbank-g20-rural (23→24 datasets), full_data.status "free" (source CC BY 4.0, no Getly pack).
- sitemap.xml: +1 URL (165→166), disisipkan setelah worldbank-g20-rural, minidom valid, 0 dup.
- llms.txt: +1 dataset section setelah worldbank-g20-rural (24 sections total).
- datasets/index.html: World Bank series 2→3 rows + lead "2 World Bank series"→"3 World Bank series".
- datasets/worldbank-g20-population.html: btn-note diganti — sekarang nyebut life expectancy pack (trio) dulu, eurostat pack dihapus dari note itu.
- datasets/worldbank-g20-rural.html: +1 paragraf cross-link ke life expectancy pack.

## Deploy + IndexNow
- Commit targeted b88c71a (12 files, no git add -A), push ke origin/main jayjex/data-vault FF.
- Live verify: page + sample.json 200 di try1 (Pages cepat), row_count 1300 / catalog 24 / sitemap 166 terkonfirmasi live.
- IndexNow: payload `state/indexnow-payload-dv-0910etl14.json`, keyLocation verify 200 + body match dulu, 10 URL semua 200 pre-POST, POST api.indexnow.org → HTTP 200.

## Biaya
$0. Keyless HTTP dari api.worldbank.org, no API berbayar, no Zenodo (bisa menyusul kalau diminta).
