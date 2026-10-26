#!/usr/bin/env python3
"""v95 새 120종: 원본 PNG/TMX SHA, B/C 제거, D 실제 사용 위치 없음 표기 확인."""
import csv,json,hashlib
from pathlib import Path
from PIL import Image,ImageChops
root=Path(__file__).resolve().parents[2]
with (root/'checkpoints/v95/observations.tsv').open(encoding='utf8',newline='') as f:rows=list(csv.DictReader(f,delimiter='\t'))
m=json.loads((root/'checkpoints/v95_preview/EVIDENCE_MANIFEST.json').read_text('utf8'))
assert m['base']=='v94' and m['observed_count_added']==0
ev={(r['key'][0],int(r['key'][1])):r for r in m['results']}
keys=[(r['tile_set_locator'],int(r['local_id'])) for r in rows]
assert len(rows)==len(keys)==len(set(keys))==len(ev)==12 and set(keys)==set(ev)
assert len(m['review_sheets'])==2
assert sum(r['review_status']=='candidate' for r in rows)==7
assert sum(r['review_status']=='held' for r in rows)==5
assert all(r['mapping_verified']==r['tilezed_verified']==r['final_certified']=='0' for r in rows)
src=set()
for r in rows:
 key=(r['tile_set_locator'],int(r['local_id']));e=ev[key];p=e['primary_placement']
 assert e['status']=='evidence_only_unreviewed' and e['uses']>=2 and e['other_placement_available'] is True
 assert r['other_tmx']==e['other_placement']['tmx'] and int(r['other_level'])==e['other_placement']['level']
 assert int(r['other_x'])==e['other_placement']['x'] and int(r['other_y'])==e['other_placement']['y'] and int(r['other_raw_gid'])==e['other_placement']['gid']
 assert p['tmx']!=e['other_placement']['tmx'] or (p['x'],p['y'])!=(e['other_placement']['x'],e['other_placement']['y'])
 assert e['D_independent_5_cells_or_other_map'] is False
 assert '독립 현장 아님' in r['review_notes']
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
print('PASS v95 12 A/B/C/D actual second positions (nearby, non-independent); 60 JPEG; hashes, uniqueness, coordinate provenance and confidence')
