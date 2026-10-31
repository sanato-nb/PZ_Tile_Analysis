#!/usr/bin/env python3
"""v248: reconstruct B/C from original TMX at another real placement for 237 held keys.
A is original source atlas crop verified by raw RGBA SHA, no novel fake A or D.
"""
from pathlib import Path
from functools import lru_cache
from collections import Counter,defaultdict
import csv,json,re,bisect,xml.etree.ElementTree as ET,hashlib,sys,io,os
from PIL import Image,ImageDraw,ImageChops,ImageEnhance,ImageFont
ROOT=Path(__file__).resolve().parents[1]
MAPS=ROOT/"B4220.3_MapExport_256/tmx"
GROUP=int(os.environ.get("V248_GROUP","0")); GROUPS=4
assert 0<=GROUP<GROUPS
OUT=ROOT/"review/v248_held251_full_alternate_BC_2026-10-30"/"groups"/f"g{GROUP}"
OUT.mkdir(parents=True,exist_ok=True)
W,H=800,580
# Prioritize representative equipment, multipart furniture, decals, wall corners and previously missing imagery.
SELECTED=[] # selected from source-exact v246 census below
LIMIT=2
def readcsv(p):
 with p.open(encoding="utf-8-sig",newline="") as f:return list(csv.DictReader(f))
def sha(b):return hashlib.sha256(b).hexdigest()
def filesha(p):
 h=hashlib.sha256()
 with p.open('rb') as f:
  for a in iter(lambda:f.read(1024*1024),b''):h.update(a)
 return h.hexdigest()
ledger={int(r["source_index"]):r for r in readcsv(ROOT/"review/v238_integrated_master_2026-10-29/MASTER_HELD_439_SOURCE_VERIFIED.csv")}
v119={(r["tile_set_name"],int(r["local_id"])):r for r in readcsv(ROOT/"review/v119_selected_A_new4633/REPRESENTATIVE_A_4633.csv")}
v117={(r["tile_set_name"],int(r["local_id"])):r for r in readcsv(ROOT/"review/v117_A_candidates_10042/A_CANDIDATE_COMBINED_10042.csv")}
best=readcsv(ROOT/"review/v246_held439_real_alt_TMX_2026-10-30/BEST_FIVE_REAL_ALTERNATE_SITES.csv")
v117manifest=json.loads((ROOT/"review/v117_A_candidates_10042/MANIFEST.json").read_text("utf8"))
tsha={r["tmx"]:r["sha256"] for r in v117manifest["source_tmx"]}
census=readcsv(ROOT/"review/v246_held439_real_alt_TMX_2026-10-30/HELD439_ALTERNATE_SITE_CENSUS.csv")
prior247={int(r["source_index"]) for r in readcsv(ROOT/"review/v247_held439_alternate_true_BC_selected_2026-10-30/TRUE_ALTERNATE_ORIGINAL_TMX_BC_SELECTED.csv")}
all251=sorted(int(r["source_index"]) for r in census if int(r["alternative_real_positions"])>0)
assert len(all251)==251 and len(prior247)==14 and prior247.issubset(set(all251))
not_yet=[i for i in all251 if i not in prior247]
assert len(not_yet)==237
SELECTED=[i for position,i in enumerate(not_yet) if position%GROUPS==GROUP]
print("selected v248 group",GROUP,len(SELECTED),flush=True)
chosen=[]
for idx in SELECTED:
 entries=[x for x in best if int(x["source_index"])==idx]
 entries.sort(key=lambda x:(int(x["map_margin_cells"])<2,int(x["same_cell_higher_layers"]),-int(x["map_margin_cells"]),int(x["rank"])))
 if not entries:continue
 chosen.extend(entries[:LIMIT])
assert len(chosen)>=10,(len(chosen),SELECTED)
def layerlevel(ly):
 if "level" in ly.attrib:return int(ly.get("level"))
 p=ly.find("properties/property[@name='level']")
 return int((p.get("value") or p.text or "0") if p is not None else "0")
@lru_cache(maxsize=20)
def mapread(name):
 f=MAPS/name
 assert filesha(f)==tsha[name],("TMX SHA mismatch",name)
 root=ET.parse(f).getroot()
 ts=sorted((int(x.get("firstgid")),x.get("name")) for x in root.findall("tileset") if x.get("name"))
 first=[v[0] for v in ts]
 w,h=int(root.get("width","256")),int(root.get("height","256"))
 layers=[]
 for ix,ly in enumerate(root.iter("layer")):
  dat=ly.find("data")
  assert dat is not None and dat.get("encoding")=="csv"
  val=[int(v) for v in re.findall(r"\d+",dat.text or "")]
  assert len(val)==w*h
  layers.append({"index":ix,"level":layerlevel(ly),"values":val})
 return {"w":w,"h":h,"ts":ts,"first":first,"layers":layers}
def resolve(m,raw):
 gid=raw&0x0fffffff
 if gid==0:return None
 p=bisect.bisect_right(m["first"],gid)-1
 if p<0:return None
 return (m["ts"][p][1],gid-m["ts"][p][0])
def cropbbox(t):
 return tuple(int(v) for v in t.strip("[]").split(",")) if t else None
def sprite_record(k):
 if k in v119:
  a=v119[k];return a["source_image_path"],cropbbox(a["selected_crop_xyxy"]),a["selected_rgba_pixel_sha256"]
 if k in v117:
  a=v117[k];choice=a.get("new_preferred_A","")
  if choice=="A3":return a.get("source_png_path",""),cropbbox(a.get("A3_crop_bbox","")),a.get("A3_pixel_sha256","")
  if choice in ("A1","A1=A2"):return a.get("source_png_path",""),cropbbox(a.get("A1_bbox","")),a.get("A1_pixel_sha256","")
  if choice=="A2":return a.get("source_png_path",""),cropbbox(a.get("A2_bbox","")),a.get("A2_pixel_sha256","")
 return "",None,""
def loc(row):
 return dict(tmx=row["tmx"],level=int(row["level"]),layer_index=int(row["layer_index"]),
       x=int(row["x"]),y=int(row["y"]),raw_gid=int(row["raw_gid"]),
       tile_set_name=row["source_key"].rsplit("/",1)[0],local_id=int(row["source_key"].rsplit("/",1)[1]))
def needed_atlases():
 paths=set()
 for x in chosen:
  l=loc(x);m=mapread(l["tmx"])
  for layer in m["layers"]:
   if layer["level"]!=l["level"]:continue
   for dy in range(-2,3):
    y=l["y"]+dy
    if not 0<=y<m["h"]:continue
    for dx in range(-2,3):
     x2=l["x"]+dx
     if not 0<=x2<m["w"]:continue
     raw=layer["values"][y*m["w"]+x2]
     if not raw:continue
     k=resolve(m,raw)
     if k is None:continue
     path,bbox,expected=sprite_record(k)
     if path and bbox and expected: paths.add(path)
 # ensure selected source A
 for idx in SELECTED:
  h=ledger[idx];key=(h["tile_set_name"],int(h["local_id"]))
  p,b,e=sprite_record(key)
  if p:paths.add(p)
 return sorted(paths)
if "--list-tmx" in sys.argv:
 for p in sorted({x["tmx"] for x in chosen}):print("B4220.3_MapExport_256/tmx/"+p)
 sys.exit(0)
if "--list-png" in sys.argv:
 for p in needed_atlases():print(p)
 sys.exit(0)
@lru_cache(maxsize=80)
def atlas(path):
 if not path:return None
 p=ROOT/path
 if not p.exists():return None
 with Image.open(p) as im:return im.convert("RGBA")
@lru_cache(maxsize=4000)
def sprite(k):
 if k is None:return None
 path,box,expected=sprite_record(k)
 if not path or not box or not expected:return None
 a=atlas(path)
 if a is None or box[0]<0 or box[1]<0 or box[2]>a.width or box[3]>a.height:return None
 image=a.crop(box)
 assert sha(image.tobytes())==expected,("A pixel hash",k,path)
 return image if image.getbbox() else None
def flip(im,raw):
 if raw&0x20000000:im=im.transpose(Image.Transpose.TRANSPOSE)
 if raw&0x80000000:im=im.transpose(Image.Transpose.FLIP_LEFT_RIGHT)
 if raw&0x40000000:im=im.transpose(Image.Transpose.FLIP_TOP_BOTTOM)
 return im
def scene(m,l,deleted=False,through=None):
 x0,y0,level,layerid=l["x"],l["y"],l["level"],l["layer_index"]
 cell=y0*m["w"]+x0
 assert m["layers"][layerid]["values"][cell]==l["raw_gid"]
 assert resolve(m,l["raw_gid"])==(l["tile_set_name"],l["local_id"])
 base=Image.new("RGBA",(W,H),(237,242,247,255))
 miss=Counter();removed=0
 for layer in m["layers"]:
  if layer["level"]!=level or (through is not None and layer["index"]>through):continue
  cmds=[]
  for dy in range(-2,3):
   y=y0+dy
   if not 0<=y<m["h"]:continue
   for dx in range(-2,3):
    x=x0+dx
    if not 0<=x<m["w"]:continue
    p=y*m["w"]+x;gid=layer["values"][p]
    if gid:cmds.append((dx+dy,dy,dx,p,gid))
  cmds.sort()
  for _,dy,dx,p,raw in cmds:
   istarget=(layer["index"]==layerid and p==cell and raw==l["raw_gid"])
   if istarget and deleted: removed+=1;continue
   img=sprite(resolve(m,raw))
   if img is None:miss["missing_source"]+=1;continue
   img=flip(img,raw)
   px=int(W/2+(dx-dy)*58-img.width/2);py=int(H/2+(dx+dy)*29+34-img.height)
   if px<0 or py<0 or px+img.width>W or py+img.height>H:
    clip=(max(0,-px),max(0,-py),min(img.width,W-px),min(img.height,H-py))
    if clip[2]<=clip[0] or clip[3]<=clip[1]:miss["outside_canvas"]+=1;continue
    img=img.crop(clip);px=max(0,px);py=max(0,py)
   base.alpha_composite(img,(px,py))
 if deleted:assert removed==1
 return base.convert("RGB"),dict(miss)
def difference(a,b):
 d=ImageChops.difference(a,b).convert("L")
 return sum(v!=0 for v in d.getdata()),d
rows=[]; panels={}
for n,item in enumerate(chosen):
 l=loc(item);m=mapread(l["tmx"])
 A=sprite((l["tile_set_name"],l["local_id"]))
 assert A is not None
 B,mb=scene(m,l);C,mc=scene(m,l,deleted=True)
 limitedB,mlb=scene(m,l,through=l["layer_index"]);limitedC,mlc=scene(m,l,through=l["layer_index"],deleted=True)
 full,df=difference(B,C);uncovered,dl=difference(limitedB,limitedC)
 evidence_key=f"{int(item['source_index']):04d}_{n:02d}"
 rank=int(item["rank"])
 status=("incomplete_neighbor_sprites" if mb.get("missing_source",0) or mc.get("missing_source",0) else
         "no_visible_change_full_layers" if full==0 else
         "visible_in_original_scene")
 flags=dict(source_index=int(item["source_index"]),source_key=item["source_key"],alternative_rank=rank,
    source_tmx=l["tmx"],source_tmx_sha256=tsha[l["tmx"]],
    level=l["level"],layer_index=l["layer_index"],x=l["x"],y=l["y"],
    raw_gid=l["raw_gid"],same_cell_higher_layers=item["same_cell_higher_layers"],
    true_original_B_C_delta_pixels=full,layer_limited_B_C_delta_pixels=uncovered,
    neighbor_sprite_missing_B=mb.get("missing_source",0),neighbor_sprite_missing_C=mc.get("missing_source",0),
    outside_canvas_B=mb.get("outside_canvas",0),outside_canvas_C=mc.get("outside_canvas",0),
    source_A_pixel_sha=sha(A.tobytes()),source_A_file=sprite_record((l["tile_set_name"],l["local_id"]))[0],
    exposure_diagnosis=status,evidence_image=f"{evidence_key}_TRUE_ABC.png",
    different_real_TMX_location_not_official_D=1,identity_candidate_KO="",official_mapping_verified=0,tilezed_verified=0,final_identity_certified=0)
 rows.append(flags)
 sheet=Image.new("RGB",(1760,600),(247,249,250));draw=ImageDraw.Draw(sheet)
 try:font=ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",18)
 except OSError:font=ImageFont.load_default()
 draw.text((14,8),f"{item['source_key']} | {l['tmx']} {l['x']},{l['y']} L{l['level']} layer {l['layer_index']} GID{l['raw_gid']} | B-C={full} / through-layer={uncovered} / missing={mb.get('missing_source',0)}",fill="#192f42",font=font)
 diff=ImageEnhance.Contrast(df).enhance(6).convert("RGB")
 for j,(title,img) in enumerate([("ORIGINAL A",A),("ALT B TRUE TMX",B),("ALT C ONE GID REMOVED",C),("B-C PIXEL DIFFERENCE",diff)]):
  tile=img.copy();tile.thumbnail((425,500),Image.Resampling.NEAREST)
  px=j*440+(440-tile.width)//2;py=70+(500-tile.height)//2
  sheet.paste(tile,(px,py))
  draw.text((j*440+12,46),title,fill="#263746",font=font)
 sheet.save(OUT/flags["evidence_image"],optimize=True)
 print("TRUE_BC",len(rows),"/",len(chosen),flags["source_key"],l["tmx"],full,uncovered,status,flush=True)
fields=list(rows[0])
with (OUT/"TRUE_ALTERNATE_ORIGINAL_TMX_BC_SELECTED.csv").open("w",encoding="utf-8-sig",newline="") as f:
 w=csv.DictWriter(f,fieldnames=fields);w.writeheader();w.writerows(rows)

# Best independently sourced alternate scene per key, with A + true B visual index.
grouped=defaultdict(list)
for r in rows:grouped[int(r["source_index"])].append(r)
assert set(grouped)==set(SELECTED)
keyrows=[]
for idx in SELECTED:
    instances=grouped[idx]
    ordered=sorted(instances,key=lambda x:(
      x["neighbor_sprite_missing_B"]>0,
      x["outside_canvas_B"]>0,
      x["true_original_B_C_delta_pixels"]<=0,
      -x["true_original_B_C_delta_pixels"],
      -x["layer_limited_B_C_delta_pixels"]))
    winner=ordered[0]
    old=ledger[idx]
    keyrows.append(dict(source_index=idx,source_key=winner["source_key"],
      history_held_A_observation=old["A_visible_shape_from_held_reaudit"],
      actual_alternate_scenes_newly_rendered=len(instances),
      any_exposed_B_C=sum(x["true_original_B_C_delta_pixels"]>0 for x in instances),
      best_TMX=winner["source_tmx"],best_level=winner["level"],
      best_layer=winner["layer_index"],best_x=winner["x"],best_y=winner["y"],
      best_raw_gid=winner["raw_gid"],
      best_full_BC_change=winner["true_original_B_C_delta_pixels"],
      best_through_layer_change=winner["layer_limited_B_C_delta_pixels"],
      best_missing_neighbors=winner["neighbor_sprite_missing_B"],
      best_outside_canvas=winner["outside_canvas_B"],
      best_evidence_panel=winner["evidence_image"],
      all_evidence_panels=";".join(x["evidence_image"] for x in instances),
      source_A_pixel_SHA_verified=winner["source_A_pixel_sha"],
      inspected_visual_identity_individually_this_run=0,
      provisional_identity_candidate="",
      hold_reason="A/B/C scene prepared; individual A-first object review not yet recorded",
      mapping_verified=0,tilezed_verified=0,certified=0))
with (OUT/"PER_KEY_BEST_ALTERNATE.csv").open("w",encoding="utf-8-sig",newline="") as ff:
    w=csv.DictWriter(ff,fieldnames=list(keyrows[0]));w.writeheader();w.writerows(keyrows)
for page in range((len(keyrows)+19)//20):
    pageitems=keyrows[page*20:(page+1)*20]
    sheet=Image.new("RGB",(2000,1920),(235,239,245))
    d=ImageDraw.Draw(sheet)
    for j,z in enumerate(pageitems):
        x=(j%4)*500;y=(j//4)*384
        d.rectangle((x+3,y+3,x+497,y+381),fill="#fff",outline="#a8b9c9",width=2)
        d.text((x+12,y+11),f'{z["source_index"]}: {z["source_key"][:47]}',font=font,fill="#142b40")
        d.text((x+12,y+35),f'{z["best_TMX"]} L{z["best_level"]} layer{z["best_layer"]} @{z["best_x"]},{z["best_y"]}',font=font,fill="#43596b")
        original=Image.open(OUT/z["best_evidence_panel"]).convert("RGB")
        left=original.crop((0,140,440,550))
        right=original.crop((440,135,880,555))
        left.thumbnail((235,290),Image.Resampling.NEAREST)
        right.thumbnail((235,290),Image.Resampling.NEAREST)
        sheet.paste(left,(x+10+(235-left.width)//2,y+65+(290-left.height)//2))
        sheet.paste(right,(x+255+(235-right.width)//2,y+65+(290-right.height)//2))
        d.text((x+10,y+360),f'B-C {z["best_full_BC_change"]} / layer {z["best_through_layer_change"]} / missing {z["best_missing_neighbors"]}',font=font,fill="#b25c27" if z["best_full_BC_change"]==0 else "#176b57")
    sheet.save(OUT/f"A_FIRST_ALTERNATE_CONTACT_{page:02d}.png",optimize=True)
    print("CONTACT",GROUP,page,flush=True)

manifest=dict(version="v248",date="2026-10-30",group=GROUP,groups=GROUPS,all_in_scope=251,prior_v247=14,remaining_scope=237,selected_keys=len({r["source_key"] for r in rows}),
 genuine_alternate_locations_rendered=len(rows),exact_one_real_gid_removed=len(rows),
 source_A_crops_rgba_hash_checked=len(rows),all_tmx_sha256_verified=True,
 full_BC_positive=sum(r["true_original_B_C_delta_pixels"]>0 for r in rows),
 full_BC_zero=sum(r["true_original_B_C_delta_pixels"]==0 for r in rows),
 incomplete_neighbor_scene=sum(r["neighbor_sprite_missing_B"]>0 for r in rows),
 layer_limited_extra_exposure=sum(r["layer_limited_B_C_delta_pixels"]>r["true_original_B_C_delta_pixels"] for r in rows),
 changed_previous_held_status=0,final_identity_certifications=0,
 original_TMX_PNG_and_v240_master_untouched=True,
 true_different_TMX_site_not_same_key_official_A_D=True,
 list="TRUE_ALTERNATE_ORIGINAL_TMX_BC_SELECTED.csv",key_best="PER_KEY_BEST_ALTERNATE.csv",contacts=(len(keyrows)+19)//20,individual_visual_certifications_new=0,prior_excluded188_not_processed=True)
(OUT/"MANIFEST.json").write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+"\n",encoding="utf8")
print("COMPLETE",json.dumps(manifest),flush=True)
