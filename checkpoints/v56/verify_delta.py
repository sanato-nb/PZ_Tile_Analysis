#!/usr/bin/env python3
import csv
from pathlib import Path
p=Path(__file__).with_name('observations.tsv')
with p.open(encoding='utf-8',newline='') as f: rows=list(csv.DictReader(f,delimiter='\t'))
keys={(r['tile_set_locator'],int(r['local_id'])) for r in rows}
assert len(rows)==len(keys)==48
assert sum(r['review_status']=='candidate' for r in rows)==33
assert sum(r['review_status']=='held' for r in rows)==15
assert all(r['mapping_verified']==r['tilezed_verified']==r['final_certified']=='0' for r in rows)
print('검사 통과: v56 신규 48종, 후보 33종, 보류 15종, 인증 0종')
