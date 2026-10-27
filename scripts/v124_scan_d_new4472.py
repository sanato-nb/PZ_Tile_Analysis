#!/usr/bin/env python3
"""v124: read all 84 original TMX files, index genuine second placements for v120 rows 160..4631.
Read-only v123 parent SQLite; append only new v124 table. D coordinate != D rendered image.
"""
from pathlib import Path
from collections import Counter
import bisect,csv,hashlib,base64,zlib,sqlite3,json,xml.etree.ElementTree as ET,re
R=Path(__file__).resolve().parents[1]
TMX=R/'B4220.3_MapExport_256/tmx'
OUT=R/'review/v124_D_locations_new4472'
DBOUT=R/'analysis/current/v124'
OUT.mkdir(parents=True,exist_ok=True);DBOUT.mkdir(parents=True,exist_ok=True)
def sha(b):return hashlib.sha256(b).hexdigest()
def filesha(p):return sha(p.read_bytes())
def rows(path):
    with path.open(encoding='utf-8-sig',newline='') as f:return list(csv.DictReader(f))
def layer_level(ly):
    if 'level' in ly.attrib:return int(ly.get('level','0'))
    p=ly.find("properties/property[@name='level']")
    return int((p.get('value') or p.text or '0') if p is not None else '0')
def load_map(name):
    root=ET.parse(TMX/name).getroot()
    ts=sorted((int(t.get('firstgid')),t.get('name')) for t in root.findall('tileset') if t.get('name'))
    firsts=[v[0] for v in ts]
    assert firsts
    w=int(root.get('width','256'));h=int(root.get('height','256'))
    layers=[]
    for i,ly in enumerate(root.iter('layer')):
        d=ly.find('data')
        assert d is not None and d.get('encoding')=='csv'
        a=[int(s) for s in re.findall(r'\d+',d.text or '')]
        assert len(a)==w*h
        layers.append(dict(index=i,name=ly.get('name',''),level=layer_level(ly),values=a))
    return dict(ts=ts,firsts=firsts,w=w,h=h,layers=layers)
def key_for(m,raw):
    gid=raw&0x0fffffff
    if not gid:return None
    i=bisect.bisect_right(m['firsts'],gid)-1
    if i<0:return None
    first,name=m['ts'][i]
    return (name,gid-first)
bfile=R/'review/v120_B_context_new4632/B_CONTEXT_4632.csv'
v120=rows(bfile)
assert len(v120)==4632
bm=json.loads((R/'review/v120_B_context_new4632/MANIFEST.json').read_text())
assert filesha(bfile)==bm['metadata_sha256']
old=rows(R/'analysis/imports/merged_catalog_5409.csv')
oldkeys={(r['tile_set_locator'],int(r['local_id'])) for r in old}
assert len(oldkeys)==5409
selected=v120[160:]
assert len(selected)==4472
targets={}
for i,r in enumerate(selected,160):
    k=(r['tile_set_name'],int(r['local_id']))
    assert k not in oldkeys and k not in targets
    targets[k]=(i,dict(tmx=r['tmx_file'],level=int(r['source_level']),
       layer_index=int(r['source_layer_index']),x=int(r['source_x']),y=int(r['source_y']),
       raw_gid=int(r['source_raw_gid'])))
assert len(targets)==4472
names=[f'{x}_{y}.tmx' for x in range(26,38) for y in range(43,50)]
assert len(names)==84
alternatives={};primary_confirmed=set();n_seen=0
for j,name in enumerate(names):
    assert filesha(TMX/name)==bm['source_TMX_sha256'][name],name
    m=load_map(name)
    for ly in m['layers']:
        for p,raw in enumerate(ly['values']):
            if not raw:continue
            k=key_for(m,raw)
            if k not in targets:continue
            n_seen+=1
            index,primary=targets[k]
            same=(name==primary['tmx'] and ly['index']==primary['layer_index']
                  and p==primary['y']*m['w']+primary['x'])
            if same:
                assert raw==primary['raw_gid'] and ly['level']==primary['level']
                primary_confirmed.add(k);continue
            loc=dict(tmx=name,level=ly['level'],layer_index=ly['index'],
                    x=p%m['w'],y=p//m['w'],raw_gid=raw)
            loc['bounded']=int(2<=loc['x']<m['w']-2 and 2<=loc['y']<m['h']-2)
            prev=alternatives.get(k)
            if prev is None or (not prev['bounded'] and loc['bounded']):
                alternatives[k]=loc
    if (j+1)%14==0:print('TMX_SCANNED',j+1,'/',len(names),'D_found',len(alternatives),flush=True)
assert len(primary_confirmed)==4472,(len(primary_confirmed),4472)
out=[]
for k,(index,a) in sorted(targets.items(),key=lambda kv:kv[1][0]):
    d=alternatives.get(k)
    record=dict(index=index,tile_set_name=k[0],local_id=k[1],
        source_tmx=a['tmx'],source_level=a['level'],source_layer_index=a['layer_index'],
        source_x=a['x'],source_y=a['y'],source_raw_gid=a['raw_gid'],
        d_status='actual_second_placement' if d else 'no_second_placement',
        d_tmx=d['tmx'] if d else '',d_level=d['level'] if d else '',
        d_layer_index=d['layer_index'] if d else '',d_x=d['x'] if d else '',
        d_y=d['y'] if d else '',d_raw_gid=d['raw_gid'] if d else '',
        d_5x5_bounded=d['bounded'] if d else '',
        D_image_generated=0,review_status='placement_index_only_not_visual_reviewed',
        mapping_verified=0,tilezed_verified=0,final_certified=0)
    out.append(record)
assert len(out)==4472 and len({(r['tile_set_name'],r['local_id']) for r in out})==4472
prior=rows(R/'review/v123_ABCD_next160/ABCD_160_319.csv')
assert len(prior)==160
for a,b in zip(out[:160],prior):
    assert a['index']==int(b['index'])
    assert (a['tile_set_name'],a['local_id'])==(b['tile_set_name'],int(b['local_id']))
    assert a['d_status']==b['d_status']
    for u,v in [('d_tmx','d_tmx'),('d_level','d_level'),('d_layer_index','d_layer_index'),('d_x','d_x'),('d_y','d_y'),('d_raw_gid','d_raw_gid')]:
        assert str(a[u])==b[v],(a['index'],u,a[u],b[v])
assert all(r['D_image_generated']==0 for r in out)
outfile=OUT/'D_REAL_PLACEMENTS_4472.csv'
with outfile.open('w',encoding='utf-8-sig',newline='') as f:
    w=csv.DictWriter(f,fieldnames=list(out[0]));w.writeheader();w.writerows(out)
actual=sum(r['d_status']=='actual_second_placement' for r in out)
missing=4472-actual
bounded=sum(r['d_5x5_bounded']==1 for r in out)
pjson=R/'analysis/current/v123/MANIFEST.json'
parent=json.loads(pjson.read_text())
assert parent['version']=='v123' and parent['v122_tables_preserved']==184
enc=''.join((R/p).read_text('ascii').strip() for p in parent['parts'])
compressed=base64.b64decode(enc,validate=True)
assert sha(compressed)==parent['compressed_sha256']
db_raw=zlib.decompress(compressed)
assert len(db_raw)==parent['sqlite_bytes'] and sha(db_raw)==parent['sqlite_sha256']
local=Path('/tmp/pz_v124_append.sqlite');local.write_bytes(db_raw)
with sqlite3.connect(local) as c:
    before={x[0] for x in c.execute("SELECT name FROM sqlite_master WHERE type='table'")}
    assert len(before)==185 and {'v121_abcd_evidence','v122_ai_visual_review_160','v123_abcd_evidence_next160'}<=before
    assert c.execute('PRAGMA integrity_check').fetchone()[0]=='ok'
    assert c.execute('SELECT count(*) FROM tile_catalog').fetchone()[0]==5409
    assert c.execute('SELECT count(*) FROM tile_catalog WHERE observed_any=1').fetchone()[0]==5400
    assert c.execute('SELECT count(*) FROM v122_ai_visual_review_160').fetchone()[0]==160
    assert c.execute('SELECT count(*) FROM v123_abcd_evidence_next160').fetchone()[0]==160
    c.execute("""CREATE TABLE v124_d_placement_4472(
        tile_set_name TEXT NOT NULL,local_id INTEGER NOT NULL,original_v120_index INTEGER NOT NULL,
        source_tmx TEXT,source_level INTEGER,source_layer_index INTEGER,source_x INTEGER,
        source_y INTEGER,source_raw_gid INTEGER,d_status TEXT NOT NULL,
        d_tmx TEXT,d_level INTEGER,d_layer_index INTEGER,d_x INTEGER,d_y INTEGER,
        d_raw_gid INTEGER,d_5x5_bounded INTEGER,D_image_generated INTEGER DEFAULT 0,
        review_status TEXT,mapping_verified INTEGER DEFAULT 0,tilezed_verified INTEGER DEFAULT 0,
        final_certified INTEGER DEFAULT 0,PRIMARY KEY(tile_set_name,local_id))""")
    c.executemany('INSERT INTO v124_d_placement_4472 VALUES ('+','.join('?' for _ in range(22))+')',[
      (r['tile_set_name'],r['local_id'],r['index'],r['source_tmx'],r['source_level'],
       r['source_layer_index'],r['source_x'],r['source_y'],r['source_raw_gid'],r['d_status'],
       r['d_tmx'],r['d_level'] or None,r['d_layer_index'] if r['d_layer_index']!='' else None,
       r['d_x'] if r['d_x']!='' else None,r['d_y'] if r['d_y']!='' else None,
       r['d_raw_gid'] if r['d_raw_gid']!='' else None,
       r['d_5x5_bounded'] if r['d_5x5_bounded']!='' else None,0,r['review_status'],0,0,0)
      for r in out])
    after={x[0] for x in c.execute("SELECT name FROM sqlite_master WHERE type='table'")}
    assert after-before=={'v124_d_placement_4472'} and len(after)==186
    assert c.execute("SELECT count(*) FROM v124_d_placement_4472").fetchone()[0]==4472
    assert c.execute('SELECT count(*) FROM tile_catalog WHERE identity_final_certified=1').fetchone()[0]==0
    assert c.execute('PRAGMA integrity_check').fetchone()[0]=='ok'
    c.commit()
result_bytes=local.read_bytes()
packed=zlib.compress(result_bytes,level=8)
encoded=base64.b64encode(packed).decode('ascii')
parts=[]
for i in range(0,len(encoded),3000000):
    path=DBOUT/f'v124.part{i//3000000:03}.b64'
    path.write_text(encoded[i:i+3000000],'ascii')
    parts.append(path.relative_to(R).as_posix())
assert sha(zlib.decompress(base64.b64decode(''.join((R/p).read_text() for p in parts))))==sha(result_bytes)
dm=dict(version='v124',parent='v123',parent_sqlite_sha256=parent['sqlite_sha256'],
        sqlite_bytes=len(result_bytes),sqlite_sha256=sha(result_bytes),
        compressed_sha256=sha(packed),parts=parts,prior_tables_preserved=185,
        new_table='v124_d_placement_4472',new_rows=4472,
        original_catalog_preserved=5409,original_observed_preserved=5400,
        newly_visually_observed=0,final_certified=0,integrity_check='ok')
(DBOUT/'MANIFEST.json').write_text(json.dumps(dm,ensure_ascii=False,indent=2)+'\n')
vm=dict(version='v124',source='v120_B_context_new4632',
    source_original_TMX_84_sha256=bm.get('source_TMX_sha256',{}),
    original_TMX_count=84,selected_indices=[160,4631],D_scan_targets=4472,
    primary_verified=4472,D_actual_second_placement=actual,
    D_no_second_placement=missing,D_5x5_bounded=bounded,
    D_location_only=4472,D_new_images_generated=0,individual_identity_certified=0,
    visual_review_promoted=0,source_v123_reconciled=160,
    csv_path=outfile.relative_to(R).as_posix(),csv_sha256=filesha(outfile),
    sqlite_sha256=sha(result_bytes),sqlite_integrity='ok',prior_tables_preserved=185,
    old_5409_preserved=True,manual_review_preserved=True,user_exclusions_preserved=True,
    note='Original TMX second use locations only, no synthetic D; no D image for this stage. No mapping or TileZed certification.')
(OUT/'MANIFEST.json').write_text(json.dumps(vm,ensure_ascii=False,indent=2)+'\n')
(OUT/'REPORT.md').write_text(
  '# v124 D 전수 실배치 색인 (신규 v120 인덱스 160..4631)\n'
  '원본 84 TMX의 모든 레이어와 실제 raw GID를 탐색했으며 같은 층 5x5 화면까지 조립한 이미지가 아니라 실제 두 번째 위치의 좌표 색인입니다.\n'
  f'원본 첫 위치 확인 {len(primary_confirmed)}종 / 실제 D 존재 {actual}종 / D 없음 {missing}종 / D 5x5 경계 내부 {bounded}종.\n'
  'v123 이미지 증거 첫 160종과 160개 전부 재대조. 기존 5,409·수동 검수 80·사용자 제외 14·원본 TMX/PNG 불변.\n'
  'DB는 부모 v123의 185개 테이블을 그대로 보존하고 D 위치표만 신규 추가. 이미지 미생성 및 시각 판독 미수행 항목은 의미 확정하지 않습니다.\n',encoding='utf8')
print('PASS V124 D LOCATION INDEX',json.dumps({k:v for k,v in vm.items() if k not in ['source_original_TMX_84_sha256']},ensure_ascii=False),flush=True)
