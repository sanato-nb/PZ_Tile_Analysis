#!/usr/bin/env python3
"""B42 source-first reverse index: TileSet/LocalID -> candidate furniture & raw function.

No extra image review; no unverified game-object identity or item/MC decisions.
"""
import csv,json,sqlite3,shutil,zipfile
from pathlib import Path
from collections import defaultdict,Counter
R=Path(__file__).resolve().parents[1]
SOURCE=R/"analysis/furniture_full_b42/2026-11-04/definition_first_v9/B42_FURNITURE_DEFINITION_FIRST_V9.zip"
O=R/"analysis/furniture_full_b42/2026-11-04/tile_reverse_index_v10"
DB=O/"B42_FURNITURE_REVERSE_INDEX_V10.sqlite"
ZIP=O/"B42_FURNITURE_REVERSE_INDEX_V10.zip"
DIRECT="EXACT_WIKI_IMAGE_SPRITE_KEY"
EXPAND="SAME_TILEDEF_NAME_STYLE_SOURCE_GROUP_UNCONFIRMED"
ONLY="SOURCE_ONLY_TILEDEF_GROUP"
def q(c,s):return [dict(row) for row in c.execute(s)]
def count(c,t):return c.execute("SELECT COUNT(*) FROM "+t).fetchone()[0]
def js(s):return json.dumps(s,ensure_ascii=False,sort_keys=True)
def uniq(s):return sorted(set(v for v in s if v not in (None,"")))
def ins(c,table,obj):
 keys=list(obj);c.execute("INSERT INTO "+table+"("+",".join(keys)+") VALUES("+",".join("?" for _ in keys)+")",[obj[k] for k in keys])
def write(name,rr):
 assert rr,name
 with (O/name).open("w",encoding="utf-8-sig",newline="") as f:
  w=csv.DictWriter(f,list(rr[0]),extrasaction="ignore");w.writeheader();w.writerows(rr)
def main():
 assert SOURCE.is_file() and not O.exists()
 O.mkdir(parents=True)
 with zipfile.ZipFile(SOURCE) as z:
  assert z.testzip() is None
  with z.open("B42_FURNITURE_DEFINITION_FIRST_V9.sqlite") as s,DB.open("wb") as dst:shutil.copyfileobj(s,dst)
 c=sqlite3.connect(DB);c.row_factory=sqlite3.Row
 assert c.execute("PRAGMA integrity_check").fetchone()[0]=="ok"
 for t,n in {"registry_entry":2231,"wiki_furniture":1268,"furniture_tile":8219,
             "registry_entry_tile":14195,"registry_entry_container":1855,
             "source_attributes":195265,"source_slots":73644,
             "v9_entry_evidence":2231}.items():assert count(c,t)==n,(t,count(c,t),n)
 c.executescript("""
 CREATE TABLE v10_tile_reverse (
  source_key TEXT PRIMARY KEY, tileset TEXT, local_id INTEGER, source_group_id TEXT,
  CustomName_raw TEXT, GroupName_raw TEXT, Facing_raw TEXT, SpriteGridPos_raw TEXT,
  IsoType_raw TEXT, materials_raw TEXT, CustomItem_raw TEXT,
  container_raw TEXT, ContainerCapacity_raw TEXT, ContainerPosition_raw TEXT,
  direct_wiki_entries_json TEXT NOT NULL, unverified_wiki_entries_json TEXT NOT NULL,
  source_only_entries_json TEXT NOT NULL, anchor_status TEXT NOT NULL,
  original_source_files TEXT NOT NULL, same_game_object_verified INTEGER NOT NULL DEFAULT 0);
 CREATE TABLE v10_reverse_edge (
  source_key TEXT NOT NULL, entry_id TEXT NOT NULL, original_evidence TEXT NOT NULL,
  direct_wiki_image_id INTEGER NOT NULL, is_inferred_name_expansion INTEGER NOT NULL,
  game_object_identity_verified INTEGER NOT NULL DEFAULT 0,PRIMARY KEY(source_key,entry_id));
 CREATE TABLE v10_group_direction_candidate(
  group_id TEXT NOT NULL, Facing TEXT NOT NULL, sprite_keys_raw TEXT,
  sprite_grid_positions_raw TEXT, source_parts INTEGER,
  source_grid_width INTEGER,source_grid_height INTEGER,assembly_status TEXT,
  direct_wiki_anchor_ids_json TEXT NOT NULL,
  same_game_object_verified INTEGER NOT NULL DEFAULT 0,PRIMARY KEY(group_id,Facing));
 CREATE TABLE v10_group_function_summary(
  group_id TEXT PRIMARY KEY, tileset TEXT, original_CustomName TEXT,
  original_GroupName TEXT,source_tile_count INTEGER NOT NULL,
  container_types_json TEXT NOT NULL, capacity_values_json TEXT NOT NULL,
  Facing_values_json TEXT NOT NULL, capacity_consistency TEXT NOT NULL,
  same_game_object_verified INTEGER NOT NULL DEFAULT 0);
 CREATE TABLE v10_lookup_issues(
  source_key TEXT NOT NULL,issue_code TEXT NOT NULL,description TEXT NOT NULL,
  runtime_identity_confirmed INTEGER NOT NULL DEFAULT 0,
  PRIMARY KEY(source_key,issue_code));
 CREATE INDEX v10_lookup_anchor ON v10_tile_reverse(anchor_status);
 CREATE INDEX v10_lookup_container ON v10_tile_reverse(container_raw);
 CREATE INDEX v10_lookup_facing ON v10_tile_reverse(Facing_raw);
 CREATE INDEX v10_reverse_entry ON v10_reverse_edge(entry_id);
 CREATE INDEX v10_grid_group ON v10_group_direction_candidate(group_id);
 """)
 tiles=q(c,"SELECT * FROM furniture_tile ORDER BY source_key")
 edges=q(c,"SELECT * FROM registry_entry_tile ORDER BY source_key,entry_id")
 groups={x["group_id"]:x for x in q(c,"SELECT * FROM furniture_group")}
 item={x["entry_id"]:x for x in q(c,"SELECT * FROM registry_entry")}
 sourced={x["source_key"]:x for x in q(c,"SELECT * FROM furniture_container_source")}
 bytile=defaultdict(list);bygroup=defaultdict(list);anchors=defaultdict(set)
 links=[];linkstats=Counter()
 for e in edges:
  k=e["source_key"];ev=e["evidence"];eid=e["entry_id"]
  assert ev in (DIRECT,EXPAND,ONLY) and eid in item
  bytile[k].append(e);bygroup[e["source_group_id"]].append(e)
  kind="EXACT_WIKI_SPRITE" if ev==DIRECT else "UNVERIFIED_NAME_GROUP" if ev==EXPAND else "SOURCE_ONLY_TILEDEF"
  if ev==DIRECT:anchors[e["source_group_id"]].add(eid)
  ins(c,"v10_reverse_edge",dict(source_key=k,entry_id=eid,original_evidence=ev,
    direct_wiki_image_id=int(ev==DIRECT),is_inferred_name_expansion=int(ev==EXPAND)))
  links.append(dict(source_key=k,entry_id=eid,original_name=item[eid]["display_name"],
    evidence_class=kind,source_evidence=ev,game_identity_verified="NO"))
  linkstats[kind]+=1
 source=[];status=Counter();issues=[];flags=Counter()
 def issue(k,code,desc):
  ins(c,"v10_lookup_issues",dict(source_key=k,issue_code=code,description=desc))
  issues.append(dict(source_key=k,issue=code,description=desc));flags[code]+=1
 for t in tiles:
  k=t["source_key"];lst=bytile[k]
  direct=uniq(e["entry_id"] for e in lst if e["evidence"]==DIRECT)
  inferred=uniq(e["entry_id"] for e in lst if e["evidence"]==EXPAND)
  only=uniq(e["entry_id"] for e in lst if e["evidence"]==ONLY)
  if len(direct)>1:state="MULTIPLE_EXACT_WIKI_ROW_ALIASES"
  elif direct:state="ONE_EXACT_WIKI_ROW_ANCHOR"
  elif inferred:state="ONLY_UNVERIFIED_NAME_GROUP_CANDIDATES"
  elif only:state="SOURCE_ONLY_TILEDEF"
  else:state="NO_REGISTRY_LINK"
  status[state]+=1
  con=sourced.get(k,{})
  container=t["container_type"] or con.get("container_type") or ""
  capacity=t["ContainerCapacity"] or con.get("capacity_raw") or ""
  pos=con.get("position_raw") or ""
  obj=dict(source_key=k,tileset=t["tileset"],local_id=t["local_id"],
   source_group_id=t["group_id"],CustomName_raw=t["CustomName"],
   GroupName_raw=t["GroupName"],Facing_raw=t["Facing"],
   SpriteGridPos_raw=t["SpriteGridPos"],IsoType_raw=t["IsoType"],
   materials_raw=t["materials"],CustomItem_raw=t["CustomItem"],
   container_raw=container,ContainerCapacity_raw=capacity,ContainerPosition_raw=pos,
   direct_wiki_entries_json=js(direct),unverified_wiki_entries_json=js(inferred),
   source_only_entries_json=js(only),anchor_status=state,
   original_source_files=t["original_source_files"])
  ins(c,"v10_tile_reverse",obj)
  source.append(dict(source_key=k,tileset=t["tileset"],local_id=t["local_id"],
   source_group_id=t["group_id"],CustomName=t["CustomName"] or "",
   GroupName=t["GroupName"] or "",Facing=t["Facing"] or "",
   SpriteGridPos=t["SpriteGridPos"] or "",IsoType=t["IsoType"] or "",
   materials_raw=t["materials"] or "",CustomItem_raw=t["CustomItem"] or "",
   container=container,ContainerCapacity_raw=capacity,ContainerPosition_raw=pos,
   exact_wiki_entry_ids="|".join(direct),
   unverified_name_group_wiki_ids="|".join(inferred),
   original_tiledef_only_entry_ids="|".join(only),
   source_to_wiki_resolution=state,game_object_identity_verified="NO"))
  if len(direct)>1:issue(k,"AMBIGUOUS_MULTIPLE_WIKI_ROWS","Exact source sprite belongs to more than one Wiki row")
  if inferred:issue(k,"UNVERIFIED_SAME_NAME_EXPANSION","Named TileDef group is not evidence of same game furniture")
  if container and not direct:issue(k,"CONTAINER_WITHOUT_DIRECT_WIKI_ID","Original container property exists without exact Wiki image ID")
 geometry=[];geomstats=Counter()
 for p in q(c,"SELECT * FROM furniture_direction_parts ORDER BY group_id,facing"):
  gid=p["group_id"];wids=sorted(anchors[gid])
  ins(c,"v10_group_direction_candidate",dict(group_id=gid,Facing=p["facing"],
   sprite_keys_raw=p["sprite_ids"],sprite_grid_positions_raw=p["source_grid_positions"],
   source_parts=p["parts"],source_grid_width=p["grid_width"],source_grid_height=p["grid_height"],
   assembly_status=p["assembly_status"],direct_wiki_anchor_ids_json=js(wids)))
  geometry.append(dict(source_group_id=gid,original_tileset=groups[gid]["tileset"],
   source_CustomName=groups[gid]["custom_name"] or "",
   source_GroupName=groups[gid]["group_name"] or "",Facing=p["facing"],
   raw_sprite_keys=p["sprite_ids"],SpriteGridPos_raw=p["source_grid_positions"] or "",
   parts=p["parts"] or "",grid_width=p["grid_width"] or "",
   grid_height=p["grid_height"] or "",source_assembly_status=p["assembly_status"],
   direct_wiki_anchor_ids="|".join(wids),same_game_object_verified="NO"))
  geomstats[p["assembly_status"] or "NULL"]+=1
 grouped=defaultdict(list)
 for t in tiles:grouped[t["group_id"]].append(t)
 funcs=[];capstats=Counter()
 for gid,g in sorted(groups.items()):
  if g["grouping_basis"]=="WIKI_ONLY_NO_MAPPED_TILE":continue
  part=grouped[gid];types=uniq(x["container_type"] for x in part)
  caps=uniq(x["ContainerCapacity"] for x in part)
  directions=uniq(x["Facing"] for x in part)
  consist="DIFFERING_RAW_CAPACITY" if len(caps)>1 else "ONE_RAW_CAPACITY" if caps else "NOT_SPECIFIED"
  capstats[consist]+=1
  ins(c,"v10_group_function_summary",dict(group_id=gid,tileset=g["tileset"],
   original_CustomName=g["custom_name"],original_GroupName=g["group_name"],
   source_tile_count=len(part),container_types_json=js(types),
   capacity_values_json=js(caps),Facing_values_json=js(directions),
   capacity_consistency=consist))
  funcs.append(dict(source_group_id=gid,tileset=g["tileset"],
   CustomName=g["custom_name"] or "",GroupName=g["group_name"] or "",
   original_sprite_count=len(part),original_container_types="|".join(types),
   capacity_values_NOT_SUMMED="|".join(caps),
   original_Facing_values="|".join(directions),
   source_capacity_consistency=consist,game_object_identity_verified="NO"))
 c.commit()
 assert c.execute("PRAGMA integrity_check").fetchone()[0]=="ok"
 for t,n in {"v10_tile_reverse":8219,"v10_reverse_edge":14195,"source_attributes":195265,
             "source_slots":73644,"registry_entry":2231,"wiki_furniture":1268,
             "v9_container_evidence":1855,"v10_group_function_summary":1852}.items():
  assert count(c,t)==n,(t,count(c,t),n)
 assert count(c,"v10_group_direction_candidate")==len(geometry)
 assert sum(status.values())==8219 and sum(linkstats.values())==14195
 assert c.execute("SELECT COUNT(*) FROM v10_tile_reverse WHERE same_game_object_verified!=0").fetchone()[0]==0
 for t in ("future_item_distribution","future_map_placement","future_minecraft_implementation"):
  assert count(c,t)==0
 write("V10_ALL_8219_TILE_TO_FURNITURE.csv",source)
 write("V10_ALL_14195_TILE_LINK_EVIDENCE.csv",links)
 write("V10_DIRECTION_MULTITILE_SOURCE_CANDIDATES.csv",geometry)
 write("V10_ALL_1852_SOURCE_GROUP_FUNCTIONS.csv",funcs)
 write("V10_LOOKUP_ISSUES.csv",issues)
 m=dict(original_wiki_rows=1268,original_registry_records=2231,
  unique_source_sprite_keys=8219,reverse_index_rows=count(c,"v10_tile_reverse"),
  reverse_evidence_edges=count(c,"v10_reverse_edge"),
  direction_candidate_rows=len(geometry),
  source_group_function_rows=count(c,"v10_group_function_summary"),
  source_attribute_records_preserved=195265,source_slots_preserved=73644,
  original_container_edges_preserved=1855,
  reverse_index_classes=dict(sorted(status.items())),
  reverse_evidence_classes=dict(sorted(linkstats.items())),
  original_assembly_classes=dict(sorted(geomstats.items())),
  capacity_consistency_classes=dict(sorted(capstats.items())),
  lookup_review_flags=dict(sorted(flags.items())),
  lookup_review_rows=count(c,"v10_lookup_issues"),
  new_game_object_identity_certified=0,created_minecraft_placements=0,
  lua_loot_rules_imported=0,minecraft_block_entity_decided=False,
  original_source_changed=False,sqlite_integrity="ok")
 (O/"MANIFEST.json").write_text(js(m)+"\n",encoding="utf8")
 (O/"README_KO.md").write_text(
 "# B42 가구 원장 v10 — 타일 ID에서 가구를 찾는 원본 역조회 색인\n\n"
 "원본 TileDef와 위키 ID의 연결만 재구성해 이미지를 추가 검수하지 않고 TMX에서 바로 사용할 역방향 인덱스를 만들었어.\n\n"
 "핵심 SQLite 조회: SELECT * FROM v10_tile_reverse WHERE source_key='furniture_shelving_01/24';\n\n"
 "v10_tile_reverse는 정확한 위키 이미지 ID / 같은 이름에 따른 미확정 확장 / 위키에 없는 원본 타일을 별도로 기록해. "
 "v10_reverse_edge는 원본 타일 14,195개 연결의 증거를 하나씩 추적해.\n\n"
 "v10_group_direction_candidate는 원본 Facing과 SpriteGridPos 및 조립 후보를 보존해. "
 "v10_group_function_summary는 1,852 원본 그룹의 컨테이너 종류 및 서로 다른 원본 용량을 보존하며 용량을 합산하지 않아.\n\n"
 "v10_lookup_issues에는 여러 위키 항목을 가리키는 원본 타일과 같은 이름 확장 후보, "
 "위키 직접 ID가 없는 수납 타일을 따로 표시했어.\n\n"
 "주의: 하나의 정확한 위키 이미지 ID가 연결되어도 게임의 Moveable Object identity가 확정된 것은 아니야. "
 "아이템 생성 Lua, 방별 loot, TMX의 실제 객체 인스턴스 및 마크 구현 방식은 여전히 미설정이야.\n",
 encoding="utf8")
 c.close()
 with zipfile.ZipFile(ZIP,"w",zipfile.ZIP_DEFLATED,compresslevel=5) as z:
  for x in sorted(O.iterdir()):
   if x.is_file() and x!=ZIP:z.write(x,x.name)
 with zipfile.ZipFile(ZIP) as z:
  assert z.testzip() is None and DB.name in z.namelist()
 print("B42_FURNITURE_V10_SOURCE_REVERSE_OK",js(m),flush=True)
if __name__=="__main__":main()
