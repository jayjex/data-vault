#!/usr/bin/env python3
"""Eurostat ETL: pull house price index + HICP rents (NL, EU27) -> clean CSVs.

Source: Eurostat dissemination API (keyless GET, JSON-stat 2.0).
License: CC BY 4.0 (http://spdx.org/licenses/CC-BY-4.0), rights PUBLIC.
Output: data/eurostat/{house-prices,rents}/
"""
import csv
import json
import os
import urllib.request

BASE = "https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/{code}?format=JSON&lang=EN"
OUT = os.path.join(os.path.dirname(__file__), "..", "data", "eurostat")
GEOS = ["NL", "EU27_2020"]
SAMPLE_N = 22


def fetch(url):
    req = urllib.request.Request(url, headers={"User-Agent": "data-vault-etl/1.0"})
    with urllib.request.urlopen(req, timeout=60) as r:
        return json.loads(r.read().decode("utf-8"))


def rows_from_jsonstat(d, keep_dims):
    """Decode JSON-stat 2.0 into list of dicts. value keys are linear indices."""
    order = d["id"]
    size = d["size"]
    dims = {}
    for name in order:
        idx = d["dimension"][name]["category"]["index"]
        dims[name] = {v: k for k, v in idx.items()}  # position -> code
    labels = {n: d["dimension"][n]["category"]["label"] for n in order}
    rows = []
    n = len(order)
    for k, val in d["value"].items():
        k = int(k)
        rec = {}
        for pos in range(n - 1, -1, -1):
            name = order[pos]
            dim_at = k % size[pos]
            k //= size[pos]
            code = dims[name][dim_at]
            if name in keep_dims:
                rec[name] = code
                rec[name + "_label"] = labels[name].get(code, code)
        rec["value"] = val
        rows.append(rec)
    return rows


def write_csv(path, columns, rows):
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=columns, extrasaction="ignore")
        w.writeheader()
        w.writerows(rows)


def write_sample(dirpath, slug, name, columns, rows):
    os.makedirs(dirpath, exist_ok=True)
    write_csv(os.path.join(dirpath, "sample.csv"), columns, rows[:SAMPLE_N])
    sample = {
        "slug": slug,
        "name": name,
        "columns": columns,
        "row_count": len(rows),
        "records": rows[:SAMPLE_N],
    }
    with open(os.path.join(dirpath, "sample.json"), "w", encoding="utf-8") as f:
        json.dump(sample, f, indent=1, ensure_ascii=False)


def sanity(name, rows, lo, hi, key="value"):
    vals = [r[key] for r in rows if r.get(key) is not None]
    bad = [v for v in vals if not (lo <= v <= hi)]
    print(f"  sanity {name}: n={len(vals)} min={min(vals)} max={max(vals)} out-of-range={len(bad)}")
    assert not bad, f"{name}: values outside [{lo},{hi}]: {bad[:5]}"


def main():
    os.makedirs(OUT, exist_ok=True)

    # 1. House price index (prc_hpi_a), annual
    print("prc_hpi_a ...")
    d = fetch(BASE.format(code="prc_hpi_a") + "&geo=NL&geo=EU27_2020")
    hpi = rows_from_jsonstat(d, keep_dims={"geo", "unit", "time", "purchase"})
    for r in hpi:
        r["year"] = r.pop("time")
        r["geo"] = r["geo"].replace("EU27_2020", "EU27")
    cols = ["year", "geo", "purchase", "unit", "value", "geo_label", "purchase_label", "unit_label"]
    hp = os.path.join(OUT, "house-prices")
    os.makedirs(hp, exist_ok=True)
    write_csv(os.path.join(hp, "house-price-index.csv"), cols, hpi)
    write_sample(hp, "eurostat-house-prices", "Eurostat House Price Index, NL & EU27, 2005-2025", cols, hpi)
    print(f"  rows={len(hpi)} years={min(r['year'] for r in hpi)}-{max(r['year'] for r in hpi)}")
    sanity("HPI index 2015=100", [r for r in hpi if r["unit"] == "I15_A_AVG"], 40, 220)
    sanity("HPI rate of change %", [r for r in hpi if r["unit"] == "RCH_A_AVG"], -30, 30)

    # 2. HICP actual rentals CP0411: monthly index (prc_hicp_midx)
    print("prc_hicp_midx CP0411 ...")
    d = fetch(BASE.format(code="prc_hicp_midx") + "&coicop=CP0411&geo=NL&geo=EU27_2020")
    mi = rows_from_jsonstat(d, keep_dims={"geo", "unit", "time"})
    for r in mi:
        r["month"] = r.pop("time")
        r["geo"] = r["geo"].replace("EU27_2020", "EU27")
    cols_mi = ["month", "geo", "unit", "value", "geo_label", "unit_label"]
    rt = os.path.join(OUT, "rents")
    os.makedirs(rt, exist_ok=True)
    write_csv(os.path.join(rt, "rent-index-monthly.csv"), cols_mi, mi)
    print(f"  rows={len(mi)} months={min(r['month'] for r in mi)}-{max(r['month'] for r in mi)}")
    sanity("rent index", mi, 50, 180)

    # 3. HICP actual rentals CP0411: annual rate of change (prc_hicp_manr)
    print("prc_hicp_manr CP0411 ...")
    d = fetch(BASE.format(code="prc_hicp_manr") + "&coicop=CP0411&geo=NL&geo=EU27_2020")
    ma = rows_from_jsonstat(d, keep_dims={"geo", "unit", "time"})
    for r in ma:
        r["month"] = r.pop("time")
        r["geo"] = r["geo"].replace("EU27_2020", "EU27")
    write_csv(os.path.join(rt, "rent-annual-rate.csv"), cols_mi, ma)
    write_sample(rt, "eurostat-rents", "Eurostat HICP Actual Rents, NL & EU27, CP0411", cols_mi, ma)
    print(f"  rows={len(ma)} months={min(r['month'] for r in ma)}-{max(r['month'] for r in ma)}")
    sanity("rent annual rate %", ma, -10, 15)

    print("done. output in data/eurostat/")


if __name__ == "__main__":
    main()
