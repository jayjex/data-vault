#!/usr/bin/env python3
"""Eurostat ETL: unemployment rate by sex (une_rt_m, monthly) -> clean CSV.

Source: Eurostat dissemination API (keyless GET, JSON-stat 2.0).
License: CC BY 4.0 (http://spdx.org/licenses/CC-BY-4.0), rights PUBLIC.
Output: data/eurostat/unemployment-monthly/
"""
import csv
import json
import os
import urllib.request

BASE = "https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/{code}?format=JSON&lang=EN"
OUT = os.path.join(os.path.dirname(__file__), "..", "data", "eurostat", "unemployment-monthly")
GEOS = ["EU27_2020", "DE", "EL", "ES", "FR", "IT", "NL", "PL", "SE"]
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

def sanity(name, rows, lo, hi, key="value"):
    vals = [r[key] for r in rows if r.get(key) is not None]
    bad = [v for v in vals if not (lo <= v <= hi)]
    print(f"  sanity {name}: n={len(vals)} min={min(vals)} max={max(vals)} out-of-range={len(bad)}")
    assert not bad, f"{name}: values outside [{lo},{hi}]: {bad[:5]}"

def main():
    os.makedirs(OUT, exist_ok=True)

    # Unemployment rate, monthly (une_rt_m), seasonally adjusted, unit PC_ACT, age TOTAL
    print("une_rt_m PC_ACT SA TOTAL ...")
    q = "".join(f"&geo={g}" for g in GEOS)
    url = (BASE.format(code="une_rt_m")
           + "&sinceTimePeriod=2003-01&unit=PC_ACT&s_adj=SA&age=TOTAL&sex=T&sex=F&sex=M" + q)
    d = fetch(url)
    une = rows_from_jsonstat(d, keep_dims={"geo", "sex", "time"})
    for r in une:
        r["month"] = r.pop("time")
        r["geo"] = r["geo"].replace("EU27_2020", "EU27")
    une.sort(key=lambda r: (r["month"], r["geo"], r["sex"]))
    cols = ["month", "geo", "sex", "age", "value", "geo_label", "sex_label", "age_label"]
    for r in une:
        r["age"] = "TOTAL"
        r["age_label"] = "Total (16 to 74 years)"
    write_csv(os.path.join(OUT, "unemployment-rate-monthly.csv"), cols, une)
    write_sample(OUT, "eurostat-unemployment-monthly",
                 "Eurostat Monthly Unemployment Rate by Sex, EU27 + 8 Countries, 2003-2026",
                 cols, une[-SAMPLE_N:], len(une))
    print(f"  rows={len(une)} months={min(r['month'] for r in une)}-{max(r['month'] for r in une)} geos={len(set(r['geo'] for r in une))}")
    sanity("unemployment rate %, monthly all sexes", une, 0, 40)

    # Fresh stats for the report
    head = {(r["geo"], r["sex"]): r["value"] for r in une if r["month"] == max(x["month"] for x in une)}
    print("  latest month:", max(x["month"] for x in une))
    for g in GEOS:
        g = g.replace("EU27_2020", "EU27")
        print(f"    {g}: T={head.get((g,'T'))} F={head.get((g,'F'))} M={head.get((g,'M'))}")
    eu27_t = {(r["month"], r["sex"]): r["value"] for r in une if r["geo"] == "EU27"}
    peak = max((v, m) for (m, s), v in eu27_t.items() if s == "T")
    print(f"  EU27 T series max: {peak[1]} {peak[0]}")

def write_sample(dirpath, slug, name, columns, rows, row_count):
    os.makedirs(dirpath, exist_ok=True)
    write_csv(os.path.join(dirpath, "sample.csv"), columns, rows)
    sample = {
        "slug": slug,
        "name": name,
        "columns": columns,
        "row_count": row_count,
        "records": rows,
    }
    with open(os.path.join(dirpath, "sample.json"), "w", encoding="utf-8") as f:
        json.dump(sample, f, indent=1, ensure_ascii=False)

if __name__ == "__main__":
    main()
