#!/usr/bin/env python3
"""Airbnb 8 new US cities ETL.

Reads eight per-city source CSVs (visualisations/listings.csv format from
Inside Airbnb snapshots, June 2026, expected as tmp/etl-airbnb8/airbnb-<city>.csv)
and emits, into data/airbnb-eight-cities/:

  airbnb-<city>.csv   one file per city, 12-column schema shared with airbnb-six-cities
  cities-index.csv    one row per city: city, snapshot_date, rows, file, median_price_usd, room_type_mix
  sample.csv          first 20 rows (Boston)
  sample.json         {slug, name, columns[], row_count, records[]}

Normalization: source rows carry host_id, host_profile_id, host_name,
neighbourhood_group, calculated_host_listings_count, number_of_reviews_ltm and
license columns; those are dropped. Kept columns (same order as airbnb-six-cities):
id, name, neighbourhood, latitude, longitude, room_type, price, minimum_nights,
availability_365, number_of_reviews, reviews_per_month, last_review. Prices are
kept as the source floats; listings with no price keep the empty cell.

Stdlib only. Rerunnable. Source: Inside Airbnb, CC BY 4.0.
"""
import csv
import json
import os
import statistics

HERE = os.path.dirname(os.path.abspath(__file__))
SRC_DIR = os.path.join(HERE, "..", "..", "tmp", "etl-airbnb8")
OUT = os.path.join(HERE, "..", "data", "airbnb-eight-cities")

SLUG = "airbnb-eight-cities"
NAME = "Airbnb Listings, 8 More US Cities"

CITIES = [
    # slug, label, state label, snapshot date
    ("boston", "Boston, MA", "2026-06-15"),
    ("chicago", "Chicago, IL", "2026-06-24"),
    ("los-angeles", "Los Angeles, CA", "2026-06-15"),
    ("new-orleans", "New Orleans, LA", "2026-06-16"),
    ("portland", "Portland, OR", "2026-06-15"),
    ("san-francisco", "San Francisco, CA", "2026-06-14"),
    ("seattle", "Seattle, WA", "2026-06-15"),
    ("washington-dc", "Washington, DC", "2026-06-24"),
]

KEEP = ["id", "name", "neighbourhood", "latitude", "longitude", "room_type",
        "price", "minimum_nights", "availability_365", "number_of_reviews",
        "reviews_per_month", "last_review"]


def price_num(raw):
    raw = (raw or "").strip().replace("$", "").replace(",", "")
    try:
        return float(raw)
    except ValueError:
        return None


def main():
    os.makedirs(OUT, exist_ok=True)
    index_rows = []
    per_city = {}
    for slug, label, date in CITIES:
        src = os.path.join(SRC_DIR, "airbnb-%s.csv" % slug)
        with open(src, newline="", encoding="utf-8") as f:
            rows = list(csv.DictReader(f))
        keep_rows = [{k: (r.get(k) or "") for k in KEEP} for r in rows]
        dst = os.path.join(OUT, "airbnb-%s.csv" % slug)
        with open(dst, "w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=KEEP)
            w.writeheader()
            w.writerows(keep_rows)
        prices = sorted(p for p in (price_num(r["price"]) for r in keep_rows) if p is not None)
        mix = {}
        for r in keep_rows:
            mix[r["room_type"]] = mix.get(r["room_type"], 0) + 1
        total = len(keep_rows)
        mix_str = ", ".join(
            "%s %d (%d%%)" % (rt, n, round(100 * n / total))
            for rt, n in sorted(mix.items(), key=lambda x: -x[1]))
        index_rows.append({
            "city": label, "snapshot_date": date, "rows": total,
            "file": "airbnb-%s.csv" % slug,
            "median_price_usd": int(statistics.median(prices)),
            "room_type_mix": mix_str,
        })
        per_city[slug] = (keep_rows, prices)

    index_path = os.path.join(OUT, "cities-index.csv")
    with open(index_path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(index_rows[0].keys()))
        w.writeheader()
        w.writerows(index_rows)

    sample_slug = CITIES[0][0]
    sample_rows = per_city[sample_slug][0][:20]
    sample_cols = KEEP
    with open(os.path.join(OUT, "sample.csv"), "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=sample_cols)
        w.writeheader()
        w.writerows(sample_rows)
    payload = {"slug": SLUG, "name": NAME, "columns": sample_cols,
               "row_count": len(sample_rows), "records": [dict(r) for r in sample_rows]}
    with open(os.path.join(OUT, "sample.json"), "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=1)

    # --- summary numbers for the landing page ---
    grand = sum(len(v[0]) for v in per_city.values())
    print("cities=%d total_rows=%d" % (len(CITIES), grand))
    for row in index_rows:
        print("  %(city)s rows=%(rows)d median=$%(median_price_usd)d" % row)
    all_prices = sorted(p for v in per_city.values() for p in v[1])
    print("8-city combined median=$%d" % statistics.median(all_prices))
    print("price empties: %d of %d rows" % (
        sum(1 for v in per_city.values() for r in v[0] if price_num(r["price"]) is None), grand))
    rt = {}
    for v in per_city.values():
        for r in v[0]:
            rt[r["room_type"]] = rt.get(r["room_type"], 0) + 1
    print("room types:", ", ".join("%s %d" % kv for kv in sorted(rt.items(), key=lambda x: -x[1])))
    print("column check:", all(sorted(keep_rows[0].keys()) == sorted(KEEP) for keep_rows, _ in per_city.values()))


if __name__ == "__main__":
    main()
