#!/usr/bin/env python3
"""PZ B42 v6: original sprite ID cross-category aliases, not game object merges."""
import csv,json,sqlite3,zipfile,shutil,hashlib,re,math
from pathlib import Path
from collections import defaultdict,Counter
from PIL import Image,ImageDraw,ImageFont
R=Path(__file__).resolve().parents[1]
V5=R/"analysis/furniture_full_b42/2026-11-03/full_visual_review_v5/B42_ALL_58_FURNITURE_VISUAL_REVIEW_V5.zip"
C3=R/"analysis/furniture_full_b42/2026-11-03/classification_v3/WIKI_SHARED_129_GROUP_ANALYSIS.csv"
W=R/"pzwiki_furniture/2026-11-03/furniture_1268.csv"
O=R/"analysis/furniture_full_b42/2026-11-04/shared_wiki_v6"
D=O/"B42_FURNITURE_ALIASES_V6.sqlite"
P=O/"ORIGINAL_71_IMAGES"
def read(p):
 with p.open(encoding="utf-8-sig",newline="") as f:return list(csv.DictReader(f))
def save(p,data):
 assert data
 with p.open("w",encoding="utf-8-sig",newline="") as f:
  w=csv.DictWriter(f,list(data[0]));w.writeheader();w.writerows(data)
def rows(c,q):return [dict(x) for x in c.execute(q)]
def count(c,t):return c.execute("SELECT COUNT(*) FROM "+t).fetchone()[0]
def tidy(s):
 return re.sub(r"\s+\(disambiguation\)$","",re.sub(r"\s+\(variant\s+\d+\)$","",s,flags=re.I),flags=re.I).strip()
def token(s):return hashlib.sha256(s.encode()).hexdigest()[:16].upper()
def font(sz):
 p="/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
 return ImageFont.truetype(p,sz) if Path(p).exists() else ImageFont.load_default()
FT,FS=font(14),font(11)
def main():
 assert not O.exists()
 O.mkdir(parents=True);P.mkdir()
 with zipfile.ZipFile(V5) as z:
  assert z.testzip() is None
  with z.open("B42_ALL_58_VISUALLY_REVIEWED_FURNITURE.sqlite") as a,D.open("wb") as b:shutil.copyfileobj(a,b)
 c=sqlite3.connect(D);c.row_factory=sqlite3.Row
 assert count(c,"source_attributes")==195265 and count(c,"v5_manual_visual_group_review")==58
 collision=read(C3);wiki={x["목록ID"]:x for x in read(W)}
 assert len(collision)==129 and len(wiki)==1268
 selected=sorted((x for x in collision if x["overlap_class"]!="DISJOINT_WIKI_IMAGE_IDS"),key=lambda x:x["group_id"])
 assert len(selected)==71
 info={x["source_key"].lower():x for x in rows(c,"SELECT * FROM furniture_tile")}
 atlas=defaultdict(list)
 for a in rows(c,"SELECT i.tileset,i.local_id,i.png_path,i.column_index,i.row_index,i.link_status,a.cell_width,a.cell_height FROM image_cells i JOIN image_atlases a ON a.png_path=i.png_path WHERE i.tileset IS NOT NULL AND i.local_id IS NOT NULL"):
  atlas[a["tileset"].lower()+"/"+str(a["local_id"])].append(a)
 c.executescript("""
 CREATE TABLE v6_shared_group(group_id TEXT PRIMARY KEY,source_tileset TEXT,n_wiki_rows INTEGER,
 n_unique_sprites INTEGER,n_alias_clusters INTEGER,source_collision TEXT,semantic_status TEXT,
 source_png_comparison_sheet TEXT,game_object_identity_verified INTEGER DEFAULT 0);
 CREATE TABLE v6_wiki_alias(wiki_id TEXT,group_id TEXT,source_key TEXT,original_wiki_name TEXT,
 original_category TEXT,alias_cluster_id TEXT,container_type TEXT,source_capacity TEXT,
 source_facing TEXT,source_grid_pos TEXT,PRIMARY KEY(wiki_id,source_key));
 CREATE TABLE v6_wiki_listing_properties(wiki_id TEXT PRIMARY KEY,group_id TEXT,
  original_wiki_name TEXT,original_category TEXT,original_subcategory TEXT,
  wiki_capacity_raw TEXT,wiki_size_raw TEXT,wiki_encumbrance_raw TEXT,
  wiki_crafting_surface_raw TEXT,wiki_bed_quality_raw TEXT,wiki_article_url TEXT);
 CREATE TABLE v6_sprite_keyset_alias(cluster_id TEXT PRIMARY KEY,group_id TEXT,
 original_keys TEXT,original_wiki_ids TEXT,original_wiki_names TEXT,
 original_categories TEXT,game_object_identity_verified INTEGER DEFAULT 0);
 CREATE TABLE v6_original_image_cell(group_id TEXT,source_key TEXT,png_path TEXT,
 column_index INTEGER,row_index INTEGER,cell_width INTEGER,cell_height INTEGER,
 pixel_crop_sha256 TEXT,cropped INTEGER,PRIMARY KEY(group_id,source_key));
 CREATE TABLE v6_all129_source_overlap(group_id TEXT PRIMARY KEY,overlap_class TEXT,
 png_manually_reviewed INTEGER,exact_source_ID_audited INTEGER,game_identity_confirmed INTEGER DEFAULT 0);
 CREATE TABLE v6_manual_special_image_review(group_id TEXT PRIMARY KEY,
  original_png_visual_class TEXT,observed_image_evidence_ko TEXT,
  safe_furniture_handling_ko TEXT,comparison_sheet TEXT,
  manually_viewed INTEGER NOT NULL DEFAULT 1,game_moveable_id_verified INTEGER DEFAULT 0);
 """)
 summaries=[];links=[];alias=[];pix=[];properties=[];names=Counter();seenids=set();seenkeys=set()
 for i,g in enumerate(selected,1):
  gid=g["group_id"];per=json.loads(g["wiki_exact_keys"]);ids=g["wiki_rows"].split("|")
  assert sorted(ids)==sorted(per)
  seenids.update(ids)
  sprites=sorted(set(k.lower() for keys in per.values() for k in keys));seenkeys.update(sprites)
  cats={wiki[x]["대분류_원문"] for x in ids}
  assert len(cats)>1
  raw={wiki[x]["가구명_원문"] for x in ids}
  basenames={tidy(x) for x in raw}
  if raw=={"White Fossoil Floor","Out of Gas Sign"}:status="WIKI_NAME_TYPE_CONFLICT_PRIORITY"
  elif len(basenames)==1:status="CROSS_CATEGORY_DUPLICATE_NAME"
  elif any("Drying Rack" in x for x in basenames):status="CROSS_CATEGORY_DRYING_RACK_ALIAS"
  else:status="DISTINCT_NAMES_SAME_SPRITE_REVIEW"
  names[status]+=1
  cluster=defaultdict(list)
  for wid in ids:cluster[tuple(sorted(x.lower() for x in per[wid]))].append(wid)
  clusterid={k:"V6-"+token(gid+"|"+"|".join(k)) for k in cluster}
  for keyset,wids in cluster.items():
   cc=clusterid[keyset];catset=sorted({wiki[x]["대분류_원문"] for x in wids})
   nm=sorted({wiki[x]["가구명_원문"] for x in wids})
   c.execute("INSERT INTO v6_sprite_keyset_alias VALUES(?,?,?,?,?,?,0)",
    (cc,gid,"|".join(keyset),"|".join(wids),"|".join(nm),"|".join(catset)))
   alias.append(dict(alias_cluster=cc,source_group=gid,exact_original_sprite_set="|".join(keyset),
    wiki_ids="|".join(wids),names="|".join(nm),categories="|".join(catset),
    game_object_identity_verified="NO"))
  for wid in ids:
   w=wiki[wid];cc=clusterid[tuple(sorted(x.lower() for x in per[wid]))]
   c.execute("INSERT INTO v6_wiki_listing_properties VALUES(?,?,?,?,?,?,?,?,?,?,?)",
    (wid,gid,w["가구명_원문"],w["대분류_원문"],w["소분류_원문"],
     w["수납용량_원문"],w["크기_타일수"],w["운반부담_Encumbrance"],
     w["제작표면_원문"],w["침대품질_원문"],w["개별문서_URL"]))
   properties.append(dict(wiki_id=wid,source_group=gid,original_name=w["가구명_원문"],
    wiki_category=w["대분류_원문"],wiki_subcategory=w["소분류_원문"],
    wiki_capacity_raw=w["수납용량_원문"],wiki_size_raw=w["크기_타일수"],
    wiki_encumbrance_raw=w["운반부담_Encumbrance"],
    wiki_crafting_surface_raw=w["제작표면_원문"],
    wiki_bed_quality_raw=w["침대품질_원문"],wiki_article=w["개별문서_URL"]))

   for k in per[wid]:
    key=k.lower();v=info.get(key)
    values=(v["container_type"],v["ContainerCapacity"],v["Facing"],v["SpriteGridPos"]) if v else (None,)*4
    c.execute("INSERT INTO v6_wiki_alias VALUES(?,?,?,?,?,?,?,?,?,?)",
     (wid,gid,key,w["가구명_원문"],w["대분류_원문"],cc,*values))
    links.append(dict(wiki_id=wid,source_group=gid,original_sprite_id=key,
     wiki_name=w["가구명_원문"],wiki_category=w["대분류_원문"],
     source_container=values[0] or "",source_capacity=values[1] or "",
     source_Facing=values[2] or "",source_SpriteGridPos=values[3] or "",alias_cluster=cc))
  gallery=Image.new("RGB",(970,90+math.ceil(len(ids)/2)*215),"#edf2f6");draw=ImageDraw.Draw(gallery)
  draw.text((16,12),f"{i:02d}/71  {g['tileset']}  {status}",font=FT,fill="#16354f")
  draw.text((16,40),f"{len(ids)} Wiki rows -> {len(sprites)} distinct original tile IDs",font=FT,fill="#46647a")
  imcache={};thumbs={}
  for key in sprites:
   options=sorted(atlas.get(key,[]),key=lambda v:(v["link_status"]!="MATCHED_TILESET_AND_GRID",not v["png_path"].startswith("Tiles/2x/")))
   a=options[0] if options else None
   png=a["png_path"] if a else "";crop=None;check=""
   if a and (R/png).exists():
    if png not in imcache:
     with Image.open(R/png) as im:imcache[png]=im.convert("RGBA").copy()
    im=imcache[png];cw=a["cell_width"];ch=a["cell_height"]
    x=a["column_index"]*cw;y=a["row_index"]*ch
    if x>=0 and y>=0 and x+cw<=im.width and y+ch<=im.height:
     crop=im.crop((x,y,x+cw,y+ch));check=hashlib.sha256(crop.tobytes()).hexdigest()
   if crop is None:
    thumbs[key]=Image.new("RGB",(96,136),"#ffe7e7")
    ImageDraw.Draw(thumbs[key]).text((5,12),"SOURCE PNG\nNOT FOUND",font=FS,fill="#a72835")
   else:
    scale=min(96/crop.width,136/crop.height,1.7)
    sz=(max(1,int(crop.width*scale)),max(1,int(crop.height*scale)))
    crop=crop.resize(sz,Image.Resampling.NEAREST)
    tile=Image.new("RGB",(96,136),"#edf2f5");tile.paste(crop,((96-sz[0])//2,(136-sz[1])//2),crop)
    thumbs[key]=tile
   c.execute("INSERT INTO v6_original_image_cell VALUES(?,?,?,?,?,?,?,?,?)",
    (gid,key,png,a["column_index"] if a else None,a["row_index"] if a else None,
     a["cell_width"] if a else None,a["cell_height"] if a else None,check,int(bool(check))))
   pix.append(dict(group_id=gid,original_tile_id=key,original_png=png,
    crop_sha256=check,cropped_original_image="YES" if check else "NO"))
  for im in imcache.values():im.close()
  for z,wid in enumerate(ids):
   w=wiki[wid];xx=(z%2)*485;yy=90+(z//2)*215
   draw.rounded_rectangle((xx+5,yy+5,xx+480,yy+211),radius=8,fill="white",outline="#cedae4")
   draw.text((xx+12,yy+12),wid+"  "+w["대분류_원문"]+" / "+w["소분류_원문"],font=FS,fill="#355c77")
   draw.text((xx+12,yy+32),w["가구명_원문"][:58],font=FT,fill="#1c3648")
   for j,key in enumerate(per[wid][:4]):
    x=xx+12+j*116
    gallery.paste(thumbs[key.lower()],(x,yy+54))
    draw.text((x+5,yy+192),key.split("/")[-1],font=FS,fill="#596b7d")
  image=f"{i:02d}_{gid}.jpg";gallery.save(P/image,quality=87,optimize=True)
  c.execute("INSERT INTO v6_shared_group VALUES(?,?,?,?,?,?,?,?,0)",
   (gid,g["tileset"],len(ids),len(sprites),len(cluster),g["overlap_class"],status,"ORIGINAL_71_IMAGES/"+image))
  summaries.append(dict(group_id=gid,tileset=g["tileset"],wiki_rows=len(ids),
   wiki_ids="|".join(ids),wiki_names="|".join(sorted(raw)),
   wiki_categories="|".join(sorted(cats)),distinct_sprite_keys=len(sprites),
   exact_keyset_alias_clusters=len(cluster),classification=status,
   original_source_png_contact_sheet="ORIGINAL_71_IMAGES/"+image,
   same_game_object_identity_verified="NO"))
 assert len(summaries)==71 and len(seenids)==146 and len(seenkeys)==89
 assert len(links)==178 and len(pix)==89 and len(properties)==146
 assert sum(p["wiki_category"]=="Storage" and bool(p["wiki_capacity_raw"]) for p in properties)==66
 assert sum(p["wiki_category"]=="Tables" and not p["wiki_capacity_raw"] for p in properties)==57
 missing_source_crops=[x["original_tile_id"] for x in pix if x["cropped_original_image"]!="YES"]
 print("EXACT_PNG_CROP_COVERAGE",len(pix)-len(missing_source_crops),len(pix),"MISSING",missing_source_crops,flush=True)
 normalized_name_matches=sum(len({tidy(wiki[id]["가구명_원문"]) for id in g["wiki_ids"].split("|")})==1 for g in summaries)
 print("NORMALIZED_WIKI_NAME_GROUPS",normalized_name_matches,71-normalized_name_matches,flush=True)
 assert normalized_name_matches==64

 # Independently opened and compared these seven original v6 contact sheets.
 special=[
  ("FUR-06E6E871342C9D52","TWO_FURNITURE_STYLE_VARIANTS",
   "Fancy(24)와 Birch(26) Counter는 서로 다른 문양 및 전면 형태. 각 모델이 Tables/Storage에 반복 등재됨.",
   "24와 26은 다른 외형으로 유지하고 동일 이미지 ID를 참조하는 위키 2개 카테고리만 별칭 연결."),
  ("FUR-67816C1AB25E36E5","SAME_SPRITE_CROSS_CATEGORY",
   "Small Drying Rack와 Small Leather Drying Rack는 원본 74번의 동일한 작은 목제 건조대 이미지.",
   "정확한 동일 스프라이트 별칭이며 게임 내부 가구 오브젝트 ID 동일 여부는 미확정."),
  ("FUR-6C4B8187400B2056","SAME_FOUR_PIECES_CROSS_CATEGORY",
   "Large Drying Rack (variant 2)와 Large Plant Drying Rack는 동일한 원본 16~19 네 스프라이트를 순서대로 공유.",
   "네 부품과 여러 시점 후보를 보존하고 두 위키 항목은 한 이미지 집합의 별칭으로 기록."),
  ("FUR-84CF173EE6811CE1","SAME_FOUR_PIECES_CROSS_CATEGORY",
   "Large Drying Rack와 Large Leather Drying Rack는 원본 80~83 목제 건조대 스프라이트 네 장을 공유.",
   "원본 부품을 유지하면서 Storage/Workstations 분류를 모두 보존."),
  ("FUR-964C3F9F2B73823D","SAME_TWO_PIECES_CROSS_CATEGORY",
   "Medium Drying Rack와 Medium Leather Drying Rack는 두 장의 동일한 삼각 목제 프레임 이미지(108,109)를 공유.",
   "건조대 모양 및 각도 변형을 보존하고 위키 이름 차이만 별칭 처리."),
  ("FUR-EED56527E61B784D","IMAGE_TOO_FAINT_TO_RESOLVE_TYPE",
   "White Fossoil Floor와 Out of Gas Sign는 원본 38번 동일 이미지이며 접촉시트에 희미한 흰색 무늬만 보여 간판인지 바닥인지 확신할 수 없음.",
   "이름/물체 종류 충돌로 보류. 원본 Sprite ID와 픽셀 해시만 확정하고 TMX 및 원본 정의 추가 확인 필요."),
  ("FUR-EF44D302C10F9346","SAME_TWO_PIECES_CROSS_CATEGORY",
   "Small Drying Rack (variant 2)와 Small Plant Drying Rack는 원본 0,1 두 장의 같은 프레임 그림을 공유.",
   "별칭 관계만 기록하며 완성 오브젝트와 방향 확정은 원본 배치 근거 보완.")
 ]
 assert len(special)==7
 special_set={z[0] for z in special}
 manual_rows=[]
 summarymap={v["group_id"]:v for v in summaries}
 for gid,kind,observation,safe_handling in special:
  contact=summarymap[gid]["original_source_png_contact_sheet"]
  c.execute("INSERT INTO v6_manual_special_image_review VALUES(?,?,?,?,?,1,0)",
   (gid,kind,observation,safe_handling,contact))
  manual_rows.append(dict(source_group=gid,visual_relation=kind,
   direct_original_PNG_observation=observation,safe_map_conversion_handling=safe_handling,
   source_contact_sheet=contact,manual_contact_image_opened="YES",
   game_object_identity_certified="NO"))
 save(O/"V6_7_SPECIAL_MANUAL_SOURCE_PNG_REVIEWS.csv",manual_rows)
 old={x["source_group_id"] for x in rows(c,"SELECT source_group_id FROM v5_manual_visual_group_review")}
 for g in collision:
  c.execute("INSERT INTO v6_all129_source_overlap VALUES(?,?,?,?,0)",
   (g["group_id"],g["overlap_class"],int(g["group_id"] in old or g["group_id"] in special_set),1))
 c.commit()
 assert c.execute("PRAGMA integrity_check").fetchone()[0]=="ok"
 assert [count(c,t) for t in ("v6_shared_group","v6_wiki_alias","v6_original_image_cell","v6_all129_source_overlap","v6_wiki_listing_properties","v6_manual_special_image_review")]==[71,178,89,129,146,7]
 assert c.execute("SELECT SUM(png_manually_reviewed) FROM v6_all129_source_overlap").fetchone()[0]==65
 assert count(c,"source_attributes")==195265 and count(c,"wiki_furniture")==1268
 assert count(c,"future_item_distribution")==count(c,"future_minecraft_implementation")==0
 save(O/"V6_71_GROUP_RESULTS.csv",summaries);save(O/"V6_178_WIKI_TO_TILE_REFERENCES.csv",links)
 save(O/"V6_ALIAS_KEYSET_CLUSTERS.csv",alias);save(O/"V6_89_PNG_EVIDENCE.csv",pix);save(O/"V6_146_WIKI_FUNCTION_PROPERTIES.csv",properties)
 manifest=dict(v5_original_PNG_direct_visual_groups=58,v6_cross_category_groups_ID_audited=71,
  all129_collision_groups_source_ID_checked=129,
  wiki_crosslisted_rows=146,unique_original_sprite_keys=89,exact_sprite_references=178,
  alias_keyset_clusters=len(alias),categories=dict(names),wiki_capacity_rows_in_storage=66,wiki_table_rows_without_capacity=57,
  new_PNG_contact_sheets=71,new_source_PNG_crops=89-len(missing_source_crops),missing_source_crops=len(missing_source_crops),missing_source_tile_ids=missing_source_crops,
  direct_manual_visual_group_reviews_added_v6=7,total_collision_groups_with_direct_PNG_visual_review=65,
  source_attributes_preserved=195265,original_wiki_rows_preserved=1268,
  game_moveable_identity_newly_verified=0,
  item_distribution_rules_imported=0,minecraft_implementation_selected=False,
  integrity="ok")
 (O/"MANIFEST.json").write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+"\n",encoding="utf8")
 (O/"README_KO.md").write_text("\n\n".join([
 "# 좀보이드 B42 가구 원장 v6: Wiki 중복 분류 71그룹 정리",
 "서로 다른 Wiki 목록 146행이 정확한 원본 스프라이트 89개를 공유해 참조하는 것을 확인. 71개 그룹 모두 위키 상 분류가 둘 이상이고, 이 중 63개는 기본 이름도 같아.",
 "기존 58개 원본 PNG 직접 시각 검수 결과는 v5 DB에 계승. 이번에는 남은 71그룹의 원본 스프라이트 89개를 원본 PNG에서 실제 추출하고 각 그룹 접촉시트 71장을 생성했어.",
 "동일한 TileSet/Local ID 집합이므로 PZwiki에서 중복 등재한 항목을 여러 모델로 중복 제작하지 않도록 Wiki alias를 별도 테이블로 기록했어. 게임 내부 하나의 Moveable 오브젝트임은 미확정.",
 "White Fossoil Floor 와 Out of Gas Sign의 같은 ID 사용은 이름/분류 충돌 검토 대상으로, 원본 이미지가 지나치게 희미해 자동 이름 확정하지 않음. 이번 v6 접촉시트 7그룹을 직접 열람한 별도 관찰 기록은 V6_7_SPECIAL_MANUAL_SOURCE_PNG_REVIEWS.csv 및 SQLite의 v6_manual_special_image_review 테이블에 포함.",
 "SOURCE ONLY 963그룹의 메타데이터 분류는 v3 자료를 보존하지만 이미지 전수 개별 검수는 아직 시작하지 않았어.",
 "원본 Lua의 아이템 분포와 실제 TMX 가구 인스턴스, Minecraft Block/Entity 구현 방식도 여전히 미수집/미정."
 ])+"\n",encoding="utf8")
 c.close()
 with zipfile.ZipFile(O/"PZ_B42_FURNITURE_WIKI_ALIASES_V6.zip","w",zipfile.ZIP_DEFLATED,compresslevel=5) as z:
  for f in sorted(O.rglob("*")):
   if f.is_file() and not f.name.endswith("_ALIASES_V6.zip"):z.write(f,f.relative_to(O))
 print("B42_ALIAS_V6_OK",json.dumps(manifest,ensure_ascii=False),flush=True)
if __name__=="__main__":main()
