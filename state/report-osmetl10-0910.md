# data-vault ETL batch 10 — Airbnb 8 more US cities (2026-09-10)

Lane: data-vault ETL batch 10 (etl10). etl9 (OSM US round 2, NYC-Chicago-Seattle, commit f895c46) sudah commit sebelum batch 10 commit — kandidat OSM US utama sudah keambil, jadi tidak diulang. Zero file conflict dengan etl9 (beda slug/beda entry catalog).

## Keputusan kandidat
1. **Airbnb cities-index refresh 6 → 8 kota baru** — DIPILIH. Inside Airbnb get-the-data menampilkan 34 US city dengan snapshot 2026; 8 kota besar di luar set six-cities tersedia semua.
2. eurostat une_rt_a Q2 2026 refresh — probe ulang: `une_rt_a` geo=NL+EU27_2020 annual tail masih 2025, 0 nilai 2026. Dud kedua kalinya (etl7 sama). Tidak dikerjakan.
3. NBA stats free API — tidak dibutuhkan (kandidat 1 jalan mulus).

## Dataset baru
`data/airbnb-eight-cities/` (90,746 rows, 12 kolom, ~12.5 MB):
- 8 per-city CSV verbatim-normalized: boston 4,414 / chicago 8,704 / los-angeles 43,932 / new-orleans 7,254 / portland 4,210 / san-francisco 7,422 / seattle 7,814 / washington-dc 6,996
- `cities-index.csv` 8 rows (city, snapshot_date, rows, file, median_price_usd, room_type_mix)
- `sample.csv` 20 Boston rows + `sample.json` {slug, name, columns[], row_count, records[]}
- `schema.md` dictionary + normalization + caveats

Schema disamakan dengan airbnb-six-cities (12 kolom: id..last_review). Source 19+ kolom (host_id, host_name, neighbourhood_group, license, dll) dibuang. Host fields zero, coordinate blur mengikuti source (4-7 desimal).

ETL: `tools/etl-airbnb-eight-cities.py` (stdlib, rerunnable). Source file: `tmp/etl-airbnb8/airbnb-<city>.csv` — catatan: copy ke fiatdock-endpoint/data/ berakhir direname/dipindah oleh proses eksternal (watcher unknown), jadi source ditaruh di tmp/ per STRUCTURE-MAP, script diarahkan ke sana.

## Angka (script-checked)
- Medians: Boston 279, Seattle 281, SF 252, Chicago 223, LA 224, DC 221, NOLA 192, Portland 160; combined 226.
- Room mix: Entire 67,526 (74%) / Private 21,402 (24%) / Hotel 1,371 (2%) / Shared 447.
- 11,594/90,746 rows (13%) tanpa harga; median hanya hitung price-bearing rows.
- SF max 99,999 dan outlier >20k = source artifact, tidak diedit.
- 8 kota baru hampir sama besarnya dengan six-cities (90,746 vs 90,169); LA 43,932 = file kota terbesar di site (NYC 30,234).

## Snapshot dates (from dir names, verbatim)
Boston 2026-06-15, Chicago 2026-06-24, LA 2026-06-15, NOLA 2026-06-16, Portland 2026-06-15, SF 2026-06-14, Seattle 2026-06-15, DC 2026-06-24.

## Halaman + indeks
- `datasets/airbnb-eight-cities.html`: Dataset JSON-LD (license CC BY 4.0, isAccessibleForFree, 12 DataDownloads, isBasedOn insideairbnb.com/get-the-data/), city-index table 8 rows == cities-index.csv (script-checked), files list dengan ukuran aktual, cross-links six-cities + 4 airbnb guides + license guide + portfolio. No-ai-slop skill diaplikasikan (0 banned words, 0 em dash, angka konkret semua). No self-AI-reference.
- catalog.json: +entry setelah airbnb-six-cities (19→20 datasets), full_data.status "free" (source CC BY 4.0, no Getly pack).
- sitemap.xml: +1 URL (157→158), string-append sebelum </urlset>, minidom valid, no dup.
- llms.txt: +1 dataset section setelah six-cities.
- datasets/index.html: +1 row core packs, lead 1 free set note.
- datasets/airbnb-six-cities.html: +1 cross-link sentence ke halaman baru.

## Biaya
$0. Keyless HTTP download dari data.insideairbnb.com, no API berbayar.
