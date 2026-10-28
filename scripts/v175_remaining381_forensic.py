#!/usr/bin/env python3
"""v175 source-first census of every remaining tile. NO observed/identity promotion.

Does not infer opacity or identity from B-C=0. Counts alternate true TMX GID
placements, validates original selected source and produces an evidence ledger.
"""
from pathlib import Path
from collections import Counter,defaultdict
from functools import lru_cache
import bisect,base64,csv,hashlib,io,json,re,sqlite3,xml.etree.ElementTree as ET,zlib,zipfile
from PIL import Image,ImageDraw,ImageFont
R=Path(__file__).resolve().parents[1]
OUT=R/'review/v175_remaining381_evidence_audit';OUT.mkdir(parents=True,exist_ok=True)
DBOUT=R/'analysis/current/v175';DBOUT.mkdir(parents=True,exist_ok=True)
SHEETS=OUT/'sheets';SHEETS.mkdir(exist_ok=True)
def sha(b):return hashlib.sha256(b).hexdigest()
def filesha(p):
 h=hashlib.sha256()
 with p.open('rb') as f:
  for x in iter(lambda:f.read(8*1024*1024),b''):h.update(x)
 return h.hexdigest()
def readcsv(path):
 with path.open(encoding='utf-8-sig',newline='') as f:return list(csv.DictReader(f))
def bbox(s):
 a=tuple(int(x.strip()) for x in s.strip('[]').split(','))
 assert len(a)==4 and 0<=a[0]<a[2] and 0<=a[1]<a[3]
 return a
parent=json.loads((R/'analysis/current/v174/MANIFEST.json').read_text())
packed=base64.b64decode(''.join((R/p).read_text('ascii').strip() for p in parent['parts']),validate=True)
assert sha(packed)==parent['compressed_sha256']
raw=zlib.decompress(packed)
assert sha(raw)==parent['sqlite_sha256'] and len(raw)==parent['sqlite_bytes']
tmp=Path('/tmp/pz_v175_remaining.sqlite');tmp.write_bytes(raw)
db=sqlite3.connect(tmp)
assert db.execute('PRAGMA integrity_check').fetchone()[0]=='ok'
before={name:db.execute('SELECT count(*) FROM "'+name+'"').fetchone()[0] for (name,) in db.execute("SELECT name FROM sqlite_master WHERE type='table'")}
assert len(before)==236 and before['v174_visual_review']==49
all_prior=set()
for table in ['v132_visual3_jumbo20','v133_visual_review_32']+['v%d_visual_review'%i for i in range(134,175)]:
 all_prior.update((r[0],int(r[1])) for r in db.execute('SELECT tile_set_name,local_id FROM "'+table+'"'))
assert len(all_prior)==4101,('prior_visual',len(all_prior))
for table in ('v122_ai_visual_review_160','v125_ai_visual_spotcheck_20'):
 rows=db.execute('SELECT tile_set_name,local_id,review_status FROM "'+table+'"')
 pre={(r[0],int(r[1])) for r in rows if r[2]=='provisional_candidate'}
 print('early visual',table,len(pre),flush=True)
 all_prior.update(pre)
assert len(all_prior)==4261,('unique_observed_new',len(all_prior))
a=readcsv(R/'review/v119_selected_A_new4633/REPRESENTATIVE_A_4633.csv')
assert len(a)==4633
missing=[]
for i,record in enumerate(a):
 key=(record['tile_set_name'],int(record['local_id']))
 if key not in all_prior:missing.append((i,key,record))
assert len(missing)==372,('new_remaining',len(missing))
oldmiss=db.execute('SELECT * FROM tile_catalog WHERE observed_any=0').fetchall()
ocol=[x[1] for x in db.execute('PRAGMA table_info(tile_catalog)')]
assert len(oldmiss)==9 and len(a)==4633
old_missing=[]
for row in oldmiss:
 d=dict(zip(ocol,row))
 key=(d.get('tile_set_locator') or d.get('tile_set_name') or d.get('tileset_name'),int(d['local_id']))
 assert key[0],d
 old_missing.append((key,d))
assert len(set(key for key,d in old_missing))==9
target={key for _,key,_ in missing}|{key for key,_ in old_missing}
assert len(target)==381 and not (target&all_prior)
print('REMAINDER VERIFIED',len(missing),'new plus',len(old_missing),'old =',len(target),flush=True)
B={(r['tile_set_name'],int(r['local_id'])):r for r in readcsv(R/'review/v120_B_context_new4632/B_CONTEXT_4632.csv')}
C={(r['tile_set_name'],int(r['local_id'])):r for r in readcsv(R/'review/v121_C_diff_new4632/C_B_DIFFERENCE_4632.csv')}
assert len(B)==len(C)==4632 and set(B)==set(C)
audit=json.loads((R/'audits/map_range_26_43_to_37_49/SUMMARY.json').read_text())
assert audit['files_present']==84 and audit['distinct_tile_keys_tile_layers']==10042
# Scan all 84 original maps, including nonselected true GID occurrences.
placement_count=Counter();interior_count=Counter();choices=defaultdict(list);map_sha={}
for ix,meta in enumerate(audit['per_map']):
 name=meta['tmx'];p=R/'B4220.3_MapExport_256/tmx'/name
 assert p.stat().st_size==meta['filesize_bytes']
 map_sha[name]=filesha(p)
 assert map_sha[name]==meta['sha256']
 root=ET.parse(p).getroot()
 w,h=int(root.get('width')),int(root.get('height'))
 ts=sorted((int(t.get('firstgid')),t.get('name')) for t in root.findall('tileset') if t.get('name'))
 firsts=[x[0] for x in ts]
 assert len(ts)==len(set(firsts))
 for layerix,ly in enumerate(root.iter('layer')):
  data=ly.find('data');assert data is not None and data.get('encoding')=='csv'
  vals=[int(v) for v in re.findall(r'\d+',data.text or '')]
  assert len(vals)==w*h,(name,layerix,len(vals),w,h)
  level=ly.get('level')
  if level is None:
   z=ly.find("properties/property[@name='level']")
   level=(z.get('value') or z.text or '0') if z is not None else '0'
  for n,g in enumerate(vals):
   gid=g&0x0fffffff
   if not gid:continue
   pos=bisect.bisect_right(firsts,gid)-1
   if pos<0:continue
   tname=ts[pos][1];lid=gid-ts[pos][0]
   key=(tname,lid)
   if key not in target:continue
   x,y=n%w,n//w
   inside=2<=x<w-2 and 2<=y<h-2
   placement_count[key]+=1
   interior_count[key]+=inside
   # Note genuine layer/level, not inferred alternate atlas identity.
   occ={'tmx':name,'layer_index':layerix,'layer':ly.get('name',''),'level':int(level),'x':x,'y':y,'raw_gid':g,'inbounds_5x5':inside}
   q=choices[key]
   if len(q)<8:q.append(occ)
   elif inside and not any(z['inbounds_5x5'] for z in q):q[-1]=occ
 if (ix+1)%12==0:print('CENSUS TMX',ix+1,'/84',flush=True)
assert len(placement_count)==381,('unplaced keys',list(target-set(placement_count))[:20])
# Independently verify representative A PNG crop pixel and original selected TMX.
@lru_cache(maxsize=8)
def png_image(p):
 with Image.open(p) as img:return img.convert('RGBA')
verified_png=0;verified_primary=0
rows=[]
for idx,key,a1 in missing:
 b=B.get(key);c=C.get(key)
 rec=dict(index=idx,origin='new_A_4633',tile_set_name=key[0],local_id=key[1],
 original_observed=0,reviewed_in_v175=1,identity_certified=0,
 source_png=a1.get('source_image_path',''),source_crop=a1.get('selected_crop_xyxy',''),
 selected_A_status=a1['selection_status'],
 original_scene_tmx=b['tmx_file'] if b else '',
 original_scene_layer=b['source_layer_index'] if b else '',
 original_scene_level=b['source_level'] if b else '',
 original_scene_x=b['source_x'] if b else '',
 original_scene_y=b['source_y'] if b else '',
 B_C_changed_pixels=c['B_minus_C_changed_pixels'] if c else '',
 B_map_edge=b['scene_truncated_at_map_edge'] if b else '',
 B_neighbor_skipped=b['neighbor_tiles_skipped'] if b else '',
 actual_occurrences_84=placement_count[key],interior_occurrences_84=interior_count[key],
 alternate_scene_candidate='',eligible_for_visual_followup=0,reason='',evidence_state='')
 if a1.get('source_image_path') and a1.get('selected_crop_xyxy') and a1.get('selected_rgba_pixel_sha256'):
  p=R/a1['source_image_path']
  assert filesha(p)==a1['source_png_sha256'],('source_png_modified',idx)
  img=png_image(p).crop(bbox(a1['selected_crop_xyxy']))
  assert sha(img.tobytes())==a1['selected_rgba_pixel_sha256'],('A_crop_mismatch',idx)
  verified_png+=1
  rec['evidence_state']='original_A_pixels_SHA256_verified'
 else:rec['evidence_state']='original_A_missing_or_selection_unresolved'
 if b and c:
  assert b['tmx_sha256']==map_sha[b['tmx_file']]
  assert int(c['removed_exactly_one_raw_gid'])==1
  # The original selected scene's raw TMX location was confirmed by the independent census;
  # retain original source file and raw GID from the original v120 evidence.
  occ=choices[key]
  primary=any(z['tmx']==b['tmx_file'] and z['layer_index']==int(b['source_layer_index']) and z['x']==int(b['source_x']) and z['y']==int(b['source_y']) and z['raw_gid']==int(b['source_raw_gid']) for z in occ)
  if not primary and placement_count[key]>8:
   # Selected occurrence may be beyond stored first 8; it is still validated by
   # the original TMX file via direct source position check below.
   root=ET.parse(R/'B4220.3_MapExport_256/tmx'/b['tmx_file']).getroot()
   ly=list(root.iter('layer'))[int(b['source_layer_index'])]
   v=[int(z) for z in re.findall(r'\d+',ly.find('data').text or '')]
   primary=v[int(b['source_y'])*int(root.get('width'))+int(b['source_x'])]==int(b['source_raw_gid'])
  assert primary,('representative_not_in_actual_TMX',idx,key)
  verified_primary+=1
  candidate=next((o for o in occ if o['inbounds_5x5'] and (o['tmx'],o['layer_index'],o['x'],o['y'])!=(b['tmx_file'],int(b['source_layer_index']),int(b['source_x']),int(b['source_y']))),None)
  if candidate:
   rec['alternate_scene_candidate']=json.dumps(candidate,ensure_ascii=False,sort_keys=True)
   rec['eligible_for_visual_followup']=1
  if int(c['B_minus_C_changed_pixels'])==0:rec['reason']='B_C_zero_original_scene'
  elif b['scene_truncated_at_map_edge']=='1':rec['reason']='original_scene_at_TMX_edge'
  elif int(b['neighbor_tiles_skipped'])>0:rec['reason']='original_scene_neighbors_missing'
  else:rec['reason']='prior_hold_or_low_evidence_requires_visual_reinspection'
 else:rec['reason']='original_B_C_representative_unavailable'
 rows.append(rec)
for key,d in old_missing:
 rec={name:'' for name in rows[0].keys()}
 rec.update(index='',origin='older_5409_unobserved',tile_set_name=key[0],local_id=key[1],
 original_observed=0,reviewed_in_v175=1,identity_certified=0,
 actual_occurrences_84=placement_count[key],interior_occurrences_84=interior_count[key],
 reason='older_catalog_unobserved_requires_source_review',
 evidence_state='old_catalog_observed_any_0',
 eligible_for_visual_followup=int(interior_count[key]>0),
 alternate_scene_candidate=json.dumps(next((x for x in choices[key] if x['inbounds_5x5']),choices[key][0]),ensure_ascii=False))
 rows.append(rec)
assert len(rows)==381 and verified_png>=370 and verified_primary>=370
# Marking a review/audit is NOT marking the actual visual identity as observed.
assert all(int(r['original_observed'])==int(r['identity_certified'])==0 for r in rows)
fieldnames=list(rows[0].keys())
with (OUT/'REMAINING_381_EVIDENCE_AUDIT.csv').open('w',encoding='utf-8-sig',newline='') as f:
 w=csv.DictWriter(f,fieldnames=fieldnames);w.writeheader();w.writerows(sorted(rows,key=lambda r:(r['origin'],str(r['index']),r['tile_set_name'])))
with (OUT/'OLD_NINE_UNOBSERVED.json').open('w',encoding='utf-8') as f:
 json.dump([{'tile_set_name':k[0],'local_id':k[1],'source_catalog_record':d} for k,d in old_missing],f,ensure_ascii=False,indent=2,default=str)
# Contact sheets of pending source A pixels for manual interpretation.
pending=[x for x in rows if x['origin']=='new_A_4633']
font=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',12)
for batch in range((len(pending)+63)//64):
 part=pending[batch*64:(batch+1)*64]
 board=Image.new('RGB',(1600,1600),(235,240,246));d=ImageDraw.Draw(board)
 for k,r in enumerate(part):
  x=(k%8)*200;y=(k//8)*200
  d.rectangle((x+1,y+1,x+198,y+198),fill=(255,255,255),outline=(175,187,201),width=1)
  d.text((x+5,y+4),f"{r['index']} {r['tile_set_name'][:23]}",font=font,fill=(29,50,70))
  d.text((x+5,y+21),f"ID {r['local_id']} / uses {r['actual_occurrences_84']}",font=font,fill=(75,95,110))
  if r['source_png'] and r['source_crop']:
   sprite=png_image(R/r['source_png']).crop(bbox(r['source_crop']))
   sprite.thumbnail((185,135))
   board.paste(sprite,(x+(200-sprite.width)//2,y+44+(135-sprite.height)//2),sprite)
  d.text((x+5,y+183),r['reason'][:27],font=font,fill=(105,50,48))
 board.save(SHEETS/f'REMAINING_A_{batch:02}.jpg',quality=83,optimize=True)
# Store all 381 forensic evidence rows in physical SQLite as a separate audit table.
fields=[('index', 'INTEGER'),('origin','TEXT'),('tile_set_name','TEXT'),('local_id','INTEGER'),('original_observed','INTEGER'),
 ('reviewed_in_v175','INTEGER'),('identity_certified','INTEGER'),('selected_A_status','TEXT'),('source_png','TEXT'),('source_crop','TEXT'),
 ('original_scene_tmx','TEXT'),('original_scene_layer','TEXT'),('original_scene_level','TEXT'),
 ('original_scene_x','TEXT'),('original_scene_y','TEXT'),('B_C_changed_pixels','TEXT'),('B_map_edge','TEXT'),
 ('B_neighbor_skipped','TEXT'),('actual_occurrences_84','INTEGER'),('interior_occurrences_84','INTEGER'),
 ('alternate_scene_candidate','TEXT'),('eligible_for_visual_followup','INTEGER'),('reason','TEXT'),('evidence_state','TEXT')]
db.execute('CREATE TABLE v175_remaining_evidence_audit ('+','.join('"'+n+'" '+typ for n,typ in fields)+', PRIMARY KEY(tile_set_name,local_id), CHECK(original_observed=0 AND identity_certified=0))')
keys=[n for n,_ in fields]
db.executemany('INSERT INTO v175_remaining_evidence_audit ('+','.join(keys)+') VALUES ('+','.join('?' for _ in keys)+')',
 [tuple(r[k] for k in keys) for r in rows])
db.commit()
after={n:db.execute('SELECT count(*) FROM "'+n+'"').fetchone()[0] for (n,) in db.execute("SELECT name FROM sqlite_master WHERE type='table'")}
assert len(after)==237 and set(after)-set(before)=={'v175_remaining_evidence_audit'}
assert all(after[n]==c for n,c in before.items())
assert after['v175_remaining_evidence_audit']==381
assert db.execute('PRAGMA integrity_check').fetchone()[0]=='ok'
db.close()
newraw=tmp.read_bytes();newpacked=zlib.compress(newraw,8)
encoded=base64.b64encode(newpacked).decode('ascii');parts=[]
for i in range(0,len(encoded),3000000):
 p=DBOUT/f'v175.part{i//3000000:03}.b64';p.write_text(encoded[i:i+3000000],encoding='ascii');parts.append(p.relative_to(R).as_posix())
assert sha(zlib.decompress(base64.b64decode(''.join((R/p).read_text('ascii') for p in parts))))==sha(newraw)
dbm=dict(version='v175',parent='v174',parent_sqlite_sha256=parent['sqlite_sha256'],sqlite_sha256=sha(newraw),
 compressed_sha256=sha(newpacked),sqlite_bytes=len(newraw),parts=parts,prior_tables_preserved=236,
 table_count=237,new_rows=381,new_observed_rows=0,integrity_check='ok',mapping_verified=0,tilezed_verified=0,certified=0)
(DBOUT/'MANIFEST.json').write_text(json.dumps(dbm,ensure_ascii=False,indent=2)+'\n')
summary=dict(version='v175',audit_type='complete_remaining_381_original_png_TMX_occurrence_census',
 total_remaining=381,new_source_missing=372,old_source_missing=9,observed_before=9661,observed_after=9661,
 remaining_after=381,original_png_pixel_verified=verified_png,original_B_TMX_placement_verified=verified_primary,
 actual_tmx_maps_checked=84,real_tmx_occurrences_total=sum(placement_count.values()),
 alternate_inbounds_candidates=sum(int(r['eligible_for_visual_followup']) for r in rows),
 reason_distribution=dict(Counter(r['reason'] for r in rows)),
 identity_certifications=0,official_mapping_verified=0,tilezed_verified=0,
 all_parent_tables_preserved=236,physical_db_table_count=237,sqlite_sha256=sha(newraw),
 audited_keys_sha256=sha(json.dumps(sorted([list(x) for x in target])).encode()),
 report_sha256=filesha(OUT/'REMAINING_381_EVIDENCE_AUDIT.csv'),
 image_sheets=[p.name for p in sorted(SHEETS.glob('*.jpg'))])
(OUT/'MANIFEST.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2)+'\n')
(OUT/'README.md').write_text(
 '# v175 남은 381종 전수 원본 증거 조사 (정체 인증·관찰 완료 추가 아님)\n\n'
 'v174 기준 9,661/10,042종 이미지 잠정 관찰, 미관찰 381종. 이전 5,409 키 중 9종(observed_any=0), 새 4,633 키 중 372종(기존 v122/125/132~174 성공후보 외)을 실제 부모 SQLite와 원본 A CSV로 정확히 구했습니다.\n\n'
 '84개 원본 TMX를 실제 GID와 tileset firstgid로 전수 스캔하고 해당 381개 키의 총 사용 횟수, 좌표/층/레이어, 가장자리 여부, 다른 5x5 가능 배치 후보를 집계합니다. 기존 B의 픽셀변화 0, 지도끝/주변누락, 기타 수동 보류 사유와 구분합니다.\n'
 '원본 A PNG 바이트 및 선택 RGBA 픽셀 해시 확인, B 원본 TMX selected GID와 실제 타일 키 일치 여부 대조; 다른 배치 후보가 있다는 사실만으로 정체 확정·관찰 완료·투명 인증하지 않습니다.\n'
 'SQLite v174의 236개 기존 테이블/모든 행 수·내용을 변경하지 않고 감사 목적 381행 별도 테이블 v175_remaining_evidence_audit 하나만 추가(237개). 관찰률 96.21%, 남은 381종 그대로.\n'
 'CSV와 원본 A 미관찰 접촉시트 6장, 실제 TMX 위치 후보, 지난 5,409 중 미관찰 9개 정체를 증거 파일로 보관. 다음 검수는 A/B/C를 실제 다른 원본 TMX 위치로 재조립하고 그 결과를 눈으로 확인해야만 승격 가능.\n',encoding='utf-8')
print('PASS v175 FULL FORENSIC',json.dumps(summary,ensure_ascii=False),flush=True)
