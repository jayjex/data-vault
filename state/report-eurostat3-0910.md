# Eurostat ETL 3 — une_rt_m monthly refresh — 2026-09-10

Lane: data-vault ETL #13 (eurostat3). Brief: cek une_rt_m (monthly) — annual tua, monthly mungkin fresh. Kalau monthly 0 baru 2026 → skip. **Monthly fresh → dataset baru di-ship.**

## Probe (fresh, bukan salin report)
- `une_rt_a` (annual, ulang probe): masih tail 2025, 0 nilai 2026. Dud ke-3 kalinya (etl7, etl10 sama). Sesuai brief, pindah ke monthly.
- `une_rt_m` (monthly, keyless JSON-stat): time axis s.d. 2026-08, **nilai ada s.d. 2026-07** (0 baris 2026-08). Metadata source: last updated **2026-09-04**.
- Dims une_rt_m: freq M; s_adj NSA/SA/TC; age TOTAL/Y25-74/Y_LT25; unit PC_ACT/THS_PER; sex F/M/T. Kode band beda dari annual (TOTAL bukan Y15-74).
- **EA20 tidak ada di une_rt_m**: request geo=EA20 (semua filter) → size 0, value 0. Euro area aggregate cuma di annual table. Slice final = 9 geo (EU27_2020 + 8 negara), disebut di schema + page.

## Dataset baru: `eurostat-unemployment-monthly`
`data/eurostat/unemployment-monthly/`:
- `unemployment-rate-monthly.csv` — 7,641 rows, 489 KB. Grid lengkap 9 geo × 283 bulan (2003-01 → 2026-07) × 3 sex = 7,641 tanpa gap. Kolom 8: month, geo, sex, age (selalu TOTAL), value, + 3 label. Slice: s_adj **SA**, unit **PC_ACT**, age **TOTAL**.
- `sample.csv` 22 rows (tail = 2026-07, ter-fresh) + `sample.json` {slug, name, columns, row_count 7641, records 22} — konvensi row_count = full rows mengikuti annual pack.
- `schema.md` — kolom, coverage, SA-only caveat, revisi bulanan, flag stripping, TOTAL vs Y15-74.

ETL: `tools/etl-eurostat-une-monthly.py` (stdlib, rerunnable, pola sama dgn etl-eurostat-une.py; sample row_count difix jadi full-row count). Scratch: `tmp/etl-eurostat3/`.

## Angka (script-checked, recompute dari API)
- 2026-07 (T): EU27 6.1, DE 4.0, EL 7.9, ES 10.0, FR 8.3, IT 5.8, NL 4.0, PL 3.4, SE 8.6. ES max, PL min.
- Sex 2026-07: F>M di 6 dari 9 geo (EU27 6.3 vs 5.9).
- EU27 T series: 9.8% (2003-01) → peak **11.7% (2013-05)** → 6.1% (2026-07).
- File max: EL 28.3% (2013-07); ES peak 26.4% (2013-02); PL peak 20.0% (2003-08); NL low 3.2% (2022-04). Sanity 0-40: n=7,641, min 2.4, max 32.3, 0 out-of-range.

## Halaman + indeks
- `datasets/eurostat-unemployment-monthly.html`: Dataset JSON-LD (3 DataDownloads, isAccessibleForFree, isBasedOn une_rt_m databrowser), stats bar, preview tabel 2026-07 T 9 geo, files list ukuran aktual, cross-link annual/rents/house-prices/labor guide/population/license guide. No-ai-slop: 0 banned words, 0 em dash, angka konkret. NO-PRICE. No self-AI-reference.
- catalog.json 22→23 (entry setelah eurostat-unemployment, full_data free).
- sitemap.xml 162→163 (string-append sebelum </urlset>, minidom valid, no dup).
- llms.txt +1 section (posisi setelah unemployment annual) — GOTCHA: insert pertama kehapus header "### World Bank Population"; langsung dipulihkan, verifikasi 23 section utuh.
- datasets/index.html +1 row di Eurostat hub.
- Cross-link dua arah: annual page (About + btn "Monthly dataset →"), labor-market-data-guide.html (Columns section +1 kalimat).

## Commit + IndexNow
- Commit `069f948` push origin/main (13 files, 8,210 insertions). Payload ikut di-commit sesuai pola etl12: `state/indexnow-payload-dv-0910etl13.json` (8 URL, keyLocation included).
- Key verify: keyLocation `.../78e095195f1e3c98ed5e6c17474dc1b6.txt` HTTP 200, body == key. Match.
- Pre-POST liveness: 8/8 URL HTTP 200 (page + 4 data files + annual page + catalog + llms; Pages build delay ±2 menit, di-retry sampai 200). Live sitemap 163 loc, live catalog 23 datasets, live CSV header/first-row cocok disk.
- POST api.indexnow.org: **HTTP 200**.

## Biaya
$0. Keyless HTTP, no API berbayar, no paid tool.
