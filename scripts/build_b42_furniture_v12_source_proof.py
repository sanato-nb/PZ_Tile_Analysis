#!/usr/bin/env python3
"""B42 v11: map each original source sprite ID to its own SpriteGridPos.
Never zip independently sorted v10 sprite-id and grid-position columns.
No PNG review, automatic game-object merge, Lua or Minecraft decisions.
"""
import csv,json,sqlite3,shutil,zipfile,re
from pathlib import Path
from collections import Counter
R=Path(__file__).resolve().parents[1]
SRC=R/"analysis/furniture_full_b42/2026-11-04/exact_assembly_v11/B42_EXACT_TILE_GRID_ASSEMBLY_V11.zip"
OUT=R/"analysis/furniture_full_b42/2026-11-04/source_proof_v12"
DB=OUT/"B42_FURNITURE_SOURCE_PROOF_V12.sqlite"
PACK=OUT/"B42_EXACT_TILE_GRID_ASSEMBLY_V11.zip"
POS=re.compile(r"^\s*(-?\d+)\s*,\s*(-?\d+)\s*$")
def query(c,s):return [dict(x) for x in c.execute(s)]
def n(c,t):return c.execute("SELECT COUNT(*) FROM "+t).fetchone()[0]
def uniq(s):return sorted({x for x in s if x not in ("",None)})
def split(s):return [x for x in (s or "").split("|") if x]
def xy(s):
 a=split(s)
 if len(a)!=1:return None
 m=POS.fullmatch(a[0])
 return (int(m.group(1)),int(m.group(2))) if m else None
def j(v):return json.dumps(v,ensure_ascii=False,sort_keys=True)
def put(c,t,row):
 ks=list(row)
 c.execute("INSERT INTO "+t+"("+",".join(ks)+") VALUES("+",".join(["?"]*len(ks))+")",[row[k] for k in ks])
def csvout(name,rr):
 assert rr,name
 with (OUT/name).open("w",encoding="utf-8-sig",newline="") as f:
  w=csv.DictWriter(f,list(rr[0]),extrasaction="ignore");w.writeheader();w.writerows(rr)

def main():
 import hashlib
 from collections import defaultdict
 assert SRC.is_file() and not OUT.exists(),"v11 missing or v12 output already exists (no overwrites)"
 source_sha=hashlib.sha256(SRC.read_bytes()).hexdigest()
 OUT.mkdir(parents=True)
 with zipfile.ZipFile(SRC) as z:
  assert z.testzip() is None
  with z.open("B42_EXACT_TILE_GRID_ASSEMBLY_V11.sqlite") as a,DB.open("wb") as b:shutil.copyfileobj(a,b)
 c=sqlite3.connect(DB);c.row_factory=sqlite3.Row
 assert c.execute("PRAGMA integrity_check").fetchone()[0]=="ok"
 baseline={"source_attributes":195265,"source_slots":73644,"furniture_tile":8219,"v10_tile_reverse":8219,
           "v11_tile_position":8219,"v11_direction_template":3840,"v11_source_warning":474,
           "v10_reverse_edge":14195,"registry_entry":2231,"wiki_furniture":1268,
           "v9_container_evidence":1855,"v9_wiki_missing_id":11,"v9_v8_image_review_reference":129}
 for t,expect in baseline.items():assert n(c,t)==expect,(t,n(c,t),expect)
 c.executescript("""
 CREATE TABLE v12_tile_proof(group_id TEXT,Facing TEXT,source_key TEXT,
  original_grid TEXT,raw_x INTEGER,raw_y INTEGER,relative_x_when_available INTEGER,relative_y_when_available INTEGER,
  collision_occupancy INTEGER,source_facing TEXT,source_container TEXT,source_capacity_raw TEXT,
  source_container_position TEXT,exact_wiki_json TEXT,source_files TEXT,identity_certified INTEGER DEFAULT 0,
  PRIMARY KEY(group_id,Facing,source_key));
 CREATE TABLE v12_template_proof(group_id TEXT,Facing TEXT,source_status TEXT,reproduced_status TEXT,
  pieces INTEGER,known_grid_cells INTEGER,unique_grid_cells INTEGER,grid_w INTEGER,grid_h INTEGER,
  holes_json TEXT,collisions_json TEXT,source_keys_json TEXT,game_identity_certified INTEGER DEFAULT 0,
  PRIMARY KEY(group_id,Facing));
 CREATE TABLE v12_warning_proof(group_id TEXT,Facing TEXT,issue TEXT,original_reason TEXT,
  independently_reproduced INTEGER,source_parts_json TEXT,source_evidence_type TEXT,
  review_state TEXT,object_certified INTEGER DEFAULT 0,
  PRIMARY KEY(group_id,Facing,issue));
 CREATE TABLE v12_wiki_unlinked_proof(wiki_id TEXT PRIMARY KEY,wiki_name TEXT,original_category TEXT,
  sibling_keys INTEGER,name_candidate_count INTEGER,source_candidate_rows INTEGER,
  new_automatic_links INTEGER DEFAULT 0,confirmed_identity INTEGER DEFAULT 0);
 CREATE TABLE v12_129_visual_reference(group_id TEXT PRIMARY KEY,review_version TEXT,
  evidence_type TEXT,identity_certified INTEGER DEFAULT 0);
 CREATE TABLE v12_work_107_scope(scope_key TEXT PRIMARY KEY,reported_groups INTEGER,reported_tiles INTEGER,
  saved_individual_review_rows_verified INTEGER,individual_reviews_imported INTEGER,evidence_status TEXT);
 CREATE INDEX v12_tile_source_index ON v12_tile_proof(source_key);
 CREATE INDEX v12_warning_issue_index ON v12_warning_proof(issue);
 """)
 pieces=query(c,"SELECT * FROM v11_tile_position ORDER BY group_id,Facing,source_key")
 grouped=defaultdict(list)
 for p in pieces:grouped[(p["group_id"],p["Facing"])].append(p)
 originals={(p["group_id"],p["Facing"],p["warning_code"]):p["description"] for p in query(c,"SELECT * FROM v11_source_warning")}
 verified={};tc=Counter();wc=Counter();a=[];b=[];w=[]
 oldmap={"RECTANGULAR_GRID_CANDIDATE":"COMPLETE_RECTANGLE",
         "INCOMPLETE_GRID_REVIEW":"INCOMPLETE_GRID","DUPLICATE_GRID_POSITION_REVIEW":"DUPLICATE_POSITION",
         "MIXED_GRID_AND_NO_GRID_REVIEW":"MISSING_GRID",
         "MULTIPLE_SPRITES_SAME_FACING_NO_GRID_REVIEW":"MULTIPLE_NO_GRID","SINGLE_SPRITE":"SINGLE_NO_GRID"}
 for t in query(c,"SELECT * FROM v11_direction_template ORDER BY group_id,Facing"):
  g,f=t["group_id"],t["Facing"];parts=grouped[(g,f)]
  assert len(parts)==t["raw_sprite_count"]
  pts=[xy(p["source_grid_pos_raw"]) for p in parts]
  for p,pt in zip(parts,pts):
   assert (p["raw_x"],p["raw_y"])==(pt if pt else (None,None)),p["source_key"]
  valid=[p for p in pts if p is not None];freq=Counter(valid)
  minx=min((p[0] for p in valid),default=None);miny=min((p[1] for p in valid),default=None)
  gw=max((p[0] for p in valid),default=-1)-minx+1 if valid else None
  gh=max((p[1] for p in valid),default=-1)-miny+1 if valid else None
  holes=[(x,y) for y in range(miny,miny+gh) for x in range(minx,minx+gw) if (x,y) not in freq] if valid and gw*gh<10000 else []
  collisions=[(x,y,n) for (x,y),n in sorted(freq.items()) if n>1]
  if not valid:status="SINGLE_NO_GRID" if len(parts)==1 else "MULTIPLE_NO_GRID"
  elif len(valid)<len(parts):status="MISSING_GRID"
  elif len(freq)<len(valid):status="DUPLICATE_POSITION"
  else:status="COMPLETE_RECTANGLE" if gw*gh==len(valid) else "INCOMPLETE_GRID"
  assert status==t["rechecked_grid_status"],(g,f,status,t["rechecked_grid_status"])
  tc[status]+=1
  flags={}
  if status in {"MULTIPLE_NO_GRID","MISSING_GRID","DUPLICATE_POSITION","INCOMPLETE_GRID"}:
   flags[status]="Raw SpriteGridPos does not provide a unique complete rectangle"
  if status!=oldmap.get(t["original_assembly_status"]):
   flags["RECHECK_DIFFERS_FROM_V10"]=str(t["original_assembly_status"])+" -> "+status
  if any(((f in split(p["source_facing_raw"])) if f!="(not set)" else not split(p["source_facing_raw"])) is False for p in parts):
   flags["FACING_CONFLICT"]="At least one TileDef sprite disagrees with candidate facing"
  ids=uniq(wiki for p in parts for wiki in json.loads(p["exact_wiki_ids_json"]))
  caps=uniq(p["source_capacity_raw"] for p in parts)
  containers=uniq(p["source_container"] for p in parts)
  if len(ids)>1:flags["MULTIPLE_EXACT_WIKI_ROWS"]="|".join(ids)
  if len(caps)>1:flags["MULTIPLE_RAW_CAPACITIES"]="|".join(caps)
  if len(containers)>1:flags["MULTIPLE_CONTAINER_TYPES"]="|".join(containers)
  for issue,reason in flags.items():
   key=(g,f,issue);verified[key]=reason;wc[issue]+=1
   sources=[dict(source_key=p["source_key"],source_grid=p["source_grid_pos_raw"],
    Facing=p["source_facing_raw"],container=p["source_container"],capacity=p["source_capacity_raw"],
    position=p["source_container_position_raw"],exact_wiki=json.loads(p["exact_wiki_ids_json"])) for p in parts]
   kind="GEOMETRY_SOURCE_UNRESOLVED" if issue in ("DUPLICATE_POSITION","MISSING_GRID","INCOMPLETE_GRID","MULTIPLE_NO_GRID") else (
    "WIKI_ANCHORS_NOT_OBJECT_IDENTITY" if issue=="MULTIPLE_EXACT_WIKI_ROWS" else "FUNCTION_OR_DEFINITION_VARIATION")
   obj=dict(group_id=g,Facing=f,issue=issue,original_reason=originals.get(key,""),
    independently_reproduced=int(originals.get(key)==reason),source_parts_json=j(sources),
    source_evidence_type=kind,review_state="OPEN_NO_OBJECT_AUTOMERGE")
   put(c,"v12_warning_proof",obj);w.append(obj)
  obj=dict(group_id=g,Facing=f,source_status=t["rechecked_grid_status"],reproduced_status=status,
   pieces=len(parts),known_grid_cells=len(valid),unique_grid_cells=len(freq),grid_w=gw,grid_h=gh,
   holes_json=j(holes),collisions_json=j(collisions),source_keys_json=j([p["source_key"] for p in parts]))
  put(c,"v12_template_proof",obj);b.append(obj)
  for p,pt in zip(parts,pts):
   obj=dict(group_id=g,Facing=f,source_key=p["source_key"],original_grid=p["source_grid_pos_raw"],
    raw_x=pt[0] if pt else None,raw_y=pt[1] if pt else None,
    relative_x_when_available=(pt[0]-minx) if pt else None,
    relative_y_when_available=(pt[1]-miny) if pt else None,
    collision_occupancy=freq[pt] if pt else 0,source_facing=p["source_facing_raw"],
    source_container=p["source_container"],source_capacity_raw=p["source_capacity_raw"],
    source_container_position=p["source_container_position_raw"],exact_wiki_json=p["exact_wiki_ids_json"],
    source_files=p["source_origin_files"])
   put(c,"v12_tile_proof",obj);a.append(obj)
 assert verified==originals,(len(verified),len(originals),set(verified)^set(originals))
 assert len(w)==474 and all(x["independently_reproduced"] for x in w)
 assert dict(tc)=={"COMPLETE_RECTANGLE":843,"DUPLICATE_POSITION":27,"INCOMPLETE_GRID":14,
  "MISSING_GRID":52,"MULTIPLE_NO_GRID":250,"SINGLE_NO_GRID":2654},tc
 assert dict(wc)=={"DUPLICATE_POSITION":27,"INCOMPLETE_GRID":14,"MISSING_GRID":52,
  "MULTIPLE_NO_GRID":250,"MULTIPLE_EXACT_WIKI_ROWS":125,"MULTIPLE_RAW_CAPACITIES":5,"MULTIPLE_CONTAINER_TYPES":1},wc
 assert len(a)==8219 and len(b)==3840
 original_keys={x["source_key"] for x in query(c,"SELECT source_key FROM v10_tile_reverse")}
 assert len(original_keys)==8219 and {x["source_key"] for x in a}==original_keys
 for x in query(c,"SELECT * FROM v9_wiki_missing_id ORDER BY wiki_id"):
  assert x["automatic_tile_link_count"]==0
  cand=c.execute("SELECT COUNT(*) FROM v9_wiki_missing_id_candidate WHERE wiki_id=?",(x["wiki_id"],)).fetchone()[0]
  put(c,"v12_wiki_unlinked_proof",dict(wiki_id=x["wiki_id"],wiki_name=x["wiki_name"],
   original_category=x["record_class"],sibling_keys=x["sibling_exact_sprite_keys"],
   name_candidate_count=x["source_name_candidates"],source_candidate_rows=cand))
 for x in query(c,"SELECT * FROM v9_v8_image_review_reference ORDER BY source_group_id"):
  assert x["runtime_identity_verified"]==0 and x["direct_image_review_record"]==1
  put(c,"v12_129_visual_reference",dict(group_id=x["source_group_id"],
   review_version=x["visual_review_version"],evidence_type="IMAGE_REVIEW_REFERENCE_NOT_GAME_IDENTITY"))
 put(c,"v12_work_107_scope",dict(scope_key="WORK_STORAGE_SOURCE_UNLINKED_2026_11_04",
  reported_groups=107,reported_tiles=574,saved_individual_review_rows_verified=0,
  individual_reviews_imported=0,evidence_status="WORK_CONVERSATION_ONLY_NO_ROW_LEVEL_DB_EVIDENCE"))
 c.commit()
 assert c.execute("PRAGMA integrity_check").fetchone()[0]=="ok"
 assert not c.execute("PRAGMA foreign_key_check").fetchall()
 for table,num in {**baseline,"v12_tile_proof":8219,"v12_template_proof":3840,
  "v12_warning_proof":474,"v12_wiki_unlinked_proof":11,
  "v12_129_visual_reference":129,"v12_work_107_scope":1}.items():
  assert n(c,table)==num,(table,n(c,table),num)
 for table in ("future_item_distribution","future_map_placement","future_minecraft_implementation"):
  assert n(c,table)==0
 test={x["source_key"].split("/")[-1]:(x["relative_x_when_available"],x["relative_y_when_available"])
       for x in a if x["group_id"]=="FUR-000429796F297C17" and x["Facing"]=="E"}
 assert test=={"40":(0,1),"41":(1,1),"42":(0,0),"43":(1,0)},test
 csvout("V12_8219_TILE_SOURCE_PROOF.csv",a)
 csvout("V12_3840_DIRECTION_GEOMETRY_AUDIT.csv",b)
 csvout("V12_474_ORIGINAL_WARNING_PROOFS.csv",w)
 csvout("V12_11_UNLINKED_WIKI_PRESERVED.csv",query(c,"SELECT * FROM v12_wiki_unlinked_proof ORDER BY wiki_id"))
 csvout("V12_129_VISUAL_REFERENCE_PRESERVED.csv",query(c,"SELECT * FROM v12_129_visual_reference ORDER BY group_id"))
 csvout("V12_WORK_107_GROUPS_574_TILES_NOT_CONFIRMED_SAVED.csv",query(c,"SELECT * FROM v12_work_107_scope"))
 manifest=dict(version="v12",input_v11_PR=293,input_sha256=source_sha,
  source_properties=195265,source_slots=73644,source_tiles=8219,source_edges=14195,
  directional_candidates=3840,reproduced_warnings=474,warning_types=dict(wc),
  status_counts=dict(tc),unlinked_wiki_preserved=11,image_review_reference_groups=129,
  work_reported_groups=107,work_reported_tiles=574,work_individual_reviews_imported=0,
  game_object_identity_certified=0,lua_loot_imported=False,minecraft_implementation_selected=False,
  sqlite_integrity="ok",zip_crc="ok")
 (OUT/"MANIFEST.json").write_text(json.dumps(manifest,indent=2,ensure_ascii=False,sort_keys=True)+"\n",encoding="utf8")
 (OUT/"README_KO.md").write_text(
  "# B42 가구 원본 근거 검증 v12\n\n"
  "v11 SQLite를 복제하여 기존 테이블을 변경하거나 삭제하지 않고 6개의 v12 증거 테이블을 추가함.\n\n"
  "* v11 원본 경고 474건: 각 타일 원본 SpriteGridPos/Facing/Wiki 앵커/수납 원문으로 독립 재계산했으며 모두 동일. 경고는 미해결 상태 유지.\n"
  "* 8,219개 source_key와 좌표는 원본 타일별로 연결. 각각 정렬한 ID/좌표 목록 zip 금지. 좌표가 일부라도 존재하면 해당 좌표의 상대 위치를 보존, 가구 동일성은 확정하지 않음.\n"
  "* 직사각형 843, 방향별 후보 3,840은 실제 게임 가구 종류 확정이 아님.\n"
  "* 위키 미연결 11건 새 타일 연결 0. 이름만 같은 그룹 병합 0.\n"
  "* 129개 이미지 검수 참조는 DB에 저장된 검수 범위 기록. 게임 오브젝트 인증 아님.\n"
  "* Work 107그룹/574타일은 이미지 열람 보고만 확인; 개별 타일 리뷰의 GitHub/SQLite 저장 증거 부재로 IMPORT=0. 가짜 리뷰행을 생성하지 않음.\n"
  "* 원본 수납 값은 타일별 보존, 용량 합산 없음. Lua loot/TMX 인스턴스/Minecraft 구현 미선택.\n",encoding="utf8")
 c.close()
 assert hashlib.sha256(SRC.read_bytes()).hexdigest()==source_sha
 with zipfile.ZipFile(PACK,"w",zipfile.ZIP_DEFLATED,compresslevel=5) as z:
  for x in sorted(OUT.iterdir()):
   if x.is_file() and x!=PACK:z.write(x,x.name)
 with zipfile.ZipFile(PACK) as z:assert z.testzip() is None and DB.name in z.namelist()
 print("V12_FURNITURE_SOURCE_PROOF_SUCCESS",j(manifest),flush=True)
if __name__=="__main__":main()
