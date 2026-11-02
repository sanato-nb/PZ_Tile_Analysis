#!/usr/bin/env python3
import csv,hashlib,pathlib,zipfile
root=pathlib.Path(__file__).resolve().parent
with (root/'SOURCE_SHA256.csv').open(encoding='utf-8-sig',newline='') as f: rows=list(csv.DictReader(f))
assert len(rows)==20
assert sorted(set(int(r['index']) for r in rows))==list(range(211,221))
for r in rows:
    b=(root/r['copied_path']).read_bytes()
    assert len(b)==int(r['bytes'])
    assert hashlib.sha256(b).hexdigest()==r['sha256'],r['copied_path']
with (root/'BATCH_211_220_MANUAL_VISUAL_REVIEW.csv').open(encoding='utf-8-sig',newline='') as f: reviews=list(csv.DictReader(f))
assert [int(r['index']) for r in reviews]==list(range(211,221))
assert sum(r['new_visual_verdict']=='CONDITIONAL_VISUAL_ONLY' for r in reviews)==1
assert all(r['game_1to1_approved']=='NO' for r in reviews)
with zipfile.ZipFile(root/'ROSEWOOD_BATCH_211_220_REVIEW.zip') as z:
    assert z.testzip() is None
    for r in rows:
        if r['kind']=='LEGACY_SIDE_BY_SIDE_JPG':
            assert hashlib.sha256(z.read(r['copied_path'])).hexdigest()==r['sha256']
print('PASS: 20 SHA-256, 10 review rows, ZIP CRC32, JPG contents')
