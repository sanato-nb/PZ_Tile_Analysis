#!/usr/bin/env python3
"""v196 user's manual review: archive 33 verbatim decisions; exclude 10
unjudged from active queue only, not source universe or historical database."""
from pathlib import Path
from collections import Counter
import base64,csv,hashlib,json,sqlite3,zlib
R=Path(__file__).resolve().parents[1]
O=R/'review/v196_user_manual33';O.mkdir(parents=True,exist_ok=True)
D=R/'analysis/current/v196';D.mkdir(parents=True,exist_ok=True)
def sha(b):return hashlib.sha256(b).hexdigest()
def readcsv(path):
 with path.open(encoding='utf-8-sig',newline='') as f:return list(csv.DictReader(f))
fn=O/'USER_UPLOADED_33_VERBATIM.csv'
sourcehash='14671a09bf43d6273e53d56cfc4521fb092551499909793c90200770b4a441ef'
assert sha(fn.read_bytes())==sourcehash
rows=readcsv(fn)
assert len(rows)==33 and Counter(r['status'] for r in rows)=={'미판정':10,'잠정 후보':23}
fields=['tile_set_name','local_id','status','candidate','part','material','orientation','confidence','evidence','source_request','official_mapping_verified','certified']
assert set(rows[0])==set(fields)
keys={(r['tile_set_name'],int(r['local_id'])) for r in rows}
assert len(keys)==33 and all(r['certified']==r['official_mapping_verified']=='0' for r in rows)
assert all(r['candidate']=='' for r in rows if r['status']=='미판정')
assert all(r['candidate'].strip() for r in rows if r['status']=='잠정 후보')
assert sum(r['confidence']=='높음' for r in rows)==1
original=readcsv(R/'review/v193_manual33_offline_review/수동검수_33종_입력양식.csv')
assert {(r['tile_set_name'],int(r['local_id'])) for r in original}==keys
prior=[r for r in readcsv(R/'review/v192_image_first_TMX_BC_142/CROSSCHECK_142.csv') if r['new_provisional_observation']=='0']
assert len(prior)==33 and {(r['tile_set_name'],int(r['local_id'])) for r in prior}==keys
parent=json.loads((R/'analysis/current/v195/MANIFEST.json').read_text())
assert parent['version']=='v195' and parent['table_count']==254
packed=base64.b64decode(''.join((R/p).read_text('ascii').strip() for p in parent['parts']),validate=True)
assert sha(packed)==parent['compressed_sha256']
raw=zlib.decompress(packed)
assert sha(raw)==parent['sqlite_sha256'] and len(raw)==parent['sqlite_bytes']
tmp=Path('/tmp/pz-v196-manual.sqlite');tmp.write_bytes(raw)
db=sqlite3.connect(tmp)
assert db.execute('PRAGMA integrity_check').fetchone()[0]=='ok'
old={n:db.execute('SELECT COUNT(*) FROM "'+n+'"').fetchone()[0] for (n,) in db.execute("SELECT name FROM sqlite_master WHERE type='table'")}
assert len(old)==254
cols=','.join('"'+f+'" '+('INTEGER' if f=='local_id' else 'TEXT') for f in fields)
db.execute('CREATE TABLE v196_user_manual33_decisions ('+cols+',review_effect TEXT NOT NULL,uploaded_source_sha256 TEXT NOT NULL,PRIMARY KEY(tile_set_name,local_id),CHECK(official_mapping_verified="0" AND certified="0"))')
db.executemany('INSERT INTO v196_user_manual33_decisions VALUES ('+','.join('?' for _ in range(len(fields)+2))+')',[
 tuple(int(r[f]) if f=='local_id' else r[f] for f in fields)+
 ('excluded_unjudged_from_active_queue_only' if r['status']=='미판정' else 'user_provisional_not_final',sourcehash) for r in rows])
db.execute('CREATE TABLE v196_user_excluded10 (tile_set_name TEXT NOT NULL,local_id INTEGER NOT NULL,reason TEXT NOT NULL,source_sha256 TEXT NOT NULL,transparent_certified INTEGER NOT NULL CHECK(transparent_certified=0),identity_certified INTEGER NOT NULL CHECK(identity_certified=0),PRIMARY KEY(tile_set_name,local_id))')
exclude=[r for r in rows if r['status']=='미판정']
db.executemany('INSERT INTO v196_user_excluded10 VALUES (?,?,?,?,0,0)',[(r['tile_set_name'],int(r['local_id']),'2026-10-28 user requested exclude all undecided from ACTIVE manual review, preserve original raw and history',sourcehash) for r in exclude])
db.commit()
new={n:db.execute('SELECT COUNT(*) FROM "'+n+'"').fetchone()[0] for (n,) in db.execute("SELECT name FROM sqlite_master WHERE type='table'")}
assert len(new)==256 and set(new)-set(old)=={'v196_user_manual33_decisions','v196_user_excluded10'}
assert all(new[n]==old[n] for n in old)
assert new['v196_user_manual33_decisions']==33 and new['v196_user_excluded10']==10
assert db.execute('PRAGMA integrity_check').fetchone()[0]=='ok'
db.close()
newraw=tmp.read_bytes();compressed=zlib.compress(newraw,8)
encoded=base64.b64encode(compressed).decode('ascii');parts=[]
for i in range(0,len(encoded),3000000):
 p=D/('v196.part%03d.b64'%(i//3000000))
 p.write_text(encoded[i:i+3000000],encoding='ascii')
 parts.append(p.relative_to(R).as_posix())
assert sha(zlib.decompress(base64.b64decode(''.join((R/p).read_text('ascii') for p in parts))))==sha(newraw)
dbinfo={'version':'v196','parent':'v195','parent_sqlite_sha256':parent['sqlite_sha256'],
 'sqlite_sha256':sha(newraw),'compressed_sha256':sha(compressed),
 'sqlite_bytes':len(newraw),'parts':parts,'table_count':256,'previous_tables_preserved':254,
 'new_manual_decisions':33,'new_user_exclusions':10,'user_provisional':23,
 'active_manual_queue_remaining':0,'newly_observed':0,'historical_observed':10007,
 'historical_unobserved':35,'official_mapping_verified':0,'tilezed_verified':0,
 'certified':0,'integrity_check':'ok','uploaded_csv_sha256':sourcehash}
(D/'MANIFEST.json').write_text(json.dumps(dbinfo,ensure_ascii=False,indent=2)+'\n')
info={'version':'v196','uploaded_csv_sha256':sourcehash,'total':33,
 'manual_provisional':23,'user_excluded_undecided':10,'active_manual_remaining':0,
 'historical_observations_unchanged':10007,'historical_unobserved_unchanged':35,
 'unresolved_history_count_gap':2,'prior_14_user_exclusions_preserved':True,
 'transparent_certifications':0,'official_mapping_certifications':0,
 'identity_certifications':0,'database_sha256':sha(newraw),'sqlite_tables':256}
(O/'MANIFEST.json').write_text(json.dumps(info,ensure_ascii=False,indent=2)+'\n')
(O/'README.md').write_text(
 '# v196: 사용자 직접 검수 33종 반영\n\n'
 '업로드 CSV 원본 바이트 SHA256 '+sourcehash+' — BOM, CRLF, 공백 포함 변경 없이 보존.\n\n'
 '- 잠정 후보 23종: 사용자 표현/확신도 그대로 보관. 최종 정체나 공식 매핑 인증 아님.\n'
 '- 미판정 10종: 사용자 최신 명시 지시로 활성 수동 검수에서 제외. 원본 PNG/TMX, 원래 10,042 키 범위 및 과거 기록 삭제 금지. 투명 확정도 금지.\n'
 '- 과거 사용자 제외14 및 사용자 수동80 유지. 신규 관찰 추가0, 역사적 관찰 10007/10042 기록 불변.\n'
 '- 활성 수동 검수 큐 잔여 0, 사용자 잠정23종은 별도의 독립 A 우선 의미 재검증 가능.\n'
 '- v195의 기존254 SQLite 테이블 보존, v196 신규 2테이블(33+10행), 256테이블, PRAGMA integrity_check=ok.\n',encoding='utf-8')
statefile=R/'PROJECT_STATE.json';state=json.loads(statefile.read_text(encoding='utf-8'))
assert state['latest_checkpoint']['version']=='v195' and state['unified_database']['version']=='v195'
assert state['unified_database']['table_count']==254 and state['unified_database']['sqlite_sha256']==parent['sqlite_sha256']
assert state['latest_checkpoint']['expanded_unique_observed']==10007 and state['latest_checkpoint']['active_review_queue_remaining']==33
state['previous_checkpoint_v195']=dict(state['latest_checkpoint'])
state['latest_checkpoint'].update({
 'version':'v196','date':'2026-10-28','physical_unified_sqlite_version':'v196',
 'kind':'user_manual_33_decisions_and_exclude_10_unjudged_from_active',
 'active_review_queue_remaining':0,'active_review_remaining':0,
 'v196_user_provisional':23,'v196_user_excluded_unjudged':10,
 'v196_user_review_file':'review/v196_user_manual33/USER_UPLOADED_33_VERBATIM.csv',
 'v196_user_review_file_sha256':sourcehash,'v196_user_manual_pending':0,
 'v196_user_semantic_verification_pending':23,'v196_original_user_excluded14_preserved':True,
 'v196_hist_observation_10007_unchanged':True,'v196_hist_unobserved35_unchanged':True,
 'v196_sqlite_sha256':sha(newraw),
 'caution':'10 unjudged excluded from active review only, NOT deleted/transparent. 23 user provisional notes are not A-mapping/TileZed or official identity certified. Historical 10007 observed/35 unobserved counts remain unchanged.'
})
state['unified_database'].update({
 'version':'v196','parent_unified_version':'v195','repo_manifest':'analysis/current/v196/MANIFEST.json',
 'status':'USER_MANUAL_PROVISIONAL23_EXCLUDED_UNJUDGED10_NOT_CERTIFIED',
 'sqlite_sha256':sha(newraw),'table_count':256,'prior_tables_preserved':254,
 'all_prior_tables_preserved':True,'sqlite_size_bytes':len(newraw),
 'manual_review_rows':33,'manual_provisional':23,'manual_user_excluded':10,
 'active_review_remaining':0,'new_observed_rows':0,'certified':0
})
state['latest_v196_user_manual_review']={'source_sha256':sourcehash,'rows':33,
 'manual_provisional':23,'user_excluded_unjudged':10,'active_review_remaining':0,
 'historical_observed_unchanged':10007,'historical_unobserved_unchanged':35,
 'sqlite_sha256':sha(newraw),'certified':0}
state['next_actions']=[
 'v196: Do not re-open user excluded 10 unjudged tiles without new explicit user request.',
 'v196: Retain 23 user-written provisional candidates verbatim. Independent A-first verification can proceed separately; do not certify from filenames or B/C.',
 *state.get('next_actions',[])]
statefile.write_text(json.dumps(state,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
brief=('## v196 사용자 수동판정 33종 (2026-10-28)\n\n'
 '- 사용자 원본 CSV SHA256 '+sourcehash+': 잠정 후보23(사용자 문구 보존), 미판정10은 명시적으로 활성 검수에서 제외. 기존 수동80·제외14 유지.\n'
 '- 제외10은 원본 10,042 키 또는 물리 DB에서 삭제/투명인증하지 않음. 역사적 관찰10,007/10,042 기록 불변, 사용자 활성 수동 검수 잔여0, 의미/공식 매핑 인증 0.\n'
 '- 부모 v195 254테이블 보존, v196 물리256테이블(사용자 판정33 + 제외10), integrity_check=ok. 증거 review/v196_user_manual33 및 analysis/current/v196.\n\n---\n')
for rel in ('AGENTS.md','docs/HANDOFF.md'):
 file=R/rel;oldtext=file.read_text(encoding='utf-8')
 assert 'v195' in oldtext[:400]
 j=oldtext.index('\n')
 file.write_text(oldtext[:j+1]+'\n'+brief+oldtext[j+1:].lstrip('\n'),encoding='utf-8')
print('PASS v196 import: user provisional23, active-excluded10, 256-table integrity-check ok',sha(newraw),flush=True)
