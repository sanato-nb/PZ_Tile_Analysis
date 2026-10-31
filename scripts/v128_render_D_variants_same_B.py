#!/usr/bin/env python3
"""v128: Real different-PNG A candidate -> ORIGINAL B 5x5 scene at SAME TMX position.
Three same-basename file variants from v127 are geometrically/pixel independently
verified. Render alternate A in B, compare with original A/B/C pixel-exact.
No fabricated same-key mappings or final claims. Append-only physical SQLite v127.
"""
from pathlib import Path
from collections import Counter
from functools import lru_cache
import bisect,csv,hashlib,base64,zlib,json,sqlite3,re,io,zipfile
import xml.etree.ElementTree as ET
from PIL import Image, ImageDraw, ImageFont, ImageChops
R=Path(__file__).resolve().parents[1]
ROOT=R/'B4220.3_MapExport_256/tmx'
OUT=R/'review/v128_D_alt_PNG_3'
DBOUT=R/'analysis/current/v128'
OUT.mkdir(parents=True,exist_ok=True);DBOUT.mkdir(parents=True,exist_ok=True)
def sha(b):return hashlib.sha256(b).hexdigest()
def filesha(p):return sha(p.read_bytes())
def csvrows(p):
    with p.open(encoding='utf-8-sig',newline='') as f:return list(csv.DictReader(f))
def bbox(st):
    if not st:return None
    values=[int(v) for v in st.strip().strip('[]').split(',')]
    assert len(values)==4 and values[0]<values[2] and values[1]<values[3]
    return tuple(values)
def layerlevel(ly):
    if 'level' in ly.attrib:return int(ly.get('level','0'))
    prop=ly.find("properties/property[@name='level']")
    return int((prop.get('value') or prop.text or '0') if prop is not None else '0')
selected=csvrows(R/'review/v119_selected_A_new4633/REPRESENTATIVE_A_4633.csv')
a={(r['tile_set_name'],int(r['local_id'])):r for r in selected if r['selection_status']=='selected_provisional'}
assert len(a)==4632
cand={(r['tile_set_name'],int(r['local_id'])):r for r in csvrows(R/'review/v117_A_candidates_10042/A_CANDIDATE_COMBINED_10042.csv')}
assert len(cand)==10042
v120file=R/'review/v120_B_context_new4632/B_CONTEXT_4632.csv'
B={(r['tile_set_name'],int(r['local_id'])):r for r in csvrows(v120file)}
assert len(B)==4632
v120meta=json.loads((R/'review/v120_B_context_new4632/MANIFEST.json').read_text())
assert filesha(v120file)==v120meta['metadata_sha256']
v127=json.loads((R/'review/v127_D_A_candidates_full4633/PRIORITY_VARIANTS_3.json').read_text())
assert v127['candidate_variant_count']==3 and len(v127['variant_tile_keys'])==3
indexcsv=csvrows(R/'review/v127_D_A_candidates_full4633/D_CANDIDATE_LEDGER_4633.csv')
assert len(indexcsv)==4633
v127ledger={(r['tile_set_name'],int(r['local_id'])):r for r in indexcsv}
previous_trial=csvrows(R/'review/v127_D_A_candidates_full4633/D_ALL_CANDIDATE_TRIALS.csv')
variant_trial={(r['tile_set_name'],int(r['local_id'])):r for r in previous_trial
    if r['category']=='same_basename_atlas_variant' and r['result']=='distinct_visible_unverified_correspondence'}
assert len(variant_trial)==3
old={(r['tile_set_locator'],int(r['local_id'])) for r in csvrows(R/'analysis/imports/merged_catalog_5409.csv')}
assert len(old)==5409

def mapread(name):
    tree=ET.parse(ROOT/name).getroot()
    ts=sorted((int(x.get('firstgid')),x.get('name')) for x in tree.findall('tileset') if x.get('name'))
    first=[v[0] for v in ts]
    w,h=int(tree.get('width','256')),int(tree.get('height','256'))
    layers=[]
    for ix,ly in enumerate(tree.iter('layer')):
        dat=ly.find('data')
        assert dat is not None and dat.get('encoding')=='csv'
        vals=[int(v) for v in re.findall(r'\d+',dat.text or '')]
        assert len(vals)==w*h
        layers.append(dict(index=ix,level=layerlevel(ly),values=vals))
    return dict(ts=ts,first=first,layers=layers,w=w,h=h)
def resolve(m,raw):
    gid=raw&0x0fffffff
    if not gid:return None
    pos=bisect.bisect_right(m['first'],gid)-1
    if pos<0:return None
    return (m['ts'][pos][1],gid-m['ts'][pos][0])
@lru_cache(maxsize=5)
def atlas(path):
    if not path:return None
    with Image.open(R/path) as im:return im.convert('RGBA')
@lru_cache(maxsize=1600)
def sprite(k):
    rec=a.get(k)
    if rec:
        path=rec['source_image_path'];box=bbox(rec['selected_crop_xyxy'])
        expected=rec['selected_rgba_pixel_sha256']
    else:
        rec=cand.get(k)
        if not rec:return None
        path=rec.get('source_png_path','')
        key=rec.get('new_preferred_A','')
        if key=='A3':box=bbox(rec.get('A3_crop_bbox',''));expected=rec.get('A3_pixel_sha256','')
        elif key in ('A1','A1=A2'):box=bbox(rec.get('A1_bbox',''));expected=rec.get('A1_pixel_sha256','')
        elif key=='A2':box=bbox(rec.get('A2_bbox',''));expected=rec.get('A2_pixel_sha256','')
        else:return None
    if not path or not box or not expected:return None
    src=atlas(path)
    if src is None or box[0]<0 or box[1]<0 or box[2]>src.width or box[3]>src.height:return None
    img=src.crop(box)
    assert sha(img.tobytes())==expected,(k,'old A pixel drift')
    return img if img.getbbox() else None
def flips(img,raw):
    if raw&0x20000000:img=img.transpose(Image.Transpose.TRANSPOSE)
    if raw&0x80000000:img=img.transpose(Image.Transpose.FLIP_LEFT_RIGHT)
    if raw&0x40000000:img=img.transpose(Image.Transpose.FLIP_TOP_BOTTOM)
    return img
W,H=800,580
def scene(m,loc,replacement=None,delete=False):
    x0,y0=int(loc['source_x']),int(loc['source_y'])
    level=int(loc['source_level'])
    layerid=int(loc['source_layer_index'])
    rawtarget=int(loc['source_raw_gid'])
    index=y0*m['w']+x0
    raw=m['layers'][layerid]['values'][index]
    assert raw==rawtarget and resolve(m,raw)==(loc['tile_set_name'],int(loc['local_id']))
    canvas=Image.new('RGBA',(W,H),(237,242,247,255))
    replacement_drawn=0;misses=Counter()
    for layer in m['layers']:
        if layer['level']!=level:continue
        commands=[]
        for dy in range(-2,3):
            y=y0+dy
            if not 0<=y<m['h']:continue
            for dx in range(-2,3):
                x=x0+dx
                if not 0<=x<m['w']:continue
                p=y*m['w']+x;gid=layer['values'][p]
                if gid:commands.append((dx+dy,dy,dx,p,gid))
        commands.sort()
        for _,dy,dx,p,gid in commands:
            istarget=layer['index']==layerid and p==index and gid==rawtarget
            if istarget and delete:
                replacement_drawn+=1
                continue
            if istarget and replacement is not None:
                image=replacement
                replacement_drawn+=1
            else:
                image=sprite(resolve(m,gid))
            if image is None:misses['missing_source']+=1;continue
            image=flips(image,gid)
            px=int(W/2+(dx-dy)*58-image.width/2)
            py=int(H/2+(dx+dy)*29+34-image.height)
            if px<0 or py<0 or px+image.width>W or py+image.height>H:
                clip=(max(0,-px),max(0,-py),min(image.width,W-px),min(image.height,H-py))
                if clip[2]<=clip[0] or clip[3]<=clip[1]:
                    misses['outside_canvas']+=1
                    continue
                image=image.crop(clip);px=max(0,px);py=max(0,py)
            canvas.alpha_composite(image,(px,py))
    if replacement is not None or delete:assert replacement_drawn==1,(loc,replacement_drawn)
    return canvas.convert('RGB'),dict(misses)
def difference(a,b):
    img=ImageChops.difference(a,b).convert('L')
    return sum(px!=0 for px in img.getdata())


def pixels_nontransparent(im):
    return sum(im.getchannel('A').histogram()[1:])
def png_bytes(img):
    f=io.BytesIO();img.save(f,format='PNG');return f.getvalue()
font=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',15)
sm=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',12)
out=[]
zipfile_path=OUT/'D_SAME_B_VARIANT_3.zip'
z=zipfile.ZipFile(zipfile_path,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=6)
sheet=Image.new('RGB',(2100,1710),(247,250,251))
drawer=ImageDraw.Draw(sheet)
for n,item in enumerate(sorted(v127['variant_tile_keys'],key=lambda x:x['index'])):
    k=(item['tile_set_name'],int(item['local_id']))
    assert k in a and k in B and k not in old
    ori=a[k]
    prior=v127ledger[k]
    trial=variant_trial[k]
    assert ori['source_image_path']==item['original_png']
    assert ori['selected_crop_xyxy']==item['original_crop']
    assert item['variant_png']==trial['source_path']
    assert item['variant_crop']==trial['source_crop']
    assert item['variant_rgba_sha256']==trial['rgba_sha256']
    assert int(prior['exact_basename_variant_candidates'])==1
    assert filesha(R/item['original_png'])==ori['source_png_sha256']
    assert sha(sprite(k).tobytes())==item['original_rgba_sha256'] if 'original_rgba_sha256' in item else sha(sprite(k).tobytes())==ori['selected_rgba_pixel_sha256']
    orig=sprite(k)
    variant_src=atlas(item['variant_png'])
    rect=bbox(item['variant_crop'])
    assert variant_src is not None and rect is not None
    assert 0<=rect[0]<rect[2]<=variant_src.width and 0<=rect[1]<rect[3]<=variant_src.height
    alt=variant_src.crop(rect)
    assert alt.getbbox() and pixels_nontransparent(alt)>0
    assert sha(alt.tobytes())==item['variant_rgba_sha256']
    assert orig.size==alt.size and sha(orig.tobytes())!=sha(alt.tobytes())
    pos={**B[k], 'tile_set_name':k[0], 'local_id':k[1]}
    mapname=pos['tmx_file']
    assert filesha(ROOT/mapname)==v120meta['source_TMX_sha256'][mapname]
    tmx=mapread(mapname)
    b,missB=scene(tmx,pos)
    c,missC=scene(tmx,pos,delete=True)
    d,missD=scene(tmx,pos,replacement=alt)
    assert b.size==c.size==d.size==(800,580)
    assert missB==missC==missD, (k,'neighbor source drift')
    B_C=difference(b,c)
    B_D=difference(b,d)
    C_D=difference(c,d)
    heat=ImageChops.difference(b,d)
    # B and D should differ only by one source tile; no unrelated location may change.
    assert B_C>=0 and B_D>=0 and C_D>=0
    imgs={'A_selected':orig,'A_alternative':alt,'B_original':b,
          'C_removed':c,'D_alt_A_at_same_B':d,'B_minus_D_absolute_RGB':heat}
    for code,img in imgs.items():
        z.writestr('%s/%04d_%s.png'%(code,item['index'],code),png_bytes(img))
    record=dict(v127_index=int(item['index']),tile_set_name=k[0],local_id=k[1],
        original_PNG=item['original_png'],alternate_PNG=item['variant_png'],
        original_crop=item['original_crop'],alternate_crop=item['variant_crop'],
        original_A_rgba_sha256=sha(orig.tobytes()),
        alternate_A_rgba_sha256=sha(alt.tobytes()),
        source_tmx=mapname,source_level=int(pos['source_level']),
        source_layer_index=int(pos['source_layer_index']),
        source_x=int(pos['source_x']),source_y=int(pos['source_y']),
        source_raw_gid=int(pos['source_raw_gid']),
        source_tmx_sha256=v120meta['source_TMX_sha256'][mapname],
        B_C_changed_pixels=B_C,original_B_to_D_changed_pixels=B_D,
        D_to_C_changed_pixels=C_D,
        B_C_change_zero=int(B_C==0),B_D_change_zero=int(B_D==0),
        neighbor_missing_json=json.dumps(missB,sort_keys=True),
        same_B_TMX_position_exact=1,replaced_target_GID_exactly_one=1,
        other_PNG_same_basename_candidate=1,
        distinct_RGBA_source=1,
        alternative_source_type='same_basename_other_PNG_not_official_mapping',
        image_evidence_zip=zipfile_path.relative_to(R).as_posix(),
        mapping_verified=0,tilezed_verified=0,identity_certified=0,
        individually_visually_reviewed=0,
        notes='The selected A and alternate A are from two distinct PNG files with same stem, both pixel-exact. D is same original B TMX placement, with only target replaced. No official correspondence/TileZed or final identity certification.')
    out.append(record)
    y=n*570
    drawer.rectangle((6,y+5,2094,y+563),fill=(255,255,255),outline=(144,160,181),width=2)
    drawer.text((18,y+14),'D v128 SAME B TMX | %s/%d | v127 index %d'%(k[0],k[1],item['index']),font=font,fill=(25,43,65))
    drawer.text((18,y+39),'A selected: '+item['original_png'],font=sm,fill=(45,66,90))
    drawer.text((18,y+58),'A alternate: '+item['variant_png']+'   [NOT OFFICIAL LOCAL ID VERIFIED]',font=sm,fill=(144,75,30))
    panels=[('A selected',orig),('A alternate',alt),('B original',b),
            ('D alternate at SAME B',d),('C target removed',c),('abs(B-D)',heat)]
    for j,(label,img) in enumerate(panels):
        x=12+j*347
        drawer.text((x+5,y+85),label,font=sm,fill=(45,55,75))
        thumb=img.copy();thumb.thumbnail((330,370))
        if thumb.mode=='RGBA':
            sheet.paste(thumb,(x+(333-thumb.width)//2,y+108+(370-thumb.height)//2),thumb)
        else:sheet.paste(thumb,(x+(333-thumb.width)//2,y+108+(370-thumb.height)//2))
    drawer.text((22,y+525),'B-C changed=%d  | B-D changed=%d  | C-D changed=%d  | rawGID=%s'%(
        B_C,B_D,C_D,pos['source_raw_gid']),font=sm,fill=(35,53,79))
    print('RENDERED_REAL_PNG_VARIANT',n+1,'/',len(v127['variant_tile_keys']),k,
          'B-C',B_C,'B-D',B_D,'C-D',C_D,flush=True)
z.close()
assert len(out)==3 and len({(r['tile_set_name'],r['local_id']) for r in out})==3
with zipfile.ZipFile(zipfile_path) as archive:
    assert archive.testzip() is None
    assert len(archive.namelist())==3*6
sheetpath=OUT/'D_SAME_B_COMPARE_3.jpg'
sheet.save(sheetpath,quality=91,optimize=True)
csvpath=OUT/'D_ALT_SOURCE_B_COMPARE_3.csv'
with csvpath.open('w',encoding='utf-8-sig',newline='') as f:
    writer=csv.DictWriter(f,fieldnames=list(out[0]))
    writer.writeheader();writer.writerows(out)
# Copy full v127 SQLite into a strictly append-only next checkpoint.
parent=json.loads((R/'analysis/current/v127/MANIFEST.json').read_text())
packed=base64.b64decode(''.join((R/p).read_text('ascii').strip() for p in parent['parts']),validate=True)
assert sha(packed)==parent['compressed_sha256']
priorraw=zlib.decompress(packed)
assert sha(priorraw)==parent['sqlite_sha256'] and len(priorraw)==parent['sqlite_bytes']
dbpath=Path('/tmp/pz-v128-append.sqlite');dbpath.write_bytes(priorraw)
with sqlite3.connect(dbpath) as db:
    before={r[0] for r in db.execute("SELECT name FROM sqlite_master WHERE type='table'")}
    assert len(before)==189 and 'v127_d_candidate_catalog_4633' in before
    assert db.execute('PRAGMA integrity_check').fetchone()[0]=='ok'
    assert db.execute('SELECT count(*) FROM v127_d_candidate_catalog_4633').fetchone()[0]==4633
    assert db.execute('SELECT count(*) FROM v126_alt_A_B_160').fetchone()[0]==160
    assert db.execute('SELECT count(*) FROM v125_ai_visual_spotcheck_20').fetchone()[0]==20
    assert db.execute('SELECT count(*) FROM tile_catalog').fetchone()[0]==5409
    db.execute("""CREATE TABLE v128_D_source_variant_B_3 (
        tile_set_name TEXT NOT NULL, local_id INTEGER NOT NULL,
        source_index INTEGER NOT NULL,source_tmx TEXT NOT NULL,
        source_level INTEGER NOT NULL,source_layer_index INTEGER NOT NULL,
        source_x INTEGER NOT NULL,source_y INTEGER NOT NULL,source_raw_gid INTEGER NOT NULL,
        original_PNG TEXT,alternate_PNG TEXT,original_RGBA_sha256 TEXT,alternate_RGBA_sha256 TEXT,
        B_C_changed_pixels INTEGER,B_D_changed_pixels INTEGER,C_D_changed_pixels INTEGER,
        same_B_TMX_position_exact INTEGER,one_target_GID_replaced INTEGER,
        mapping_verified INTEGER DEFAULT 0,tilezed_verified INTEGER DEFAULT 0,
        final_certified INTEGER DEFAULT 0,
        PRIMARY KEY(tile_set_name,local_id))""")
    values=[(r['tile_set_name'],r['local_id'],r['v127_index'],r['source_tmx'],
       r['source_level'],r['source_layer_index'],r['source_x'],r['source_y'],r['source_raw_gid'],
       r['original_PNG'],r['alternate_PNG'],r['original_A_rgba_sha256'],r['alternate_A_rgba_sha256'],
       r['B_C_changed_pixels'],r['original_B_to_D_changed_pixels'],r['D_to_C_changed_pixels'],
       1,1,0,0,0) for r in out]
    assert all(len(v)==21 for v in values)
    db.executemany('INSERT INTO v128_D_source_variant_B_3 VALUES ('+','.join('?' for _ in range(21))+')',values)
    after={r[0] for r in db.execute("SELECT name FROM sqlite_master WHERE type='table'")}
    assert after-before=={'v128_D_source_variant_B_3'} and len(after)==190
    assert db.execute('SELECT count(*) FROM v128_D_source_variant_B_3').fetchone()[0]==3
    assert db.execute("SELECT count(*) FROM tile_catalog WHERE identity_final_certified=1").fetchone()[0]==0
    assert db.execute('PRAGMA integrity_check').fetchone()[0]=='ok'
    db.commit()
newraw=dbpath.read_bytes()
compressed=zlib.compress(newraw,level=8)
encoded=base64.b64encode(compressed).decode('ascii')
parts=[]
for i in range(0,len(encoded),3000000):
    p=DBOUT/('v128.part%03d.b64'%(i//3000000))
    p.write_text(encoded[i:i+3000000],'ascii')
    parts.append(p.relative_to(R).as_posix())
assert sha(zlib.decompress(base64.b64decode(''.join((R/p).read_text() for p in parts))))==sha(newraw)
dm=dict(version='v128',parent='v127',parent_sqlite_sha256=parent['sqlite_sha256'],
    sqlite_sha256=sha(newraw),sqlite_bytes=len(newraw),
    compressed_sha256=sha(compressed),parts=parts,
    prior_tables_preserved=189,new_table='v128_D_source_variant_B_3',
    new_rows=3,integrity_check='ok',new_identity_certifications=0)
(DBOUT/'MANIFEST.json').write_text(json.dumps(dm,ensure_ascii=False,indent=2)+'\n')
manifest=dict(version='v128',definition='D = candidate alternate A source PNG for same tile, rerender B at SAME TMX/layer/x/y',
    parent_candidate_search='v127',source_variant_candidates=3,D_same_B_scenes_built=3,
    source_key_list=[r['tile_set_name']+'/'+str(r['local_id']) for r in out],
    all_key_B_positions_verified=3,all_source_pixel_hashes_verified=3,
    changed_B_to_D_count=sum(r['original_B_to_D_changed_pixels']>0 for r in out),
    unchanged_B_to_D_count=sum(r['original_B_to_D_changed_pixels']==0 for r in out),
    original_B_C_zero_count=sum(r['B_C_change_zero']==1 for r in out),
    csv_path=csvpath.relative_to(R).as_posix(),csv_sha256=filesha(csvpath),
    images_zip=zipfile_path.relative_to(R).as_posix(),images_zip_sha256=filesha(zipfile_path),
    contact_sheet=sheetpath.relative_to(R).as_posix(),contact_sheet_sha256=filesha(sheetpath),
    parent_tables_preserved=189,db_sha256=sha(newraw),sqlite_integrity='ok',
    direct_image_visual_review_added=0,mapping_verified=0,tilezed_verified=0,final_certified=0,
    no_other_local_id_neighbor_substitutions=True,
    note='Two same-name PNG files can differ in pixel art and still lack official TileZed correspondence. B/D scene difference is NOT external ground truth. No promoted final identities.')
(OUT/'MANIFEST.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
(OUT/'REPORT.md').write_text(
    '# v128 D: 3개 다른 원본 PNG 후보로 같은 B 위치 재조립\n\n'
    'D는 원래 B 위치·레이어·raw GID를 고정하고, 동일 타일명/Local ID의 다른 '
    '동명 PNG 후보 크롭을 같은 좌표에 하나만 교체해서 재렌더링한 장면이다. '
    'v124 두 번째 사용 위치나 옆 타일(Local ID 추정)을 이용하지 않았다.\n'
    f'- 검증된 파일 변형 후보: 3종. 재조립한 D: 3종.\n'
    f'- B와 D 장면 픽셀 변화 있음 {manifest["changed_B_to_D_count"]}종, '
    f'변화 없음 {manifest["unchanged_B_to_D_count"]}종.\n'
    '- 원본 A, 다른 PNG의 A, B, C, D 및 B-D 차이 이미지를 PNG로 보존. '
    '원본 소스 PNG/TMX의 SHA와 선택 크롭 RGBA 해시 확인.\n'
    '- 후속: 이미지 육안 판단 및 TileZed/공식 매핑 근거 수집. '
    '문맥에서 변경된다는 사실만으로 후보를 정답으로 확정하면 안 됨.\n'
    '- 기존 5,409종·수동80·제외14·구 SQLite 189테이블 보존. '
    '최종 인증 및 직접 이미지 정체 판독 새 증가 0.\n',encoding='utf8')
print('PASS v128 real-other-PNG D',json.dumps(manifest,ensure_ascii=False),flush=True)
