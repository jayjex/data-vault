# CHANGELOG — data-vault

Log update site. 1 baris per push yang berisi perubahan konten. Terbaru di atas.

## 2026-09-11

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
