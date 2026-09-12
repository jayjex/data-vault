# DATA-VAULT MAP — struktur site, siapa ngedit apa

Update terakhir: 2026-09-12. Doc ini WAJIB diupdate setiap ada halaman baru / produk baru masuk site.

Crosslink count: 5 related-pack lines live di guides (09-11 run — housing pack ×3: rent-affordability-calculator, hud-fmr-by-state, section-8-voucher-rent; icon pack ×1: mcp-claude-desktop; poster collection ×1: print-in-use-organizers; mcp-server-build-tutorial sudah link icon pack dari build 09-10; vendor pack = 0, no procurement guide). Counts source of truth (09-11 dvcc audit + 09-12 sweep): catalog.json datasets = 26 live-only (produk PREP tidak masuk), guides = 142 (guides/ 143 file incl. hub index), halaman `datasets/` = 26 produk + index, `printables/` = 23 lembar STL + halaman template + 1 preview planner 2027, free-printables-index ItemList = 224, products.html <article> = 98, catalog.html ItemList = 102 (100 paid + 2 free, $1,489), sitemap.xml = 221 URL, state/portfolio.json = 140 rows (live 100+2). 3 halaman preview produk staged (09-12, tabel di bawah) = 0 link beli. Disclaimer QA (09-11 audit): seluruh 143 guides dicek — 74 punya disclaimer (byline atau section), 69 technical-data optional tanpa; WAJIB-topic (keuangan/pajak/hukum/aset) kosong = 0; pattern = klausa hedged di `<p class="byline">` (blog5).
## Halaman (root)

| File | Fungsi | Link beli? | Kapan diedit |
|---|---|---|---|
| `index.html` | Homepage: hero + nav + section ringkas; baris "Browse everything" bawah main = 8 link hub (catalog, guides, datasets, free-datasets, printables, roundup, xmas hub, agents) | Link ke store | Nav baru / hero copy; hub baru masuk daftar itu |
| `portfolio.html` | Redirect 301-style ke catalog.html (legacy URL) | — | Jangan edit; single source = catalog.html |
| `catalog.html` | Katalog penuh 102 kartu + link beli per produk (52 Getly + 50 FW; Wall Art prints 12) | YA, per produk | Tiap produk baru live → `python3 tools/catalog-gen.py` → commit+push |
| `products.html` | "New this week" — 8 kartu produk baru | Ya (Getly) | Tiap produk baru live → tambah/rotasi kartu |
| `free-datasets-for-ai-agents.html` | Landing dataset gratis (funnel dataset-mcp) | Sample download | Dataset baru masuk |
| `free-printables-index.html` | Index printable gratis (funnel planner) | — | Printable baru |
| `printable-index-roundup.html` | Roundup artikel printables | — | Jarang |
| `christmas-gift-planning-hub.html` | Seasonal hub: Santa letter freebie, gift budget tracker $9, planner grid sample | Ya (2 link placeholder GUMROAD_XMAS_URL / GETLY_XMAS_URL — swap saat produk live) | Swap placeholder saat freebie/tracker live; sudah dikard di free-printables-index + li di printable-index-roundup (224 total, xnav 0911) |
| `guides/index.html` | Hub 142 guides (SEO internal links) | — | Tiap guide/baru blog live → tambah kartu |
| `guides/*.html` | 142 guide SEO | CTA store di footer | — |
| `agents/index.html` | Halaman "For agents": MCP servers + install npm | npm | MCP server baru / versi baru |
| `assets/`, `data/`, `datasets/`, `printables/` | File statis (img, CSV sample, PDF) | — | — |

## File pendukung (edit saat nambah halaman)

| File | Isi | Trigger edit |
|---|---|---|
| `sitemap.xml` | 221 URL; +3 halaman preview staged 09-12 (occupation-wages, agent-skills-vol1, planner-2027), lastmod 3 index yang diedit juga di-bump 09-12 | +1 entry per halaman/guide baru |
| `llms.txt` / `llms-full.txt` | Index buat AI agents. `llms-full.txt` = hasil `python3 tools/llmsfull-gen.py` (dibaca dari README.md + 10 dataset page + 3 guide terakhir + blok DOI) — jangan edit manual, edit README.md lalu regen | +1 line per halaman baru |
| `catalog.json` | Data katalog terstruktur | Ikut catalog-gen.py |
| `MAP.md` (ini) | Peta struktur | Setiap perubahan struktur |
| `CHANGELOG.md` | Log update dated | Setiap push yang berisi konten |

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

1. `catalog.html` → regenerate: `python3 tools/catalog-gen.py` (source of truth)
2. `products.html` → rotasi kartu baru (judul, harga, desc 1 kalimat, link Getly `/product/<slug>`)
2. `catalog.html` → regenerate: `python3 tools/catalog-gen.py` (sumber: portfolio.json + Getly API)
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
