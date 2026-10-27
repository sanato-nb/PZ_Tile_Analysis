#!/usr/bin/env python3
"""v131 reconcile the entire corrected D stage after 12 parallel rendering jobs.

Never infer that a neighboring grid sprite has same Local ID. Preserve the full
v130 SQLite and all preceding user annotations. Work may proceed only after all
12 completed ZIP+CSV batches are present, validated and disjoint.
"""
from pathlib import Path
import csv,json,hashlib,sqlite3,zipfile,base64,zlib
from collections import Counter
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'review/v131_D_full_remaining'
DBOUT=ROOT/'analysis/current/v131'
DBOUT.mkdir(parents=True,exist_ok=True)
def sha(p):
    h=hashlib.sha256()
    with p.open('rb') as f:
        for b in iter(lambda:f.read(1024*1024),b''):h.update(b)
    return h.hexdigest()
def readcsv(path):
    with path.open(encoding='utf-8-sig',newline='') as f:return list(csv.DictReader(f))
def writecsv(path,records):
    with path.open('w',encoding='utf-8-sig',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(records[0]))
        w.writeheader();w.writerows(records)
v120=json.loads((ROOT/'review/v120_B_context_new4632/MANIFEST.json').read_text('utf-8'))
all_b=readcsv(ROOT/'review/v120_B_context_new4632/B_CONTEXT_4632.csv')
assert len(all_b)==4632
prior=readcsv(ROOT/'analysis/imports/merged_catalog_5409.csv')
old_keys={(x['tile_set_locator'],str(int(x['local_id']))) for x in prior}
assert len(old_keys)==5409
expected_ranges=[(0,319)]+[(1120+(i-1)*320,min(4631,1119+i*320)) for i in range(1,12)]
assert expected_ranges[-1]==(4320,4631)
batches=[];newrows=[];artifact_manifest=[]
for batch in range(12):
    d=OUT/f'batch_{batch:02}'
    m=json.loads((d/'MANIFEST.json').read_text('utf-8'))
    assert m['version']=='v131' and m['batch']==batch
    lo,hi=expected_ranges[batch]
    assert m['source_v120_index_range']==[lo,hi]
    assert m['scope_new_only']==hi-lo+1
    assert m['correspondence_verified']==m['tilezed_verified']==m['identity_certified']==0
    assert m['human_visual_review_completed']==0
    assert m['D_alternative_rendered']+m['D_held']==m['scope_new_only']
    for key,digest in [
      ('D_scene_archive','D_scene_archive_sha256'),
      ('evidence_csv','evidence_csv_sha256'),
      ('trials_csv','trials_csv_sha256')]:
        p=ROOT/m[key]
        assert p.exists() and sha(p)==m[digest],(p,key)
    with zipfile.ZipFile(ROOT/m['D_scene_archive']) as z:
        assert z.testzip() is None,(batch,'CRC')
        assert len(z.namelist())==3*m['scope_new_only']+2*m['D_alternative_rendered']
    assert len(m['review_sheet_sha256'])==(m['scope_new_only']+39)//40
    for file,h in m['review_sheet_sha256'].items():
        p=d/file
        assert sha(p)==h
    rows=readcsv(ROOT/m['evidence_csv'])
    assert len(rows)==hi-lo+1
    assert [int(rows[0]['index']),int(rows[-1]['index'])]==[lo,hi]
    assert all(int(r['index'])==i for i,r in enumerate(rows,lo))
    assert all(r['correspondence_verified']==r['tilezed_verified']==r['identity_certified']=='0' and r['human_visual_review_completed']=='0' for r in rows)
    for r in rows:
        i=int(r['index']);k=(r['tile_set_name'],str(int(r['local_id'])))
        assert k not in old_keys and k==(all_b[i]['tile_set_name'],str(int(all_b[i]['local_id'])))
        assert r['source_tmx']==all_b[i]['tmx_file']
        assert r['source_tmx_sha256']==v120['source_TMX_sha256'][r['source_tmx']]
        assert int(r['source_x'])==int(all_b[i]['source_x']) and int(r['source_y'])==int(all_b[i]['source_y'])
        assert int(r['source_layer_index'])==int(all_b[i]['source_layer_index'])
        assert int(r['source_raw_gid'])==int(all_b[i]['source_raw_gid'])
        r['D_evidence_version']='v131'
        r['D_evidence_archive']=m['D_scene_archive']
        r['D_sheet_path']=str((d/f"ALT_A_B_sheet_{(i-lo)//40:02}.jpg").relative_to(ROOT))
        r['D_sheet_cell']=(i-lo)%40
    newrows+=rows
    batches.append(dict(batch=batch,range=[lo,hi],rendered=m['D_alternative_rendered'],held=m['D_held'],
                        changes=m['B_to_D_changed'],unchanged=m['B_to_D_unchanged'],
                        evidence=m['evidence_csv'],evidence_sha256=m['evidence_csv_sha256'],
                        ZIP=m['D_scene_archive'],ZIP_sha256=m['D_scene_archive_sha256']))
assert len(newrows)==3832
assert len({int(r['index']) for r in newrows})==3832
# Reuse, never regenerate, previously completed evidence batches.
historical=[
 ('v126',ROOT/'review/v126_D_alt_A_B_160/MANIFEST.json'),
 ('v129',ROOT/'review/v129_D_alt_A_B_320/MANIFEST.json'),
 ('v130',ROOT/'review/v130_D_alt_A_B_320/MANIFEST.json')]
oldrows=[]
for tag,p in historical:
    m=json.loads(p.read_text('utf8'))
    cf=ROOT/m['evidence_csv']
    assert sha(cf)==m['evidence_csv_sha256']
    rows=readcsv(cf)
    assert len(rows)==m['scope_new_only']
    for r in rows:
        i=int(r['index'])
        assert i>=0 and i<4632
        k=(r['tile_set_name'],str(int(r['local_id'])))
        assert k==(all_b[i]['tile_set_name'],str(int(all_b[i]['local_id'])))
        r['D_evidence_version']=tag
        r['D_evidence_archive']=m['D_scene_archive']
        r['D_sheet_path']=str((p.parent/f"ALT_A_B_sheet_{(i-int(m['source_v120_index_range'][0]))//40:02}.jpg").relative_to(ROOT))
        r['D_sheet_cell']=(i-int(m['source_v120_index_range'][0]))%40
    oldrows+=rows
assert len(oldrows)==800
# 0..319 v131, 320..479 v126, 480..799 v129, 800..1119 v130, 1120..4631 v131.
whole=sorted(newrows+oldrows,key=lambda x:int(x['index']))
assert len(whole)==4632 and [int(x['index']) for x in whole]==list(range(4632))
assert len({(r['tile_set_name'],int(r['local_id'])) for r in whole})==4632
status=Counter(r['alternate_status'] for r in whole)
assert set(status)<={'alternative_A_hypothesis_rendered','held_no_distinct_visible_A_hypothesis'}
rendered=status['alternative_A_hypothesis_rendered']
held=status['held_no_distinct_visible_A_hypothesis']
assert rendered+held==4632
assert all(int(r['correspondence_verified'])==int(r['tilezed_verified'])==int(r['identity_certified'])==int(r['human_visual_review_completed'])==0 for r in whole)
# A recorded source variant is just another experiment, not independent image identification.
names=list(dict.fromkeys(k for r in whole for k in r))
for r in whole:
    for key in names:r.setdefault(key,'')
rawpath=OUT/'D_ALL_4632_STATUS.csv'
writecsv(rawpath,whole)
newpath=OUT/'D_NEW_3832_STATUS.csv'
writecsv(newpath,newrows)

dbparent=json.loads((ROOT/'analysis/current/v130/MANIFEST.json').read_text('utf8'))
compressed=base64.b64decode(''.join((ROOT/p).read_text('ascii').strip() for p in dbparent['parts']),validate=True)
assert hashlib.sha256(compressed).hexdigest()==dbparent['compressed_sha256']
raw=zlib.decompress(compressed)
assert hashlib.sha256(raw).hexdigest()==dbparent['sqlite_sha256']
db=Path('/tmp/pz-v131-all-D.sqlite');db.write_bytes(raw)
with sqlite3.connect(db) as con:
    before={p[0] for p in con.execute("SELECT name FROM sqlite_master WHERE type='table'")}
    assert len(before)==192
    assert con.execute('PRAGMA integrity_check').fetchone()[0]=='ok'
    assert con.execute('SELECT count(*) FROM tile_catalog').fetchone()[0]==5409
    assert con.execute('SELECT count(*) FROM v126_alt_A_B_160').fetchone()[0]==160
    assert con.execute('SELECT count(*) FROM v129_alt_A_B_320').fetchone()[0]==320
    assert con.execute('SELECT count(*) FROM v130_alt_A_B_320').fetchone()[0]==320
    con.execute("""CREATE TABLE v131_D_full_4632 (
        tile_set_name TEXT NOT NULL, local_id INTEGER NOT NULL,
        v120_index INTEGER NOT NULL UNIQUE, d_status TEXT NOT NULL,
        evidence_version TEXT NOT NULL, source_tmx TEXT, source_level INTEGER,
        source_layer_index INTEGER, source_x INTEGER, source_y INTEGER, source_raw_gid INTEGER,
        original_rgba_sha256 TEXT, alternate_rgba_sha256 TEXT,
        alternate_kind TEXT, alternate_source_grid TEXT, B_C_changed_pixels INTEGER,
        D_C_changed_pixels INTEGER, B_D_changed_pixels INTEGER, D_evidence_archive TEXT,
        review_sheet TEXT, review_sheet_cell INTEGER,
        correspondence_verified INTEGER DEFAULT 0,tilezed_verified INTEGER DEFAULT 0,
        identity_certified INTEGER DEFAULT 0,human_visual_review_completed INTEGER DEFAULT 0,
        PRIMARY KEY(tile_set_name,local_id))""")
    def nullable_int(x):return int(x) if x not in ('',None) else None
    con.executemany("INSERT INTO v131_D_full_4632 VALUES ("+','.join(['?']*25)+")",[
       (r['tile_set_name'],int(r['local_id']),int(r['index']),r['alternate_status'],r['D_evidence_version'],
        r['source_tmx'],int(r['source_level']),int(r['source_layer_index']),int(r['source_x']),
        int(r['source_y']),int(r['source_raw_gid']),r['original_rgba_sha256'],
        r['alternate_rgba_sha256'],r['alternate_kind'],r['alternate_source_grid'],
        nullable_int(r['original_B_C_changed_pixels']),nullable_int(r['D_alternate_B_C_changed_pixels']),
        nullable_int(r['original_B_to_D_changed_pixels']),r['D_evidence_archive'],
        r['D_sheet_path'],int(r['D_sheet_cell']),0,0,0,0) for r in whole])
    after={p[0] for p in con.execute("SELECT name FROM sqlite_master WHERE type='table'")}
    assert len(after)==193 and after-before=={'v131_D_full_4632'}
    assert con.execute("SELECT count(*) FROM v131_D_full_4632").fetchone()[0]==4632
    assert con.execute('SELECT count(*) FROM tile_catalog').fetchone()[0]==5409
    assert con.execute('PRAGMA integrity_check').fetchone()[0]=='ok'
    con.commit()
dbraw=db.read_bytes()
dbytes=zlib.compress(dbraw,8);enc=base64.b64encode(dbytes).decode('ascii')
parts=[]
for i in range(0,len(enc),3000000):
    p=DBOUT/f'v131.part{i//3000000:03}.b64'
    p.write_text(enc[i:i+3000000],'ascii')
    parts.append(p.relative_to(ROOT).as_posix())
assert hashlib.sha256(zlib.decompress(base64.b64decode(''.join((ROOT/p).read_text('ascii') for p in parts)))).hexdigest()==hashlib.sha256(dbraw).hexdigest()
dbm=dict(version='v131',parent='v130',parent_sqlite_sha256=dbparent['sqlite_sha256'],
  prior_tables_preserved=192,new_table='v131_D_full_4632',new_rows=4632,
  sqlite_sha256=hashlib.sha256(dbraw).hexdigest(),sqlite_bytes=len(dbraw),
  compressed_sha256=hashlib.sha256(dbytes).hexdigest(),parts=parts,integrity_check='ok',
  mapping_verified=0,identity_certified=0,all_prior_data_preserved=True)
(DBOUT/'MANIFEST.json').write_text(json.dumps(dbm,ensure_ascii=False,indent=2)+'\n','utf8')
newR=sum(r['alternate_status']=='alternative_A_hypothesis_rendered' for r in newrows)
newH=3832-newR
report=dict(version='v131',date='2026-10-27',source='v127_prespecified_other_A_hypotheses',
 range_unique=4632,old_5409_reprocessed=0,remaining_3832_processed=3832,
 newly_rendered=newR,newly_held=newH,
 past_reused=800,full_D_same_B_source_hypotheses_attempted=4632,
 full_alternate_D_scenes_rendered=rendered,full_held=held,
 new_batches=batches,
 B_to_D_pixels_changed=sum(r['original_B_to_D_changed_pixels']!='' and int(r['original_B_to_D_changed_pixels'])>0 for r in whole),
 B_to_D_zero=sum(r['original_B_to_D_changed_pixels']!='' and int(r['original_B_to_D_changed_pixels'])==0 for r in whole),
 B_to_C_zero=sum(int(r['original_B_C_changed_pixels'])==0 for r in whole),
 full_all_keys_csv=rawpath.relative_to(ROOT).as_posix(),full_all_keys_csv_sha256=sha(rawpath),
 new_3832_csv=newpath.relative_to(ROOT).as_posix(),new_3832_csv_sha256=sha(newpath),
 full_source_120_csv_sha256=v120['metadata_sha256'],source_db_parent_v130_sha256=dbparent['sqlite_sha256'],
 sqlite_manifest='analysis/current/v131/MANIFEST.json',
 separate_v128_png_source_experiments=3,official_mapping_verified=0,TileZed_verified=0,final_identity_certified=0,
 caveat='Neighbor atlas crop D probes are NOT evidence of alternate A for SAME official tile Local ID; ALL are experimental, even if pixel changed. Identity review requires independent image and atlas mapping proof.')
(OUT/'SUMMARY.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n','utf8')
(OUT/'REPORT.md').write_text(
 f"# v131 D 전체 배치 일괄 생성 결과\n\n기존 완료 800키와 신규 처리 3,832키를 합쳐 **전체 4,632키**의 D 상태를 구성했습니다. "
 f"새 배치 생성 {newR}키·보류 {newH}키, 합산 생성 {rendered}키·보류 {held}키. "
 f"B−D 변화 양수 {report['B_to_D_pixels_changed']}, 변화0 {report['B_to_D_zero']}. "
 f"SQLite v131 **193테이블**, 과거 192개 전부 보존, PRAGMA integrity_check 통과.\n\n"
 f"**중요: 주변 격자 A 후보는 다른 Local ID일 수 있음. D 그림을 만들었다고 올바른 A 대응이나 물체 정체를 인증할 수 없음.** "
 f"검증된 개별 대응·TileZed·정체 0. 원본 TMX/PNG 및 기존 5,409 기록 전부 보존.\n",encoding='utf8')
print('PASS V131 ALL 4632 D STATUS',json.dumps({k:report[k] for k in
 ('remaining_3832_processed','newly_rendered','newly_held','full_alternate_D_scenes_rendered','full_held',
  'B_to_D_pixels_changed','B_to_D_zero')},ensure_ascii=False),
 'SQLITE_SHA',dbm['sqlite_sha256'],flush=True)
