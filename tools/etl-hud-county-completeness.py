#!/usr/bin/env python3
"""HUD FMR FY2026 county completeness ETL.

Reads the shared source CSV (fiatdock-endpoint/data/hud-fmr-county-2026.csv,
one row per county equivalent, median+max for 0-4BR) and emits:

  data/hud-fmr-county-2026/fmr-county-2026.csv    full copy, verbatim source rows
  data/hud-fmr-county-2026/spread-counties.csv    the 8 counties where max != median
  data/hud-fmr-county-2026/sample.csv             first 22 rows
  data/hud-fmr-county-2026/sample.json            {slug, name, columns[], row_count, records[]}

Stdlib only. Rerunnable. Source: HUD FY2026 FMR release (US government, public domain).
"""
import csv
import json
import os

SRC = os.path.join(os.path.dirname(__file__), "..", "..", "fiatdock-endpoint", "data", "hud-fmr-county-2026.csv")
OUT = os.path.join(os.path.dirname(__file__), "..", "data", "hud-fmr-county-2026")

SLUG = "hud-fmr-county-2026"
NAME = "HUD Fair Market Rents FY2026 by County: completeness & spread"

NUM_COLS = [c for c in (
    "fmr_0br_median", "fmr_0br_max", "fmr_1br_median", "fmr_1br_max",
    "fmr_2br_median", "fmr_2br_max", "fmr_3br_median", "fmr_3br_max",
    "fmr_4br_median", "fmr_4br_max") ]


def main():
    os.makedirs(OUT, exist_ok=True)
    with open(SRC, newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    cols = list(rows[0].keys())

    # --- verbatim full copy ---
    with open(os.path.join(OUT, "fmr-county-2026.csv"), "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=cols)
        w.writeheader()
        w.writerows(rows)

    # --- spread counties: fmr_2br_max > fmr_2br_median ---
    spread = []
    for r in rows:
        med, mx = int(r["fmr_2br_median"]), int(r["fmr_2br_max"])
        if mx > med:
            spread.append({
                "state": r["state"], "state_name": r["state_name"],
                "county": r["county"], "metro": r["metro"],
                "fmr_2br_median": r["fmr_2br_median"], "fmr_2br_max": r["fmr_2br_max"],
                "gap_2br": mx - med, "gap_pct_2br": round((mx / med - 1) * 100, 1),
                "area_rows": r["area_rows"],
            })
    spread.sort(key=lambda x: -x["gap_2br"])
    scols = list(spread[0].keys())
    with open(os.path.join(OUT, "spread-counties.csv"), "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=scols)
        w.writeheader()
        w.writerows(spread)

    # --- sample (first 22 rows, verbatim) ---
    sample = rows[:22]
    with open(os.path.join(OUT, "sample.csv"), "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=cols)
        w.writeheader()
        w.writerows(sample)
    payload = {"slug": SLUG, "name": NAME, "columns": cols, "row_count": len(rows),
               "records": [dict(r) for r in sample]}
    with open(os.path.join(OUT, "sample.json"), "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=1)

    # --- summary numbers for the landing page (all recomputed here) ---
    empties = sum(1 for r in rows for c in NUM_COLS if r[c].strip() == "")
    states = sorted({r["state"] for r in rows})
    metro = sum(1 for r in rows if r["metro"] == "metro")
    eq = sum(1 for r in rows if int(r["fmr_2br_max"]) == int(r["fmr_2br_median"]))
    multi = [r for r in rows if int(r["area_rows"]) > 1]
    med2 = sorted(int(r["fmr_2br_median"]) for r in rows)[len(rows) // 2]
    ladders = [int(r["fmr_4br_median"]) / int(r["fmr_0br_median"]) for r in rows if int(r["fmr_0br_median"]) > 0]
    ladders.sort()
    print("rows=%d states=%d metro=%d nonmetro=%d empty_cells=%d" % (len(rows), len(states), metro, len(rows) - metro, empties))
    print("2br max==median: %d of %d; spread counties: %d" % (eq, len(rows), len(spread)))
    print("national 2br median (counties): $%d" % med2)
    print("area_rows>1 counties: %d; sum area_rows: %d" % (len(multi), sum(int(r["area_rows"]) for r in rows)))
    print("4br/0br median ratio: median %.2f min %.2f max %.2f" % (ladders[len(ladders) // 2], ladders[0], ladders[-1]))


if __name__ == "__main__":
    main()
