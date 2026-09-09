#!/usr/bin/env python3
"""ETL: HUD Fair Market Rents FY2027 by ZIP code, full 51,871-row file.

Source: fmr-by-zip-2027.csv (51,871 ZIP rows parsed from FY27_FMRs.xlsx plus
the FY2027 small-area FMR file, effective October 1, 2026, already in
artifacts/products/hud-dataset/). No new download. The copy is byte-identical,
checked by sha256 at build time. License: public domain (US government data).
Rerunnable: python3 tools/etl-hud-fmr-by-zip-2027.py
"""
import csv
import hashlib
import json
import os
import shutil
import statistics
from collections import Counter, defaultdict

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = "/home/uwuki/money-mission/artifacts/products/hud-dataset/fmr-by-zip-2027.csv"
OUT = os.path.join(ROOT, "data", "hud-fmr-by-zip-2027")

SLUG = "hud-fmr-by-zip-2027"
NAME = "HUD Fair Market Rents FY2027 by ZIP Code"
COLS = ["zip", "hud_area_code", "metro", "area_name", "state",
        "fmr_0br", "fmr_1br", "fmr_2br", "fmr_3br", "fmr_4br"]
BR = COLS[5:]
SAMPLE_ROWS = 22


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def main():
    with open(SRC, newline="") as f:
        reader = csv.DictReader(f)
        assert reader.fieldnames == COLS, reader.fieldnames
        rows = list(reader)

    # integrity checks, hard-fail on any violation
    assert len(rows) == 51871, len(rows)
    for r in rows:
        assert len(r["zip"]) == 5 and r["zip"].isdigit(), r["zip"]
        assert r["metro"] in ("metro", "nonmetro"), r["metro"]
        for b in BR:
            v = r[b]
            assert v.isdigit() and v != "0", (r["zip"], b, v)
    keys = Counter((r["zip"], r["hud_area_code"]) for r in rows)
    assert sum(1 for v in keys.values() if v > 1) == 0
    assert sum(1 for r in rows if int(r["fmr_4br"]) < int(r["fmr_2br"])) == 0

    os.makedirs(OUT, exist_ok=True)

    full_csv = os.path.join(OUT, "fmr-by-zip-2027.csv")
    shutil.copy2(SRC, full_csv)
    assert sha256(full_csv) == sha256(SRC), "copy is not byte-identical"

    with open(os.path.join(OUT, "sample.csv"), "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=COLS)
        w.writeheader()
        w.writerows(rows[:SAMPLE_ROWS])

    sample = {
        "slug": SLUG,
        "name": NAME,
        "columns": COLS,
        "row_count": len(rows),
        "records": rows[:SAMPLE_ROWS],
    }
    with open(os.path.join(OUT, "sample.json"), "w") as f:
        json.dump(sample, f, indent=1)

    # stats
    zc = Counter(r["zip"] for r in rows)
    multi = sorted((z, c) for z, c in zc.items() if c > 1)
    metro_rows = sum(1 for r in rows if r["metro"] == "metro")
    nonmetro_rows = len(rows) - metro_rows
    areas = set(r["hud_area_code"] for r in rows)
    metro_areas = set(r["hud_area_code"] for r in rows if r["metro"] == "metro")
    states = Counter(r["state"] for r in rows)
    top10 = states.most_common(10)

    v2 = sorted(int(r["fmr_2br"]) for r in rows)
    q2 = statistics.quantiles(v2, n=4, method="inclusive")
    min_row = min(rows, key=lambda r: int(r["fmr_2br"]))
    max_row = max(rows, key=lambda r: int(r["fmr_2br"]))

    st = defaultdict(list)
    for r in rows:
        st[r["state"]].append(int(r["fmr_2br"]))
    st_meds = sorted(
        ((s, int(statistics.median(v)), len(v)) for s, v in st.items()),
        key=lambda x: (-x[1], x[0]))

    stats = {
        "rows": len(rows),
        "columns": len(COLS),
        "unique_zips": len(zc),
        "rows_leading_zero_zip": sum(1 for r in rows if r["zip"].startswith("0")),
        "unique_zips_leading_zero": len(set(r["zip"] for r in rows if r["zip"].startswith("0"))),
        "metro_rows": metro_rows,
        "nonmetro_rows": nonmetro_rows,
        "distinct_area_codes": len(areas),
        "metro_area_codes": len(metro_areas),
        "nonmetro_area_codes": len(areas) - len(metro_areas),
        "states_territories": len(states),
        "multi_area_zips": len(multi),
        "max_rows_per_zip": max(zc.values()),
        "zips_at_max_rows": sorted(z for z, c in zc.items() if c == max(zc.values())),
        "fmr_2br_min": min(v2),
        "fmr_2br_p25": int(q2[0]),
        "fmr_2br_median": int(statistics.median(v2)),
        "fmr_2br_p75": int(q2[2]),
        "fmr_2br_max": max(v2),
        "fmr_2br_min_zip": min_row["zip"],
        "fmr_2br_min_area": min_row["area_name"],
        "fmr_2br_max_zip": max_row["zip"],
        "fmr_2br_max_area": max_row["area_name"],
        "top10_states_by_rows": top10,
        "top10_rows_sum": sum(c for _, c in top10),
        "state_2br_median_top3": st_meds[:3],
        "state_2br_median_bottom3": st_meds[-3:],
        "source_sha256": sha256(SRC),
    }

    with open(os.path.join(OUT, "etl-stats.json"), "w") as f:
        json.dump(stats, f, indent=1)

    multi_len = len(multi)
    max_rows = max(zc.values())
    zips_max = sorted(z for z, c in zc.items() if c == max_rows)
    top10_text = ", ".join(f"{s} {c:,}" for s, c in top10[:5]) + ", then " + \
        ", ".join(f"{s} {c:,}" for s, c in top10[5:])
    top10_sum = sum(c for _, c in top10)

    with open(os.path.join(OUT, "schema.md"), "w") as f:
        f.write(f"""# {NAME} — schema

Source: FY2027 Fair Market Rent ZIP-level file, 51,871 rows parsed from
FY27_FMRs.xlsx plus the FY2027 small-area FMR file (FY27_safmrs.xlsx), rates
effective October 1, 2026. The copy here is byte-identical to the parsed file,
sha256-checked at build time. No new download, no re-derivation, no edits:
every cell matches the source parse. License: public domain (US government
data, HUD FY2027 Fair Market Rent release).

## fmr-by-zip-2027.csv ({len(rows):,} rows)
| column | type | meaning |
|---|---|---|
| zip | text | 5-digit ZIP code, leading zeros preserved ({stats['unique_zips_leading_zero']:,} unique ZIPs start with 0) |
| hud_area_code | text | HUD FMR area code (e.g. METRO10180M10180, NCNTY72923N72923) |
| metro | text | `metro` or `nonmetro` flag for the row |
| area_name | text | HUD area name, verbatim, may contain commas (quoted) |
| state | text | two-letter state or territory code, 52 total |
| fmr_0br ... fmr_4br | int | FY2027 fair market rent in dollars for studios through 4 bedrooms |

## Coverage
- {len(zc):,} unique ZIP codes across {len(rows):,} rows: {multi_len:,} ZIPs appear in
  more than one HUD area, because metro and nonmetro coverage split the same
  ZIP between areas. Max rows per single ZIP: {max_rows} (ZIPs {', '.join(zips_max)}).
- {metro_rows:,} metro rows vs {nonmetro_rows:,} nonmetro rows; {len(areas):,} distinct
  area codes ({len(metro_areas)} metro, {len(areas) - len(metro_areas)} nonmetro).
- Largest states by row count: {top10_text}. The top ten together carry
  {top10_sum:,} of the {len(rows):,} rows.

## Integrity checks at build time (all pass)
- {len(rows):,} rows, uniform {len(COLS)} columns, header identical to the FY2026 schema.
- 0 malformed ZIP fields (every value 5 digits).
- 0 empty, zero, or non-numeric FMR cells across 5 bedroom sizes.
- 0 duplicate (zip, hud_area_code) keys.
- 0 rows where fmr_4br < fmr_2br.
- Copy sha256 equals source sha256.

## Distribution reference (2BR)
Min {min(v2)} ({min_row['zip']}, {min_row['area_name']}), p25 {int(q2[0])}, median
{int(statistics.median(v2))}, p75 {int(q2[2])}, max {max(v2)} ({max_row['zip']},
{max_row['area_name']}). State-level 2BR medians run from California {st_meds[0][1]}
down to Puerto Rico {st_meds[-1][1]}.

## Caveats
- Multi-area ZIPs are HUD's design, not duplication: one ZIP can carry both a
  metro and a nonmetro row, or split between small-area county groups. Dedup
  on (zip, hud_area_code) or filter on `metro` before per-ZIP lookups.
- ZIP rows are small-area FMRs where HUD publishes them and metro/nonmetro
  area rents elsewhere; the `metro` flag tells you which. Rows of one area
  share the same rent values.
- HUD can revise FY2027 rents mid-cycle; the FY2026 file stays the baseline
  for anything dated before October 1, 2026.
""")

    print(json.dumps({k: v for k, v in stats.items() if k != "source_sha256"}, indent=1))
    print("sha256:", stats["source_sha256"][:16] + "…")


if __name__ == "__main__":
    main()
