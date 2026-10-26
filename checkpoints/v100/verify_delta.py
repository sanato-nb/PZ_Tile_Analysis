#!/usr/bin/env python3
"""v100 visual evidence: 216 unique PNG/TMX A/B/C, actual near D 23, absent D 193."""
import csv,json,hashlib
from pathlib import Path
from PIL import Image,ImageChops
root=Path(__file__).resolve().parents[2]
with (root/'checkpoints/v100/observations.tsv').open(encoding='utf8',newline='') as f:rows=list(csv.DictReader(f,delimiter='\t'))
m=json.loads((root/'checkpoints/v100_preview/EVIDENCE_MANIFEST.json').read_text('utf8'))
assert m['base']=='v99' and m['observed_count_added']==0
evidence={(e['key'][0],int(e['key'][1])):e for e in m['results']}
keys=[(r['tile_set_locator'],int(r['local_id'])) for r in rows]
assert len(rows)==len(keys)==len(set(keys))==len(evidence)==216 and set(keys)==set(evidence)
assert len(m['review_sheets'])==36
assert sum(r['review_status']=='candidate' for r in rows)==181
assert sum(r['review_status']=='held' for r in rows)==35
assert all(r['mapping_verified']==r['tilezed_verified']==r['final_certified']=='0' for r in rows)
actual=0;notavailable=0
for r in rows:
 key=(r['tile_set_locator'],int(r['local_id']))
 e=evidence[key];p=e['primary_placement'];q=e['other_placement']
 assert e['status']=='evidence_only_unreviewed' and e['uses']>=1 and e['D_independent_5_cells_or_other_map'] is False
 if e['other_placement_available']:
  actual+=1
  assert e['uses']>=2 and r['other_tmx']==q['tmx']
  assert (int(r['other_level']),int(r['other_x']),int(r['other_y']),int(r['other_raw_gid']))==(q['level'],q['x'],q['y'],q['gid'])
  assert q['tmx']==p['tmx'] and abs(q['x']-p['x'])+abs(q['y']-p['y'])<5
 else:
  notavailable+=1
  assert e['uses']==1 and r['other_tmx']==''
  assert int(r['other_level'])==int(r['other_x'])==int(r['other_y'])==-1 and int(r['other_raw_gid'])==0
 assert (r['source_tmx'],int(r['level']),int(r['x']),int(r['y']),int(r['raw_gid']))==(p['tmx'],p['level'],p['x'],p['y'],p['gid'])
 assert int(r['visible_pixel_delta'])==e['visible_pixel_delta']
 assert int(r['png_height_mismatch'])==int(e['atlas_status']=='height_mismatch') and r['atlas_status']==e['atlas_status']
 assert r['observed_features'].strip() and r['part_role'].strip()
 if r['review_status']=='candidate':
  assert r['identity_candidate'].strip() and r['confidence']=='low' and int(r['visible_pixel_delta'])>=500
 else:assert not r['identity_candidate'].strip()
 for name,col in ((p['tmx'],'source_tmx_sha256'),('Tiles/2x/'+key[0]+'.png','source_png_sha256')):
  path=root/('B4220.3_MapExport_256/tmx/'+name if name.endswith('.tmx') else name)
  assert path.is_file() and hashlib.sha256(path.read_bytes()).hexdigest()==m['sha256'][name]==r[col]
  if path.suffix=='.png':
   with Image.open(path) as im:im.verify()
 imgs=[]
 for kind in ('A','B','C','D','board'):
  path=root/r['evidence_'+kind]
  assert path.is_file() and path.stat().st_size>1000
  with Image.open(path) as im:im.verify()
  imgs.append(path)
 with Image.open(imgs[1]) as B,Image.open(imgs[2]) as C:
  assert e['visible_pixel_delta']==0 or ImageChops.difference(B.convert('RGB'),C.convert('RGB')).getbbox()
assert (actual,notavailable)==(23,193)
print('PASS v100 216 unique 181 candidate 35 held, 23 near D and 193 D absent, 600 JPEG; original SHA/GID/coordinate')
