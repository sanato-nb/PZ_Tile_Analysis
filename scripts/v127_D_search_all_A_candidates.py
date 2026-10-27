#!/usr/bin/env python3
"""v127: Exhaustive OTHER-A candidate search for all 4,633 NEW TMX tile keys.
D means: find another A crop for SAME key to later re-render original B 5x5.
A1/A2/A3 are geometric hypotheses; adjacent grid cells are NOT the same local ID.
This stage searches/enumerates images; it does NOT render a new B or certify mappings.
"""
from pathlib import Path
from collections import Counter
from functools import lru_cache
import csv,hashlib,json,base64,zlib,sqlite3,zipfile,io
from PIL import Image,ImageDraw,ImageFont
R=Path(__file__).resolve().parents[1]
OUT=R/'review/v127_D_A_candidates_full4633'
DBDIR=R/'analysis/current/v127'
for p in (OUT,DBDIR,OUT/'previews'):p.mkdir(parents=True,exist_ok=True)
def sha(b):return hashlib.sha256(b).hexdigest()
def filehash(p):return sha(p.read_bytes())
def rows(p):
    with p.open(encoding='utf-8-sig',newline='') as f:return list(csv.DictReader(f))
def box(st):
    if not st:return None
    a=[int(x) for x in st.strip().strip('[]').split(',')]
    assert len(a)==4 and a[0]<a[2] and a[1]<a[3]
    return tuple(a)
A119=R/'review/v119_selected_A_new4633/REPRESENTATIVE_A_4633.csv'
C117=R/'review/v117_A_candidates_10042/A_CANDIDATE_COMBINED_10042.csv'
B120=R/'review/v120_B_context_new4632/B_CONTEXT_4632.csv'
a=rows(A119); c=rows(C117); b=rows(B120)
assert (len(a),len(c),len(b))==(4633,10042,4632)
man119=json.loads((R/'review/v119_selected_A_new4633/MANIFEST.json').read_text())
man120=json.loads((R/'review/v120_B_context_new4632/MANIFEST.json').read_text())
assert filehash(A119)==man119['selected_ledger_sha256']
assert filehash(B120)==man120['metadata_sha256']
m117=json.loads((R/'review/v117_A_candidates_10042/jumbo_a3/A3_SUMMARY.json').read_text())
assert filehash(C117)==m117['full_ledger_sha256']
old={(r['tile_set_locator'],int(r['local_id'])) for r in rows(R/'analysis/imports/merged_catalog_5409.csv')}
assert len(old)==5409
canon=lambda r:(r['tile_set_name'],int(r['local_id']))
candidate={canon(r):r for r in c}
newa={canon(r):r for r in a}
B={canon(r):r for r in b}
assert len(newa)==4633 and len(candidate)==10042 and len(B)==4632
assert not(old & set(newa))
missing=[r for r in a if r['selection_status']=='held_missing_source']
assert len(missing)==1 and canon(missing[0])==('overlay_graffiti_wall_02',2)
assert set(newa)-set(B)=={canon(missing[0])}
@lru_cache(maxsize=4)
def atlas(rel):
    if not rel:return None
    p=R/rel
    if not p.is_file():return None
    with Image.open(p) as image:return image.convert('RGBA')
def crop(src,rect):
    if src is None or rect is None:return None
    x,y,r,b=rect
    if not(0<=x<r<=src.width and 0<=y<b<=src.height):return None
    return src.crop(rect)
def alpha(im):
    return sum(im.getchannel('A').histogram()[1:]) if im else 0
def uniq_box(b):return ','.join(map(str,b)) if b else ''
def writecsv(path,records,cols):
    with path.open('w',encoding='utf-8-sig',newline='') as f:
        w=csv.DictWriter(f,fieldnames=cols)
        w.writeheader();w.writerows(records)
trials=[];ledger=[];scenes=[];stats=Counter();seenpng=set()
font=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',10)
zipfile_now=None;zipfile_parts=[]
current_zip_idx=-1
def zipthumb(index,img):
    global zipfile_now,current_zip_idx
    shard=index//400
    if shard!=current_zip_idx:
        if zipfile_now:zipfile_now.close()
        path=OUT/'previews'/('D_CANDIDATES_%02d.zip'%shard)
        zipfile_now=zipfile.ZipFile(path,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=4)
        zipfile_parts.append(path)
        current_zip_idx=shard
    p=io.BytesIO();img.save(p,format='PNG',compress_level=5)
    entry='%04d_candidate.png'%index
    zipfile_now.writestr(entry,p.getvalue())
    return path.relative_to(R).as_posix(),entry,sha(p.getvalue())
def thumb(img,w=115,h=108):
    bg=Image.new('RGB',(w,h),(243,245,248))
    if img:
        t=img.copy();t.thumbnail((w-8,h-8))
        bg.paste(t,((w-t.width)//2,(h-t.height)//2),t)
    return bg
for idx,row in enumerate(a):
    k=canon(row)
    prior=candidate[k]
    selected=row['selection_status']=='selected_provisional'
    rec=dict(index=idx,tile_set_name=k[0],local_id=k[1],
        source_png=row['source_image_path'],original_A=row['representative_A'],
        original_bbox=row['selected_crop_xyxy'],original_rgba_sha256=row['selected_rgba_pixel_sha256'],
        original_tmx=B[k]['tmx_file'] if k in B else '',
        original_level=B[k]['source_level'] if k in B else '',
        original_x=B[k]['source_x'] if k in B else '',
        original_y=B[k]['source_y'] if k in B else '',
        search_status='',direct_other_A_candidates=0,exact_basename_variant_candidates=0,
        adjacent_grid_probe_candidates=0,all_distinct_visible_hypotheses=0,
        renderable_preview=0,preview_class='',preview_image_sha256='',
        preview_zip='',preview_entry='',mapping_verified=0,
        tilezed_verified=0,final_certified=0,
        note='All 8 neighboring-grid cells are OTHER IDs until proven otherwise; no D image/B rerender certified.')
    if not selected:
        rec['search_status']='held_no_source_PNG'
        stats['missing_source']+=1;ledger.append(rec);continue
    src=atlas(row['source_image_path'])
    assert src is not None,k
    assert filehash(R/row['source_image_path'])==row['source_png_sha256'] if row['source_image_path'] not in seenpng else True
    seenpng.add(row['source_image_path'])
    origbox=box(row['selected_crop_xyxy']);orig=crop(src,origbox)
    assert orig is not None and alpha(orig)>0 and sha(orig.tobytes())==row['selected_rgba_pixel_sha256'],k
    seen={sha(orig.tobytes())}
    real=[];variants=[];probes=[]
    def attempt(code,kind,path,rect,relation):
        im=crop(atlas(path) if path else None,rect)
        status='no_crop_or_out_of_bounds'
        hs='';ac=0
        if im is not None:
            hs=sha(im.tobytes());ac=alpha(im)
            if ac==0:status='zero_alpha_not_transparent_certification'
            elif hs in seen:status='identical_pixel_duplicate'
            else:
                status='distinct_visible_unverified_correspondence'
                seen.add(hs)
        t=dict(index=idx,tile_set_name=k[0],local_id=k[1],candidate_id=code,
               category=kind,source_path=path,source_crop=uniq_box(rect),
               rgba_sha256=hs,alpha_pixels=ac,result=status,
               local_id_relation=relation,mapping_verified=0,tilezed_verified=0,
               final_certified=0)
        trials.append(t)
        if status=='distinct_visible_unverified_correspondence':
            data=dict(tile=im,**t)
            if kind=='same_key_A_grid':real.append(data)
            elif kind=='same_basename_atlas_variant':variants.append(data)
            else:probes.append(data)
    for typ in ('A1','A2','A3'):
        key=typ+'_bbox' if typ in ('A1','A2') else 'A3_crop_bbox'
        attempt(typ,'same_key_A_grid',row['source_image_path'],box(prior.get(key,'')),
                'same_local_id_v117_geometry_hypothesis_NOT_OFFICIAL')
    altpaths=[p.strip() for p in prior.get('other_exact_name_pngs','').split(';') if p.strip()]
    for v,altpath in enumerate(altpaths[:3]):
        alt=atlas(altpath)
        if alt is not None and src.size==alt.size:
            attempt('BASENAME_VARIANT_%s'%v,'same_basename_atlas_variant',altpath,origbox,
                    'exact_basename_other_file_variant_local_id_unverified')
        else:
            attempt('BASENAME_VARIANT_%s'%v,'same_basename_atlas_variant',altpath,None,
                    'atlas_dimensions_incompatible_no_candidate')
    sw=origbox[2]-origbox[0];sh=origbox[3]-origbox[1]
    for dx,dy in ((-1,-1),(0,-1),(1,-1),(-1,0),(1,0),(-1,1),(0,1),(1,1)):
        rect=(origbox[0]+dx*sw,origbox[1]+dy*sh,
              origbox[2]+dx*sw,origbox[3]+dy*sh)
        attempt('NEIGHBOR_%+d_%+d'%(dx,dy),'adjacent_grid_not_same_key',
                row['source_image_path'],rect,
                'different_local_id_possible_never_same_tile_verified')
    rec['direct_other_A_candidates']=len(real)
    rec['exact_basename_variant_candidates']=len(variants)
    rec['adjacent_grid_probe_candidates']=len(probes)
    rec['all_distinct_visible_hypotheses']=len(real)+len(variants)+len(probes)
    if real:rec['search_status']='other_A_geometric_hypothesis_found'
    elif variants:rec['search_status']='alternate_atlas_basename_hypothesis_found'
    elif probes:rec['search_status']='only_neighbor_grid_probes_NOT_same_key'
    else:rec['search_status']='no_distinct_visible_alternative'
    stats[rec['search_status']]+=1
    stats['direct_distinct']+=len(real)
    stats['variants_distinct']+=len(variants)
    stats['neighbor_probes']+=len(probes)
    lead=(real or variants or probes or [None])[0]
    if lead:
        rec['preview_class']=lead['category']
        rec['renderable_preview']=1
        path,entry,proof=zipthumb(idx,lead['tile'])
        rec['preview_zip']=path;rec['preview_entry']=entry;rec['preview_image_sha256']=proof
    if idx%80==0:
        sheet=Image.new('RGB',(1920,1760),(242,246,248));draw=ImageDraw.Draw(sheet)
    i=idx%80
    x=(i%8)*240;y=(i//8)*176
    draw.rectangle((x+1,y+1,x+237,y+173),fill=(255,255,255),outline=(145,161,176))
    draw.text((x+5,y+6),'%04d %s/%d'%(idx,k[0][:17],k[1]),font=font,fill=(25,42,60))
    draw.text((x+7,y+23),'SELECTED A',font=font,fill=(45,65,85))
    draw.text((x+124,y+23),'ALT (UNVERIFIED)',font=font,fill=(162,78,30))
    sheet.paste(thumb(orig),(x+3,y+42))
    if lead:sheet.paste(thumb(lead['tile']),(x+121,y+42))
    draw.text((x+5,y+155),'D:%d V:%d N:%d'%(len(real),len(variants),len(probes)),
              font=font,fill=(48,63,81))
    if idx%80==79 or idx==len(a)-1:
        f=OUT/('D_A_sheet_%02d.jpg'%(idx//80))
        sheet.save(f,quality=87,optimize=True)
        scenes.append(f)
    ledger.append(rec)
    if (idx+1)%400==0:print('SEARCHED',idx+1,'/',len(a),'direct_tiles',stats['other_A_geometric_hypothesis_found'],
                            'only_neighbor_tiles',stats['only_neighbor_grid_probes_NOT_same_key'],flush=True)
if zipfile_now:zipfile_now.close()
assert len(ledger)==4633 and len({(x['tile_set_name'],x['local_id']) for x in ledger})==4633
assert len(scenes)==58
assert len(trials)>=4632*11
for z in zipfile_parts:
    with zipfile.ZipFile(z) as ar:assert ar.testzip() is None
writecsv(OUT/'D_CANDIDATE_LEDGER_4633.csv',ledger,list(ledger[0]))
writecsv(OUT/'D_ALL_CANDIDATE_TRIALS.csv',trials,list(trials[0]))
# v126 first160 subrange is provenance only; its neighboring offsets were UNVERIFIED too.
v126m=json.loads((R/'review/v126_D_alt_A_B_160/MANIFEST.json').read_text())
assert v126m['source_v120_index_range']==[320,479]
# Physical DB append only. Prior 188 tables, no reclassification.
parent=json.loads((R/'analysis/current/v126/MANIFEST.json').read_text())
packed=base64.b64decode(''.join((R/p).read_text('ascii').strip() for p in parent['parts']),validate=True)
assert sha(packed)==parent['compressed_sha256']
raw=zlib.decompress(packed)
assert sha(raw)==parent['sqlite_sha256']
dbpath=Path('/tmp/pz_v127.sqlite');dbpath.write_bytes(raw)
with sqlite3.connect(dbpath) as db:
    before={t[0] for t in db.execute("SELECT name FROM sqlite_master WHERE type='table'")}
    assert len(before)==188 and 'v126_alt_A_B_160' in before
    assert db.execute('PRAGMA integrity_check').fetchone()[0]=='ok'
    db.execute("""CREATE TABLE v127_d_candidate_catalog_4633(
      tile_set_name TEXT NOT NULL,local_id INTEGER NOT NULL,source_index INTEGER,
      search_status TEXT,other_A_geometric_count INTEGER,alternate_atlas_count INTEGER,
      neighbor_grid_probe_count INTEGER,total_alternates INTEGER,
      representative_preview_kind TEXT,source_png TEXT,original_tmx TEXT,
      mapping_verified INTEGER DEFAULT 0,tilezed_verified INTEGER DEFAULT 0,
      final_certified INTEGER DEFAULT 0,PRIMARY KEY(tile_set_name,local_id))""")
    db.executemany('INSERT INTO v127_d_candidate_catalog_4633 VALUES ('+','.join(['?']*14)+')',
       [(r['tile_set_name'],r['local_id'],r['index'],r['search_status'],
         r['direct_other_A_candidates'],r['exact_basename_variant_candidates'],
         r['adjacent_grid_probe_candidates'],r['all_distinct_visible_hypotheses'],
         r['preview_class'],r['source_png'],r['original_tmx'],0,0,0) for r in ledger])
    after={t[0] for t in db.execute("SELECT name FROM sqlite_master WHERE type='table'")}
    assert len(after)==189 and after-before=={'v127_d_candidate_catalog_4633'}
    assert db.execute('SELECT count(*) FROM v127_d_candidate_catalog_4633').fetchone()[0]==4633
    assert db.execute('SELECT count(*) FROM tile_catalog').fetchone()[0]==5409
    assert db.execute('SELECT count(*) FROM v126_alt_A_B_160').fetchone()[0]==160
    assert db.execute('SELECT count(*) FROM v125_ai_visual_spotcheck_20').fetchone()[0]==20
    assert db.execute('SELECT count(*) FROM tile_catalog WHERE identity_final_certified=1').fetchone()[0]==0
    assert db.execute('PRAGMA integrity_check').fetchone()[0]=='ok'
    db.commit()
dbraw=dbpath.read_bytes();compressed=zlib.compress(dbraw,8)
b64=base64.b64encode(compressed).decode()
parts=[]
for i in range(0,len(b64),3000000):
    f=DBDIR/('v127.part%03d.b64'%(i//3000000))
    f.write_text(b64[i:i+3000000],'ascii')
    parts.append(f.relative_to(R).as_posix())
assert sha(zlib.decompress(base64.b64decode(''.join((R/p).read_text() for p in parts))))==sha(dbraw)
dm=dict(version='v127',parent='v126',parent_sqlite_sha256=parent['sqlite_sha256'],
        sqlite_bytes=len(dbraw),sqlite_sha256=sha(dbraw),
        compressed_sha256=sha(compressed),parts=parts,
        prior_tables_preserved=188,new_table='v127_d_candidate_catalog_4633',
        new_rows=4633,final_certified=0,integrity_check='ok')
(DBDIR/'MANIFEST.json').write_text(json.dumps(dm,ensure_ascii=False,indent=2)+'\n')
summary=dict(version='v127',definition='D = other A for SAME local ID, then later same-B-position rerender',
  new_total=4633,original_PNG_missing=1,searchable=4632,search_exhaustive_in_defined_hypotheses=True,
  direct_other_A_tile_count=sum(r['direct_other_A_candidates']>0 for r in ledger),
  variant_other_atlas_tile_count=sum(r['exact_basename_variant_candidates']>0 for r in ledger),
  grid_probe_only_tile_count=sum(r['search_status']=='only_neighbor_grid_probes_NOT_same_key' for r in ledger),
  without_any_alt_tile_count=sum(r['search_status']=='no_distinct_visible_alternative' for r in ledger),
  number_of_direct_alt_crops=stats['direct_distinct'],
  number_of_alt_variant_crops=stats['variants_distinct'],
  number_of_grid_probe_crops=stats['neighbor_probes'],
  candidate_trials=len(trials),individual_A_previews=sum(r['renderable_preview'] for r in ledger),
  image_preview_zip_shards=[dict(path=p.relative_to(R).as_posix(),
    sha256=filehash(p),entries=len(zipfile.ZipFile(p).namelist())) for p in zipfile_parts],
  contact_sheet_sha256={p.name:filehash(p) for p in scenes},
  master_csv='review/v127_D_A_candidates_full4633/D_CANDIDATE_LEDGER_4633.csv',
  master_csv_sha256=filehash(OUT/'D_CANDIDATE_LEDGER_4633.csv'),
  all_trials_csv='review/v127_D_A_candidates_full4633/D_ALL_CANDIDATE_TRIALS.csv',
  all_trials_sha256=filehash(OUT/'D_ALL_CANDIDATE_TRIALS.csv'),
  sqlite_sha256=sha(dbraw),sqlite_integrity='ok',old_tables_preserved=188,
  D_scene_B_rerendered_by_this_stage=0,visual_identity_observed_added=0,
  mapping_verified=0,tilezed_verified=0,final_certified=0,
  critical_limit='Adjacent grid crops may be completely different Local IDs. This is a geometry/pixel search only. It is NOT verified matching or a B-scene D completion.')
(OUT/'MANIFEST.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2)+'\n')
(OUT/'REPORT.md').write_text(
 '# v127 D: 다른 A 후보 전수탐색\n\n'
 'v119 신규 4,633종 전체에 대해 v117 A1/A2/A3 및 동명이형 PNG 경로와 '
 '8방향 인접 격자 크롭을 검토했다. **인접 격자 후보는 같은 Local ID로 인증하지 않는다.**\n\n'
 '후보 검색 대상 4,633종 중 PNG 미확보 1종을 보류. 원본 A 4,632종 SHA 검증. '
 '상세 현황은 MANIFEST.json과 원본 이미지/대체 크롭 및 후보 ZIP/SHA가 기록된 CSV 참조.\n'
 'v127은 후보 탐색 전수이지 4,632개 B 재조립이 아니다. 원본 5,409, 수동 검수80, '
 '사용자 제외14, 모든 구 SQLite와 PNG/TMX 변경하지 않음.\n',encoding='utf8')
print('PASS V127 FULL D OTHER A CANDIDATE SEARCH',json.dumps({k:v for k,v in summary.items()
 if k not in ['contact_sheet_sha256','image_preview_zip_shards']},ensure_ascii=False),flush=True)
