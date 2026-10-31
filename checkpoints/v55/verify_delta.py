#!/usr/bin/env python3
import csv
from pathlib import Path
with Path(__file__).with_name('observations.tsv').open(encoding='utf-8',newline='') as f:rs=list(csv.DictReader(f,delimiter='\t'))
ks={(r['tile_set_locator'],int(r['local_id'])) for r in rs}
assert len(rs)==len(ks)==48
assert sum(r['review_status']=='candidate' for r in rs)==35
assert sum(r['review_status']=='held' for r in rs)==13
assert all(r['mapping_verified']==r['tilezed_verified']==r['final_certified']=='0' for r in rs)
assert len({r['tile_set_locator'] for r in rs})==8
print('검사 통과: 신규 48종, 후보 35종, 보류 13종, 인증 0종')
