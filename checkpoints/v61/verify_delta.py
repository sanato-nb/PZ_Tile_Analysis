#!/usr/bin/env python3
"""v61 신규 12종의 원본 증거/미관찰 중복/인증 플래그 검증."""
import csv,json,hashlib
from pathlib import Path
root=Path(__file__).resolve().parents[2]
with (root/'checkpoints/v61/observations.tsv').open(encoding='utf8',newline='') as f:
    rows=list(csv.DictReader(f,delimiter='\t'))
keys={(r['tile_set_locator'],int(r['local_id'])) for r in rows}
assert len(rows)==len(keys)==12,(len(rows),len(keys))
assert sum(r['review_status']=='candidate' for r in rows)==8
assert sum(r['review_status']=='held' for r in rows)==4
assert all(r['mapping_verified']==r['tilezed_verified']==r['final_certified']=='0' for r in rows)
assert all(r['png_height_mismatch']=='1' for r in rows)
manifest=json.loads((root/'checkpoints/v61_preview/EVIDENCE_MANIFEST.json').read_text('utf8'))
assert manifest['base']=='v60' and manifest['observed_count_added']==0
evidence={(r['key'][0],int(r['key'][1])):r for r in manifest['results']}
assert set(evidence)==keys
for r in rows:
    key=(r['tile_set_locator'],int(r['local_id']))
    item=evidence[key]
    assert item['status']=='evidence_only_unreviewed'
    assert int(r['visible_pixel_delta'])==item['visible_pixel_delta']
    if r['review_status']=='held': assert int(r['visible_pixel_delta'])<=11
    if r['review_status']=='candidate': assert int(r['visible_pixel_delta'])>0
    for col in ('evidence_A','evidence_B','evidence_C','evidence_D','evidence_board'):
        p=root/r[col]
        assert p.is_file() and p.stat().st_size>1000,(key,col)
    assert r['observed_features'].strip()
    if r['review_status']=='candidate': assert r['identity_candidate'].strip()
print('PASS v61 증거 검증 / 12종 / 후보 8 / 보류 4 / 인증 0')
