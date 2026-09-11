# data-vault

Sample-first data catalog. Free samples for every dataset, machine-readable for agents and scripts, live at **https://jayjex.github.io/data-vault/**

Every pack previews on the page: real rows, documented schema, no email wall. Scripts and agents can skip the browser and read `catalog.json` instead. Full packs ship through [Getly](https://www.getly.store/store/matchbook-labs-mtrfh66f).

## Ready-made packs

Instant downloads on the [Fourthwall store](https://jayjex-shop.fourthwall.com/), with the same packs also on [SellApp](https://datavaultdesk.sell.app/):

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
| `nfl-games` | NFL Games & Betting Lines 1999-2026 | 7,548 | sports | [CSV](data/nfl-games/sample.csv) / [JSON](data/nfl-games/sample.json) | [free (Zenodo)](https://zenodo.org/records/22643177/latest) |
| `hud-fmr-2026` | HUD Fair Market Rents FY2026 | 51,895 | gov-data | [CSV](data/hud-fmr-2026/sample.csv) / [JSON](data/hud-fmr-2026/sample.json) | [free (Zenodo)](https://zenodo.org/records/22643149/latest) |
| `hud-fmr-2027` | HUD Fair Market Rents FY2027 | 51,871 | gov-data | [CSV](data/hud-fmr-2027/sample.csv) / [JSON](data/hud-fmr-2027/sample.json) | [free (Zenodo)](https://zenodo.org/records/22649503/latest) |
| `airbnb-six-cities` | Airbnb Listings, 6 US Cities | 90,169 | real-estate | [CSV](data/airbnb-six-cities/sample.csv) / [JSON](data/airbnb-six-cities/sample.json) | [free (Zenodo)](https://zenodo.org/records/22643189/latest) |
| `airbnb-eight-cities` | Airbnb Listings, 8 More US Cities (free) | 90,746 | real-estate | [CSV](data/airbnb-eight-cities/sample.csv) / [JSON](data/airbnb-eight-cities/sample.json) | [free](datasets/airbnb-eight-cities.html) |
| `earn-bounties` | Superteam Earn Live Listings | 28 | ai-agents | [CSV](data/earn-bounties/sample.csv) / [JSON](data/earn-bounties/sample.json) | [Getly](https://www.getly.store/product/superteam-earn-28-live-listings-dataset-186-reverse-engineered-api-routes-mtrfumk0) |
| `scraper-pack` | Web Scraping Script Pack | 10 | dev-tools | [CSV](data/scraper-pack/sample.csv) / [JSON](data/scraper-pack/sample.json) | [Getly](https://www.getly.store/product/web-scraping-script-pack-10-production-ready-playwright-templates-mtrfwfcd) |
| `eurostat-house-prices` | Eurostat House Price Index, NL & EU27, 2005-2025 | 342 | econ-data | [CSV](data/eurostat/house-prices/sample.csv) / [JSON](data/eurostat/house-prices/sample.json) | [free](data/eurostat/house-prices/house-price-index.csv) |
| `eurostat-rents` | Eurostat HICP Actual Rents, NL & EU27, CP0411 | 580 | econ-data | [CSV](data/eurostat/rents/sample.csv) / [JSON](data/eurostat/rents/sample.json) | [free](data/eurostat/rents/rent-index-monthly.csv) |
| `eurostat-unemployment` | Eurostat Unemployment Rate by Sex and Age, EU27 + 9 Countries, 2003-2025 | 3,768 | econ-data | [CSV](data/eurostat/unemployment/sample.csv) / [JSON](data/eurostat/unemployment/sample.json) | [free](data/eurostat/unemployment/unemployment-rate.csv) |
| `eurostat-unemployment-monthly` | Eurostat Monthly Unemployment Rate by Sex, EU27 + 8 Countries, 2003-2026 | 7,641 | econ-data | [CSV](data/eurostat/unemployment-monthly/sample.csv) / [JSON](data/eurostat/unemployment-monthly/sample.json) | [free](data/eurostat/unemployment-monthly/unemployment-rate-monthly.csv) |
| `worldbank-g20-population` | World Bank Population, G20 Countries + EU27, 1960-2025 (free) | 1,320 | econ-data | [CSV](data/worldbank-g20-population/sample.csv) / [JSON](data/worldbank-g20-population/sample.json) | [free](datasets/worldbank-g20-population.html) |
| `worldbank-g20-rural` | World Bank Rural Population Share, G20 Countries + EU27, 1960-2025 (free) | 1,320 | econ-data | [CSV](data/worldbank-g20-rural/sample.csv) / [JSON](data/worldbank-g20-rural/sample.json) | [free](datasets/worldbank-g20-rural.html) |
| `worldbank-g20-life-expectancy` | World Bank Life Expectancy, G20 Countries + EU27, 1960-2024 (free) | 1,300 | econ-data | [CSV](data/worldbank-g20-life-expectancy/sample.csv) / [JSON](data/worldbank-g20-life-expectancy/sample.json) | [free](datasets/worldbank-g20-life-expectancy.html) |
| `osm-asia-civic-amenities` | OpenStreetMap Civic Amenities, Tokyo-Jakarta-Seoul, 2026-09 | 9 | open-data | [CSV](data/osm-asia-civic/sample.csv) / [JSON](data/osm-asia-civic/sample.json) | [free](data/osm-asia-civic/counts-2026-09.csv) |
| `osm-us-civic-amenities` | OpenStreetMap Civic Amenities, New York-Los Angeles-Chicago-Austin-Seattle, 2026-09 | 15 | open-data | [CSV](data/osm-civic/sample.csv) / [JSON](data/osm-civic/sample.json) | [free](data/osm-civic/us-civic-amenities.csv) |
| `osm-eu-civic-amenities` | OpenStreetMap Civic Amenities, Berlin-Amsterdam-Paris-Madrid-Warsaw, 2026-09 | 15 | open-data | [CSV](data/osm-eu-civic/sample.csv) / [JSON](data/osm-eu-civic/sample.json) | [free](data/osm-eu-civic/eu-civic-amenities.csv) |
| `printable-engineering-bundle` | Printable Engineering Bundle | 120 pages + 5 sheets | printables | [index](free-printables-index.html) | [Getly](https://www.getly.store/store/matchbook-labs-mtrfh66f) |
| `osm-latam-civic-amenities` | OpenStreetMap Civic Amenities, Sao Paulo-Buenos Aires-Mexico City, 2026-09 | 9 | open-data | [CSV](data/osm-latam-civic/sample.csv) / [JSON](data/osm-latam-civic/sample.json) | [free](data/osm-latam-civic/latam-civic-amenities.csv) |
| `osm-mena-civic-amenities` | OpenStreetMap Civic Amenities, Istanbul-Cairo-Mumbai, 2026-09 | 9 | open-data | [CSV](data/osm-mena-civic/sample.csv) / [JSON](data/osm-mena-civic/sample.json) | [free](data/osm-mena-civic/mena-civic-amenities.csv) |
| `osm-africa-civic-amenities` | OpenStreetMap Civic Amenities, Lagos-Nairobi-Addis Ababa, 2026-09 | 9 | open-data | [CSV](data/osm-africa-civic/sample.csv) / [JSON](data/osm-africa-civic/sample.json) | [free](data/osm-africa-civic/africa-civic-amenities.csv) |
| `osm-oceania-civic-amenities` | OpenStreetMap Civic Amenities, Sydney-Melbourne-Auckland, 2026-09 | 9 | open-data | [CSV](data/osm-oceania-civic/sample.csv) / [JSON](data/osm-oceania-civic/sample.json) | [free](data/osm-oceania-civic/oceania-civic-amenities.csv) |
| `osm-us2-civic-amenities` | OpenStreetMap Civic Amenities, New York-Chicago-Seattle, 2026-09 | 9 | open-data | [CSV](data/osm-us2-civic/sample.csv) / [JSON](data/osm-us2-civic/sample.json) | [free](data/osm-us2-civic/us2-civic-amenities.csv) |
| `hud-fmr-county-2026` | HUD Fair Market Rents FY2026 by County: completeness & spread | 3,229 | gov-data | [CSV](data/hud-fmr-county-2026/sample.csv) / [JSON](data/hud-fmr-county-2026/sample.json) | [free](data/hud-fmr-county-2026/fmr-county-2026.csv) |
| `hud-fmr-metro-2027` | HUD Fair Market Rents FY2027, Top-50 Metro Areas | 50 | gov-data | [CSV](data/hud-fmr-metro-2027/sample.csv) / [JSON](data/hud-fmr-metro-2027/sample.json) | [free](data/hud-fmr-metro-2027/fmr-metro-2027.csv) |
| `hud-fmr-by-zip-2027` | HUD Fair Market Rents FY2027 by ZIP Code | 51,871 | gov-data | [CSV](data/hud-fmr-by-zip-2027/sample.csv) / [JSON](data/hud-fmr-by-zip-2027/sample.json) | [free](data/hud-fmr-by-zip-2027/fmr-by-zip-2027.csv) |

Every dataset ships with a sample in this repo (first 9-22 rows per table, small sets complete). Free datasets also carry their complete files in-repo, and four big packs (NFL games, HUD FMR FY2026, HUD FMR FY2027, Airbnb 6-cities) download free from Zenodo. Total data volume: about 18 MB.

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

A dedicated MCP server wraps this catalog: [github.com/jayjex/dataset-mcp](https://github.com/jayjex/dataset-mcp), listed in the official registry as `io.github.jayjex/dataset-mcp`. `query_dataset` filters and paginates any released table (100 rows per call), `get_stats` returns row counts and numeric min/max/mean, and `list_datasets`, `get_dataset_info`, and `get_sample` cover discovery and previews. Setup, Claude Desktop config, and worked examples: [/agents/](agents/).

## Pages

- `index.html`: catalog with niche filters (sports, real-estate, gov-data, ai-agents, dev-tools, open-data)
- `datasets/<slug>.html`: per-dataset page, description + stats + preview table + sample download + full-data link
- `agents/index.html`: endpoint docs + worked examples
- `products.html`: buyer catalog of every public product, generated by `tools/gen-products.py` from `../state/portfolio.json`. Rerun `python3 tools/gen-products.py` after every product push or status flip, commit the output, then IndexNow the URL. A live product missing from the script's GROUPS/COPY tables aborts the run: add its entry first.

Static site, vanilla HTML/CSS/JS, no build step. To preview locally: `python3 -m http.server` and open `http://localhost:8000`.

## License

License: CC BY 4.0 for samples, except OpenStreetMap-derived samples (ODbL 1.0, © OpenStreetMap contributors). Full data licensed per purchase. Upstream sources credited per dataset page: nflverse (CC BY 4.0), HUD (public domain), Inside Airbnb (CC BY 4.0), Eurostat (CC BY 4.0), World Bank Open Data (CC BY 4.0), OpenStreetMap contributors (ODbL 1.0), superteam.fun (harvested API data). If you republish samples, credit "Data Vault (jayjex.github.io/data-vault)" plus the upstream source and its license (CC BY 4.0, or ODbL 1.0 for OpenStreetMap data).

---

Data Vault is a Matchbook Labs project · [github.com/jayjex](https://github.com/jayjex)
