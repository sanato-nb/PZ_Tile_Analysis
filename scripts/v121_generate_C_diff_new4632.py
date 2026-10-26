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
OUT=ROOT/'review/v121_C_diff_new4632'
SCENES=OUT/'c_png_shards'
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


# C is a genuine removal from a *single TMX layer* and *single cell*.
# v120 B must be reproduced byte-for-byte before C and B-C are trusted.
from PIL import ImageChops
from tempfile import TemporaryDirectory
DIFFS=OUT/'difference_png_shards'
DIFFS.mkdir(exist_ok=True)
BASE=ROOT/'review/v120_B_context_new4632'
prev=json.loads((BASE/'MANIFEST.json').read_text('utf8'))
assert prev['B_5x5_rendered']==4632 and prev['source_A_ledger_sha256']==v119['selected_ledger_sha256']
with (BASE/'B_CONTEXT_4632.csv').open(encoding='utf-8-sig',newline='') as f:
    baserows=list(csv.DictReader(f))
assert len(baserows)==4632
assert rawsha((BASE/'B_CONTEXT_4632.csv').read_bytes())==prev['metadata_sha256']
assert len({(r['tile_set_name'],int(r['local_id'])) for r in baserows})==4632
assert set((r['tile_set_name'],int(r['local_id'])) for r in baserows)==set(target)
assert all(r['source_raw_gid'] for r in baserows)
DIFF_W=800;DIFF_H=580
CLOG=Counter()
def pair_scene(m,p,key):
    """Reproduce v120 original B, then C with one target GID skipped,
    using the same sprite composition order and original PNG source pixels."""
    x0=int(p['source_x']);y0=int(p['source_y'])
    idx=int(p['source_layer_index']);rawtarget=int(p['source_raw_gid'])
    level=int(p['source_level'])
    assert 0<=x0<m['w'] and 0<=y0<m['h']
    B=Image.new('RGBA',(CW,CH),(237,242,247,255))
    C=Image.new('RGBA',(CW,CH),(237,242,247,255))
    missing=Counter();rendered=0;layers_same=0;removed=0
    visible_tgt=0;occluded_tgt=0
    for ly in m['layers']:
        if ly['level']!=level:continue
        layers_same+=1
        w=ly['width'];vals=ly['values'];cmd=[]
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
            k=key_from_raw(m,raw)
            if k is None:missing['unmapped_gid']+=1;continue
            im,provider=tile(k)
            if im is None:
                missing[provider]+=1
                continue
            image=flip_sprite(im,raw)
            px=int(CW/2+(dx-dy)*58-image.width/2)
            py=int(CH/2+(dx+dy)*29+34-image.height)
            if px<0 or py<0 or px+image.width>CW or py+image.height>CH:
                box=(max(0,-px),max(0,-py),min(image.width,CW-px),min(image.height,CH-py))
                if box[2]<=box[0] or box[3]<=box[1]:
                    missing['outside_scene_canvas']+=1
                    continue
                image=image.crop(box);px=max(0,px);py=max(0,py)
                stats['clipped_sprite_draws']+=1
            # The original B layer and draw order is identical to the v120 renderer.
            B.alpha_composite(image,(px,py))
            rendered+=1
            exactly_target=(ly['index']==idx and dx==0 and dy==0)
            if exactly_target:
                assert raw==rawtarget and k==key,(p['tmx_file'],idx,x0,y0,key,k,raw,rawtarget)
                removed+=1
                visible_tgt=int(bool(image.getbbox()))
                # Skip this one draw in C; do NOT remove other tiles on same cell.
            else:
                C.alpha_composite(image,(px,py))
    assert removed==1,(key,'target sprite not actually rendered',p)
    return B.convert('RGB'),C.convert('RGB'),rendered,dict(missing),layers_same,visible_tgt

def webp(image,lossless=False):
    out=io.BytesIO()
    if lossless:image.save(out,format='WEBP',lossless=True,method=4)
    else:image.save(out,format='WEBP',quality=78,method=3)
    return out.getvalue()

def difference_exact(b,c):
    """No lossy WebP/JPEG in the pixel-difference calculation."""
    assert b.size==c.size==(DIFF_W,DIFF_H)
    channels=ImageChops.difference(b,c)
    mask=channels.convert('L').point(lambda value:255 if value else 0)
    pix=mask.histogram()[255]
    box=mask.getbbox()
    diff=Image.new('RGBA',b.size,(0,0,0,0))
    # Red mask marks every changed RGB pixel. Alpha=0 elsewhere.
    red=Image.new('RGBA',b.size,(250,38,48,215))
    diff.paste(red,(0,0),mask)
    assert diff.getchannel('A').getbbox()==box
    return diff,pix,box

# Scenes may be grouped by TMX for just one XML parse per map.
bymap=defaultdict(list)
for rownum,r in enumerate(baserows):
    bymap[r['tmx_file']].append((rownum,r))
assert len(bymap)<=84
fieldkeys=['tile_set_name','local_id','tmx_file','source_level','source_layer',
    'source_layer_index','source_x','source_y','source_raw_gid',
    'B_webp_file_sha256','B_source_zip_shard','B_source_zip_entry',
    'C_status','removed_exactly_one_raw_gid','C_zip_shard','C_zip_entry',
    'C_webp_file_sha256','C_webp_bytes','DIFF_zip_shard','DIFF_zip_entry',
    'DIFF_png_file_sha256','DIFF_png_bytes',
    'B_minus_C_changed_pixels','B_minus_C_nonzero','B_minus_C_bbox',
    'source_neighbor_tiles_rendered_B','source_neighbor_skipped_B',
    'scene_window','B_C_same_floor','B_C_same_layer_order',
    'target_A_RGBA_hash','quality_reason','visible_target_crop_in_B',
    'v119_A_status','mapping_verified','tilezed_verified',
    'identity_final_certified','C_contact_sheet','C_sheet_slot']
report=[None]*4632
with TemporaryDirectory(prefix='pz_v121_C_') as tmp:
    TMP=Path(tmp)
    for i,name in enumerate(names):
        path=MAPROOT/name
        expect=audit['per_map'][i]
        assert expect['tmx']==name
        assert path.stat().st_size==expect['filesize_bytes']
        assert sha(path)==expect['sha256'],(name,'source TMX SHA changed')
        if not bymap[name]:continue
        m=load_map(name)
        for rownum,r in bymap[name]:
            key=(r['tile_set_name'],int(r['local_id']))
            assert key in target
            layer=m['layers'][int(r['source_layer_index'])]
            x=int(r['source_x']);y=int(r['source_y'])
            assert layer['name']==r['source_layer']
            assert layer['level']==int(r['source_level'])
            assert layer['values'][y*m['w']+x]==int(r['source_raw_gid'])
            assert key_from_raw(m,layer['values'][y*m['w']+x])==key
            B,C,drawn,missing,layerCount,visible=pair_scene(m,r,key)
            assert drawn==int(r['neighbor_tiles_rendered']),(key,'render count mismatch')
            assert sum(missing.values())==int(r['neighbor_tiles_skipped']),(key,missing)
            assert json.dumps(missing,ensure_ascii=False,sort_keys=True)==r['missing_reason_json']
            assert layerCount==int(r['layer_count_same_floor'])
            # Byte-exact v120 regeneration check; rejects silent renderer drift.
            encodedB=webp(B)
            assert rawsha(encodedB)==r['B_webp_file_sha256'], (key,'B render mismatch to archived v120')
            encodedC=webp(C,lossless=True)
            delta,pixels,bbox=difference_exact(B,C)
            dbuf=io.BytesIO();delta.save(dbuf,format='PNG',compress_level=5)
            dbytes=dbuf.getvalue()
            (TMP/f'{rownum:05}_B.webp').write_bytes(encodedB)
            (TMP/f'{rownum:05}_C.webp').write_bytes(encodedC)
            (TMP/f'{rownum:05}_DIFF.png').write_bytes(dbytes)
            CLOG['rendered']+=1
            if pixels:CLOG['nonzero']+=1
            else:CLOG['zero_delta']+=1
            if int(r['scene_truncated_at_map_edge']):CLOG['edge']+=1
            if missing:CLOG['some_neighbor_missing']+=1
            q=('zero_diff_not_transparency_clipped_occluded_or_missing_mapping'
               if pixels==0 else 'changed_pixels_only_provisional_atlas_mapping')
            czip=f'c_png_shards/C_5x5_{rownum//400:02d}.zip'
            dzip=f'difference_png_shards/DELTA_{rownum//400:02d}.zip'
            report[rownum]=dict(
                tile_set_name=key[0],local_id=key[1],
                tmx_file=name,source_level=int(r['source_level']),
                source_layer=r['source_layer'],source_layer_index=int(r['source_layer_index']),
                source_x=x,source_y=y,source_raw_gid=int(r['source_raw_gid']),
                B_webp_file_sha256=r['B_webp_file_sha256'],
                B_source_zip_shard=r['B_zip_shard'],B_source_zip_entry=r['B_zip_entry'],
                C_status='same_scene_single_tile_removed',removed_exactly_one_raw_gid=1,
                C_zip_shard=czip,C_zip_entry=f'C_{rownum:05}.webp',
                C_webp_file_sha256=rawsha(encodedC),C_webp_bytes=len(encodedC),
                DIFF_zip_shard=dzip,DIFF_zip_entry=f'DELTA_{rownum:05}.png',
                DIFF_png_file_sha256=rawsha(dbytes),DIFF_png_bytes=len(dbytes),
                B_minus_C_changed_pixels=pixels,B_minus_C_nonzero=int(pixels>0),
                B_minus_C_bbox=json.dumps(bbox) if bbox else '',
                source_neighbor_tiles_rendered_B=drawn,
                source_neighbor_skipped_B=sum(missing.values()),
                scene_window='5x5',
                B_C_same_floor=1,B_C_same_layer_order=1,
                target_A_RGBA_hash=target[key]['selected_rgba_pixel_sha256'],
                quality_reason=q,visible_target_crop_in_B=visible,
                v119_A_status=target[key]['selection_status'],
                mapping_verified=0,tilezed_verified=0,identity_final_certified=0,
                C_contact_sheet=f'sheets/C_B_DIFF_{rownum//80:03d}.jpg',
                C_sheet_slot=rownum%80)
        tile.cache_clear()
        get_atlas.cache_clear()
        if (i+1)%7==0:
            print('C_RENDER_PROGRESS',i+1,'/84','scenes',CLOG['rendered'],'of 4632',flush=True)
    assert all(x is not None for x in report)
    assert CLOG['rendered']==4632
    # Archive C and difference with CRC and exact SHA per entry.
    Czip=None;Dzip=None
    for n,r in enumerate(report):
        if n%400==0:
            if Czip:Czip.close();Dzip.close()
            Czip=zipfile.ZipFile(SCENES/f'C_5x5_{n//400:02d}.zip','w',
                compression=zipfile.ZIP_DEFLATED,compresslevel=2)
            Dzip=zipfile.ZipFile(DIFFS/f'DELTA_{n//400:02d}.zip','w',
                compression=zipfile.ZIP_DEFLATED,compresslevel=2)
        a=(TMP/f'{n:05}_C.webp').read_bytes()
        d=(TMP/f'{n:05}_DIFF.png').read_bytes()
        assert rawsha(a)==r['C_webp_file_sha256']
        assert rawsha(d)==r['DIFF_png_file_sha256']
        Czip.writestr(r['C_zip_entry'],a)
        Dzip.writestr(r['DIFF_zip_entry'],d)
        if n%80==0:
            board=Image.new('RGB',(3600,2050),(235,241,246))
            pen=ImageDraw.Draw(board)
        x=(n%8)*450;y=((n%80)//8)*205
        pen.rectangle((x+1,y+1,x+448,y+203),fill=(254,254,255),outline=(163,174,188))
        pen.text((x+7,y+7),f'{n:05d} {r["tile_set_name"][:36]}',font=tiny,fill=(29,47,66))
        pen.text((x+7,y+24),f'ID {r["local_id"]}   B-C pixels {r["B_minus_C_changed_pixels"]}',
                 font=tiny,fill=(155,53,52) if r['B_minus_C_nonzero'] else (112,89,62))
        # Display three actual images with stable 143x140 subpanels.
        for k,filename,desc in [(0,'B.webp','B original'),(1,'C.webp','C removed'),(2,'DIFF.png','B-C delta')]:
            f=TMP/f'{n:05}_{filename}'
            with Image.open(f) as im:
                if im.mode!='RGBA':im=im.convert('RGBA')
                if desc=='B-C delta':
                    pale=Image.new('RGB',(143,130),(235,241,248))
                else:
                    pale=Image.new('RGB',(143,130),(240,244,247))
                im.thumbnail((141,127),Image.Resampling.LANCZOS)
                pale.paste(im,((143-im.width)//2,(130-im.height)//2),im)
            board.paste(pale,(x+3+148*k,y+46))
            pen.text((x+9+148*k,y+182),desc,font=tiny,fill=(70,89,104))
        if n%80==79 or n==4631:
            board.save(SHEETS/f'C_B_DIFF_{n//80:03d}.jpg',quality=87,optimize=True)
        if (n+1)%500==0:
            print('C_ARCHIVE_PROGRESS',n+1,'of 4632',flush=True)
    Czip.close();Dzip.close()
assert len(report)==4632
assert len(list(SHEETS.glob('C_B_DIFF_*.jpg')))==58
assert len(list(SCENES.glob('C_5x5_*.zip')))==12
assert len(list(DIFFS.glob('DELTA_*.zip')))==12
def archive_report(paths):
    out=[]
    for p in sorted(paths):
        with zipfile.ZipFile(p) as z:
            assert z.testzip() is None
            n=len(z.namelist())
        out.append(dict(path=p.relative_to(ROOT).as_posix(),entries=n,
                        bytes=p.stat().st_size,sha256=sha(p),CRC='PASS'))
    assert sum(x['entries'] for x in out)==4632
    return out
carchives=archive_report(SCENES.glob('C_5x5_*.zip'))
darchives=archive_report(DIFFS.glob('DELTA_*.zip'))
ledger=OUT/'C_B_DIFFERENCE_4632.csv'
with ledger.open('w',encoding='utf-8-sig',newline='') as f:
    w=csv.DictWriter(f,fieldnames=fieldkeys);w.writeheader();w.writerows(report)
zero=OUT/'ZERO_DELTA_REVIEW.csv'
with zero.open('w',encoding='utf-8-sig',newline='') as f:
    w=csv.DictWriter(f,fieldnames=fieldkeys);w.writeheader()
    w.writerows(r for r in report if not r['B_minus_C_nonzero'])
assert sum(int(r['B_minus_C_nonzero']) for r in report)==CLOG['nonzero']
assert sum(1 for r in report if not r['B_minus_C_nonzero'])==CLOG['zero_delta']
m=dict(version='v121',date='2026-10-27',phase='C=one_actual_TMX_GID_removed',
     scope='only_new_4632_with_v119_selected_A',
     source_TMX_84_sha=audit['distinct_tile_keys_sha256'],
     source_B_manifest_sha=prev['metadata_sha256'],
     source_A_manifest_sha=v119['selected_ledger_sha256'],
     existing_5409_reused_not_reanalyzed=True,
     target_new_4632=4632,processed_4632=CLOG['rendered'],
     exact_one_layer_one_cell_GID_removed=4632,
     B_byte_exact_regenerated_and_SHA_matches=4632,
     C_5x5_rendered=4632,
     nonzero_B_minus_C=CLOG['nonzero'],
     zero_B_minus_C=CLOG['zero_delta'],
     scenes_edge_window_incomplete=CLOG['edge'],
     scenes_with_missing_neighbor_source=CLOG['some_neighbor_missing'],
     contact_sheets=58, C_archives=carchives, DIFF_archives=darchives,
     output_CSV=ledger.relative_to(ROOT).as_posix(),
     output_CSV_sha256=sha(ledger),
     zero_diff_csv=zero.relative_to(ROOT).as_posix(),
     zero_diff_csv_sha256=sha(zero),
     official_mapping_verified=0,identity_certified=0,TileZed_render_certified=0,
     AI_per_tile_visual_review_completed=False,
     note='Original v120 B regenerated byte-identically, C differs by only original target TMX raw GID in one exact layer/cell. Pixel diff before any lossy encoding. Zero delta does not prove transparent tile: may be occluded, cropped, or incorrectly atlas-mapped. Unchanged original PNG/TMX/v116 SQLite.'
)
(OUT/'MANIFEST.json').write_text(json.dumps(m,ensure_ascii=False,indent=2)+'\n','utf8')
print('PASS v121 C pair exact removal and B SHA',json.dumps({
    k:m[k] for k in ('processed_4632','nonzero_B_minus_C','zero_B_minus_C',
                     'scenes_edge_window_incomplete','scenes_with_missing_neighbor_source',
                     'contact_sheets')}),
    'archives',len(carchives),len(darchives),flush=True)
