#!/usr/bin/env python3
"""B42 v9: original-definition-first inventory and unresolved Wiki ID audit.
No fabricated game-object identity, item distribution, or Minecraft implementation.
"""
import csv,json,re,sqlite3,zipfile,shutil
from pathlib import Path
from collections import Counter,defaultdict
ROOT=Path(__file__).resolve().parents[1]
SRC=ROOT/"analysis/furniture_full_b42/2026-11-03/wiki_first_v2/B42_WIKI_FIRST_FURNITURE_REGISTRY.zip"
V8=ROOT/"analysis/furniture_full_b42/2026-11-04/visual_completion_v8/V8_ALL_129_REVIEW_COVERAGE.csv"
OUT=ROOT/"analysis/furniture_full_b42/2026-11-04/definition_first_v9"
DB=OUT/"B42_FURNITURE_DEFINITION_FIRST_V9.sqlite"
Z=OUT/"B42_FURNITURE_DEFINITION_FIRST_V9.zip"
GENERICS={"PZW-0808","PZW-0876","PZW-0944"}
VARIANTS={"PZW-0938","PZW-1060","PZW-1072"}
GAPS={"PZW-0808","PZW-0876","PZW-0938","PZW-0944","PZW-0950",
      "PZW-0951","PZW-1060","PZW-1072","PZW-1231","PZW-1237","PZW-1258"}
def cs(path):
 with path.open(encoding="utf-8-sig",newline="") as f:return list(csv.DictReader(f))
def wr(path,items,fields):
 with path.open("w",encoding="utf-8-sig",newline="") as f:
  w=csv.DictWriter(f,fieldnames=fields,extrasaction="ignore");w.writeheader();w.writerows(items)
def norm(s):
 return re.sub(r"[^a-z0-9]+"," ",s.lower().replace("spiffo's","spiffos")).strip()
def base(s):
 return re.sub(r"\s+\(variant\s+\d+\)$","",s,flags=re.I)
def q(con,sql):
 return [dict(r) for r in con.execute(sql)]
def n(con,t):
 return con.execute("SELECT COUNT(*) FROM "+t).fetchone()[0]
def main():
 assert not OUT.exists() and SRC.exists() and V8.exists()
 OUT.mkdir(parents=True)
 with zipfile.ZipFile(SRC) as z:
  assert z.testzip() is None
  with z.open("PZ_B42_FURNITURE_REGISTRY_WIKI_FIRST.sqlite") as inp,DB.open("wb") as out:
   shutil.copyfileobj(inp,out)
 c=sqlite3.connect(DB);c.row_factory=sqlite3.Row
 assert c.execute("PRAGMA integrity_check").fetchone()[0]=="ok"
 for t,expected in [("registry_entry",2231),("registry_entry_tile",14195),
                    ("registry_entry_container",1855),("wiki_furniture",1268),
                    ("source_attributes",195265),("source_slots",73644)]:
  assert n(c,t)==expected,(t,n(c,t))
 cover=cs(V8);assert len(cover)==129 and len({r["source_group"] for r in cover})==129
 assert all(r["runtime_identity_verified"]=="0" and r["visual_review_record_present"]=="1" for r in cover)
 entries=q(c,"SELECT * FROM registry_entry ORDER BY entry_id")
 links=q(c,"SELECT * FROM registry_entry_tile ORDER BY entry_id,source_key")
 containers=q(c,"SELECT * FROM registry_entry_container ORDER BY entry_id,source_key")
 wiki=q(c,"SELECT * FROM wiki_furniture")
 groups=q(c,"SELECT * FROM furniture_group")
 bylinks=defaultdict(list);bycont=defaultdict(list);bybase=defaultdict(list)
 for x in links:bylinks[x["entry_id"]].append(x)
 for x in containers:bycont[x["entry_id"]].append(x)
 for x in wiki:bybase[norm(base(x["name"]))].append(x["wiki_id"])
 c.executescript("""
 CREATE TABLE v9_entry_evidence(
  entry_id TEXT PRIMARY KEY, source_system TEXT,
  wiki_exact_tile_ids INTEGER, same_name_unverified_tiles INTEGER,
  tiledef_only_tiles INTEGER, original_container_rows INTEGER,
  wiki_direct_original_container_rows INTEGER,
  unverified_expansion_container_rows INTEGER,
  source_direct_facing TEXT,source_expanded_facing TEXT,
  wiki_capacity_raw TEXT,original_container_types_json TEXT,
  original_capacity_values_json TEXT,
  same_game_object_verified INTEGER NOT NULL DEFAULT 0);
 CREATE TABLE v9_container_evidence(
  entry_id TEXT,source_key TEXT,container_type TEXT,
  capacity_raw TEXT,position_raw TEXT,source_link_quality TEXT,
  item_contents_verified INTEGER NOT NULL DEFAULT 0,
  PRIMARY KEY(entry_id,source_key));
 CREATE TABLE v9_wiki_missing_id(
  wiki_id TEXT PRIMARY KEY,wiki_name TEXT,record_class TEXT,
  sibling_exact_sprite_keys INTEGER,source_name_candidates INTEGER,
  automatic_tile_link_count INTEGER NOT NULL DEFAULT 0);
 CREATE TABLE v9_wiki_missing_id_candidate(
  wiki_id TEXT,source_ref TEXT,candidate_kind TEXT,evidence TEXT,
  same_game_object_verified INTEGER NOT NULL DEFAULT 0,
  PRIMARY KEY(wiki_id,source_ref,candidate_kind));
 CREATE TABLE v9_v8_image_review_reference(
  source_group_id TEXT PRIMARY KEY,visual_review_version TEXT,
  direct_image_review_record INTEGER NOT NULL,
  runtime_identity_verified INTEGER NOT NULL DEFAULT 0);
 """)
 for r in cover:
  c.execute("INSERT INTO v9_v8_image_review_reference VALUES(?,?,?,0)",
   (r["source_group"],r["review_version"],int(r["visual_review_record_present"])))
 full=[];store=[];links_count=Counter();store_count=Counter()
 for e in entries:
  eid=e["entry_id"];ll=bylinks[eid];cc=bycont[eid]
  direct=[r for r in ll if r["evidence"]=="EXACT_WIKI_IMAGE_SPRITE_KEY"]
  extra=[r for r in ll if r["evidence"]=="SAME_TILEDEF_NAME_STYLE_SOURCE_GROUP_UNCONFIRMED"]
  alone=[r for r in ll if r["evidence"]=="SOURCE_ONLY_TILEDEF_GROUP"]
  assert len(ll)==len(direct)+len(extra)+len(alone)
  idx={x["source_key"]:x["evidence"] for x in ll}
  ct=sorted({x["container_type"] for x in cc if x["container_type"]})
  cap=sorted({x["capacity_raw"] for x in cc if x["capacity_raw"] not in ("",None)})
  facing=sorted({x["source_sprite_facing"] for x in direct if x["source_sprite_facing"]})
  other=sorted({x["source_sprite_facing"] for x in extra if x["source_sprite_facing"]})
  exact_c=sum(idx[x["source_key"]]=="EXACT_WIKI_IMAGE_SPRITE_KEY" for x in cc)
  extra_c=sum(idx[x["source_key"]]=="SAME_TILEDEF_NAME_STYLE_SOURCE_GROUP_UNCONFIRMED" for x in cc)
  c.execute("INSERT INTO v9_entry_evidence VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,0)",
   (eid,e["source_system"],len(direct),len(extra),len(alone),len(cc),
    exact_c,extra_c,"|".join(facing),"|".join(other),e["wiki_capacity_raw"],
    json.dumps(ct,ensure_ascii=False),json.dumps(cap,ensure_ascii=False)))
  full.append(dict(entry_id=eid,original_name=e["display_name"],
   list_source=e["source_system"],exact_wiki_tile_ids=len(direct),
   same_name_tile_ids_NOT_VERIFIED=len(extra),source_only_tile_ids=len(alone),
   source_inventory_property_rows=len(cc),direct_wiki_inventory_tile_ids=exact_c,
   unverified_name_group_inventory_tile_ids=extra_c,
   original_source_container_types="|".join(ct),original_source_capacity_values="|".join(cap),
   original_wiki_capacity_raw=e["wiki_capacity_raw"] or "",
   direct_Facing="|".join(facing),expanded_Facing_UNVERIFIED="|".join(other),
   same_physical_furniture_verified="NO",loot_rule_imported="NO"))
  for r in ll:links_count[r["evidence"]]+=1
  for x in cc:
   source=idx[x["source_key"]]
   quality=("WIKI_DIRECT_ID" if source=="EXACT_WIKI_IMAGE_SPRITE_KEY" else
     "SAME_NAME_UNVERIFIED" if source=="SAME_TILEDEF_NAME_STYLE_SOURCE_GROUP_UNCONFIRMED"
     else "SOURCE_ONLY_ORIGINAL")
   c.execute("INSERT INTO v9_container_evidence VALUES(?,?,?,?,?,?,0)",
    (eid,x["source_key"],x["container_type"],x["capacity_raw"],x["container_position_raw"],quality))
   store.append(dict(entry_id=eid,source_key=x["source_key"],
    container_type=x["container_type"] or "",ContainerCapacity_raw=x["capacity_raw"] or "",
    ContainerPosition_raw=x["container_position_raw"] or "",
    source_link_quality=quality,actual_item_contents_verified="NO"))
   store_count[quality]+=1
 gaps=q(c,"SELECT * FROM registry_entry WHERE identity_status='WIKI_LISTED_NO_ID_FROM_IMAGE'")
 assert len(gaps)==11 and {x["wiki_id"] for x in gaps}==GAPS
 candidate=[];gap_export=[];gapcounts=Counter()
 source_groups=[g for g in groups if g["grouping_basis"]!="WIKI_ONLY_NO_MAPPED_TILE" and g["source_sprite_count"]]
 for e in sorted(gaps,key=lambda x:x["wiki_id"]):
  wid=e["wiki_id"];name=e["display_name"];target=norm(base(name))
  kind=("COLLECTION_HEADING_NOT_SINGLE_SPRITE" if wid in GENERICS else
        "VARIANT_IMAGE_MISSING" if wid in VARIANTS else "SPECIFIC_ITEM_IMAGE_MISSING")
  siblings=[x for x in bybase[target] if x!=wid]
  sibling_keys=set()
  if siblings:
   args=",".join("?" for _ in siblings)
   sibling_keys={x[0] for x in c.execute(
    "SELECT DISTINCT source_key FROM wiki_image_tile WHERE matching_status='SOURCE_ID_FOUND' AND wiki_id IN ("+args+")",siblings)}
  source_candidates=[]
  if wid not in GENERICS:
   for g in source_groups:
    cn=norm(g["custom_name"] or "");gn=norm(g["group_name"] or "")
    original=norm(" ".join((g["custom_name"] or "",g["group_name"] or "")))
    if not original:continue
    exact=target in (cn,gn)
    phrase=len(target)>=8 and target in original
    if exact or phrase:source_candidates.append((g,"SOURCE_NAME_EXACT" if exact else "SOURCE_NAME_PHRASE"))
  # Candidates are explicitly unverified. No candidate modifies the original mapping.
  own=[]
  for g,reason in sorted(source_candidates,key=lambda z:(z[1]!="SOURCE_NAME_EXACT",z[0]["group_id"]))[:30]:
   own.append((g["group_id"],"TILEDEF_NAME_ONLY",reason))
  for key in sorted(sibling_keys)[:80]:
   own.append((key,"OTHER_WIKI_VARIANT_SPRITE_NOT_THIS_ROW","SIBLING_IMAGE_ID"))
  for ref,kind2,evidence in own:
   c.execute("INSERT OR IGNORE INTO v9_wiki_missing_id_candidate VALUES(?,?,?,?,0)",
    (wid,ref,kind2,evidence))
   candidate.append(dict(wiki_id=wid,wiki_name=name,candidate_ref=ref,
    candidate_kind=kind2,evidence=evidence,verified_game_object="NO"))
  c.execute("INSERT INTO v9_wiki_missing_id VALUES(?,?,?,?,?,0)",
   (wid,name,kind,len(sibling_keys),len(source_candidates)))
  gap_export.append(dict(wiki_id=wid,wiki_name=name,
    original_page_url=e["article_url"],gap_class=kind,
    sibling_variant_exact_keys=len(sibling_keys),
    source_group_NAME_MATCH_CANDIDATES=len(source_candidates),
    reviewed_candidate_refs=len(own),
    verified_original_sprite_id_count=0,added_automatic_links=0,
    action="Separate category header from specific item; require exact source sprite ID"))
  gapcounts[kind]+=1
 assert sum(links_count.values())==14195 and sum(store_count.values())==1855
 assert sum(gapcounts.values())==11
 assert sum(r["exact_wiki_tile_ids"]==0 and r["list_source"]=="WIKI" for r in full)==11
 c.commit()
 assert c.execute("PRAGMA integrity_check").fetchone()[0]=="ok"
 for table,expected in [("v9_entry_evidence",2231),("v9_container_evidence",1855),
                        ("v9_wiki_missing_id",11),("v9_v8_image_review_reference",129),
                        ("source_attributes",195265),("registry_entry_tile",14195)]:
  assert n(c,table)==expected,(table,n(c,table))
 for table in ["future_item_distribution","future_map_placement","future_minecraft_implementation"]:
  assert n(c,table)==0
 assert c.execute("SELECT SUM(automatic_tile_link_count) FROM v9_wiki_missing_id").fetchone()[0]==0
 for name,data,fields in [
  ("V9_2231_SOURCE_EVIDENCE.csv",full,list(full[0])),
  ("V9_1855_STORAGE_EVIDENCE.csv",store,list(store[0])),
  ("V9_11_UNLINKED_WIKI_AUDIT.csv",gap_export,list(gap_export[0])),
  ("V9_11_NAME_CANDIDATES_UNVERIFIED.csv",candidate,
   ["wiki_id","wiki_name","candidate_ref","candidate_kind","evidence","verified_game_object"])
 ]:wr(OUT/name,data,fields)
 manifest=dict(wiki_rows=1268,wiki_exact_sprite_connected_rows=1257,
  wiki_unlinked_rows=11,source_only_groups=963,registry_entry_rows=2231,
  original_tile_link_rows=14195,original_container_link_rows=1855,
  original_tiledef_attributes=195265,original_slots=73644,
  v8_visually_reviewed_conflict_groups=129,
  link_evidence=dict(links_count),storage_evidence=dict(store_count),
  wiki_missing_record_classes=dict(gapcounts),
  wiki_missing_candidate_rows=len(candidate),
  new_wiki_direct_ids_verified=0,source_files_modified=False,
  loot_rules_imported=0,minecraft_decisions=0,
  game_object_identity_verified_new=0,sqlite_integrity="ok")
 (OUT/"MANIFEST.json").write_text(json.dumps(manifest,indent=2,ensure_ascii=False)+"\n",encoding="utf8")
 report=["# B42 가구 원장 v9 — 원본 정의 우선 근거 검수",
 "원본 정의로 확인할 수 있는 가구 종류·타일 ID·Facing·SpriteGridPos·수납 속성을 먼저 분리한 DB야. 기존 v2 원본 2,231행 및 195,265 속성을 보존했고, v8 이미지 검수 129그룹은 출처/범위만 계승했어.",
 "## 미연결 위키 항목 11건"]
 for row in gap_export:report.append("- "+row["wiki_id"]+" "+row["wiki_name"]+": "+row["gap_class"]+"; 원본 이름 후보 "+str(row["source_group_NAME_MATCH_CANDIDATES"])+"그룹, 정확 ID 추가 없음")
 report+=["## 판단 기준",
 "Painting, Decorations, Signs는 컬렉션/범주형 항목일 수 있으므로 하나의 독립 가구로 단정하지 않아.",
 "Ominous Sign variant 2와 Flowerbed variant 12/24는 다른 형제 변형의 ID가 있어도 해당 변형의 ID로 복사하지 않아.",
 "원본 CustomName/GroupName을 이용한 후보 연결은 타일 ID 검증이 아니며 후보 테이블에서만 조회 가능.",
 "원본 container, ContainerCapacity, ContainerPosition은 각각 원본 값으로 저장. Wiki 수납 용량은 별도의 원문 필드로 남겨 서로 섞지 않아. 한 가구를 구성하는 여러 원본 타일의 용량을 자동 합산하지 않아.",
 "게임 Lua Loot Distribution 및 RoomDefs와의 결합은 원본 Lua가 확보될 때만 수행하고, Block/Entity 선택은 계속 보류해.",
 "## 파일",
 "B42_FURNITURE_DEFINITION_FIRST_V9.sqlite 와 ZIP: 원본 전체 DB에 5개의 v9 근거 테이블을 추가.",
 "V9_2231_SOURCE_EVIDENCE.csv: 모든 가구 목록 레코드별 직접 ID/이름 확장/기능 속성/방향 근거.",
 "V9_1855_STORAGE_EVIDENCE.csv: 모든 수납 타일 연결의 원본 기능 값 및 증거 등급.",
 "V9_11_UNLINKED_WIKI_AUDIT.csv: 링크 없는 11개 항목의 원인·대응 현황.",
 "V9_11_NAME_CANDIDATES_UNVERIFIED.csv: 확인 전의 출처 이름·형제 변형 후보.",
 "MANIFEST.json: 전체 SQLite·ZIP 검증에 사용된 집계.",
 "이 단계에서는 개별 타일 그림을 불필요하게 추가 검수하지 않았어. 정체/방향/부품의 실제 게임 객체 동일성은 공식 근거가 확인되어야 확정할 수 있어."]
 (OUT/"README_KO.md").write_text("\n\n".join(report)+"\n",encoding="utf8")
 c.close()
 with zipfile.ZipFile(Z,"w",zipfile.ZIP_DEFLATED,compresslevel=5) as z:
  for p in sorted(OUT.iterdir()):
   if p.is_file() and p!=Z:z.write(p,p.name)
 with zipfile.ZipFile(Z) as z:
  assert z.testzip() is None
  assert DB.name in z.namelist()
 print("B42_DEFINITION_FIRST_V9_OK",json.dumps(manifest,ensure_ascii=False),flush=True)
if __name__=="__main__":main()
