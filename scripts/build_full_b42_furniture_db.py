#!/usr/bin/env python3
"""Full B42 original-furniture source database; no Minecraft implementation choice."""
import csv, json, sqlite3, shutil, hashlib, re, zipfile
from urllib.parse import unquote, urlparse
from pathlib import Path
from collections import defaultdict, Counter

R=Path(__file__).resolve().parents[1]
SRC=R/"analysis/current/v259/PZ_v259_all_png_tile_definitions.sqlite"
W=R/"pzwiki_furniture/2026-11-03/furniture_1268.csv"
RO=R/"analysis/rosewood_furniture/2026-10-31/furniture_identity_catalog_20261103"
OUT=R/"analysis/furniture_full_b42/2026-11-03"
DB=OUT/"B42_FURNITURE_ALL_SOURCE.sqlite"
TAG_KEYS={"CustomName","GroupName","IsMoveAble","container","ContainerCapacity","IsoType",
"bed","BedType","chairN","chairE","chairS","chairW","SpriteGridPos","IsTable",
"GenericCraftingSurface","waterPiped","waterAmount","IsHigh","IsLow","MoveType"}
FUNCTION_KEYS={"container","ContainerCapacity","ContainerPosition","ContainerOpenSound",
"ContainerCloseSound","ContainerPutSound","ContainerTakeSound","IsoType",
"GenericCraftingSurface","waterPiped","waterAmount","waterMaxAmount"}

def rows(p):
 with p.open(encoding="utf-8-sig",newline="") as f:return list(csv.DictReader(f))
def write(p,items):
 if not items:return
 with p.open("w",encoding="utf-8-sig",newline="") as f:
  w=csv.DictWriter(f,list(items[0]));w.writeheader();w.writerows(items)
def uniq(x):return sorted(set(v for v in x if v not in (None,"")))
def joined(x):return "|".join(uniq(x))
def stable(*a):return hashlib.sha256("\x1f".join(map(str,a)).encode("utf8")).hexdigest()[:16].upper()
def pic(u):
 if not u:return [],"NO_IMAGE_URL"
 n=unquote(urlparse(u).path.split("/")[-1])
 m=re.fullmatch(r"(.+?)_(\d+(?:\+\d+)*)\.(?:png|jpg|jpeg|webp)",n,re.I)
 if not m:return [],"NO_PARSEABLE_LOCAL_ID"
 return [(m[1].lower(),int(x)) for x in m[2].split("+")],"PARSED_FILENAME_ID"
def parse_xy(x):
 m=re.fullmatch(r"\s*(-?\d+)\s*,\s*(-?\d+)\s*",x)
 return tuple(map(int,m.groups())) if m else None

def main():
 assert not OUT.exists(),"Refuse overwrite"
 OUT.mkdir(parents=True)
 original_hash=hashlib.sha256(SRC.read_bytes()).hexdigest()
 assert original_hash=="dd3bbf980e92734369456aa0c7226825e940acc6d29156c8c5ab443a40e1408a"
 shutil.copy2(SRC,DB)
 con=sqlite3.connect(DB)
 assert con.execute("PRAGMA integrity_check").fetchone()[0]=="ok"
 counts={t:con.execute("SELECT COUNT(*) FROM "+t).fetchone()[0] for t in
   ("source_slots","source_attributes","image_cells","source_files","source_tilesets","image_atlases")}
 assert counts["source_slots"]==73644 and counts["source_attributes"]==195265
 # All original source tables are preserved in the copied database.
 slots=defaultdict(set)
 for n,i,f in con.execute("SELECT name,local_id,source_file FROM source_slots"):
  slots[(n,i)].add(f)
 assert len(slots)==61418
 prop=defaultdict(lambda:defaultdict(list))
 for n,i,k,v,f in con.execute("SELECT name,local_id,attribute,value,source_file FROM source_attributes"):
  prop[(n,i)][k].append((v,f))
 imgs=defaultdict(list)
 for n,i,p,visible in con.execute("SELECT tileset,local_id,png_path,has_visible_pixels FROM image_cells WHERE tileset IS NOT NULL AND local_id IS NOT NULL"):
  imgs[(n,i)].append((p,int(visible or 0)))
 bylower=defaultdict(list)
 for k in slots:bylower[(k[0].lower(),k[1])].append(k)
 wiki=rows(W);assert len(wiki)==1268
 wiki_req={}; wiki_hit=defaultdict(list);wiki_evidence=set()
 for wr in wiki:
  req,state=pic(wr["이미지_URL"])
  wiki_req[wr["목록ID"]]=(req,state)
  for key in req:
   for source in bylower.get(key,[]):
    wiki_hit[wr["목록ID"]].append(source);wiki_evidence.add(source)
 tagged={}
 for key in slots:
  p=prop.get(key,{})
  reasons=["ATTR:"+field for field in sorted(p) if field in TAG_KEYS]
  if key in wiki_evidence:reasons.append("PZWIKI_IMAGE_FILENAME_ID")
  if reasons:tagged[key]=reasons
 assert len(tagged)>1000
 sql="""
 CREATE TABLE furniture_group(group_id TEXT PRIMARY KEY,tileset TEXT,custom_name TEXT,group_name TEXT,
   grouping_basis TEXT NOT NULL,source_sprite_count INTEGER,directions TEXT,container_types TEXT,
   capacity_raw TEXT,iso_types TEXT,png_paths TEXT,assembly_status TEXT NOT NULL,
   game_object_confirmed INTEGER NOT NULL DEFAULT 0);
 CREATE TABLE furniture_tile(source_key TEXT PRIMARY KEY,group_id TEXT NOT NULL,tileset TEXT,
   local_id INTEGER,CustomName TEXT,GroupName TEXT,Facing TEXT,SpriteGridPos TEXT,
   container_type TEXT,ContainerCapacity TEXT,IsoType TEXT,materials TEXT,CustomItem TEXT,
   raw_properties_with_source_json TEXT NOT NULL,original_source_files TEXT NOT NULL,
   source_png_paths TEXT,png_visible_count INTEGER,candidate_reasons TEXT NOT NULL,
   property_conflicts_json TEXT NOT NULL);
 CREATE TABLE furniture_direction_parts(group_id TEXT NOT NULL,facing TEXT NOT NULL,
   sprite_ids TEXT NOT NULL,source_grid_positions TEXT,parts INTEGER,
   grid_width INTEGER,grid_height INTEGER,assembly_status TEXT,
   game_object_composition_confirmed INTEGER NOT NULL DEFAULT 0,
   PRIMARY KEY(group_id,facing));
 CREATE TABLE furniture_function_property(group_id TEXT NOT NULL,property_name TEXT NOT NULL,
   observed_values_json TEXT NOT NULL,value_conflict INTEGER NOT NULL,
   PRIMARY KEY(group_id,property_name));
 CREATE TABLE furniture_container_source(group_id TEXT NOT NULL,source_key TEXT NOT NULL,
   container_type TEXT,capacity_raw TEXT,position_raw TEXT,
   evidence_scope TEXT NOT NULL,PRIMARY KEY(group_id,source_key));
 CREATE TABLE wiki_furniture(wiki_id TEXT PRIMARY KEY,source_row_json TEXT NOT NULL,
   category TEXT,subcategory TEXT,name TEXT,encumbrance_raw TEXT,size_raw TEXT,
   storage_raw TEXT,bed_quality_raw TEXT,construction_surface_raw TEXT,
   pickup_skill_raw TEXT,pickup_tool_raw TEXT,dismantle_skill_raw TEXT,dismantle_tool_raw TEXT,
   image_url TEXT,article_url TEXT,category_page TEXT);
 CREATE TABLE wiki_image_tile(wiki_id TEXT NOT NULL,part_index INTEGER NOT NULL,
   source_key TEXT NOT NULL,matching_status TEXT NOT NULL,
   PRIMARY KEY(wiki_id,part_index));
 CREATE TABLE wiki_group_candidate(wiki_id TEXT NOT NULL,group_id TEXT NOT NULL,
   matching_sprite_count INTEGER NOT NULL,
   link_status TEXT NOT NULL,confirmed_same_game_object INTEGER NOT NULL DEFAULT 0,
   PRIMARY KEY(wiki_id,group_id));
 CREATE TABLE rosewood_357_3d_bridge(legacy_style_id TEXT,legacy_index INTEGER,
   group_id TEXT,source_preview_path TEXT,viewpoint_model_id TEXT,
   source_sprite_key TEXT,identity_status TEXT NOT NULL,
   PRIMARY KEY(legacy_style_id,group_id,source_sprite_key));
 CREATE TABLE future_map_placement(placement_id TEXT PRIMARY KEY,group_id TEXT,
   x INTEGER,y INTEGER,z INTEGER,facing TEXT,room_type TEXT,
   source_sprite_ids TEXT,inventory_json TEXT,source_tmx TEXT);
 CREATE TABLE future_item_distribution(rule_id TEXT PRIMARY KEY,room_type TEXT,
   container_type TEXT,distribution_name TEXT,pz_item TEXT,weight_raw TEXT,
   source_lua_script TEXT,version TEXT);
 CREATE TABLE future_minecraft_implementation(group_id TEXT PRIMARY KEY,
   minecraft_model_id TEXT,implementation_kind TEXT,confirmed INTEGER);
 CREATE TABLE furniture_source_conflict(source_key TEXT,attribute TEXT,values_json TEXT,
   PRIMARY KEY(source_key,attribute));
 CREATE INDEX ix_furn_group ON furniture_tile(group_id);
 CREATE INDEX ix_furn_name ON furniture_group(custom_name,group_name);
 CREATE INDEX ix_furn_container ON furniture_tile(container_type);
 CREATE INDEX ix_wiki_group ON wiki_group_candidate(group_id);
 CREATE INDEX ix_legacy_group ON rosewood_357_3d_bridge(group_id);
 """
 con.executescript(sql)
 group_for={};group_tiles=defaultdict(list);grp_key={}
 for (name,id),reason in tagged.items():
  d=prop.get((name,id),{})
  a=uniq(x for x,f in d.get("CustomName",[]))
  b=uniq(x for x,f in d.get("GroupName",[]))
  if a or b:
   cname=joined(a);gname=joined(b)
   group_kind="NAME_STYLE_TILESET_UNVERIFIED"
   group_sig=("named",name,cname,gname)
  else:
   cname=gname=""
   group_kind="ONE_UNNAMED_SPRITE_UNVERIFIED"
   group_sig=("unnamed",name,id)
  gid="FUR-"+stable(*group_sig)
  group_for[(name,id)]=gid;group_tiles[gid].append((name,id))
  grp_key[gid]=(name,cname,gname,group_kind)
 # Use exact raw values and source files instead of arbitrarily resolving original conflicts.
 sprite_export=[];feature_export=[];direction_export=[];group_export=[]
 for (name,id),reasons in sorted(tagged.items()):
  k=(name,id);p=prop.get(k,{})
  get=lambda field:uniq(v for v,f in p.get(field,[]))
  raw={field:[{"value":v,"source_file":f} for v,f in vlist] for field,vlist in sorted(p.items())}
  conflicts={field:get(field) for field in p if len(get(field))>1}
  for field,vs in conflicts.items():
   con.execute("INSERT INTO furniture_source_conflict VALUES(?,?,?)",
    (name+"/"+str(id),field,json.dumps(vs,ensure_ascii=False)))
  pics=imgs.get(k,[])
  source_key=name+"/"+str(id)
  value=(source_key,group_for[k],name,id,joined(get("CustomName")),joined(get("GroupName")),
   joined(get("Facing")),joined(get("SpriteGridPos")),joined(get("container")),
   joined(get("ContainerCapacity")),joined(get("IsoType")),joined(get("Material")),
   joined(get("CustomItem")),json.dumps(raw,ensure_ascii=False),joined(slots[k]),
   joined(x[0] for x in pics),sum(x[1] for x in pics),joined(reasons),
   json.dumps(conflicts,ensure_ascii=False))
  con.execute("INSERT INTO furniture_tile VALUES("+",".join("?" for x in value)+")",value)
  sprite_export.append(dict(source_key=source_key,group_id=group_for[k],
   CustomName=value[4],GroupName=value[5],Facing=value[6],SpriteGridPos=value[7],
   container=value[8],ContainerCapacity=value[9],IsoType=value[10],
   png_paths=value[15],property_conflicts=value[18]))
  if "container" in p or "ContainerCapacity" in p:
   con.execute("INSERT INTO furniture_container_source VALUES(?,?,?,?,?,?)",
    (group_for[k],source_key,joined(get("container")),joined(get("ContainerCapacity")),
     joined(get("ContainerPosition")),"ORIGINAL_TILEDEF_NOT_INVENTED"))
 for gid,keys in sorted(group_tiles.items()):
  name,cname,gname,kind=grp_key[gid]
  values=defaultdict(set);faces=defaultdict(list);pictures=[]
  for key in keys:
   p=prop.get(key,{})
   for attr,vs in p.items():
    values[attr].update(v for v,f in vs if v is not None)
   f=uniq(v for v,src in p.get("Facing",[]))
   for d in f or ["(not set)"]:faces[d].append(key)
   pictures += [x[0] for x in imgs.get(key,[])]
  states=[]
  for facing,parts in sorted(faces.items()):
   pos_values=[uniq(v for v,s in prop.get(k,{}).get("SpriteGridPos",[])) for k in parts]
   positions=[parse_xy(x[0]) if len(x)==1 else None for x in pos_values]
   known=[p for p in positions if p is not None]
   if not known:
    status="SINGLE_SPRITE" if len(parts)==1 else "MULTIPLE_SPRITES_SAME_FACING_NO_GRID_REVIEW"
    width=height=None
   elif len(known)!=len(parts):status="MIXED_GRID_AND_NO_GRID_REVIEW";width=height=None
   elif len(set(known))!=len(known):status="DUPLICATE_GRID_POSITION_REVIEW";width=height=None
   else:
    width=max(x for x,y in known)-min(x for x,y in known)+1
    height=max(y for x,y in known)-min(y for x,y in known)+1
    status="RECTANGULAR_GRID_CANDIDATE" if width*height==len(parts) else "INCOMPLETE_GRID_REVIEW"
   states.append(status)
   ids=joined(k[0]+"/"+str(k[1]) for k in parts)
   grid=joined(v for x in pos_values for v in x)
   con.execute("INSERT INTO furniture_direction_parts VALUES(?,?,?,?,?,?,?,?,?)",
    (gid,facing,ids,grid,len(parts),width,height,status,0))
   direction_export.append(dict(group_id=gid,tileset=name,CustomName=cname,GroupName=gname,
    Facing=facing,sprite_source_ids=ids,SpriteGridPos=grid,
    width=width,height=height,assembly_status=status))
  for attr,vs in values.items():
   con.execute("INSERT INTO furniture_function_property VALUES (?,?,?,?)",
    (gid,attr,json.dumps(sorted(vs),ensure_ascii=False),int(len(vs)>1)))
   if attr in FUNCTION_KEYS:
    feature_export.append(dict(group_id=gid,CustomName=cname,GroupName=gname,
      attribute=attr,original_values=joined(vs),value_conflict=int(len(vs)>1)))
  status="REVIEW_MULTIPLE_VARIANTS_OR_PARTS" if any("REVIEW" in x for x in states) else "SOURCE_GROUPED_NOT_GAME_CERTIFIED"
  con.execute("INSERT INTO furniture_group VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)",
   (gid,name,cname,gname,kind,len(keys),
    joined(x for x in faces if x!="(not set)"),joined(values.get("container",[])),
    joined(values.get("ContainerCapacity",[])),joined(values.get("IsoType",[])),
    joined(pictures),status,0))
  group_export.append(dict(group_id=gid,tileset=name,CustomName=cname,GroupName=gname,
   original_tile_keys=joined(k[0]+"/"+str(k[1]) for k in keys),
   member_sprite_count=len(keys),direction_values=joined(faces),
   container_types=joined(values.get("container",[])),
   capacity_raw=joined(values.get("ContainerCapacity",[])),
   IsoTypes=joined(values.get("IsoType",[])),source_png_files=joined(pictures),
   grouping_basis=kind,assembly_status=status,game_object_certified="NO"))
 wiki_export=[];wiki_status=Counter()
 for w in wiki:
  wid=w["목록ID"]
  obj=(wid,json.dumps(w,ensure_ascii=False),w["대분류_원문"],w["소분류_원문"],
   w["가구명_원문"],w["운반부담_Encumbrance"],w["크기_타일수"],
   w["수납용량_원문"],w["침대품질_원문"],w["제작표면_원문"],
   w["회수_기술"],w["회수_도구"],w["분해_기술"],w["분해_도구"],
   w["이미지_URL"],w["개별문서_URL"],w["목록페이지_URL"])
  con.execute("INSERT INTO wiki_furniture VALUES("+",".join("?" for x in obj)+")",obj)
  req,parsing=wiki_req[wid];pairs=Counter()
  for idx,requested in enumerate(req):
   got=bylower.get(requested,[])
   con.execute("INSERT INTO wiki_image_tile VALUES(?,?,?,?)",
    (wid,idx,requested[0]+"/"+str(requested[1]),"SOURCE_ID_FOUND" if got else "NOT_IN_ORIGINAL_TILEDEF"))
   for k in got:pairs[group_for[k]]+=1
  if not pairs:
   gid="FUR-WIKI-"+wid
   con.execute("INSERT INTO furniture_group VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)",
    (gid,None,w["가구명_원문"],None,"WIKI_ONLY_NO_MAPPED_TILE",
      0,"","","","","","WIKI_ONLY_UNRESOLVED",0))
   pairs[gid]=0
  for gid,n in pairs.items():
   con.execute("INSERT INTO wiki_group_candidate VALUES(?,?,?,?,?)",
    (wid,gid,n,"SOURCE_SPRITE_ID_MATCH_NOT_GAME_CERTIFIED" if n else "WIKI_ONLY_UNRESOLVED",0))
  wiki_status["WITH_SOURCE_ID" if any(pairs.values()) else "NO_SOURCE_ID"]+=1
  wiki_export.append(dict(wiki_id=wid,original_name=w["가구명_원문"],
   original_category=w["대분류_원문"],source_image_url=w["이미지_URL"],
   image_parse_state=parsing,matching_tiledef_ids=len(wiki_hit[wid]),
   linked_furniture_group_ids=joined(pairs.keys()),raw_tile_size=w["크기_타일수"],
   raw_storage_capacity=w["수납용량_원문"],is_game_identity_confirmed="NO"))
 refs=rows(RO/"SOURCE_SPRITES_1347.csv")
 for x in refs:
  src=(x["tileset"],int(x["local_id"]))
  if src not in group_for:continue
  con.execute("INSERT OR IGNORE INTO rosewood_357_3d_bridge VALUES(?,?,?,?,?,?,?)",
   (x["style_id"],None,group_for[src],None,x["viewpoint_model_id"],
    x["source_key"],"SOURCE_ID_LINK_REFERENCE_NOT_OFFICIAL_GAME_IDENTITY"))
 index={r["style_id"]:r for r in rows(RO/"CATALOG_357_STYLES.csv")}
 for i in index.values():
  con.execute("UPDATE rosewood_357_3d_bridge SET legacy_index=?,source_preview_path=? WHERE legacy_style_id=?",
   (i["index"],i["original_preview_path"],i["style_id"]))
 con.commit()
 assert con.execute("PRAGMA integrity_check").fetchone()[0]=="ok"
 names=["furniture_group","furniture_tile","furniture_direction_parts",
 "furniture_function_property","furniture_container_source",
 "wiki_furniture","wiki_image_tile","wiki_group_candidate",
 "rosewood_357_3d_bridge","future_map_placement",
 "future_item_distribution","future_minecraft_implementation","furniture_source_conflict"]
 output_counts={n:con.execute("SELECT COUNT(*) FROM "+n).fetchone()[0] for n in names}
 assert output_counts["wiki_furniture"]==1268
 assert output_counts["furniture_tile"]==len(tagged)
 assert output_counts["future_map_placement"]==output_counts["future_item_distribution"]==output_counts["future_minecraft_implementation"]==0
 con.close()
 write(OUT/"FURNITURE_GROUPS.csv",group_export)
 write(OUT/"FURNITURE_TILES_AND_ATTRIBUTES.csv",sprite_export)
 write(OUT/"FURNITURE_DIRECTIONS_AND_PARTS.csv",direction_export)
 write(OUT/"FURNITURE_FUNCTION_PROPERTIES.csv",feature_export)
 write(OUT/"ALL_PZWIKI_1268_LINKED.csv",wiki_export)
 manifest={"source":"B42_v259_7_original_tiledefs_plus_PZwiki_1268",
  "full_source_distinct_tiles":len(slots),"full_source_original_rows":counts,
  "wiki_rows":len(wiki),"wiki_status":dict(wiki_status),
  "furniture_property_or_wiki_candidate_tiles":len(tagged),
  "candidate_group_count_from_original":len(group_tiles),
  "new_database_table_counts":output_counts,
  "no_certified_unique_game_objects":True,
  "source_db_sha256":original_hash,
  "original_sources_preserved_in_sqlite":True,
  "loot_rules_extracted":False,"map_placements_extracted":False,
  "minecraft_block_or_entity_selected":False,
  "no_original_files_modified":True,"sqlite_integrity":"ok"}
 (OUT/"MANIFEST.json").write_text(json.dumps(manifest,indent=2,ensure_ascii=False)+"\n",encoding="utf8")
 readme=["# Project Zomboid B42 전체 가구 원장 (최초 DB)",
  "목표: 모든 원본 가구 스프라이트/방향/부품/속성을 보존해 후속 Minecraft 맵 변환에 사용.",
  "가구를 Block/Entity로 만들지는 아직 결정하지 않았다.",
  "## 원본이 보존된 범위",
  "- 원본 TileDef의 "+str(len(slots))+"개 고유 타일 키, 원본 source_slots "
    +str(counts["source_slots"])+"행, 원본 source_attributes "
    +str(counts["source_attributes"])+"행과 PNG 격자 "
    +str(counts["image_cells"])+"행을 SQLite에 그대로 보존.",
  "- 위키 1268행 원문 JSON, 이미지 링크, 위키 항목에서 지목된 원본 타일 ID, 가구별 명칭/크기/수납 정보.",
  "- 속성 또는 위키 원본 ID로 연결된 가구 후보 타일: "+str(len(tagged))+"개.",
  "- 잠정 가구 그룹: "+str(output_counts["furniture_group"])+"개. 이는 실제 고유 가구 디자인 수가 아님.",
  "## 원본 정보와 추정값 구분",
  "- furniture_tile: 각 타일의 모든 원본 속성값과 그 값이 기록된 source_file 정보.",
  "- furniture_group: 같은 타일셋의 CustomName+GroupName 기준 잠정 그룹. 무명 타일은 ID별로 보존.",
  "- furniture_direction_parts: Facing 방향과 SpriteGridPos 부품 좌표. 타일 중복/방향 누락은 REVIEW 상태.",
  "- furniture_container_source: container, ContainerCapacity, ContainerPosition. 원본 그대로 보존.",
  "- furniture_function_property: 수납/가전/물/기타 기능 관련 원본 속성값.",
  "- wiki_furniture/wiki_image_tile/wiki_group_candidate: PZwiki 원문 1268행과 원본 타일 ID 후보 관계.",
  "- rosewood_357_3d_bridge: 기존 로즈우드 357 검수와 Viewpoint 3D 참조를 연결. 공식 객체 ID 보증은 아님.",
  "- future_map_placement, future_item_distribution, future_minecraft_implementation: 의도적으로 비움. 데이터 근거 확보 뒤 작성.",
  "## 중요",
  "61,418개 원본 타일 모두가 가구인 것은 아니다. 타일 속성이 부실하거나 위키에 없는 가구도 남아 있을 수 있다. 전체 원본 61,418개는 보존하되 가구 후보 자동 선별은 실물 가구 판정이 아니다.",
  "같은 CustomName+GroupName이라도 구조가 다를 수 있고, 다른 이름이 같은 디자인일 수도 있다. 방향·부품을 임의로 합쳐 확정하지 않는다.",
  "Item distribution을 구현하려면 별도 원본 Lua 분포와 맵 방 유형을 연결해야 한다. 아직 수납 내용물 생성 규칙을 추정하지 않았다.",
  "## 출력물",
  "- B42_FURNITURE_ALL_SOURCE.sqlite: 원본 전체 자료 + 가구/방향/속성/위키 관계형 DB.",
  "- FURNITURE_GROUPS.csv: 잠정 가구 그룹과 연결된 모든 타일 ID.",
  "- FURNITURE_TILES_AND_ATTRIBUTES.csv: 원본 타일/방향/그룹/수납 속성.",
  "- FURNITURE_DIRECTIONS_AND_PARTS.csv: 방향·구성 부품 기록.",
  "- FURNITURE_FUNCTION_PROPERTIES.csv: 기능 관련 속성.",
  "- ALL_PZWIKI_1268_LINKED.csv: 전체 위키 가구 행 매핑.",
  "- MANIFEST.json: 실제 작업 범위와 검증 수치.",
  "- PZ_B42_FULL_FURNITURE_DB.zip: SQLite DB 포함 통합 압축본."
 ]
 (OUT/"README_KO.md").write_text("\n\n".join(readme)+"\n",encoding="utf8")
 with zipfile.ZipFile(OUT/"PZ_B42_FULL_FURNITURE_DB.zip","w",zipfile.ZIP_DEFLATED,compresslevel=6) as z:
  for p in sorted(OUT.iterdir()):
   if p.is_file() and p.suffix!=".zip":z.write(p,p.name)
 with zipfile.ZipFile(OUT/"PZ_B42_FULL_FURNITURE_DB.zip") as z:
  assert z.testzip() is None
  assert DB.name in z.namelist()
 print("BUILT_FURNITURE_CATALOG",json.dumps(manifest,ensure_ascii=False),flush=True)
if __name__=="__main__":main()
