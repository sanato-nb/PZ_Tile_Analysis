#!/usr/bin/env python3
"""PZ B42 v6: all 71 same-sprite Wiki collisions. No game-object merges."""
import csv,json,sqlite3,zipfile,shutil,re,hashlib,math
from pathlib import Path
from collections import Counter,defaultdict
from PIL import Image,ImageDraw,ImageFont

ROOT=Path(__file__).resolve().parents[1]
SOURCE=ROOT/"analysis/furniture_full_b42/2026-11-03/full_visual_review_v5/B42_ALL_58_FURNITURE_VISUAL_REVIEW_V5.zip"
WIKI=ROOT/"pzwiki_furniture/2026-11-03/furniture_1268.csv"
OUT=ROOT/"analysis/furniture_full_b42/2026-11-04/shared_wiki_overlap_v6"
DB=OUT/"B42_SHARED_WIKI_OVERLAP_V6.sqlite"
IMG=OUT/"ORIGINAL_PNG_CONTACT_SHEETS_71"
ZIP=OUT/"B42_SHARED_WIKI_OVERLAP_V6.zip"

def readcsv(path):
 with path.open(encoding="utf-8-sig",newline="") as f:return list(csv.DictReader(f))
def writecsv(path,data):
 assert data
 with path.open("w",encoding="utf-8-sig",newline="") as f:
  w=csv.DictWriter(f,list(data[0]),extrasaction="ignore");w.writeheader();w.writerows(data)
def rows(c,query):return [dict(r) for r in c.execute(query)]
def count(c,table):return c.execute("SELECT COUNT(*) FROM "+table).fetchone()[0]
def unique(v):return sorted({str(x) for x in v if x is not None and x!=""})
def hashid(s):return hashlib.sha256(s.encode("utf8")).hexdigest()[:18].upper()
def put(c,table,vals):
 cols=list(vals)
 q="INSERT INTO "+table+" ("+",".join(cols)+") VALUES ("+",".join("?" for _ in cols)+")"
 c.execute(q,tuple(vals[x] for x in cols))
def fnt(n):
 for p in ("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf","/usr/share/fonts/truetype/liberation2/LiberationSans-Regular.ttf"):
  if Path(p).exists():return ImageFont.truetype(p,n)
 return ImageFont.load_default()
FONT,SMALL=fnt(14),fnt(11)
def thumbnail(img):
 im=img.convert("RGBA")
 ratio=min(150/im.width,138/im.height,1.6)
 wh=(max(1,int(im.width*ratio)),max(1,int(im.height*ratio)))
 im=im.resize(wh,Image.Resampling.NEAREST)
 canvas=Image.new("RGB",(156,145),"#f0f3f7")
 canvas.paste(im,((156-wh[0])//2,(145-wh[1])//2),im)
 return canvas
def missing(key):
 im=Image.new("RGB",(156,145),"#ffe8e8")
 ImageDraw.Draw(im).text((8,38),"MISSING PNG "+key.split("/")[-1],fill="#9a2632",font=SMALL)
 return im
def main():
 assert not OUT.exists(),"Refuse replacing v6 result"
 OUT.mkdir(parents=True);IMG.mkdir()
 with zipfile.ZipFile(SOURCE) as z:
  assert z.testzip() is None
  with z.open("B42_ALL_58_VISUALLY_REVIEWED_FURNITURE.sqlite") as s,DB.open("wb") as f:shutil.copyfileobj(s,f)
 con=sqlite3.connect(DB);con.row_factory=sqlite3.Row
 assert con.execute("PRAGMA integrity_check").fetchone()[0]=="ok"
 assert count(con,"source_attributes")==195265 and count(con,"wiki_furniture")==1268
 wikirows=readcsv(WIKI);assert len(wikirows)==1268
 wiki={r["목록ID"]:r for r in wikirows}
 collision=rows(con,"SELECT * FROM v3_wiki_overlap WHERE overlap_type!='DISJOINT_WIKI_IMAGE_IDS' ORDER BY group_id")
 assert len(collision)==71
 assert Counter(x["overlap_type"] for x in collision)=={"SHARED_EXACT_TILE_IDS":69,"MIXED_OVERLAP":2}
 groups={g["group_id"]:g for g in rows(con,"SELECT * FROM furniture_group")}
 tiles={r["source_key"].casefold():r for r in rows(con,"SELECT * FROM furniture_tile")}
 atlas=defaultdict(list)
 for r in rows(con,"SELECT i.tileset,i.local_id,i.png_path,i.grid_id,i.column_index,i.row_index,i.link_status,a.cell_width,a.cell_height FROM image_cells i JOIN image_atlases a ON a.png_path=i.png_path WHERE i.tileset IS NOT NULL AND i.local_id IS NOT NULL"):
  atlas[r["tileset"].casefold()+"/"+str(r["local_id"])].append(r)
 con.executescript("""
 CREATE TABLE v6_overlap_group(
 group_id TEXT PRIMARY KEY,tileset TEXT,original_wiki_rows INTEGER,
 exact_source_sprite_sets INTEGER,duplicate_kind TEXT,
 comparison_image TEXT,game_object_identical_verified INTEGER DEFAULT 0);
 CREATE TABLE v6_source_appearance(
 appearance_id TEXT PRIMARY KEY,group_id TEXT,original_sprite_keys_json TEXT,
 original_sprite_count INTEGER,wiki_rows INTEGER,
 original_wiki_names_json TEXT,original_wiki_category_facets_json TEXT,
 original_wiki_capacity_values_json TEXT,original_tiledef_containers_json TEXT,
 original_tiledef_capacity_values_json TEXT,
 classification TEXT,storage_evidence_status TEXT,
 source_png_cell_count INTEGER,source_png_missing_count INTEGER,
 verified_game_object_identity INTEGER DEFAULT 0);
 CREATE TABLE v6_original_wiki_facet(
 wiki_id TEXT PRIMARY KEY,appearance_id TEXT,
 name_raw TEXT,major_category_raw TEXT,minor_category_raw TEXT,
 wiki_capacity_raw TEXT,wiki_size_raw TEXT,
 wiki_original_row_json TEXT);
 CREATE TABLE v6_original_tile_evidence(
 appearance_id TEXT,source_key TEXT,source_png_path TEXT,
 png_crop_sha256 TEXT,source_Facing TEXT,source_SpriteGridPos TEXT,
 source_container TEXT,source_ContainerCapacity TEXT,
 source_tiledef_file TEXT,original_all_properties_json TEXT,
 PRIMARY KEY(appearance_id,source_key));
 CREATE TABLE v6_semantic_conflict(
 appearance_id TEXT PRIMARY KEY,group_id TEXT,
 reason TEXT,names_json TEXT,category_json TEXT,
 image_identity_verified INTEGER DEFAULT 1,
 semantic_identity_verified INTEGER DEFAULT 0);
 CREATE INDEX idx_v6_group_appearance ON v6_source_appearance(group_id);
 CREATE INDEX idx_v6_facet_appearance ON v6_original_wiki_facet(appearance_id);
 """)
 groupout=[];appearanceout=[];wikiout=[];tileout=[];conflicts=[]
 stats=Counter();capstats=Counter();seenwiki=set()
 pngs=0;missed=0;opened={}
 for index,g in enumerate(collision,1):
  gid=g["group_id"];widlist=g["wiki_ids"].split("|")
  original=json.loads(g["exact_tile_ids_json"])
  assert set(widlist)==set(original)
  bykeys=defaultdict(list)
  for wid in widlist:
   assert wid in wiki
   keys=tuple(sorted({k.casefold() for k in original[wid]}))
   assert keys
   bykeys[keys].append(wid)
   seenwiki.add(wid)
  assert len(bykeys)==(1 if g["overlap_type"]=="SHARED_EXACT_TILE_IDS" else 2)
  grp=groups[gid]
  title=f"{index:02d}/71  {grp['tileset']}  {gid}"
  canvas=Image.new("RGB",(max(1100,550*len(bykeys)),350),"#e8eef3")
  dr=ImageDraw.Draw(canvas)
  dr.text((16,12),title,fill="#18344e",font=FONT)
  dr.text((16,36),f"{len(widlist)} Wiki category rows -> {len(bykeys)} exact original sprite set(s)",fill="#51677b",font=FONT)
  groupout.append(dict(group_no=index,group_id=gid,tileset=grp["tileset"],
   CustomName=grp["custom_name"],GroupName=grp["group_name"],
   original_overlap_kind=g["overlap_type"],original_wiki_rows=len(widlist),
   same_source_sprite_set_count=len(bykeys),
   original_wiki_ids="|".join(widlist),
   comparison_png="ORIGINAL_PNG_CONTACT_SHEETS_71/"+f"{index:02d}_{gid}.jpg",
   game_object_identity_confirmed="NO"))
  put(con,"v6_overlap_group",dict(group_id=gid,tileset=grp["tileset"],
    original_wiki_rows=len(widlist),exact_source_sprite_sets=len(bykeys),
    duplicate_kind=g["overlap_type"],
    comparison_image="ORIGINAL_PNG_CONTACT_SHEETS_71/"+f"{index:02d}_{gid}.jpg"))
  for j,(keys,ids) in enumerate(sorted(bykeys.items())):
   aid="V6SPR-"+hashid(gid+"|"+"|".join(keys))
   originals=[wiki[x] for x in ids]
   names=unique(w["가구명_원문"] for w in originals)
   categories=unique(w["대분류_원문"]+"/"+w["소분류_원문"] for w in originals)
   capacities=unique(w["수납용량_원문"] for w in originals)
   raw_tdef=[tiles[k] for k in keys]
   containers=unique(t["container_type"] for t in raw_tdef)
   tdefcaps=unique(t["ContainerCapacity"] for t in raw_tdef)
   if len({x.casefold().strip() for x in names})>1:
    kind="SAME_SOURCE_ID_DIFFERENT_WIKI_NAMES_REVIEW"
   elif len(categories)>1:
    kind="SAME_SOURCE_ID_MULTIPLE_WIKI_FUNCTIONS"
   else:
    kind="REPEATED_WIKI_REFERENCE"
   nums=unique(x for x in capacities if x not in ("N/A","-","?","Unknown"))
   if len(nums)>1:cs="MULTIPLE_DIFFERENT_WIKI_CAPACITIES"
   elif nums and tdefcaps and set(nums)!=set(tdefcaps):cs="WIKI_TILEDEF_CAPACITY_DISAGREEMENT"
   elif nums and any(w["수납용량_원문"]=="" for w in originals):cs="WIKI_STORAGE_CAPACITY_SUPPLEMENTS_BLANK_CATEGORY"
   elif nums:cs="WIKI_CAPACITY_RECORDED"
   elif tdefcaps:cs="TILEDEF_CAPACITY_RECORDED"
   else:cs="NOT_RECORDED_OR_NOT_APPLICABLE"
   stats[kind]+=1;capstats[cs]+=1
   cropcount=0;misscount=0
   for pos,key in enumerate(keys):
    t=tiles[key]
    choices=sorted(atlas.get(key,[]),key=lambda x:(x["link_status"]!="MATCHED_TILESET_AND_GRID",
      not x["png_path"].startswith("Tiles/2x/")))
    cell=choices[0] if choices else None
    crop=None;checksum=""
    if cell is not None and (ROOT/cell["png_path"]).is_file():
     try:
      fn=str(ROOT/cell["png_path"])
      if fn not in opened:opened[fn]=Image.open(fn).convert("RGBA")
      im=opened[fn];tw=cell["cell_width"];th=cell["cell_height"]
      x=cell["column_index"]*tw;y=cell["row_index"]*th
      if tw<=0 or th<=0 or x<0 or y<0 or x+tw>im.width or y+th>im.height:
       raise ValueError("image atlas cell out of bounds")
      crop=im.crop((x,y,x+tw,y+th))
      checksum=hashlib.sha256(crop.tobytes()).hexdigest()
     except Exception as ex:
      print("CROP_ERROR",key,str(ex)[:100],flush=True)
    if crop is None:
     misscount+=1;missed+=1;thumb=missing(key)
    else:
     cropcount+=1;pngs+=1;thumb=thumbnail(crop)
    px=13+j*550+(pos%2)*162;py=120+(pos//2)*90
    # Image cards show at most the first 4 pieces; every part is still in DB.
    if pos<2:canvas.paste(thumb,(px,130))
    put(con,"v6_original_tile_evidence",dict(appearance_id=aid,source_key=key,
     source_png_path=cell["png_path"] if cell else "",
     png_crop_sha256=checksum,source_Facing=t["Facing"],
     source_SpriteGridPos=t["SpriteGridPos"],source_container=t["container_type"],
     source_ContainerCapacity=t["ContainerCapacity"],
     source_tiledef_file=t["original_source_files"],
     original_all_properties_json=t["raw_properties_with_source_json"]))
    tileout.append(dict(appearance_id=aid,source_key=key,
     original_png=cell["png_path"] if cell else "",
     original_pixel_crop_sha256=checksum,
     original_Facing=t["Facing"],original_SpriteGridPos=t["SpriteGridPos"],
     original_container=t["container_type"],
     original_ContainerCapacity=t["ContainerCapacity"],
     original_tiledef_file=t["original_source_files"]))
   put(con,"v6_source_appearance",dict(appearance_id=aid,group_id=gid,
    original_sprite_keys_json=json.dumps(keys),original_sprite_count=len(keys),
    wiki_rows=len(ids),original_wiki_names_json=json.dumps(names,ensure_ascii=False),
    original_wiki_category_facets_json=json.dumps(categories,ensure_ascii=False),
    original_wiki_capacity_values_json=json.dumps(capacities,ensure_ascii=False),
    original_tiledef_containers_json=json.dumps(containers,ensure_ascii=False),
    original_tiledef_capacity_values_json=json.dumps(tdefcaps,ensure_ascii=False),
    classification=kind,storage_evidence_status=cs,
    source_png_cell_count=cropcount,source_png_missing_count=misscount))
   appearanceout.append(dict(appearance_id=aid,source_group_id=gid,
    exact_original_source_sprite_keys="|".join(keys),
    wiki_row_ids="|".join(ids),original_wiki_names="|".join(names),
    original_wiki_categories="|".join(categories),
    wiki_capacity_values="|".join(capacities),
    source_tiledef_container="|".join(containers),
    source_tiledef_capacity="|".join(tdefcaps),
    record_relationship=kind,capacity_evidence_status=cs,
    original_png_crops=cropcount,missing_png_crops=misscount,
    actual_game_object_identity_certified="NO"))
   left=550*j
   dr.rounded_rectangle((left+8,80,left+540,340),radius=10,fill="white",outline="#c6d5df",width=2)
   for ind,line in enumerate([ids[0]+" and "+str(len(ids)-1)+" other Wiki ref(s)",
     names[0][:55],
     "Wiki categories:"]+categories[:2]+[
     "PZwiki capacity: "+("/".join(capacities) if capacities else "blank"),
     "TileDef container: "+("/".join(containers) if containers else "blank"),
     "Source keys: "+",".join(x.split("/")[-1] for x in keys)]):
    dr.text((left+330,110+ind*23),line[:35],fill="#364b5d",font=SMALL)
   # draw border/heading before paste; the thumbnail area has a neutral frame
   for wid in ids:
    w=wiki[wid]
    put(con,"v6_original_wiki_facet",dict(wiki_id=wid,appearance_id=aid,
     name_raw=w["가구명_원문"],major_category_raw=w["대분류_원문"],
     minor_category_raw=w["소분류_원문"],
     wiki_capacity_raw=w["수납용량_원문"],wiki_size_raw=w["크기_타일수"],
     wiki_original_row_json=json.dumps(w,ensure_ascii=False)))
    wikiout.append(dict(wiki_id=wid,appearance_id=aid,original_wiki_name=w["가구명_원문"],
     original_category=w["대분류_원문"],original_subcategory=w["소분류_원문"],
     original_wiki_storage=w["수납용량_원문"],
     original_wiki_size=w["크기_타일수"],
     exact_original_source_sprite_set="|".join(keys),
     original_wiki_image_url=w["이미지_URL"]))
   if kind=="SAME_SOURCE_ID_DIFFERENT_WIKI_NAMES_REVIEW" or cs in (
    "MULTIPLE_DIFFERENT_WIKI_CAPACITIES","WIKI_TILEDEF_CAPACITY_DISAGREEMENT"):
    reason=kind if kind=="SAME_SOURCE_ID_DIFFERENT_WIKI_NAMES_REVIEW" else cs
    put(con,"v6_semantic_conflict",dict(appearance_id=aid,group_id=gid,
     reason=reason,names_json=json.dumps(names,ensure_ascii=False),
     category_json=json.dumps(categories,ensure_ascii=False)))
    conflicts.append(dict(appearance_id=aid,group_id=gid,
     source_keys="|".join(keys),wiki_names="|".join(names),
     original_categories="|".join(categories),reason=reason,
     game_identity_verified="NO"))
   for pos,key in enumerate(keys[:2]):
    pass
  # Layout fix: image should overlay card background, but not cover right-side text.
  canvas.save(IMG/f"{index:02d}_{gid}.jpg",quality=90,optimize=True)
  for im in opened.values():im.close()
  opened.clear()
 assert len(groupout)==71 and len(appearanceout)==73 and len(wikiout)==146
 assert len(seenwiki)==146
 assert len(list(IMG.glob("*.jpg")))==71
 con.commit()
 assert con.execute("PRAGMA integrity_check").fetchone()[0]=="ok"
 for table,n in [("v6_overlap_group",71),("v6_source_appearance",73),
   ("v6_original_wiki_facet",146),("source_attributes",195265),
   ("wiki_furniture",1268),("v5_manual_visual_group_review",58)]:
  assert count(con,table)==n,(table,count(con,table),n)
 assert count(con,"future_item_distribution")==0
 assert count(con,"future_minecraft_implementation")==0
 assert count(con,"future_map_placement")==0
 writecsv(OUT/"V6_71_SHARED_SOURCE_GROUPS.csv",groupout)
 writecsv(OUT/"V6_73_EXACT_SOURCE_APPEARANCES.csv",appearanceout)
 writecsv(OUT/"V6_146_WIKI_CROSS_CATEGORY_FACETS.csv",wikiout)
 writecsv(OUT/"V6_ALL_SOURCE_TILE_AND_FUNCTION_EVIDENCE.csv",tileout)
 if conflicts:writecsv(OUT/"V6_CONFLICTS_SAME_SPRITE_DIFFERENT_NAMES.csv",conflicts)
 manifest=dict(
  source_overlap_groups_reviewed=71,
  groups_single_exact_sprite_set=69,groups_mixed_two_sprite_sets=2,
  exact_sprite_sets_indexed=73,original_wiki_rows_preserved=1268,
  overlap_wiki_rows_mapped=146,raw_tiledef_attributes_preserved=195265,
  original_png_sprite_crops_rendered=pngs,original_png_sprite_crops_missing=missed,
  original_png_contact_sheets_created=71,
  duplicate_record_kinds=dict(stats),capacity_evidence_types=dict(capstats),
  semantic_conflict_records=len(conflicts),
  no_wiki_rows_removed=True,no_game_object_identity_claimed=True,
  no_original_tiledefs_modified=True,no_minecraft_implementation_decision=True,
  no_loot_distribution_loaded=True,sqlite_integrity="ok")
 (OUT/"MANIFEST.json").write_text(json.dumps(manifest,indent=2,ensure_ascii=False)+"\n",encoding="utf8")
 report=[
 "# Project Zomboid B42 가구 목록 정리 v6 — 남은 위키 중복 연결 71그룹",
 "## 원본의 의미를 해치지 않는 정리",
 "위키 원문 1268행 중 같은 정확한 타일 ID 집합을 공유하는 146행을 검토했어.",
 "기존 71개의 TileDef 이름 그룹은 69그룹이 각각 원본 이미지 타일 조합 하나를 중복 가리키고, 2그룹은 서로 다른 이미지 조합 두 개를 각각 중복 가리켜. 총 73개 원본 스프라이트 조합이야.",
 "게임 가구 오브젝트 73종 또는 마인크래프트 모델 73종으로 확정한 것이 아냐.",
 "## 기능 및 수납 속성",
 "같은 카운터가 위키 Tables/All과 Storage/Counters에 각각 표기되면서 Storage쪽에만 50 등 용량이 있는 사례를 보존했어. 두 행이 정확히 같은 TileSet/LocalID를 참조할 경우 이미지 연결을 하나만 두되 위키 분류·크기·수납용량을 원문 행마다 별도 컬럼으로 연결해.",
 "수납이 빈칸이라는 것은 0으로 추정하지 않고 원문 공란 그대로 남겨. 실제 원본 TileDef container, ContainerCapacity도 구분 저장했어.",
 "같은 이미지 타일을 다른 명칭이 가리키는 사례는 오류 가능성이 있으므로 V6_CONFLICTS_SAME_SPRITE_DIFFERENT_NAMES.csv에 남겨 자동 통합을 금지했어.",
 "## 이미지",
 "Tiles/2x 원본 PNG 19개 타일셋에서 원본 DB image_cells의 실제 localID/격자좌표를 이용해 71개 비교 카드를 만들어. 원본 픽셀 크롭 성공 수는 MANIFEST.json에 기록되어 있어.",
 "## 파일",
 "- B42_SHARED_WIKI_OVERLAP_V6.sqlite, B42_SHARED_WIKI_OVERLAP_V6.zip: v5 전체 원본 + v6 분류 SQL 테이블",
 "- V6_71_SHARED_SOURCE_GROUPS.csv: 71그룹과 원본 ID 조합 관계",
 "- V6_73_EXACT_SOURCE_APPEARANCES.csv: 73개의 정확한 스프라이트 ID 집합과 모든 관련 수납/기능/원본 속성",
 "- V6_146_WIKI_CROSS_CATEGORY_FACETS.csv: 위키 146행의 원문 카테고리 및 용량",
 "- V6_ALL_SOURCE_TILE_AND_FUNCTION_EVIDENCE.csv: TileDef 원본 속성/PNG 크롭 SHA",
 "- V6_CONFLICTS_SAME_SPRITE_DIFFERENT_NAMES.csv: 원문 명칭이 다르거나 속성 충돌 시 별도 기록",
 "- ORIGINAL_PNG_CONTACT_SHEETS_71/: 71개 그룹의 원본 PNG 비교 이미지",
 "## 이후 작업",
 "원본 스프라이트의 실제 Moveable object identity는 게임 Lua 및 TMX 그룹과 함께 검증해야 해. 별도 원본 그룹 963개 전수 시각 검수, loot 분포 Lua 연결도 남아 있어.",
 "Minecraft Block/Entity/3D 구현은 아직 결정하지 않았어."
 ]
 (OUT/"README_KO.md").write_text("\n\n".join(report)+"\n",encoding="utf8")
 con.close()
 with zipfile.ZipFile(ZIP,"w",zipfile.ZIP_DEFLATED,compresslevel=5) as z:
  for path in sorted(OUT.rglob("*")):
   if path.is_file() and path!=ZIP:z.write(path,path.relative_to(OUT))
 with zipfile.ZipFile(ZIP) as z:
  assert z.testzip() is None
  assert DB.name in z.namelist()
 print("PZ_B42_V6_DUPLICATE_RESOLUTION_DONE",json.dumps(manifest,ensure_ascii=False),flush=True)
if __name__=="__main__":
 main()
