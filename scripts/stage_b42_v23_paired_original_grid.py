#!/usr/bin/env python3
"""v23: compare ORIGINAL PZ SpriteGridPos grids for TWO facings of 60 newly selected groups.
This is a paired image review, NOT a certified isometric object or game runtime identity.
"""
import csv,hashlib,json,re,shutil,sqlite3,sys,zipfile,base64
from pathlib import Path
from collections import defaultdict,Counter
from PIL import Image,ImageDraw,ImageFont
ROOT=Path(__file__).resolve().parents[1]
SRC=ROOT/"analysis/furniture_full_b42/2026-11-05/cross_facing_v22/B42_FURNITURE_CROSS_FACING_REVIEW_V22.zip"
OUT=ROOT/"analysis/furniture_full_b42/2026-11-05/cross_facing_v23"
DBTMP=Path("/tmp/b42_v23_stage.sqlite")
N=60
def rows(c,q):return [dict(x) for x in c.execute(q)]
def j(o):return json.dumps(o,ensure_ascii=False,sort_keys=True)
def write(name,items):
 assert items,name
 with (OUT/name).open("w",encoding="utf-8-sig",newline="") as f:
  w=csv.DictWriter(f,fieldnames=list(items[0]));w.writeheader();w.writerows(items)
def read(name):
 with (OUT/name).open(encoding="utf-8-sig",newline="") as f:return list(csv.DictReader(f))
def select():
 assert SRC.is_file() and not OUT.exists()
 OUT.mkdir(parents=True)
 with zipfile.ZipFile(SRC) as z:
  assert z.testzip() is None
  with z.open("B42_FURNITURE_CROSS_FACING_REVIEW_V22.sqlite") as a,DBTMP.open("wb") as b:shutil.copyfileobj(a,b)
 c=sqlite3.connect(DBTMP);c.row_factory=sqlite3.Row
 assert c.execute("PRAGMA integrity_check").fetchone()[0]=="ok"
 rect=rows(c,"SELECT * FROM v21_all_source_rectangle_template")
 parts=rows(c,"SELECT * FROM v21_source_tile_positioned_png")
 viewed=rows(c,"SELECT group_id,Facing FROM v21_direct_multisprite_grid_visual_observation UNION ALL SELECT group_id,Facing FROM v22_new_facing_original_grid")
 assert len(rect)==843 and len(parts)==2221 and len(viewed)==200
 prev_group={x["group_id"] for x in viewed}
 prev_pairs={(x["group_id"],x["Facing"]) for x in viewed}
 grouped=defaultdict(list);pmap=defaultdict(list)
 for x in rect:
  if int(x["raw_sprite_part_count"])>=2 and int(x["original_png_parts_missing"])==0:
   grouped[x["group_id"]].append(x)
 for p in parts:pmap[(p["group_id"],p["Facing"])].append(p)
 assert sum(len(x) for x in grouped.values())==820
 names=defaultdict(set)
 for n in rows(c,"SELECT rg.source_group_id AS group_id,r.display_name AS name FROM registry_entry_group rg JOIN registry_entry r ON rg.entry_id=r.entry_id WHERE r.source_system='WIKI'"):
  if n["name"]:names[n["group_id"]].add(n["name"])
 potential=[];named=0;eligible_total=0
 priorities=re.compile(r"bed|table|desk|chair|sofa|cabinet|wardrobe|dresser|shelf|bookshelf|cupboard|counter|stove|fridge|sink|locker|hospital|toilet|lamp|bench|couch|seat|rack|furniture",re.I)
 noise=re.compile(r"poster|sign|cow hide|animal hide|rock|boulder|sand pile|tent|dirt|road|grass|wall|floor|painting",re.I)
 order={"E":0,"S":1,"N":2,"W":3}
 for g,candidates in grouped.items():
  if g in prev_group:continue
  eligible=[v for v in candidates if 2<=int(v["raw_sprite_part_count"])<=9 and int(v["grid_w"])<=4 and int(v["grid_h"])<=4]
  if len(eligible)<2:continue
  eligible_total+=1
  eligible.sort(key=lambda x:(order.get(x["Facing"],99),x["Facing"]))
  aa=eligible[:2]
  name=sorted(names.get(g,()))[0] if names.get(g) else aa[0]["source_display_name"]
  is_source_only=int(aa[0]["source_only_group"])
  score=100*(not is_source_only)+40*bool(priorities.search(name or ""))-35*bool(noise.search(name or ""))
  score+=25*min(len(eligible),4)+5*min(int(aa[0]["raw_sprite_part_count"]),5)
  if int(aa[0]["grid_w"])!=int(aa[1]["grid_w"]) or int(aa[0]["grid_h"])!=int(aa[1]["grid_h"]):score+=20
  potential.append((score,g,aa,name or g))
 potential.sort(key=lambda t:(-t[0],t[1]))
 chosen=potential[:N]
 assert len(chosen)==N,(len(chosen),"not enough distinct paired facings")
 pairrows=[];faces=[];selectedparts=[];atlas=set()
 for i,(score,g,aa,name) in enumerate(chosen,1):
  assert g not in prev_group
  f1,f2=aa
  assert f1["Facing"]!=f2["Facing"]
  first=dict(pair_no=i,group_id=g,original_name=name,source_only_group=int(f1["source_only_group"]),
    Facing_A=f1["Facing"],Facing_B=f2["Facing"],
    original_grid_A=f'{f1["grid_w"]}x{f1["grid_h"]}',
    original_grid_B=f'{f2["grid_w"]}x{f2["grid_h"]}',
    source_part_count_A=int(f1["raw_sprite_part_count"]),
    source_part_count_B=int(f2["raw_sprite_part_count"]),
    candidate_sort_score=score,
    prior_v21_v22_visual_group_overlap=0,
    same_game_object_identity_certified=0,cross_facing_identity_certified=0)
  pairrows.append(first)
  for idx,rr in enumerate(aa):
   key=(g,rr["Facing"])
   assert key not in prev_pairs
   pp=pmap[key]
   assert len(pp)==int(rr["raw_sprite_part_count"])
   valid=set()
   for p in pp:
    coords=(int(p["relative_x"]),int(p["relative_y"]))
    assert coords not in valid and 0<=coords[0]<int(rr["grid_w"]) and 0<=coords[1]<int(rr["grid_h"])
    valid.add(coords)
    assert p["original_png_path"].startswith("Tiles/2x/") and p["original_png_path"].endswith(".png")
    atlas.add(p["original_png_path"])
    selectedparts.append(dict(pair_no=i,face_slot=("A" if idx==0 else "B"),**p))
   assert len(valid)==int(rr["grid_w"])*int(rr["grid_h"])
   faces.append(dict(pair_no=i,group_id=g,Facing=rr["Facing"],
    face_slot=("A" if idx==0 else "B"),width=int(rr["grid_w"]),height=int(rr["grid_h"]),
    original_parts=len(pp),original_keys_json=j([p["source_key"] for p in pp]),png_index_mapped_parts=len(pp),
    direct_visual_review_done=0,game_identity_certified=0))
 assert len(pairrows)==60 and len(faces)==120
 assert len({(x["group_id"],x["Facing"]) for x in faces})==120
 assert len({x["group_id"] for x in faces})==60
 write("V23_60_PAIR_SELECTION_SOURCE_ONLY.csv",pairrows)
 write("V23_120_FACING_GRID_CANDIDATES.csv",faces)
 write("V23_SELECTED_ORIGINAL_PART_POSITIONS.csv",selectedparts)
 (OUT/"_required_original_png_paths.txt").write_text("\n".join(sorted(atlas))+"\n",encoding="utf8")
 stat=dict(stage="SELECTED_PENDING_PIXEL_AND_VISUAL_REVIEW",
  original_complete_rectangles=843,original_multitile_rectangles=820,
  previous_direct_grid_visual_candidates=200,
  new_distinct_pair_groups=60,new_direction_candidates=120,
  new_direction_overlaps_with_v21_v22=0,new_group_overlaps_with_v21_v22=0,
  source_multiface_groups_eligible_after_prior_group_exclusions=eligible_total,
  selected_source_only_groups=sum(x["source_only_group"] for x in pairrows),
  selected_wiki_linked_groups=sum(not x["source_only_group"] for x in pairrows),
  original_png_atlases_required=len(atlas),selected_raw_part_positions=len(selectedparts),
  observed_pair_visual_review_rows=0,actual_game_object_identity_certified=0,
  warning_cases_unresolved=474)
 (OUT/"STAGING_MANIFEST.json").write_text(json.dumps(stat,ensure_ascii=False,sort_keys=True,indent=2)+"\n",encoding="utf8")
 c.close();DBTMP.unlink()
 print("V23_60_GROUPS_120_NEW_FACING_SOURCE_KEYS_PROVEN",j(stat),flush=True)
def render():
 pairs=read("V23_60_PAIR_SELECTION_SOURCE_ONLY.csv")
 parts=read("V23_SELECTED_ORIGINAL_PART_POSITIONS.csv")
 assert len(pairs)==60 and len({r["group_id"] for r in pairs})==60
 byface=defaultdict(list)
 for r in parts:byface[(r["group_id"],r["Facing"])].append(r)
 needed=sorted({r["original_png_path"] for r in parts})
 atlases={};digest={}
 for path in needed:
  fp=ROOT/path
  assert fp.is_file(),path
  digest[path]=hashlib.sha256(fp.read_bytes()).hexdigest()
  atlases[path]=Image.open(fp).convert("RGBA")
 crops={};pixelproof=[]
 for p in parts:
  atlas=atlases[p["original_png_path"]]
  w,h=int(p["original_cell_w"]),int(p["original_cell_h"])
  col,row=int(p["atlas_col"]),int(p["atlas_row"])
  assert w>0 and h>0 and col>=0 and row>=0
  xx,yy=col*w,row*h
  assert xx+w<=atlas.width and yy+h<=atlas.height
  cell=atlas.crop((xx,yy,xx+w,yy+h))
  sha=hashlib.sha256(cell.tobytes()).hexdigest()
  key=(int(p["pair_no"]),p["face_slot"],p["source_key"])
  crops[key]=cell
  pixelproof.append(dict(pair_no=p["pair_no"],face_slot=p["face_slot"],group_id=p["group_id"],Facing=p["Facing"],
   source_key=p["source_key"],raw_grid=p["raw_sprite_grid_pos"],
   relative_x=p["relative_x"],relative_y=p["relative_y"],
   png_path=p["original_png_path"],original_png_sha256=digest[p["original_png_path"]],
   png_cell_pixel_sha256=sha,atlas_col=col,atlas_row=row,cell_w=w,cell_h=h,
   actual_original_pixels_cropped=1,actual_in_game_object_certified=0))
 assert len(pixelproof)==len(parts)
 font=ImageFont.load_default()
 outpages=[];sha_pages={}
 for start in range(0,len(pairs),10):
  PW,PH=1260,380
  img=Image.new("RGB",(PW,5*PH),(243,245,247))
  draw=ImageDraw.Draw(img)
  for jx in range(10):
   ind=start+jx
   if ind>=len(pairs):break
   r=pairs[ind];g=r["group_id"];index=int(r["pair_no"]);left=jx%2;top=jx//2
   x0=left*(PW//2);y0=top*PH;cardw=PW//2
   draw.rectangle((x0+4,y0+4,x0+cardw-5,y0+PH-6),fill="white",outline=(162,177,188),width=2)
   name=r["original_name"][:65]
   draw.text((x0+14,y0+10),f'{index}. {name}',font=font,fill=(30,43,56))
   draw.text((x0+14,y0+29),f'{g} | left={r["Facing_A"]} {r["original_grid_A"]} | right={r["Facing_B"]} {r["original_grid_B"]}',font=font,fill=(75,87,104))
   for slot in ["A","B"]:
    f=r["Facing_"+slot];pp=byface[(g,f)]
    w=int(r["original_grid_"+slot].split("x")[0]);h=int(r["original_grid_"+slot].split("x")[1])
    step=min(235//w,225//h,102)
    originx=x0+(30 if slot=="A" else 340);originy=y0+66
    draw.text((originx,originy-12),f"Facing {f}",font=font,fill=(50,65,80))
    for ppitem in pp:
     relx,rely=int(ppitem["relative_x"]),int(ppitem["relative_y"])
     xx=originx+relx*(step+4);yy=originy+rely*(step+4)
     draw.rectangle((xx,yy,xx+step,yy+step),fill=(242,247,250),outline=(178,190,201))
     cell=crops[(index,slot,ppitem["source_key"])]
     thumb=cell.copy();thumb.thumbnail((max(1,step-8),max(1,step-18)),Image.Resampling.NEAREST)
     bg=Image.new("RGBA",thumb.size,(251,251,252,255));bg.alpha_composite(thumb)
     img.paste(bg.convert("RGB"),(xx+(step-thumb.width)//2,yy+(step-thumb.height)//2))
     draw.text((xx+3,yy+step-11),ppitem["source_key"].split("/")[-1][:12],font=font,fill=(66,78,88))
   draw.text((x0+14,y0+PH-32),"ORIGINAL SOURCE TILE GRID | NOT CERTIFIED 3D/ISOMETRIC GAME OBJECT",font=font,fill=(124,73,56))
  page=start//10+1
  filename=f"V23_60_PAIRS_FACING_CONTACT_{page:02d}.png"
  path=OUT/filename
  img.save(path,optimize=True)
  sha_pages[filename]=hashlib.sha256(path.read_bytes()).hexdigest()
  outpages.append(filename)
  (OUT/f"STAGED_V23_PAIR_CONTACT_{page:02d}_BASE64.txt").write_text(base64.b64encode(path.read_bytes()).decode("ascii"),encoding="ascii")
 for atlas in atlases.values():atlas.close()
 write("V23_DIRECT_ORIGINAL_SOURCE_PIXEL_SHA256.csv",pixelproof)
 manifest=json.loads((OUT/"STAGING_MANIFEST.json").read_text(encoding="utf8"))
 manifest.update(stage="RENDERED_PENDING_DIRECT_VISUAL_OBSERVATION",
  all_new_source_tile_crops_verified=len(pixelproof),distinct_original_png_sha_sources=len(digest),
  actual_pair_contact_page_count=len(outpages),original_pair_contact_sha256=sha_pages,
  visual_pair_groups_certified=0,actual_game_object_identity_certified=0)
 (OUT/"STAGING_MANIFEST.json").write_text(json.dumps(manifest,ensure_ascii=False,sort_keys=True,indent=2)+"\n",encoding="utf8")
 print("V23_60_FACING_PAIRS_120_CANDIDATES_REAL_ORIGINAL_PNG_RENDERED",j(manifest),flush=True)
if __name__=="__main__":
 if len(sys.argv)!=2 or sys.argv[1] not in ("--select","--render"):raise SystemExit("use --select or --render")
 if sys.argv[1]=="--select":select()
 else:render()
