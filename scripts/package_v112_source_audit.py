#!/usr/bin/env python3
"""Package the genuine v112 source audit; no database or observation changes."""
from pathlib import Path
from PIL import Image
import hashlib,json,zipfile
R=Path(__file__).resolve().parents[1]
A=R/'audits/v112_remaining9';PRE=R/'checkpoints/v112_jumbo_preview'
report=json.loads((A/'SOURCE_AUDIT.json').read_text('utf8'))
m=json.loads((PRE/'EVIDENCE_MANIFEST.json').read_text('utf8'))
assert report['base_version']=='v111' and report['new_observed']==0
assert report['remaining_unobserved']==9 and len(report['zero_BC'])==4 and len(report['missing_png'])==5
assert m['base']=='v111' and len(m['results'])==3 and all(x['visible_pixel_delta']==0 for x in m['results'])
assert len(m['review_sheets'])==1
assets=[
 A/'SOURCE_AUDIT.json',A/'SOURCE_AUDIT.csv',
 R/'docs/V112_SOURCE_AUDIT.md',PRE/'EVIDENCE_MANIFEST.json',
 *[R/x['image_file'] for x in report['zero_BC']],
 *[PRE/e[k] for e in m['results'] for k in ('A','B','C','D','board')],
 *[R/x for x in m['review_sheets']]
]
assert len(assets)==24,len(assets)
assert len(set(assets))==len(assets)
for im in assets:
    assert im.is_file() and im.stat().st_size
    if im.suffix.lower() in ('.jpg','.png'):
        with Image.open(im) as x:x.verify()
zip_path=A/'v112_nine_unresolved_source_evidence.zip'
with zipfile.ZipFile(zip_path,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=6) as z:
    for p in assets:z.write(p,arcname=p.relative_to(R).as_posix())
with zipfile.ZipFile(zip_path) as z:
    assert len(z.namelist())==len(assets) and z.testzip() is None
out=dict(version='v112',type='diagnostic_no_observed_change',base_version='v111',
     baseline_observed=5400,remaining_unobserved=9,official_final_certified=0,
     png_source_found_subdirectory_keys=3,unresolved_original_png_or_mapping_keys=9,
     alpha_empty_source_crops=3,nonempty_source_zero_composited_delta=1,
     jumbo_provisional_rechecks=3,jumbo_delta_positive=0,
     source_pngs_exact_nested=2,similar_basename_not_verified=1,missing_exact_source=1,
     evidence_images=20,images_jpeg=15,images_png=4,review_sheets=1,
     zip_crc='PASS',zip_items=len(assets),zip_bytes=zip_path.stat().st_size,
     zip_sha256=hashlib.sha256(zip_path.read_bytes()).hexdigest(),mapping_verified=0,tilezed_verified=0)
(A/'ZIP_CRC_REPORT.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n','utf8')
print('PASS v112 source audit ZIP',out)
