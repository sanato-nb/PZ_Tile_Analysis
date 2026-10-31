#!/usr/bin/env python3
"""v110 strict 30 actual-D image evidence, SHA, GID, and provisional TileZed grid audit."""
import csv,json,hashlib
from pathlib import Path
from PIL import Image,ImageChops
root=Path(__file__).resolve().parents[2]
with (root/'checkpoints/v110/observations.tsv').open(encoding='utf8',newline='') as f:
 rows=list(csv.DictReader(f,delimiter='\t'))
m=json.loads((root/'checkpoints/v110_tiledef_preview/EVIDENCE_MANIFEST.json').read_text('utf8'))
assert m['base']=='v108' and m['observed_count_added']==0
assert m['tiledef_grid_provisional'] and not m['mapping_verified']
evidence={(e['key'][0],int(e['key'][1])):e for e in m['results']}
keys=[(r['tile_set_locator'],int(r['local_id'])) for r in rows]
assert len(rows)==len(keys)==len(set(keys))==len(evidence)==30 and set(keys)==set(evidence)
assert len(m['review_sheets'])==5
assert sum(r['review_status']=='candidate' for r in rows)==25
assert sum(r['review_status']=='held' for r in rows)==5
assert all(r['mapping_verified']==r['tilezed_verified']==r['final_certified']=='0' for r in rows)
assert len(m['unrenderable_with_actual_D'])==2
far_count=0
for r in rows:
 key=(r['tile_set_locator'],int(r['local_id']))
 e=evidence[key];p=e['primary_placement'];q=e['other_placement']
 assert e['status']=='evidence_only_unreviewed' and e['uses']>=2 and e['other_placement_available']
 assert (p['tmx'],p['level'],p['x'],p['y'])!=(q['tmx'],q['level'],q['x'],q['y'])
 assert r['other_tmx']==q['tmx']
 assert (int(r['other_level']),int(r['other_x']),int(r['other_y']),int(r['other_raw_gid']))==(q['level'],q['x'],q['y'],q['gid'])
 far=q['tmx']!=p['tmx'] or abs(q['x']-p['x'])+abs(q['y']-p['y'])>=5
 assert far==bool(e['D_independent_5_cells_or_other_map'])
 far_count+=int(far)
 assert (r['source_tmx'],int(r['level']),int(r['x']),int(r['y']),int(r['raw_gid']))==(p['tmx'],p['level'],p['x'],p['y'],p['gid'])
 assert int(r['visible_pixel_delta'])==e['visible_pixel_delta'] and e['visible_pixel_delta']>0
 assert r['atlas_status']==e['atlas_status']=='tiledef_grid_provisional'
 assert int(r['png_height_mismatch'])==1
 assert r['observed_features'].strip() and r['part_role'].strip()
 if r['review_status']=='candidate':
  assert r['identity_candidate'].strip() and r['confidence']=='low' and int(r['visible_pixel_delta'])>=500
 else:assert not r['identity_candidate'].strip()
 for name,col in ((p['tmx'],'source_tmx_sha256'),('Tiles/2x/'+key[0]+'.png','source_png_sha256')):
  path=root/('B4220.3_MapExport_256/tmx/'+name if name.endswith('.tmx') else name)
  assert path.is_file() and hashlib.sha256(path.read_bytes()).hexdigest()==m['sha256'][name]==r[col]
  if path.suffix=='.png':
   with Image.open(path) as im:im.verify()
 for kind in ('A','B','C','D','board'):
  path=root/r['evidence_'+kind]
  assert path.is_file() and path.stat().st_size>1000
  with Image.open(path) as im:im.verify()
 with Image.open(root/r['evidence_B']) as B,Image.open(root/r['evidence_C']) as C:
  assert ImageChops.difference(B.convert('RGB'),C.convert('RGB')).getbbox()
assert far_count==28,far_count
for f in m['review_sheets']:
 with Image.open(root/f) as im:im.verify()
print('PASS v110 30 unique 25 candidate 5 held; 30 real D (28 distant), 150 JPEG, original PNG/TMX SHA and TMX GID; no final certification')
