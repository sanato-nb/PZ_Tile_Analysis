#!/usr/bin/env python3
import csv
from pathlib import Path
p=Path(__file__).with_name('observations.tsv')
with p.open(encoding='utf-8',newline='') as f:r=list(csv.DictReader(f,delimiter='\t'))
keys={(x['tile_set_locator'],int(x['local_id'])) for x in r}
assert len(keys)==len(r)==50
assert sum(x['review_status']=='candidate' for x in r)==33
assert sum(x['review_status']=='held' for x in r)==17
assert all(x['mapping_verified']==x['tilezed_verified']==x['final_certified']=='0' for x in r)
assert all(x['observed_features'] and x['identity_candidate'] for x in r)
print('통과: v54 원본 이미지 50종 / 잠정 후보 33종 / 보류 17종 / 최종 인증 0종')
