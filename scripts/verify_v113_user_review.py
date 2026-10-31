#!/usr/bin/env python3
"""Verify nine user judgments and evidence caveats before applying to the B42 database."""
from pathlib import Path
import csv,json
R=Path(__file__).resolve().parents[1]
j=json.loads((R/'checkpoints/v113/user_review_summary.json').read_text('utf8'))
with (R/'checkpoints/v113/user_review.csv').open('r',encoding='utf-8-sig',newline='') as f:
    rows=list(csv.DictReader(f))
assert len(rows)==9 and len({(x['tile_set_locator'],x['local_id']) for x in rows})==9
assert [int(r['review_number']) for r in rows]==list(range(1,10))
assert [int(x['review_number']) for x in rows if x['user_action']=='keep_provisional']==[2]
assert sum(x['user_action']=='exclude_from_active_review' for x in rows)==8
assert [x['user_candidate'] for x in rows if x['user_action']=='keep_provisional']==['풀 또는 꽃 계열 식물']
assert not any(x['source_evidence_status']=='verified_empty_alpha_in_provisional_crop' for x in rows if x['review_number'] not in ('1','3','4'))
assert sum(x['source_evidence_status']=='verified_empty_alpha_in_provisional_crop' for x in rows)==3
assert sum(x['source_evidence_status']=='nested_png_blank_provisional_crop_mapping_unverified' for x in rows)==3
assert sum(x['source_evidence_status']=='exact_source_missing' for x in rows)==2
assert (j['historical_unobserved'],j['user_excluded_from_active_review'],j['active_unobserved_to_review'],j['new_verified_observations'])==(9,8,1,0)
assert j['new_auditable_candidates']==j['new_final_certifications']==0
print('PASS v113 nine grounded user actions, 8 excluded, 1 low provisional, 0 certification')