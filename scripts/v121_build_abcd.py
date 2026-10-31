#!/usr/bin/env python3
"""v121: reproducible A/B/C/D evidence for 160 new keys from v120.
New 4,633 pool only. Historical v116 database, 5,409 old keys, and manual
review records remain intact. These are machine-generated scenes, NOT AI review.
"""
from pathlib import Path
from collections import Counter,defaultdict
from functools import lru_cache
import bisect,csv,hashlib,html,io,json,re,sqlite3,subprocess,sys,xml.etree.ElementTree as ET,zipfile,base64,zlib
from PIL import Image,ImageDraw,ImageFont,ImageChops
R=Path(__file__).resolve().parents[1]
O=R/'review/v121_ABCD_first160'
O.mkdir(exist_ok=True,parents=True)
TMX=R/'B4220.3_MapExport_256/tmx'
def records(p):
    with p.open(encoding='utf-8-sig',newline='') as f:return list(csv.DictReader(f))
def sha(b):return hashlib.sha256(b).hexdigest()
def filesha(p):return sha(p.read_bytes())
def cropbox(s):
    a=[int(x) for x in s.strip().strip('[]').split(',')]
    assert len(a)==4 and a[2]>a[0] and a[3]>a[1]
    return tuple(a)
all_a=records(R/'review/v119_selected_A_new4633/REPRESENTATIVE_A_4633.csv')
good_a={(r['tile_set_name'],int(r['local_id'])):r for r in all_a if r['selection_status']=='selected_provisional'}
assert len(good_a)==4632
old=records(R/'analysis/imports/merged_catalog_5409.csv')
oldkeys={(r['tile_set_locator'],int(r['local_id'])) for r in old}
assert len(oldkeys)==5409 and not set(good_a)&oldkeys
fallback={(r['tile_set_name'],int(r['local_id'])):r for r in records(R/'review/v117_A_candidates_10042/A_CANDIDATE_COMBINED_10042.csv')}
v120=records(R/'review/v120_B_context_new4632/B_CONTEXT_4632.csv')
assert len(v120)==4632
selected=v120[:160]
assert len(selected)==160
selectedkeys={(r['tile_set_name'],int(r['local_id'])) for r in selected}
assert len(selectedkeys)==160 and not selectedkeys&oldkeys
v120meta=json.loads((R/'review/v120_B_context_new4632/MANIFEST.json').read_text())
assert filesha(R/'review/v120_B_context_new4632/B_CONTEXT_4632.csv')==v120meta['metadata_sha256']
names=[f'{x}_{y}.tmx' for x in range(26,38) for y in range(43,50)]
assert len(names)==84
def layer_level(ly):
    if 'level' in ly.attrib:return int(ly.get('level','0'))
    p=ly.find("properties/property[@name='level']")
    return int((p.get('value') or p.text or '0') if p is not None else '0')
def load_map(name):
    root=ET.parse(TMX/name).getroot()
    ts=sorted((int(z.get('firstgid')),z.get('name')) for z in root.findall('tileset') if z.get('name'))
    firsts=[t[0] for t in ts]
    assert firsts
    w=int(root.get('width','256'));h=int(root.get('height','256'))
    layers=[]
    for i,ly in enumerate(root.iter('layer')):
        d=ly.find('data')
        assert d is not None and d.get('encoding')=='csv'
        vals=[int(s) for s in re.findall(r'\d+',d.text or '')]
        assert len(vals)==w*h
        layers.append(dict(index=i,name=ly.get('name',''),level=layer_level(ly),values=vals))
    return dict(ts=ts,firsts=firsts,w=w,h=h,layers=layers)
def key_for(m,raw):
    raw=raw&0x0fffffff
    if not raw:return None
    i=bisect.bisect_right(m['firsts'],raw)-1
    if i<0:return None
    first,name=m['ts'][i]
    return name,raw-first
@lru_cache(maxsize=3)
def atlas(rel):
    with Image.open(R/rel) as im:return im.convert('RGBA')
@lru_cache(maxsize=1600)
def tile(k):
    a=good_a.get(k)
    if a:
        rel=a['source_image_path']
        bbox=cropbox(a['selected_crop_xyxy'])
        expect=a['selected_rgba_pixel_sha256']
    else:
        a=fallback.get(k)
        if a is None:return None,'not_in_a_ledger'
        rel=a.get('source_png_path','')
        choice=a.get('new_preferred_A','')
        if choice=='A3':bbox=cropbox(a['A3_crop_bbox']);expect=a['A3_pixel_sha256']
        elif choice in ('A1','A1=A2'):bbox=cropbox(a['A1_bbox']);expect=a['A1_pixel_sha256']
        elif choice=='A2':bbox=cropbox(a['A2_bbox']);expect=a['A2_pixel_sha256']
        else:return None,'no_provisional_A'
    if not rel or not expect:return None,'missing_source'
    src=atlas(rel)
    if bbox[0]<0 or bbox[1]<0 or bbox[2]>src.width or bbox[3]>src.height:
        return None,'bbox_outside'
    im=src.crop(bbox)
    assert sha(im.tobytes())==expect,(k,'RGBA source drift')
    return (im,'v119' if k in good_a else 'v117') if im.getbbox() else (None,'empty_crop')
def flip(im,raw):
    if raw&0x20000000:im=im.transpose(Image.Transpose.TRANSPOSE)
    if raw&0x80000000:im=im.transpose(Image.Transpose.FLIP_LEFT_RIGHT)
    if raw&0x40000000:im=im.transpose(Image.Transpose.FLIP_TOP_BOTTOM)
    return im
W,H=800,580
def scene(m,loc,remove=False):
    x0,y0,lv=int(loc['x']),int(loc['y']),int(loc['level'])
    target=(int(loc['layer_index']),y0*m['w']+x0,int(loc['raw_gid']))
    image=Image.new('RGBA',(W,H),(237,242,247,255))
    misses=Counter();drawn=0;deleted=0
    for layer in m['layers']:
        if layer['level']!=lv:continue
        q=[]
        for dy in range(-2,3):
            y=y0+dy
            if not 0<=y<m['h']:continue
            for dx in range(-2,3):
                x=x0+dx
                if not 0<=x<m['w']:continue
                p=y*m['w']+x;raw=layer['values'][p]
                if raw:q.append((dx+dy,dy,dx,p,raw))
        q.sort()
        for _,dy,dx,p,raw in q:
            if remove and (layer['index'],p,raw)==target:
                deleted+=1;continue
            key=key_for(m,raw)
            if key is None:misses['bad_gid']+=1;continue
            t,provenance=tile(key)
            if t is None:misses[provenance]+=1;continue
            t=flip(t,raw)
            px=int(W/2+(dx-dy)*58-t.width/2)
            py=int(H/2+(dx+dy)*29+34-t.height)
            if px<0 or py<0 or px+t.width>W or py+t.height>H:
                cl=(max(0,-px),max(0,-py),min(t.width,W-px),min(t.height,H-py))
                if cl[2]<=cl[0] or cl[3]<=cl[1]:misses['out_of_canvas']+=1;continue
                t=t.crop(cl);px=max(0,px);py=max(0,py)
            image.alpha_composite(t,(px,py));drawn+=1
    if remove:assert deleted==1,(loc,deleted)
    return image.convert('RGB'),dict(misses),drawn
font=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',11)
small=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',10)
targets={}
for i,r in enumerate(selected):
    k=(r['tile_set_name'],int(r['local_id']))
    targets[k]=dict(tmx=r['tmx_file'],level=int(r['source_level']),layer_index=int(r['source_layer_index']),x=int(r['source_x']),y=int(r['source_y']),raw_gid=int(r['source_raw_gid']))
# D second occurrence: genuinely separate TMX tile placement; never synthetic.
alternatives={}
for j,name in enumerate(names):
    assert filesha(TMX/name)==v120meta['source_TMX_sha256'][name],name
    m=load_map(name)
    for ly in m['layers']:
        for p,raw in enumerate(ly['values']):
            if not raw:continue
            k=key_for(m,raw)
            if k not in targets:continue
            orig=targets[k]
            if name==orig['tmx'] and ly['index']==orig['layer_index'] and p==orig['y']*m['w']+orig['x']:continue
            loc=dict(tmx=name,level=ly['level'],layer_index=ly['index'],x=p%m['w'],y=p//m['w'],raw_gid=raw)
            bounded=2<=loc['x']<m['w']-2 and 2<=loc['y']<m['h']-2
            prev=alternatives.get(k)
            if prev is None or (not prev['bounded'] and bounded):
                loc['bounded']=bounded;alternatives[k]=loc
    if (j+1)%14==0:print('SCANNED alternative placement',j+1,'/84',len(alternatives),flush=True)
# All 4 image types available in HTML; A original crop, B existing original WebP, C newly
# rendered removal, D alternate occurrence or explicit no-D (NOT a fabricated scene).
zip_path=O/'ABCD_160_evidence.zip'
zf=zipfile.ZipFile(zip_path,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=4)
out=[];cards=[];sheets=[];mapcache_name=None;mapcache=None
rgba_src_sha={}
bzip=zipfile.ZipFile(R/'review/v120_B_context_new4632/b_png_shards/B_5x5_00.zip')
for i,row in enumerate(selected):
    k=(row['tile_set_name'],int(row['local_id']))
    loc=targets[k]
    if mapcache_name!=loc['tmx']:
        mapcache=load_map(loc['tmx']);mapcache_name=loc['tmx']
        tile.cache_clear();atlas.cache_clear()
    bfull,missing_b,n_b=scene(mapcache,loc)
    cfull,missing_c,n_c=scene(mapcache,loc,True)
    assert missing_b==missing_c or (sum(missing_b.values())>=sum(missing_c.values()))
    actual_old=bzip.read(row['B_zip_entry'])
    assert sha(actual_old)==row['B_webp_file_sha256']
    oldpix=Image.open(io.BytesIO(actual_old)).convert('RGB')
    # B regeneration must be perceptually compatible with v120 lossy WebP.
    assert oldpix.size==bfull.size
    diff=ImageChops.difference(bfull,cfull)
    changed=sum(1 for q in diff.convert('L').getdata() if q!=0)
    a,source=tile(k)
    assert a is not None and source=='v119'
    a_buf=io.BytesIO();a.save(a_buf,'PNG');a_data=a_buf.getvalue()
    dloc=alternatives.get(k)
    if dloc:
        dm=mapcache if dloc['tmx']==mapcache_name else load_map(dloc['tmx'])
        dfull,missing_d,n_d=scene(dm,dloc)
    else:dfull=None;missing_d={};n_d=0
    panels=[('A',a),('B',bfull),('C',cfull),('D',dfull)]
    dataurls={}
    for code,im in panels:
        if im is None:continue
        buf=io.BytesIO()
        if code=='A':raw=a_data;mime='image/png';ext='png'
        else:
            im.save(buf,format='WEBP',quality=85,method=3)
            raw=buf.getvalue();mime='image/webp';ext='webp'
        entry=f'{code}/{i:04d}_{code}.{ext}'
        zf.writestr(entry,raw);dataurls[code]='data:'+mime+';base64,'+base64.b64encode(raw).decode()
    summary=f"{i:03d} {k[0]} / {k[1]} | {loc['tmx']} L{loc['level']} ({loc['x']},{loc['y']}) | B-C changed={changed} | D={'yes' if dloc else 'no'}"
    cards.append((summary,dataurls))
    rec=dict(index=i,tile_set_name=k[0],local_id=k[1],tmx_file=loc['tmx'],
      level=loc['level'],layer_index=loc['layer_index'],x=loc['x'],y=loc['y'],
      raw_gid=loc['raw_gid'],tmx_sha256=v120meta['source_TMX_sha256'][loc['tmx']],
      a_png_sha256=good_a[k]['source_png_sha256'],a_rgba_pixel_sha256=sha(a.tobytes()),
      b_prior_webp_sha256=row['B_webp_file_sha256'],
      b_c_changed_pixels=changed,b_c_same_pixels=int(changed==0),
      neighbor_missing_B_json=json.dumps(missing_b,sort_keys=True),
      neighbor_missing_C_json=json.dumps(missing_c,sort_keys=True),
      b_drawn=n_b,c_drawn=n_c,target_removed_exactly_one=1,
      d_status='actual_second_placement' if dloc else 'not_found_in_84_maps',
      d_tmx=dloc['tmx'] if dloc else '',d_level=dloc['level'] if dloc else '',
      d_layer_index=dloc['layer_index'] if dloc else '',d_x=dloc['x'] if dloc else '',
      d_y=dloc['y'] if dloc else '',d_raw_gid=dloc['raw_gid'] if dloc else '',
      d_neighbor_missing_json=json.dumps(missing_d,sort_keys=True),
      identity_candidate='',part_role='',observed_features='',
      confidence='not_reviewed',review_status='evidence_generated_not_yet_visually_reviewed',
      mapping_verified=0,tilezed_verified=0,final_certified=0,
      stage_note='A provisional PNG source; B prior approximate; C exact target placement removed; D genuine second map occurrence only')
    assert rec['a_rgba_pixel_sha256']==good_a[k]['selected_rgba_pixel_sha256']
    out.append(rec)
    if i%40==0:board=Image.new('RGB',(1920,2900),(246,249,251))
    dr=ImageDraw.Draw(board)
    slot=i%40;xx=(slot%4)*480;yy=(slot//4)*290
    dr.rectangle((xx+1,yy+1,xx+477,yy+287),outline=(138,153,171),fill=(255,255,255))
    dr.text((xx+8,yy+8),summary[:74],font=small,fill=(28,46,61))
    for j,(code,im) in enumerate(panels):
        cx=xx+7+j*118
        dr.text((cx+5,yy+28),code,font=font,fill=(44,72,92))
        if im is not None:
            thumb=im.copy();thumb.thumbnail((115,225))
            board.paste(thumb,(cx+(115-thumb.width)//2,yy+51+(224-thumb.height)//2))
        else:dr.text((cx+6,yy+110),'NO SECOND',font=small,fill=(154,42,42))
    dr.text((xx+8,yy+269),f'Delta pixels: {changed} / {W*H}',font=small,fill=(62,70,87))
    if i%40==39:
        sheet=O/f'ABCD_sheet_{i//40:02d}.jpg';board.save(sheet,quality=85,optimize=True);sheets.append(sheet)
    if (i+1)%40==0:print('RENDERED ABCD',i+1,'of 160',flush=True)
bzip.close();zf.close()
assert len(out)==160 and len(cards)==160 and len(sheets)==4
fields=list(out[0])
with (O/'ABCD_160.csv').open('w',encoding='utf-8-sig',newline='') as f:
    w=csv.DictWriter(f,fieldnames=fields);w.writeheader();w.writerows(out)
h=['<!doctype html><html lang="ko"><head><meta charset="utf-8"><title>v121 B42 A/B/C/D evidence</title>',
'<style>body{font:14px system-ui;background:#e9edf2;margin:20px;color:#192939}section{background:white;border:1px solid #c5d2dc;margin:8px;padding:12px;border-radius:8px}img{width:24.5%;height:265px;object-fit:contain;background:#f0f3f5}h3{margin:0 0 9px}small{color:#617489}</style></head><body>',
'<h1>v121: 160 new tile A / B / C / D evidence</h1><p>A provisional raw sprite; B same-floor 5×5; C removal of exactly one source-layer placement; D separate real 84-map placement, if available. Pixel comparison uses uncompressed B/C, not lossy WebP. No model review, no TileZed certification.</p>']
for caption,dataurls in cards:
    h.append('<section><h3>'+html.escape(caption)+'</h3>')
    for code in ('A','B','C','D'):
        if code in dataurls:h.append('<img loading="lazy" alt="'+code+'" src="'+dataurls[code]+'">')
        else:h.append('<span style="display:inline-block;width:24%">D absent in 84 TMX</span>')
    h.append('</section>')
h.append('</body></html>')
(O/'ABCD_160_embedded.html').write_text(''.join(h),encoding='utf-8')
# Restore full v116 physical DB; append new evidence table without changing a historic row.
db=R/'analysis/current/v121'
db.mkdir(parents=True,exist_ok=True)
temp=Path('/tmp/pz_v121_full.sqlite')
subprocess.run([sys.executable,str(R/'scripts/restore_unified_v116.py'),str(temp)],check=True)
with sqlite3.connect(temp) as c:
    before={x[0] for x in c.execute("SELECT name FROM sqlite_master WHERE type='table'")}
    assert 'v121_abcd_evidence' not in before
    c.execute('CREATE TABLE v121_abcd_evidence (tile_set_name TEXT NOT NULL,local_id INTEGER NOT NULL,source_tmx TEXT,source_level INTEGER,source_x INTEGER,source_y INTEGER,source_raw_gid INTEGER,b_c_changed_pixels INTEGER,d_status TEXT,ai_review_status TEXT,identity_candidate TEXT,confidence TEXT,mapping_verified INTEGER DEFAULT 0,tilezed_verified INTEGER DEFAULT 0,final_certified INTEGER DEFAULT 0,PRIMARY KEY(tile_set_name,local_id))')
    c.executemany('INSERT INTO v121_abcd_evidence VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)',[
      (x['tile_set_name'],x['local_id'],x['tmx_file'],x['level'],x['x'],x['y'],x['raw_gid'],x['b_c_changed_pixels'],x['d_status'],x['review_status'],x['identity_candidate'],x['confidence'],0,0,0) for x in out])
    assert c.execute('SELECT count(*) FROM v121_abcd_evidence').fetchone()[0]==160
    assert c.execute('SELECT count(*) FROM tile_catalog WHERE observed_any=1').fetchone()[0]==5400
    assert c.execute('SELECT count(*) FROM v115_ai_candidate_queue').fetchone()[0]==882
    assert c.execute('SELECT count(*) FROM tile_catalog WHERE identity_final_certified=1').fetchone()[0]==0
    assert before<={x[0] for x in c.execute("SELECT name FROM sqlite_master WHERE type='table'")}
    assert c.execute('PRAGMA integrity_check').fetchone()[0]=='ok'
sqlite_bytes=temp.read_bytes()
dbhash=sha(sqlite_bytes)
compressed=zlib.compress(sqlite_bytes,level=8)
encoded=base64.b64encode(compressed).decode()
partpaths=[]
for i in range(0,len(encoded),3000000):
    path=db/f'v121.part{i//3000000:03}.b64'
    path.write_text(encoded[i:i+3000000],encoding='ascii')
    partpaths.append(path.relative_to(R).as_posix())
dbm=dict(version='v121',parent='v116',sqlite_bytes=len(sqlite_bytes),sqlite_sha256=dbhash,compressed_sha256=sha(compressed),parts=partpaths,
            v116_tables_preserved=len(before),v121_abcd_evidence=160,old_catalog=5409,old_observed=5400,old_auditable_candidates=4512,prior_v115_additional_candidates=882,identity_certified=0)
(db/'MANIFEST.json').write_text(json.dumps(dbm,ensure_ascii=False,indent=2)+'\n')
# Self-check restored exact zip, table rows and SQL integrity.
packed=base64.b64decode(''.join((R/p).read_text('ascii') for p in partpaths))
assert sha(packed)==sha(compressed)
assert sha(zlib.decompress(packed))==dbhash
with zipfile.ZipFile(zip_path) as z:
    assert z.testzip() is None and len(z.namelist())==160*3+sum(x['d_status']=='actual_second_placement' for x in out)
m=dict(version='v121',parent_visual='v120',physical_db_parent='v116',new_keys_for_abcd=160,
       image_generated=160,ai_individually_observed=0,provisional_identity_candidate=0,
       held_due_to_unreviewed=160,cumulative_5409_observed=5400,
       old_5409_unobserved=9,expanded_10042_new_pending=4633,
       actual_d_second_placements=sum(x['d_status']=='actual_second_placement' for x in out),
       bc_zero_delta=sum(x['b_c_same_pixels'] for x in out),
       evidence_csv_sha256=filesha(O/'ABCD_160.csv'),
       evidence_zip_sha256=filesha(zip_path),html_sha256=filesha(O/'ABCD_160_embedded.html'),
       review_sheet_sha256={x.name:filesha(x) for x in sheets},
       sqlite_sha256=dbhash,sqlite_integrity='ok',zip_crc='ok',mapping_verified=0,tilezed_verified=0,final_certified=0,
       limitation='Images generated programmatically, NOT all individually visually interpreted yet. B/C approximate and original A Local ID unverified.')
(O/'MANIFEST.json').write_text(json.dumps(m,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print('PASS V121',json.dumps(m,ensure_ascii=False),flush=True)
