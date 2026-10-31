#!/usr/bin/env python3
import csv
from pathlib import Path
p=Path(__file__).with_name('observations.tsv')
with p.open(encoding='utf-8',newline='') as f:r=list(csv.DictReader(f,delimiter='\t'))
keys={(x['tile_set_locator'],int(x['local_id'])) for x in r}
assert len(r)==len(keys)==66
assert sum(x['review_status']=='candidate' for x in r)==41
assert sum(x['review_status']=='held' for x in r)==25
assert all(x['mapping_verified']==x['tilezed_verified']==x['final_certified']=='0' for x in r)
assert all(bool(x['observed_features']) and bool(x['identity_candidate']) for x in r)
print('PASS v52: 66 distinct directly observed, provisional 41, held 25, certified 0')
