#!/usr/bin/env python3
"""Archive v113 user's nine review decisions with seven verified historical A/B/C/D boards."""
from pathlib import Path
from PIL import Image
import hashlib,json,zipfile
ROOT=Path(__file__).resolve().parents[1]
CP=ROOT/'checkpoints/v113'
boards=[
 'checkpoints/v111_singleuse_preview/location_business_office_generic_01__009_ABCD.jpg',
 'checkpoints/v111_singleuse_preview/f_bushes_1__066_ABCD.jpg',
 'checkpoints/v111_singleuse_preview/location_business_office_generic_01__011_ABCD.jpg',
 'checkpoints/v111_singleuse_preview/location_business_office_generic_01__012_ABCD.jpg',
 'checkpoints/v112_jumbo_preview/e_cockspurhawthornJUMBO_1__000_ABCD.jpg',
 'checkpoints/v112_jumbo_preview/e_cockspurhawthornJUMBO_1__001_ABCD.jpg',
 'checkpoints/v112_jumbo_preview/e_redmapleJUMBO_1__000_ABCD.jpg'
]
inputs=[CP/'user_review.csv',CP/'user_review_summary.json',
 ROOT/'docs/USER_REVIEW_V113.md',ROOT/'docs/REVIEW_UNOBSERVED_9.md',
 ROOT/'checkpoints/v111/unresolved_9.csv',
 ROOT/'audits/v112_remaining9/SOURCE_AUDIT.json',
 ROOT/'analysis/current/v113/MANIFEST.json',
 *[ROOT/p for p in boards]]
assert len(inputs)==14 and len(set(inputs))==14
for p in inputs:assert p.is_file() and p.stat().st_size>0,p
for p in boards:
    with Image.open(ROOT/p) as im:im.verify()
name=CP/'v113_사용자검수9종_활성제외8종_증거.zip'
with zipfile.ZipFile(name,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=6) as z:
    for p in inputs:z.write(p,arcname=p.relative_to(ROOT).as_posix())
with zipfile.ZipFile(name) as z:
    assert len(z.namelist())==14 and z.testzip() is None
manifest=json.loads((ROOT/'analysis/current/v113/MANIFEST.json').read_text('utf8'))
report=dict(version='v113',review_entries=9,excluded_from_active=8,active_review=1,
  newly_observed=0,newly_certified=0,zip_crc='PASS',zip_entry_count=14,
  reference_comparison_boards=7,zip_sha256=hashlib.sha256(name.read_bytes()).hexdigest(),
  zip_size_bytes=name.stat().st_size,sqlite_sha256=manifest['sqlite_sha256'])
(CP/'ZIP_CRC_REPORT.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
print('PASS v113 ZIP CRC 14 artifacts, 7 previous visual boards, 8 filtered + 1 provisional')