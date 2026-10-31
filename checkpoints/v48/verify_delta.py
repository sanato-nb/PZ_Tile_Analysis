#!/usr/bin/env python3
import csv
from pathlib import Path
root=Path(__file__).resolve().parents[2]
with (root/'analysis/imports/merged_catalog_5409.csv').open(encoding='utf-8-sig',newline='') as f:
    base={(r['tile_set_locator'],int(r['local_id'])):r for r in csv.DictReader(f)}
with (Path(__file__).with_name('observations.tsv')).open(encoding='utf-8-sig',newline='') as f:
    new=list(csv.DictReader(f,delimiter='\t'))
keys=[(r['tile_set_locator'],int(r['local_id'])) for r in new]
assert len(base)==5409 and len(keys)==len(set(keys))==30
assert all(k in base and base[k]['observed_any']=='0' and base[k]['provisional_candidate_any_auditable']=='0' for k in keys)
assert sum(r['review_status']=='candidate' for r in new)==23
assert sum(r['review_status']=='held' for r in new)==7
assert all(r['mapping_verified']==r['tilezed_verified']==r['certified']=='0' for r in new)
assert sum(int(r['observed_any']) for r in base.values())==2584
assert 2584+len(keys)==2614 and 5409-2614==2795
print('PASS: v48 30 new observed, 23 candidates, 7 held; total 2614/5409 (48.3269%)')
