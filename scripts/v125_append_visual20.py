#!/usr/bin/env python3
"""v125 20 individually viewed visual spotchecks from v123 original A/B/C/D sheet.
These are provisional visual family and part candidates, not official mapping or TileZed certifications.
"""
from pathlib import Path
import csv,json,hashlib,sqlite3,base64,zlib
R=Path(__file__).resolve().parents[1]
OUT=R/'review/v125_AI_ABCD_20'
DBDIR=R/'analysis/current/v125'
OUT.mkdir(parents=True,exist_ok=True)
DBDIR.mkdir(parents=True,exist_ok=True)
def sha(b):return hashlib.sha256(b).hexdigest()
def readcsv(path):
    with path.open(encoding='utf-8-sig',newline='') as f:return list(csv.DictReader(f))
parentcsv=readcsv(R/'review/v123_ABCD_next160/ABCD_160_319.csv')
assert len(parentcsv)==160 and [int(r['index']) for r in parentcsv[:20]]==list(range(160,180))
sheet=R/'review/v123_ABCD_next160/ABCD_sheet_00.jpg'
sheet_hash=sha(sheet.read_bytes())
source_manifest=json.loads((R/'review/v123_ABCD_next160/MANIFEST.json').read_text())
assert source_manifest['review_sheet_sha256'][sheet.name]==sheet_hash
spec=json.loads('''[["회색의 둥근 작은 돌이 여러 개 모여 보임","야외 돌무더기","바위·지형 조각","medium","provisional_candidate"],["낮은 둥근 돌 테두리가 원형으로 놓여 보임","돌로 둘러싼 야외 화덕 자리","야외 불자리 테두리","medium","provisional_candidate"],["둥근 돌벽과 세로 나무 지지대가 결합되어 보임","우물 형태 구조물","우물 몸체 및 지지대","medium","provisional_candidate"],["뿔을 가진 동물의 머리 모양이 장식으로 돌출되어 보임","동물 머리 박제 장식","벽걸이 장식","medium","provisional_candidate"],["갈색 각재로 만든 속이 빈 네모난 통 모양이 보임","나무 보관 상자","상자 본체","medium","provisional_candidate"],["길고 평평한 갈색 판재 여러 겹이 나란히 보임","나무 판재 적재 조각","다칸 목재 적재물 조각","low","provisional_candidate"],["밝은 원형 나무 단면 여러 개가 쌓여 보임","쌓인 통나무","장작 더미 조각","medium","provisional_candidate"],["짙은 갈색의 짧은 목재 여러 개가 가로로 놓여 보임","나무 적재물","목재 더미 조각","low","provisional_candidate"],["갈색 둥근 통나무가 겹쳐 쌓여 보임","작은 장작 더미","적층 장작 부품","medium","provisional_candidate"],["얇고 긴 짙은 갈색 판재가 수평으로 겹쳐 보임","목재 판재 적재물","더미 연결 조각","low","provisional_candidate"],["절단면이 노출된 목재 여러 개가 층을 이뤄 보임","장작 더미","장작 더미 조각","medium","provisional_candidate"],["짙은 갈색 판자형 목재가 여러 겹 쌓여 보임","나무 판자 더미","목재 적재물 일부","low","provisional_candidate"],["가로로 정돈된 통나무의 둥근 끝단이 보임","통나무 더미","통나무 적재물 일부","medium","provisional_candidate"],["넓고 납작한 갈색의 불규칙한 형태가 보임","","정체 불확실한 야외 조각","low","held"],["어두운 갈색의 짧은 나무판이 여러 겹 보임","나무 적재물","판자 더미 일부","low","provisional_candidate"],["밝은 원통형 나무 단면이 여러 층으로 쌓여 보임","장작 더미","장작 적재 부품","medium","provisional_candidate"],["긴 갈색 판재 면이 가로로 놓여 보임","적재 목재 판재","목재 더미 한 부분","low","provisional_candidate"],["굵은 갈색 통나무와 세로 방향의 묶는 띠가 보임","묶인 통나무","통나무 묶음의 세로 면","medium","provisional_candidate"],["넓은 나뭇결 모양의 갈색 표면이 보이나 다른 조각과 관계가 불분명함","","불확실한 목재 조각","low","held"],["둥근 통나무 끝단과 바깥쪽의 결속 띠가 보임","묶인 통나무 더미","통나무 더미 옆면","medium","provisional_candidate"]]''')
assert len(spec)==20
rows=[]
for i,notes in enumerate(spec):
    s=parentcsv[i]
    assert s['b_c_same_pixels']=='0' and s['review_status']=='evidence_generated_not_yet_visually_reviewed'
    features,candidate,part,confidence,status=notes
    rows.append(dict(index=160+i,tile_set_name=s['tile_set_name'],local_id=int(s['local_id']),
      observed_features=features,identity_candidate=candidate,part_role=part,confidence=confidence,
      review_status=status,visual_observed=1,
      source_sheet='review/v123_ABCD_next160/ABCD_sheet_00.jpg',
      sheet_sha256=sheet_hash,tmx_file=s['tmx_file'],source_level=int(s['level']),
      source_x=int(s['x']),source_y=int(s['y']),source_raw_gid=int(s['raw_gid']),
      b_c_changed_pixels=int(s['b_c_changed_pixels']),d_status=s['d_status'],
      mapping_verified=0,tilezed_verified=0,final_certified=0,
      note='실물 A와 주변 B/C 및 D 시트 직접 관찰에 기초한 잠정 후보. 공식 Local ID, TileZed 및 정체 인증 아님.'))
assert len({(r['tile_set_name'],r['local_id']) for r in rows})==20
assert sum(r['review_status']=='held' for r in rows)==2
assert sum(r['review_status']=='provisional_candidate' for r in rows)==18
outcsv=OUT/'AI_VISUAL_SPOTCHECK_20.csv'
with outcsv.open('w',encoding='utf-8-sig',newline='') as f:
    w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
dbm=json.loads((R/'analysis/current/v124/MANIFEST.json').read_text())
assert dbm['version']=='v124'
packed=base64.b64decode(''.join((R/p).read_text('ascii') for p in dbm['parts']),validate=True)
assert sha(packed)==dbm['compressed_sha256']
raw=zlib.decompress(packed)
assert sha(raw)==dbm['sqlite_sha256'] and len(raw)==dbm['sqlite_bytes']
dbfile=Path('/tmp/v125-full.sqlite')
dbfile.write_bytes(raw)
with sqlite3.connect(dbfile) as c:
    before={r[0] for r in c.execute("SELECT name FROM sqlite_master WHERE type='table'")}
    assert len(before)==186
    for name,count in [('tile_catalog',5409),('v121_abcd_evidence',160),('v122_ai_visual_review_160',160),('v123_abcd_evidence_next160',160),('v124_d_placement_4472',4472)]:
        assert c.execute('SELECT COUNT(*) FROM '+name).fetchone()[0]==count
    c.execute("""CREATE TABLE v125_ai_visual_spotcheck_20 (
        tile_set_name TEXT NOT NULL,local_id INTEGER NOT NULL,
        original_index INTEGER NOT NULL,observed_features TEXT,identity_candidate TEXT,
        part_role TEXT,confidence TEXT,review_status TEXT,visual_observed INTEGER,
        source_sheet TEXT,sheet_sha256 TEXT,source_tmx TEXT,source_level INTEGER,
        source_x INTEGER,source_y INTEGER,source_raw_gid INTEGER,
        b_c_changed_pixels INTEGER,d_status TEXT,note TEXT,
        mapping_verified INTEGER DEFAULT 0,tilezed_verified INTEGER DEFAULT 0,
        final_certified INTEGER DEFAULT 0,PRIMARY KEY(tile_set_name,local_id))""")
    c.executemany('INSERT INTO v125_ai_visual_spotcheck_20 VALUES ('+','.join(['?']*22)+')',[
      (r['tile_set_name'],r['local_id'],r['index'],r['observed_features'],r['identity_candidate'],
       r['part_role'],r['confidence'],r['review_status'],1,r['source_sheet'],r['sheet_sha256'],
       r['tmx_file'],r['source_level'],r['source_x'],r['source_y'],r['source_raw_gid'],
       r['b_c_changed_pixels'],r['d_status'],r['note'],0,0,0) for r in rows])
    after={r[0] for r in c.execute("SELECT name FROM sqlite_master WHERE type='table'")}
    assert len(after)==187 and after-before=={'v125_ai_visual_spotcheck_20'}
    assert c.execute('SELECT COUNT(*) FROM tile_catalog WHERE observed_any=1').fetchone()[0]==5400
    assert c.execute('SELECT COUNT(*) FROM tile_catalog WHERE identity_final_certified=1').fetchone()[0]==0
    assert c.execute('PRAGMA integrity_check').fetchone()[0]=='ok'
    c.commit()
newraw=dbfile.read_bytes()
compressed=zlib.compress(newraw,8)
encoded=base64.b64encode(compressed).decode()
parts=[]
for i in range(0,len(encoded),3000000):
    p=DBDIR/f'v125.part{i//3000000:03}.b64'
    p.write_text(encoded[i:i+3000000],'ascii')
    parts.append(p.relative_to(R).as_posix())
assert sha(zlib.decompress(base64.b64decode(''.join((R/p).read_text('ascii') for p in parts))))==sha(newraw)
manifest=dict(version='v125',source='v123_ABCD_next160',indices=[160,179],
    individually_visually_observed=20,provisional=18,held=2,combined_new_observed=180,
    prior_v122_observed=160,expanded_observed=5580,expanded_unobserved=4462,
    source_sheet_sha256=sheet_hash,csv_sha256=sha(outcsv.read_bytes()),
    csv_path=outcsv.relative_to(R).as_posix(),
    prior_SQLite_tables_preserved=186,sqlite_sha256=sha(newraw),
    mapping_verified=0,tilezed_verified=0,final_certified=0,
    limitation='Low/medium visual provisional families and parts; no definitive source Local ID or TileZed mapping; other 140 in v123 remain unreviewed.')
(OUT/'MANIFEST.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
(DBDIR/'MANIFEST.json').write_text(json.dumps(dict(version='v125',parent='v124',
    parent_sqlite_sha256=dbm['sqlite_sha256'],sqlite_bytes=len(newraw),
    sqlite_sha256=sha(newraw),compressed_sha256=sha(compressed),
    parts=parts,prior_tables_preserved=186,new_table='v125_ai_visual_spotcheck_20',
    new_rows=20,provisional=18,held=2,integrity_check='ok',final_certified=0),
    ensure_ascii=False,indent=2)+'\n')
(OUT/'REPORT.md').write_text(
    '# v125 실제 시각 판독 20종\n\n'
    'v123 기존 ABCD_sheet_00.jpg 실물 A/B/C/D 검수판 직접 관찰. 인덱스 160~179, 잠정 18종·보류 2종. '
    '기존 160종 v122 이미지 관찰과 고유키 분리. 새로운 공식 매핑/TileZed/최종 정체 인증 0. '
    '과거 5,409종·수동80·사용자 제외14·원본 PNG/TMX 미수정. '
    '전체 10,042종의 고유 시각 관찰은 5,580종, 신규 180종. '
    '물체가 여러 칸에 걸쳐도 판재·장작 조각을 완성된 개별 물체로 인증하지 않음.\n',encoding='utf8')
print('PASS v125',json.dumps(manifest,ensure_ascii=False),flush=True)
