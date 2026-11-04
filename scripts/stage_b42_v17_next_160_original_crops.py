#!/usr/bin/env python3
"""Stage 160 NEW and disjoint source-only original PZ sprite cells for direct visual review.
Staging is not a claim of visual review or game identity certification.
"""
import csv,hashlib,json,sqlite3,sys,zipfile,shutil,base64
from pathlib import Path
from collections import defaultdict,Counter
from PIL import Image,ImageDraw,ImageFont
R=Path(__file__).resolve().parents[1]
SRC=R/"analysis/furniture_full_b42/2026-11-04/visual_review_v16/B42_FURNITURE_MASTER_INVENTORY_V16.zip"
DIR=R/"analysis/furniture_full_b42/2026-11-04/visual_review_v17"
DB=Path("/tmp/pzb42_v17_staging.sqlite")
def q(c,s):
 return [dict(r) for r in c.execute(s)]
def init():
 assert SRC.is_file()
 with zipfile.ZipFile(SRC) as z:
  assert z.testzip() is None
  with z.open("B42_FURNITURE_MASTER_INVENTORY_V16.sqlite") as a,DB.open("wb") as b:shutil.copyfileobj(a,b)
 c=sqlite3.connect(DB);c.row_factory=sqlite3.Row
 assert c.execute("PRAGMA integrity_check").fetchone()[0]=="ok"
 before=q(c,"SELECT entry_id FROM v15_visual_part_observation UNION SELECT entry_id FROM v16_visual_part_observation")
 prior={x["entry_id"] for x in before}
 assert len(prior)==320
 all_source=q(c,"SELECT * FROM v14_source_only_ledger")
 assert len(all_source)==963
 imgs=defaultdict(list)
 for r in q(c,"SELECT i.tileset,i.local_id,i.png_path,i.grid_id,i.column_index,i.row_index,i.link_status,i.has_visible_pixels,a.cell_width,a.cell_height FROM image_cells i JOIN image_atlases a ON a.png_path=i.png_path WHERE i.tileset IS NOT NULL AND i.local_id IS NOT NULL"):
  imgs[(r["tileset"].lower(),r["local_id"])].append(r)
 ts=q(c,"SELECT source_key,tileset,local_id FROM furniture_tile")
 tiles={t["source_key"]:t for t in ts}
 eligible=[]
 for s in all_source:
  if s["entry_id"] in prior:continue
  k=s["original_png_tile_key"];t=tiles.get(k)
  if not t:continue
  options=[x for x in imgs[(t["tileset"].lower(),t["local_id"])] if x["png_path"]==s["original_png_path"] and
    x["column_index"] is not None and x["row_index"] is not None and x["cell_width"] and x["cell_height"]]
  if not options:continue
  a=options[0]
  tileset=s["tileset"].lower()
  score=(25 if tileset.startswith("furniture_") else 20 if tileset.startswith(("appliances_","fixtures_"))
   else 10 if tileset.startswith(("location_","crafted_")) else 5)
  score+=min(4,int(s["direction_templates"]))*3
  score+=min(3,int(s["geometrically_rectangular_candidates"]))*5
  score+=min(8,int(s["original_tile_count"]))
  score+=6 if s["original_png_path"] and a["has_visible_pixels"] else 0
  eligible.append((score,s,a))
 eligible.sort(key=lambda x:(-x[0],x[1]["tileset"],x[1]["entry_id"]))
 picks=[];already=set();atlas_caps=Counter()
 for limit in [4,8,10000]:
  for _,s,a in eligible:
   if len(picks)==160:break
   if s["entry_id"] in already or atlas_caps[a["png_path"]]>=limit:continue
   picks.append((s,a));already.add(s["entry_id"]);atlas_caps[a["png_path"]]+=1
  if len(picks)==160:break
 assert len(picks)==160,(len(picks),len(eligible))
 assert not prior.intersection(already)
 DIR.mkdir(parents=True,exist_ok=True)
 paths=sorted(atlas_caps)
 (DIR/"_v17_required_png_atlases.txt").write_text("\n".join(paths)+"\n",encoding="utf8")
 with (DIR/"V17_160_NEW_SOURCE_TILE_SELECTION.csv").open("w",encoding="utf-8-sig",newline="") as f:
  fields=["sample_index","entry_id","group_id","original_name","tileset","source_key","png_path",
   "grid_id","column_index","row_index","cell_width","cell_height","prior_v15_v16_review_overlap"]
  w=csv.DictWriter(f,fieldnames=fields);w.writeheader()
  for i,(s,a) in enumerate(picks,1):
   w.writerow(dict(sample_index=320+i,entry_id=s["entry_id"],group_id=s["group_id"],
    original_name=s["original_name"],tileset=s["tileset"],source_key=s["original_png_tile_key"],
    png_path=a["png_path"],grid_id=a["grid_id"],column_index=a["column_index"],
    row_index=a["row_index"],cell_width=a["cell_width"],cell_height=a["cell_height"],
    prior_v15_v16_review_overlap=0))
 c.close()
 print("V17_NEW_SOURCE_STAGED_SELECTION",json.dumps(dict(new=160,existing=320,distinct_total=480,
   selected_atlases=len(paths),first_new_group=picks[0][0]["group_id"]),ensure_ascii=False),flush=True)
def render():
 assert DIR.exists()
 with (DIR/"V17_160_NEW_SOURCE_TILE_SELECTION.csv").open(encoding="utf-8-sig",newline="") as f:
  rows=list(csv.DictReader(f))
 assert len(rows)==160
 cached={};pngsha={};pix=[]
 for r in rows:
  p=r["png_path"];full=R/p;img=None;ph="";status="OK"
  try:
   assert full.exists(),full
   if p not in cached:
    pngsha[p]=hashlib.sha256(full.read_bytes()).hexdigest()
    cached[p]=Image.open(full).convert("RGBA")
   w,h=int(r["cell_width"]),int(r["cell_height"])
   x,y=int(r["column_index"])*w,int(r["row_index"])*h
   atlas=cached[p]
   assert 0<=x<=atlas.width-w and 0<=y<=atlas.height-h and w>0 and h>0
   img=atlas.crop((x,y,x+w,y+h))
   ph=hashlib.sha256(img.tobytes()).hexdigest()
   assert img.getbbox() is not None,"all transparent"
  except Exception as e:status="FAIL:"+str(e)[:120]
  r.update(png_sha256=pngsha.get(p,""),crop_pixel_sha256=ph,crop_status=status,
    visually_inspected=0,game_identity_certified=0)
  pix.append(img)
 for img in cached.values():img.close()
 with (DIR/"V17_160_NEW_ORIGINAL_PNG_CROP_SHA256.csv").open("w",encoding="utf-8-sig",newline="") as f:
  w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
 font=ImageFont.load_default();sheetshas={}
 for start in range(0,160,40):
  cardw,cardh=237,219
  board=Image.new("RGB",(5*cardw,8*cardh),(239,244,248))
  d=ImageDraw.Draw(board)
  for j in range(40):
   i=start+j;r=rows[i];x0=j%5*cardw;y0=j//5*cardh
   d.rectangle((x0+3,y0+3,x0+cardw-3,y0+cardh-3),fill=(255,255,255),outline=(174,189,201),width=2)
   cell=pix[i]
   if cell:
    thumb=cell.copy();thumb.thumbnail((213,153),Image.Resampling.NEAREST)
    backdrop=Image.new("RGBA",thumb.size,(251,251,253,255))
    backdrop.alpha_composite(thumb)
    board.paste(backdrop.convert("RGB"),(x0+(cardw-thumb.width)//2,y0+7+(153-thumb.height)//2))
   d.text((x0+7,y0+166),str(320+i+1)+". "+r["source_key"][:34],font=font,fill=(38,54,69))
   d.text((x0+7,y0+185),r["crop_status"][:28],font=font,fill=(74,87,103))
   d.text((x0+7,y0+203),p.split("/")[-1][:32] if (p:=r["png_path"]) else "",font=font,fill=(79,89,104))
  page=start//40+1
  fn=DIR/("V17_NEW_SOURCE_CONTACT_%02d.png"%page)
  board.save(fn,optimize=True)
  raw=fn.read_bytes();sheetshas[str(page)]=hashlib.sha256(raw).hexdigest()
  (DIR/("STAGED_V17_CONTACT_%02d_BASE64.txt"%page)).write_text(base64.b64encode(raw).decode("ascii"),encoding="ascii")
 manifest=dict(stage="V17_NEW_PNG_EXTRACTED_BUT_NOT_YET_VISUALLY_CLASSIFIED",
  source_only_groups=963,previously_reviewed_v15_v16=320,new_source_only_samples=160,
  distinct_source_only_samples=480,overlap_with_v15_v16=0,original_png_atlas_count=len(pngsha),
  original_png_pixel_crops_ok=sum(r["crop_status"]=="OK" for r in rows),
  failed=[r["source_key"] for r in rows if r["crop_status"]!="OK"],
  stage_image_reviewed=0,actual_game_objects_certified=0,
  contact_sheet_sha256=sheetshas)
 (DIR/"STAGING_MANIFEST.json").write_text(json.dumps(manifest,ensure_ascii=False,indent=2,sort_keys=True)+"\n",encoding="utf8")
 print("V17_NEW_ORIGINAL_PIXELS_EXTRACTED",json.dumps(manifest,ensure_ascii=False),flush=True)
if __name__=="__main__":
 assert len(sys.argv)==2
 if sys.argv[1]=="--select":init()
 elif sys.argv[1]=="--crop":render()
 else:raise SystemExit("select or crop")
