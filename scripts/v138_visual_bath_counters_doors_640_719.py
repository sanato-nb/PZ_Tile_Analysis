#!/usr/bin/env python3
"""v138: manual A/B/C image observation for indices 180..319. D never certifies mappings.

Author-reviewed source notes are stored in MANUAL_VISUAL_NOTES.json.
Every promoted visual candidate is rechecked against original PNG and exact
TMX raw-GID/level/layer/x/y, and B/C image bytes with SHA-256.
All existing v133 physical SQLite tables and records are preserved verbatim.
"""
from pathlib import Path
import csv,io,json,hashlib,zipfile,base64,zlib,sqlite3,re,xml.etree.ElementTree as ET
from PIL import Image,ImageDraw,ImageFont
R=Path(__file__).resolve().parents[1]
OUT=R/'review/v138_bath_counters_doors_640_719'; OUT.mkdir(parents=True,exist_ok=True)
DBOUT=R/'analysis/current/v138'; DBOUT.mkdir(parents=True,exist_ok=True)
SHEETS=OUT/'sheets'; SHEETS.mkdir(parents=True,exist_ok=True)
def sha(x):return hashlib.sha256(x).hexdigest()
def fh(p):return sha(p.read_bytes())
def csvrows(p):
 with p.open(encoding='utf-8-sig',newline='') as f:return list(csv.DictReader(f))
def bb(s):
 a=tuple(map(int,s.strip('[]').split(',')));assert len(a)==4 and a[0]<a[2] and a[1]<a[3];return a
meta=json.loads((OUT/'MANUAL_VISUAL_NOTES.json').read_text())
notes={int(i):x for i,x in meta['notes'].items()}
assert len(notes)==80 and set(notes)==set(range(640,720))
A=csvrows(R/'review/v119_selected_A_new4633/REPRESENTATIVE_A_4633.csv')
B=csvrows(R/'review/v120_B_context_new4632/B_CONTEXT_4632.csv')
C=csvrows(R/'review/v121_C_diff_new4632/C_B_DIFFERENCE_4632.csv')
old=csvrows(R/'analysis/imports/merged_catalog_5409.csv')
oldkeys={(x['tile_set_locator'],int(x['local_id'])) for x in old}
assert len(A)==4633 and len(B)==len(C)==4632 and len(oldkeys)==5409
parent=json.loads((R/'analysis/current/v137/MANIFEST.json').read_text())
compressed=base64.b64decode(''.join((R/p).read_text('ascii').strip() for p in parent['parts']),validate=True)
assert sha(compressed)==parent['compressed_sha256']
raw=zlib.decompress(compressed)
assert len(raw)==parent['sqlite_bytes'] and sha(raw)==parent['sqlite_sha256']
tmp=Path('/tmp/pz_v138_physical.sqlite');tmp.write_bytes(raw)
db=sqlite3.connect(tmp)
assert db.execute('PRAGMA integrity_check').fetchone()[0]=='ok'
before={name:db.execute('SELECT count(*) FROM "'+name+'"').fetchone()[0] for (name,) in db.execute("SELECT name FROM sqlite_master WHERE type='table'")}
assert len(before)==199 and before['v137_visual_review']==79
prior={(r[0],int(r[1])) for table in ['v132_visual3_jumbo20','v133_visual_review_32','v134_visual_review','v135_visual_review','v136_visual_review','v137_visual_review'] for r in db.execute('SELECT tile_set_name,local_id FROM '+table)}
assert len(prior)==400
tmxs={}
def verify_tmx(rec):
 name=rec['tmx_file'];p=R/'B4220.3_MapExport_256/tmx'/name
 assert fh(p)==rec['tmx_sha256']
 if name not in tmxs:
  root=ET.parse(p).getroot()
  tmxs[name]=(root,list(root.iter('layer')),sorted((int(q.get('firstgid')),q.get('name')) for q in root.findall('tileset') if q.get('name')))
 root,layers,firsts=tmxs[name]
 layer=layers[int(rec['source_layer_index'])]
 x,y=int(rec['source_x']),int(rec['source_y'])
 w,h=int(root.get('width')),int(root.get('height'))
 assert 0<=x<w and 0<=y<h
 cells=[int(v) for v in re.findall(r'\d+',layer.find('data').text or '')]
 assert len(cells)==w*h and cells[y*w+x]==int(rec['source_raw_gid'])
 lv=layer.get('level')
 if lv is None:
  q=layer.find("properties/property[@name='level']")
  lv=(q.get('value') or q.text or '0') if q is not None else '0'
 assert int(lv)==int(rec['source_level'])
 gid=int(rec['source_raw_gid']) & 0x0fffffff
 first,name=max((z for z in firsts if z[0]<=gid))
 assert (name,gid-first)==(rec['tile_set_name'],int(rec['local_id']))
 return first
archives={}
def source_entry(path,entry,h):
 if path not in archives:
  archives[path]=zipfile.ZipFile(path)
  assert archives[path].testzip() is None
 v=archives[path].read(entry)
 assert sha(v)==h,(str(path),entry)
 return v
font=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',12)
FIELDS=['index','tile_set_name','local_id','visual_status','visual_observed','observed_features','provisional_identity','part_role','material','orientation','connections','confidence',
 'A_png','A_png_sha256','A_crop_xyxy','A_rgba_pixel_sha256','B_tmx_file','B_tmx_sha256','level','layer_index','x','y','raw_gid','firstgid',
 'B_archive','B_entry','B_sha256','C_archive','C_entry','C_sha256','DELTA_archive','DELTA_entry','DELTA_sha256',
 'B_C_changed_pixels','D_status','D_current_definition','D_official_mapping_verified','mapping_verified','tilezed_verified','certified','review_note']
RESULT=[];SKIPS=[]
evidence=zipfile.ZipFile(OUT/'ABC_EVIDENCE_VERIFIED.zip','w',compression=zipfile.ZIP_DEFLATED,compresslevel=5)
def saveproof(n,a,b,c,d):
 buf=io.BytesIO();a.save(buf,format='PNG')
 evidence.writestr(f'{n:05d}/A_source.png',buf.getvalue())
 evidence.writestr(f'{n:05d}/B_original.webp',b)
 evidence.writestr(f'{n:05d}/C_removed.webp',c)
 evidence.writestr(f'{n:05d}/B_minus_C.png',d)
def thumbnail(image,width=290,height=195):
 im=image.copy();im.thumbnail((width,height));return im
canvas=None
for index in sorted(notes):
 a=A[index];b=B[index];c=C[index];note=notes[index]
 key=(a['tile_set_name'],int(a['local_id']))
 assert key==(b['tile_set_name'],int(b['local_id']))==(c['tile_set_name'],int(c['local_id']))
 assert key not in oldkeys and key not in prior
 assert a['selection_status']=='selected_provisional'
 why=[]
 if int(c['B_minus_C_changed_pixels'])<=0:why.append('B_C_zero_not_transparency')
 if int(b['neighbor_tiles_skipped'])>0:why.append('B_neighbor_missing')
 if b['scene_truncated_at_map_edge']=='1':why.append('B_map_edge_truncated')
 if a['source_image_path']!=a['selected_zip_entry'] and not a['source_image_path']:why.append('missing_A')
 if why:
  SKIPS.append(dict(index=index,tile_set_name=key[0],local_id=key[1],reason=';'.join(why),observed=0,certified=0));continue
 first=verify_tmx(b)
 png=R/a['source_image_path']
 assert fh(png)==a['source_png_sha256']
 with Image.open(png) as original:
  src=original.convert('RGBA')
  x0,y0,x1,y1=bb(a['selected_crop_xyxy'])
  assert 0<=x0<x1<=src.width and 0<=y0<y1<=src.height
  Aimg=src.crop((x0,y0,x1,y1))
 assert sha(Aimg.tobytes())==a['selected_rgba_pixel_sha256']
 bp='review/v120_B_context_new4632/'+b['B_zip_shard']
 cp='review/v121_C_diff_new4632/'+c['C_zip_shard']
 dp='review/v121_C_diff_new4632/'+c['DIFF_zip_shard']
 bi=source_entry(R/bp,b['B_zip_entry'],b['B_webp_file_sha256'])
 ci=source_entry(R/cp,c['C_zip_entry'],c['C_webp_file_sha256'])
 di=source_entry(R/dp,c['DIFF_zip_entry'],c['DIFF_png_file_sha256'])
 with Image.open(io.BytesIO(bi)) as im:Bimg=im.convert('RGB')
 with Image.open(io.BytesIO(ci)) as im:Cimg=im.convert('RGB')
 with Image.open(io.BytesIO(di)) as im:Delta=im.convert('RGB')
 assert Bimg.size==Cimg.size==Delta.size==(800,580)
 assert int(c['removed_exactly_one_raw_gid'])==1
 saveproof(index,Aimg,bi,ci,di)
 RESULT.append(dict(index=index,tile_set_name=key[0],local_id=key[1],visual_status='provisional_candidate',visual_observed=1,
  observed_features=note['features'],provisional_identity=note['candidate'],part_role=note['part'],material=note['material'],
  orientation='unverified',connections='unverified',confidence=note['confidence'],
  A_png=a['source_image_path'],A_png_sha256=a['source_png_sha256'],A_crop_xyxy=a['selected_crop_xyxy'],
  A_rgba_pixel_sha256=sha(Aimg.tobytes()),B_tmx_file=b['tmx_file'],B_tmx_sha256=b['tmx_sha256'],
  level=b['source_level'],layer_index=b['source_layer_index'],x=b['source_x'],y=b['source_y'],raw_gid=b['source_raw_gid'],firstgid=first,
  B_archive=bp,B_entry=b['B_zip_entry'],B_sha256=b['B_webp_file_sha256'],
  C_archive=cp,C_entry=c['C_zip_entry'],C_sha256=c['C_webp_file_sha256'],
  DELTA_archive=dp,DELTA_entry=c['DIFF_zip_entry'],DELTA_sha256=c['DIFF_png_file_sha256'],
  B_C_changed_pixels=int(c['B_minus_C_changed_pixels']),D_status='prior_D_experiment_only_not_source_of_identity',
  D_current_definition='other_A_candidate_at_exact_original_B_location',D_official_mapping_verified=0,
  mapping_verified=0,tilezed_verified=0,certified=0,
  review_note='Original A sprite and physical TMX GID verified; B, C, delta pixel files verified; identity inferred visually. Prior D experimental candidates are NOT local-ID-certified.'))
 n=len(RESULT)-1
 if n%8==0:
  canvas=Image.new('RGB',(1540,2120),'#edf2f6')
  draw=ImageDraw.Draw(canvas)
 y=(n%8)*265
 draw.rectangle((3,y+2,1538,y+263),fill='#ffffff',outline='#bac4ce',width=2)
 draw.text((12,y+10),f'{index:04d}  {key[0]}/{key[1]}  -  {note["candidate"]}  (provisional)',font=font,fill='#263b56')
 for j,(label,img) in enumerate([('A SOURCE',Aimg),('B TMX',Bimg),('C REMOVED',Cimg),('B-C PIXEL',Delta)]):
  x=j*385
  draw.text((x+6,y+31),label,font=font,fill='#465e73')
  preview=thumbnail(img,360,204)
  pos=(x+(380-preview.width)//2,y+54+(204-preview.height)//2)
  if preview.mode=='RGBA':canvas.paste(preview,pos,preview)
  else:canvas.paste(preview,pos)
 if n%8==7:canvas.save(SHEETS/f'proof_{n//8:02}.jpg',quality=87,optimize=True)
if RESULT and (len(RESULT)-1)%8!=7:canvas.save(SHEETS/f'proof_{(len(RESULT)-1)//8:02}.jpg',quality=87,optimize=True)
evidence.close()
for z in archives.values():z.close()
assert len(RESULT)+len(SKIPS)==80
assert len(RESULT)>=65,(len(RESULT),SKIPS)
assert len({(r['tile_set_name'],r['local_id']) for r in RESULT})==len(RESULT)
with (OUT/'VISUAL_REVIEW.csv').open('w',encoding='utf-8-sig',newline='') as fp:
 w=csv.DictWriter(fp,fieldnames=FIELDS);w.writeheader();w.writerows(RESULT)
with (OUT/'EXCLUDED_EXCEPTIONS.csv').open('w',encoding='utf-8-sig',newline='') as fp:
 w=csv.DictWriter(fp,fieldnames=['index','tile_set_name','local_id','reason','observed','certified']);w.writeheader();w.writerows(SKIPS)
schema=','.join('"'+n+'" '+('INTEGER' if n in ['index','local_id','visual_observed','level','layer_index','x','y','raw_gid','firstgid','B_C_changed_pixels','D_official_mapping_verified','mapping_verified','tilezed_verified','certified'] else 'TEXT') for n in FIELDS)
db.execute(f'CREATE TABLE v138_visual_review ({schema}, PRIMARY KEY(tile_set_name,local_id),CHECK(mapping_verified=0 AND tilezed_verified=0 AND certified=0))')
db.executemany('INSERT INTO v138_visual_review VALUES ('+','.join('?' for _ in FIELDS)+')',[[r[n] for n in FIELDS] for r in RESULT])
db.commit()
after={name:db.execute('SELECT count(*) FROM "'+name+'"').fetchone()[0] for (name,) in db.execute("SELECT name FROM sqlite_master WHERE type='table'")}
assert len(after)==200 and set(after)-set(before)=={'v138_visual_review'}
assert all(after[n]==v for n,v in before.items())
assert after['v138_visual_review']==len(RESULT)
assert db.execute('PRAGMA integrity_check').fetchone()[0]=='ok'
db.close()
newraw=tmp.read_bytes();newpacked=zlib.compress(newraw,8)
encoded=base64.b64encode(newpacked).decode('ascii');parts=[]
for i in range(0,len(encoded),3000000):
 p=DBOUT/f'v138.part{i//3000000:03}.b64';p.write_text(encoded[i:i+3000000],encoding='ascii');parts.append(p.relative_to(R).as_posix())
assert sha(zlib.decompress(base64.b64decode(''.join((R/p).read_text('ascii') for p in parts))))==sha(newraw)
manifest=dict(version='v138',parent='v133',parent_sqlite_sha256=parent['sqlite_sha256'],sqlite_sha256=sha(newraw),
 compressed_sha256=sha(newpacked),sqlite_bytes=len(newraw),parts=parts,prior_tables_preserved=199,table_count=200,
 new_rows=len(RESULT),skipped_rows=len(SKIPS),integrity_check='ok',mapping_verified=0,tilezed_verified=0,certified=0)
(DBOUT/'MANIFEST.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
with zipfile.ZipFile(OUT/'ABC_EVIDENCE_VERIFIED.zip') as z:
 assert z.testzip() is None
 assert len(z.namelist())==len(RESULT)*4
proofs=[OUT/'VISUAL_REVIEW.csv',OUT/'EXCLUDED_EXCEPTIONS.csv',OUT/'ABC_EVIDENCE_VERIFIED.zip',*sorted(SHEETS.glob('*.jpg'))]
review=dict(version='v138',original_scope=[640,719],manual_image_annotations=80,promoted_provisional=len(RESULT),
 excluded_unverified=len(SKIPS),excluded_indices=[r['index'] for r in SKIPS],
 original_PNG_TMX_B_C_files_verified=len(RESULT),D_current_alternative_not_used_to_certify=True,
 source_notes_sha256=fh(OUT/'MANUAL_VISUAL_NOTES.json'),
 parent_sha256=parent['sqlite_sha256'],sqlite_sha256=sha(newraw),
 mapping_verified=0,tilezed_verified=0,certified=0,
 files_sha256={p.relative_to(OUT).as_posix():fh(p) for p in proofs})
(OUT/'MANIFEST.json').write_text(json.dumps(review,ensure_ascii=False,indent=2)+'\n')
(OUT/'README.md').write_text('# v138 실제 신규 타일 A/B/C 이미지 정체 판독\n\n기존 시각 접촉시트 640~719에서 타일별 외형·역할·재질을 수동 관찰하였고, 각 결과의 원본 PNG RGBA 픽셀 해시, 실제 TMX GID·층·레이어·위치, B/C/픽셀차이 파일을 다시 검증하였다. B−C 변화 0, B 이웃 결손, 지도 경계 대상은 별도 CSV에 보류하고 신규 관찰 수치에 포함하지 않았다. 기존 D 인접격자/두 번째 배치는 현재 사용자 정의의 공식 다른 A 인증이 아니므로 정체 인증에 사용하지 않는다.\n\n모든 식별은 provisional_candidate, 정확한 타일셋 아틀라스 이미지/TileZed/최종 정체 인증 0. 증거 ZIP은 정확한 원본 A·B·C·픽셀차이 네 종류씩 수록한다. 부모 v133 195 물리 테이블과 이전 행 수는 전부 보존하고 v138 한 테이블만 덧붙여 196테이블이다. 사용자 제외/수동기록/보류와 모든 PNG/TMX 원본을 변경하지 않았다.\n',encoding='utf-8')
print('PASS v138',len(RESULT),'observed provisional;',len(SKIPS),'held exceptions; sqlite_sha',sha(newraw),flush=True)
