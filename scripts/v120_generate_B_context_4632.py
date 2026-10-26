#!/usr/bin/env python3
"""v120: Generate B = original TMX same-floor 5x5 placement scene for each
of the 4,632 NEW keys with v119 selected provisional A.

Scan all 84 TMX files, record exact layer/x/y/raw_gid for every key, reconstruct
scene with original PNG source pixels using v119 A for new sprites, v117 provisional
A for older neighboring sprites. B is an approximation of isometric TileZed
rendering, NOT an official TileZed Local ID/map verification.

No C target removal, no D alternate placement, no identity classifications are
made or claimed. Preserve 5,409 older keys; do not re-review them as targets.
"""
from __future__ import annotations
from pathlib import Path
from collections import Counter,defaultdict
from functools import lru_cache
import bisect,csv,hashlib,io,json,os,re,xml.etree.ElementTree as ET,zipfile
from PIL import Image,ImageDraw,ImageFont
ROOT=Path(__file__).resolve().parents[1]
MAPROOT=ROOT/'B4220.3_MapExport_256/tmx'
OUT=ROOT/'review/v120_B_context_new4632'
SCENES=OUT/'b_png_shards'
SHEETS=OUT/'sheets'
for p in (OUT,SCENES,SHEETS):p.mkdir(exist_ok=True,parents=True)
def readcsv(p):
    with p.open('r',encoding='utf-8-sig',newline='') as f:return list(csv.DictReader(f))
def sha(path):
    h=hashlib.sha256()
    with path.open('rb') as f:
        for chunk in iter(lambda:f.read(1024*1024),b''):h.update(chunk)
    return h.hexdigest()
def rawsha(buf):return hashlib.sha256(buf).hexdigest()
v119=json.loads((ROOT/'review/v119_selected_A_new4633/MANIFEST.json').read_text('utf8'))
v117=json.loads((ROOT/'review/v117_A_candidates_10042/jumbo_a3/A3_SUMMARY.json').read_text('utf8'))
audit=json.loads((ROOT/'audits/map_range_26_43_to_37_49/SUMMARY.json').read_text('utf8'))
assert (audit['files_present'],audit['distinct_tile_keys_tile_layers'])==(84,10042)
selected=readcsv(ROOT/'review/v119_selected_A_new4633/REPRESENTATIVE_A_4633.csv')
assert len(selected)==4633
target={(r['tile_set_name'],int(r['local_id'])):r for r in selected
        if r['selection_status']=='selected_provisional'}
assert len(target)==4632 and len(selected)-len(target)==1
assert all(x['tile_set_name']!='' for x in selected)
assert all(r['local_id_mapping_verified']=='0' for r in target.values())
old=readcsv(ROOT/'analysis/imports/merged_catalog_5409.csv')
oldkeys={(r['tile_set_locator'],int(r['local_id'])) for r in old}
assert len(oldkeys)==5409 and not (oldkeys&target.keys())
master=readcsv(ROOT/'review/v117_A_candidates_10042/A_CANDIDATE_COMBINED_10042.csv')
fallback={(r['tile_set_name'],int(r['local_id'])):r for r in master}
assert len(fallback)==10042 and set(target).issubset(fallback)
names=[f'{x}_{y}.tmx' for x in range(26,38) for y in range(43,50)]
assert len(names)==84

# TMX layer 'level' may be either an attribute or a named property.
def layer_level(ly):
    if 'level' in ly.attrib:return int(ly.get('level','0'))
    prop=ly.find("properties/property[@name='level']")
    if prop is not None:return int(prop.get('value') or prop.text or '0')
    return 0
def load_map(name):
    root=ET.parse(MAPROOT/name).getroot()
    tiles=[]
    for e in root.findall('tileset'):
        if not e.get('name'):continue
        tiles.append((int(e.get('firstgid')),e.get('name')))
    tiles.sort()
    firsts=[x[0] for x in tiles]
    assert firsts and firsts==sorted(set(firsts))
    w=int(root.get('width','256'));h=int(root.get('height','256'))
    layers=[]
    for ix,ly in enumerate(root.iter('layer')):
        dat=ly.find('data')
        assert dat is not None and dat.get('encoding')=='csv', (name,ly.get('name'))
        lw=int(ly.get('width',w));lh=int(ly.get('height',h))
        vals=[int(v) for v in re.findall(r'\d+',dat.text or '')]
        assert len(vals)==lw*lh,(name,ly.get('name'),len(vals),lw,lh)
        assert lw==w and lh==h
        layers.append(dict(index=ix,name=ly.get('name',''),level=layer_level(ly),width=lw,
                           values=vals))
    return dict(firsts=firsts,tiles=tiles,w=w,h=h,layers=layers)
def key_from_raw(m,raw):
    value=raw&0x0fffffff
    if not value:return None
    ix=bisect.bisect_right(m['firsts'],value)-1
    if ix<0:return None
    first,name=m['tiles'][ix]
    return name,value-first

# 1. Enumerate true TMX uses, not guessed placements from sprite atlas. First
# in-bounds occurrence is chosen; if none, use first edge occurrence.
placements={};count_used=Counter();mapSHA={}
for idx,name in enumerate(names):
    path=MAPROOT/name
    item=audit['per_map'][idx]
    assert item['tmx']==name
    assert path.stat().st_size==item['filesize_bytes']
    actual=sha(path)
    assert actual==item['sha256'],(name,'source TMX SHA mismatch')
    mapSHA[name]=actual
    m=load_map(name)
    hits=0
    for ly in m['layers']:
        w=ly['width'];h=m['h']
        for i,raw in enumerate(ly['values']):
            if not raw:continue
            key=key_from_raw(m,raw)
            if key not in target:continue
            count_used[key]+=1
            x=i%w;y=i//w
            old=placements.get(key)
            # Reserve first occurrence, improve only if first was at the 5x5 edge.
            bounded=2<=x<w-2 and 2<=y<h-2
            if old is None or (old['near_boundary'] and bounded):
                placements[key]=dict(tmx=name,layer=ly['name'],layer_index=ly['index'],
                  level=ly['level'],x=x,y=y,raw_gid=raw,
                  near_boundary=not bounded,selected_preference='first_valid_in_bounds'
                  if bounded else 'first_boundary_fallback')
                hits+=int(old is None)
    if (idx+1)%7==0:
        print('INDEXED',idx+1,'/84','FOUND',len(placements),'/4632','CURRENT',name,flush=True)
assert len(placements)==4632, ('keys without placement',list(target.keys()-placements.keys())[:12])
assert len(count_used)==4632 and all(v>0 for v in count_used.values())
path=OUT/'PLACEMENTS_4632.csv'
placefields=['tile_set_name','local_id','tmx','level','layer','layer_index','x','y','raw_gid',
  'total_uses_84_tmx','near_boundary','selection_preference']
with path.open('w',encoding='utf-8-sig',newline='') as f:
    w=csv.writer(f);w.writerow(placefields)
    for key in sorted(placements):
        v=placements[key]
        w.writerow([*key,v['tmx'],v['level'],v['layer'],v['layer_index'],v['x'],v['y'],
                    v['raw_gid'],count_used[key],int(v['near_boundary']),v['selected_preference']])
print('LOCATIONS verified 4632, began B assembly',flush=True)

# 2. Rehydrate exact v119 chosen A crops for every new target and every visible
# newer neighbor, while using v117 provisional A for older scene neighbors.
# Strict per-pixel SHA check verifies v119 source correspondence.
@lru_cache(maxsize=3)
def get_atlas(relpath):
    with Image.open(ROOT/relpath) as im:
        return im.convert('RGBA')
def parse_bbox(st):
    if not st:return None
    st=st.strip().strip('[]')
    a=[int(x.strip()) for x in st.split(',')]
    assert len(a)==4 and a[2]>a[0] and a[3]>a[1]
    return a
@lru_cache(maxsize=1600)
def tile(key):
    src=target.get(key)
    if src:
        rel=src['source_image_path'];bbox=parse_bbox(src['selected_crop_xyxy'])
        check=src['selected_rgba_pixel_sha256']
        provider='v119_selected'
    else:
        src=fallback.get(key)
        if src is None:return None,'unlisted_tile'
        rel=src['source_png_path']
        choice=src['new_preferred_A']
        if choice=='A3':
            bbox=parse_bbox(src['A3_crop_bbox']);check=src['A3_pixel_sha256']
        elif choice in ('A1','A1=A2'):
            bbox=parse_bbox(src['A1_bbox']);check=src['A1_pixel_sha256']
        elif choice=='A2':
            bbox=parse_bbox(src['A2_bbox']);check=src['A2_pixel_sha256']
        else:return None,'prior_no_selected_crop'
        provider='v117_neighbor_provisional'
    if not rel or bbox is None or not check:return None,'png_or_bbox_absent'
    atlas=get_atlas(rel)
    if bbox[0]<0 or bbox[1]<0 or bbox[2]>atlas.width or bbox[3]>atlas.height:
        return None,'source_bbox_out_of_bounds'
    sprite=atlas.crop(tuple(bbox))
    assert rawsha(sprite.tobytes())==check, (key,'SOURCE IMAGE PIXEL SHA MISMATCH')
    if not sprite.getbbox():return None,'zero_alpha_source_crop'
    return sprite,provider

def flip_sprite(im,raw):
    # Tiled 32-bit 3 orthogonal transform flags; PZ export generally has no flips.
    # Supported as visual approximation with flag explicitly recorded.
    diagonal=bool(raw&0x20000000)
    horizontal=bool(raw&0x80000000)
    vertical=bool(raw&0x40000000)
    if not(horizontal or vertical or diagonal):return im
    if diagonal:im=im.transpose(Image.Transpose.TRANSPOSE)
    if horizontal:im=im.transpose(Image.Transpose.FLIP_LEFT_RIGHT)
    if vertical:im=im.transpose(Image.Transpose.FLIP_TOP_BOTTOM)
    return im
fontp='/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
font=ImageFont.truetype(fontp,12)
tiny=ImageFont.truetype(fontp,10)
CW=800;CH=580
stats=Counter()
reports=[]
def draw_b(m,place):
    x0,y0=place['x'],place['y']
    assert 0<=x0<m['w'] and 0<=y0<m['h']
    canvas=Image.new('RGBA',(CW,CH),(237,242,247,255))
    level=place['level']; missing=Counter();rendered=0
    layers_same=0
    # This is the B scene, *without target removal*; v120 does not build C.
    for ly in m['layers']:
        if ly['level']!=level:continue
        layers_same+=1
        cmd=[]
        w=ly['width'];vals=ly['values']
        for dy in range(-2,3):
            y=y0+dy
            if y<0 or y>=m['h']:continue
            for dx in range(-2,3):
                x=x0+dx
                if x<0 or x>=m['w']:continue
                raw=vals[y*w+x]
                if raw:cmd.append((dx+dy,dy,dx,raw))
        cmd.sort()
        for _,dy,dx,raw in cmd:
            key=key_from_raw(m,raw)
            if key is None:missing['unmapped_gid']+=1;continue
            im,provenance=tile(key)
            if im is None:missing[provenance]+=1;continue
            image=flip_sprite(im,raw)
            x=int(CW/2+(dx-dy)*58-image.width/2)
            y=int(CH/2+(dx+dy)*29+34-image.height)
            # Pillow.alpha_composite 2-arg requires nonnegative positions, so
            # clip large JUMBO sprites without changing or rescaling source pixels.
            if x<0 or y<0 or x+image.width>CW or y+image.height>CH:
                cl=(max(0,-x),max(0,-y),min(image.width,CW-x),min(image.height,CH-y))
                if cl[2]<=cl[0] or cl[3]<=cl[1]:
                    missing['outside_scene_canvas']+=1
                    continue
                image=image.crop(cl)
                x=max(0,x);y=max(0,y)
                stats['clipped_sprite_draws']+=1
            canvas.alpha_composite(image,(x,y))
            rendered+=1
    return canvas.convert('RGB'),rendered,dict(missing),layers_same
def panel(board,slot,im,title,bbox,empty=False):
    x=(slot%8)*240;y=(slot//8)*185
    dr=ImageDraw.Draw(board)
    dr.rectangle((x+1,y+1,x+237,y+183),fill=(252,253,254),outline=(148,168,185))
    dr.text((x+7,y+7),title[:34],font=tiny,fill=(34,53,67))
    dr.text((x+7,y+24),bbox,font=tiny,fill=(71,82,93))
    if not empty:
        thumb=im.copy();thumb.thumbnail((234,143),Image.Resampling.LANCZOS)
        board.paste(thumb,(x+(240-thumb.width)//2,y+38+(143-thumb.height)//2))
    else:
        dr.text((x+15,y+80),'B NOT AVAILABLE',font=font,fill=(148,60,47))
class OutputZip:
    def __init__(self):self.current=None;self.shard=-1;self.count=0
    def write(self,index,image):
        shard=(index//400)
        if shard!=self.shard:
            if self.current:self.current.close()
            self.shard=shard
            path=SCENES/f'B_5x5_{shard:02}.zip'
            self.current=zipfile.ZipFile(path,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=2)
        entry=f'B_{index:05}.webp'
        buf=io.BytesIO();image.save(buf,format='WEBP',quality=78,method=3)
        b=buf.getvalue()
        self.current.writestr(entry,b)
        self.count+=1
        return (f'b_png_shards/B_5x5_{shard:02}.zip',entry,rawsha(b),len(b))
    def close(self):
        if self.current:self.current.close()
output=OutputZip()
# Group by TMX to load each map once in the rendering pass.
pairs={k:v for k,v in placements.items()}
permap=defaultdict(list)
for idx,(key,v) in enumerate(sorted(pairs.items())):
    permap[v['tmx']].append((idx,key,v))
ORDERED=[None]*4632
cards={}
for imap,name in enumerate(names):
    req=permap.get(name,[])
    if not req:continue
    m=load_map(name)
    for idx,key,v in req:
        image,drawn,missing,layers_same=draw_b(m,v)
        # Delay compressed archives until global sorted index order is restored.
        # Store WebP bytes, not full images, to bound peak RSS.
        buf=io.BytesIO();image.save(buf,format='WEBP',quality=78,method=3)
        b=buf.getvalue()
        ORDERED[idx]=(key,v,drawn,missing,layers_same,b)
        stats['B_rendered']+=1
        if missing:stats['B_with_any_missing_neighbors']+=1
        if v['near_boundary']:stats['B_edge_5x5_truncated']+=1
        stats['B_missing_neighbor_sprite_draws']+=sum(missing.values())
    tile.cache_clear()
    get_atlas.cache_clear()
    if (imap+1)%7==0:print('RENDER',imap+1,'/84','rendered',stats['B_rendered'],'of',4632,flush=True)
assert all(item is not None for item in ORDERED)
# 3. Output B images and 58 contact sheets in canonical stable key order.
board=Image.new('RGB',(1920,1850),(234,240,246))
for idx,item in enumerate(ORDERED):
    key,v,drawn,missing,layers_same,encoded=item
    if idx%80==0:board=Image.new('RGB',(1920,1850),(234,240,246))
    with Image.open(io.BytesIO(encoded)) as im:bim=im.convert('RGB')
    shard=(idx//400)
    if shard!=output.shard:
        if output.current:output.current.close()
        output.shard=shard
        output.current=zipfile.ZipFile(SCENES/f'B_5x5_{shard:02}.zip',
            'w',compression=zipfile.ZIP_DEFLATED,compresslevel=2)
    entry=f'B_{idx:05}.webp'
    output.current.writestr(entry,encoded)
    output.count+=1
    panel(board,idx%80,bim,f'{idx:05} {key[0]}',
          f'ID {key[1]}  {v["tmx"]} L{v["level"]} x{v["x"]} y{v["y"]}')
    if idx%80==79 or idx==4631:
        board.save(SHEETS/f'B_5x5_{idx//80:03}.jpg',quality=83,optimize=True)
    target_src=target[key]
    reports.append(dict(
      tile_set_name=key[0],local_id=key[1],scene_status='rendered_approximate',
      tmx_file=v['tmx'],tmx_sha256=mapSHA[v['tmx']],
      source_level=v['level'],source_layer=v['layer'],source_layer_index=v['layer_index'],
      source_x=v['x'],source_y=v['y'],source_raw_gid=v['raw_gid'],
      source_raw_gid_hex=hex(v['raw_gid']),source_tmx_flips=hex(v['raw_gid']&0xf0000000),
      source_occurrence_count_84_maps=count_used[key],
      layer_count_same_floor=layers_same,neighbor_tiles_rendered=drawn,
      neighbor_tiles_skipped=sum(missing.values()),
      missing_reason_json=json.dumps(missing,ensure_ascii=False,sort_keys=True),
      scene_truncated_at_map_edge=int(v['near_boundary']),
      scene_canvas_clipping_possible=1,scene_window='5x5',
      scene_rendering='isometric_approximation_using_original_PNG_RGBA_layer_order',
      B_zip_shard=f'b_png_shards/B_5x5_{shard:02}.zip',
      B_zip_entry=entry,B_webp_file_sha256=rawsha(encoded),
      B_file_bytes=len(encoded),
      B_contact_sheet=f'sheets/B_5x5_{idx//80:03}.jpg',
      B_contact_sheet_cell=idx%80,
      selected_A_zip_shard=target_src['selected_shard'],
      selected_A_zip_entry=target_src['selected_zip_entry'],
      selected_A_RGBA_pixel_sha256=target_src['selected_rgba_pixel_sha256'],
      used_v119_selected_A=True,
      official_tmx_localid_mapping_verified=0,
      A_b_mapping_verification='pending',
      tilezed_verified=0,
      final_identity_certified=0))
    if (idx+1)%800==0:print('COMPRESSED',idx+1,'of',4632,flush=True)
output.close()
assert output.count==4632
assert len(reports)==4632
assert len(list(SHEETS.glob('B_5x5_*.jpg')))==58
shards=sorted(SCENES.glob('B_5x5_*.zip'))
assert len(shards)==12
checks=[]
for p in shards:
    with zipfile.ZipFile(p) as z:
        assert z.testzip() is None
        entries=len(z.namelist())
    checks.append(dict(file=p.name,entries=entries,bytes=p.stat().st_size,sha256=sha(p),crc='PASS'))
assert sum(x['entries'] for x in checks)==4632
ledger=OUT/'B_CONTEXT_4632.csv'
keys=list(reports[0])
with ledger.open('w',encoding='utf-8-sig',newline='') as f:
    w=csv.DictWriter(f,fieldnames=keys);w.writeheader();w.writerows(reports)
manifest=dict(version='v120',date='2026-10-27',
 scope='only_new_4632_with_A_provisional',
 range='26_43_to_37_49_84_tmx',source_tile_scope_10042=10042,
 reused_prior_5409_unchanged=True,
 new_keys_with_A=4632,
 B_actual_tmx_placement_indexed=4632,
 B_5x5_rendered=4632,
 prior_existing_target_images_regenerated=0,
 remaining_new_without_A=1,
 held_new_key='overlay_graffiti_wall_02/2',
 source_TMX_sha256=mapSHA,
 B_with_missing_neighbors=stats['B_with_any_missing_neighbors'],
 missing_neighbor_draws=stats['B_missing_neighbor_sprite_draws'],
 B_truncated_by_map_edge=stats['B_edge_5x5_truncated'],
 sprite_draws_clipped_by_canvas=stats['clipped_sprite_draws'],
 metadata_csv=ledger.relative_to(ROOT).as_posix(),
 metadata_sha256=sha(ledger),
 placement_csv=path.relative_to(ROOT).as_posix(),
 placement_sha256=sha(path),
 B_contact_sheet_count=58,
 B_image_zip_shards=checks,
 source_A_version='v119',
 source_A_ledger_sha256=v119['selected_ledger_sha256'],
 used_prior_v117_A_for_neighbor_context=True,
 original_png_pixel_integrity_checked=True,
 official_mapping_verified=0,
 TileZed_rendering_certified=0,
 AI_scene_visually_verified_all=0,
 identity_certified=0,
 B_only=True,
 note='B shows a real TMX tile occurrence and same-floor 5x5 neighborhood rendered via approximated isometric sprite layering; surrounding old/other A crops remain provisional and scene can be occluded/clipped. C and D not generated. Not an official TileZed render.')
(OUT/'MANIFEST.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n','utf8')
print('PASS V120',json.dumps({k:manifest[k] for k in
  ('B_actual_tmx_placement_indexed','B_5x5_rendered','B_with_missing_neighbors',
  'missing_neighbor_draws','B_truncated_by_map_edge','B_contact_sheet_count')},
  ensure_ascii=False),'ZIP SHARDS',len(checks),flush=True)
