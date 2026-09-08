#!/usr/bin/env python3
"""Eurostat ETL: unemployment rate by sex and age (une_rt_a, annual) -> clean CSV.

Source: Eurostat dissemination API (keyless GET, JSON-stat 2.0).
License: CC BY 4.0 (http://spdx.org/licenses/CC-BY-4.0), rights PUBLIC.
Output: data/eurostat/unemployment/
"""
import csv
import json
import os
import urllib.request

BASE = "https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/{code}?format=JSON&lang=EN"
OUT = os.path.join(os.path.dirname(__file__), "..", "data", "eurostat", "unemployment")
GEOS = ["EU27_2020", "EA20", "DE", "EL", "ES", "FR", "IT", "NL", "PL", "SE"]
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
        dims[name] = {v: k for k, v in idx.items()}
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

    # Unemployment rate, annual (une_rt_a), unit PC_ACT
    print("une_rt_a PC_ACT ...")
    q = "".join(f"&unit=PC_ACT&geo={g}" for g in GEOS)
    d = fetch(BASE.format(code="une_rt_a") + q)
    une = rows_from_jsonstat(d, keep_dims={"geo", "sex", "age", "time"})
    for r in une:
        r["year"] = r.pop("time")
        r["geo"] = r["geo"].replace("EU27_2020", "EU27")
    une.sort(key=lambda r: (r["year"], r["geo"], r["age"], r["sex"]))
    cols = ["year", "geo", "sex", "age", "value", "geo_label", "sex_label", "age_label"]
    write_csv(os.path.join(OUT, "unemployment-rate.csv"), cols, une)
    write_sample(OUT, "eurostat-unemployment", "Eurostat Unemployment Rate by Sex and Age, EU27 + 9 Countries, 2003-2025", cols, une)
    print(f"  rows={len(une)} years={min(r['year'] for r in une)}-{max(r['year'] for r in une)} geos={len(set(r['geo'] for r in une))}")
    sanity("unemployment rate %, total age Y15-74", [r for r in une if r["age"] == "Y15-74"], 0, 40)
    sanity("unemployment rate %, all bands incl youth", une, 0, 70)

    print("done. output in data/eurostat/unemployment/")

if __name__ == "__main__":
    main()
