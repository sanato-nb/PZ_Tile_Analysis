#!/usr/bin/env python3
"""B42 v25 — complete direct image comparison of hitherto unpaired multi-tile source groups.
For a partly reviewed group, re-display the previous facing but count ONLY its unreviewed partner.
The visual TileDef rectangle is NOT a certified in-game furniture object or isometric rendering.
"""
from pathlib import Path
from collections import defaultdict,Counter
import csv,json,sqlite3,shutil,zipfile,hashlib,sys,base64
from PIL import Image,ImageDraw,ImageFont
R=Path(__file__).resolve().parents[1]
BASE=R/"analysis/furniture_full_b42/2026-11-05/cross_facing_v24/B42_FURNITURE_CROSS_FACING_REVIEW_V24.zip"
OUT=R/"analysis/furniture_full_b42/2026-11-05/cross_facing_v25"
TEMP=Path("/tmp/b42_v25_staging.sqlite")
ORDER={"E":0,"S":1,"N":2,"W":3,"(not set)":4}
def rows(c,q):return [dict(r) for r in c.execute(q)]
def write(name,items):
 assert items,name
 with (OUT/name).open("w",encoding="utf-8-sig",newline="") as f:
  w=csv.DictWriter(f,fieldnames=list(items[0]));w.writeheader();w.writerows(items)
def read(name):
 with (OUT/name).open(encoding="utf-8-sig",newline="") as f:return list(csv.DictReader(f))
def j(o):return json.dumps(o,sort_keys=True,ensure_ascii=False)
def select():
 assert BASE.is_file() and not OUT.exists()
 OUT.mkdir(parents=True)
 with zipfile.ZipFile(BASE) as z:
  assert z.testzip() is None
  with z.open("B42_FURNITURE_CROSS_FACING_REVIEW_V24.sqlite") as src,TEMP.open("wb") as dst:shutil.copyfileobj(src,dst)
 c=sqlite3.connect(TEMP);c.row_factory=sqlite3.Row
 assert c.execute("PRAGMA integrity_check").fetchone()[0]=="ok"
 rect=rows(c,"SELECT * FROM v21_all_source_rectangle_template WHERE raw_sprite_part_count>=2")
 assert len(rect)==820
 oldviews=rows(c,"SELECT group_id,Facing FROM v21_direct_multisprite_grid_visual_observation UNION ALL SELECT group_id,Facing FROM v22_new_facing_original_grid UNION ALL SELECT group_id,Facing FROM v23_new_facing_original_source UNION ALL SELECT group_id,Facing FROM v24_new_facing_original_source")
 assert len(oldviews)==480
 viewed={(x["group_id"],x["Facing"]) for x in oldviews}
 assert len(viewed)==480
 paired=rows(c,"SELECT group_id FROM v22_direct_two_facing_visual_comparison UNION ALL SELECT group_id FROM v23_direct_two_facing_visual_comparison UNION ALL SELECT group_id FROM v24_direct_two_facing_visual_comparison")
 paired_groups={r["group_id"] for r in paired}
 assert len(paired_groups)==200
 bygroup=defaultdict(list);bykey={}
 for r in rect:
  bygroup[r["group_id"]].append(r);bykey[(r["group_id"],r["Facing"])]=r
 multiface={g for g,fs in bygroup.items() if len(fs)>=2}
 assert len(bygroup)==346 and len(multiface)==274
 missing=multiface-paired_groups
 assert len(missing)==74,(len(missing),"expected remaining unpaired original groups")
 src_part=defaultdict(list)
 for p in rows(c,"SELECT * FROM v21_source_tile_positioned_png"):
  src_part[(p["group_id"],p["Facing"])].append(p)
 names=defaultdict(set)
 for r in rows(c,"SELECT rg.source_group_id AS group_id, r.display_name AS label FROM registry_entry_group rg JOIN registry_entry r ON r.entry_id=rg.entry_id"):
  if r["label"]:names[r["group_id"]].add(r["label"])
 previous_one=0;previous_zero=0
 pairplan=[];directionplans=[];sourceparts=[]
 refs=set();new_faces=set();reused_faces=set()
 for pair_no,g in enumerate(sorted(missing),1):
  available=sorted(bygroup[g],key=lambda x:(ORDER.get(x["Facing"],99),x["Facing"]))
  had=[x for x in available if (g,x["Facing"]) in viewed]
  unseen=[x for x in available if (g,x["Facing"]) not in viewed]
  assert len(had) in (0,1),(g,len(had))
  if had:
   assert len(unseen)>=1
   a,b=had[0],unseen[0];previous_one+=1
  else:
   assert len(unseen)>=2
   a,b=unseen[:2];previous_zero+=1
  nnew=int((g,a["Facing"]) not in viewed)+int((g,b["Facing"]) not in viewed)
  assert nnew in (1,2)
  name=sorted(names.get(g,[]))[0] if names.get(g) else (a["source_display_name"] or g)
  pp=dict(pair_no=pair_no,group_id=g,original_reference_name=name,
   source_only_group=int(a["source_only_group"]),
   Facing_A=a["Facing"],Facing_B=b["Facing"],
   grid_A=f'{a["grid_w"]}x{a["grid_h"]}',
   grid_B=f'{b["grid_w"]}x{b["grid_h"]}',
   part_count_A=a["raw_sprite_part_count"],part_count_B=b["raw_sprite_part_count"],
   A_previously_viewed=int((g,a["Facing"]) in viewed),
   B_previously_viewed=int((g,b["Facing"]) in viewed),
   number_new_facing_views=nnew,
   new_v25_game_object_certifications=0)
  pairplan.append(pp)
  for slot,r in (("A",a),("B",b)):
   key=(g,r["Facing"])
   old=int(key in viewed);arr=src_part[key]
   assert len(arr)==r["raw_sprite_part_count"] and len(arr)>=2
   position=set()
   for p in arr:
    x,y=p["relative_x"],p["relative_y"]
    assert 0<=x<r["grid_w"] and 0<=y<r["grid_h"] and (x,y) not in position
    position.add((x,y))
    path=p["original_png_path"]
    assert path.startswith("Tiles/2x/") and path.endswith(".png")
    assert p["original_cell_w"]>0 and p["original_cell_h"]>0
    refs.add(path)
    sourceparts.append(dict(pair_no=pair_no,face_slot=slot,already_seen_at_prior_version=old,
      newly_viewed_v25=int(not old),**p))
   assert len(position)==r["grid_w"]*r["grid_h"]
   d=dict(pair_no=pair_no,group_id=g,Facing=r["Facing"],face_slot=slot,
    width=r["grid_w"],height=r["grid_h"],source_parts=r["raw_sprite_part_count"],
    source_keys_json=j(sorted(p["source_key"] for p in arr)),
    previously_directly_viewed=old,new_v25_view=int(not old),runtime_identity_certified=0)
   directionplans.append(d)
   if old:reused_faces.add(key)
   else:new_faces.add(key)
 assert len(pairplan)==74 and len(directionplans)==148
 assert len(new_faces)==previous_one+2*previous_zero
 assert len(new_faces|reused_faces)==148 and not (new_faces&reused_faces)
 assert not new_faces.intersection(viewed) and reused_faces.issubset(viewed)
 assert not set(x["group_id"] for x in pairplan).intersection(paired_groups)
 write("V25_74_SOURCE_FACING_PAIR_PLANS.csv",pairplan)
 write("V25_148_DIRECTION_GRIDS_AND_PRIOR_REUSE_FLAGS.csv",directionplans)
 write("V25_148_DIRECTION_ORIGINAL_PART_SOURCE_COORDINATES.csv",sourceparts)
 (OUT/"_required_original_png_paths.txt").write_text("\n".join(sorted(refs))+"\n",encoding="utf8")
 progress=dict(stage="SELECTED_AWAITING_ORIGINAL_PNG_RENDER",
  original_group_facing_multitile_candidates=820,source_multifacing_groups=274,
  previously_paired_direct_visual_groups=200,remaining_unpaired_source_groups=74,
  v25_pair_groups=74,previous_facing_reused_count=len(reused_faces),
  new_group_facing_views=len(new_faces),
  new_source_groups_with_no_prior_facing_views=previous_zero,
  existing_once_viewed_source_groups=previous_one,
  total_grids_displayed_in_comparisons=148,
  new_after_v25_direct_visual_total=480+len(new_faces),
  original_png_atlases_referenced=len(refs),
  original_tile_cells_in_pair_comparisons=len(sourceparts),
  runtime_object_identity_certified=0,old_warning_count=474,old_missing_source_png_groups=23)
 (OUT/"STAGING_MANIFEST.json").write_text(json.dumps(progress,ensure_ascii=False,sort_keys=True,indent=2)+"\n",encoding="utf8")
 c.close();TEMP.unlink()
 print("V25_EXACT_ALL_REMAINING_TWO_FACING_PAIR_GROUPS_STAGED",j(progress),flush=True)
def render():
 pp=read("V25_74_SOURCE_FACING_PAIR_PLANS.csv")
 source=read("V25_148_DIRECTION_ORIGINAL_PART_SOURCE_COORDINATES.csv")
 assert len(pp)==74
 bydir=defaultdict(list)
 for p in source:
  bydir[(p["group_id"],p["Facing"])].append(p)
 atlas_paths=sorted({p["original_png_path"] for p in source})
 atlases={};original_png_sha={}
 for path in atlas_paths:
  fp=R/path;assert fp.is_file(),path
  original_png_sha[path]=hashlib.sha256(fp.read_bytes()).hexdigest()
  atlases[path]=Image.open(fp).convert("RGBA")
 crops={};pixels=[]
 for p in source:
  idx=int(p["pair_no"]);slot=p["face_slot"];key=p["source_key"]
  atlas=atlases[p["original_png_path"]]
  w,h=int(p["original_cell_w"]),int(p["original_cell_h"])
  x=int(p["atlas_col"])*w;y=int(p["atlas_row"])*h
  assert 0<=x<=atlas.width-w and 0<=y<=atlas.height-h
  img=atlas.crop((x,y,x+w,y+h))
  sha=hashlib.sha256(img.tobytes()).hexdigest()
  crops[(idx,slot,key)]=img
  pixels.append(dict(pair_no=idx,face_slot=slot,group_id=p["group_id"],Facing=p["Facing"],
   source_key=key,raw_sprite_grid_pos=p["raw_sprite_grid_pos"],
   relative_x=p["relative_x"],relative_y=p["relative_y"],
   original_png_path=p["original_png_path"],
   exact_original_png_sha256=original_png_sha[p["original_png_path"]],
   exact_pixel_cell_sha256=sha,
   atlas_col=p["atlas_col"],atlas_row=p["atlas_row"],
   original_cell_w=w,original_cell_h=h,
   previously_viewed_at_prior_version=p["already_seen_at_prior_version"],
   counted_new_facing_v25=p["newly_viewed_v25"],
   official_game_furniture_identity_certified=0))
 assert len(pixels)==len(source)
 font=ImageFont.load_default()
 fn_sha={};pages=[]
 for start in range(0,len(pp),8):
  PW,PH=1380,465
  board=Image.new("RGB",(PW,4*PH),(244,247,249))
  d=ImageDraw.Draw(board)
  for ix in range(8):
   row=start+ix
   if row>=len(pp):break
   rec=pp[row]
   idx=int(rec["pair_no"]);g=rec["group_id"]
   col=ix%2;line=ix//2
   xx=col*(PW//2);yy=line*PH
   d.rectangle((xx+3,yy+3,xx+PW//2-3,yy+PH-3),fill="white",outline=(168,182,190),width=2)
   title=rec["original_reference_name"]
   d.text((xx+12,yy+10),f'{idx}. {title}'[:98],font=font,fill=(35,50,61))
   d.text((xx+12,yy+29),f'{g}  Facing A {rec["Facing_A"]} ({rec["grid_A"]}) / Facing B {rec["Facing_B"]} ({rec["grid_B"]})',font=font,fill=(68,82,99))
   for slot in ("A","B"):
    face=rec["Facing_"+slot]
    arr=bydir[(g,face)]
    gw,gh=(int(k) for k in rec["grid_"+slot].split("x"))
    step=min(258//max(gw,1),255//max(gh,1),104)
    step=max(8,step)
    x0=xx+(35 if slot=="A" else 370);y0=yy+65
    was=int(rec[slot+"_previously_viewed"])
    d.text((x0,y0-16),f'Facing {face}: {"REUSED PREVIOUS VIEW" if was else "NEW V25 VIEW"}',font=font,fill=(60,65,80))
    for p in arr:
     relx,rely=int(p["relative_x"]),int(p["relative_y"])
     x=x0+relx*(step+4);y=y0+rely*(step+4)
     d.rectangle((x,y,x+step,y+step),fill=(242,248,250),outline=(168,189,196))
     img=crops[(idx,slot,p["source_key"])].copy()
     img.thumbnail((max(1,step-9),max(1,step-19)),Image.Resampling.NEAREST)
     bg=Image.new("RGBA",img.size,(253,253,253,255));bg.alpha_composite(img)
     board.paste(bg.convert("RGB"),(x+(step-img.width)//2,y+(step-img.height)//2))
     d.text((x+2,y+step-11),p["source_key"].split("/")[-1][:10],fill=(80,91,99),font=font)
   d.text((xx+12,yy+PH-26),"ORIGINAL SPRITE TILE GRID — NO CERTIFIED GAME OBJECT IDENTITY",font=font,fill=(123,70,64))
  pagenum=start//8+1
  fn=f"V25_74_REMAINING_FACING_PAIRS_SOURCE_CONTACT_{pagenum:02d}.png"
  fp=OUT/fn
  board.save(fp,optimize=True)
  pages.append(fn)
  fn_sha[fn]=hashlib.sha256(fp.read_bytes()).hexdigest()
  (OUT/f"STAGED_V25_PAIR_CONTACT_{pagenum:02d}_BASE64.txt").write_text(base64.b64encode(fp.read_bytes()).decode("ascii"),encoding="ascii")
 for img in atlases.values():img.close()
 write("V25_ALL_PAIRED_SOURCE_PNG_PIXEL_SHA256.csv",pixels)
 manifest=json.loads((OUT/"STAGING_MANIFEST.json").read_text(encoding="utf8"))
 manifest.update(stage="RENDERED_PENDING_DIRECT_VISUAL_CLASSIFICATION",
  original_png_sprites_reextracted=len(pixels),
  new_facing_part_pixel_hash_rows=sum(int(p["counted_new_facing_v25"]) for p in pixels),
  reused_previous_facing_part_pixel_hash_rows=sum(int(p["previously_viewed_at_prior_version"]) for p in pixels),
  original_png_atlases_verified=len(original_png_sha),
  contact_pages=len(pages),contact_sheet_original_png_sha256=fn_sha,
  v25_pair_visual_classification_rows=0,game_object_runtime_identity_certified=0)
 (OUT/"STAGING_MANIFEST.json").write_text(json.dumps(manifest,ensure_ascii=False,sort_keys=True,indent=2)+"\n",encoding="utf8")
 print("V25_REAL_ORIGINAL_74_FACE_PAIRS_EXTRACTED_AND_CONTACT_RENDERED",j(manifest),flush=True)
if __name__=="__main__":
 if len(sys.argv)!=2 or sys.argv[1] not in ("--select","--render"):raise SystemExit("use --select or --render")
 if sys.argv[1]=="--select":select()
 else:render()
