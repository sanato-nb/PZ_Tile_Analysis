#!/usr/bin/env python3
"""B42 furniture v27 source warning triage; never certify game identity from geometry."""
import csv,hashlib,json,shutil,sqlite3,subprocess,zipfile
from pathlib import Path
from collections import Counter,defaultdict
R=Path(__file__).resolve().parents[1]
B=R/"analysis/furniture_full_b42/2026-11-05/all_multitile_visual_v26"
O=R/"analysis/furniture_full_b42/2026-11-05/source_warning_triage_v27"
Z=B/"B42_FURNITURE_SOURCE_GRID_VISUAL_V26.zip"
D=O/"B42_FURNITURE_SOURCE_DIAGNOSTICS_V27.sqlite"
P=O/"B42_FURNITURE_SOURCE_DIAGNOSTICS_V27.zip"
S="B42_FURNITURE_SOURCE_GRID_VISUAL_V26.sqlite"
expected={'source_attributes':195265,'source_slots':73644,'furniture_tile':8219,
'registry_entry':2231,'wiki_furniture':1268,'v13_warning_case':474,
'v13_warning_part':None,'v14_source_only_ledger':963,
'v20_source_only_review_coverage':963,'v20_unreviewed_source_queue':23,
'v20_23_original_atlas_filename_audit':23,'v21_all_source_rectangle_template':843,
'v21_source_tile_positioned_png':2221,
'v25_all_274_multifacing_group_pair_coverage':274,
'v26_all_820_source_direction_grid_visual_evidence':820,
'v26_all_346_source_multitile_group_coverage':346}
kinds={'MULTIPLE_NO_GRID':250,'MULTIPLE_EXACT_WIKI_ROWS':125,'MISSING_GRID':52,
'DUPLICATE_POSITION':27,'INCOMPLETE_GRID':14,
'MULTIPLE_RAW_CAPACITIES':5,'MULTIPLE_CONTAINER_TYPES':1}
def rows(c,q):return [dict(x) for x in c.execute(q)]
def js(x):return json.dumps(x,ensure_ascii=False,sort_keys=True)
def jarr(s):
 try:
  x=json.loads(s or '[]')
  return x if isinstance(x,list) else []
 except (TypeError,ValueError):return []
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def csvout(c,table,fn):
 cur=c.execute("SELECT * FROM "+table)
 names=[d[0] for d in cur.description]
 with (O/fn).open('w',encoding='utf-8-sig',newline='') as f:
  w=csv.writer(f);w.writerow(names);w.writerows(cur)
def add(c,t,col,values):c.executemany("UPDATE "+t+" SET "+col+"=? WHERE "+("entry_id=?" if t.endswith("png_triage") else "group_id=? AND Facing=? AND warning_code=?"),values)
def main():
 assert Z.exists() and not D.exists() and not P.exists()
 O.mkdir(parents=True,exist_ok=True)
 with zipfile.ZipFile(Z) as z:
  assert z.testzip() is None
  with z.open(S) as f,D.open('wb') as w:shutil.copyfileobj(f,w)
 source_hash=sha(D)
 c=sqlite3.connect(D);c.row_factory=sqlite3.Row
 assert c.execute('PRAGMA integrity_check').fetchone()[0]=='ok'
 assert not c.execute('PRAGMA foreign_key_check').fetchall()
 for t,n in expected.items():
  if n is not None:assert c.execute('SELECT COUNT(*) FROM '+t).fetchone()[0]==n,t
 assert not rows(c,"SELECT group_id,Facing,COUNT(*) n FROM v26_all_820_source_direction_grid_visual_evidence GROUP BY 1,2 HAVING n>1")
 assert c.execute("SELECT SUM(complete_isometric_assembly_game_verified+same_runtime_furniture_across_facings_certified) FROM v26_all_820_source_direction_grid_visual_evidence").fetchone()[0]==0
 files=subprocess.check_output(['git','ls-tree','-r','--name-only','HEAD','--','Tiles'],cwd=R,text=True).splitlines()
 png=defaultdict(list)
 for p in files:
  if p.lower().endswith('.png'):png[Path(p).name.lower()].append(p)
 assert len(png)>=300,('Git tree PNGs',len(png))
 # Full original records are inherited; append rechecked filename provenance and statuses.
 c.executescript("""
 CREATE TABLE v27_unlinked_png_triage AS
 SELECT q.entry_id,q.source_group_id AS group_id,q.original_name,
 l.tileset,l.original_tile_ids_json AS original_source_keys_json,
 a.original_tilesets_json,a.expected_png_filenames_json,
 a.possible_neighbor_or_state_alias_assets_json,a.reason AS previous_audit_reason,
 a.source_image_cell_matches_in_prior_db,
 '' AS exact_github_png_paths_json,'' AS neighboring_github_png_paths_json,
 '' AS missing_expected_filenames_json,'' AS github_filename_probe,
 0 AS original_png_local_id_cell_link_certified,
 0 AS runtime_furniture_identity_certified
 FROM v20_unreviewed_source_queue q
 JOIN v20_23_original_atlas_filename_audit a ON q.entry_id=a.entry_id
 JOIN v14_source_only_ledger l ON q.entry_id=l.entry_id;
 CREATE UNIQUE INDEX v27_png_eid ON v27_unlinked_png_triage(entry_id);
 CREATE TABLE v27_warning_triage AS SELECT *,
 0 AS source_part_count_keys_rechecked,
 'OPEN_REQUIRES_GAME_OR_ORIGINAL_IMAGE_EVIDENCE' AS v27_resolution_status,
 0 AS runtime_furniture_identity_certified
 FROM v13_warning_case;
 CREATE UNIQUE INDEX v27_warning_id ON v27_warning_triage(group_id,Facing,warning_code);
 """)
 q=rows(c,"SELECT * FROM v27_unlinked_png_triage ORDER BY entry_id")
 assert len(q)==23
 statuses=Counter()
 for r in q:
  expected_names=jarr(r['expected_png_filenames_json'])
  hints=jarr(r['possible_neighbor_or_state_alias_assets_json'])
  exact=sorted(set(p for n in expected_names for p in png.get(n.lower(),[])))
  neighbors=sorted(set(p for n in hints for p in png.get(n.lower(),[])))
  absent=sorted(set(n for n in expected_names if not png.get(n.lower())))
  state="EXACT_FILENAME_FOUND_CELL_UNPROVEN" if exact else "EXPECTED_FILENAME_NOT_IN_GIT_TREE"
  statuses[state]+=1
  assert c.execute('SELECT image_mapping_present FROM v14_source_only_ledger WHERE entry_id=?',(r['entry_id'],)).fetchone()[0]==0
  assert c.execute('SELECT direct_one_cell_visual_reviewed FROM v20_source_only_review_coverage WHERE entry_id=?',(r['entry_id'],)).fetchone()[0]==0
  c.execute("""UPDATE v27_unlinked_png_triage SET exact_github_png_paths_json=?,
   neighboring_github_png_paths_json=?,missing_expected_filenames_json=?,github_filename_probe=?
   WHERE entry_id=?""",(js(exact),js(neighbors),js(absent),state,r['entry_id']))
 warnings=rows(c,"SELECT * FROM v27_warning_triage ORDER BY priority,warning_code,group_id,Facing")
 assert len(warnings)==474 and dict(Counter(x['warning_code'] for x in warnings))==kinds
 parts=defaultdict(list)
 for p in rows(c,"SELECT group_id,Facing,warning_code,source_key FROM v13_warning_part"):
  parts[(p['group_id'],p['Facing'],p['warning_code'])].append(p['source_key'])
 for w in warnings:
  key=(w['group_id'],w['Facing'],w['warning_code'])
  check=sorted(jarr(w['source_keys_json']))==sorted(parts[key]) and len(parts[key])==w['source_tile_count']
  assert check,('warning proof mismatch',key)
  c.execute("UPDATE v27_warning_triage SET source_part_count_keys_rechecked=1 WHERE group_id=? AND Facing=? AND warning_code=?",key)
 c.executescript("""
 CREATE TABLE v27_warning_type_summary AS
 SELECT warning_code,COUNT(*) AS original_cases,
 SUM(source_part_count_keys_rechecked) AS source_cases_rechecked,
 0 AS certified_resolved,COUNT(*) AS still_open
 FROM v27_warning_triage GROUP BY warning_code;
 CREATE UNIQUE INDEX v27_warning_code ON v27_warning_type_summary(warning_code);
 CREATE TABLE v27_multifacing_geometry_recheck(
 group_id TEXT PRIMARY KEY,facing_count INTEGER,source_geometry_and_png_index_rechecked INTEGER,
 facing_shapes_and_source_atlas_json TEXT,
 certified_isometric_furniture_assembly INTEGER DEFAULT 0,
 certified_same_runtime_furniture_across_facings INTEGER DEFAULT 0);
 """)
 directions=defaultdict(list)
 for f in rows(c,"SELECT * FROM v26_all_820_source_direction_grid_visual_evidence"):
  directions[f['group_id']].append(f)
 indexed=defaultdict(list)
 for p in rows(c,"SELECT group_id,Facing,source_key,relative_x,relative_y,original_png_path FROM v21_source_tile_positioned_png"):
  indexed[(p['group_id'],p['Facing'])].append(p)
 group_count=0
 for gid,faces in sorted(directions.items()):
  if len(faces)<2:continue
  checks=[]
  for f in sorted(faces,key=lambda x:x['Facing']):
   pp=indexed[(gid,f['Facing'])]
   positions=[(p['relative_x'],p['relative_y']) for p in pp]
   grid={(x,y) for x in range(f['source_grid_w']) for y in range(f['source_grid_h'])}
   check=len(pp)==f['source_part_count'] and len(positions)==len(set(positions)) and set(positions)==grid and all(p['original_png_path'] for p in pp)
   assert check,(gid,f['Facing'])
   checks.append(dict(Facing=f['Facing'],grid_w=f['source_grid_w'],grid_h=f['source_grid_h'],parts=len(pp),atlas=sorted(set(p['original_png_path'] for p in pp))))
  c.execute("INSERT INTO v27_multifacing_geometry_recheck(group_id,facing_count,source_geometry_and_png_index_rechecked,facing_shapes_and_source_atlas_json) VALUES(?,?,1,?)",(gid,len(faces),js(checks)))
  group_count+=1
 assert group_count==274
 c.commit()
 assert c.execute('PRAGMA integrity_check').fetchone()[0]=='ok' and not c.execute('PRAGMA foreign_key_check').fetchall()
 for t,n in [('v27_unlinked_png_triage',23),('v27_warning_triage',474),('v27_warning_type_summary',7),('v27_multifacing_geometry_recheck',274)]:
  assert c.execute('SELECT COUNT(*) FROM '+t).fetchone()[0]==n,(t,n)
 for t,name in [('v27_unlinked_png_triage','V27_23_PNG_UNLINKED.csv'),
 ('v27_warning_triage','V27_474_SOURCE_WARNINGS.csv'),
 ('v27_warning_type_summary','V27_7_WARNING_TYPE_COUNTS.csv'),
 ('v27_multifacing_geometry_recheck','V27_274_MULTIFACING_SOURCE_RECHECK.csv')]:csvout(c,t,name)
 c.close()
 manifest={'version':'v27','base_commit':'cb4c048b1f1063c1737b25ab24f9e62428c53406',
 'parent_v26_zip_sha256':sha(Z),'parent_v26_sqlite_sha256':source_hash,
 'v27_sqlite_sha256':sha(D),'parent_zip_crc':'ok','v27_sqlite_integrity':'ok',
 'v27_foreign_keys':'ok','v26_source_tables_preserved':True,
 'repo_png_paths_indexed':sum(map(len,png.values())),
 'png_filename_probe':dict(statuses),'png_unlinked_groups_examined':23,
 'warnings_by_type':kinds,'warning_cases_source_proof_rechecked':474,
 'multifacing_source_geometries_rechecked':274,
 'new_image_visual_reviews':0,'old_820_visual_reviews_preserved':True,
 'png_cell_links_certified_resolved':0,'warnings_certified_resolved':0,
 'runtime_object_identity_certified':0,'isometric_assemblies_certified':0,
 'cross_facing_runtime_identity_certified':0}
 (O/'MANIFEST.json').write_text(json.dumps(manifest,indent=2,ensure_ascii=False,sort_keys=True)+'\n',encoding='utf8')
 (O/'README_KO.md').write_text(
  "# B42 가구 분석 v27: 원본 누락·경고 실제 목록 추출 및 재검증\n\n"
  "v26 전체 SQLite 사본에서 **23개 PNG 미연결 그룹**, **474개 원본 경고**, "
  "**274개 다방향 그룹**의 실제 키·부품·좌표·타일 이미지 연결 근거를 재확인했습니다.\n\n"
  "경고 유형과 건수(원본 경고 자체는 변경·삭제하지 않음):\n"+
  "\n".join('- '+k+': '+str(v) for k,v in kinds.items())+
  "\n\n원본 타일셋 PNG 파일명 검사: "+js(dict(statuses))+
  "\n\n**인증 한계:** PNG 파일명 일치는 특정 Local ID 이미지 연결이 아닙니다. "
  "직사각형 기하는 완성 아이소메트릭 가구·게임 런타임 방향별 동일성의 증거가 아닙니다. "
  "누락 PNG 연결 인증 해결 0/23, 경고 해결 0/474, 런타임 객체·아이소메트릭·다방향 동일성 인증 0건입니다. "
  "v26의 820개 이미지 검수는 새로 수행했다고 계산하지 않았습니다.\n\n"
  "다음 독립 근거: B42 SpriteGrid/객체 인스턴스·방향 참조, TileDef↔PNG 정식 Local ID "
  "셀 좌표 대응, 원점/렌더 오프셋/가림 순서, 필요한 경우 인게임 화면.\n",encoding='utf8')
 with zipfile.ZipFile(P,'w',zipfile.ZIP_DEFLATED,compresslevel=5) as z:
  for f in sorted(O.iterdir()):
   if f.is_file() and f!=P:z.write(f,f.name)
 with zipfile.ZipFile(P) as z:
  assert z.testzip() is None and D.name in z.namelist()
 print('V27_AUDIT_COMPLETE',json.dumps(manifest,ensure_ascii=False),flush=True)
if __name__=='__main__':main()
