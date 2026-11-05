#!/usr/bin/env python3
"""v28: independent per-facing native PNG-grid metadata audit, not runtime certification."""
from pathlib import Path
from collections import defaultdict,Counter
import csv,hashlib,json,sqlite3,shutil,zipfile
R=Path(__file__).resolve().parents[1]
B=R/"analysis/furniture_full_b42/2026-11-05/missing_atlas_warning_v27"
O=R/"analysis/furniture_full_b42/2026-11-05/cross_facing_structure_v28"
ZIP=B/"B42_FURNITURE_SOURCE_AUDIT_V27.zip"
MEMBER="B42_FURNITURE_SOURCE_AUDIT_V27.sqlite"
DB=O/"B42_FURNITURE_CROSS_FACING_STRUCTURE_V28.sqlite"
OUT=O/"B42_FURNITURE_CROSS_FACING_STRUCTURE_V28.zip"
def J(x):return json.dumps(x,ensure_ascii=False,sort_keys=True)
def q(c,sql):return [dict(x) for x in c.execute(sql)]
def csvw(name,data):
 assert data
 with (O/name).open("w",encoding="utf-8-sig",newline="") as f:
  w=csv.DictWriter(f,fieldnames=list(data[0]));w.writeheader();w.writerows(data)
def ins(c,t,data):
 keys=list(data[0])
 sql="INSERT INTO "+t+"("+",".join(keys)+") VALUES("+",".join('?' for _ in keys)+")"
 c.executemany(sql,[list(r.values()) for r in data])
def sha(p):
 h=hashlib.sha256()
 with p.open("rb") as f:
  for b in iter(lambda:f.read(1024*1024),b""):h.update(b)
 return h.hexdigest()
def main():
 O.mkdir(parents=True,exist_ok=True)
 assert ZIP.is_file() and not DB.exists() and not OUT.exists()
 with zipfile.ZipFile(ZIP) as z:
  assert z.testzip() is None
  assert MEMBER in z.namelist()
  with z.open(MEMBER) as a,DB.open("wb") as b:shutil.copyfileobj(a,b)
 base_hash=sha(DB)
 c=sqlite3.connect(DB);c.row_factory=sqlite3.Row
 assert c.execute('PRAGMA integrity_check').fetchone()[0]=='ok'
 assert not c.execute('PRAGMA foreign_key_check').fetchall()
 for t,n in {'source_attributes':195265,'source_slots':73644,'registry_entry':2231,
 'furniture_tile':8219,'v13_warning_case':474,'v27_missing_atlas_group':23,
 'v27_missing_atlas_source_key':89,'v27_three_absent_atlas_filenames':3,
 'v27_warning_source_proof':474,'v21_source_tile_positioned_png':2221,
 'v25_all_274_multifacing_group_pair_coverage':274,
 'v26_all_820_source_direction_grid_visual_evidence':820,
 'v26_all_346_source_multitile_group_coverage':346}.items():
  assert c.execute("SELECT COUNT(*) FROM "+t).fetchone()[0]==n,(t,n)
 previous={r['group_id'] for r in q(c,"SELECT group_id FROM v25_all_274_multifacing_group_pair_coverage")}
 source_parts=defaultdict(list)
 for p in q(c,"SELECT group_id,Facing,source_key,relative_x,relative_y,original_png_path,raw_sprite_grid_pos,container_type_original,container_capacity_original FROM v21_source_tile_positioned_png"):
  source_parts[(p['group_id'],p['Facing'])].append(p)
 allfaces=q(c,"SELECT * FROM v26_all_820_source_direction_grid_visual_evidence ORDER BY group_id,Facing")
 per_group=defaultdict(list);face_out=[]
 for face in allfaces:
  g,f=face['group_id'],face['Facing'];pp=source_parts[(g,f)]
  coords=[(x['relative_x'],x['relative_y']) for x in pp]
  expected={(x,y) for x in range(face['source_grid_w']) for y in range(face['source_grid_h'])}
  valid=len(pp)==face['source_part_count'] and len(coords)==len(set(coords)) and set(coords)==expected and all(x['original_png_path'] for x in pp)
  assert valid,(g,f,"rectangular source proof")
  properties=sorted({str(x['container_type_original']) for x in pp if x['container_type_original']})
  caps=sorted({str(x['container_capacity_original']) for x in pp if x['container_capacity_original'] not in ('',None)})
  tile_keys=sorted(x['source_key'] for x in pp)
  atlas=sorted({x['original_png_path'] for x in pp})
  r=dict(group_id=g,Facing=f,original_part_count=len(pp),
   original_grid_w=face['source_grid_w'],original_grid_h=face['source_grid_h'],
   original_png_atlases_json=J(atlas),original_source_keys_json=J(tile_keys),
   original_container_types_json=J(properties),original_container_capacities_json=J(caps),
   source_rectangular_geometry_rechecked=1,source_png_mapping_rechecked=1,
   inherited_visual_review_source_version=face['direct_original_png_visual_review_version'],
   v28_new_visual_inspection=0,isometric_assembly_certified=0,
   runtime_object_facing_identity_certified=0)
  face_out.append(r);per_group[g].append(r)
 assert len(face_out)==820 and len(per_group)==346
 multi_out=[];classifications=Counter()
 for g,faces in sorted(per_group.items()):
  if len(faces)<2:continue
  assert g in previous
  area={x['original_part_count'] for x in faces}
  sizes={(x['original_grid_w'],x['original_grid_h']) for x in faces}
  atlases={x['original_png_atlases_json'] for x in faces}
  types={x['original_container_types_json'] for x in faces}
  caps={x['original_container_capacities_json'] for x in faces}
  signature='SOURCE_PART_COUNTS_DIFFER' if len(area)>1 else 'SAME_SOURCE_PART_COUNT'
  if len(types)>1 or len(caps)>1:signature+='__CONTAINER_METADATA_VARIES'
  if len(atlases)>1:signature+='__ATLAS_SETS_VARY'
  classifications[signature]+=1
  multi_out.append(dict(group_id=g,source_facing_count=len(faces),
   source_part_counts_consistent=int(len(area)==1),
   source_dimensions_same=int(len(sizes)==1),
   atlas_path_sets_same=int(len(atlases)==1),
   original_container_metadata_same=int(len(types)==len(caps)==1),
   source_structure_comparison_category=signature,
   facing_and_original_png_metadata_json=J(faces),
   all_facing_rectangles_and_png_index_rechecked=1,
   exact_runtime_object_identity_certified=0,
   isometric_assembly_certified=0,
   next_needed_proof='GAME_RUNTIME_OBJECT_GRID_AND_ORIGIN_OFFSET_OVERLAP_RENDER_ORDER'))
 assert len(multi_out)==len(previous)==274
 c.executescript("""
 CREATE TABLE v28_820_source_facing_structure(
 group_id TEXT,Facing TEXT,original_part_count INTEGER,original_grid_w INTEGER,
 original_grid_h INTEGER,original_png_atlases_json TEXT,
 original_source_keys_json TEXT,original_container_types_json TEXT,
 original_container_capacities_json TEXT,source_rectangular_geometry_rechecked INTEGER,
 source_png_mapping_rechecked INTEGER,inherited_visual_review_source_version TEXT,
 v28_new_visual_inspection INTEGER,isometric_assembly_certified INTEGER,
 runtime_object_facing_identity_certified INTEGER,PRIMARY KEY(group_id,Facing));
 CREATE TABLE v28_274_cross_facing_source_metadata(
 group_id TEXT PRIMARY KEY,source_facing_count INTEGER,
 source_part_counts_consistent INTEGER,source_dimensions_same INTEGER,
 atlas_path_sets_same INTEGER,original_container_metadata_same INTEGER,
 source_structure_comparison_category TEXT,
 facing_and_original_png_metadata_json TEXT,
 all_facing_rectangles_and_png_index_rechecked INTEGER,
 exact_runtime_object_identity_certified INTEGER,
 isometric_assembly_certified INTEGER,next_needed_proof TEXT);
 """)
 ins(c,'v28_820_source_facing_structure',face_out)
 ins(c,'v28_274_cross_facing_source_metadata',multi_out)
 c.commit()
 assert c.execute('PRAGMA integrity_check').fetchone()[0]=='ok'
 assert not c.execute('PRAGMA foreign_key_check').fetchall()
 for t,n in {'v28_820_source_facing_structure':820,'v28_274_cross_facing_source_metadata':274,
 'v27_warning_source_proof':474,'v27_missing_atlas_group':23}.items():
  assert c.execute('SELECT COUNT(*) FROM '+t).fetchone()[0]==n,(t,n)
 c.close()
 csvw('V28_820_SOURCE_FACING_STRUCTURE_CHECKS.csv',face_out)
 csvw('V28_274_GROUP_SOURCE_FACING_COMPARISONS.csv',multi_out)
 cats=[{'source_structure_comparison_category':k,'group_count':v,
        'game_object_equivalence_certified':0} for k,v in sorted(classifications.items())]
 csvw('V28_STRUCTURE_COMPARISON_CATEGORIES.csv',cats)
 manifest=dict(version='v28',parent_git_commit='687176be209302746849820164f4e79a26b75991',
 parent_v27_zip_sha256=sha(ZIP),parent_v27_sqlite_sha256=base_hash,
 v28_sqlite_sha256=sha(DB),sqlite_integrity='ok',foreign_key_check='ok',zip_crc='ok',
 preserved_v27_unlinked_groups=23,preserved_v27_source_keys=89,preserved_v27_original_warnings=474,
 original_source_face_rectangles_rechecked=820,
 original_source_multifacing_groups_metadata_compared=274,
 provisional_metadata_comparison_categories=dict(classifications),
 newly_directly_visually_observed_facings=0,
 original_v26_direct_visual_facing_count_inherited=820,
 original_warnings_certified_resolved=0,png_cell_link_certified_resolved=0,
 runtime_objects_certified=0,complete_isometric_assemblies_certified=0,
 runtime_cross_facing_equivalence_certified=0)
 (O/'MANIFEST.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2,sort_keys=True)+'\n',encoding='utf8')
 (O/'README_KO.md').write_text(
 "# B42 가구 분석 v28 — 274그룹 전방향 원본 구조 교차검증\n\n"
 "입력은 성공한 Draft PR #309의 **v27 전체 SQLite ZIP**입니다. 기존 모든 테이블을 유지하고 새 구조 증거 테이블 두 개만 추가했습니다.\n\n"
 "- 총 **820개 group×Facing**의 원본 SpriteGridPos 직사각형 범위, 부품 source key, PNG 아틀라스 대응, 컨테이너 메타데이터를 다시 독립 검증.\n"
 "- **274개 다방향 그룹**의 모든 인덱싱된 Facing에 대해 부품 수, 그리드 크기, PNG 출처, 원본 컨테이너 메타데이터의 일치·차이를 기록.\n"
 "- 분류별 건수: "+J(dict(classifications))+"\n"
 "- v27 경고 474건·PNG 미연결 23그룹·관련 키 89개 유지. 경고나 미연결 문제가 해결됐다고 표기하지 않음.\n\n"
 "**한계:** 위 수치는 게임 내 실제 가구 조립이나 같은 런타임 게임 객체의 방향 동일성 인증이 아닙니다. "
 "신규 이미지 직접 관찰은 0건이며 인증도 0건입니다. "
 "실제 조립 판단에는 게임 SpriteGrid 원점·오프셋·겹침/렌더 순서와 런타임 객체 인스턴스 근거가 추가로 필요합니다.\n",encoding='utf8')
 with zipfile.ZipFile(OUT,'w',zipfile.ZIP_DEFLATED,compresslevel=5) as z:
  for f in sorted(O.iterdir()):
   if f.is_file() and f!=OUT:z.write(f,f.name)
 with zipfile.ZipFile(OUT) as z:assert z.testzip() is None and DB.name in z.namelist()
 print('V28_ALL_SOURCE_FACING_GEOMETRY_RECHECK_OK',J(manifest),flush=True)
if __name__=='__main__':main()
