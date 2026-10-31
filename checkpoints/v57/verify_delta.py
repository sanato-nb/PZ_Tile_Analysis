#!/usr/bin/env python3
import csv
from pathlib import Path
with Path(__file__).with_name('observations.tsv').open(encoding='utf-8',newline='') as f: rows=list(csv.DictReader(f,delimiter='\t'))
keys={(r['tile_set_locator'],int(r['local_id'])) for r in rows}
assert len(rows)==len(keys)==48
assert sum(r['review_status']=='candidate' for r in rows)==37
assert sum(r['review_status']=='held' for r in rows)==11
assert all(r['mapping_verified']==r['tilezed_verified']==r['final_certified']=='0' for r in rows)
print('v57 기록 검증 통과: 신규 48종, 잠정 후보 37종, 보류 11종, 인증 0종')
