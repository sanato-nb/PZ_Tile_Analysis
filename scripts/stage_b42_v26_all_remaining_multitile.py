#!/usr/bin/env python3
"""B42 v26 — all 235 unreviewed source grid×Facing candidates, exact original TileDef sprite PNG.
Original source grid observations cannot certify a unique runtime furniture item or real PZ isometric assembly.
"""
import csv,sqlite3,zipfile,shutil,json,hashlib,base64,sys
from pathlib import Path
from collections import defaultdict,Counter
from PIL import Image,ImageDraw,ImageFont
ROOT=Path(__file__).resolve().parents[1]
OLD=ROOT/"analysis/furniture_full_b42/2026-11-05/cross_facing_v25/B42_FURNITURE_CROSS_FACING_REVIEW_V25.zip"
OUT=ROOT/"analysis/furniture_full_b42/2026-11-05/all_multitile_visual_v26"
TEMP=Path("/tmp/b42_v26_stage.sqlite")
def qr(c,q):return [dict(r) for r in c.execute(q)]
def J(v):return json.dumps(v,ensure_ascii=False,sort_keys=True)
def save(name,rows):
 assert rows,name
 with (OUT/name).open("w",encoding="utf-8-sig",newline="") as f:
  w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
def read(name):
 with (OUT/name).open(encoding="utf-8-sig",newline="") as f:return list(csv.DictReader(f))
def select():
 assert OLD.is_file() and not OUT.exists()
 OUT.mkdir(parents=True)
 with zipfile.ZipFile(OLD) as z:
  assert z.testzip() is None
  with z.open("B42_FURNITURE_CROSS_FACING_REVIEW_V25.sqlite") as inp,TEMP.open("wb") as out:shutil.copyfileobj(inp,out)
 c=sqlite3.connect(TEMP);c.row_factory=sqlite3.Row
 assert c.execute("PRAGMA integrity_check").fetchone()[0]=="ok"
 queue=qr(c,"SELECT * FROM v25_235_remaining_direction_queue ORDER BY group_id,Facing")
 assert len(queue)==235
 rect={(x["group_id"],x["Facing"]):x for x in qr(c,
  "SELECT * FROM v21_all_source_rectangle_template WHERE raw_sprite_part_count>=2")}
 assert len(rect)==820
 ledger=qr(c,"SELECT * FROM v25_all_820_multitile_direction_visual_ledger")
 assert len(ledger)==820 and sum(x["source_grid_pixels_visually_checked"] for x in ledger)==585
 seen={(r["group_id"],r["Facing"]) for r in ledger if r["source_grid_pixels_visually_checked"]}
 pending={(r["group_id"],r["Facing"]) for r in queue}
 assert len(seen)==585 and len(pending)==235 and not seen&pending and seen|pending==set(rect)
 pp=defaultdict(list)
 for r in qr(c,"SELECT * FROM v21_source_tile_positioned_png"):
  pp[(r["group_id"],r["Facing"])].append(r)
 names=defaultdict(set)
 for r in qr(c,"SELECT rg.source_group_id AS group_id,r.display_name AS label FROM registry_entry_group rg JOIN registry_entry r ON r.entry_id=rg.entry_id"):
  if r["label"]:names[r["group_id"]].add(r["label"])
 source={r["source_key"]:r for r in qr(c,
  "SELECT source_key,group_id,SpriteGridPos,Facing FROM furniture_tile")}
 prior_pair={r["group_id"] for r in qr(c,"SELECT group_id FROM v25_all_274_multifacing_group_pair_coverage")}
 assert len(prior_pair)==274
 selections=[];partmeta=[];paths=set();newgroup=set()
 for i,q in enumerate(queue,1):
  key=(q["group_id"],q["Facing"])
  rr=rect[key]
  assert rr["raw_sprite_part_count"]==q["source_parts"]>=2
  assert rr["grid_w"]==q["raw_grid_w"] and rr["grid_h"]==q["raw_grid_h"]
  arr=pp[key]
  assert len(arr)==q["source_parts"] and rr["original_png_parts_mapped"]==len(arr)
  group=q["group_id"];name=sorted(names.get(group,()))[0] if names.get(group) else (rr["source_display_name"] or group)
  selections.append(dict(sample_index=i,group_id=group,Facing=q["Facing"],original_name=name,
   source_only_group=q["source_only_group"],grid_w=q["raw_grid_w"],grid_h=q["raw_grid_h"],
   source_parts=len(arr),prior_two_facing_group_comparison=int(group in prior_pair),
   prior_facing_directly_reviewed=0,original_atlas_cell_all_indexed=1,
   newly_viewed_grid_v26=1,exact_game_object_identity_certified=0))
  observed=set()
  for p in arr:
   assert (p["relative_x"],p["relative_y"]) not in observed
   observed.add((p["relative_x"],p["relative_y"]))
   assert 0<=p["relative_x"]<rr["grid_w"] and 0<=p["relative_y"]<rr["grid_h"]
   assert p["original_png_path"].startswith("Tiles/2x/") and p["original_png_path"].endswith(".png")
   assert p["original_cell_w"]>0 and p["original_cell_h"]>0
   assert source[p["source_key"]]["group_id"]==group
   assert source[p["source_key"]]["SpriteGridPos"]==p["raw_sprite_grid_pos"]
   paths.add(p["original_png_path"])
   partmeta.append(dict(sample_index=i,**p))
  assert len(observed)==rr["grid_w"]*rr["grid_h"]
  newgroup.add(group)
 assert len(selections)==235 and len({(x["group_id"],x["Facing"]) for x in selections})==235
 assert len({x["sample_index"] for x in partmeta})==235
 save("V26_235_SOURCE_FACING_TO_VISUALLY_REVIEW.csv",selections)
 save("V26_ALL_RAW_SOURCE_PARTS_POSITION_AND_ATLAS_MAP.csv",partmeta)
 (OUT/"_required_original_png_paths.txt").write_text("\n".join(sorted(paths))+"\n",encoding="utf8")
 summary=dict(stage="SOURCE_ONLY_SELECTED_PENDING_ORIGINAL_PNG_PIXEL_EXTRACTION",
  original_multitile_source_grid_facing_candidates=820,old_directly_viewed_facing_grids=585,
  new_unreviewed_unique_source_facing_grid_count=len(selections),
  new_unique_source_groups_without_prior_any_facing=len(newgroup-{g for g,f in seen}),
  new_source_groups_with_some_previous_facing=len(newgroup&{g for g,f in seen}),
  unique_source_groups_in_selected_grid_queue=len(newgroup),
  source_grid_original_parts=len(partmeta),
  original_png_atlases_needed=len(paths),all_235_source_png_cells_mapped=True,
  direct_visual_review_complete=0,confirmed_runtime_game_furniture_identity=0)
 (OUT/"STAGING_MANIFEST.json").write_text(json.dumps(summary,sort_keys=True,ensure_ascii=False,indent=2)+"\n",encoding="utf8")
 c.close();TEMP.unlink()
 print("V26_ALL_235_UNSEEN_SOURCE_DIRECTION_GRIDS_SELECTED",J(summary),flush=True)
def render():
 chosen=read("V26_235_SOURCE_FACING_TO_VISUALLY_REVIEW.csv")
 parts=read("V26_ALL_RAW_SOURCE_PARTS_POSITION_AND_ATLAS_MAP.csv")
 assert len(chosen)==235
 bysample=defaultdict(list)
 for p in parts:bysample[int(p["sample_index"])].append(p)
 atlas_paths=sorted({p["original_png_path"] for p in parts})
 atlases={};hashes={}
 for name in atlas_paths:
  fp=ROOT/name;assert fp.is_file(),name
  hashes[name]=hashlib.sha256(fp.read_bytes()).hexdigest()
  atlases[name]=Image.open(fp).convert("RGBA")
 cropped={};pixel_proofs=[]
 for p in parts:
  sample=int(p["sample_index"]);key=p["source_key"];atlas=atlases[p["original_png_path"]]
  w,h=int(p["original_cell_w"]),int(p["original_cell_h"])
  col,row=int(p["atlas_col"]),int(p["atlas_row"])
  x,y=col*w,row*h
  assert col>=0 and row>=0 and x+w<=atlas.width and y+h<=atlas.height
  img=atlas.crop((x,y,x+w,y+h))
  sha=hashlib.sha256(img.tobytes()).hexdigest()
  cropped[(sample,key)]=img
  pixel_proofs.append(dict(sample_index=sample,group_id=p["group_id"],Facing=p["Facing"],
   source_key=key,original_sprite_grid_pos=p["raw_sprite_grid_pos"],
   source_relative_x=p["relative_x"],source_relative_y=p["relative_y"],
   original_png_path=p["original_png_path"],original_atlas_png_sha256=hashes[p["original_png_path"]],
   original_cropped_cell_pixel_sha256=sha,
   atlas_col=col,atlas_row=row,cell_w=w,cell_h=h,
   originally_unreviewed_facing=1,new_v26_direct_sprite_visual_observation=1,
   exact_in_game_object_identity_certified=0))
 assert len(pixel_proofs)==len(parts)
 font=ImageFont.load_default()
 pages=[];page_hashes={}
 for offset in range(0,len(chosen),10):
  img=Image.new("RGB",(1280,1880),(242,245,249))
  draw=ImageDraw.Draw(img)
  for j in range(10):
   index=offset+j
   if index>=len(chosen):break
   rec=chosen[index];sample=int(rec["sample_index"])
   src=sorted(bysample[sample],key=lambda p:(int(p["relative_y"]),int(p["relative_x"])))
   left=j%2;top=j//2;x0=left*640;y0=top*376
   draw.rectangle((x0+4,y0+4,x0+636,y0+372),outline=(168,181,191),width=2,fill="white")
   draw.text((x0+12,y0+10),f'{sample}. {rec["original_name"]}'[:90],fill=(25,47,62),font=font)
   draw.text((x0+12,y0+30),f'{rec["group_id"]} facing={rec["Facing"]} grid={rec["grid_w"]}x{rec["grid_h"]} source-parts={rec["source_parts"]}',fill=(55,81,95),font=font)
   gw,gh=int(rec["grid_w"]),int(rec["grid_h"])
   step=min(300//gw,245//gh,113)
   step=max(10,step)
   ox=x0+28;oy=y0+65
   for p in src:
    px=int(p["relative_x"]);py=int(p["relative_y"])
    x=ox+px*(step+5);y=oy+py*(step+5)
    draw.rectangle((x,y,x+step,y+step),fill=(245,249,251),outline=(173,186,196))
    sprite=cropped[(sample,p["source_key"])].copy()
    sprite.thumbnail((max(1,step-8),max(1,step-19)),Image.Resampling.NEAREST)
    bg=Image.new("RGBA",sprite.size,(253,253,253,255));bg.alpha_composite(sprite)
    img.paste(bg.convert("RGB"),(x+(step-sprite.width)//2,y+(step-sprite.height)//2))
    draw.text((x+3,y+step-12),p["source_key"].split("/")[-1][:13],fill=(55,74,85),font=font)
   draw.text((x0+12,y0+352),"ORIGINAL SOURCE GRID - NOT CERTIFIED RUNTIME FURNITURE",fill=(114,73,60),font=font)
  page=offset//10+1
  name=f"V26_ORIGINAL_MULTITILE_SOURCE_CONTACT_{page:02d}.png"
  fp=OUT/name;img.save(fp,optimize=True)
  pages.append(name)
  page_hashes[name]=hashlib.sha256(fp.read_bytes()).hexdigest()
  (OUT/f"STAGED_V26_CONTACT_{page:02d}_BASE64.txt").write_text(base64.b64encode(fp.read_bytes()).decode("ascii"),encoding="ascii")
 for src in atlases.values():src.close()
 save("V26_ALL_NEW_SPRITE_PIXEL_SHA256.csv",pixel_proofs)
 m=json.loads((OUT/"STAGING_MANIFEST.json").read_text(encoding="utf8"))
 m.update(stage="EXTRACTED_ALL_235_PENDING_DIRECT_VISUAL_CATEGORIES",
  source_pixel_crops_completed=len(pixel_proofs),
  original_atlases_sha_verified=len(atlas_paths),
  contact_sheet_count=len(pages),original_contact_sheet_sha256=page_hashes,
  indexed_facing_grid_original_png_visual_evidence=235,confirmed_runtime_game_furniture_identity=0)
 (OUT/"STAGING_MANIFEST.json").write_text(json.dumps(m,sort_keys=True,ensure_ascii=False,indent=2)+"\n",encoding="utf8")
 print("V26_ALL_235_ORIGINAL_SPRITE_GROUP_FACING_IMAGE_GRIDS_CROPPED",J(m),flush=True)
if __name__=="__main__":
 if len(sys.argv)!=2 or sys.argv[1] not in ("--select","--render"):raise SystemExit("use --select or --render")
 if sys.argv[1]=="--select":select()
 else:render()
