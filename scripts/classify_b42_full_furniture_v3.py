#!/usr/bin/env python3
import sqlite3,csv,json,zipfile,shutil,re
from pathlib import Path
from collections import Counter,defaultdict
from itertools import combinations
R=Path(__file__).resolve().parents[1]
Z=R/"analysis/furniture_full_b42/2026-11-03/wiki_first_v2/B42_WIKI_FIRST_FURNITURE_REGISTRY.zip"
O=R/"analysis/furniture_full_b42/2026-11-03/classification_v3"
D=O/"FURNITURE_CLASSIFIED_V3.sqlite"
def select(c,q):return [dict(x) for x in c.execute(q)]
def count(c,t):return c.execute("SELECT COUNT(*) FROM "+t).fetchone()[0]
def output(name,records):
 assert records
 with (O/name).open("w",encoding="utf-8-sig",newline="") as f:
  w=csv.DictWriter(f,list(records[0]));w.writeheader();w.writerows(records)
def classif(g):
 t=(g["tileset"] or "").lower()
 n=((g["custom_name"] or "")+" "+(g["group_name"] or "")).lower()
 if g["container_types"]:return ("STORAGE_FUNCTION","RAW_CONTAINER_PROPERTY",g["container_types"])
 if t.startswith(("walls_decoration_","signs_","papernotices_","floors_rugs_","rugs_")):
  return ("DECORATION_REVIEW","TILESET_FAMILY",t)
 if t.startswith(("floors_","floor_","blends_","street_","roofs_","ceilings_","fencing_","fixtures_stairs_","fixtures_railings_")):
  return ("ARCHITECTURE_OR_GROUND_NOT_FURNITURE","TILESET_FAMILY",t)
 if t.startswith(("walls_","fixtures_doors_","fixtures_windows_")):
  return ("BUILDING_PART_NOT_FURNITURE","TILESET_FAMILY",t)
 if t.startswith(("vegetation_","f_bush","f_flowerbed")):
  return ("VEGETATION_VISUAL_REVIEW","TILESET_FAMILY",t)
 if t.startswith(("appliances_","lighting_")):
  return ("APPLIANCE_OR_LIGHT","TILESET_FAMILY",t)
 if t.startswith(("furniture_","fixtures_counters_","fixtures_sinks_","fixtures_bathroom_","fixtures_fireplaces_","trashcontainers_")):
  return ("FURNITURE_OR_FIXTURE","TILESET_FAMILY",t)
 def hit(words):return any(re.search(r"(?<![a-z])"+re.escape(w)+r"(?![a-z])",n) for w in words)
 if hit(("door","window","fence","pillar","wall","floor","stairs","roof")):
  return ("STRUCTURE_NAME_REVIEW","SOURCE_OBJECT_NAME",n)
 if hit(("poster","painting","sign","carpet","rug","banner","curtain","trophy","picture")):
  return ("DECORATION_REVIEW","SOURCE_OBJECT_NAME",n)
 if hit(("shelf","cabinet","wardrobe","dresser","locker","counter","table","desk","chair","sofa","couch","bed","bench","stool","cupboard","rack","chest","sink","toilet","shower")):
  return ("FURNITURE_NAME_REVIEW","SOURCE_OBJECT_NAME",n)
 if hit(("forge","furnace","generator","pump","radio","lamp","stove","heater","machine")):
  return ("EQUIPMENT_NAME_REVIEW","SOURCE_OBJECT_NAME",n)
 if n.strip():return ("NAMED_OBJECT_UNKNOWN","SOURCE_OBJECT_NAME",n)
 return ("UNNAMED_SPRITE_REVIEW","TILESET_ONLY",t)
def main():
 assert not O.exists()
 O.mkdir(parents=True)
 with zipfile.ZipFile(Z) as z:
  assert z.testzip() is None
  with z.open("PZ_B42_FURNITURE_REGISTRY_WIKI_FIRST.sqlite") as a,D.open("wb") as b:shutil.copyfileobj(a,b)
 c=sqlite3.connect(D);c.row_factory=sqlite3.Row
 assert c.execute("PRAGMA integrity_check").fetchone()[0]=="ok"
 assert count(c,"registry_entry")==2231 and count(c,"registry_group_conflict")==129
 c.executescript("""
 CREATE TABLE v3_source_taxonomy(group_id TEXT PRIMARY KEY,category TEXT,basis TEXT,evidence TEXT,identity_verified INTEGER DEFAULT 0);
 CREATE TABLE v3_wiki_overlap(group_id TEXT PRIMARY KEY,wiki_ids TEXT,exact_tile_ids_json TEXT,overlap_type TEXT,merge_verified INTEGER DEFAULT 0);
 CREATE TABLE v3_tile_link(entry_id TEXT,source_key TEXT,group_id TEXT,link_grade TEXT,source_record_type TEXT,PRIMARY KEY(entry_id,source_key));
 """)
 groups={x["group_id"]:x for x in select(c,"SELECT * FROM furniture_group WHERE grouping_basis!='WIKI_ONLY_NO_MAPPED_TILE'")}
 originals=select(c,"SELECT * FROM registry_entry WHERE source_system='B42_SOURCE_ONLY'")
 assert len(originals)==963
 categories=Counter();catalog=[]
 for e in originals:
  g=groups[e["source_group_id"]];cat,basis,ev=classif(g);categories[cat]+=1
  c.execute("INSERT INTO v3_source_taxonomy VALUES(?,?,?,?,0)",(g["group_id"],cat,basis,ev))
  catalog.append(dict(entry_id=e["entry_id"],group_id=g["group_id"],name=e["display_name"],
   tileset=g["tileset"],source_tiles=g["source_sprite_count"],
   container_original=g["container_types"] or "",capacity_original=g["capacity_raw"] or "",
   classification=cat,evidence_kind=basis,evidence=ev,
   final_3d_identity_confirmed="NO"))
 ids=defaultdict(set);bygroup=defaultdict(set);gkeys=defaultdict(set)
 for x in select(c,"SELECT wiki_id,source_key FROM wiki_image_tile WHERE matching_status='SOURCE_ID_FOUND'"):
  ids[x["wiki_id"]].add(x["source_key"].casefold())
 for x in select(c,"SELECT group_id,wiki_id FROM wiki_group_candidate WHERE group_id NOT LIKE 'FUR-WIKI-%'"):
  bygroup[x["group_id"]].add(x["wiki_id"])
 for x in select(c,"SELECT group_id,source_key FROM furniture_tile"):
  gkeys[x["group_id"]].add(x["source_key"].casefold())
 assert len(bygroup)==889
 conflicts=[];ct=Counter();conflicted=set()
 for x in select(c,"SELECT group_id FROM registry_group_conflict"):
  g=x["group_id"];conflicted.add(g)
  members=sorted(bygroup[g])
  per={w:sorted(ids[w]&gkeys[g]) for w in members}
  sets=[set(v) for v in per.values()]
  overlaps=[len(a&b) for a,b in combinations(sets,2)]
  if any(not s for s in sets):kind="MISSING_EXACT_ID"
  elif overlaps and all(v==0 for v in overlaps):kind="DISJOINT_WIKI_IMAGE_IDS"
  elif overlaps and all(v>0 for v in overlaps):kind="SHARED_EXACT_TILE_IDS"
  else:kind="MIXED_OVERLAP"
  c.execute("INSERT INTO v3_wiki_overlap VALUES(?,?,?,?,0)",
   (g,"|".join(members),json.dumps(per,ensure_ascii=False),kind))
  conflicts.append(dict(group_id=g,tileset=groups[g]["tileset"],
   wiki_rows="|".join(members),wiki_exact_keys=json.dumps(per,ensure_ascii=False),
   overlap_class=kind,merge_as_one_furniture="NO"))
  ct[kind]+=1
 assert len(conflicts)==129
 links=[];lc=Counter()
 for e,g,k,source in c.execute("SELECT entry_id,source_group_id,source_key,evidence FROM registry_entry_tile"):
  if source=="EXACT_WIKI_IMAGE_SPRITE_KEY":grade="DIRECT_WIKI_SPRITE_ID"
  elif source=="SAME_TILEDEF_NAME_STYLE_SOURCE_GROUP_UNCONFIRMED":
   grade="UNSAFE_SHARED_GROUP_EXPANSION" if g in conflicted else "UNVERIFIED_NAME_GROUP_EXPANSION"
  else:grade="SOURCE_ONLY"
  lc[grade]+=1
  c.execute("INSERT INTO v3_tile_link VALUES(?,?,?,?,?)",(e,k,g,grade,source))
  links.append(dict(entry_id=e,source_key=k,group_id=g,relation=grade,
    original_connection=source,physical_furniture_design_confirmed="NO"))
 assert len(links)==14195
 c.commit()
 assert c.execute("PRAGMA integrity_check").fetchone()[0]=="ok"
 assert count(c,"v3_source_taxonomy")==963
 assert count(c,"v3_wiki_overlap")==129
 assert count(c,"v3_tile_link")==14195
 assert count(c,"source_attributes")==195265
 assert count(c,"future_item_distribution")==0
 assert count(c,"future_minecraft_implementation")==0
 c.close()
 output("SOURCE_ONLY_963_CLASSIFICATION.csv",catalog)
 output("WIKI_SHARED_129_GROUP_ANALYSIS.csv",conflicts)
 output("TILE_RELATIONSHIP_14195_QUALITY.csv",links)
 manifest=dict(source_only_classified=963,wiki_shared_groups=129,tile_relations_checked=14195,
  source_only_by_class=dict(categories),shared_group_by_overlap=dict(ct),
  relation_by_evidence=dict(lc),all_original_attributes_preserved=195265,
  identity_certifications_added=0,auto_merges_performed=0,
  lua_loot_rules_imported=False,minecraft_implementation_selected=False,integrity="ok")
 (O/"MANIFEST.json").write_text(json.dumps(manifest,indent=2,ensure_ascii=False)+"\n",encoding="utf8")
 text=["# 전체 가구 DB v3 분류","Wiki 원문 1268행과 원본 TileDef 195265 속성을 유지하며, 위키 바깥 963그룹을 출처 규칙으로 구분했다.",
 "## 963그룹 분류"]
 for k,v in categories.most_common():text.append("- "+k+": "+str(v))
 text.append("## 이름이 같은 그룹을 공유하는 Wiki 항목")
 for k,v in ct.most_common():text.append("- "+k+": "+str(v))
 text.append("## 원본 타일 링크 근거 분류")
 for k,v in lc.most_common():text.append("- "+k+": "+str(v))
 text.extend(["원본 container 기능은 사실이며 타일셋/이름 기반 물체 종류는 분류 추론이다.",
 "동일 CustomName+GroupName이어도 별개의 가구일 수 있어서 Wiki 별 실제 Sprite ID 집합을 비교했고 병합하지 않았다.",
 "원본 속성/방향/다중타일은 기존 전체 DB를 계승. 아이템 생성 Lua, 맵 배치, 마크 Block/Entity 구현은 미결정.",
 "이 단계에서 새로 눈으로 모든 스프라이트를 확인하지 않았으므로 서로 다른 완성형 가구 수를 확정하지 않는다."])
 (O/"README_KO.md").write_text("\n\n".join(text)+"\n",encoding="utf8")
 with zipfile.ZipFile(O/"B42_FURNITURE_CLASSIFICATION_V3.zip","w",zipfile.ZIP_DEFLATED,compresslevel=5) as z:
  for p in sorted(O.iterdir()):
   if p.is_file() and p.suffix!=".zip":z.write(p,p.name)
 print("B42_CLASSIFICATION_V3_DONE",json.dumps(manifest,ensure_ascii=False),flush=True)
if __name__=="__main__":main()
