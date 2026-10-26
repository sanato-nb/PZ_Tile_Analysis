#!/usr/bin/env python3
"""v94 새 120종: 원본 PNG/TMX SHA, B/C 제거, D 실제 사용 위치 없음 표기 확인."""
import csv,json,hashlib
from pathlib import Path
from PIL import Image,ImageChops
root=Path(__file__).resolve().parents[2]
with (root/'checkpoints/v94/observations.tsv').open(encoding='utf8',newline='') as f:rows=list(csv.DictReader(f,delimiter='\t'))
m=json.loads((root/'checkpoints/v94_preview/EVIDENCE_MANIFEST.json').read_text('utf8'))
assert m['base']=='v93' and m['observed_count_added']==0
ev={(r['key'][0],int(r['key'][1])):r for r in m['results']}
keys=[(r['tile_set_locator'],int(r['local_id'])) for r in rows]
assert len(rows)==len(keys)==len(set(keys))==len(ev)==120 and set(keys)==set(ev)
assert len(m['review_sheets'])==20
assert sum(r['review_status']=='candidate' for r in rows)==98
assert sum(r['review_status']=='held' for r in rows)==22
assert all(r['mapping_verified']==r['tilezed_verified']==r['final_certified']=='0' for r in rows)
src=set()
for r in rows:
 key=(r['tile_set_locator'],int(r['local_id']));e=ev[key];p=e['primary_placement']
 assert e['status']=='evidence_only_unreviewed' and e['uses']==1 and e['other_placement_available'] is False
 assert r['other_tmx']=='' and int(r['other_level'])==int(r['other_x'])==int(r['other_y'])==-1 and int(r['other_raw_gid'])==0
 assert r['review_notes'].find('D는 다른 배치가 없음을 명시')>=0
 assert r['source_tmx']==p['tmx'] and int(r['raw_gid'])==p['gid'] and int(r['x'])==p['x'] and int(r['y'])==p['y'] and int(r['level'])==p['level']
 assert int(r['visible_pixel_delta'])==e['visible_pixel_delta']
 assert int(r['png_height_mismatch'])==int(e['atlas_status']=='height_mismatch')
 assert r['atlas_status']==e['atlas_status']
 assert r['observed_features'].strip() and r['part_role'].strip()
 if r['review_status']=='candidate':
  assert r['identity_candidate'].strip() and r['confidence']=='low' and int(r['visible_pixel_delta'])>=500
 else:assert not r['identity_candidate'].strip()
 source_keys=[(p['tmx'],'source_tmx_sha256'),('Tiles/2x/'+key[0]+'.png','source_png_sha256')]
 for name,col in source_keys:
  path=root/('B4220.3_MapExport_256/tmx/'+name if name.endswith('.tmx') else name)
  assert path.is_file()
  digest=hashlib.sha256(path.read_bytes()).hexdigest()
  assert digest==m['sha256'][name]==r[col],(key,name)
  src.add(name)
  if path.suffix=='.png':
   with Image.open(path) as im:im.verify()
 images=[]
 for kind in ('A','B','C','D','board'):
  image=root/r['evidence_'+kind]
  assert image.is_file() and image.stat().st_size>1000
  with Image.open(image) as im:im.verify()
  images.append(image)
 with Image.open(images[1]) as B, Image.open(images[2]) as C:
  assert e['visible_pixel_delta']==0 or ImageChops.difference(B.convert('RGB'),C.convert('RGB')).getbbox()
print('PASS v94 120 independent single-use A/B/C + D unavailable; 600 JPEG; hashes, uniqueness, coordinate provenance and confidence')
