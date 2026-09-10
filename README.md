# data-vault

Sample-first data catalog. Free samples for every dataset, machine-readable for agents and scripts, live at **https://jayjex.github.io/data-vault/**

Every pack previews on the page: real rows, documented schema, no email wall. Scripts and agents can skip the browser and read `catalog.json` instead. Full packs ship through [Getly](https://www.getly.store/store/matchbook-labs-mtrfh66f).

## Ready-made packs

Instant downloads on the [Fourthwall store](https://jayjex-shop.fourthwall.com/):

| Pack | Price | What's inside |
|---|---|---|
| [World Civic Amenities Pack](https://jayjex-shop.fourthwall.com/products/world-civic-amenities-pack) | $12 | 84 amenity count rows for 25 cities on six continents, counted from OpenStreetMap on 2026-09-10: drinking water points, water fountains, public toilets, benches, public bookcases and bike repair stations. |
| [Agent Prompt Pack Vol.1](https://jayjex-shop.fourthwall.com/products/agent-prompt-pack-vol1) | $9 | 23 AI prompts that already ran in production. |
| [US Housing Affordability Pack](https://jayjex-shop.fourthwall.com/products/us-housing-affordability-pack) | $12 | Fair market rents for 51,871 ZIP codes and 3,229 counties, paired with Eurostat unemployment, house price and rent indices, in one 14-table CSV pack. |
| [Dark Wallpaper Best-Of Pack](https://jayjex-shop.fourthwall.com/products/dark-wallpaper-best-of-pack) | $7 | Twelve hand-picked dark wallpapers from the Dark Wallpaper Pack volumes: retro-futurist synthwave horizons, glowing bioluminescent caves, deep space nebulae, brutalist concrete, and retro CRT scanline textures. |
| [60 Line Icons Essentials](https://jayjex-shop.fourthwall.com/products/line-icons-60) | $5 | 60 hand-built line icons for UI work: dashboards, landing pages, docs sites, side projects. |

All five also come as one download, the [Data Vault Desk Mega Bundle](https://jayjex-shop.fourthwall.com/products/data-vault-desk-mega-bundle) for $29 ($45 bought separately).

## Datasets

| slug | name | rows | niche | sample | full data |
|---|---|---|---|---|---|
| `nfl-games` | NFL Games & Betting Lines 1999–2026 | 7,548 rows | sports | [CSV](data/nfl-games/sample.csv) / [JSON](data/nfl-games/sample.json) | [Getly](https://www.getly.store/product/nfl-betting-game-data-pack-1999-2026-7-548-games-spreads-totals-moneylines-mtrfvdt7) |
| `hud-fmr-2026` | HUD Fair Market Rents FY2026 | 51,895 rows | gov-data | [CSV](data/hud-fmr-2026/sample.csv) / [JSON](data/hud-fmr-2026/sample.json) | [coming](https://www.getly.store/store/matchbook-labs-mtrfh66f) |
| `airbnb-six-cities` | Airbnb Listings, 6 US Cities | 90,169 rows | real-estate | [CSV](data/airbnb-six-cities/sample.csv) / [JSON](data/airbnb-six-cities/sample.json) | [Getly](https://www.getly.store/product/airbnb-multi-city-investor-pack-6-cities-60k-listings-90-169-rows-2026-snapshots-mtrfuvf3) |
| `earn-bounties` | Superteam Earn Live Listings | 28 listings | ai-agents | [CSV](data/earn-bounties/sample.csv) / [JSON](data/earn-bounties/sample.json) | [Getly](https://www.getly.store/product/superteam-earn-28-live-listings-dataset-186-reverse-engineered-api-routes-mtrfumk0) |
| `scraper-pack` | Web Scraping Script Pack | 10 scripts | dev-tools | [JSON](data/scraper-pack/sample.json) | [Getly](https://www.getly.store/product/web-scraping-script-pack-10-production-ready-playwright-templates-mtrfwfcd) |
| `printable-engineering-bundle` | Printable Engineering Bundle | 120 pages + 5 sheets | printables | [index](free-printables-index.html) | [Getly](https://www.getly.store/store/matchbook-labs-mtrfh66f) |

Full datasets are **not** in this repo. The repo carries samples only (first 10–25 rows per table, plus small complete aggregate tables). Total data volume: under 100 KB.

## Agent access

Start from the catalog, then fetch samples:

```bash
# machine-readable index of every dataset
curl -s https://jayjex.github.io/data-vault/catalog.json | jq '.datasets[] | {slug, niche, rows: .stats.rows}'

# schema + first records of one pack
curl -s https://jayjex.github.io/data-vault/data/hud-fmr-2026/sample.json | jq '.columns, .records[0]'
```

Endpoints:

- `/catalog.json`: index of slugs, niches, stats, sample URLs, full-data links
- `/data/<slug>/sample.json`: `{slug, name, columns[], row_count, records[]}`
- `/data/<slug>/sample.csv`: same rows as CSV
- `/llms.txt`: plain-text catalog for LLM crawlers
- `/agents/`: docs for agent developers
- `/sitemap.xml`, `/robots.txt`

The repo is MCP-ready by convention: `catalog.json` is the discovery document and every `sample.json` maps to a read-only resource. A dedicated MCP server is planned as phase 2.

## Pages

- `index.html`: catalog with niche filters (sports, real-estate, gov-data, ai-agents, dev-tools)
- `datasets/<slug>.html`: per-dataset page, description + stats + preview table + sample download + full-data link
- `agents/index.html`: endpoint docs + worked examples

Static site, vanilla HTML/CSS/JS, no build step. To preview locally: `python3 -m http.server` and open `http://localhost:8000`.

## License

License: CC BY 4.0 for samples, full data licensed per purchase. Upstream sources credited per dataset page: nflverse (CC BY 4.0), HUD (public domain), Inside Airbnb (CC BY 4.0), superteam.fun (harvested API data). If you republish samples, credit "Data Vault (jayjex.github.io/data-vault), CC BY 4.0" plus the upstream source.

---

Data Vault is a Matchbook Labs project · [github.com/jayjex](https://github.com/jayjex)
