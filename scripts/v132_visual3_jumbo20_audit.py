#!/usr/bin/env python3
"""v132: original PNG/TMX and historic A/B/C/D pixel evidence reinspection.
Only 3 visually reviewed tile keys; 20 jumbo pixel/placement audits remain held.
All prior v131 physical SQLite tables copied unchanged. Never certify mappings.
"""
from pathlib import Path
import csv,io,json,re,hashlib,zipfile,zlib,base64,sqlite3,xml.etree.ElementTree as ET
from PIL import Image,ImageDraw,ImageFont
R=Path.cwd();O=R/'review/v132_visual3_jumbo20';O.mkdir(parents=True,exist_ok=True)
D=R/'analysis/current/v132';D.mkdir(parents=True,exist_ok=True)
def sha(b):return hashlib.sha256(b).hexdigest()
def hs(p):return sha(p.read_bytes())
def rows(p):
 with p.open(encoding='utf-8-sig',newline='') as f:return list(csv.DictReader(f))
def box(s):return tuple(int(x) for x in s.strip('[]').split(','))
def crop(p,b):
 with Image.open(R/p) as im:
  img=im.convert('RGBA');assert 0<=b[0]<b[2]<=img.width and 0<=b[1]<b[3]<=img.height
  return img.crop(b)
def tmx_verify(r):
 p=R/'B4220.3_MapExport_256/tmx'/r['source_tmx'];assert hs(p)==r['source_tmx_sha256']
 t=ET.parse(p).getroot();layers=list(t.iter('layer'))
 l=layers[int(r['source_layer_index'])];w=int(t.get('width'));x=int(r['source_x']);y=int(r['source_y'])
 vals=[int(v) for v in re.findall(r'\d+',l.find('data').text or '')]
 assert len(vals)==w*int(t.get('height')) and vals[y*w+x]==int(r['source_raw_gid'])
 lev=l.get('level')
 if lev is None:
  p=l.find("properties/property[@name='level']");lev=(p.get('value') or p.text) if p is not None else '0'
 assert int(lev)==int(r['source_level'])
 gid=int(r['source_raw_gid'])&0x0fffffff
 ts=sorted((int(q.get('firstgid')),q.get('name')) for q in t.findall('tileset') if q.get('name'))
 g=max((q for q in ts if q[0]<=gid),default=None);assert g and (g[1],gid-g[0])==(r['tile_set_name'],int(r['local_id']))
 return g[0]
v131=json.loads((R/'analysis/current/v131/MANIFEST.json').read_text())
compressed=base64.b64decode(''.join((R/p).read_text('ascii').strip() for p in v131['parts']),validate=True)
assert sha(compressed)==v131['compressed_sha256']
raw=zlib.decompress(compressed);assert sha(raw)==v131['sqlite_sha256'] and len(raw)==v131['sqlite_bytes']
a={(r['tile_set_name'],int(r['local_id'])):r for r in rows(R/'review/v119_selected_A_new4633/REPRESENTATIVE_A_4633.csv')}
b={(r['tile_set_name'],int(r['local_id'])):r for r in rows(R/'review/v120_B_context_new4632/B_CONTEXT_4632.csv')}
s=rows(R/'review/v128_D_alt_PNG_3/D_ALT_SOURCE_B_COMPARE_3.csv')
assert len(a)==4633 and len(b)==4632 and len(s)==3
old={(r['tile_set_locator'],int(r['local_id'])) for r in rows(R/'analysis/imports/merged_catalog_5409.csv')}
priorreviews={(r['tile_set_name'],int(r['local_id'])) for p in [R/'review/v122_AI_ABCD_160/AI_VISUAL_REVIEW_160.csv',R/'review/v125_AI_ABCD_20/AI_VISUAL_SPOTCHECK_20.csv'] for r in rows(p)}
assert len(old)==5409
observations={
0:('낮고 둥근 갈색·황토색 잎덩이; 주택 출입구의 화단 가까이 배치','갈색 낮은 관목 또는 생울타리 조각','low'),
1:('자주색 잎이 길고 직립한 타원형 관목; 울타리와 수거통 근처에 배치','자주색 관목','medium'),
3:('밝고 짙은 녹색 잎이 결합한 소형 관목; 나무 울타리 옆에 배치','작은 녹색 관목','medium')
}
fields=['tile_set_name','local_id','status','observed','visual_features','identity_candidate','part_role','material','direction','connection','confidence','source_png','source_pixel_sha','alternate_png','alternate_pixel_sha','source_tmx','source_tmx_sha256','source_level','source_layer_index','source_x','source_y','source_raw_gid','source_firstgid','source_crop','B_C_changed_pixels','B_D_changed_pixels','mapping_verified','tilezed_verified','certified','evidence']
out=[]; font=ImageFont.load_default();board=Image.new('RGB',(1800,990),'#f0f4f7');draw=ImageDraw.Draw(board)
with zipfile.ZipFile(R/'review/v128_D_alt_PNG_3/D_SAME_B_VARIANT_3.zip') as z:
 assert z.testzip() is None
 for i,r in enumerate(sorted(s,key=lambda x:int(x['local_id']))):
  k=(r['tile_set_name'],int(r['local_id']));assert k not in old and k not in priorreviews
  sel=a[k];assert r['original_PNG']==sel['source_image_path']
  assert hs(R/r['original_PNG'])==sel['source_png_sha256']
  original=crop(r['original_PNG'],box(r['original_crop']))
  alternate=crop(r['alternate_PNG'],box(r['alternate_crop']))
  assert sha(original.tobytes())==r['original_A_rgba_sha256']==sel['selected_rgba_pixel_sha256']
  assert sha(alternate.tobytes())==r['alternate_A_rgba_sha256']
  assert original.size==alternate.size
  first=tmx_verify(r);assert int(b[k]['source_raw_gid'])==int(r['source_raw_gid'])
  assert r['same_B_TMX_position_exact']==r['replaced_target_GID_exactly_one']=='1'
  for j,label in enumerate(['A_selected','A_alternative','B_original','C_removed','D_alt_A_at_same_B']):
   with Image.open(io.BytesIO(z.read(f'{label}/{int(r["v127_index"]):04}_{label}.png'))) as im:
    spr=im.convert('RGBA');spr.thumbnail((345,275))
   x=j*360;y=i*330;draw.text((x+8,y+8),f'{k[0]}/{k[1]}  {label}',fill='#273d4a',font=font)
   board.paste(spr,(x+(360-spr.width)//2,y+35),spr)
  features,candidate,confidence=observations[k[1]]
  out.append(dict(tile_set_name=k[0],local_id=k[1],status='provisional_candidate',observed=1,visual_features=features,identity_candidate=candidate,part_role='관목 잎·줄기 군집',material='식물성/잎',direction='unverified',connection='unverified',confidence=confidence,source_png=r['original_PNG'],source_pixel_sha=sha(original.tobytes()),alternate_png=r['alternate_PNG'],alternate_pixel_sha=sha(alternate.tobytes()),source_tmx=r['source_tmx'],source_tmx_sha256=r['source_tmx_sha256'],source_level=r['source_level'],source_layer_index=r['source_layer_index'],source_x=r['source_x'],source_y=r['source_y'],source_raw_gid=r['source_raw_gid'],source_firstgid=first,source_crop=r['original_crop'],B_C_changed_pixels=r['B_C_changed_pixels'],B_D_changed_pixels=r['original_B_to_D_changed_pixels'],mapping_verified=0,tilezed_verified=0,certified=0,evidence='original PNG physically rechecked; original TMX GID verified; prior A/B/C/D PNG visibly inspected in chat 2026-10-27'))
board.save(O/'VISUAL_3_ABCDE.jpg',quality=89,optimize=True)
jumbo=[r for r in a.values() if r['is_jumbo_geometry_guess']=='1'];assert len(jumbo)==20,len(jumbo)
held=[]
for r in jumbo:
 k=(r['tile_set_name'],int(r['local_id']));pos=b[k]
 im=crop(r['source_image_path'],box(r['selected_crop_xyxy']))
 assert hs(R/r['source_image_path'])==r['source_png_sha256']
 assert sha(im.tobytes())==r['selected_rgba_pixel_sha256']
 loc=dict(tile_set_name=k[0],local_id=k[1],source_tmx=pos['tmx_file'],source_tmx_sha256=pos['tmx_sha256'],source_level=pos['source_level'],source_layer_index=pos['source_layer_index'],source_x=pos['source_x'],source_y=pos['source_y'],source_raw_gid=pos['source_raw_gid'])
 first=tmx_verify(loc)
 held.append(dict(status='held',observed=0,visual_features='not_individually_reviewed',identity_candidate='',part_role='',material='',direction='',connection='',confidence='none',source_png=r['source_image_path'],source_pixel_sha=sha(im.tobytes()),alternate_png='',alternate_pixel_sha='',**loc,source_firstgid=first,source_crop=r['selected_crop_xyxy'],B_C_changed_pixels='',B_D_changed_pixels='',mapping_verified=0,tilezed_verified=0,certified=0,evidence='JUMBO A3 original sprite and raw GID verified; atlas grid/sprite alignment NOT verified'))
for group in range(2):
 sheet=Image.new('RGB',(2000,1200),'#eff3f7');d=ImageDraw.Draw(sheet)
 for j,r in enumerate(jumbo[group*10:(group+1)*10]):
  x=(j%5)*400;y=(j//5)*600
  im=crop(r['source_image_path'],box(r['selected_crop_xyxy']))
  im.thumbnail((384,522))
  d.rectangle((x+3,y+3,x+397,y+597),fill='white',outline='#a1aebc',width=2)
  d.text((x+9,y+10),f'{r["tile_set_name"]}/{r["local_id"]}',fill='#203c54',font=font)
  d.text((x+9,y+27),'JUMBO A3: ALIGNMENT UNVERIFIED',fill='#a45d31',font=font)
  sheet.paste(im,(x+(400-im.width)//2,y+49),im)
 sheet.save(O/f'JUMBO_20_sheet_{group}.jpg',quality=85,optimize=True)
total=out+held;assert len(total)==23 and len({(r['tile_set_name'],r['local_id']) for r in total})==23
for name,items in [('VISUAL_OBSERVATIONS_3.csv',out),('JUMBO_AUDIT_20.csv',held),('ALL_STATUS_23.csv',total)]:
 with (O/name).open('w',encoding='utf-8-sig',newline='') as f:
  w=csv.DictWriter(f,fieldnames=fields);w.writeheader();w.writerows(items)
zero=rows(R/'review/v121_C_diff_new4632/ZERO_DELTA_REVIEW.csv');assert len(zero)==215
missing=[r for r in b.values() if int(r['neighbor_tiles_skipped'])>0];assert len(missing)==8
edge=[r for r in b.values() if r['scene_truncated_at_map_edge']=='1'];assert len(edge)==48
priority=[dict(exception=flag,tile_set_name=r.get('tile_set_name',''),local_id=r.get('local_id',''),review_status='held',transparent_certified=0) for flag,items in [('B_C_zero_unresolved',zero),('neighbor_missing',missing),('map_boundary_truncated',edge)] for r in items]
assert len(priority)==271
with (O/'PRIORITY_271_EXCEPTIONS.csv').open('w',encoding='utf-8-sig',newline='') as f:
 w=csv.DictWriter(f,fieldnames=list(priority[0]));w.writeheader();w.writerows(priority)
tmp=Path('/tmp/PZ_v132_physical.sqlite');tmp.write_bytes(raw)
with sqlite3.connect(tmp) as db:
 before={r[0] for r in db.execute("SELECT name FROM sqlite_master WHERE type='table'")};assert len(before)==193
 counts={n:db.execute('SELECT COUNT(*) FROM "'+n+'"').fetchone()[0] for n in before}
 assert db.execute('PRAGMA integrity_check').fetchone()[0]=='ok'
 assert db.execute('SELECT COUNT(*) FROM v131_D_full_4633').fetchone()[0]==4633
 db.execute('CREATE TABLE v132_visual3_jumbo20 ('+','.join('"'+f+'" '+('INTEGER' if f in ['local_id','observed','source_level','source_layer_index','source_x','source_y','source_raw_gid','source_firstgid','B_C_changed_pixels','B_D_changed_pixels','mapping_verified','tilezed_verified','certified'] else 'TEXT') for f in fields)+',PRIMARY KEY(tile_set_name,local_id),CHECK(mapping_verified=0 AND tilezed_verified=0 AND certified=0))')
 db.executemany('INSERT INTO v132_visual3_jumbo20 VALUES ('+','.join('?' for _ in fields)+')',[[r.get(f) for f in fields] for r in total]);db.commit()
 after={r[0] for r in db.execute("SELECT name FROM sqlite_master WHERE type='table'")}
 assert after-before=={'v132_visual3_jumbo20'} and len(after)==194
 assert all(db.execute('SELECT COUNT(*) FROM "'+n+'"').fetchone()[0]==x for n,x in counts.items())
 assert db.execute('SELECT COUNT(*) FROM v132_visual3_jumbo20 WHERE observed=1').fetchone()[0]==3
 assert db.execute('SELECT COUNT(*) FROM v132_visual3_jumbo20 WHERE status="held"').fetchone()[0]==20
 assert db.execute('PRAGMA integrity_check').fetchone()[0]=='ok'
rawnew=tmp.read_bytes();pack=zlib.compress(rawnew,8);enc=base64.b64encode(pack).decode('ascii');parts=[]
for n in range(0,len(enc),3000000):
 p=D/f'v132.part{n//3000000:03d}.b64';p.write_text(enc[n:n+3000000],encoding='ascii');parts.append(p.relative_to(R).as_posix())
assert sha(zlib.decompress(base64.b64decode(''.join((R/p).read_text() for p in parts))))==sha(rawnew)
manifest=dict(version='v132',parent='v131',parent_sqlite_sha256=v131['sqlite_sha256'],sqlite_sha256=sha(rawnew),sqlite_bytes=len(rawnew),compressed_sha256=sha(pack),parts=parts,parent_tables_preserved=193,table_count=194,new_rows=23,new_observations=3,jumbo_source_tmx_audited=20,unreviewed_exception_queue=271,mapping_verified=0,tilezed_verified=0,certified=0,integrity_check='ok')
(D/'MANIFEST.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
(O/'MANIFEST.json').write_text(json.dumps(dict(version='v132',source_main_commit='5bae2a6ef593b074f8731a19c48ad0bff5a5eff1',direct_visual_reviews=3,jumbo_source_and_gid_verified_but_not_grid=20,unreviewed_exception_rows=271,mapping_verified=0,tilezed_verified=0,certified=0,images={p.name:hs(p) for p in O.glob('*.jpg')},csvs={p.name:hs(p) for p in O.glob('*.csv')}),ensure_ascii=False,indent=2)+'\n',encoding='utf8')
print('PASS 3 reviewed, 20 jumbo source+TMX audited, 271 exception queue; v132 SQLite '+sha(rawnew),flush=True)
