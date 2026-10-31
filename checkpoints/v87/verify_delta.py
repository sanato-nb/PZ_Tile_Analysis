#!/usr/bin/env python3
"""v87 신규 12종: 원본 PNG/TMX SHA, A/B/C/D 로딩, 위치·키·중복·보류·인증 분리 검증."""
import csv, json, hashlib
from pathlib import Path
from PIL import Image, ImageChops
root=Path(__file__).resolve().parents[2]
cp=root/'checkpoints/v87'
with (cp/'observations.tsv').open(encoding='utf8',newline='') as f:
    rows=list(csv.DictReader(f,delimiter='\t'))
keys={(r['tile_set_locator'],int(r['local_id'])) for r in rows}
assert len(rows)==len(keys)==12,(len(rows),len(keys))
assert sum(r['review_status']=='candidate' for r in rows)==7
assert sum(r['review_status']=='held' for r in rows)==5
assert all(r['mapping_verified']==r['tilezed_verified']==r['final_certified']=='0' for r in rows)
manifest=json.loads((root/'checkpoints/v87_preview/EVIDENCE_MANIFEST.json').read_text('utf8'))
assert manifest['base']=='v86' and manifest['observed_count_added']==0
evidence={(r['key'][0],int(r['key'][1])):r for r in manifest['results']}
assert len(evidence)==12 and set(evidence)==keys
def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()
seen=set()
for r in rows:
    key=(r['tile_set_locator'],int(r['local_id']))
    item=evidence[key]
    assert item['status']=='evidence_only_unreviewed'
    assert int(r['visible_pixel_delta'])==item['visible_pixel_delta']
    assert r['observed_features'].strip() and r['part_role'].strip()
    if r['review_status']=='held': assert not r['identity_candidate'].strip()
    else:
        assert r['identity_candidate'].strip()
        assert int(r['visible_pixel_delta'])>0
    assert r['atlas_status']==item['atlas_status']
    assert int(r['png_height_mismatch'])==int(item['atlas_status']=='height_mismatch')
    assert r['source_tmx']==item['primary_placement']['tmx']
    assert int(r['raw_gid'])==item['primary_placement']['gid']
    assert int(r['other_raw_gid'])==item['other_placement']['gid']
    assert (r['source_tmx'],int(r['x']),int(r['y']),int(r['level']))==(item['primary_placement']['tmx'],item['primary_placement']['x'],item['primary_placement']['y'],item['primary_placement']['level'])
    assert (r['other_tmx'],int(r['other_x']),int(r['other_y']),int(r['other_level']))==(item['other_placement']['tmx'],item['other_placement']['x'],item['other_placement']['y'],item['other_placement']['level'])
    for path_key,sha_col in [(r['source_tmx'],'source_tmx_sha256'),('Tiles/2x/'+key[0]+'.png','source_png_sha256')]:
        source=root/('B4220.3_MapExport_256/tmx/'+path_key if path_key.endswith('.tmx') else path_key)
        assert source.exists(),source
        assert sha(source)==r[sha_col]==manifest['sha256'][path_key],(key,path_key)
        seen.add(source)
        if source.suffix=='.png':
            with Image.open(source) as im: im.verify()
    paths=[]
    for kind in ('A','B','C','D','board'):
        path=root/r['evidence_'+kind]
        assert path.exists() and path.stat().st_size>1000,(key,kind)
        with Image.open(path) as im:
            im.verify()
        paths.append(path)
    with Image.open(paths[1]) as b, Image.open(paths[2]) as c:
        assert item['visible_pixel_delta']==0 or ImageChops.difference(b.convert('RGB'),c.convert('RGB')).getbbox(),('B-C positive delta missing',key)
assert len({(r['tile_set_locator'],int(r['local_id'])) for r in rows})==12
print('PASS v87 12 unique / 7 candidate / 5 held / 60 JPEG /',len(seen),'distinct original PNG+TMX sources / SHA256 + image loading + B-C + provenance')
