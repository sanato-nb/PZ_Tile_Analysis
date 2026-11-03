#!/usr/bin/env python3
"""Create original-PNG evidence for 58 wiki source groups; no object auto-merge."""
import sqlite3,csv,json,zipfile,shutil,re,hashlib,math
from pathlib import Path
from collections import defaultdict,Counter
from PIL import Image,ImageDraw,ImageFont
ROOT=Path(__file__).resolve().parents[1]
SOURCE=ROOT/"analysis/furniture_full_b42/2026-11-03/classification_v3/B42_FURNITURE_CLASSIFICATION_V3.zip"
WIKI=ROOT/"pzwiki_furniture/2026-11-03/furniture_1268.csv"
OUT=ROOT/"analysis/furniture_full_b42/2026-11-03/disjoint_visual_v4"
DB=OUT/"PZ_B42_FURNITURE_DISJOINT_VISUAL_V4.sqlite"
PICS=OUT/"CONTACT_SHEETS_58"
def getrows(c,q):return [dict(x) for x in c.execute(q)]
def loadcsv(p):
 with p.open(encoding="utf-8-sig",newline="") as f:return list(csv.DictReader(f))
def emit(p,rr):
 assert rr
 with p.open("w",encoding="utf-8-sig",newline="") as f:
  w=csv.DictWriter(f,fieldnames=list(rr[0]));w.writeheader();w.writerows(rr)
def rootname(name):
 return re.sub(r"\s+\(disambiguation\)$","",re.sub(r"\s+\(variant\s+\d+\)$","",name,flags=re.I),flags=re.I).strip()
def variant(name):return bool(re.search(r"\(variant\s+\d+\)$",name,re.I))
def tok(s):return hashlib.sha256(s.encode("utf8")).hexdigest()[:16].upper()
def font(size):
 for p in ("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf","/usr/share/fonts/truetype/liberation2/LiberationSans-Regular.ttf"):
  if Path(p).is_file():return ImageFont.truetype(p,size)
 return ImageFont.load_default()
TITLE,BODY,SMALL=font(18),font(13),font(11)
def preview(crop,width=80,height=160):
 im=crop.convert("RGBA")
 scale=min(width/im.width,height/im.height,1.5)
 size=(max(1,round(im.width*scale)),max(1,round(im.height*scale)))
 im=im.resize(size,Image.Resampling.NEAREST)
 canvas=Image.new("RGB",(width,height),"#edf2f6")
 canvas.paste(im,((width-size[0])//2,(height-size[1])//2),im)
 return canvas
def missing(k):
 im=Image.new("RGB",(80,160),"#f9e8e8")
 d=ImageDraw.Draw(im);d.text((3,26),"NO ORIGINAL\nPNG CELL",fill="#9b2635",font=SMALL)
 d.text((3,82),k.split("/")[-1],fill="#9b2635",font=SMALL)
 return im
def main():
 assert not OUT.exists(),"Never overwrite source/version"
 OUT.mkdir(parents=True);PICS.mkdir()
 with zipfile.ZipFile(SOURCE) as z:
  assert z.testzip() is None
  with z.open("FURNITURE_CLASSIFIED_V3.sqlite") as stream,DB.open("wb") as f:
   shutil.copyfileobj(stream,f)
 c=sqlite3.connect(DB);c.row_factory=sqlite3.Row
 assert c.execute("PRAGMA integrity_check").fetchone()[0]=="ok"
 assert c.execute("SELECT COUNT(*) FROM wiki_furniture").fetchone()[0]==1268
 assert c.execute("SELECT COUNT(*) FROM source_attributes").fetchone()[0]==195265
 wiki=loadcsv(WIKI);w={x["목록ID"]:x for x in wiki}
 assert len(w)==1268
 disjoint=getrows(c,"SELECT * FROM v3_wiki_overlap WHERE overlap_type='DISJOINT_WIKI_IMAGE_IDS' ORDER BY group_id")
 assert len(disjoint)==58
 selected={wid for g in disjoint for wid in g["wiki_ids"].split("|")}
 assert len(selected)==357
 groups={x["group_id"]:x for x in getrows(c,"SELECT * FROM furniture_group")}
 origin={x["source_key"].casefold():x for x in getrows(c,"SELECT * FROM furniture_tile")}
 atlas=defaultdict(list)
 for r in getrows(c,"SELECT i.tileset,i.local_id,i.png_path,i.grid_id,i.column_index,i.row_index,i.link_status,i.has_visible_pixels,a.cell_width,a.cell_height,a.link_status AS atlas_status FROM image_cells i JOIN image_atlases a ON a.png_path=i.png_path WHERE i.tileset IS NOT NULL AND i.local_id IS NOT NULL"):
  atlas[r["tileset"].casefold()+"/"+str(r["local_id"])].append(r)
 c.executescript("""
 CREATE TABLE v4_wiki_name_index(wiki_id TEXT PRIMARY KEY,raw_name TEXT,base_name TEXT,
   category TEXT,explicit_variant INTEGER,selected_for_visual INTEGER);
 CREATE TABLE v4_disjoint_group(group_id TEXT PRIMARY KEY,tileset TEXT,wiki_rows INTEGER,
   distinct_base_names INTEGER,relationship TEXT,contact_sheet TEXT,
   game_object_identity_certified INTEGER NOT NULL DEFAULT 0);
 CREATE TABLE v4_name_family(family_id TEXT PRIMARY KEY,source_group_id TEXT,base_name TEXT,
   source_category TEXT,wiki_members INTEGER,physical_design_certified INTEGER NOT NULL DEFAULT 0);
 CREATE TABLE v4_name_family_member(family_id TEXT,wiki_id TEXT,source_sprite_keys_json TEXT,
   original_name TEXT,original_tile_size TEXT,original_capacity TEXT,original_image_url TEXT,
   PRIMARY KEY(family_id,wiki_id));
 CREATE TABLE v4_original_crop_evidence(wiki_id TEXT,source_key TEXT,png_path TEXT,
   atlas_grid_id INTEGER,atlas_status TEXT,image_cell_status TEXT,
   original_pixel_crop_sha256 TEXT,png_crop_available INTEGER,
   source_facing TEXT,source_sprite_grid_pos TEXT,source_container TEXT,
   source_capacity TEXT,PRIMARY KEY(wiki_id,source_key));
 CREATE INDEX v4_member_idx ON v4_name_family_member(wiki_id);
 CREATE INDEX v4_crop_idx ON v4_original_crop_evidence(source_key);
 """)
 for row in wiki:
  c.execute("INSERT INTO v4_wiki_name_index VALUES(?,?,?,?,?,?)",
   (row["목록ID"],row["가구명_원문"],rootname(row["가구명_원문"]),
    row["대분류_원문"],int(variant(row["가구명_원문"])),
    int(row["목록ID"] in selected)))
 atlas_cache={}
 group_results=[];family_results=[];member_results=[];cell_results=[]
 failed=[];rendered=0;notrendered=0;stats=Counter()
 for no,g in enumerate(disjoint,1):
  gid=g["group_id"];gm=groups[gid];ids=g["wiki_ids"].split("|")
  raw_ids=json.loads(g["exact_tile_ids_json"])
  families=defaultdict(list)
  for wid in ids:families[rootname(w[wid]["가구명_원문"])].append(wid)
  relation="SAME_WIKI_BASE_WITH_EXPLICIT_VARIANTS" if len(families)==1 else "MULTIPLE_BASE_NAMES_KEEP_SEPARATE"
  stats[relation]+=1
  cards=[]
  for name,members in sorted(families.items(),key=lambda a:min(a[1])):
   fid="FAM-"+tok(gid+"|"+name)
   category="|".join(sorted({w[wid]["대분류_원문"] for wid in members}))
   c.execute("INSERT INTO v4_name_family VALUES(?,?,?,?,?,0)",(fid,gid,name,category,len(members)))
   family_results.append(dict(family_id=fid,group_id=gid,family_name=name,
    source_category=category,wiki_rows=len(members),wiki_ids="|".join(members),
    actual_game_furniture_design_verified="NO"))
   for wid in members:
    row=w[wid];sprite_keys=raw_ids[wid];assert sprite_keys,(wid,gid)
    c.execute("INSERT INTO v4_name_family_member VALUES(?,?,?,?,?,?,?)",
     (fid,wid,json.dumps(sprite_keys),row["가구명_원문"],row["크기_타일수"],
      row["수납용량_원문"],row["이미지_URL"]))
    member_results.append(dict(wiki_id=wid,family_id=fid,group_id=gid,
     original_name=row["가구명_원문"],normalized_base_name=name,
     category=row["대분류_원문"],subcategory=row["소분류_원문"],
     wiki_size_raw=row["크기_타일수"],wiki_capacity_raw=row["수납용량_원문"],
     wiki_encumbrance_raw=row["운반부담_Encumbrance"],
     wiki_page=row["개별문서_URL"],wiki_image=row["이미지_URL"],
     exact_source_sprite_keys="|".join(sprite_keys),source_group_CustomName=gm["custom_name"],
     source_group_GroupName=gm["group_name"],confirmed_same_game_object="NO"))
    thumbs=[]
    for key in sprite_keys:
     info=origin.get(key.casefold(),{})
     opts=sorted(atlas.get(key.casefold(),[]),
       key=lambda x:(x["link_status"]!="MATCHED_TILESET_AND_GRID",
        not x["png_path"].startswith("Tiles/2x/")))
     item=opts[0] if opts else None
     pix=None;checksum=""
     if item is not None and (ROOT/item["png_path"]).exists():
      try:
       path=item["png_path"]
       if path not in atlas_cache:atlas_cache[path]=Image.open(ROOT/path).convert("RGBA")
       img=atlas_cache[path]
       tw,th=item["cell_width"],item["cell_height"]
       xx=item["column_index"]*tw;yy=item["row_index"]*th
       if min(tw,th)<=0 or xx<0 or yy<0 or xx+tw>img.width or yy+th>img.height:
        raise ValueError("Source atlas crop out of bound")
       pix=img.crop((xx,yy,xx+tw,yy+th))
       checksum=hashlib.sha256(pix.tobytes()).hexdigest()
      except Exception as exc:
       failed.append(dict(wiki_id=wid,source_key=key,reason=str(exc)))
     if pix is not None:
      rendered+=1;thumbs.append(preview(pix))
     else:
      notrendered+=1;thumbs.append(missing(key))
     c.execute("INSERT INTO v4_original_crop_evidence VALUES(?,?,?,?,?,?,?,?,?,?,?,?)",
      (wid,key,item["png_path"] if item else "",item["grid_id"] if item else None,
       item["atlas_status"] if item else "",item["link_status"] if item else "",
       checksum,int(pix is not None),info.get("Facing",""),info.get("SpriteGridPos",""),
       info.get("container_type",""),info.get("ContainerCapacity","")))
     cell_results.append(dict(wiki_id=wid,source_key=key,
      source_png_path=item["png_path"] if item else "",
      image_grid_id=item["grid_id"] if item else "",
      original_atlas_status=item["atlas_status"] if item else "",
      original_image_cell_status=item["link_status"] if item else "",
      original_crop_sha256=checksum,rendered_original_png="YES" if pix is not None else "NO",
      Facing=info.get("Facing",""),SpriteGridPos=info.get("SpriteGridPos",""),
      container=info.get("container_type",""),ContainerCapacity=info.get("ContainerCapacity","")))
    cards.append((wid,row["가구명_원문"],sprite_keys,thumbs))
  columns=4;cw=290;ch=247
  out=Image.new("RGB",(columns*cw,80+math.ceil(len(cards)/columns)*ch),"#e9eef3")
  drawer=ImageDraw.Draw(out)
  drawer.text((12,10),f"ORIGINAL SOURCE SPRITES {no:02d}/58    {gm['tileset']}",font=TITLE,fill="#16334d")
  drawer.text((12,42),f"WIKI ROWS {len(ids)}  /  {relation}  /  {gid}",font=BODY,fill="#456077")
  for idx,(wid,name,keys,thumbs) in enumerate(cards):
   x=(idx%columns)*cw;y=80+(idx//columns)*ch
   drawer.rounded_rectangle((x+5,y+5,x+cw-5,y+ch-5),radius=9,
      fill="white",outline="#cad5e0",width=2)
   drawer.text((x+13,y+12),wid,font=TITLE,fill="#183b57")
   drawer.text((x+13,y+37),name[:38],font=SMALL,fill="#344b60")
   for ti,thumb in enumerate(thumbs):
    xx=x+13+ti*84
    if xx+80<x+cw-8:out.paste(thumb,(xx,y+55))
   drawer.text((x+13,y+218),("|".join(keys))[:43],font=SMALL,fill="#58697b")
  imgname=f"{no:02d}_{gid}.jpg"
  out.save(PICS/imgname,quality=88,optimize=True)
  c.execute("INSERT INTO v4_disjoint_group VALUES(?,?,?,?,?,?,0)",
   (gid,gm["tileset"],len(ids),len(families),relation,"CONTACT_SHEETS_58/"+imgname))
  group_results.append(dict(index=no,source_group_id=gid,tileset=gm["tileset"],
   original_CustomName=gm["custom_name"],original_GroupName=gm["group_name"],
   wiki_entries=len(ids),normalized_name_families=len(families),
   family_names="|".join(sorted(families)),relation=relation,
   image_path="CONTACT_SHEETS_58/"+imgname,game_object_identity_verified="NO"))
  for v in atlas_cache.values():v.close()
  atlas_cache.clear()
 c.commit()
 assert len(group_results)==58 and len(member_results)==357
 assert len(family_results)==66,len(family_results)
 assert c.execute("PRAGMA integrity_check").fetchone()[0]=="ok"
 assert c.execute("SELECT COUNT(*) FROM v4_wiki_name_index").fetchone()[0]==1268
 assert c.execute("SELECT COUNT(*) FROM v4_disjoint_group").fetchone()[0]==58
 assert c.execute("SELECT COUNT(*) FROM v4_name_family").fetchone()[0]==66
 assert c.execute("SELECT COUNT(*) FROM v4_name_family_member").fetchone()[0]==357
 assert c.execute("SELECT COUNT(*) FROM v4_original_crop_evidence").fetchone()[0]==len(cell_results)
 assert c.execute("SELECT COUNT(*) FROM source_attributes").fetchone()[0]==195265
 assert c.execute("SELECT COUNT(*) FROM future_item_distribution").fetchone()[0]==0
 assert c.execute("SELECT COUNT(*) FROM future_minecraft_implementation").fetchone()[0]==0
 write=emit
 write(OUT/"GROUPS_58_V4.csv",group_results)
 write(OUT/"WIKI_NAME_FAMILIES_66.csv",family_results)
 write(OUT/"WIKI_VARIANT_ROWS_357.csv",member_results)
 write(OUT/"ORIGINAL_PNG_CROP_EVIDENCE.csv",cell_results)
 manifest=dict(original_v3_wiki_rows=1268,disjoint_name_group_count=58,
  wiki_rows_in_58_groups=357,
  same_base_name_variant_groups=stats["SAME_WIKI_BASE_WITH_EXPLICIT_VARIANTS"],
  mixed_base_name_groups=stats["MULTIPLE_BASE_NAMES_KEEP_SEPARATE"],
  normalized_wiki_name_families=66,
  contact_sheet_count=len(list(PICS.glob("*.jpg"))),
  original_png_source_cell_records=len(cell_results),
  original_png_cells_rendered=rendered,original_png_cells_not_rendered=notrendered,
  crop_errors=failed[:12],all_tileset_atlas_mappings_certified=False,
  physical_object_identity_newly_certified=0,
  item_distribution_rules_imported=False,minecraft_implementation_selected=False,
  original_source_attributes_preserved=195265,sqlite_integrity="ok")
 (OUT/"MANIFEST.json").write_text(json.dumps(manifest,indent=2,ensure_ascii=False)+"\n",encoding="utf8")
 lines=["# 58개 원본 ID 비중복 가구 그룹 — 실제 원본 스프라이트 검수판",
 "원본 PZ PNG의 타일을 v259 이미지 셀 메타데이터의 열/행/크기에 따라 잘라 비교했어. 원본 PNG 없는 경우에는 누락 표시가 나와.",
 "50개 그룹은 Wiki 변형 접미사 제거 후 기본 이름이 같고, 8개 그룹은 기본 이름이 둘 이상이어서 분리했어.",
 "66개 이름 계열은 디자인 확정 수가 아니고 Wiki 분류용 가족 이름이야.",
 "58장 접촉시트 역시 실제 PZ 게임 엔티티/Moveable 오브젝트의 동일성을 직접 확정하지 않아.",
 "## 전체 접촉시트"]
 for g in group_results:
  lines.append("### "+str(g["index"]).zfill(2)+" · "+g["family_names"])
  lines.append("원본: "+g["tileset"]+" · 위키 행 "+str(g["wiki_entries"])+"개 · "+g["relation"])
  lines.append("![Original PZ sprites]("+g["image_path"]+")")
 (OUT/"ALL_58_VISUAL_GALLERY.md").write_text("\n\n".join(lines)+"\n",encoding="utf8")
 (OUT/"README_KO.md").write_text("\n\n".join([
 "# B42 가구 분류 v4",
 "위키 1,268항목에서 같은 원본 TileDef 그룹에 속하지만 위키 이미지 ID 집합이 서로 겹치지 않는 58개 그룹을 분석했어.",
 "이 58개 그룹에는 357개의 서로 다른 위키 기록이 있어. 그중 50개 원본 그룹에서 기본 명칭을 공유하는 변형 행을 확인했고, 서로 다른 명칭이 혼합된 8개 그룹은 가구 이름 계열을 분리했어.",
 "원본 타일 PNG 및 image_cells / image_atlases의 위치 메타데이터로 만든 접촉시트 58장, 원본 이미지 크롭 SHA-256, 위키 행/원본 스프라이트/속성을 추적 가능하게 저장했어.",
 "같은 이름 계열 안에 여러 실제 디자인이 있을 수 있고, 서로 다른 로컬 ID가 같은 가구의 방향/부품일 수도 있어. 따라서 하나의 완성 3D 모델로 자동 병합하거나 개별 확정하지 않았어.",
 "원본 source_attributes 195,265행, 기존 full TileDef, 위키 1,268행 및 v3 테이블은 모두 보존했어.",
 "마크 Block/Entity 구현, 실맵 가구 인스턴스, 루팅 Lua 분포 규칙은 여전히 미결정/미수집 상태.",
 "주요 산출물: SQLite, GROUPS_58_V4.csv, WIKI_NAME_FAMILIES_66.csv, WIKI_VARIANT_ROWS_357.csv, ORIGINAL_PNG_CROP_EVIDENCE.csv, ALL_58_VISUAL_GALLERY.md, CONTACT_SHEETS_58 폴더, 통합 ZIP."
 ])+"\n",encoding="utf8")
 c.close()
 with zipfile.ZipFile(OUT/"B42_DISJOINT_VISUAL_V4_BUNDLE.zip","w",zipfile.ZIP_DEFLATED,compresslevel=5) as z:
  for p in sorted(OUT.rglob("*")):
   if p.is_file() and p.name!="B42_DISJOINT_VISUAL_V4_BUNDLE.zip":
    z.write(p,p.relative_to(OUT))
 with zipfile.ZipFile(OUT/"B42_DISJOINT_VISUAL_V4_BUNDLE.zip") as z:
  assert z.testzip() is None
  assert len([x for x in z.namelist() if x.startswith("CONTACT_SHEETS_58/") and x.endswith(".jpg")])==58
 print("DISJOINT_V4_SUCCESS",json.dumps(manifest,ensure_ascii=False),flush=True)
if __name__=="__main__":main()
