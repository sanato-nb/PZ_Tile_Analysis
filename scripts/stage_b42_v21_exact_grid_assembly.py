#!/usr/bin/env python3
"""v21 source tile multi-part GROUP×FACING rectangle audit.
Exactly preserve TileDef SpriteGridPos per tile; one assembled GRID CONTACT is NOT game render.
"""
import csv,hashlib,json,sqlite3,zipfile,shutil,sys
from pathlib import Path
from collections import Counter,defaultdict
from PIL import Image,ImageDraw,ImageFont
ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT/"analysis/furniture_full_b42/2026-11-04/visual_review_v20/B42_FURNITURE_MASTER_INVENTORY_V20.zip"
OUT=ROOT/"analysis/furniture_full_b42/2026-11-04/multipart_grid_v21"
TEMP=Path("/tmp/b42_v21_grid_source.sqlite")
def qr(c,s):return [dict(v) for v in c.execute(s)]
def j(v):return json.dumps(v,ensure_ascii=False,sort_keys=True)
def csvwrite(p,rows):
 assert rows,p
 with (OUT/p).open("w",encoding="utf-8-sig",newline="") as f:
  wr=csv.DictWriter(f,fieldnames=list(rows[0]));wr.writeheader();wr.writerows(rows)
def csvread(p):
 with (OUT/p).open("r",encoding="utf-8-sig",newline="") as f:return list(csv.DictReader(f))
def select():
 assert BASE.is_file() and not OUT.exists()
 OUT.mkdir(parents=True)
 with zipfile.ZipFile(BASE) as z:
  assert z.testzip() is None
  with z.open("B42_FURNITURE_MASTER_INVENTORY_V20.sqlite") as i,TEMP.open("wb") as o:shutil.copyfileobj(i,o)
 c=sqlite3.connect(TEMP);c.row_factory=sqlite3.Row
 assert c.execute("PRAGMA integrity_check").fetchone()[0]=="ok"
 template=qr(c,"SELECT * FROM v12_template_proof ORDER BY group_id,Facing")
 assert len(template)==3840
 complete=[x for x in template if x["reproduced_status"]=="COMPLETE_RECTANGLE"]
 assert len(complete)==843,(len(complete),Counter(x["reproduced_status"] for x in template))
 allpieces=defaultdict(list)
 for p in qr(c,"SELECT * FROM v12_tile_proof ORDER BY group_id,Facing,source_key"):
  allpieces[(p["group_id"],p["Facing"])].append(p)
 original={x["source_key"]:x for x in qr(c,"SELECT source_key,tileset,local_id,SpriteGridPos,Facing,group_id FROM furniture_tile")}
 assert len(original)==8219
 cells=defaultdict(list)
 for a in qr(c,"SELECT i.tileset,i.local_id,i.png_path,i.column_index,i.row_index,i.has_visible_pixels,a.cell_width,a.cell_height FROM image_cells i JOIN image_atlases a ON a.png_path=i.png_path WHERE i.tileset IS NOT NULL AND i.local_id IS NOT NULL"):
  cells[(a["tileset"].casefold(),a["local_id"])].append(a)
 for options in cells.values():
  options.sort(key=lambda v:(-int(bool(v["has_visible_pixels"])),0 if str(v["png_path"]).startswith("Tiles/2x/") else 1,str(v["png_path"])))
 sourceOnly={x["group_id"]:x for x in qr(c,"SELECT * FROM v14_source_only_ledger")}
 v9wiki=defaultdict(set)
 for x in qr(c,"SELECT entry_id,source_group_id FROM registry_entry_group"):
  if x["entry_id"].startswith("WIKI:"):v9wiki[x["source_group_id"]].add(x["entry_id"])
 print("stage input",len(sourceOnly),len(v9wiki),len(cells),flush=True)
 groups=[];partrows=[];eligible=[]
 for row in complete:
  g=row["group_id"];f=row["Facing"];pp=allpieces[(g,f)]
  assert len(pp)==row["pieces"] and len(pp)>=1,(g,f,len(pp),row["pieces"])
  width,height=row["grid_w"],row["grid_h"]
  assert width and height and width*height==len(pp),(g,f,width,height)
  keys=json.loads(row["source_keys_json"])
  assert set(keys)=={p["source_key"] for p in pp},g
  occupied=set();data=[];mapped=0
  for p in pp:
   key=p["source_key"];orig=original[key]
   assert orig["group_id"]==g and orig["SpriteGridPos"]==p["original_grid"],(g,key)
   x,y=p["relative_x_when_available"],p["relative_y_when_available"]
   assert x is not None and y is not None and (x,y) not in occupied
   occupied.add((x,y))
   assert 0<=x<width and 0<=y<height
   opts=[a for a in cells[(orig["tileset"].casefold(),orig["local_id"])]
     if a["png_path"] and a["column_index"] is not None and a["row_index"] is not None
     and a["cell_width"] and a["cell_height"] and a["png_path"].endswith(".png")]
   best=opts[0] if opts else None
   if best:mapped+=1
   rec=dict(group_id=g,Facing=f,source_key=key,raw_sprite_grid_pos=p["original_grid"],
    raw_x=p["raw_x"],raw_y=p["raw_y"],relative_x=x,relative_y=y,
    source_tileset=orig["tileset"],source_local_id=orig["local_id"],
    png_path=best["png_path"] if best else "",
    atlas_column=best["column_index"] if best else "",
    atlas_row=best["row_index"] if best else "",
    atlas_cell_width=best["cell_width"] if best else "",
    atlas_cell_height=best["cell_height"] if best else "",
    source_capacity_raw=p["source_capacity_raw"] or "",
    source_container_raw=p["source_container"] or "",
    source_facing_raw=p["source_facing"] or "",
    identity_certified=0,whole_furniture_assembly_visual_certified=0)
   data.append(rec);partrows.append(rec)
  assert len(occupied)==width*height and all((x,y) in occupied for x in range(width) for y in range(height))
  only=g in sourceOnly
  obj=dict(group_id=g,Facing=f,raw_grid_width=width,raw_grid_height=height,
   original_tile_count=len(pp),source_only_group=int(only),
   display_name=sourceOnly[g]["original_name"] if only else "",
   direct_wiki_group_reference_count=len(v9wiki.get(g,())),
   png_mapped_part_count=mapped,png_missing_part_count=len(pp)-mapped,
   image_cell_grid_fully_mapped=int(mapped==len(pp)),
   original_source_keys_json=j(keys),assembly_geometry="COMPLETE_RECTANGLE_TILEDEF_ONLY",
   orientation_exact_in_game_verified=0,whole_game_object_identity_certified=0)
  groups.append(obj)
  if len(pp)>=2 and mapped==len(pp) and width<=4 and height<=4 and len(pp)<=10:
   score=100*only+24*min(len(pp),5)+15*min(width*height,8)+min(len(v9wiki.get(g,())),4)
   eligible.append((score,obj))
 assert len(groups)==843
 assert sum(x["original_tile_count"] for x in groups)==len(partrows)
 c.close();TEMP.unlink()
 grouped=defaultdict(list)
 for score,obj in eligible:grouped[obj["group_id"]].append((score,obj))
 selected=[]
 for g,seq in grouped.items():
  seq.sort(key=lambda x:(-x[0],x[1]["Facing"]))
  selected.append(seq[0])
 selected.sort(key=lambda x:(-x[0],x[1]["group_id"],x[1]["Facing"]))
 # Require genuine multi-part, tile-source mapped and represent at most one facing per group.
 selected=[x for _,x in selected[:80]]
 assert len(selected)>=40,("unexpected low mapped multi-part candidates",len(selected))
 keys={(x["group_id"],x["Facing"]) for x in selected}
 assert len(keys)==len(selected) and len({x["group_id"] for x in selected})==len(selected)
 selectedrows=[]
 for i,x in enumerate(selected,1):
  rec=dict(preview_no=i,**x,visual_inspection_performed=0,game_identity_certified=0)
  selectedrows.append(rec)
 selectedparts=[p for p in partrows if (p["group_id"],p["Facing"]) in keys]
 paths=sorted({p["png_path"] for p in selectedparts})
 assert all(x.startswith("Tiles/") and x.endswith(".png") for x in paths),(paths[:5])
 (OUT/"_required_original_png_paths.txt").write_text("\n".join(paths)+"\n",encoding="utf8")
 csvwrite("V21_843_ALL_COMPLETE_RECTANGLE_TEMPLATE_SOURCE_AUDIT.csv",groups)
 csvwrite("V21_ALL_RECTANGLE_EXACT_SOURCE_TILE_POSITION_AND_PNG_MAP.csv",partrows)
 csvwrite("V21_SELECTED_ORIGINAL_MULTIPART_PREVIEW_QUEUE.csv",selectedrows)
 summary=dict(stage="V21_GEOMETRY_AND_SOURCE_IMAGE_MAP_STAGED",
  v20_raw_furniture_tiles=8219,v20_direction_templates=3840,
  v21_rectangular_geometry_templates=843,
  rectangle_with_all_source_png_cells=sum(x["image_cell_grid_fully_mapped"] for x in groups),
  rectangle_missing_any_source_png_cells=sum(x["png_missing_part_count"]>0 for x in groups),
  source_only_rectangles=sum(x["source_only_group"] for x in groups),
  source_geometry_single_tile_rectangles=sum(x["original_tile_count"]==1 for x in groups),
  source_geometry_actual_multi_tile_rectangles=sum(x["original_tile_count"]>=2 for x in groups),
  inspected_group_direction_previews=0,
  selected_preview_groups=len(selectedrows),selected_preview_parts=len(selectedparts),
  selected_atlas_pngs=len(paths),game_object_identity_certified=0,
  original_474_warnings_unresolved=True,
  note="TileDef SpriteGridPos matrix is NOT an isometric world render; do not label exact game furniture")
 (OUT/"STAGING_MANIFEST.json").write_text(json.dumps(summary,ensure_ascii=False,indent=2,sort_keys=True)+"\n",encoding="utf8")
 print("V21_MULTIPART_SOURCE_RECTANGLE_AUDIT_STAGED",j(summary),flush=True)
def render():
 rows=csvread("V21_SELECTED_ORIGINAL_MULTIPART_PREVIEW_QUEUE.csv")
 parts=csvread("V21_ALL_RECTANGLE_EXACT_SOURCE_TILE_POSITION_AND_PNG_MAP.csv")
 assert len(rows)>=40
 bygroup=defaultdict(list)
 wanted={(r["group_id"],r["Facing"]) for r in rows}
 for x in parts:
  if (x["group_id"],x["Facing"]) in wanted:bygroup[(x["group_id"],x["Facing"])].append(x)
 pics={};atlases={};pngsha={};imageproof=[]
 for p in sorted({part["png_path"] for group in bygroup.values() for part in group}):
  path=ROOT/p
  assert path.is_file(),p
  pngsha[p]=hashlib.sha256(path.read_bytes()).hexdigest()
  atlases[p]=Image.open(path).convert("RGBA")
 for r in rows:
  group=(r["group_id"],r["Facing"]);pp=bygroup[group]
  assert len(pp)==int(r["original_tile_count"])
  for p in pp:
   atlas=atlases[p["png_path"]]
   w,h=int(p["atlas_cell_width"]),int(p["atlas_cell_height"])
   x,y=int(p["atlas_column"])*w,int(p["atlas_row"])*h
   assert w>0 and h>0 and 0<=x<=atlas.width-w and 0<=y<=atlas.height-h
   crop=atlas.crop((x,y,x+w,y+h))
   ph=hashlib.sha256(crop.tobytes()).hexdigest()
   pics[(group,p["source_key"])]=crop
   imageproof.append(dict(group_id=r["group_id"],Facing=r["Facing"],source_key=p["source_key"],
    png_path=p["png_path"],png_sha256=pngsha[p["png_path"]],source_pixel_sha256=ph,
    relative_x=p["relative_x"],relative_y=p["relative_y"],
    cell_width=w,cell_height=h,atlas_column=p["atlas_column"],atlas_row=p["atlas_row"],
    displayed_as_positioned_tile_grid=1,isometric_furniture_assembly_certified=0))
 font=ImageFont.load_default()
 pages=[];page_sha={}
 for start in range(0,len(rows),10):
  W,H=580,405
  board=Image.new("RGB",(2*W,5*H),(242,246,248))
  draw=ImageDraw.Draw(board)
  for jx in range(10):
   i=start+jx
   if i>=len(rows):break
   r=rows[i];pp=bygroup[(r["group_id"],r["Facing"])]
   gx=jx%2;gy=jx//2;x0=gx*W;y0=gy*H
   draw.rectangle((x0+3,y0+3,x0+W-3,y0+H-3),outline=(176,193,208),width=2,fill="white")
   name=r["display_name"] or r["group_id"]
   draw.text((x0+14,y0+10),f'{r["preview_no"]}. {name}'[:86],font=font,fill=(31,45,58))
   draw.text((x0+14,y0+30),f'{r["group_id"]} facing={r["Facing"]} matrix={r["raw_grid_width"]}x{r["raw_grid_height"]}',font=font,fill=(63,78,91))
   gw,gh=int(r["raw_grid_width"]),int(r["raw_grid_height"])
   step=min(240//max(gw,1),240//max(gh,1),128)
   bx=x0+50;by=y0+62
   for part in pp:
    ix=int(part["relative_x"]);iy=int(part["relative_y"])
    xx=bx+ix*(step+6);yy=by+iy*(step+6)
    draw.rectangle((xx,yy,xx+step,yy+step),fill=(244,246,248),outline=(171,186,196))
    crop=pics[((r["group_id"],r["Facing"]),part["source_key"])]
    thumb=crop.copy();thumb.thumbnail((step-9,step-18),Image.Resampling.NEAREST)
    white=Image.new("RGBA",thumb.size,(250,250,252,255));white.alpha_composite(thumb)
    board.paste(white.convert("RGB"),(xx+(step-thumb.width)//2,yy+(step-thumb.height)//2))
    draw.text((xx+3,yy+step-12),part["source_key"].split("/")[-1][:20],fill=(50,59,69),font=font)
   draw.text((x0+14,y0+375),"GRID POSITION CONTACT ONLY — NOT AN IN-GAME ISO COMPOSITE",font=font,fill=(111,62,53))
  page=start//10+1
  path=OUT/("V21_MULTIPART_ORIGINAL_SPRITES_GRID_CONTACT_%02d.png"%page)
  board.save(path,optimize=True)
  pages.append(path.name);page_sha[path.name]=hashlib.sha256(path.read_bytes()).hexdigest()
  import base64
  (OUT/("STAGED_V21_MULTIPART_CONTACT_%02d_BASE64.txt"%page)).write_text(base64.b64encode(path.read_bytes()).decode("ascii"),encoding="ascii")
 for a in atlases.values():a.close()
 csvwrite("V21_SELECTED_PARTS_ORIGINAL_PIXEL_SHA256.csv",imageproof)
 manifest=json.loads((OUT/"STAGING_MANIFEST.json").read_text(encoding="utf8"))
 manifest.update(stage="V21_MULTIPART_GRID_CONTACT_IMAGES_EXTRACTED_PENDING_DIRECT_VISUAL_REVIEW",
  rendered_original_multisprite_group_direction_contact_candidates=len(rows),
  source_png_verified_and_cropped_parts=len(imageproof),
  rendered_contact_pages=pages,contact_sheet_sha256=page_sha,
  original_png_sha256_count=len(pngsha),full_object_assembly_certified=0)
 (OUT/"STAGING_MANIFEST.json").write_text(json.dumps(manifest,ensure_ascii=False,indent=2,sort_keys=True)+"\n",encoding="utf8")
 print("V21_MULTIPART_GRID_CONTACT_RENDER_PASSED",j(manifest),flush=True)
if __name__=="__main__":
 if len(sys.argv)!=2 or sys.argv[1] not in ("--select","--render"):raise SystemExit("--select or --render")
 if sys.argv[1]=="--select":select()
 else:render()
