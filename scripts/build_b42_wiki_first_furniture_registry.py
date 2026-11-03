#!/usr/bin/env python3
"""Source-first, wiki-anchored B42 furniture registry for later map conversion.

No claims of 1:1 game-object identity or model/block/Entity implementation.
Wiki rows are preserved individually. Source-group expansions are explicitly
distinguished from exact wiki image sprite keys.
"""
from __future__ import annotations
from pathlib import Path
from collections import Counter,defaultdict
import csv,json,sqlite3,zipfile,hashlib,shutil
ROOT=Path(__file__).resolve().parents[1]
OLD=ROOT/"analysis/furniture_full_b42/2026-11-03/PZ_B42_FULL_FURNITURE_DB.zip"
OUT=ROOT/"analysis/furniture_full_b42/2026-11-03/wiki_first_v2"
WIKI=ROOT/"pzwiki_furniture/2026-11-03/furniture_1268.csv"
DB=OUT/"PZ_B42_FURNITURE_REGISTRY_WIKI_FIRST.sqlite"

def readcsv(p):
 with p.open(encoding="utf-8-sig",newline="") as f:return list(csv.DictReader(f))
def writecsv(p,rows):
 if not rows:return
 with p.open("w",encoding="utf-8-sig",newline="") as f:
  w=csv.DictWriter(f,fieldnames=list(rows[0]),extrasaction="ignore")
  w.writeheader();w.writerows(rows)
def unique(items):return sorted(set(str(v) for v in items if v is not None and str(v)!=""))
def joined(items):return "|".join(unique(items))
def loadone(conn,sql):return conn.execute(sql).fetchone()[0]
def iterrows(conn,q,params=()):
 return [dict(r) for r in conn.execute(q,params)]
def detect_scope(g):
 name=(g.get("custom_name") or "").lower()
 group=(g.get("group_name") or "").lower()
 tileset=(g.get("tileset") or "").lower()
 if g["grouping_basis"]=="ONE_UNNAMED_SPRITE_UNVERIFIED":
  return "UNNAMED_SPRITE_CLASSIFICATION_REQUIRED"
 if tileset.startswith(("floors_","walls_","vegetation_","roofs_")):
  return "SURFACE_OR_ENVIRONMENT_TILE_NOT_ASSUMED_FURNITURE"
 if name in ("sign","poster","painting","picture","graffiti","carpet","rug","tile","tiles","wallpaper"):
  return "DECOR_OR_ARCHITECTURAL_OBJECT_REVIEW"
 if name.lower() in ("customname","groupname","none","unknown"):
  return "SUSPECT_SOURCE_NAME_VALUE_REVIEW"
 if g["container_types"]:
  return "SOURCE_CONTAINER_PROPERTY_PRESENT"
 if g["iso_types"] or g["directions"]:
  return "NAMED_PLACED_OBJECT_PROPERTY_PRESENT"
 return "TILEDEF_NAMED_OBJECT_NEEDS_CLASSIFICATION"
def main():
 assert not OUT.exists(),"Refuse overwrite existing registry"
 OUT.mkdir(parents=True)
 assert OLD.exists()
 with zipfile.ZipFile(OLD) as archive:
  assert archive.testzip() is None
  rawname="B42_FURNITURE_ALL_SOURCE.sqlite"
  assert rawname in archive.namelist(),archive.namelist()
  with archive.open(rawname) as src,DB.open("wb") as dest:
   shutil.copyfileobj(src,dest)
 wiki=readcsv(WIKI)
 assert len(wiki)==1268
 con=sqlite3.connect(DB)
 con.row_factory=sqlite3.Row
 assert loadone(con,"PRAGMA integrity_check")=="ok"
 oldcount={k:loadone(con,"SELECT COUNT(*) FROM "+k) for k in
  ("source_slots","source_attributes","image_cells","furniture_group",
   "furniture_tile","wiki_furniture","wiki_group_candidate",
   "furniture_direction_parts","furniture_container_source")}
 assert oldcount["source_slots"]==73644 and oldcount["source_attributes"]==195265
 assert oldcount["wiki_furniture"]==1268 and oldcount["furniture_tile"]==8219
 assert oldcount["furniture_group"]==1863
 assert loadone(con,"SELECT COUNT(*) FROM future_minecraft_implementation")==0

 # Registry entries correspond to PZwiki list rows, NOT unique physical meshes.
 # Source-only groups make otherwise hidden original TileDef data discoverable.
 con.executescript("""
 CREATE TABLE registry_entry(
  entry_id TEXT PRIMARY KEY, source_system TEXT NOT NULL,
  wiki_id TEXT UNIQUE, source_group_id TEXT,
  display_name TEXT NOT NULL,category TEXT,subcategory TEXT,
  original_wiki_row_json TEXT,photo_url TEXT,article_url TEXT,
  wiki_size_raw TEXT,wiki_capacity_raw TEXT,wiki_encumbrance_raw TEXT,
  tile_group_count INTEGER NOT NULL DEFAULT 0,
  direct_sprite_count INTEGER NOT NULL DEFAULT 0,
  expanded_sprite_count INTEGER NOT NULL DEFAULT 0,
  identity_status TEXT NOT NULL,
  spatial_object_identity_verified INTEGER NOT NULL DEFAULT 0,
  minecraft_implementation TEXT NOT NULL DEFAULT 'UNDECIDED'
 );
 CREATE TABLE registry_entry_group(
  entry_id TEXT NOT NULL,source_group_id TEXT NOT NULL,
  role TEXT NOT NULL,other_wiki_rows_sharing_group INTEGER NOT NULL,
  PRIMARY KEY(entry_id,source_group_id)
 );
 CREATE TABLE registry_entry_tile(
  entry_id TEXT NOT NULL,source_group_id TEXT NOT NULL,source_key TEXT NOT NULL,
  evidence TEXT NOT NULL,original_tiledef_source_files TEXT NOT NULL,
  source_sprite_facing TEXT,source_sprite_grid_pos TEXT,
  container_type_raw TEXT,capacity_raw TEXT,
  PRIMARY KEY(entry_id,source_key)
 );
 CREATE TABLE registry_entry_container(
  entry_id TEXT NOT NULL,source_key TEXT NOT NULL,
  container_type TEXT,capacity_raw TEXT,container_position_raw TEXT,
  room_distribution_key TEXT,
  exact_item_contents_known INTEGER NOT NULL DEFAULT 0,
  PRIMARY KEY(entry_id,source_key)
 );
 CREATE TABLE registry_group_conflict(
  source_group_id TEXT PRIMARY KEY,wiki_ids TEXT NOT NULL,
  affected_wiki_entry_count INTEGER NOT NULL,review_kind TEXT NOT NULL
 );
 CREATE TABLE registry_orientation(
  entry_id TEXT NOT NULL,group_id TEXT NOT NULL,facing TEXT NOT NULL,
  sprite_ids TEXT NOT NULL,source_grid_positions TEXT,
  grid_width INTEGER,grid_height INTEGER,assembly_status TEXT NOT NULL,
  game_object_composition_verified INTEGER NOT NULL DEFAULT 0,
  PRIMARY KEY(entry_id,group_id,facing)
 );
 CREATE TABLE registry_review_queue(
  review_id TEXT PRIMARY KEY, entry_id TEXT NOT NULL,
  reason TEXT NOT NULL, evidence TEXT,priority INTEGER NOT NULL DEFAULT 2,
  corrected_object_identity TEXT,manual_verified INTEGER NOT NULL DEFAULT 0
 );
 CREATE TABLE registry_item_rule_source(
  room_type TEXT,container_type TEXT,distribution_id TEXT,
  raw_lua_source_path TEXT,verification_status TEXT NOT NULL
 );
 CREATE INDEX idx_reg_source ON registry_entry(source_system);
 CREATE INDEX idx_reg_display ON registry_entry(display_name);
 CREATE INDEX idx_reg_tile_key ON registry_entry_tile(source_key);
 CREATE INDEX idx_reg_tile_entry ON registry_entry_tile(entry_id);
 CREATE INDEX idx_reg_container_type ON registry_entry_container(container_type);
 CREATE INDEX idx_reg_review_entry ON registry_review_queue(entry_id);
 """)

 groups={x["group_id"]:x for x in iterrows(con,"SELECT * FROM furniture_group")}
 wiki_rows={x["wiki_id"]:x for x in iterrows(con,"SELECT * FROM wiki_furniture")}
 tiles={x["source_key"]:x for x in iterrows(con,"SELECT * FROM furniture_tile")}
 bygrp=defaultdict(list)
 for t in tiles.values():bygrp[t["group_id"]].append(t)
 links=defaultdict(list);grouptowiki=defaultdict(set)
 for t in iterrows(con,"SELECT * FROM wiki_group_candidate"):
  if t["group_id"].startswith("FUR-WIKI-"):continue
  links[t["wiki_id"]].append(t)
  grouptowiki[t["group_id"]].add(t["wiki_id"])
 source_direct=defaultdict(set)
 for r in iterrows(con,"SELECT * FROM wiki_image_tile WHERE matching_status='SOURCE_ID_FOUND'"):
  source_direct[r["wiki_id"]].add(r["source_key"])
 # case-agnostic exact key membership; preserve original case in source table.
 direct_lower={k:set(x.casefold() for x in v) for k,v in source_direct.items()}
 orientations=defaultdict(list)
 for r in iterrows(con,"SELECT * FROM furniture_direction_parts"):
  orientations[r["group_id"]].append(r)
 container=defaultdict(list)
 for r in iterrows(con,"SELECT * FROM furniture_container_source"):
  container[r["group_id"]].append(r)
 categories=Counter()
 allentries=[];alltiles=[];allreview=[];container_export=[];direction_export=[]
 entrycounts=Counter()
 def review(entry,why,evidence="",priority=2):
  qid="REV-"+hashlib.sha256((entry+"|"+why+"|"+evidence).encode("utf8")).hexdigest()[:20].upper()
  con.execute("INSERT OR IGNORE INTO registry_review_queue(review_id,entry_id,reason,evidence,priority) VALUES(?,?,?,?,?)",(qid,entry,why,evidence,priority))
  allreview.append(dict(review_id=qid,entry_id=entry,issue=why,source_evidence=evidence,priority=priority))

 def create(entry_id,source_system,wiki_id,sgid,display,category,subcategory,
            raw,photo,page,size,capacity,weight,group_links):
  direct=direct_lower.get(wiki_id,set()) if wiki_id else set()
  total_direct=total_expand=0
  linked=set()
  group_conflict=False
  for link in group_links:
   gid=link["group_id"]
   if gid.startswith("FUR-WIKI-"):continue
   linked.add(gid)
   multiple=len(grouptowiki.get(gid,()))
   if multiple>1:group_conflict=True
   con.execute("INSERT INTO registry_entry_group VALUES(?,?,?,?)",
    (entry_id,gid,"WIKI_IMAGE_FILENAME_REFERENCES_SOURCE_GROUP" if wiki_id else "TILEDEF_SOURCE_GROUP_UNLISTED",
    max(0,multiple-1)))
   for r in bygrp[gid]:
    if r["source_key"].casefold() in direct:
     evidence="EXACT_WIKI_IMAGE_SPRITE_KEY"
     total_direct+=1
    elif wiki_id:
     evidence="SAME_TILEDEF_NAME_STYLE_SOURCE_GROUP_UNCONFIRMED"
     total_expand+=1
    else:
     evidence="SOURCE_ONLY_TILEDEF_GROUP"
    con.execute("INSERT INTO registry_entry_tile VALUES(?,?,?,?,?,?,?,?,?)",
     (entry_id,gid,r["source_key"],evidence,r["original_source_files"],
      r["Facing"],r["SpriteGridPos"],r["container_type"],r["ContainerCapacity"]))
    alltiles.append(dict(entry_id=entry_id,source_group_id=gid,source_key=r["source_key"],
     evidence=evidence,tileset=r["tileset"],local_id=r["local_id"],
     Facing=r["Facing"],SpriteGridPos=r["SpriteGridPos"],
     container=r["container_type"],ContainerCapacity=r["ContainerCapacity"],
     property_source_files=r["original_source_files"],
     original_all_attributes_table="furniture_tile.raw_properties_with_source_json"))
   for r in container[gid]:
    con.execute("INSERT OR IGNORE INTO registry_entry_container VALUES(?,?,?,?,?,?,?)",
     (entry_id,r["source_key"],r["container_type"],r["capacity_raw"],r["position_raw"],
      None,0))
    container_export.append(dict(entry_id=entry_id,source_key=r["source_key"],
     original_container_type=r["container_type"],original_capacity=r["capacity_raw"],
     original_position=r["position_raw"],item_distribution_rule="NOT_YET_IMPORTED"))
   for r in orientations[gid]:
    con.execute("INSERT INTO registry_orientation VALUES(?,?,?,?,?,?,?,?,?)",
     (entry_id,gid,r["facing"],r["sprite_ids"],r["source_grid_positions"],
      r["grid_width"],r["grid_height"],r["assembly_status"],0))
    direction_export.append(dict(entry_id=entry_id,source_group_id=gid,
     facing=r["facing"],sprite_keys=r["sprite_ids"],
     grid_positions=r["source_grid_positions"],
     source_width=r["grid_width"],source_height=r["grid_height"],
     assembly_status=r["assembly_status"]))
  if source_system=="WIKI":
   if not linked:status="WIKI_LISTED_NO_ID_FROM_IMAGE"
   elif len(linked)>1:status="WIKI_ONE_ROW_REFERENCES_MULTIPLE_SOURCE_GROUPS"
   elif group_conflict:status="MULTIPLE_WIKI_ROWS_REFER_TO_SAME_SOURCE_GROUP"
   elif total_expand:status="WIKI_DIRECT_ID_PLUS_UNVERIFIED_DIRECTION_EXPANSION"
   else:status="WIKI_IMAGE_ID_LINKED_ONLY"
  else:
   status="B42_SOURCE_UNLISTED_"+detect_scope(groups[sgid])
  con.execute("INSERT INTO registry_entry(entry_id,source_system,wiki_id,source_group_id,display_name,category,subcategory,original_wiki_row_json,photo_url,article_url,wiki_size_raw,wiki_capacity_raw,wiki_encumbrance_raw,tile_group_count,direct_sprite_count,expanded_sprite_count,identity_status) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
   (entry_id,source_system,wiki_id,sgid,display,category,subcategory,raw,photo,page,size,capacity,weight,len(linked),total_direct,total_expand,status))
  allentries.append(dict(entry_id=entry_id,source_system=source_system,
   wiki_id=wiki_id or "",group_id=sgid or "",display_name=display,
   category=category or "",subcategory=subcategory or "",
   source_group_count=len(linked),exact_image_sprite_keys=total_direct,
   other_sprite_keys_same_group=total_expand,linked_all_source_sprite_keys=sum(len(bygrp[g]) for g in linked),
   record_status=status,original_wiki_image_url=photo or "",
   wiki_page_url=page or "",raw_wiki_size=size or "",
   raw_wiki_storage_capacity=capacity or "",raw_wiki_encumbrance=weight or "",
   game_object_identity_verified="NO",implementation_kind="UNDECIDED"))
  entrycounts[status]+=1
  categories[category or "(source only)"]+=1
  if source_system=="WIKI":
   if not linked:review(entry_id,"WIKI_IMAGE_NO_PARSEABLE_OR_MATCHING_ORIGINAL_SOURCE_ID",page or "",1)
   if len(linked)>1:review(entry_id,"WIKI_IMAGE_REFERENCES_MULTIPLE_TILEDEF_SOURCE_GROUPS",
       joined(linked),1)
   if group_conflict:review(entry_id,"DIFFERENT_WIKI_FURNITURE_ROWS_SHARE_SAME_TILEDEF_GROUP",
       joined(g for g in linked if len(grouptowiki.get(g,()))>1),1)
   if total_expand:review(entry_id,"SAME_NAME_GROUP_EXPANSION_NEEDS_DIRECTION_PART_VISUAL_VERIFICATION",
       str(total_expand)+" indirectly linked sprites",2)
  else:
   review(entry_id,"SOURCE_ONLY_GROUP_NOT_LISTED_IN_PZWIKI_FURNITURE",
    groups[sgid]["tileset"]+" "+(groups[sgid]["custom_name"] or ""),3)
  if any("REVIEW" in r["assembly_status"] for g in linked for r in orientations[g]):
   review(entry_id,"TILEDEF_DIRECTION_GRID_MISSING_OR_AMBIGUOUS",
      joined(r["assembly_status"] for g in linked for r in orientations[g] if "REVIEW" in r["assembly_status"]),2)
  if any(len(grouptowiki.get(g,()))>1 for g in linked):
   review(entry_id,"SOURCE_NAME_NOT_UNIQUE_DESIGN_PROOF",
       "Original TileDef name+group shared by multiple Wiki rows",2)

 for w in wiki:
  wid=w["목록ID"]
  q=wiki_rows[wid]
  assert q["name"]==w["가구명_원문"]
  create("WIKI:"+wid,"WIKI",wid,None,w["가구명_원문"],w["대분류_원문"],
     w["소분류_원문"],q["source_row_json"],w["이미지_URL"],
     w["개별문서_URL"],w["크기_타일수"],w["수납용량_원문"],
     w["운반부담_Encumbrance"],links.get(wid,[]))

 unlisted=sorted(set(gid for gid,g in groups.items() if not gid.startswith("FUR-WIKI-"))-set(grouptowiki))
 for gid in unlisted:
  g=groups[gid]
  display=(" ".join(x for x in (g["group_name"],g["custom_name"]) if x) or
          ("Unlabeled source sprite "+(g["tileset"] or ""))).strip()
  create("SOURCE:"+gid,"B42_SOURCE_ONLY",None,gid,display,
    "SOURCE_ONLY_UNCLASSIFIED",None,None,None,None,None,None,None,
    [dict(group_id=gid)])
 assert len(grouptowiki)==889,("wiki-referenced source-group count",len(grouptowiki))
 for gid,ids in sorted(grouptowiki.items()):
  if len(ids)>1:
   con.execute("INSERT INTO registry_group_conflict VALUES(?,?,?,?)",
    (gid,joined(ids),len(ids),"MULTIPLE_DISTINCT_WIKI_ROWS_SAME_SOURCE_GROUP_DO_NOT_MERGE"))

 assert len(unlisted)==963,len(unlisted)
 assert len(allentries)==1268+963
 assert len({r["entry_id"] for r in allentries})==len(allentries)
 assert sum(x["source_group_count"] for x in allentries)>=889
 assert all(x["game_object_identity_verified"]=="NO" for x in allentries)
 assert loadone(con,"SELECT COUNT(*) FROM registry_item_rule_source")==0
 assert loadone(con,"SELECT COUNT(*) FROM future_minecraft_implementation")==0
 assert loadone(con,"SELECT COUNT(*) FROM registry_entry WHERE minecraft_implementation!='UNDECIDED'")==0
 assert loadone(con,"SELECT COUNT(*) FROM source_attributes")==195265

 con.commit()
 assert loadone(con,"PRAGMA integrity_check")=="ok"
 counts={name:loadone(con,"SELECT COUNT(*) FROM "+name) for name in
  ("registry_entry","registry_entry_group","registry_entry_tile",
   "registry_entry_container","registry_group_conflict",
   "registry_orientation","registry_review_queue","registry_item_rule_source")}
 direct_wiki=sum(1 for r in allentries if r["source_system"]=="WIKI" and r["exact_image_sprite_keys"]>0)
 wikinone=sum(1 for r in allentries if r["source_system"]=="WIKI" and r["source_group_count"]==0)
 assert direct_wiki==1257 and wikinone==11,(direct_wiki,wikinone)
 manifest=dict(
  wiki_list_rows=1268,source_only_groups=len(unlisted),
  total_registry_entries=len(allentries),wiki_items_with_original_source_id=direct_wiki,
  wiki_items_without_original_source_id=wikinone,
  original_source_groups_linked_to_at_least_one_wiki_row=len(grouptowiki),
  source_original_groups_not_linked_to_wiki=len(unlisted),
  original_tiledef_unique_keys=61418,original_tiledef_property_rows=195265,
  original_furniture_candidate_tile_keys=8219,
  derived_tables=counts,identity_status_counts=dict(sorted(entrycounts.items())),
  original_v1_tables_preserved=oldcount,
  classification_status="WIKI_LISTINGS_CONFIRMED_SOURCE_IMAGE_IDS_ONLY",
  per_tile_original_properties_preserved=True,
  wiki_does_not_cover_every_build_42_furniture=True,
  same_game_object_composition_certified_count=0,
  actual_in_game_loot_rules_loaded=0,
  minecraft_implementation_selected=False,
  no_source_file_overwritten=True,
  sqlite_integrity="ok")
 writecsv(OUT/"WIKI_FIRST_ALL_CATALOG_ENTRIES.csv",allentries)
 writecsv(OUT/"FURNITURE_ENTRY_ALL_LINKED_TILE_IDS.csv",alltiles)
 writecsv(OUT/"FURNITURE_ENTRY_STORAGE_ATTRIBUTES.csv",container_export)
 writecsv(OUT/"FURNITURE_ENTRY_DIRECTION_PARTS.csv",direction_export)
 writecsv(OUT/"FURNITURE_IDENTITY_REVIEW_QUEUE.csv",allreview)
 writecsv(OUT/"WIKI_SOURCE_ONLY_UNLISTED_GROUPS.csv",[e for e in allentries if e["source_system"]=="B42_SOURCE_ONLY"])
 writecsv(OUT/"WIKI_CONFIRMED_LISTINGS.csv",[e for e in allentries if e["source_system"]=="WIKI"])
 (OUT/"MANIFEST.json").write_text(json.dumps(manifest,indent=2,ensure_ascii=False)+"\n",encoding="utf8")
 (OUT/"README_KO.md").write_text("\n\n".join([
  "# B42 전체 가구 원장 v2 — PZwiki 기반 + 원본 TileDef 전체 연결",
  "## 정확한 기록 단위",
  "이 DB는 게임에서 실제로 구분하는 2,231개 고유 가구라고 주장하지 않아. PZwiki 가구 목록의 원문 행 1,268개와, 위키 어떤 행에도 연결되지 않은 B42 원본 TileDef 그룹 963개를 합한 **검증 가능한 목록 항목 2,231개**야.",
  "위키 1,268행 중 1,257행에 대해 이미지 파일명의 원본 타일 ID를 연결했고, 11행은 위키 표에는 존재하지만 이미지 ID가 없어 미연결로 보존. 전체 원본 가구 후보의 1,852개 그룹 중 889개 그룹을 위키와 연결했고 963개는 원본 단독 후보로 남아 있어.",
  "원본 타일의 모든 속성은 동일 SQLite 안의 source_attributes(195,265행)와 furniture_tile.raw_properties_with_source_json에 보존돼. 61,418개 원본 키 전체는 source_slots에서 찾을 수 있어.",
  "## 사실과 추론의 구별",
  "- WIKI 목록에 실린 이름/분류/자료: 위키 원문 출처로 확인됨. Wiki에 있다는 사실을 게임 내 동일한 객체 인증과 혼동하면 안 됨.",
  "- EXACT_WIKI_IMAGE_SPRITE_KEY: 위키 이미지 파일명에 나오는 특정 TileSet/LocalID가 원본 TileDef에 존재함. 원본 타일 ID 문자열 근거는 직접 확인.",
  "- SAME_TILEDEF_NAME_STYLE_SOURCE_GROUP_UNCONFIRMED: 같은 타일셋 CustomName+GroupName인 방향/부품 타일을 추가로 연결한 상태. 동일 물체인지, 별도 변형인지 추가 검토.",
  "- B42_SOURCE_ONLY: 위키 이미지가 연결되지 않은 원본 TileDef의 타일 그룹. 바닥재, 간판, 장식물 등의 비가구가 포함될 수 있으므로 개별 시각 분류 필요.",
  "- WIKI_ONLY_NO_ID_FROM_IMAGE: 위키 원문은 있으나 대응 원본 타일 ID가 없음. 11건을 임의의 타일에 연결하지 않았음.",
  "## 가구 속성 및 아이템 생성",
  "registry_entry_tile로 가구 항목에서 모든 관련 타일의 Facing/SpriteGridPos/원본 출처 파일을 찾을 수 있어. 전체 속성은 furniture_tile 및 source_attributes에서 쿼리 가능.",
  "registry_entry_container에는 타일별 container/ContainerCapacity/ContainerPosition을 기록해. 같은 2칸짜리 책장에 여러 타일이 각각 컨테이너를 갖는 경우 이를 함부로 합치지 않아.",
  "실제 아이템 생성은 방 종류 및 컨테이너 종류의 Lua 규칙이 필요하므로 registry_item_rule_source와 기존 future_item_distribution는 비워둠. 창고에 책이 들어간다고 허위 기록하지 않아.",
  "Minecraft 구현 방식(Block 또는 Entity)은 결정하지 않고 향후 연결 테이블도 비워둠.",
  "## 주요 산출물",
  "- PZ_B42_FURNITURE_REGISTRY_WIKI_FIRST.sqlite: 전체 원본 v259 TileDef/PNG 소스와 v1 관계, Wiki 우선 새 테이블 및 검토 큐를 포함.",
  "- WIKI_FIRST_ALL_CATALOG_ENTRIES.csv: PZwiki 목록+추가 B42 원본 가구 항목, 각각 정확히 한 행.",
  "- WIKI_CONFIRMED_LISTINGS.csv: 위키에 등재된 1,268항목(그중 11항목 원본 타일 ID 미연결).",
  "- WIKI_SOURCE_ONLY_UNLISTED_GROUPS.csv: 위키에 연결되지 않은 963개 B42 원본 그룹(전부 가구로 확정 아님).",
  "- FURNITURE_ENTRY_ALL_LINKED_TILE_IDS.csv: 모든 항목별 원본 타일 ID, 타일별 수납 속성, 정확한 ID와 그룹 확장 연결의 차이.",
  "- FURNITURE_ENTRY_STORAGE_ATTRIBUTES.csv: 가구의 타일별 수납 유형과 용량, 아이템 분포는 미수집.",
  "- FURNITURE_ENTRY_DIRECTION_PARTS.csv: 해당 항목의 출처별 방향·부품 구성 후보.",
  "- FURNITURE_IDENTITY_REVIEW_QUEUE.csv: 같은 그룹을 두 위키 행이 공유할 때 등의 위험과 검토 사유.",
  "## 향후 검증",
  "위키와 소스 타일 ID의 정확한 연결을 유지하면서, 실제 게임 가구로 간주할 정확한 경계와 방향/부품/색상 변형을 검수해야 해. 사용자 목표는 게임에서 정의된 모든 가구/설치물에 대한 DB 완성이며, 이 작업의 원본 가구 후보 선별은 아직 완전성을 인증하지 않아.",
  "원본 정의·위키·이전 DB·이미지·GitHub 브랜치를 덮어쓰지 않고 별도 분석 산출물로 보존."
 ])+"\n",encoding="utf8")
 con.close()
 with zipfile.ZipFile(OUT/"B42_WIKI_FIRST_FURNITURE_REGISTRY.zip","w",zipfile.ZIP_DEFLATED,compresslevel=5) as z:
  for p in sorted(OUT.iterdir()):
   if p.is_file() and p.suffix!=".zip":z.write(p,p.name)
 with zipfile.ZipFile(OUT/"B42_WIKI_FIRST_FURNITURE_REGISTRY.zip") as z:
  assert z.testzip() is None
  assert "PZ_B42_FURNITURE_REGISTRY_WIKI_FIRST.sqlite" in z.namelist()
 print("WIKI_FIRST_REGISTRY_BUILT",json.dumps(manifest,ensure_ascii=False),flush=True)
if __name__=="__main__":main()
