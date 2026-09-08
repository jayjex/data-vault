#!/usr/bin/env python3
"""ETL: World Bank SP.POP.TOTL for G20 countries + EU27, 1960-2025.

Source: World Bank API v2, keyless JSON (saved at tmp/etl-wb-g20/wb-pop.json).
License: World Bank Open Data, CC BY 4.0.
Rerunnable: python3 tools/etl-wb-g20-population.py
"""
import csv
import json
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "tmp", "etl-wb-g20", "wb-pop.json")
OUT = os.path.join(ROOT, "data-vault", "data", "worldbank-g20-population")

SLUG = "worldbank-g20-population"
NAME = "World Bank Population, G20 Countries + EU27, 1960-2025"

def main():
    with open(SRC) as f:
        meta, rows = json.load(f)
    assert meta["total"] == len(rows), f"meta {meta['total']} != rows {len(rows)}"

    os.makedirs(OUT, exist_ok=True)

    # long CSV: entity, iso3, year, population
    records = []
    for r in rows:
        v = r["value"]
        if v is None:
            continue
        records.append({
            "entity": r["country"]["value"],
            "iso3": r["countryiso3code"],
            "year": int(r["date"]),
            "population": int(v),
        })
    records.sort(key=lambda x: (x["iso3"], x["year"]))
    with open(os.path.join(OUT, "g20-population.csv"), "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["entity", "iso3", "year", "population"])
        w.writeheader()
        w.writerows(records)

    # latest-year summary CSV
    by_iso = {}
    for r in records:
        if r["iso3"] not in by_iso or r["year"] > by_iso[r["iso3"]]["year"]:
            by_iso[r["iso3"]] = r
    latest_rows = sorted(by_iso.values(), key=lambda x: -x["population"])
    with open(os.path.join(OUT, "g20-population-2025.csv"), "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["entity", "iso3", "year", "population"])
        for r in latest_rows:
            w.writerow([r["entity"], r["iso3"], r["year"], r["population"]])

    # sample.csv: first 20 rows of long CSV (Argentina 1960-1979)
    with open(os.path.join(OUT, "sample.csv"), "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["entity", "iso3", "year", "population"])
        w.writeheader()
        w.writerows(records[:20])

    sample = {
        "slug": SLUG,
        "name": NAME,
        "columns": ["entity", "iso3", "year", "population"],
        "row_count": len(records),
        "records": records[:20],
    }
    with open(os.path.join(OUT, "sample.json"), "w") as f:
        json.dump(sample, f, indent=1)

    # schema.md
    with open(os.path.join(OUT, "schema.md"), "w") as f:
        f.write(f"""# {NAME} — schema

Source: World Bank API v2, indicator SP.POP.TOTL (Population, total), WDI series,
retrieved 2026-09-10. Source license CC BY 4.0; this pack stays CC BY 4.0.
Entity list: the 19 national G20 members plus the European Union aggregate (ISO3 EUU,
EU27 grouping). Missing-value convention: years where the World Bank reports no value
are dropped from the CSV (none in the 1960-2025 window for these 20 entities).

## g20-population.csv (long format, {len(records)} rows)
| column | type | meaning |
|---|---|---|
| entity | text | World Bank country name (e.g. "Korea, Rep.", "Turkiye", "European Union") |
| iso3 | text | World Bank ISO3 code (EUU = EU27 aggregate) |
| year | int | observation year, 1960-2025 |
| population | int | total population, persons (SP.POP.TOTL) |

## g20-population-2025.csv ({len(latest_rows)} rows)
Latest observation per entity, sorted by population descending. All rows are year 2025.

## Normalization
- Values parsed from the API JSON and cast to int; no rounding, no imputation.
- Entity names kept verbatim from the World Bank ("Korea, Rep.", "Turkiye",
  "Russian Federation").
- One row per entity-year; every entity has a full 1960-2025 run (66 values).

## Caveats
- EU27 aggregate (EUU) is not a country; exclude it when summing national members.
- South Africa's series ends at the World Bank's latest WDI update (2025); the
  retrieval date is stamped above.
- 2025 observations reflect World Bank estimates as of the WDI database update of
  2026-07-13 and can be revised.
""")

    # stats for page/report
    china = {r["year"]: r["population"] for r in records if r["iso3"] == "CHN"}
    india = {r["year"]: r["population"] for r in records if r["iso3"] == "IND"}
    cross = next((y for y in sorted(china) if india[y] > china[y] and india[y - 1] <= china[y - 1]), None)
    mult = {}
    for iso in by_iso:
        y0 = next(r["population"] for r in records if r["iso3"] == iso and r["year"] == 1960)
        mult[by_iso[iso]["entity"]] = by_iso[iso]["population"] / y0
    top_mult = sorted(mult.items(), key=lambda x: -x[1])[:3]
    stats = {
        "rows_long": len(records),
        "rows_2025": len(latest_rows),
        "crossover_india_china": cross,
        "top_2025": [(r["entity"], r["population"]) for r in latest_rows[:5]],
        "multipliers_1960_2025": top_mult,
        "usa_2025": by_iso["USA"]["population"],
        "euu_2025": by_iso["EUU"]["population"],
        "jpn_2025": by_iso["JPN"]["population"],
        "rus_2025": by_iso["RUS"]["population"],
    }
    print(json.dumps(stats, indent=1))
    with open(os.path.join(OUT, "etl-stats.json"), "w") as f:
        json.dump(stats, f, indent=1)

if __name__ == "__main__":
    main()
