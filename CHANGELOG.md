# CHANGELOG — data-vault

Log update site. 1 baris per push yang berisi perubahan konten. Terbaru di atas.

## 2026-09-11

- `index.html`: baris "Browse everything" 5→8 link — tambah christmas-gift-planning-hub, free-datasets-for-ai-agents, printable-index-roundup; IndexNow 1x (idxbrowse)
- `free-printables-index.html` + `printable-index-roundup.html`: +1 link Christmas gift planning hub (card events / li events, ItemList 223→224, count 22→23, sitemap lastmod 0911)
- `christmas-gift-planning-hub.html`: hub musiman baru — plan-early (deadline November/mail), Santa letter freebie 3 hal (GUMROAD_XMAS_URL), tracker $9 live-math (GETLY_XMAS_URL, live 09-17), grid sample 4 baris, 5 tips, FAQ; sitemap 217→218, llms.txt +1, IndexNow 1x

- `catalog.html` + `datasets/earn-bounties.html` + `llms.txt`/`llms-full.txt`: earn-dataset DOI 10.5281/zenodo.22707493 cite-byline + `identifier` JSON-LD di kartu (pos 4) dan hub page; DOI list 13→14 + mapping earn

- `catalog.html`: kartu housing-pack dapat DOI cite-byline 10.5281/zenodo.22706557 + `identifier` JSON-LD (generator doi-aware via portfolio `doi` field) — Zenodo DOI site sync 13/13

- `catalog.html`: wave3/4 poster desc verbatim — `poster_copy()` match fix (slug `-dusk-dither` strip), 6 kartu fallback generik → copy listing FW; tetap 102 kartu, Wall Art prints 12 (f0ff543)

- `catalog.html`: LIVE — 93 produk, link beli per kartu (Getly fresh-slug + FW), JSON-LD, regen tools/catalog-gen.py (a9b7e88)
- `portfolio.html`: jadi redirect ke catalog.html; nav swap "Full catalog"; sitemap -portfolio +catalog (47736f2)
- `products.html`: 2 kartu baru staged (interview-prep $12, starter-bundle $19) — slug swap saat live (e743bf3)
- `MAP.md` + `CHANGELOG.md`: struktur site + traffic sources + checklist edit (USER request 09-11)

- `agents/` + `llms*.txt`: MCP section refresh — install `npx @jayjex/dataset-mcp`, tambah pdfcheck-mcp (commit d3fe0c6)
- `guides/index.html`: hub 142 guides + kartu blog landlord-bookkeeping (2233434)
- `guides/landlord-bookkeeping.html`: blog5 LIVE (5c9...) + sitemap + llms.txt + IndexNow
- `products.html`: "New this week" 8 kartu LIVE (10d5634)
- `printables-index.html`: m38 + jadwal m41-46 (6106703)

## 2026-09-10

- guides hub lead 141 guides
- agents page live (MCP servers, glama links)

## 2026-09-09

- awesome-public-datasets sync (apd-core), DOI catalog 12 Zenodo
