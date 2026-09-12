# DATA-VAULT MAP — struktur site, siapa ngedit apa

Update terakhir: 2026-09-12. Doc ini WAJIB diupdate setiap ada halaman baru / produk baru masuk site.

Crosslink count: 5 related-pack lines live di guides (09-11 run — housing pack ×3: rent-affordability-calculator, hud-fmr-by-state, section-8-voucher-rent; icon pack ×1: mcp-claude-desktop; poster collection ×1: print-in-use-organizers; mcp-server-build-tutorial sudah link icon pack dari build 09-10; vendor pack = 0, no procurement guide). Counts source of truth (09-11 dvcc audit + 09-12 sweep): catalog.json datasets = 26 live-only (produk PREP tidak masuk), guides = 143 (guides/ 144 file incl. hub index), halaman `datasets/` = 26 produk + index, `printables/` = 23 lembar STL + halaman template + 1 preview planner 2027, free-printables-index ItemList = 224, products.html <article> = 101 (94 kartu nunjuk halaman produk: 90 paid $1,235 + 4 free; 7 kartu lagi masih nempel halaman store karena produknya belum active, termasuk freelancer-starter-bundle), catalog.html ItemList = 106 (102 paid + 4 free, $1,463), sitemap.xml = 222 URL, state/portfolio.json = 146 rows (108 baris LIVE, 106 jadi kartu ber-link — 2 sisanya LIVE-GUMROAD-DRAFT belum punya halaman jual, 39 baris PREP/queued/pending/DISCARDED). Sample rent + NFL (`mtwxoc3y` / `mtwxonks`) udah jadi kartu sejak 09-12: `reason` "pending_review" dibuang setelah GET by-id nunjukin dua-duanya active, dan folder `lead-hud-sample` / `lead-nfl-sample` masuk `CATEGORIES` + `GROUPS` + `COPY`. Flip 09-12 sore (EOD sync 0912d, 0 network): `interview-prep` PENDING-REVIEW-0912 -> LIVE-GETLY (id 3260f7e3-3bb4-4d9d-aa23-34a7ab929646, slug mty4lcu8, status active kebaca di snapshot kanon state/analytics/getly-metrics-0912d.json), kartunya pindah dari rail ke section Books & Workbooks / Guides, harga $12. Cell harga 17 baris `sale_band` 0912 di kedua halaman ikut disinkronkan ke `price_cents` (999/1999/4199 dll, dulu masih nampilin list price 1200/2400/4900). 3 kartu catalog punya byline cite + DOI Zenodo (superteam-earn, nfl-dataset, housing-affordability — 09-12). 3 halaman preview produk staged (09-12, tabel di bawah) = 0 link beli. Disclaimer QA (09-11 audit): seluruh 143 guides saat itu dicek — 74 punya disclaimer (byline atau section), 69 technical-data optional tanpa; WAJIB-topic (keuangan/pajak/hukum/aset) kosong = 0; pattern = klausa hedged di `<p class="byline">` (blog5). Guide baru 09-12 `hsa-vs-fsa-2026-limits-run-out` (keuangan/pajak) bawa disclaimer "Not tax advice" + cite Pub 969 di byline.
## Halaman (root)

| File | Fungsi | Link beli? | Kapan diedit |
|---|---|---|---|
| `index.html` | Homepage: hero + nav + section ringkas; baris "Browse everything" bawah main = 8 link hub (catalog, guides, datasets, free-datasets, printables, roundup, xmas hub, agents). Baris "Free samples available" di bawah hero = 4 entri sample $0 Getly (earn mtryl1pi, walls mtrykrp1, rent mtwxoc3y, nfl mtwxonks) — href-nya slug live dari dump kanon, bukan diketik manual | Link ke store | Nav baru / hero copy; hub baru masuk daftar itu; sample baru aktif = entri baris itu ikut nambah |
| `portfolio.html` | Redirect 301-style ke catalog.html (legacy URL) | — | Jangan edit; single source = catalog.html |
| `catalog.html` | Katalog penuh 106 kartu + link beli per produk (59 Getly + 47 FW; Wall Art prints 12) | YA, per produk (halaman produk yang benar-benar live saja) | Tiap produk baru live → refresh dump kanon dulu (`curl -H "Authorization: Bearer $TOKEN" "https://www.getly.store/api/v1/products?limit=200" -o /home/uwuki/money-mission/tmp/getly-list-0912-fresh-dvsample.json && cp .../tmp/getly-list-0912-fresh-dvsample.json .../tmp/catalogfull-getly.json`; generator + deadlink-check baca dua path ini; refresh dump = tulis ulang DUA file itu sampai itemnya identik, 0912d bikin 58 -> 59 item active), terus regen `DV_SITE=$PWD python3 /home/uwuki/money-mission/tools/data-vault/catalog-gen.py` → commit+push |
| `products.html` | 101 kartu: 94 kartu kategori/link produk + rail "New this week" 7 kartu | Ya. 94 kartu nunjuk halaman produk beneran (90 paid + 4 free); 7 kartu rail "new this week" masih nempel `getly.store/store/matchbook-labs-mtrfh66f` karena listingnya belum active — `freelancer-starter-bundle` staged, 6 lainnya antrian Getly. `agent-prompt-pack-vol2` nambah kartu 09-12 di section Prompt Packs, dua sample rent + NFL nambah 09-12 di Free Samples. Angka hero 94 produk / 90 paid / $1,235 / 4 free = kartu ber-halaman-produk saja, rail gak kehitung. Harga per kartu = `price_cents` portfolio; karena generator masih abort, 17 sel harga band 0912 disinkronkan pakai `python3 tools/refresh-prices.py` (baca buy-link tiap kartu -> row portfolio -> tulis ulang `<b>$N</b> price`) | Tiap produk baru live → tambah/rotasi kartu; generator `tools/gen-products.py` sekarang baca `DV_SITE` / `DV_ROOT` / `DV_PORTFOLIO` tapi masih abort di 12 baris poster (`GROUPS` belum kenal `artifacts/products/fw-posters`) dan outputnya kehilangan rail "New this week" + link nav "Full catalog", jadi halaman ini hand-edit. Channel 14 kartu dual-rail ikut catalog: mega bundle, airbnb-vol2, line-icons-60 dibalik pagi (flips 3), sore ini 11 lagi `Get it on Getly` + `also on Fourthwall →` (NFL pack `mtrfvdt7`, base/L2 directory `mtscjkjy`, Web3 events calendar `mtrltlaw`, bookkeeping `mtt9uas2`, habit tracker `mtt3qobp`, HR ops kit `mtt9ufxg`, student dashboard `mtt7h222`, second-brain vault `mtu8xlqv`, ADHD planner `mtt3qpi3`, STR host binder `mtuvdpew`, web scraping script pack `mtrfwfcd`). Kartu vendor binder (`mtvuzj7k`) sengaja tetap Fourthwall-only: listingnya active di dump tapi `/product/`-nya masih nyaji 404 hasil cache ISR jaman pending (aturan 09-07, TTL 7 hari), jadi itu satu-satunya pengecualian di set. Enam kartu Getly-first lama (amenities, housing pack, prompt pack vol.1, best-of wallpapers, airbnb-vol2, line icons) ikut nambah `also on Fourthwall →` biar polanya sama semua, 17 link FW sekunder di halaman ini, semuanya di-GET 200 sore ini. `tools/gen-products.py` ngejalan aturan yang sama: `link_for()` milih Getly kalau `getly_id` ada di set active dump (bukan dari string `reason`, catatan vendor-pack nyebut `pending_review` masa lalunya), fallback ke Fourthwall kalau listing belum keliatan active, `ISR_404` nahan kasus vendor, dump dibaca dari `DV_GETLY_DUMP` atau `tmp/getly-list-0912-fresh-dvsample.json`. Selisih output generator vs `products.html` = 0 kartu dari 94, dicek pakai `DV_PORTFOLIO=/tmp/dvsim-portfolio.json` (146 baris dikurangi 12 baris poster yang bikin abort) |
| `free-datasets-for-ai-agents.html` | Landing dataset gratis (funnel dataset-mcp) | Sample download | Dataset baru masuk |
| `free-printables-index.html` | Index printable gratis (funnel planner) | — | Printable baru. Kartu di grid 225: 224 halaman printable + 1 kartu STL MakerWorld (`Herb Markers`, link keluar, bukan di dalam ItemList 224). Stat bar nyebut dua-duanya biar gak keliatan off-by-one |
| `printable-index-roundup.html` | Roundup artikel printables | — | Jarang |
| `christmas-gift-planning-hub.html` | Seasonal hub: Santa letter freebie, gift budget tracker $9, planner grid sample | Tidak — dua tombol `Coming soon` `aria-disabled` tanpa `href` (09-12; sebelumnya 2 placeholder mentah `GUMROAD_XMAS_URL` / `GETLY_XMAS_URL` yang balas 404) | Swap ke URL asli saat freebie/tracker beneran live (cek `state/portfolio.json`: Santa letter = Gumroad draft, `xmas-gift-tracker` = PREP-GRLY-0918); sudah dikard di free-printables-index + li di printable-index-roundup (224 total, xnav 0911) |
| `guides/index.html` | Hub 143 guides (SEO internal links) | — | Tiap guide/baru blog live → tambah kartu |
| `guides/*.html` | 143 guide SEO | CTA store di footer | — |
| `agents/index.html` | Halaman "For agents": MCP servers + install npm | npm | MCP server baru / versi baru |
| `assets/`, `data/`, `datasets/`, `printables/` | File statis (img, CSV sample, PDF) | — | — |

## File pendukung (edit saat nambah halaman)

| File | Isi | Trigger edit |
|---|---|---|
| `sitemap.xml` | 222 URL; +3 halaman preview staged 09-12 (occupation-wages, agent-skills-vol1, planner-2027), lastmod 3 index yang diedit juga di-bump 09-12 | +1 entry per halaman/guide baru |
| `llms.txt` / `llms-full.txt` | Index buat AI agents. `llms-full.txt` = hasil `python3 tools/llmsfull-gen.py` (dibaca dari README.md + 10 dataset page + 3 guide terakhir + blok DOI) — jangan edit manual, edit README.md lalu regen | +1 line per halaman baru |
| `catalog.json` | Data katalog terstruktur | Ikut catalog-gen.py |
| `MAP.md` (ini) | Peta struktur | Setiap perubahan struktur |
| `CHANGELOG.md` | Log update dated | Setiap push yang berisi konten |
| `tmp/deadlink-check.py` | QA link mati offline (0 HTTP): semua `href` di 11 halaman inti + 3 halaman preview vs baris live `money-mission/state/portfolio.json`, dump Getly `money-mission/tmp/catalogfull-getly.json` (copy byte-identik dari dump kanon `tmp/getly-list-0912-fresh-dvsample.json`, 59 item active dari `GET ?limit=200`, di-refresh eod-sync-0912d 09-12), slug SellApp di `money-mission/state/sellapp/store-status.md`, DOI vs `state/zenodo-dois.json`; plus audit count kartu == link beli, `.come` list bebas link, pola Coming-soon di halaman preview, dan token placeholder (`SLUGPENDING`, `_XMAS_URL`) | Setiap habis regen / tambah produk; jalan `python3 tmp/deadlink-check.py`, harus `OK: 0 dead link` |

## Halaman preview produk staged (belum ada link beli)

Produk PREP (artifact jadi, belum ada slug live di Getly) punya halaman preview sendiri: sample gratis + data dictionary/spec + tombol `<span class="btn" aria-disabled="true">Coming soon</span>` tanpa `href`. Aturan: 0 link beli palsu, nama O*NET/BLS cuma jadi adjective (bukan nama produk/slug), atribusi verbatim + daftar perubahan nempel di halaman, disclaimer hedged di `<p class="byline">`.

| Halaman | Produk | Sample gratis | Status Getly |
|---|---|---|---|
| `datasets/occupation-wages.html` | Occupation Skills and Wages Map, $24 planned | `data/occupation-wages/sample.csv` + `sample.json` (25 baris dari 1.016, 19 kolom) | PREP, belum di-list |
| `agents/agent-skills-vol1.html` | Matchbook Ops Skill Pack Vol.1, $8 planned | `data/agent-skills-vol1/` 2 file skill utuh + `sample.csv` + `sample.json` + `LICENSE.txt` | PREP, belum di-list |
| `printables/planner-2027.html` | 2027 Dated Planner + Wall Calendar, $9 planned | tidak ada PDF gratis; page map + grid Oktober 2027 + tabel bulan 2027 dirender di HTML | PREP, belum di-list |

Crosslink: `datasets/index.html` (7 core packs), `printables/index.html`, `agents/free-agent-tools.html` (section "Paid and staged items", ItemList 7→8). `catalog.json` / `catalog.html` / `products.html` TIDAK disentuh — generatornya cuma untuk produk live; swap link beli + entri `full_data` saat slug Getly muncul.

OG image: `assets/og/{occupation-wages,agent-skills-vol1,planner-2027}.png`, dirender `tools/gen-og.py` (3 entri PAGES baru).

## Checklist nambah 1 produk baru ke site

1. `catalog.html` → regenerate: `DV_SITE=$PWD python3 /home/uwuki/money-mission/tools/data-vault/catalog-gen.py` (source of truth)
2. `products.html` → rotasi kartu baru (judul, harga, desc 1 kalimat, link Getly `/product/<slug>`)
2. `catalog.html` → regenerate: `DV_SITE=$PWD python3 /home/uwuki/money-mission/tools/data-vault/catalog-gen.py` (sumber: portfolio.json + dump Getly / API Getly kalau ada token)
3. `guides/index.html` → kalau ada blog/guide pendampingnya, tambah kartu
4. `sitemap.xml` → +1 URL (kalau halaman baru; produk tidak)
5. `llms.txt` → +1 line (halaman baru saja)
6. `CHANGELOG.md` → 1 baris dated
7. Commit + push + cek 200 + IndexNow (key `78e0951...`, file `state/indexnow-payload-*`)

## Checklist nambah 1 guide/blog baru

1. `guides/<slug>.html` (template: `guides/landlord-bookkeeping.html`)
2. `guides/index.html` → +1 kartu di grup topiknya
3. `sitemap.xml` +1, `llms.txt` +1, `CHANGELOG.md` +1
4. IndexNow ping
5. Kalau blog jual produk: link Getly `/product/<slug>` (swap dari store-link placeholder saat produk live)

## Traffic sources — dari mana pengunjung datang

| Sumber | Mekanisme | Status 09-11 |Cadence |
|---|---|---|---|
| Reddit (u/jayjayex) | 5 post/hari, 00:10Z, value-first + 1x link | 5 komentar live, score 1, 0 removal | Harian, cap 5 |
| Google/Bing SEO | guides 142 + blog funnel + sitemap + IndexNow | Baru nendang 09-11 (blog5, hub, IndexNow ×3) | Blog 1-2/minggu, ping tiap push |
| MCP directories | Glama (2 server live), mcp.so (hold #3981), Smithery (butuh user key) | dataset-mcp 294 dl minggu-1 | Pas rilis versi |
| GitHub backlink | PR ke awesome-lists (punkpeye #14168/#14169 open) | 2 PR open | Saat ada server/repo baru |
| npm | README package → data-vault | 2 package live | Pas rilis |
| Getly marketplace | Store internal traffic + auto-newest | 126 real views total | Pasif |
| Zenodo DOI (credential + backlink) | DOI cite-byline di kartu/halaman dataset + `identifier` JSON-LD; zenodo.org records link balik ke vault | **14/14 DOI synced** (earn 10.5281/zenodo.22707493 kartu pos 4 + hub earn-bounties 09-11) | Pasif (citability) |
| Fourthwall/SellApp | Sama, pasif | — | Pasif |
| Free samples funnel | datasets/printables gratis → CTA store | Halaman live | Pasif |

## Apa yang belum ada (jelasin biar gak ditanya lagi)

- Analytics per-source belum kebaca: Getly API gak expose referrer (`read:analytics` = dashboard-only). Setelah user buat key `read:store`+`read:analytics` (USER-ACTIONS #13) → breakdown github.io vs organic vs reddit bisa dipantau mingguan.
- Email list belum ada (lead magnet freebie3 baru masuk Gumroad 09-12). Setelah live → tambah `newsletter signup`? Butuh keputusan user (Gumroad follows feature).
