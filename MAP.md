# DATA-VAULT MAP — struktur site, siapa ngedit apa

Update terakhir: 2026-09-11. Doc ini WAJIB diupdate setiap ada halaman baru / produk baru masuk site.

Crosslink count: 5 related-pack lines live di guides (09-11 run — housing pack ×3: rent-affordability-calculator, hud-fmr-by-state, section-8-voucher-rent; icon pack ×1: mcp-claude-desktop; poster collection ×1: print-in-use-organizers; mcp-server-build-tutorial sudah link icon pack dari build 09-10; vendor pack = 0, no procurement guide). Counts source of truth (09-11 sweep): catalog.json datasets = 26, guides/ = 143, printables ItemList = 224, products.html <article> = 98.

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
| `sitemap.xml` | 218 URL; lastmod sweep 09-11: 9 URL konten hari itu (index, roundup, 2 index page, xmas hub, 5 guide crosslink) = 2026-09-11 | +1 entry per halaman/guide baru |
| `llms.txt` / `llms-full.txt` | Index buat AI agents | +1 line per halaman baru |
| `catalog.json` | Data katalog terstruktur | Ikut catalog-gen.py |
| `MAP.md` (ini) | Peta struktur | Setiap perubahan struktur |
| `CHANGELOG.md` | Log update dated | Setiap push yang berisi konten |

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
