#!/usr/bin/env python3
"""v195 A-first independent audit of the second early batch v133 (32)
and first 36 v134 indices incl four historically excluded.
This is a visual second opinion, NEVER a new observation/certification.
All original PNG/TMX and prior 253 SQLite tables are immutable.
"""
from pathlib import Path
from collections import Counter
from io import BytesIO
from functools import lru_cache
import base64,bisect,csv,hashlib,json,math,re,sqlite3,zlib,zipfile
import xml.etree.ElementTree as ET
from PIL import Image,ImageDraw,ImageFont
R=Path(__file__).resolve().parents[1]
O=R/'review/v195_A_first_independent_reaudit'
S=O/'A_ONLY_SHEETS';S.mkdir(parents=True,exist_ok=True)
D=R/'analysis/current/v195';D.mkdir(parents=True,exist_ok=True)
def sha(b):return hashlib.sha256(b).hexdigest()
def filehash(p):
 h=hashlib.sha256()
 with p.open('rb') as f:
  for c in iter(lambda:f.read(8*1024*1024),b''):h.update(c)
 return h.hexdigest()
def csvrows(path):
 with path.open(encoding='utf-8-sig',newline='') as f:return list(csv.DictReader(f))
@lru_cache(maxsize=24)
def atlas(path):
 with Image.open(R/path) as im:return im.convert('RGBA')
@lru_cache(maxsize=50)
def tmx(name):
 p=R/'B4220.3_MapExport_256/tmx'/name
 root=ET.parse(p).getroot();layers=list(root.iter('layer'))
 sets=sorted((int(x.get('firstgid')),x.get('name')) for x in root.findall('tileset'))
 return root,layers,sets,filehash(p)
def box(s):
 b=tuple(int(x) for x in re.findall(r'\d+',s))
 assert len(b)==4 and b[0]<b[2] and b[1]<b[3]
 return b
notes=json.loads((O/'MANUAL_A_ONLY_SECOND_OPINION_68.json').read_text(encoding='utf-8'))
assert notes['version']=='v195' and len(notes['notes'])==68
assert len(notes['actual_A_contact_sheets_directly_viewed'])==8
assert notes['mapping_verified']==notes['tilezed_verified']==notes['certified']==0
assert sorted(int(x) for x in notes['notes'] if 180<=int(x)<=215)==list(range(180,216))
old133=csvrows(R/'review/v133_visual32/VISUAL_REVIEW_32.csv')
old134=csvrows(R/'review/v134_visual_180_319/VISUAL_REVIEW.csv')
rep=csvrows(R/'review/v119_selected_A_new4633/REPRESENTATIVE_A_4633.csv')
assert len(old133)==32 and len(rep)==4633
r133={int(x['source_index']):x for x in old133}
r134={int(x['index']):x for x in old134}
assert set(r133)=={int(i) for i in notes['notes'] if int(i)>=360}
assert len(set(range(180,216))&set(r134))==32
assert {190,197,198,210}.isdisjoint(r134)
for rel in ['review/v133_visual32/ABC_D_32_PROOF.zip','review/v134_visual_180_319/ABC_EVIDENCE_VERIFIED.zip']:
 with zipfile.ZipFile(R/rel) as z:assert z.testzip() is None and len(z.namelist())>64
print('source B/C image ZIP CRC OK',flush=True)
for rel in notes['actual_A_contact_sheets_directly_viewed']:
 assert (R/rel).is_file()
n133=json.loads((R/'review/v133_visual32/MANIFEST.json').read_text())
n134=json.loads((R/'review/v134_visual_180_319/MANIFEST.json').read_text())
for p in ['ABC_D_32_PROOF.zip']:
 assert filehash(R/'review/v133_visual32'/p)==n133['files_sha256'][p]
for p in ['ABC_EVIDENCE_VERIFIED.zip']:
 assert filehash(R/'review/v134_visual_180_319'/p)==n134['files_sha256'][p]
for n in range(4):
 fn='sheets/visual_%02d.jpg'%n
 assert filehash(R/'review/v133_visual32'/fn)==n133['files_sha256'][fn]
 fn='sheets/proof_%02d.jpg'%n
 assert filehash(R/'review/v134_visual_180_319'/fn)==n134['files_sha256'][fn]
records=[];images={}
for key,audit in sorted(notes['notes'].items(),key=lambda kv:int(kv[0])):
 idx=int(key);s=rep[idx]
 assert idx in r133 or 180<=idx<=215
 assert s['selection_status']=='selected_provisional'
 path=s['source_image_path']
 assert path.startswith('Tiles/') and '..' not in path
 assert filehash(R/path)==s['source_png_sha256'],('sourcePNG_SHA',idx)
 im=atlas(path)
 crop=box(s['selected_crop_xyxy'])
 orig=im.crop(crop)
 assert sha(orig.tobytes())==s['selected_rgba_pixel_sha256'],('pixel_A_SHA',idx)
 assert orig.getchannel('A').getbbox() is not None
 old=r133.get(idx) if idx in r133 else r134.get(idx)
 verified_tmx=0;bc_pixels=None;old_candidate='';scene='';gid=None;level=None;lyr=None;x=None;y=None
 if old is not None:
  fields=('source_index','source_png','png_sha256','A_crop','A_rgba_sha256','tmx_file','tmx_sha256','B_C_pixel_change','identity_candidate','raw_gid','level','layer_index') if idx in r133 else ('index','A_png','A_png_sha256','A_crop_xyxy','A_rgba_pixel_sha256','B_tmx_file','B_tmx_sha256','B_C_changed_pixels','provisional_identity','raw_gid','level','layer_index')
  _,sp,hp,cr,hc,tm,hs,bc,candidate,raw_gid,zindex,layerindex=fields
  assert old[sp]==path and old[hp]==s['source_png_sha256']
  assert box(old[cr])==crop and old[hc]==s['selected_rgba_pixel_sha256']
  root,layers,sets,th=tmx(old[tm])
  assert th==old[hs],('original_TMX_sha',idx)
  li=int(old[layerindex]);x=int(old['x']);y=int(old['y'])
  assert 0<=li<len(layers) and 0<=x<int(root.get('width')) and 0<=y<int(root.get('height'))
  lyr=li;layer=layers[li]
  assert layer.find('data').get('encoding')=='csv'
  cells=[int(v) for v in re.findall(r'\d+',layer.find('data').text or '')]
  gid=cells[y*int(root.get('width'))+x]
  assert gid==int(old[raw_gid])
  base=gid&0x0fffffff
  j=bisect.bisect_right([v[0] for v in sets],base)-1
  assert j>=0 and (sets[j][1],base-sets[j][0])==(s['tile_set_name'],int(s['local_id']))
  level=int(zindex and old[zindex]);assert int(layer.get('level','0'))==level
  bc_pixels=int(old[bc]);assert bc_pixels>=0
  old_candidate=old[candidate];verified_tmx=1;scene=old[tm]
 else:
  assert idx in (190,197,198,210)
 assert audit['A_visual_reviewed'] and audit['B_C_as_secondary_only']
 assert audit['audit_flag'] in ['A_supported','BC_context_overreach','A_ambiguous','prior_excluded','A_contradiction']
 records.append(dict(source_index=idx,tile_set_name=s['tile_set_name'],local_id=int(s['local_id']),
  old_version='v133' if idx in r133 else 'v134',previous_candidate=old_candidate,
  independent_original_A_shape=audit['revised_A_only_description'],
  audit_flag=audit['audit_flag'],specific_reason=audit['reason'],
  wiki_term_only=audit['pzwiki_reference_term_only'] or '',
  A_png=path,A_png_sha256=s['source_png_sha256'],A_RGBA_sha256=s['selected_rgba_pixel_sha256'],
  A_crop=s['selected_crop_xyxy'],source_GID_TMX_verified=verified_tmx,
  original_tmx=scene,level=level,layer_index=lyr,x=x,y=y,raw_gid=gid,
  original_B_C_changed_pixels=bc_pixels,prior_exclusion_preserved=int(audit['audit_flag']=='prior_excluded'),
  certified=0,mapping_verified=0,tilezed_verified=0,independent_A_visual_review=1,
  review_caution='PZwiki automatically generated 42.0.0 movable-name guide only; NOT official B42.20 or sprite/local ID proof. B/C contextual use secondary.'))
 images[idx]=(orig,im,crop)
assert len(records)==68
assert sum(x['source_GID_TMX_verified'] for x in records)==64
assert sum(x['prior_exclusion_preserved'] for x in records)==4
counter=Counter(r['audit_flag'] for r in records)
assert counter=={'A_supported':58,'BC_context_overreach':2,'A_ambiguous':3,'prior_excluded':4,'A_contradiction':1}
with (O/'A_FIRST_REAUDIT_68.csv').open('w',encoding='utf-8-sig',newline='') as f:
 w=csv.DictWriter(f,fieldnames=list(records[0]));w.writeheader();w.writerows(records)
# Image-based proof sheet: unmodified source PNG sprite + neighbor atlas grid (not a correct local ID claim).
try:font=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',14)
except:font=ImageFont.load_default()
def checker(w,h):
 a=Image.new('RGBA',(w,h),(240,240,240,255));draw=ImageDraw.Draw(a)
 for yy in range(0,h,20):
  for xx in range(0,w,20):
   if (yy//20+xx//20)%2:draw.rectangle((xx,yy,xx+19,yy+19),fill=(207,215,222,255))
 return a
for page in range(math.ceil(len(records)/8)):
 sheet=Image.new('RGB',(1200,4*296),(245,248,251));d=ImageDraw.Draw(sheet)
 for n,r in enumerate(records[page*8:page*8+8]):
  yy=(n//2)*296;xx=(n%2)*600
  d.rectangle((xx+1,yy+1,xx+598,yy+294),outline=(140,158,175),width=2)
  head=f"{r['source_index']:04d} {r['tile_set_name']}/{r['local_id']} | {r['audit_flag']}"
  d.text((xx+9,yy+8),head,fill=(30,55,82),font=font)
  im,atlas_im,crop=images[r['source_index']]
  canvas=checker(185,244)
  a=im.copy();a.thumbnail((180,240),Image.Resampling.LANCZOS)
  canvas.alpha_composite(a,((185-a.width)//2,(244-a.height)//2))
  sheet.paste(canvas.convert('RGB'),(xx+8,yy+38))
  # Neighbors are only atlas adjacency, not verified same object's parts.
  bw,bh=im.size
  left=max(0,crop[0]-128);top=max(0,crop[1]-256)
  right=min(atlas_im.width,crop[2]+128);bottom=min(atlas_im.height,crop[3]+256)
  context=atlas_im.crop((left,top,right,bottom))
  context.thumbnail((375,234),Image.Resampling.LANCZOS)
  canvas=checker(378,244);canvas.alpha_composite(context,((378-context.width)//2,(244-context.height)//2))
  sheet.paste(canvas.convert('RGB'),(xx+207,yy+38))
  d.text((xx+10,yy+283),"A ORIGINAL",font=font,fill=(50,65,95))
  d.text((xx+209,yy+283),"ATLAS NEIGHBORS - UNVERIFIED",font=font,fill=(86,72,55))
 p=S/f'A_FIRST_AUDIT_{page:02}.jpg';sheet.save(p,quality=88,optimize=True)
parent=json.loads((R/'analysis/current/v192/MANIFEST.json').read_text())
assert parent['table_count']==253 and parent['version']=='v192'
compressed=base64.b64decode(''.join((R/p).read_text('ascii').strip() for p in parent['parts']))
assert sha(compressed)==parent['compressed_sha256']
raw=zlib.decompress(compressed);assert len(raw)==parent['sqlite_bytes'] and sha(raw)==parent['sqlite_sha256']
tmp=Path('/tmp/pz-v195-A-first-audit.sqlite');tmp.write_bytes(raw)
db=sqlite3.connect(tmp)
assert db.execute('PRAGMA integrity_check').fetchone()[0]=='ok'
tables={x[0]:db.execute('SELECT count(*) FROM "'+x[0]+'"').fetchone()[0] for x in db.execute("SELECT name FROM sqlite_master WHERE type='table'")}
assert len(tables)==253
cols=list(records[0]);intcols={'source_index','local_id','source_GID_TMX_verified','level','layer_index','x','y','raw_gid','original_B_C_changed_pixels','prior_exclusion_preserved','certified','mapping_verified','tilezed_verified','independent_A_visual_review'}
db.execute('CREATE TABLE v195_A_first_second_opinion ('+','.join('"'+k+'" '+('INTEGER' if k in intcols else 'TEXT') for k in cols)+',PRIMARY KEY(tile_set_name,local_id),CHECK(certified=0 AND mapping_verified=0 AND tilezed_verified=0))')
db.executemany('INSERT INTO v195_A_first_second_opinion ('+','.join('"'+x+'"' for x in cols)+') VALUES ('+','.join('?' for _ in cols)+')', [tuple(r[k] for k in cols) for r in records])
db.commit()
after={x[0]:db.execute('SELECT count(*) FROM "'+x[0]+'"').fetchone()[0] for x in db.execute("SELECT name FROM sqlite_master WHERE type='table'")}
assert len(after)==254 and set(after)-set(tables)=={'v195_A_first_second_opinion'} and all(after[k]==v for k,v in tables.items())
assert db.execute('PRAGMA integrity_check').fetchone()[0]=='ok';db.close()
newraw=tmp.read_bytes();packed=zlib.compress(newraw,8);enc=base64.b64encode(packed).decode('ascii')
parts=[]
for offset in range(0,len(enc),3000000):
 p=D/f'v195.part{offset//3000000:03}.b64';p.write_text(enc[offset:offset+3000000],encoding='ascii');parts.append(p.relative_to(R).as_posix())
assert sha(zlib.decompress(base64.b64decode(''.join((R/p).read_text('ascii') for p in parts))))==sha(newraw)
dbm=dict(version='v195',parent='v192',parent_sqlite_sha256=parent['sqlite_sha256'],
 sqlite_sha256=sha(newraw),compressed_sha256=sha(packed),sqlite_bytes=len(newraw),parts=parts,
 table_count=254,previous_tables_preserved=253,audit_entries=68,new_observed_rows=0,certified=0,
 official_mapping_verified=0,tilezed_verified=0,integrity_check='ok')
(D/'MANIFEST.json').write_text(json.dumps(dbm,ensure_ascii=False,indent=2)+'\n')
summary=dict(version='v195',parent_checkpoint='v192',starting_batch='second added v133',prior_v194_A_audit='review/v194_Afirst_second160_319',
 A_images_individually_reinspected=68,v133=32,v134_first_indices_including_excluded=36,
 png_file_and_A_RGBA_sha_reverified=68,original_TMX_GID_reverified=64,
 archive_BC_CRC_and_SHA_verified=True,official_mapping_verified=0,certified=0,tilezed_verified=0,
 wiki_source='https://pzwiki.net/wiki/PZwiki:Tile_list',wiki_date='2024-12-20',wiki_build='42.0.0',
 wiki_role='movables_EN/script names used only as possible family names; no automatic local ID mapping',
 audit_flags=dict(counter),parent_sqlite_tables_preserved=253,sqlite_tables=254,
 sqlite_sha256=sha(newraw),
 review_csv_sha256=filehash(O/'A_FIRST_REAUDIT_68.csv'),
 original_A_sheets=[p.relative_to(R).as_posix() for p in sorted(S.glob('A_FIRST_AUDIT_*.jpg'))],
 image_observation_progress_unchanged='10007/10042',
 official_identity_certification_unchanged=0,
 next_unchecked_scope='v134 indices216-319 and later v135-v192: require individual original A visual second opinion in subsequent batches',
 evidence_note='Legacy A and TMX hashes were correctly linked but do not prove semantic correctness. Prior errors flagged without overriding originals.')
(O/'MANIFEST.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2)+'\n')
(O/'README.md').write_text(
 '# v195 — 두 번째 추가 배치부터 원본 A 중심 독립 재감사\n\n'
 '**A 실제 재열람**: v133 32종 전부 + v134 초반 180-215의 36종(옛 제외4 포함), 총68종. '
 '원본 타일 A PNG 바이트 SHA256 및 RGBA 픽셀 SHA256 재검증, 대표 출처 TMX64종 raw GID/좌표·층·레이어·firstgid 점검. '
 '8장 원본 A/B/C 증거 시트를 다시 직접 보고 A 단독 형태/전체 장면 효과를 분리해 기록.\n'
 '**의미 과잉판정**: camping_01/52는 장작 더미의 윗판이라는 정확한 역할이 A 자체로 입증되지 않음. '
 'camping_02/76 등 거친 털/짚 재질 조각에 천·깔개를 단정했던 기록은 원본 A 근거 부족. '
 'camping_03/16은 돌 원형 둘레+나무 걸이 구조로, 기존 화덕 기능은 근거 미흡. 화덕 확정 대신 우물형 장치 가능성 검토.\n'
 'Wiki는 B42.0.0에서 Moveables_EN/스크립트명 두 목록으로 생성된 보조 자료이므로 정확한 TileZed 스프라이트 Local ID 인증 증거가 아님.\n'
 '과거 결과 및 사용자 수동검수/제외 기록 전부 그대로 두고 별도 감사 테이블 68행 추가. '
 '원래 누적 관찰 10007/10042와 최종 인증0 및 대상 33종 사용자 검수 패키지는 불변. '
 'v134 후반·v135 이후 전체는 아직 이 신규 독립 A 재열람이 끝난 상태가 아님.\n',encoding='utf-8')
print('PASS v195',json.dumps(summary,ensure_ascii=False),flush=True)
