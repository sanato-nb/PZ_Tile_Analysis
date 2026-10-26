#!/usr/bin/env python3
"""v112 diagnostic: nine remaining unobserved, no change to certified/observed counts."""
from pathlib import Path
from collections import Counter
from difflib import SequenceMatcher
from xml.etree import ElementTree as ET
from PIL import Image, ImageDraw, ImageFont
import csv,hashlib,json,re,os
R=Path(__file__).resolve().parents[1]
OUT=R/'audits/v112_remaining9'
OUT.mkdir(parents=True,exist_ok=True)
with (R/'checkpoints/v111/unresolved_9.csv').open('r',encoding='utf-8-sig',newline='') as f:
    unresolved=list(csv.DictReader(f))
assert len(unresolved)==9 and len({(x['tile_set_locator'],x['local_id']) for x in unresolved})==9
manifest=json.loads((R/'checkpoints/v111_singleuse_preview/EVIDENCE_MANIFEST.json').read_text('utf8'))
E={(x['key'][0],str(x['key'][1])):x for x in manifest['results']}
tiletext=(R/'Tiles/tiledefinitions.tiles.txt').read_text(encoding='utf8')
tiledefs={}
for block in re.findall(r'tileset\s*\{(.*?)\}',tiletext,re.S):
    n=re.search(r'file\s*=\s*(\S+)',block); dim=re.search(r'size\s*=\s*(\d+)\s*,\s*(\d+)',block)
    if n and dim: tiledefs[n.group(1)]=[int(dim.group(1)),int(dim.group(2))]
all_png=sorted({x.resolve() for x in (R/'Tiles').rglob('*.png') if x.is_file()})
def short(f): return f.stem.lower().replace(' ','').replace('-','').replace("'",'')
names={str(p):short(p) for p in all_png}
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
# Search same repository only: alternatives are leads, never substitute for the requested source.
missing=[]
for row in unresolved:
    if row['status']!='held_missing_PNG':continue
    n=row['tile_set_locator']; tidy=re.sub(r'\s*\([^)]*conflicted copy[^)]*\)','',n,flags=re.I).strip()
    expected=[str(R/'Tiles/2x'/(n+'.png')),str(R/'Tiles'/(n+'.png'))]
    q=tidy.lower().replace(' ','').replace('-','').replace("'",'')
    match=[]
    for path in all_png:
        p=names[str(path)]
        score=max(SequenceMatcher(None,q,p).ratio(), SequenceMatcher(None,n.lower(),p).ratio())
        if p==q:score=1.0
        if q in p or p in q:score=max(score,0.82)
        if score>=0.56:
            match.append((score,path))
    match.sort(key=lambda t:(-t[0],str(t[1])))
    candidates=[]
    for score,path in match[:12]:
        with Image.open(path) as im:
            w,h=im.size
        candidates.append(dict(path=str(path.relative_to(R)),similarity=round(score,4),size=[w,h],sha256=sha(path)))
    missing.append(dict(key=[n,int(row['local_id'])],reason='exact_png_missing',expected_paths=[x[len(str(R))+1:] for x in expected],
         tile_definition_grid=tiledefs.get(n),normalized_name=tidy,
         similar_existing_png_names_only=candidates, warning='File-name similarity does not establish same tile, sprite ID, or correct pixels.'))
assert len(missing)==5
# Extract all matching placements and the actual layer order from 31_45, 31_46.
target={(r['tile_set_locator'],int(r['local_id'])) for r in unresolved if r['status']=='held_no_BC_change'}
maps={}
for tmx in ('31_45.tmx','31_46.tmx'):
    root=ET.parse(R/'B4220.3_MapExport_256/tmx'/tmx).getroot()
    ts=[]
    for t in root.findall('tileset'):
        image=t.find('image')
        ts.append(dict(firstgid=int(t.get('firstgid')),name=t.get('name'),tw=int(t.get('tilewidth')),
                       th=int(t.get('tileheight')),im_w=int(image.get('width')),im_h=int(image.get('height')),
                       source=image.get('source')))
    ts.sort(key=lambda t:t['firstgid'])
    layers=[]
    for ix,lay in enumerate(root.findall('layer')):
        data=lay.find('data')
        if data is None or data.attrib.get('encoding')!='csv':continue
        vals=[int(z.strip()) for z in data.text.split(',') if z.strip()]
        assert len(vals)==65536
        layers.append(dict(index=ix,name=lay.get('name'),level=int(lay.get('level','0')),
                           visible=lay.get('visible','1'),opacity=lay.get('opacity','1'),vals=vals))
    maps[tmx]=(ts,layers)
def resolve(ts,gid):
    gid &= 0x1fffffff
    eligible=[t for t in ts if t['firstgid']<=gid]
    if not eligible:return None
    t=eligible[-1]
    return (t['name'],gid-t['firstgid'])
def png_crop(name,local_id,ts):
    f=R/'Tiles/2x'/(name+'.png')
    if not f.exists():f=R/'Tiles'/(name+'.png')
    assert f.exists(),name
    with Image.open(f) as im:
        rgba=im.convert('RGBA')
    grid=tiledefs.get(name)
    assert grid and rgba.width==grid[0]*ts['tw']*2 and rgba.height==grid[1]*ts['th']*2, (name,grid,rgba.size)
    sw,sh=ts['tw']*2,ts['th']*2
    x=(local_id%grid[0])*sw; y=(local_id//grid[0])*sh
    return rgba.crop((x,y,x+sw,y+sh)),str(f.relative_to(R)),list(rgba.size)
zero=[]
for row in unresolved:
    if row['status']!='held_no_BC_change':continue
    key=(row['tile_set_locator'],int(row['local_id']))
    e=E[(key[0],str(key[1]))]
    p=e['primary_placement'];ts,layers=maps[p['tmx']]
    layer=next(x for x in layers if x['index']==p['layer_index'])
    assert layer['vals'][p['y']*256+p['x']]==p['gid'] and resolve(ts,p['gid'])==key
    t=next(t for t in ts if t['name']==key[0])
    img,source,img_size=png_crop(key[0],key[1],t)
    alpha=img.getchannel('A')
    bbox=alpha.getbbox()
    alpha_pixels=sum(int(v>0) for v in alpha.getdata())
    # What was drawn in the same coordinate, in which order? Includes all same-level layers.
    stacked=[]
    for l in layers:
        if l['level']!=p['level']:continue
        gid=l['vals'][p['y']*256+p['x']]
        if gid:
            stacked.append(dict(layer_index=l['index'],layer_name=l['name'],raw_gid=gid,
                                resolved=resolve(ts,gid),after_target=(l['index']>p['layer_index']),
                                layer_visible=l['visible'],opacity=l['opacity']))
    img_path=OUT/(re.sub(r'[^A-Za-z0-9_-]','_',key[0])+'_'+str(key[1])+'_A_rgba.png')
    img.save(img_path)
    zero.append(dict(key=list(key),status='unobserved_zero_BC_delta',primary_placement=p,
       atlas_path=source,atlas_size=img_size,tiledef_grid=tiledefs.get(key[0]),
       crop_size=list(img.size),alpha_visible_pixels=alpha_pixels,alpha_bbox=list(bbox) if bbox else None,
       actual_same_cell_layers=stacked,overlying_same_cell_layers=[x for x in stacked if x['after_target']],
       image_file=str(img_path.relative_to(R)),zero_delta_by_source_manifest=e['visible_pixel_delta']==0,
       conclusion='Alpha empty' if alpha_pixels==0 else 'Non-empty A; composited B-C still zero. Overlap, occlusion and layer visibility need TileZed validation.'))
assert len(zero)==4 and all(x['zero_delta_by_source_manifest'] for x in zero)
# ZIP deliberately absent: this is a source investigation, not new certified review.
report=dict(version='v112',mode='source_path_and_layer_diagnostic',base_version='v111',
    baseline_observed=5400,new_observed=0,remaining_unobserved=9,
    missing_png_count=5,zero_BC_count=4,missing_png=missing,zero_BC=zero,
    original_tmx_sha256={k:sha(R/'B4220.3_MapExport_256/tmx'/k) for k in maps},
    tiledefinitions_sha256=sha(R/'Tiles/tiledefinitions.tiles.txt'),
    warning='No candidate, observed, final certification, or official Local ID validation added. Similar filenames are not source equivalence.',
    mapping_verified=False,tilezed_verified=False,final_certified=0)
(OUT/'SOURCE_AUDIT.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
with (OUT/'SOURCE_AUDIT.csv').open('w',encoding='utf-8-sig',newline='') as f:
    w=csv.writer(f);w.writerow(['tileset','local_id','issue','finding','alternatives_or_same_cell_layers'])
    for r in missing:w.writerow([*r['key'],'PNG missing',r['normalized_name'],'; '.join(z['path'] for z in r['similar_existing_png_names_only'][:5])])
    for r in zero:w.writerow([*r['key'],'No B-C delta',f"RGBA visible alpha pixels: {r['alpha_visible_pixels']}",str(r['actual_same_cell_layers'])])
assert len(missing)+len(zero)==9
print('PASS v112 audited all 9 unresolved; PNG missing',len(missing),'zero B-C',len(zero),'alpha counts',[{ 'key':x['key'],'alpha':x['alpha_visible_pixels'],'layers':len(x['actual_same_cell_layers'])} for x in zero])
