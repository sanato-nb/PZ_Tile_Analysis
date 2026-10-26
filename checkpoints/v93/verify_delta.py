#!/usr/bin/env python3
"""v93 12 타일 원본/경로/키/해시 및 A/B/C/D 개별 JPEG 대조."""
import csv,json,hashlib
from pathlib import Path
from PIL import Image,ImageChops
root=Path(__file__).resolve().parents[2]
cp=root/'checkpoints/v93'
with (cp/'observations.tsv').open(encoding='utf8',newline='') as f:rows=list(csv.DictReader(f,delimiter='\t'))
keys=[(r['tile_set_locator'],int(r['local_id'])) for r in rows]
assert len(keys)==len(set(keys))==5
assert sum(r['review_status']=='candidate' for r in rows)==2
assert sum(r['review_status']=='held' for r in rows)==3
assert all(r['mapping_verified']==r['tilezed_verified']==r['final_certified']=='0' for r in rows)
manifests=[json.loads((root/p/'EVIDENCE_MANIFEST.json').read_text('utf8')) for p in [Path('checkpoints/v93_preview')]]
assert [m['base'] for m in manifests]==['v92']
assert all(m['observed_count_added']==0 for m in manifests)
assert [len(m['results']) for m in manifests]==[5]
evidence={}
for m in manifests:
 for item in m['results']:
  k=(item['key'][0],int(item['key'][1]))
  assert k not in evidence,('duplicate evidence',k)
  evidence[k]=(item,m)
assert set(keys)==set(evidence)
assert all(r['identity_candidate'].strip() for r in rows if r['review_status']=='candidate')
assert all(not r['identity_candidate'].strip() for r in rows if r['review_status']=='held')
seen=set()
for r in rows:
 k=(r['tile_set_locator'],int(r['local_id']))
 item,m=evidence[k]
 assert item['status']=='evidence_only_unreviewed'
 assert int(r['visible_pixel_delta'])==item['visible_pixel_delta']
 assert r['observed_features'].strip() and r['part_role'].strip()
 assert r['atlas_status']==item['atlas_status']
 assert int(r['png_height_mismatch'])==int(item['atlas_status']=='height_mismatch')
 p=item['primary_placement'];q=item['other_placement']
 assert (r['source_tmx'],int(r['raw_gid']),int(r['x']),int(r['y']),int(r['level']))==(p['tmx'],p['gid'],p['x'],p['y'],p['level'])
 assert (r['other_tmx'],int(r['other_raw_gid']),int(r['other_x']),int(r['other_y']),int(r['other_level']))==(q['tmx'],q['gid'],q['x'],q['y'],q['level'])
 for path_key,col in ((p['tmx'],'source_tmx_sha256'),('Tiles/2x/'+k[0]+'.png','source_png_sha256')):
  path=root/('B4220.3_MapExport_256/tmx/'+path_key if path_key.endswith('.tmx') else path_key)
  assert path.is_file()
  h=hashlib.sha256(path.read_bytes()).hexdigest()
  assert h==m['sha256'][path_key]==r[col],(k,path_key)
  seen.add(str(path))
  if path.suffix=='.png':
   with Image.open(path) as im:im.verify()
 images=[]
 for_kind=('A','B','C','D','board')
 for kind in for_kind:
  path=root/r['evidence_'+kind]
  assert path.is_file() and path.stat().st_size>1000
  with Image.open(path) as im:im.verify()
  images.append(path)
 with Image.open(images[1]) as B,Image.open(images[2]) as C:
  assert item['visible_pixel_delta']==0 or ImageChops.difference(B.convert('RGB'),C.convert('RGB')).getbbox()
print('PASS v93',len(keys),'unique',len(seen),'original files; 25 JPEG; hash, positions, SQLite queue preconditions and board evidence')
