#!/usr/bin/env python3
import csv
from pathlib import Path
p=Path(__file__).with_name("observations.tsv")
with p.open(encoding="utf-8",newline="") as f:
 rows=list(csv.DictReader(f,delimiter="\t"))
keys={(r["tile_set_locator"],int(r["local_id"])) for r in rows}
assert len(rows)==len(keys)==41
assert sum(r["review_status"]=="candidate" for r in rows)==35
assert sum(r["review_status"]=="held" for r in rows)==6
assert sum(r["tile_set_locator"]=="water_tank" for r in rows)==13
assert all(r["mapping_verified"]==r["tilezed_verified"]==r["final_certified"]=="0" for r in rows)
print("PASS: v51 checkpoint 41 unique records, 35 candidate, 6 held, water_tank 13")
