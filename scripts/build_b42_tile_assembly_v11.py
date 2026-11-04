#!/usr/bin/env python3
"""B42 v11: map each original source sprite ID to its own SpriteGridPos.
Never zip independently sorted v10 sprite-id and grid-position columns.
No PNG review, automatic game-object merge, Lua or Minecraft decisions.
"""
import csv,json,sqlite3,shutil,zipfile,re
from pathlib import Path
from collections import Counter
R=Path(__file__).resolve().parents[1]
SRC=R/"analysis/furniture_full_b42/2026-11-04/tile_reverse_index_v10/B42_FURNITURE_REVERSE_INDEX_V10.zip"
OUT=R/"analysis/furniture_full_b42/2026-11-04/exact_assembly_v11"
DB=OUT/"B42_EXACT_TILE_GRID_ASSEMBLY_V11.sqlite"
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
 assert not OUT.exists(),"No overwrite of evidence snapshots"
 OUT.mkdir(parents=True)
 with zipfile.ZipFile(SRC) as z:
  assert z.testzip() is None
  with z.open("B42_FURNITURE_REVERSE_INDEX_V10.sqlite") as a, DB.open("wb") as b:
   shutil.copyfileobj(a,b)
 c=sqlite3.connect(DB);c.row_factory=sqlite3.Row
 assert c.execute("PRAGMA integrity_check").fetchone()[0]=="ok"
 for t,expected in [("source_slots",73644),("source_attributes",195265),
  ("furniture_tile",8219),("wiki_furniture",1268),("registry_entry",2231),
  ("v10_tile_reverse",8219),("v10_group_direction_candidate",3840)]:
  assert n(c,t)==expected,(t,n(c,t),expected)
 c.executescript("""
 CREATE TABLE v11_direction_template(
  group_id TEXT NOT NULL,Facing TEXT NOT NULL,
  original_assembly_status TEXT,rechecked_grid_status TEXT NOT NULL,
  raw_sprite_count INTEGER NOT NULL,grid_min_x INTEGER,grid_min_y INTEGER,
  grid_width INTEGER,grid_height INTEGER,occupied_grid_cells INTEGER,
  wiki_exact_anchor_ids_json TEXT NOT NULL,
  original_container_types_json TEXT NOT NULL,original_capacity_values_json TEXT NOT NULL,
  source_game_object_identity_verified INTEGER NOT NULL DEFAULT 0,
  PRIMARY KEY(group_id,Facing));
 CREATE TABLE v11_tile_position(
  group_id TEXT NOT NULL,Facing TEXT NOT NULL,source_key TEXT NOT NULL,
  source_grid_pos_raw TEXT,raw_x INTEGER,raw_y INTEGER,
  relative_x INTEGER,relative_y INTEGER,
  source_facing_raw TEXT,source_container TEXT,source_capacity_raw TEXT,
  source_container_position_raw TEXT,exact_wiki_ids_json TEXT NOT NULL,
  source_origin_files TEXT NOT NULL,
  PRIMARY KEY(group_id,Facing,source_key));
 CREATE TABLE v11_source_warning(
  group_id TEXT NOT NULL,Facing TEXT NOT NULL,warning_code TEXT NOT NULL,
  description TEXT NOT NULL,PRIMARY KEY(group_id,Facing,warning_code));
 CREATE INDEX v11_tile_id_lookup ON v11_tile_position(source_key);
 CREATE INDEX v11_template_status ON v11_direction_template(rechecked_grid_status);
 """)
 tiles={x["source_key"]:x for x in query(c,"SELECT * FROM v10_tile_reverse")}
 records=query(c,"SELECT * FROM v10_group_direction_candidate ORDER BY group_id,Facing")
 summaries=[];pieces=[];warnings=[];totals=Counter();flags=Counter()
 oldmap={"RECTANGULAR_GRID_CANDIDATE":"COMPLETE_RECTANGLE",
  "INCOMPLETE_GRID_REVIEW":"INCOMPLETE_GRID",
  "DUPLICATE_GRID_POSITION_REVIEW":"DUPLICATE_POSITION",
  "MIXED_GRID_AND_NO_GRID_REVIEW":"MISSING_GRID",
  "MULTIPLE_SPRITES_SAME_FACING_NO_GRID_REVIEW":"MULTIPLE_NO_GRID",
  "SINGLE_SPRITE":"SINGLE_NO_GRID"}
 def warning(g,f,code,description):
  put(c,"v11_source_warning",dict(group_id=g,Facing=f,warning_code=code,description=description))
  warnings.append(dict(group_id=g,Facing=f,issue=code,reason=description))
  flags[code]+=1
 for r in records:
  g=r["group_id"];f=r["Facing"];keys=split(r["sprite_keys_raw"])
  assert keys and len(keys)==len(set(keys)) and len(keys)==r["source_parts"],(g,f)
  parts=[tiles[x] for x in keys]
  assert all(x["source_group_id"]==g for x in parts),(g,f)
  coords=[xy(x["SpriteGridPos_raw"]) for x in parts]
  valid=[x for x in coords if x is not None]
  minx=miny=wid=hei=None
  if not valid:
   status="SINGLE_NO_GRID" if len(parts)==1 else "MULTIPLE_NO_GRID"
  elif len(valid)<len(coords):status="MISSING_GRID"
  elif len(set(valid))<len(valid):status="DUPLICATE_POSITION"
  else:
   minx=min(x[0] for x in valid);miny=min(x[1] for x in valid)
   wid=max(x[0] for x in valid)-minx+1
   hei=max(x[1] for x in valid)-miny+1
   status="COMPLETE_RECTANGLE" if wid*hei==len(valid) else "INCOMPLETE_GRID"
  totals[status]+=1
  if status!=oldmap.get(r["assembly_status"]):
   warning(g,f,"RECHECK_DIFFERS_FROM_V10",str(r["assembly_status"])+" -> "+status)
  if status in ("MISSING_GRID","DUPLICATE_POSITION","INCOMPLETE_GRID","MULTIPLE_NO_GRID"):
   warning(g,f,status,"Raw SpriteGridPos does not provide a unique complete rectangle")
  for x in parts:
   facing_values=split(x["Facing_raw"])
   match=(f in facing_values) if f!="(not set)" else not facing_values
   if not match:warning(g,f,"FACING_CONFLICT","At least one TileDef sprite disagrees with candidate facing")
  direct=uniq(w for x in parts for w in json.loads(x["direct_wiki_entries_json"]))
  cont=uniq(x["container_raw"] for x in parts)
  caps=uniq(x["ContainerCapacity_raw"] for x in parts)
  if len(caps)>1:warning(g,f,"MULTIPLE_RAW_CAPACITIES","|".join(caps))
  if len(cont)>1:warning(g,f,"MULTIPLE_CONTAINER_TYPES","|".join(cont))
  if len(direct)>1:warning(g,f,"MULTIPLE_EXACT_WIKI_ROWS","|".join(direct))
  put(c,"v11_direction_template",dict(group_id=g,Facing=f,
    original_assembly_status=r["assembly_status"],rechecked_grid_status=status,
    raw_sprite_count=len(parts),grid_min_x=minx,grid_min_y=miny,
    grid_width=wid,grid_height=hei,occupied_grid_cells=len(valid),
    wiki_exact_anchor_ids_json=j(direct),
    original_container_types_json=j(cont),original_capacity_values_json=j(caps)))
  summaries.append(dict(group_id=g,Facing=f,
    source_keys="|".join(keys),source_status=r["assembly_status"],
    rechecked_status=status,parts=len(parts),
    grid_width=wid if wid is not None else "",grid_height=hei if hei is not None else "",
    source_wiki_exact_anchors="|".join(direct),source_container_types="|".join(cont),
    source_capacity_values_NOT_SUMMED="|".join(caps),
    same_game_furniture_verified="NO"))
  for x,point in zip(parts,coords):
   k=x["source_key"]
   dx=point[0]-minx if point is not None and minx is not None else None
   dy=point[1]-miny if point is not None and miny is not None else None
   put(c,"v11_tile_position",dict(group_id=g,Facing=f,source_key=k,
    source_grid_pos_raw=x["SpriteGridPos_raw"],raw_x=point[0] if point else None,
    raw_y=point[1] if point else None,relative_x=dx,relative_y=dy,
    source_facing_raw=x["Facing_raw"],source_container=x["container_raw"],
    source_capacity_raw=x["ContainerCapacity_raw"],
    source_container_position_raw=x["ContainerPosition_raw"],
    exact_wiki_ids_json=x["direct_wiki_entries_json"],
    source_origin_files=x["original_source_files"]))
   pieces.append(dict(group_id=g,Facing=f,source_key=k,
    original_SpriteGridPos=x["SpriteGridPos_raw"] or "",
    absolute_grid_x=point[0] if point else "",
    absolute_grid_y=point[1] if point else "",
    relative_grid_x=dx if dx is not None else "",
    relative_grid_y=dy if dy is not None else "",
    source_Facing=x["Facing_raw"] or "",source_container=x["container_raw"] or "",
    source_ContainerCapacity=x["ContainerCapacity_raw"] or "",
    source_ContainerPosition=x["ContainerPosition_raw"] or "",
    exact_wiki_image_anchors="|".join(json.loads(x["direct_wiki_entries_json"])),
    original_source_files=x["original_source_files"],
    game_object_identity_verified="NO"))
 assert len(summaries)==3840
 assert totals["COMPLETE_RECTANGLE"]==843,totals
 assert len({x["source_key"] for x in pieces})==8219
 c.commit()
 assert c.execute("PRAGMA integrity_check").fetchone()[0]=="ok"
 for t,k in [("v11_direction_template",3840),("v11_tile_position",len(pieces)),
             ("v11_source_warning",len(warnings)),("source_attributes",195265),
             ("source_slots",73644),("registry_entry",2231),
             ("v10_reverse_edge",14195)]:
  assert n(c,t)==k,(t,n(c,t),k)
 for t in ("future_item_distribution","future_map_placement","future_minecraft_implementation"):
  assert n(c,t)==0
 csvout("V11_3840_SOURCE_DIRECTION_TEMPLATES.csv",summaries)
 csvout("V11_ORIGINAL_TILE_ID_GRID_OFFSET_MAPPING.csv",pieces)
 csvout("V11_843_RECTANGLE_SOURCE_TEMPLATES.csv",
  [x for x in summaries if x["rechecked_status"]=="COMPLETE_RECTANGLE"])
 if warnings:csvout("V11_SOURCE_ASSEMBLY_REVIEW_QUEUE.csv",warnings)
 manifest=dict(original_source_tile_keys=8219,source_direction_templates=3840,
  tile_to_position_rows=len(pieces),
  complete_rectangular_source_templates=843,
  source_status_counts=dict(sorted(totals.items())),
  warning_counts=dict(sorted(flags.items())),warnings=len(warnings),
  original_source_attribute_rows_preserved=195265,
  original_source_slots_preserved=73644,
  original_wiki_rows_preserved=1268,registry_entries_preserved=2231,
  actual_PZ_furniture_identity_certified=0,actual_TMX_placements_created=0,
  minecraft_implementation_decided=False,original_Lua_loot_rules_imported=False,
  original_source_files_changed=False,sqlite_integrity="ok")
 (OUT/"MANIFEST.json").write_text(j(manifest)+"\n",encoding="utf8")
 (OUT/"README_KO.md").write_text(
 "# B42 가구 DB v11 — 원본 SpriteGridPos의 타일별 좌표를 확정적으로 연결\n\n"
 "v10의 sprite ID 목록과 그리드 목록은 각각 정렬되어 있어서 두 목록을 단순 zip으로 엮으면 잘못된 배치가 될 수 있어. v11은 각 원본 타일 행의 SpriteGridPos를 직접 읽어 원본 TileSet/LocalID와 정확하게 연결했어.\n\n"
 "v11_direction_template: 전체 3,840개의 그룹×Facing 조립 후보의 원본 좌표 및 검토 상태.\n\n"
 "v11_tile_position: 각 타일 ID별 원본 SpriteGridPos, 템플릿 내 상대 x/y, 해당 타일의 수납 유형·용량·위치, Wiki 직접 번호.\n\n"
 "v11_source_warning: 중복 좌표, 불완전 격자, 원본 Facing 충돌, 상이한 수납 용량, 여러 위키 앵커.\n\n"
 "원본 격자가 직사각형인 후보 843개가 존재하지만 이것이 843개의 게임 내 가구 개체라는 의미는 아냐. 같은 이름 그룹의 여러 종류/변형과 실제 TMX 배치 확인은 별도 작업이야. 수납 용량은 부품별로 보존하고 합산하지 않았어.\n\n"
 "조회 예시:\n\n"
 "SELECT source_key, relative_x,relative_y,source_container,source_capacity_raw FROM v11_tile_position WHERE group_id='FUR-000429796F297C17' AND Facing='E' ORDER BY relative_y,relative_x;\n\n"
 "원본 파일, 위키 자료, v10 DB를 보존하고 이미지 전수 재검수나 마크 구현 선택은 하지 않았어.\n",encoding="utf8")
 c.close()
 with zipfile.ZipFile(PACK,"w",zipfile.ZIP_DEFLATED,compresslevel=5) as z:
  for x in sorted(OUT.iterdir()):
   if x.is_file() and x!=PACK:z.write(x,x.name)
 with zipfile.ZipFile(PACK) as z:
  assert z.testzip() is None and DB.name in z.namelist()
 print("V11_EXACT_TILE_POSITIONS_SUCCESS",j(manifest),flush=True)
if __name__=="__main__":main()
