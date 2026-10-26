#!/usr/bin/env python3
"""v110 holds all 51 unresolved keys; tests image, original hashes, blockers and blanks."""
from pathlib import Path
import csv,hashlib,json,collections
from PIL import Image,ImageChops
ROOT=Path(__file__).resolve().parents[1]
m=json.loads((ROOT/'checkpoints/v110_preview/EVIDENCE_MANIFEST.json').read_text('utf8'))
assert m['base']=='v109' and m['observed_count_added']==0
assert len(m['results'])==9 and m['blocked_count']==len(m['blocked_unobserved'])==42
assert len(m['review_sheets'])==2
reasons=collections.Counter(x['reason'] for x in m['blocked_unobserved'])
assert reasons=={'local_id_out_of_png':37,'missing':5},reasons
all_keys=[tuple(x['key']) for x in m['results']+m['blocked_unobserved']]
assert len(all_keys)==len(set(all_keys))==51
lines=(ROOT/'checkpoints/v110/review_notes_000_008.psv').read_text('utf8').splitlines()
assert len(lines)==10 and all(x.split('|')[2]=='held' for x in lines[1:])
for e in m['results']:
    assert e['status']=='evidence_only_unreviewed' and e['visible_pixel_delta']==0
    p=e['primary_placement'];name=e['key'][0]
    for source,col in [(p['tmx'],'tmx'),('Tiles/2x/'+name+'.png','png')]:
        file=ROOT/('B4220.3_MapExport_256/tmx/'+source if col=='tmx' else source)
        assert file.is_file() and hashlib.sha256(file.read_bytes()).hexdigest()==m['sha256'][source]
    imgs=[]
    for k in ('A','B','C','D','board'):
        path=ROOT/'checkpoints/v110_preview'/e[k]
        assert path.is_file() and path.stat().st_size>1000
        with Image.open(path) as im:im.verify()
        imgs.append(path)
    with Image.open(imgs[1]) as B,Image.open(imgs[2]) as C:
        assert ImageChops.difference(B.convert('RGB').crop((0,64,B.width,B.height)),C.convert('RGB').crop((0,64,C.width,C.height))).getbbox() is None
for s in m['review_sheets']:
    with Image.open(ROOT/s) as im:im.verify()
print('PASS v110 9 blank B/C panels + 42 source blockers, 45 JPEG 2 review sheets; observed_added=0')