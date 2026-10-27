#!/usr/bin/env python3
"""v133: direct A/B/C/D image review, strictly provisional, v132 DB immutable."""
from pathlib import Path
import csv,json,hashlib,zlib,base64,sqlite3,zipfile,io,re,xml.etree.ElementTree as ET
from PIL import Image,ImageDraw,ImageFont
R=Path(__file__).resolve().parents[1]
OUT=R/'review/v133_visual32';OUT.mkdir(parents=True,exist_ok=True)
DB=R/'analysis/current/v133';DB.mkdir(parents=True,exist_ok=True)
NOTES={"360":{"features":"금속 원통형 통과 어두운 윗면","candidate":"회색 금속 통","part":"저장 통 본체","material":"금속","confidence":"medium"},"361":{"features":"상부가 열린 듯한 청회색 원통","candidate":"열린 금속 통","part":"저장 통 본체","material":"금속","confidence":"low"},"362":{"features":"둥근 회색 덮개와 세로벽이 보이는 통","candidate":"회색 금속 통","part":"원통 본체","material":"금속","confidence":"medium"},"365":{"features":"높은 목판과 평평한 작업면","candidate":"목재 작업대","part":"세로 지지판·상판","material":"목재","confidence":"medium"},"366":{"features":"검은 도구가 설치된 갈색 작업대","candidate":"도구 부착 목재 작업대","part":"작업면·도구 지지부","material":"목재/금속","confidence":"medium"},"367":{"features":"낮은 목재 상판과 짧은 다리","candidate":"목재 벤치 또는 평상","part":"상판·다리","material":"목재","confidence":"low"},"368":{"features":"비스듬한 판재와 하부 다리","candidate":"낮은 목재 받침","part":"상판·지지부","material":"목재","confidence":"low"},"369":{"features":"갈색 판자와 사선 받침","candidate":"작은 목재 작업대","part":"상판·다리","material":"목재","confidence":"low"},"370":{"features":"평평한 목재 판과 짧은 다리","candidate":"낮은 목재 받침","part":"상판·다리","material":"목재","confidence":"low"},"371":{"features":"회색 네모 테두리와 오목한 내부","candidate":"사각 수조 또는 그릇","part":"벽면·내부","material":"회색 가공재","confidence":"medium"},"372":{"features":"나무 상판과 가는 네 다리","candidate":"작은 나무 탁자","part":"상판·다리","material":"목재","confidence":"medium"},"373":{"features":"두께 있는 짧은 나무 판자","candidate":"목재 판재 부품","part":"상판 조각","material":"목재","confidence":"low"},"374":{"features":"평평한 판재와 어두운 하부면","candidate":"목재 판재 부품","part":"연결판","material":"목재","confidence":"low"},"375":{"features":"가장자리가 꺾인 짧은 갈색 판","candidate":"목재 상단 부품","part":"판재 조각","material":"목재","confidence":"low"},"376":{"features":"작은 직사각 목재 널판","candidate":"목재 상판 부품","part":"상판","material":"목재","confidence":"low"},"379":{"features":"오목한 목재 상자형 조각","candidate":"낮은 목재 상자 또는 받침","part":"짧은 받침","material":"목재","confidence":"low"},"380":{"features":"네모 목판과 가는 다리","candidate":"소형 목재 탁자","part":"상판·다리","material":"목재","confidence":"medium"},"383":{"features":"나무 지주와 짧은 가로대가 교차","candidate":"십자형 목재 지주","part":"수직·가로 지지대","material":"목재","confidence":"medium"},"384":{"features":"목판 여러 장과 낮은 다리","candidate":"거친 목재 작업대","part":"상판·다리","material":"목재","confidence":"medium"},"385":{"features":"세로 지주가 장착된 짧은 목재 받침","candidate":"목재 지지 프레임","part":"수직 지주","material":"목재","confidence":"low"},"386":{"features":"세로 목재와 사선 버팀대","candidate":"삼각 목재 지지틀","part":"경사 버팀대","material":"목재","confidence":"medium"},"387":{"features":"높은 목재 지주와 돌출 팔 및 줄","candidate":"목재 인양 지지대 후보","part":"지주·팔·매달림 부품","material":"목재/끈","confidence":"low"},"389":{"features":"검은 원통과 위로 구부러진 연통","candidate":"금속 화덕 또는 난로","part":"본체·연통","material":"금속","confidence":"medium"},"390":{"features":"둥근 어두운 상단을 가진 갈색 통","candidate":"갈색 드럼통","part":"용기 몸체","material":"금속","confidence":"medium"},"391":{"features":"높은 갈색 판자벽과 틈이 있는 문짝, 세로로 긴 목재 수납 구조","candidate":"좁고 높은 목재 보관장","part":"문짝·수직 판재","material":"목재","confidence":"medium"},"392":{"features":"뚜껑이 덮인 회색 네모 상자","candidate":"회색 보관 상자","part":"상자 본체","material":"재질 미확정","confidence":"medium"},"393":{"features":"뚜껑과 측면이 보이는 사각 상자","candidate":"회색 상자 또는 궤","part":"뚜껑·측면","material":"재질 미확정","confidence":"medium"},"394":{"features":"아주 작은 갈색 원통 용기","candidate":"작은 통 또는 컵","part":"소형 용기","material":"재질 미확정","confidence":"low"},"395":{"features":"녹이 슨 갈색 통과 검은 윗면","candidate":"녹슨 드럼통","part":"금속 몸체","material":"금속","confidence":"medium"},"396":{"features":"녹슨 원통형 금속 저장 용기","candidate":"녹슨 금속 통","part":"용기 몸체","material":"금속","confidence":"medium"},"398":{"features":"작은 갈색 원통형 용기","candidate":"소형 통/양동이","part":"용기 몸체","material":"재질 미확정","confidence":"low"},"399":{"features":"비스듬한 목재 막대가 교차한 지지틀","candidate":"목재 사선 지지 프레임","part":"대각 버팀대","material":"목재","confidence":"low"}}
def sha(b):return hashlib.sha256(b).hexdigest()
def digest(p):return sha(p.read_bytes())
def readcsv(p):
 with p.open(encoding='utf-8-sig',newline='') as f:return list(csv.DictReader(f))
def loadpic(raw):return Image.open(io.BytesIO(raw)).convert('RGB')
A=readcsv(R/'review/v119_selected_A_new4633/REPRESENTATIVE_A_4633.csv')
B=readcsv(R/'review/v120_B_context_new4632/B_CONTEXT_4632.csv')
C=readcsv(R/'review/v121_C_diff_new4632/C_B_DIFFERENCE_4632.csv')
D=readcsv(R/'review/v126_D_alt_A_B_160/D_ALTERNATIVE_A_B_160.csv')
OLD={(q['tile_set_locator'],int(q['local_id'])) for q in readcsv(R/'analysis/imports/merged_catalog_5409.csv')}
assert len(A)==4633 and len(B)==len(C)==4632 and len(D)==160 and len(OLD)==5409
assert len(NOTES)==32
parent=json.loads((R/'analysis/current/v132/MANIFEST.json').read_text())
packed=base64.b64decode(''.join((R/p).read_text('ascii').strip() for p in parent['parts']),validate=True)
assert sha(packed)==parent['compressed_sha256']
oldraw=zlib.decompress(packed)
assert sha(oldraw)==parent['sqlite_sha256'] and len(oldraw)==parent['sqlite_bytes']
f=Path('/tmp/v133_additive.sqlite');f.write_bytes(oldraw)
with sqlite3.connect(f) as cn:
 assert cn.execute('PRAGMA integrity_check').fetchone()[0]=='ok'
 counts={name:cn.execute('SELECT count(*) FROM "'+name+'"').fetchone()[0] for (name,) in cn.execute("SELECT name FROM sqlite_master WHERE type='table'")}
 assert len(counts)==194
 previous={(k,int(i)) for k,i in cn.execute('SELECT tile_set_name,local_id FROM v132_visual3_jumbo20')}
 assert len(previous)==23
 T={}
 def verify_map(b):
  name=b['tmx_file'];src=R/'B4220.3_MapExport_256/tmx'/name
  assert digest(src)==b['tmx_sha256']
  if name not in T:
   root=ET.parse(src).getroot()
   ts=sorted((int(t.get('firstgid')),t.get('name')) for t in root.findall('tileset') if t.get('name'))
   T[name]=(root,list(root.iter('layer')),ts)
  root,layers,ts=T[name]
  layer=layers[int(b['source_layer_index'])]
  w,h=int(root.get('width')),int(root.get('height'))
  x,y=int(b['source_x']),int(b['source_y'])
  assert 0<=x<w and 0<=y<h
  data=layer.find('data'); assert data.get('encoding')=='csv'
  cells=[int(v) for v in re.findall(r'\d+',data.text or '')]
  assert len(cells)==w*h and cells[y*w+x]==int(b['source_raw_gid'])
  gid=int(b['source_raw_gid'])&0x0fffffff
  first,name1=max((z for z in ts if z[0]<=gid))
  assert (name1,gid-first)==(b['tile_set_name'],int(b['local_id']))
  lv=layer.get('level')
  if lv is None:
   p=layer.find("properties/property[@name='level']")
   lv=(p.get('value') or p.text or '0') if p is not None else '0'
  assert int(lv)==int(b['source_level'])
  return first
 def loadchecked(p,entry,h):
  with zipfile.ZipFile(p) as z:
   assert z.testzip() is None
   data=z.read(entry)
  assert sha(data)==h
  return loadpic(data)
 fields=['source_index','tile_set_name','local_id','status','observed','visual_features','identity_candidate','part_role','material','direction','connection','confidence',
 'source_png','png_sha256','A_crop','A_rgba_sha256','tmx_file','tmx_sha256','level','layer_index','x','y','raw_gid','firstgid',
 'B_sha','C_sha','DIFF_sha','B_C_pixel_change','D_archive_entry','D_is_neighbor_experiment','mapping_verified','tilezed_verified','certified','source_note']
 output=[]
 zpath=R/'review/v126_D_alt_A_B_160/D_ALT_A_B_SCENES_160.zip'
 with zipfile.ZipFile(zpath) as z:
  assert z.testzip() is None
  dn=set(z.namelist())
 unique=set();zout=zipfile.ZipFile(OUT/'ABC_D_32_PROOF.zip','w',compression=zipfile.ZIP_DEFLATED,compresslevel=5)
 ss=OUT/'sheets';ss.mkdir(exist_ok=True)
 font=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',13)
 for count,index in enumerate(sorted(map(int,NOTES))):
  assert 360<=index<=399
  a,b,c,d=A[index],B[index],C[index],D[index-320]
  key=(a['tile_set_name'],int(a['local_id']))
  assert all((r['tile_set_name'],int(r['local_id']))==key for r in (b,c,d))
  assert key not in OLD and key not in previous and key not in unique
  unique.add(key)
  assert a['selection_status']=='selected_provisional'
  assert int(c['B_minus_C_changed_pixels'])>0 and c['B_minus_C_nonzero']=='1'
  assert b['neighbor_tiles_skipped']=='0' and b['scene_truncated_at_map_edge']=='0'
  assert c['removed_exactly_one_raw_gid']=='1'
  assert d['correspondence_verified']==d['tilezed_verified']==d['identity_certified']=='0'
  assert a['source_image_path']==d['original_png']
  first=verify_map(b)
  png=R/a['source_image_path'];assert digest(png)==a['source_png_sha256']
  bounds=tuple(map(int,a['selected_crop_xyxy'].split(',')))
  with Image.open(png) as img:
   im=img.convert('RGBA')
   assert 0<=bounds[0]<bounds[2]<=im.width and 0<=bounds[1]<bounds[3]<=im.height
   orig=im.crop(bounds)
  assert sha(orig.tobytes())==a['selected_rgba_pixel_sha256']==d['original_rgba_sha256']
  Bi=loadchecked(R/'review/v120_B_context_new4632'/b['B_zip_shard'],b['B_zip_entry'],b['B_webp_file_sha256'])
  Ci=loadchecked(R/'review/v121_C_diff_new4632'/c['C_zip_shard'],c['C_zip_entry'],c['C_webp_file_sha256'])
  DEL=loadchecked(R/'review/v121_C_diff_new4632'/c['DIFF_zip_shard'],c['DIFF_zip_entry'],c['DIFF_png_file_sha256'])
  assert Bi.size==Ci.size==DEL.size==(800,580)
  dn1=f'DaltB/{index:04}_DaltB.webp'
  assert dn1 in dn and d['alternate_status']=='alternative_A_hypothesis_rendered'
  with zipfile.ZipFile(zpath) as z: Di=loadpic(z.read(dn1))
  assert Di.size==(800,580)
  item=NOTES[str(index)]
  output.append(dict(source_index=index,tile_set_name=key[0],local_id=key[1],status='provisional_candidate',observed=1,
   visual_features=item['features'],identity_candidate=item['candidate'],part_role=item['part'],material=item['material'],
   direction='unverified',connection='unverified',confidence=item['confidence'],source_png=a['source_image_path'],
   png_sha256=a['source_png_sha256'],A_crop=a['selected_crop_xyxy'],A_rgba_sha256=sha(orig.tobytes()),
   tmx_file=b['tmx_file'],tmx_sha256=b['tmx_sha256'],level=b['source_level'],layer_index=b['source_layer_index'],
   x=b['source_x'],y=b['source_y'],raw_gid=b['source_raw_gid'],firstgid=first,
   B_sha=b['B_webp_file_sha256'],C_sha=c['C_webp_file_sha256'],DIFF_sha=c['DIFF_png_file_sha256'],
   B_C_pixel_change=int(c['B_minus_C_changed_pixels']),D_archive_entry=dn1,D_is_neighbor_experiment=1,
   mapping_verified=0,tilezed_verified=0,certified=0,source_note='Visual A/B/C plus original PNG pixel and exact TMX placement confirmed; D alternative is a different-neighbor Local ID risk and does not prove identity.'))
  imgs=[('ORIGINAL_A',orig),('B_TMX',Bi),('C_REMOVED',Ci),('B_C_DELTA',DEL),('D_UNVERIFIED',Di)]
  if count%8==0:
   board=Image.new('RGB',(1810,2400),'#ebf0f6')
   draw=ImageDraw.Draw(board)
  y=(count%8)*300
  draw.rectangle((4,y+3,1805,y+296),fill='white',outline='#879aaf',width=2)
  draw.text((10,y+12),f'{index} {key[0]}/{key[1]}    local id/mapping NOT CERTIFIED',font=font,fill='#233c56')
  for ix,(label,src) in enumerate(imgs):
   x=ix*362
   draw.text((x+9,y+33),label,font=font,fill='#2b4862')
   vv=src.copy();vv.thumbnail((345,230))
   if vv.mode=='RGBA':board.paste(vv,(x+(360-vv.width)//2,y+58+(234-vv.height)//2),vv)
   else:board.paste(vv,(x+(360-vv.width)//2,y+58+(234-vv.height)//2))
   stream=io.BytesIO();src.save(stream,format='PNG')
   zout.writestr(f'{index:05}/{label}.png',stream.getvalue())
  if count%8==7 or count==31:board.save(ss/f'visual_{count//8:02}.jpg',quality=89,optimize=True)
 zout.close()
 with (OUT/'VISUAL_REVIEW_32.csv').open('w',encoding='utf-8-sig',newline='') as fcsv:
  w=csv.DictWriter(fcsv,fieldnames=fields);w.writeheader();w.writerows(output)
 assert len(output)==32 and len(unique)==32
 schema=','.join('"'+name+'" '+('INTEGER' if name in ('source_index','local_id','observed','level','layer_index','x','y','raw_gid','firstgid','B_C_pixel_change','D_is_neighbor_experiment','mapping_verified','tilezed_verified','certified') else 'TEXT') for name in fields)
 cn.execute(f'CREATE TABLE v133_visual_review_32 ({schema},PRIMARY KEY(tile_set_name,local_id),CHECK(mapping_verified=0 AND tilezed_verified=0 AND certified=0))')
 cn.executemany('INSERT INTO v133_visual_review_32 VALUES ('+','.join('?' for _ in fields)+')',[[r[p] for p in fields] for r in output])
 cn.commit()
 after={name:cn.execute('SELECT count(*) FROM "'+name+'"').fetchone()[0] for (name,) in cn.execute("SELECT name FROM sqlite_master WHERE type='table'")}
 assert len(after)==195 and after['v133_visual_review_32']==32
 assert all(after[k]==v for k,v in counts.items())
 assert cn.execute('PRAGMA integrity_check').fetchone()[0]=='ok'
raw=f.read_bytes();zipped=zlib.compress(raw,8)
encode=base64.b64encode(zipped).decode('ascii')
parts=[]
for i in range(0,len(encode),3000000):
 p=DB/f'v133.part{i//3000000:03}.b64';p.write_text(encode[i:i+3000000],encoding='ascii');parts.append(p.relative_to(R).as_posix())
assert sha(zlib.decompress(base64.b64decode(''.join((R/p).read_text('ascii') for p in parts))))==sha(raw)
dbm=dict(version='v133',parent='v132',parent_sqlite_sha256=parent['sqlite_sha256'],sqlite_sha256=sha(raw),compressed_sha256=sha(zipped),
 sqlite_bytes=len(raw),parts=parts,prior_tables_preserved=194,table_count=195,new_table='v133_visual_review_32',new_rows=32,integrity_check='ok',
 mapping_verified=0,tilezed_verified=0,certified=0)
(DB/'MANIFEST.json').write_text(json.dumps(dbm,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
files=[OUT/'VISUAL_REVIEW_32.csv',OUT/'ABC_D_32_PROOF.zip',*sorted(ss.glob('*.jpg'))]
with zipfile.ZipFile(OUT/'ABC_D_32_PROOF.zip') as z:assert z.testzip() is None and len(z.namelist())==160
audit=dict(version='v133',source_index_range=[360,399],processed=32,deferred_not_held=[363,377,378,381,382,388,391,397],
 original_A_pixel_TMX_position_verified=32,original_B_C_image_hashes_verified=32,D_experimental_image_inspected=32,
 observed_provisional=32,certified=0,mapping_verified=0,tilezed_verified=0,source_parent_sha=parent['sqlite_sha256'],
 sqlite_sha256=sha(raw),files_sha256={p.relative_to(OUT).as_posix():digest(p) for p in files})
(OUT/'MANIFEST.json').write_text(json.dumps(audit,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
(OUT/'README.md').write_text('# v133 new visual observations 32\n\nDirect visual inspection of 32 source A/B/C/D groups within new-index 360..399. Eight other cases (including boundary and ambiguous pixels) are not newly classified. A and B/C images are source-hash checked, exact TMX level/layer/x/y/raw GID verified. D is an adjacent-image candidate that may belong to a different Local ID; no authoritative TileZed mapping or final object certification. Previous user-held and historical records are preserved. New SQLite = v132 194 tables plus one 32-row table (195 tables), integrity_check ok.\n',encoding='utf8')
print('PASS v133 visual32, append-only sqlite',sha(raw),flush=True)
