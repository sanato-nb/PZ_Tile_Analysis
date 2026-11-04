#!/usr/bin/env python3
"""B42 furniture v13: normalize unresolved geometry/wiki/function evidence.
Reads immutable v12 ZIP. No fuzzy object merging, no image review claims.
"""
import csv, hashlib, html, json, shutil, sqlite3, zipfile
from collections import Counter, defaultdict
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
SOURCE=ROOT/"analysis/furniture_full_b42/2026-11-04/source_proof_v12/B42_FURNITURE_SOURCE_PROOF_V12.zip"
OUT=ROOT/"analysis/furniture_full_b42/2026-11-04/conflict_triage_v13"
DB=OUT/"B42_FURNITURE_CONFLICT_TRIAGE_V13.sqlite"
PACK=OUT/"B42_FURNITURE_CONFLICT_TRIAGE_V13.zip"

def query(c,sql,params=()):
 return [dict(x) for x in c.execute(sql,params)]
def count(c,t):
 return c.execute("SELECT COUNT(*) FROM "+t).fetchone()[0]
def js(x):
 return json.dumps(x,ensure_ascii=False,sort_keys=True)
def add(c,t,row):
 cols=list(row)
 c.execute("INSERT INTO "+t+" ("+",".join(cols)+") VALUES ("+",".join("?" for _ in cols)+")",[row[k] for k in cols])
def csvout(name,data):
 if not data:raise RuntimeError(name+" cannot be empty")
 with (OUT/name).open("w",encoding="utf-8-sig",newline="") as f:
  w=csv.DictWriter(f,fieldnames=list(data[0]))
  w.writeheader();w.writerows(data)

def html_reviewer(items):
 # Provides a filtering worklist, NOT an original PNG image review.
 data=json.dumps(items,ensure_ascii=False,separators=(",",":")).replace("</","<\\/")
 page="""<!doctype html><html lang="ko"><head><meta charset="utf-8">
<title>B42 v13 원본 경고 검토 원장</title><meta name="viewport" content="width=device-width,initial-scale=1">
<style>body{font-family:system-ui,'Malgun Gothic',sans-serif;background:#f5f7f9;color:#1d2e42;margin:0}
header{background:#16334d;color:white;padding:22px}header h1{margin:0;font-size:22px}
main{max-width:1300px;margin:18px auto;padding:0 14px}
.note{background:#fff4de;border-left:3px solid #a47929;padding:10px;margin-bottom:12px}
.tools{display:flex;gap:8px;flex-wrap:wrap;margin:10px 0}
input,select{padding:10px;border:1px solid #cad6e0;border-radius:6px;font:inherit;min-width:170px}
.case{background:white;border:1px solid #d7e1e9;border-radius:8px;margin:10px 0;padding:12px}
.hdr{display:flex;gap:12px;align-items:baseline;flex-wrap:wrap}.hdr strong{font-size:15px}
.tag{background:#e5edf5;border-radius:5px;padding:3px 7px;font-size:12px}
.sub{font-size:12px;color:#52667a;overflow-wrap:anywhere}
table{border-collapse:collapse;width:100%;font-size:12px;margin-top:8px}
td,th{padding:6px;border-bottom:1px solid #e1e7ed;text-align:left;overflow-wrap:anywhere}
details{margin-top:7px}summary{cursor:pointer;font-weight:600}
.count{font-weight:700}code{overflow-wrap:anywhere}
</style></head><body><header><h1>B42 가구 v13 · 원본 경고 검토 원장</h1>
<p>474개 원본 경고의 부품·Facing·위키 이름·수납 원문 확인. 한 줄의 경고는 하나의 게임 가구 확정이 아닙니다.</p></header>
<main><div class="note"><b>주의:</b> 이 검토기는 DB의 원본 속성만 보여줍니다.
원본 PNG를 직접 시각 검수한 결과가 아니며, 동일한 이름/좌표도 같은 게임 오브젝트라는 증거가 아닙니다.
모든 경고는 검토 대기 상태입니다.</div>
<div class="tools"><input id="search" type="search" placeholder="원본 타일·가구명·그룹 검색">
<select id="kind"><option value="">전체 유형</option></select>
<select id="priority"><option value="">모든 우선순위</option><option value="1">우선 1 — 수납 차이</option>
<option value="2">우선 2 — 위치 충돌·누락</option><option value="3">우선 3 — 위키 중복 연결</option>
<option value="4">우선 4 — 그리드 미정의</option></select></div>
<div class="count" id="info"></div><div id="list"></div></main>
<script>
const DATA=%%DATA%%;
const q=document.getElementById('search'), k=document.getElementById('kind'), p=document.getElementById('priority');
const esc=x=>String(x==null?'':x).replace(/[&<>"']/g,ch=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[ch]));
for(const key of [...new Set(DATA.map(x=>x.warning_code))].sort()){const o=document.createElement('option');o.value=key;o.textContent=key;k.append(o);}
function draw(){
 const s=q.value.trim().toLowerCase();
 const x=DATA.filter(r=>(!k.value||r.warning_code===k.value)&&(!p.value||String(r.priority)===p.value)&&
  (!s||[r.group_id,r.facing,r.display_name,r.source_keys,r.wiki_names,r.warning_code].join(' ').toLowerCase().includes(s)));
 document.getElementById('info').textContent=x.length.toLocaleString()+' / '+DATA.length.toLocaleString()+'개 경고';
 document.getElementById('list').innerHTML=x.map(r=>'<article class="case"><div class="hdr"><strong>'+esc(r.display_name||'(원본 이름 없음)')+
  '</strong><span class="tag">'+esc(r.warning_code)+'</span><span class="tag">우선 '+esc(r.priority)+
  '</span><span class="tag">'+esc(r.facing)+'</span></div><div class="sub">그룹 '+esc(r.group_id)+
  ' · '+esc(r.tileset)+'</div><p>'+esc(r.why_open)+'</p><div class="sub">위키 앵커: '+esc(r.wiki_names||'없음')+
  '</div><details><summary>원본 부품 '+r.parts.length+'개와 좌표/수납 속성 보기</summary>'+
  '<table><thead><tr><th>source_key</th><th>원본 좌표</th><th>Facing</th><th>container</th><th>capacity 원문</th></tr></thead><tbody>'+
  r.parts.map(t=>'<tr><td><code>'+esc(t.source_key)+'</code></td><td>'+esc(t.grid)+'</td><td>'+
   esc(t.facing)+'</td><td>'+esc(t.container)+'</td><td>'+esc(t.capacity)+'</td></tr>').join('')+
  '</tbody></table></details></article>').join('');
}
for(const el of [q,k,p])el.addEventListener('input',draw);
draw();
</script></body></html>"""
 (OUT/"V13_WARNING_REVIEW_BROWSER.html").write_text(page.replace("%%DATA%%",data),encoding="utf-8")

def main():
 assert SOURCE.exists() and not OUT.exists(),"Source v12 ZIP missing or v13 destination already exists"
 digest=hashlib.sha256(SOURCE.read_bytes()).hexdigest()
 OUT.mkdir(parents=True)
 with zipfile.ZipFile(SOURCE) as z:
  assert z.testzip() is None
  with z.open("B42_FURNITURE_SOURCE_PROOF_V12.sqlite") as a,DB.open("wb") as b:
   shutil.copyfileobj(a,b)
 c=sqlite3.connect(DB);c.row_factory=sqlite3.Row
 assert c.execute("PRAGMA integrity_check").fetchone()[0]=="ok"
 expected={"source_attributes":195265,"source_slots":73644,"furniture_tile":8219,"v10_tile_reverse":8219,
           "v10_reverse_edge":14195,"registry_entry":2231,"wiki_furniture":1268,
           "v11_tile_position":8219,"v11_direction_template":3840,"v11_source_warning":474,
           "v12_tile_proof":8219,"v12_template_proof":3840,"v12_warning_proof":474,
           "v12_wiki_unlinked_proof":11,"v9_container_evidence":1855,"v9_v8_image_review_reference":129}
 for table,n in expected.items():
  assert count(c,table)==n,(table,count(c,table),n)
 c.executescript("""
 CREATE TABLE v13_warning_case(
  group_id TEXT,Facing TEXT,warning_code TEXT,priority INTEGER,
  tileset TEXT,CustomName TEXT,GroupName TEXT,source_tile_count INTEGER,
  exact_wiki_anchors_json TEXT,wiki_descriptions_json TEXT,
  source_keys_json TEXT,geometry_status TEXT,geometry_holes_json TEXT,geometry_collisions_json TEXT,
  analysis_note TEXT,source_evidence TEXT,review_state TEXT NOT NULL DEFAULT 'OPEN',
  same_game_object_certified INTEGER NOT NULL DEFAULT 0,
  PRIMARY KEY(group_id,Facing,warning_code));
 CREATE TABLE v13_warning_part(
  group_id TEXT,Facing TEXT,warning_code TEXT,source_key TEXT,raw_grid TEXT,
  source_facing TEXT,container_type TEXT,capacity_raw TEXT,position_raw TEXT,
  raw_source_files TEXT,PRIMARY KEY(group_id,Facing,warning_code,source_key));
 CREATE TABLE v13_storage_link(
  entry_id TEXT,source_key TEXT,source_group_id TEXT,entry_name TEXT,
  source_system TEXT,link_quality TEXT,container_type TEXT,capacity_raw TEXT,
  position_raw TEXT,original_container_type TEXT,original_capacity_raw TEXT,
  original_position_raw TEXT,value_crosscheck TEXT,loot_verified INTEGER DEFAULT 0,
  same_game_object_certified INTEGER DEFAULT 0,PRIMARY KEY(entry_id,source_key));
 CREATE TABLE v13_multiwiki_anchor(
  group_id TEXT,Facing TEXT,wiki_id TEXT,wiki_name TEXT,wiki_category TEXT,
  wiki_subcategory TEXT,wiki_capacity_raw TEXT,wiki_article_url TEXT,
  source_anchor_verified INTEGER NOT NULL,
  same_game_object_certified INTEGER NOT NULL DEFAULT 0,
  PRIMARY KEY(group_id,Facing,wiki_id));
 CREATE TABLE v13_unlinked_wiki_candidate(
  wiki_id TEXT,source_ref TEXT,candidate_kind TEXT,candidate_evidence TEXT,
  source_name_if_known TEXT,confirmed_source_tile_link INTEGER DEFAULT 0,
  PRIMARY KEY(wiki_id,source_ref,candidate_kind));
 CREATE TABLE v13_progress_metric(
  metric_key TEXT PRIMARY KEY,numerator INTEGER,denominator INTEGER,
  interpretation TEXT,certification_level TEXT);
 CREATE INDEX v13_source_part_lookup ON v13_warning_part(source_key);
 CREATE INDEX v13_warning_priority ON v13_warning_case(priority,warning_code);
 CREATE INDEX v13_storage_source_lookup ON v13_storage_link(source_key);
 """)
 group={r["group_id"]:r for r in query(c,"SELECT * FROM furniture_group")}
 tiles={r["source_key"]:r for r in query(c,"SELECT * FROM v10_tile_reverse")}
 entries={r["entry_id"]:r for r in query(c,"SELECT * FROM registry_entry")}
 wikidata={r["wiki_id"]:r for r in query(c,"SELECT * FROM wiki_furniture")}
 templates={(r["group_id"],r["Facing"]):r for r in query(c,"SELECT * FROM v12_template_proof")}
 parts_by=defaultdict(list)
 for r in query(c,"SELECT * FROM v12_tile_proof ORDER BY group_id,Facing,source_key"):
  parts_by[(r["group_id"],r["Facing"])].append(r)
 warnings=query(c,"SELECT * FROM v12_warning_proof ORDER BY group_id,Facing,issue")
 notes={
  "MULTIPLE_CONTAINER_TYPES":"원본 타일의 container 유형이 다름. 동일 컨테이너로 합치거나 강제 선택 금지.",
  "MULTIPLE_RAW_CAPACITIES":"원본 ContainerCapacity 값이 다름. 용량을 합산하거나 위키 값으로 대체 금지.",
  "DUPLICATE_POSITION":"여러 원본 타일이 같은 SpriteGridPos를 차지함. 디자인/상태/다른 물체인지 추가 확인.",
  "MISSING_GRID":"다중 구성 후보에 좌표가 없는 타일 존재. 그 타일의 위치를 임의 보간하지 않음.",
  "INCOMPLETE_GRID":"원본 좌표의 최소 직사각형에 빈 칸 존재. 실제 불규칙 물체일 수도 있음.",
  "MULTIPLE_EXACT_WIKI_ROWS":"같은 원본 템플릿이 여러 위키 이미지 행에 직접 연결됨. 카테고리/별칭/서로 다른 물체 구별.",
  "MULTIPLE_NO_GRID":"좌표 없는 여러 원본 스프라이트가 이름/방향에 따라 묶임. 다칸 구성 증거 없음."
 }
 priority={"MULTIPLE_CONTAINER_TYPES":1,"MULTIPLE_RAW_CAPACITIES":1,
  "DUPLICATE_POSITION":2,"MISSING_GRID":2,"INCOMPLETE_GRID":2,
  "MULTIPLE_EXACT_WIKI_ROWS":3,"MULTIPLE_NO_GRID":4}
 case_rows=[];case_parts=[];wiki_rows=[];counter=Counter();wiki_anchor_missing=0
 for w in warnings:
  gid,f=w["group_id"],w["Facing"];issue=w["issue"];p=parts_by[(gid,f)];t=templates[(gid,f)]
  assert p and all(x["group_id"]==gid and x["Facing"]==f for x in p)
  gr=group.get(gid)
  direct=sorted({a for x in p for a in json.loads(x["exact_wiki_json"])})
  wikiref=[]
  for val in direct:
   wid=val.split(":",1)[-1]
   wd=wikidata.get(wid)
   if not wd:wiki_anchor_missing+=1
   wikiref.append({"wiki_id":wid,"name":wd["name"] if wd else "",
    "category":wd["category"] if wd else "","storage_raw":wd["storage_raw"] if wd else ""})
   if issue=="MULTIPLE_EXACT_WIKI_ROWS":
    has_source=any(val in json.loads(x["exact_wiki_json"]) for x in p)
    record=dict(group_id=gid,Facing=f,wiki_id=wid,
     wiki_name=wd["name"] if wd else "",wiki_category=wd["category"] if wd else "",
     wiki_subcategory=wd["subcategory"] if wd else "",wiki_capacity_raw=wd["storage_raw"] if wd else "",
     wiki_article_url=wd["article_url"] if wd else "",source_anchor_verified=int(has_source and wd is not None))
    add(c,"v13_multiwiki_anchor",record);wiki_rows.append(record)
  source_keys=[x["source_key"] for x in p]
  record=dict(group_id=gid,Facing=f,warning_code=issue,priority=priority[issue],
   tileset=gr["tileset"] if gr else "",CustomName=gr["custom_name"] if gr else "",
   GroupName=gr["group_name"] if gr else "",source_tile_count=len(p),
   exact_wiki_anchors_json=js(direct),wiki_descriptions_json=js(wikiref),
   source_keys_json=js(source_keys),geometry_status=t["reproduced_status"],
   geometry_holes_json=t["holes_json"],geometry_collisions_json=t["collisions_json"],
   analysis_note=notes[issue],source_evidence="v12 + original per-tile TileDef + PZwiki text")
  add(c,"v13_warning_case",record);case_rows.append(record);counter[issue]+=1
  for tile in p:
   v=tiles[tile["source_key"]]
   rr=dict(group_id=gid,Facing=f,warning_code=issue,source_key=tile["source_key"],
     raw_grid=tile["original_grid"],source_facing=tile["source_facing"],
     container_type=tile["source_container"],capacity_raw=tile["source_capacity_raw"],
     position_raw=tile["source_container_position"],raw_source_files=tile["source_files"])
   assert rr["raw_grid"]==v["SpriteGridPos_raw"] and rr["source_facing"]==v["Facing_raw"]
   add(c,"v13_warning_part",rr);case_parts.append(rr)
 assert len(case_rows)==474 and set(notes)==set(counter)
 assert counter==Counter({"MULTIPLE_NO_GRID":250,"MULTIPLE_EXACT_WIKI_ROWS":125,
                          "MISSING_GRID":52,"DUPLICATE_POSITION":27,"INCOMPLETE_GRID":14,
                          "MULTIPLE_RAW_CAPACITIES":5,"MULTIPLE_CONTAINER_TYPES":1})
 assert wiki_anchor_missing==0,("Wiki anchors missing",wiki_anchor_missing)

 storage_rows=[];qualities=Counter();mismatches=Counter()
 for item in query(c,"SELECT * FROM v9_container_evidence ORDER BY entry_id,source_key"):
  k=item["source_key"];t=tiles[k];entry=entries[item["entry_id"]]
  exact=(item["container_type"]==t["container_raw"] and
   item["capacity_raw"]==t["ContainerCapacity_raw"] and
   item["position_raw"]==t["ContainerPosition_raw"])
  reason="MATCH" if exact else "DIFFERENCE_REQUIRES_REVIEW"
  if not exact:mismatches["SOURCE_VALUES"]+=1
  assert item["item_contents_verified"]==0
  obj=dict(entry_id=item["entry_id"],source_key=k,source_group_id=t["source_group_id"],
    entry_name=entry["display_name"],source_system=entry["source_system"],
    link_quality=item["source_link_quality"],container_type=item["container_type"],
    capacity_raw=item["capacity_raw"],position_raw=item["position_raw"],
    original_container_type=t["container_raw"],original_capacity_raw=t["ContainerCapacity_raw"],
    original_position_raw=t["ContainerPosition_raw"],value_crosscheck=reason)
  add(c,"v13_storage_link",obj);storage_rows.append(obj);qualities[obj["link_quality"]]+=1
 assert len(storage_rows)==1855 and sum(qualities.values())==1855
 assert set(qualities)=={"WIKI_DIRECT_ID","SAME_NAME_UNVERIFIED","SOURCE_ONLY_ORIGINAL"},qualities

 missing_rows=[]
 for item in query(c,"SELECT * FROM v9_wiki_missing_id_candidate ORDER BY wiki_id,source_ref,candidate_kind"):
  original=group.get(item["source_ref"])
  if not original:original=tiles.get(item["source_ref"])
  name=""
  if original:name=original.get("custom_name") or original.get("CustomName_raw") or ""
  obj=dict(wiki_id=item["wiki_id"],source_ref=item["source_ref"],
    candidate_kind=item["candidate_kind"],candidate_evidence=item["evidence"],
    source_name_if_known=name)
  add(c,"v13_unlinked_wiki_candidate",obj);missing_rows.append(obj)
 assert count(c,"v9_wiki_missing_id")==11
 assert c.execute("SELECT COALESCE(SUM(automatic_tile_link_count),0) FROM v9_wiki_missing_id").fetchone()[0]==0

 metrics=[
  ("wiki_records_directly_linked",1257,1268,"위키 항목 중 원본 타일 ID 링크 존재(게임 오브젝트 동일성 아님)","WIKI_IMAGE_ID"),
  ("original_tile_grid_provenance",8219,8219,"가구 후보 타일별 원본 SpriteGridPos 보존","SOURCE_TILE_ID"),
  ("directional_template_classification",3840,3840,"방향별 후보의 기하 상태 분석 완료. 개체 확정은 별도","SOURCE_TEMPLATE"),
  ("valid_rectangle_source_candidates",843,3840,"직사각형 기하를 가진 후보 비율. 실제 완성 가구 수와 다름","GEOMETRIC_CANDIDATE"),
  ("original_warning_reproduction",474,474,"경고 재현 성공, 해결 또는 인증 의미 아님","SOURCE_WARNING"),
  ("original_warning_resolved",0,474,"원본 경고를 수정/해결했다고 인증한 행 없음","UNRESOLVED"),
  ("inventory_links_source_joined",1855,1855,"수납 링크 원본 대조, Lua/아이템 내용 인증 아님","SOURCE_STORAGE"),
  ("duplicate_groups_review_reference",129,129,"기존 이미지 검수 참조 범위, 동일 개체 인증 아님","VISUAL_REVIEW_REFERENCE"),
  ("work_107_groups_individual_results_imported",0,107,"Work 열람 그룹 수 vs DB 개별 검수 레코드","NO_PERSISTED_REVIEW"),
  ("wiki_missing_id_auto_resolution",0,11,"미연결 11건 임의 ID 확정 없음","UNRESOLVED")
 ]
 for key,num,den,meaning,grade in metrics:
  add(c,"v13_progress_metric",dict(metric_key=key,numerator=num,denominator=den,
   interpretation=meaning,certification_level=grade))
 c.commit()
 assert c.execute("PRAGMA integrity_check").fetchone()[0]=="ok"
 assert c.execute("PRAGMA foreign_key_check").fetchall()==[]
 for table,num in {**expected,"v13_warning_case":474,
   "v13_warning_part":len(case_parts),"v13_storage_link":1855,
   "v13_multiwiki_anchor":len(wiki_rows),"v13_unlinked_wiki_candidate":len(missing_rows),
   "v13_progress_metric":len(metrics)}.items():
  assert count(c,table)==num,(table,count(c,table),num)
 for t in ["future_item_distribution","future_map_placement","future_minecraft_implementation"]:
  assert count(c,t)==0
 c.close()
 csvout("V13_474_WARNING_PRIORITY_WORKLIST.csv",case_rows)
 csvout("V13_ALL_WARNING_PART_SOURCE_KEYS.csv",case_parts)
 csvout("V13_1855_STORAGE_LINK_SOURCE_CROSSCHECK.csv",storage_rows)
 csvout("V13_WIKI_OVERLAP_IDENTITY_UNCONFIRMED.csv",wiki_rows)
 csvout("V13_UNLINKED_11_CANDIDATES_UNVERIFIED.csv",missing_rows)
 csvout("V13_PROGRESS_SCORES_SCOPE_LABELED.csv",[
  dict(metric_key=k,numerator=num,denominator=den,
       percent=round(num/den*100,2) if den else None,
       interpretation=meaning,certification_level=grade) for k,num,den,meaning,grade in metrics])
 browser=[]
 for r in sorted(case_rows,key=lambda x:(x["priority"],x["warning_code"],x["group_id"],x["Facing"])):
  gid,f=r["group_id"],r["Facing"]
  pp=parts_by[(gid,f)]
  browser.append(dict(group_id=gid,facing=f,priority=r["priority"],
   warning_code=r["warning_code"],display_name=(r["CustomName"] or r["GroupName"]),
   tileset=r["tileset"],source_keys="|".join(p["source_key"] for p in pp),
   wiki_names=" | ".join(y["name"] for y in json.loads(r["wiki_descriptions_json"])),
   why_open=r["analysis_note"],parts=[
    dict(source_key=p["source_key"],grid=p["original_grid"],
     facing=p["source_facing"],container=p["source_container"],
     capacity=p["source_capacity_raw"]) for p in pp]))
 html_reviewer(browser)
 manifest=dict(version="v13",base_v12_zip_sha256=digest,
   original_tile_keys=8219,original_attribute_rows=195265,original_slots=73644,
   source_template_count=3840,source_rectangle_candidates=843,
   unresolved_original_warnings=474,warning_parts_rows=len(case_parts),
   warning_priority_count=dict(sorted(Counter(x["priority"] for x in case_rows).items())),
   warning_type_count=dict(sorted(counter.items())),
   wiki_overlap_anchor_rows=len(wiki_rows),
   storage_join_rows=len(storage_rows),storage_link_evidence_counts=dict(sorted(qualities.items())),
   storage_original_value_difference_rows=sum(mismatches.values()),
   missing_wiki_rows=11,unverified_missing_wiki_candidate_rows=len(missing_rows),
   image_review_reference_groups=129,work_107_images_not_imported=True,
   game_object_identifications_certified=0,actual_image_inspections_new=0,
   original_lua_loot_imported=False,minecraft_implementation_selected=False,
   sqlite_integrity="ok",zip_crc="ok")
 (OUT/"MANIFEST.json").write_text(json.dumps(manifest,ensure_ascii=False,sort_keys=True,indent=2)+"\n",encoding="utf8")
 (OUT/"README_KO.md").write_text(
 "# B42 가구 DB v13 — 원본 경고 상세 분류와 수납 근거 연결\n\n"
 "PR #294 v12를 복사한 새로운 SQLite에 6개 테이블을 추가했습니다. v12 및 이전 테이블은 수정하지 않았습니다.\n\n"
 "* 경고 474건 각각의 그룹·Facing·원본 타일 ID·스프라이트 좌표·Wiki 실제 명칭·분류·수납 출처를 정규화했습니다.\n"
 "* 수납 관련 1,855개 링크를 본래 TileDef 원문과 교차 검증하여 직접 ID·동명 추정·원본만 있는 링크를 분리했습니다.\n"
 "* 11개 위키 미연결과 기존 후보는 증거로 보관하지만 확정 ID 0개입니다.\n"
 "* 동명 그룹을 합치거나 수납 용량을 합산하지 않았습니다. 474 경고를 해결했다고 주장하지 않습니다.\n"
 "* HTML 검토기는 텍스트 기반으로, 신규 원본 PNG를 시각 관찰했다는 기록이 아닙니다.\n"
 "* Work의 107그룹/574타일 기록은 별도 열람 보고이며 저장된 개별 이미지 결과 0건입니다.\n"
 "* Game Moveable identity, Lua loot, 마인크래프트 구현은 미확정이며, 원본은 변경하지 않았습니다.\n",encoding="utf8")
 with zipfile.ZipFile(PACK,"w",zipfile.ZIP_DEFLATED,compresslevel=5) as z:
  for path in sorted(OUT.iterdir()):
   if path.is_file() and path!=PACK:z.write(path,path.name)
 with zipfile.ZipFile(PACK) as z:
  assert z.testzip() is None and DB.name in z.namelist()
 print("V13_FURNITURE_SOURCE_TRIAGE_SUCCESS",js(manifest),flush=True)
if __name__=="__main__":
 main()
