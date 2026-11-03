#!/usr/bin/env python3
"""Analyze ambiguous shared TileDef groups and crop real original sprite images.
Do not merge game furniture or select a Minecraft implementation.
"""
from pathlib import Path
from collections import Counter,defaultdict
from functools import lru_cache
import csv,json,hashlib,sqlite3,shutil,zipfile,html
from PIL import Image

ROOT=Path(__file__).resolve().parents[1]
SOURCE=ROOT/"analysis/furniture_full_b42/2026-11-03/wiki_first_v2/B42_WIKI_FIRST_FURNITURE_REGISTRY.zip"
OUT=ROOT/"analysis/furniture_full_b42/2026-11-03/collision_review_v3"
DB=OUT/"PZ_B42_FURNITURE_IDENTITY_AUDIT.sqlite"
PREV=OUT/"source_sprite_crops"

def values(rows):
 return [dict(r) for r in rows]
def joined(items):
 return "|".join(sorted(set(str(i) for i in items if i not in (None,""))))
def csvout(path,items):
 if not items:raise AssertionError("empty "+str(path))
 with path.open("w",encoding="utf-8-sig",newline="") as f:
  w=csv.DictWriter(f,list(items[0]));w.writeheader();w.writerows(items)
def digest(ks):
 return hashlib.sha256("\x1e".join(sorted(ks)).encode()).hexdigest()[:16].upper()
def pattern(anchors,names):
 aa=list(anchors.values())
 if all(x==aa[0] for x in aa):
  return "SAME_IMAGE_IDS_SAME_NAME" if len(set(names.values()))==1 else "SAME_IMAGE_IDS_DIFFERENT_NAMES"
 return "OVERLAPPING_IMAGE_IDS" if any(x&y for i,x in enumerate(aa) for j,y in enumerate(aa) if j>i) else "DISJOINT_IMAGE_IDS"
def orient(anchors,source):
 sets=[]
 for a in anchors.values():
  s=set()
  for k in a:
   s|=set(x for x in (source[k]["Facing"] or "").split("|") if x)
  sets.append(s)
 if any(not s for s in sets):return "FACING_NOT_RECORDED"
 if all(not x&y for i,x in enumerate(sets) for j,y in enumerate(sets) if j>i):return "DISJOINT_FACING_POSSIBLE_ROTATION"
 if all(x==sets[0] for x in sets):return "SAME_FACING_POSSIBLE_DESIGN_VARIANTS"
 return "MIXED_FACING_REQUIRES_REVIEW"
@lru_cache(maxsize=4)
def loadatlas(path):
 return Image.open(ROOT/path).convert("RGBA")
def main():
 assert not OUT.exists(),"No overwrite"
 OUT.mkdir(parents=True)
 PREV.mkdir()
 with zipfile.ZipFile(SOURCE) as z:
  assert z.testzip() is None
  with z.open("PZ_B42_FURNITURE_REGISTRY_WIKI_FIRST.sqlite") as s,DB.open("wb") as f:
   shutil.copyfileobj(s,f)
 con=sqlite3.connect(DB)
 con.row_factory=sqlite3.Row
 assert con.execute("PRAGMA integrity_check").fetchone()[0]=="ok"
 assert con.execute("SELECT COUNT(*) FROM registry_entry").fetchone()[0]==2231
 assert con.execute("SELECT COUNT(*) FROM source_attributes").fetchone()[0]==195265
 con.executescript("""
 CREATE TABLE audit_group_collision(
  group_id TEXT PRIMARY KEY,source_tile_set TEXT,CustomName TEXT,GroupName TEXT,
  collision_type TEXT NOT NULL,source_facing_relation TEXT NOT NULL,
  wiki_id_count INTEGER NOT NULL,source_tile_count INTEGER NOT NULL,
  original_container TEXT,original_capacity TEXT,
  game_identity_confirmed INTEGER NOT NULL DEFAULT 0
 );
 CREATE TABLE audit_wiki_listing(
  group_id TEXT NOT NULL,wiki_id TEXT NOT NULL,wiki_name TEXT,
  wiki_category TEXT,wiki_article TEXT,wiki_image TEXT,
  exact_original_tile_ids TEXT NOT NULL,source_facing TEXT,source_grid TEXT,
  duplicate_listing_of TEXT,physical_furniture_same_verified INTEGER NOT NULL DEFAULT 0,
  PRIMARY KEY(group_id,wiki_id)
 );
 CREATE TABLE audit_source_sprite(
  group_id TEXT NOT NULL,source_key TEXT NOT NULL,facing TEXT,
  sprite_grid_pos TEXT,container_type TEXT,capacity_raw TEXT,
  source_atlas TEXT,native_crop TEXT,
  PRIMARY KEY(group_id,source_key)
 );
 CREATE TABLE audit_repeated_wiki_listing(
  group_id TEXT NOT NULL,canonical_wiki_id TEXT NOT NULL,
  duplicate_wiki_id TEXT NOT NULL,exact_image_signature TEXT NOT NULL,
  physical_furniture_same_verified INTEGER NOT NULL DEFAULT 0,
  PRIMARY KEY(group_id,duplicate_wiki_id)
 );
 """)
 groups={x["group_id"]:x for x in values(con.execute("SELECT * FROM furniture_group"))}
 wikimap={x["wiki_id"]:x for x in values(con.execute("SELECT * FROM wiki_furniture"))}
 count=defaultdict(set)
 for r in values(con.execute("SELECT group_id,wiki_id FROM wiki_group_candidate")):
  if not r["group_id"].startswith("FUR-WIKI-"):count[r["group_id"]].add(r["wiki_id"])
 flagged={k:sorted(v) for k,v in count.items() if len(v)>1}
 assert len(flagged)==129,len(flagged)
 sources=defaultdict(dict)
 for r in values(con.execute("SELECT * FROM furniture_tile")):
  if r["group_id"] in flagged:
   sources[r["group_id"]][r["source_key"].casefold()]=r
 crops={}
 errors=[]
 def extract(k):
  if k in crops:return crops[k]
  try:
   n,i=k.rsplit("/",1)
   v=int(i)
  except ValueError:return ""
  rows=con.execute("""SELECT c.png_path,c.column_index,c.row_index,
   a.cell_width,a.cell_height,c.has_visible_pixels
   FROM image_cells c JOIN image_atlases a ON a.png_path=c.png_path
   WHERE lower(c.tileset)=? AND c.local_id=?
   ORDER BY c.has_visible_pixels DESC,c.png_path""",(n,v)).fetchall()
  for r in rows:
   if not int(r["has_visible_pixels"]):continue
   f=ROOT/r["png_path"]
   if not f.is_file():continue
   try:
    im=loadatlas(r["png_path"])
    cw,ch=r["cell_width"],r["cell_height"]
    x,y=r["column_index"]*cw,r["row_index"]*ch
    assert cw>0 and ch>0 and x+cw<=im.width and y+ch<=im.height
    frame=im.crop((x,y,x+cw,y+ch))
    frame.thumbnail((148,200),resample=Image.Resampling.NEAREST)
    name=k.replace("/","__")+".webp"
    frame.save(PREV/name,"WEBP",lossless=True,method=4)
    crops[k]="source_sprite_crops/"+name
    return crops[k]
   except Exception as exc:
    errors.append(dict(source_key=k,png_path=r["png_path"],error=str(exc)))
  return ""

 classifications=Counter()
 groupout=[];wikiout=[];srcout=[];repeat=[];disjoint=[];view=[]
 for gid,ids in sorted(flagged.items()):
  src=sources[gid]
  assert src and all(k in src for k in src)
  anchor={}
  for wid in ids:
   reported=[x["source_key"].casefold() for x in values(con.execute(
    "SELECT source_key FROM wiki_image_tile WHERE wiki_id=? AND matching_status='SOURCE_ID_FOUND'",(wid,)))]
   anchor[wid]=set(x for x in reported if x in src)
   assert anchor[wid],(gid,wid)
  names={wid:wikimap[wid]["name"] for wid in ids}
  kind=pattern(anchor,names)
  direction=orient(anchor,src)
  classifications[kind]+=1
  sigmap=defaultdict(list)
  for wid in ids:sigmap[(names[wid],digest(anchor[wid]))].append(wid)
  canon={}
  for (_,sig),members in sigmap.items():
   root=min(members)
   for wid in members:
    canon[wid]=root
    if wid!=root:
     item=dict(group_id=gid,canonical_wiki_id=root,duplicate_wiki_id=wid,
       wiki_name=names[wid],same_original_sprite_keys=joined(anchor[wid]),
       source_signature=sig,
       rationale="SAME_WIKI_NAME_AND_EXACT_IMAGE_SOURCE_IDS_NOT_PROOF_OF_SAME_3D_MODEL")
     repeat.append(item)
     con.execute("INSERT INTO audit_repeated_wiki_listing VALUES(?,?,?,?,0)",(gid,root,wid,sig))
  co=joined(x["container_type"] for x in src.values())
  cap=joined(x["ContainerCapacity"] for x in src.values())
  g=groups[gid]
  con.execute("INSERT INTO audit_group_collision VALUES(?,?,?,?,?,?,?,?,?,?,0)",
   (gid,g["tileset"],g["custom_name"],g["group_name"],kind,direction,len(ids),len(src),co,cap))
  rec=dict(group_id=gid,tileset=g["tileset"],CustomName=g["custom_name"],GroupName=g["group_name"],
   wiki_row_count=len(ids),wiki_ids=joined(ids),wiki_names=joined(names.values()),
   wiki_categories=joined(wikimap[i]["category"] for i in ids),
   classification=kind,facing_relation=direction,
   exact_wiki_source_tile_ids=joined(k for a in anchor.values() for k in a),
   full_name_group_source_tile_ids=joined(src),
   source_sprite_count=len(src),original_container_type=co,
   original_capacity=cap,
   duplicate_wiki_row_ids=joined(x for x in ids if canon[x]!=x),
   object_identity_verified="NO")
  groupout.append(rec)
  if kind in ("DISJOINT_IMAGE_IDS","OVERLAPPING_IMAGE_IDS"):disjoint.append(rec)
  sourcecard={}
  for key,x in sorted(src.items()):
   crop=extract(key)
   sourcecard[key]={"key":x["source_key"],"crop":crop,
    "Facing":x["Facing"],"Grid":x["SpriteGridPos"]}
   row=dict(group_id=gid,source_key=x["source_key"],Facing=x["Facing"],
    SpriteGridPos=x["SpriteGridPos"],container=x["container_type"],
    capacity=x["ContainerCapacity"],original_png=x["source_png_paths"],crop_path=crop)
   srcout.append(row)
   con.execute("INSERT INTO audit_source_sprite VALUES(?,?,?,?,?,?,?,?)",
    (gid,x["source_key"],x["Facing"],x["SpriteGridPos"],x["container_type"],
     x["ContainerCapacity"],x["source_png_paths"],crop))
  links=[]
  for wid in ids:
   w=wikimap[wid]
   keys=sorted(anchor[wid])
   facer=joined(src[k]["Facing"] for k in keys)
   grids=joined(src[k]["SpriteGridPos"] for k in keys)
   dupe=canon[wid] if canon[wid]!=wid else None
   row=dict(group_id=gid,wiki_id=wid,name=w["name"],category=w["category"],
    article_url=w["article_url"],original_wiki_image=w["image_url"],
    exact_source_keys=joined(keys),facing=facer,grid_positions=grids,
    repeated_listing_of=dupe or "",same_game_object_verified="NO")
   wikiout.append(row)
   con.execute("INSERT INTO audit_wiki_listing VALUES(?,?,?,?,?,?,?,?,?,?,0)",
    (gid,wid,w["name"],w["category"],w["article_url"],w["image_url"],
     joined(keys),facer,grids,dupe))
   links.append({"id":wid,"name":w["name"],"category":w["category"],
    "article":w["article_url"],"wiki_image":w["image_url"],
    "anchor":keys,"faces":facer,"grid":grids,"duplicate_of":dupe,
    "source_crops":[sourcecard[k] for k in keys]})
  view.append(dict(id=gid,name=(g["group_name"] or "")+" "+(g["custom_name"] or ""),
   tileset=g["tileset"],kind=kind,orient=direction,storage=co,capacity=cap,
   items=links))
 assert classifications==Counter({
  "SAME_IMAGE_IDS_SAME_NAME":63,
  "SAME_IMAGE_IDS_DIFFERENT_NAMES":6,
  "OVERLAPPING_IMAGE_IDS":2,
  "DISJOINT_IMAGE_IDS":58
 }),dict(classifications)
 assert len(groupout)==129
 con.commit()
 assert con.execute("PRAGMA integrity_check").fetchone()[0]=="ok"
 assert con.execute("SELECT COUNT(*) FROM source_attributes").fetchone()[0]==195265
 assert con.execute("SELECT COUNT(*) FROM wiki_furniture").fetchone()[0]==1268
 assert con.execute("SELECT COUNT(*) FROM registry_entry_container").fetchone()[0]==1855
 assert con.execute("SELECT COUNT(*) FROM future_item_distribution").fetchone()[0]==0
 assert con.execute("SELECT COUNT(*) FROM future_minecraft_implementation").fetchone()[0]==0
 assert con.execute("SELECT COUNT(*) FROM audit_group_collision").fetchone()[0]==129
 con.close()
 csvout(OUT/"129_GROUP_COLLISIONS_CLASSIFIED.csv",groupout)
 csvout(OUT/"WIKI_ROWS_WITH_EXACT_TILE_ID_EVIDENCE.csv",wikiout)
 csvout(OUT/"ORIGINAL_TILE_CROP_AND_PROPERTIES.csv",srcout)
 csvout(OUT/"EXACT_DUPLICATE_WIKI_LISTINGS.csv",repeat)
 csvout(OUT/"DISTINCT_OR_OVERLAPPING_TILE_ID_GROUPS.csv",disjoint)
 if errors:csvout(OUT/"ORIGINAL_CROP_ERRORS.csv",errors)
 def h(x):return html.escape(str(x or ""),quote=True)
 s=['<!doctype html><html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">',
 '<title>129개 Project Zomboid 원본 가구 중복 검수</title>',
 '<style>body{font:14px system-ui,sans-serif;background:#e9eff2;color:#233745;margin:0}',
 'header{background:white;padding:16px 3%;position:sticky;top:0;border-bottom:1px solid #cbd6e0}h1{font-size:23px}',
 'main{padding:14px 3%;display:grid;grid-template-columns:repeat(auto-fill,minmax(min(100%,470px),1fr));gap:14px}',
 'details{background:white;border:1px solid #d6e0e7;border-radius:10px;padding:12px}',
 'summary{cursor:pointer;font-size:17px;font-weight:bold}section{padding:8px;background:#f4f7f9;margin:8px 0;border-radius:7px}',
 'p{font-size:12px;line-height:1.5;color:#4a6275}.thumbs{display:flex;gap:9px;flex-wrap:wrap}',
 '.thumb{background:white;padding:7px;max-width:155px;border-radius:7px;text-align:center}',
 'img{display:block;width:140px;height:180px;object-fit:contain;image-rendering:pixelated}',
 'code{font-size:11px;overflow-wrap:anywhere}a{color:#075a93}</style></head><body>',
 '<header><h1>B42 가구 정체 중복 129그룹 원본 타일 비교</h1>',
 '<p>이 이미지는 원본 Tiles PNG에서 타일 정의 그리드대로 잘라낸 실제 스프라이트이며 AI가 만든 3D 이미지가 아님.',
 '동일한 게임 가구/모델인지 수동 판정은 아직 진행 전.</p></header><main>']
 for record in view:
  s.append('<details><summary>'+h(record["name"])+' · '+h(record["kind"])+'</summary>')
  s.append('<p>'+h(record["tileset"])+' / 원본 수납 '+h(record["storage"] or "미기록")+
   ' / 원본 용량 '+h(record["capacity"] or "미기록")+' / 방향 '+h(record["orient"])+'</p>')
  for w in record["items"]:
   s.append('<section><b>'+h(w["id"])+' · '+h(w["name"])+'</b>')
   if w["duplicate_of"]:s.append('<p>위키 중복 기록 기준 ID: '+h(w["duplicate_of"])+'</p>')
   s.append('<p>'+h(w["category"])+' · Facing '+h(w["faces"] or "미기록")+
    ' · <a href="'+h(w["article"])+'" target="_blank" rel="noopener">PZwiki 문서</a> · '+
    '<a href="'+h(w["wiki_image"])+'" target="_blank" rel="noopener">위키 이미지</a></p>')
   s.append('<div class="thumbs">')
   for img in w["source_crops"]:
    s.append('<div class="thumb">'+
     ('<img loading="lazy" src="'+h(img["crop"])+'" alt="original sprite"/>' if img["crop"] else '<p>미연결 이미지</p>')+
     '<code>'+h(img["key"])+'</code><p>Facing '+h(img["Facing"] or "?")+
     ' · Grid '+h(img["Grid"] or "-")+'</p></div>')
   s.append('</div></section>')
  s.append('</details>')
 s.append('</main></body></html>')
 (OUT/"ORIGINAL_SPRITE_COMPARE_129.html").write_text("".join(s),encoding="utf8")
 manifest=dict(
  collision_groups=len(groupout),
  collision_types=dict(classifications),
  wiki_entries_in_collision_groups=len(wikiout),
  exact_duplicate_wiki_alias_relationships=len(repeat),
  groups_requiring_disjoint_or_overlap_review=len(disjoint),
  original_tile_sprite_evidence_rows=len(srcout),
  actual_original_sprite_crops=len(crops),
  native_crop_missing=len(srcout)-len(crops),
  crop_errors=len(errors),
  original_source_attribute_rows_preserved=195265,
  original_wiki_rows_preserved=1268,
  original_v2_registry_rows_preserved=2231,
  original_v2_storage_attribute_link_rows_preserved=1855,
  manual_game_object_identity_checks_confirmed=0,
  original_source_data_modified=False,
  minecraft_block_entity_model_decision="UNDECIDED",
  sqlite_integrity="ok")
 (OUT/"MANIFEST.json").write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+"\n",encoding="utf8")
 readme=[
 "# 전체 가구 정체 검수 v3 — 같은 TileDef 그룹을 공유하는 Wiki 항목 129그룹",
 "이 결과는 기존 B42 전체 가구 원장 v2의 원본 DB를 보존하면서 위키의 중복 행과 실제 다른 원본 타일 번호를 구분하는 작업이다.",
 "## 직접 확인한 타일 ID 중복 유형"
 ]
 for k,v in sorted(classifications.items(),key=lambda x:-x[1]):
  readme.append("- "+k+": "+str(v)+"그룹")
 readme.extend([
 "같은 이름+같은 타일 ID인 경우 위키의 동일 항목 반복 기재로 볼 근거가 충분하지만 원문 Wiki 행은 삭제하지 않고 canonical row로 참조만 한다. 게임 내 단일 3D/가구임을 인증하지는 않는다.",
 "같은 TileDef 그룹인데 직접 이미지 ID가 다르면 다른 방향인지, 상태 변형인지, 실물 디자인이 다른지는 별도 분류가 필요하다. 특히 GroupName과 CustomName만 같다는 이유로 자동 병합하지 않는다.",
 "## 원본 이미지 증거",
 "원본 Tiles/ PNG + v259의 image_cells, image_atlases에 기록된 ID, 그리드 좌표, 픽셀 크기를 이용해 실제 스프라이트 크롭 이미지 "+str(len(crops))+"장을 생성했다.",
 "웹 접근 없이도 HTML과 함께 ZIP으로 열어 129그룹을 방향·부품·원본 픽셀로 비교할 수 있다. PZwiki 외부 문서 링크는 인터넷이 있어야 한다.",
 "## 자료 파일",
 "- PZ_B42_FURNITURE_COLLISION_AUDIT_V3.zip: 원본 v2 SQLite 내용 + 검토 증거 + 실제 원본 스프라이트 크롭이 들어 있는 통합 자료.",
 "- ORIGINAL_SPRITE_COMPARE_129.html: 129그룹의 원본 이미지 비교.",
 "- 129_GROUP_COLLISIONS_CLASSIFIED.csv: 그룹별 충돌 유형, 모든 원본 소스 타일, 원본 수납속성.",
 "- WIKI_ROWS_WITH_EXACT_TILE_ID_EVIDENCE.csv: Wiki 항목별 확인된 타일 번호/방향/그리드 및 문서 URL.",
 "- EXACT_DUPLICATE_WIKI_LISTINGS.csv: 위키 중복 등재 관계.",
 "- DISTINCT_OR_OVERLAPPING_TILE_ID_GROUPS.csv: 다른 실제 가구 여부를 추가 확인할 문제 그룹.",
 "- ORIGINAL_TILE_CROP_AND_PROPERTIES.csv: 타일 ID별 원본 스프라이트, Facing, SpriteGridPos, container, 용량.",
 "## 하지 않은 작업",
 "게임 내 IsoObject 및 IsoSpriteGrid 생성/회전 검증, 완제품 3D 시각 동일성 인증, 963개의 위키 미등재 소스 그룹 전수 시각검토, Lua 방별 아이템 생성, Minecraft 구현은 이번 단계에서 완료하지 않았다.",
 "원본 TileDef/PZwiki/TMX/이전 DB의 가구 분류와 수납 아이템 생성 규칙은 변경하지 않았다."
 ])
 (OUT/"README_KO.md").write_text("\n\n".join(readme)+"\n",encoding="utf8")
 with zipfile.ZipFile(OUT/"PZ_B42_FURNITURE_COLLISION_AUDIT_V3.zip","w",zipfile.ZIP_DEFLATED,compresslevel=5) as z:
  for path in sorted(OUT.rglob("*")):
   if path.is_file() and path.name!="PZ_B42_FURNITURE_COLLISION_AUDIT_V3.zip":z.write(path,path.relative_to(OUT))
 with zipfile.ZipFile(OUT/"PZ_B42_FURNITURE_COLLISION_AUDIT_V3.zip") as z:
  assert z.testzip() is None
  assert "ORIGINAL_SPRITE_COMPARE_129.html" in z.namelist()
  assert "PZ_B42_FURNITURE_IDENTITY_AUDIT.sqlite" in z.namelist()
 print("IDENTITY_129_AUDIT_COMPLETE",json.dumps(manifest,ensure_ascii=False),flush=True)
if __name__=="__main__":main()
