#!/usr/bin/env python3
"""ETL: HUD Fair Market Rents FY2027, top-50 metro FMR areas by ZIP coverage.

Source: fmr-by-zip-2027.csv (51871 ZIP rows parsed from FY27_FMRs.xlsx +
fy2027_safmrs.xlsx, already in artifacts/products/hud-dataset/). No new download.
License: public domain (US government data).
Rerunnable: python3 tools/etl-hud-fmr-metro-2027.py
"""
import csv
import json
import os
import statistics
from collections import defaultdict

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = "/home/uwuki/money-mission/artifacts/products/hud-dataset/fmr-by-zip-2027.csv"
OUT = os.path.join(ROOT, "data", "hud-fmr-metro-2027")

SLUG = "hud-fmr-metro-2027"
NAME = "HUD Fair Market Rents FY2027, Top-50 Metro Areas"
BR = ["fmr_0br", "fmr_1br", "fmr_2br", "fmr_3br", "fmr_4br"]
COLS = ["metro_code", "metro_name", "state", "zip_count"] + [b + "_median" for b in BR]


def main():
    with open(SRC, newline="") as f:
        rows = [r for r in csv.DictReader(f) if r["metro"] == "metro"]

    by_code = defaultdict(list)
    for r in rows:
        by_code[r["hud_area_code"]].append(r)

    records = []
    for code, rs in by_code.items():
        names = set(r["area_name"] for r in rs)
        states = set(r["state"] for r in rs)
        assert len(names) == 1 and len(states) == 1, (code, names, states)
        rec = {
            "metro_code": code,
            "metro_name": rs[0]["area_name"],
            "state": rs[0]["state"],
            "zip_count": len(rs),
        }
        for b in BR:
            rec[b + "_median"] = int(statistics.median(int(r[b]) for r in rs))
        records.append(rec)

    records.sort(key=lambda r: (-r["zip_count"], r["metro_code"]))
    top = records[:50]

    pricey = sorted(records, key=lambda r: (-r["fmr_2br_median"], r["metro_code"]))[:50]

    os.makedirs(OUT, exist_ok=True)

    with open(os.path.join(OUT, "fmr-metro-2027.csv"), "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=COLS)
        w.writeheader()
        w.writerows(top)

    with open(os.path.join(OUT, "most-expensive-2br.csv"), "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=COLS)
        w.writeheader()
        w.writerows(pricey)

    with open(os.path.join(OUT, "sample.csv"), "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=COLS)
        w.writeheader()
        w.writerows(top[:12])

    sample = {
        "slug": SLUG,
        "name": NAME,
        "columns": COLS,
        "row_count": len(top),
        "records": top[:12],
    }
    with open(os.path.join(OUT, "sample.json"), "w") as f:
        json.dump(sample, f, indent=1)

    n_all = len(records)
    pricey = sorted(records, key=lambda r: (-r["fmr_2br_median"], r["metro_code"]))[:50]
    n_overlap = len(set(r["metro_code"] for r in top) & set(r["metro_code"] for r in pricey))
    med_all = int(statistics.median(r["fmr_2br_median"] for r in records))
    top_zip_share = sum(r["zip_count"] for r in top)
    total_zips = sum(r["zip_count"] for r in records)

    with open(os.path.join(OUT, "schema.md"), "w") as f:
        f.write(f"""# {NAME} — schema

Source: FY2027 Fair Market Rent ZIP-level file (51,871 ZIP rows parsed from
FY27_FMRs.xlsx plus the FY2027 small-area FMR file, effective October 1, 2026),
already published in the hud-fmr-2027 pack. The metro rows here are recomputed
from that file, not copied from any HUD summary. No new download. License:
public domain (US government data). The full FY2027 FMR list has 649 metro FMR
areas; this pack keeps the 50 with the most ZIP codes, which together cover
{top_zip_share:,} of the {total_zips:,} metro-assigned ZIPs.

## fmr-metro-2027.csv ({len(top)} rows)
| column | type | meaning |
|---|---|---|
| metro_code | text | HUD metro FMR area code (e.g. METRO35620MM5600) |
| metro_name | text | HUD area name, verbatim (e.g. "New York, NY HUD Metro FMR Area") |
| state | text | two-letter state or territory code |
| zip_count | int | FY2027 ZIP rows inside the area |
| fmr_0br_median ... fmr_4br_median | int | median FY2027 FMR in dollars across the area's ZIPs, per bedroom size |

## Selection and aggregation
- Rows with the ZIP-level `metro` flag only; nonmetro and county-level
  small-area rows are excluded.
- One area = one hud_area_code. Each code has exactly one name and one state
  in the source file, checked at build time (asserted).
- Per area and bedroom size, the value is the integer median of the ZIP FMRs
  (statistics.median of ints; when the ZIP count is even the two middle values
  are averaged then floored by int()). Areas are ranked by zip_count
  descending, tie-broken by metro_code, and the top 50 are kept.

## most-expensive-2br.csv ({len(pricey)} rows)
Same columns. The 50 areas with the highest fmr_2br_median across all 649
metro areas, sorted by fmr_2br_median descending, tie-broken by metro_code.
Only {n_overlap} of these 50 overlap with the ZIP-coverage top 50, so the two files
answer different questions.

## Caveats
- The aggregate is a median across the area's ZIPs, which weights every ZIP
  equally. It is not a ZIP-count-weighted average and not the official 40th
  percentile FMR HUD publishes at the area level.
- Puerto Rico areas (state PR) are in the source and were eligible for both
  rankings; none made the ZIP-coverage top 50.
- Rates are effective October 1, 2026 and reflect the FY2027 files HUD
  published in 2026; HUD can revise them mid-cycle.
""")

    by_name = {r["metro_name"]: r for r in pricey}
    stats = {
        "rows_main": len(top),
        "rows_expensive": len(pricey),
        "metro_areas_total": n_all,
        "zip_rows_source": 51871,
        "top50_zip_share": top_zip_share,
        "total_metro_zips": total_zips,
        "median_2br_across_649_metros": med_all,
        "most_expensive_2br": [(r["metro_name"], r["fmr_2br_median"]) for r in pricey[:5]],
        "most_expensive_2br_50th": pricey[-1]["fmr_2br_median"],
        "overlap_two_rankings": n_overlap,
        "cheapest_in_top50_2br": min(r["fmr_2br_median"] for r in top),
        "cheapest_in_top50_name": min(top, key=lambda r: r["fmr_2br_median"])["metro_name"],
        "new_york": by_name["New York, NY HUD Metro FMR Area"],
        "los_angeles": by_name["Los Angeles-Long Beach-Glendale, CA HUD Metro FMR Area"],
    }
    with open(os.path.join(OUT, "etl-stats.json"), "w") as f:
        json.dump(stats, f, indent=1)
    print(json.dumps(stats, indent=1))
    print("top 3 coverage:", [(r["metro_name"], r["zip_count"], r["fmr_2br_median"]) for r in top[:3]])
    print("top 5 expensive:", [(r["metro_name"], r["fmr_2br_median"]) for r in pricey[:5]])


if __name__ == "__main__":
    main()
