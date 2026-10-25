#!/usr/bin/env python3
import csv,json
from pathlib import Path
root=Path(__file__).resolve().parents[2]
with (root/'checkpoints/v58/observations.tsv').open(encoding='utf8',newline='') as f:
 rows=list(csv.DictReader(f,delimiter='\t'))
keys={(r['tile_set_locator'],int(r['local_id'])) for r in rows}
assert len(rows)==len(keys)==6
assert sum(r['review_status']=='candidate' for r in rows)==5
assert sum(r['review_status']=='held' for r in rows)==1
assert all(r['mapping_verified']==r['tilezed_verified']==r['final_certified']=='0' for r in rows)
assert all(int(r['visible_pixel_delta'])>0 for r in rows)
assert all(r['png_height_mismatch']=='1' for r in rows)
for r in rows:
 for col in ('evidence_A','evidence_B','evidence_C','evidence_D','evidence_board'):
  p=root/r[col]
  assert p.is_file() and p.stat().st_size>1000,(r['local_id'],col,p)
m=json.loads((root/'checkpoints/v58_preview/EVIDENCE_MANIFEST.json').read_text('utf8'))
assert len(m['results'])==6
assert {(r['key'][0],int(r['key'][1])) for r in m['results']}==keys
print('v58 신규 6종 증거 검증 통과: 후보 5, 보류 1, 인증 0')
