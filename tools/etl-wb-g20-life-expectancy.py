#!/usr/bin/env python3
"""ETL: World Bank SP.DYN.LE00.IN life expectancy for G20 countries + EU27, 1960-2024.

Source: World Bank API v2, keyless JSON (saved at tmp/etl-wb-le/wb-le.json).
License: World Bank Open Data, CC BY 4.0.
Rerunnable: python3 tools/etl-wb-g20-life-expectancy.py
"""
import csv
import json
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "tmp", "etl-wb-le", "wb-le.json")
OUT = os.path.join(ROOT, "data", "worldbank-g20-life-expectancy")

SLUG = "worldbank-g20-life-expectancy"
NAME = "World Bank Life Expectancy, G20 Countries + EU27, 1960-2024"

G20 = ["ARG", "AUS", "BRA", "CAN", "CHN", "FRA", "DEU", "IND", "IDN", "ITA",
       "JPN", "KOR", "MEX", "RUS", "SAU", "ZAF", "TUR", "GBR", "USA", "EUU"]


def main():
    with open(SRC) as f:
        meta, rows = json.load(f)

    os.makedirs(OUT, exist_ok=True)

    # long CSV: entity, iso3, year, life_expectancy_years (2dp)
    records = []
    for r in rows:
        v = r["value"]
        if v is None or r["countryiso3code"] not in G20:
            continue
        records.append({
            "entity": r["country"]["value"],
            "iso3": r["countryiso3code"],
            "year": int(r["date"]),
            "life_expectancy_years": round(v, 2),
        })
    records.sort(key=lambda x: (x["iso3"], x["year"]))
    with open(os.path.join(OUT, "g20-life-expectancy.csv"), "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["entity", "iso3", "year", "life_expectancy_years"])
        w.writeheader()
        w.writerows(records)

    # latest-year summary CSV
    by_iso = {}
    for r in records:
        if r["iso3"] not in by_iso or r["year"] > by_iso[r["iso3"]]["year"]:
            by_iso[r["iso3"]] = r
    latest_rows = sorted(by_iso.values(), key=lambda x: -x["life_expectancy_years"])
    with open(os.path.join(OUT, "g20-life-expectancy-2024.csv"), "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["entity", "iso3", "year", "life_expectancy_years"])
        for r in latest_rows:
            w.writerow([r["entity"], r["iso3"], r["year"], r["life_expectancy_years"]])

    # sample.csv: first 20 rows of long CSV (Argentina 1960-1979)
    with open(os.path.join(OUT, "sample.csv"), "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["entity", "iso3", "year", "life_expectancy_years"])
        w.writeheader()
        w.writerows(records[:20])

    sample = {
        "slug": SLUG,
        "name": NAME,
        "columns": ["entity", "iso3", "year", "life_expectancy_years"],
        "row_count": len(records),
        "records": records[:20],
    }
    with open(os.path.join(OUT, "sample.json"), "w") as f:
        json.dump(sample, f, indent=1)

    # schema.md
    with open(os.path.join(OUT, "schema.md"), "w") as f:
        f.write(f"""# {NAME} — schema

Source: World Bank API v2, indicator SP.DYN.LE00.IN (Life expectancy at birth, total
years), WDI series, retrieved 2026-09-10. Source license CC BY 4.0; this pack stays
CC BY 4.0. Entity list: the 19 national G20 members plus the European Union aggregate
(ISO3 EUU, EU27 grouping), same as the SP.POP.TOTL and SP.RUR.TOTL.ZS sibling packs.
Missing-value convention: years where the World Bank reports no value are dropped
from the CSV. The WDI series for these 20 entities runs 1960-2024 (no 2025 value
published yet), 65 observations per entity, 1,300 rows total.

## g20-life-expectancy.csv (long format, {len(records)} rows)
| column | type | meaning |
|---|---|---|
| entity | text | World Bank country name (e.g. "Korea, Rep.", "Turkiye", "European Union") |
| iso3 | text | World Bank ISO3 code (EUU = EU27 aggregate) |
| year | int | observation year, 1960-2024 |
| life_expectancy_years | float | life expectancy at birth in years (SP.DYN.LE00.IN), rounded to 2 decimals from the API's full precision |

## g20-life-expectancy-2024.csv ({len(latest_rows)} rows)
Latest observation per entity, sorted by life expectancy descending. All rows are
year 2024.

## Normalization
- Values parsed from the API JSON and rounded to 2 decimal places; the underlying
  WDI series itself is an annual estimate, so the two decimals carry no extra
  precision. No imputation; gaps would be dropped, and none occur in this window.
- Entity names kept verbatim from the World Bank ("Korea, Rep.", "Turkiye",
  "Russian Federation").
- One row per entity-year; every entity has a full 1960-2024 run (65 values).

## Caveats
- The series runs through 2024, not 2025: WDI publishes life expectancy with a
  longer lag than the population counts, and no 2025 value existed at retrieval.
- SP.DYN.LE00.IN is the total-population (both sexes) series. The World Bank also
  publishes SP.DYN.LE00.FE.IN and SP.DYN.LE00.MA.IN separately; those are not in
  this pack.
- The 2020-2021 rows carry the COVID-19 mortality shock in most members; year-over
  -year comparisons across that window are not comparable to normal years.
- EU27 aggregate (EUU) is not a country; exclude it when ranking national members.
- 2024 observations reflect the WDI database update of 2026-07-13 and can be revised.
""")

    # stats for page/report
    def series(iso):
        return {r["year"]: r["life_expectancy_years"] for r in records if r["iso3"] == iso}

    names = {r["iso3"]: r["entity"] for r in records}
    g20 = list(by_iso)
    # who leads each year
    leaders = {}
    for y in range(1960, 2025):
        vals = {i: series(i).get(y) for i in g20}
        vals = {i: v for i, v in vals.items() if v is not None}
        if vals:
            top = max(vals, key=vals.get)
            leaders.setdefault(top, []).append(y)

    gains = {}
    for i in g20:
        s = series(i)
        y0, y1 = min(s), max(s)
        gains[names[i]] = (s[y0], s[y1], round(s[y1] - s[y0], 2))

    stats = {
        "rows_long": len(records),
        "rows_2024": len(latest_rows),
        "wdi_lastupdated": meta["lastupdated"],
        "top_2024": [(r["entity"], r["life_expectancy_years"]) for r in latest_rows[:5]],
        "bottom_2024": [(r["entity"], r["life_expectancy_years"]) for r in latest_rows[-3:]],
        "japan_leader_since": min(leaders["JPN"]),
        "japan_leader_years": len(leaders["JPN"]),
        "canada_leader_years": len(leaders.get("CAN", [])),
        "gains_1960_2024_top": sorted(gains.items(), key=lambda kv: -kv[1][2])[:3],
        "china_min_1960": series("CHN")[1960],
        "russia_trough_1994": series("RUS")[1994],
        "russia_recovered_1960_level": next(y for y in sorted(series("RUS")) if y > 1995 and series("RUS")[y] > series("RUS")[1960]),
        "usa_2021_dip": series("USA")[2021],
        "usa_recovered_2019_level": next(y for y in sorted(series("USA")) if y > 2019 and series("USA")[y] > series("USA")[2019]),
        "not_record_2024": [(names[i], max(series(i), key=series(i).get)) for i in g20 if max(series(i)) == 2024 and series(i)[2024] < max(series(i).values())],
    }
    print(json.dumps(stats, indent=1))
    with open(os.path.join(OUT, "etl-stats.json"), "w") as f:
        json.dump(stats, f, indent=1)


if __name__ == "__main__":
    main()
