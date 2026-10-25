#!/usr/bin/env python3
import csv
from pathlib import Path
root=Path(__file__).resolve().parents[2]
with (Path(__file__).with_name("observations.tsv")).open(encoding="utf-8",newline="") as f:
 rows=list(csv.DictReader(f,delimiter="\t"))
keys={(r["tile_set_locator"],int(r["local_id"])) for r in rows}
assert len(rows)==len(keys)==29
assert sum(r["review_status"]=="candidate" for r in rows)==18
assert sum(r["review_status"]=="held" for r in rows)==11
assert all(r["mapping_verified"]==r["tilezed_verified"]==r["final_certified"]=="0" for r in rows)
print("PASS v50: 29 unique new records, 18 candidates, 11 held")
