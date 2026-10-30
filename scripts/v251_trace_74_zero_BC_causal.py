#!/usr/bin/env python3
"""v251: trace 74 B/C-zero genuine single-location sprite keys by actual draw order.
A is original source atlas crop verified by raw RGBA SHA, no novel fake A or D.
"""
from pathlib import Path
from functools import lru_cache
from collections import Counter,defaultdict
import csv,json,re,bisect,xml.etree.ElementTree as ET,hashlib,sys,io,os
from PIL import Image,ImageDraw,ImageChops,ImageEnhance,ImageFont
ROOT=Path(__file__).resolve().parents[1]
MAPS=ROOT/"B4220.3_MapExport_256/tmx"
OUT=ROOT/"review/v251_held188_single_location_Afirst_2026-10-30"/"occlusion74"
OUT.mkdir(parents=True,exist_ok=True)
W,H=800,580
# Prioritize representative equipment, multipart furniture, decals, wall corners and previously missing imagery.
SELECTED=[] # derived from the verified v248 still-unexposed list below
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
v117manifest=json.loads((ROOT/"review/v117_A_candidates_10042/MANIFEST.json").read_text("utf8"))
tsha={r["tmx"]:r["sha256"] for r in v117manifest["source_tmx"]}
real=readcsv(ROOT/"review/v251_held188_single_location_Afirst_2026-10-30/REAL_ORIGINAL_SINGLE_188_BC.csv")
assert len(real)==188
pending=sorted([x for x in real if int(x["original_full_BC_diff"])==0],key=lambda x:int(x["source_index"]))
assert len(pending)==74
chosen=[]
for r in pending:
 chosen.append(dict(source_index=r["source_index"],source_key=r["source_key"],
  tmx=r["actual_original_TMX"],level=r["original_level"],layer_index=r["original_layer"],
  x=r["x"],y=r["y"],raw_gid=r["actual_raw_gid"],rank="1",
  expected_full=int(r["original_full_BC_diff"]),expected_through=int(r["through_target_layer_BC_diff"])))
SELECTED=sorted(int(x["source_index"]) for x in chosen)
assert len(SELECTED)==len(set(SELECTED))==74
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

def fit_draw(canvas,img,dx,dy,raw):
  img=flip(img,raw)
  px=int(W/2+(dx-dy)*58-img.width/2)
  py=int(H/2+(dx+dy)*29+34-img.height)
  clip=(max(0,-px),max(0,-py),min(img.width,W-px),min(img.height,H-py))
  if clip[2]<=clip[0] or clip[3]<=clip[1]:return None
  if px<0 or py<0 or px+img.width>W or py+img.height>H:
    img=img.crop(clip); px=max(0,px);py=max(0,py)
  return (img,px,py)
def boxclamp(img,px,py):
  local=img.getchannel("A").getbbox()
  if local is None:return None
  return (px+local[0],py+local[1],px+local[2],py+local[3])
def overlaps(a,b):
  return bool(a and b and min(a[2],b[2])>max(a[0],b[0]) and min(a[3],b[3])>max(a[1],b[1]))
def dcount(B,C,region):
  if region is None:return 0
  di=ImageChops.difference(B.crop(region).convert("RGB"),C.crop(region).convert("RGB")).convert("L")
  return sum(bool(v) for v in di.getdata())
def analyze(row):
 l=loc(row);m=mapread(l["tmx"])
 pos=l["y"]*m["w"]+l["x"]
 assert m["layers"][l["layer_index"]]["values"][pos]==l["raw_gid"]
 assert resolve(m,l["raw_gid"])==(l["tile_set_name"],l["local_id"])
 B=Image.new("RGBA",(W,H),(237,242,247,255))
 C=B.copy()
 target=False;target_box=None;A=None;crop_placed=None
 initial_diff=None;through_diff=None;full_diff=None;post=0;missing=0;occlusion=[]
 seen_target=0
 for layer in m["layers"]:
  if layer["level"]!=l["level"]:continue
  cmds=[]
  for dy in range(-2,3):
   y=l["y"]+dy
   if not 0<=y<m["h"]:continue
   for dx in range(-2,3):
    x=l["x"]+dx
    if not 0<=x<m["w"]:continue
    p=y*m["w"]+x; raw=layer["values"][p]
    if raw:cmds.append((dx+dy,dy,dx,p,raw))
  cmds.sort()
  for _,dy,dx,p,raw in cmds:
   k=resolve(m,raw)
   img=sprite(k)
   if img is None:
    missing+=1
    continue
   placed=fit_draw(B,img,dx,dy,raw)
   if placed is None:continue
   img,px,py=placed
   box=boxclamp(img,px,py)
   istarget=(layer["index"]==l["layer_index"] and p==pos and raw==l["raw_gid"])
   if istarget:
    seen_target+=1; A=img.copy();crop_placed=(px,py)
    target_box=box
    if box is None:raise AssertionError("A no nontransparent pixels "+str(l))
    B.alpha_composite(img,(px,py))
    initial_diff=dcount(B,C,target_box)
    target=True
   else:
    before=None
    if target and overlaps(target_box,box):
      before=dcount(B,C,target_box)
    B.alpha_composite(img,(px,py));C.alpha_composite(img,(px,py))
    if before is not None:
      after=dcount(B,C,target_box)
      if before!=after:
        occlusion.append(dict(
          occluder_tmx=l["tmx"],occluder_layer=layer["index"],occluder_level=layer["level"],
          occluder_x=l["x"]+dx,occluder_y=l["y"]+dy,
          occluder_raw_gid=raw,occluder_key=(k[0]+"/"+str(k[1])) if k else "",
          original_target_pixels_before=before,original_target_pixels_after=after,
          target_pixels_suppressed=max(0,before-after),
          target_pixels_exposed=max(0,after-before),
          same_layer_as_target=int(layer["index"]==l["layer_index"]),
          sprite_alpha_bbox=str(box),
          exact_same_canvas_and_draw_order=True))
  if layer["index"]==l["layer_index"]:
   through_diff=dcount(B,C,target_box)
 assert seen_target==1 and initial_diff is not None
 assert target_box is not None
 full_diff=dcount(B,C,target_box)
 # Verify exact original B-C pixels across entire canvas (not only target canvas)
 dif=ImageChops.difference(B.convert("RGB"),C.convert("RGB")).convert("L")
 full_all=sum(bool(v) for v in dif.getdata())
 # The v248 difference image used convert("L") on RGB difference; use identical convention.
 assert full_all==int(row["expected_full"]),(row["source_key"],full_all,row["expected_full"])
 assert through_diff==int(row["expected_through"]),(row["source_key"],through_diff,row["expected_through"])
 # Pixel-level delta created on source tile placement, without other later draw.
 source_alpha=sum(bool(v) for v in A.getchannel("A").getdata())
 later=max(0,initial_diff-full_diff)
 # B last: exact same actual source A placed over final C to prove graphic isn't blank; diagnostic, not original scene.
 target_last=C.copy();target_last.alpha_composite(A,crop_placed)
 target_last_changed=dcount(target_last,C,target_box)
 # Selected culprit: actual following sprites that suppressed target B-C stepwise, no identity inferred.
 culprits=[r for r in occlusion if r["target_pixels_suppressed"]>0]
 if full_diff!=0:status="unexpected_nonzero"
 elif initial_diff>0 and culprits:status="source_target_contributes_then_is_occluded"
 elif initial_diff==0 and source_alpha>0:status="target_draw_has_no_RGB_delta_in_scene_despite_source_alpha"
 elif initial_diff>0 and not culprits:status="no_detected_culprit_despite_initial_delta"
 else:status="missing_source_or_unresolved"
 output=dict(source_index=int(row["source_index"]),source_key=row["source_key"],
   original_tmx=l["tmx"],original_tmx_sha256=tsha[l["tmx"]],level=l["level"],
   target_layer=l["layer_index"],target_x=l["x"],target_y=l["y"],target_raw_gid=l["raw_gid"],
   target_A_RGBA_sha256=sha(sprite((l["tile_set_name"],l["local_id"])).tobytes()),
   target_A_alpha_nonzero_pixels=source_alpha,target_canvas_bbox=str(target_box),
   original_B_C_full_scene_pixels=full_all,
   immediately_after_target_RGB_difference=initial_diff,
   through_target_layer_B_C_pixels=through_diff,
   after_all_layers_B_C_pixels=full_diff,
   render_target_last_diagnostic_delta=target_last_changed,
   later_same_layer_culprits=sum(r["same_layer_as_target"] for r in culprits),
   later_different_layer_culprits=sum(not r["same_layer_as_target"] for r in culprits),
   total_actual_oversprite_suppressor_events=len(culprits),
   max_individual_suppressor_pixels=max((r["target_pixels_suppressed"] for r in culprits),default=0),
   best_suppressor_key=max(culprits,key=lambda r:r["target_pixels_suppressed"])["occluder_key"] if culprits else "",
   best_suppressor_raw_gid=max(culprits,key=lambda r:r["target_pixels_suppressed"])["occluder_raw_gid"] if culprits else "",
   missing_other_scene_sprite_sources=missing,
   classification=status,
   user_excluded188_unmodified=True,official_identity_certified=False)
 evidence=Image.new("RGB",(1800,780),(248,250,252));d=ImageDraw.Draw(evidence)
 try:ft=ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",18)
 except OSError:ft=ImageFont.load_default()
 d.text((16,10),f'{row["source_key"]}  {l["tmx"]} @{l["x"]},{l["y"]} L{l["level"]} layer{l["layer_index"]}',fill="#162c40",font=ft)
 d.text((16,38),f'after target={initial_diff}  target layer={through_diff}  final={full_all}  culprits={len(culprits)}  last={target_last_changed}',fill="#324d64",font=ft)
 for i,(title,image) in enumerate([("A verified",sprite((l["tile_set_name"],l["local_id"]))),("Original B",B.convert("RGB")),("Original C",C.convert("RGB")),("Target drawn last (diagnostic)",target_last.convert("RGB"))]):
  render=image.copy();render.thumbnail((425,555),Image.Resampling.NEAREST)
  x=i*450+(450-render.width)//2;y=94+(555-render.height)//2
  if i==0 and render.mode=="RGBA":evidence.paste(render,(x,y),render)
  else:evidence.paste(render,(x,y))
  d.text((i*450+8,70),title,fill="#243b4a",font=ft)
 d.text((15,695),"Diagnostic target-last is not the game's actual B. C removes one source raw GID only.",fill="#a34e35",font=ft)
 fname=f'{int(row["source_index"]):04d}_OCCLUDER_CAUSAL.png'
 evidence.save(OUT/fname,optimize=True)
 output["diagnostic_contact"]=fname
 return output,occlusion
results=[]; events=[]
for i,r in enumerate(chosen):
 o,occ=analyze(r)
 results.append(o)
 for ev in occ:
  events.append(dict(source_index=int(r["source_index"]),source_key=r["source_key"],**ev))
 print("V249",i+1,"/",len(chosen),o["source_key"],o["classification"],o["immediately_after_target_RGB_difference"],o["total_actual_oversprite_suppressor_events"],flush=True)
def writecsv(path,items,fields):
 with path.open("w",encoding="utf-8-sig",newline="") as f:
  w=csv.DictWriter(f,fieldnames=fields);w.writeheader();w.writerows(items)
writecsv(OUT/"38_TARGET_STEPWISE_OCCLUSION_DIAGNOSTICS.csv",results,list(results[0]))
columns=list(events[0]) if events else ["source_index","source_key"]
writecsv(OUT/"EXACT_FOLLOWING_GID_CAUSAL_PIXEL_CHANGES.csv",events,columns)
counts=Counter(x["classification"] for x in results)
manifest=dict(version="v251_zero74",date="2026-10-30",scope_single188=188,selected_still_no_BC_exposure=74,
 no_alternative_original_TMX_sites_exist=True,original_TMX_sha_verified_for_all_selected=True,
 original_A_RGBA_pixel_hash_verified_for_all_selected=True,
 original_BC_pixel_diff_reproduced_from_v251_for_all=74,
 target_original_A_alpha_nontransparent_for_all=74,
 selected_C_removed_one_exact_original_GID=74,
 source_target_draw_initially_visible=sum(x["immediately_after_target_RGB_difference"]>0 for x in results),
 source_target_draw_initially_zero=sum(x["immediately_after_target_RGB_difference"]==0 for x in results),
 visually_exposed_in_full_scene=0,
 identified_direct_following_source_suppressor_count=sum(x["total_actual_oversprite_suppressor_events"] for x in results),
 keys_with_direct_suppressor_events=sum(x["total_actual_oversprite_suppressor_events"]>0 for x in results),
 status_counts=dict(counts),
 missing_neighbors_in_selected_scenes=sum(x["missing_other_scene_sprite_sources"] for x in results),
 new_official_LocalID_authentications=0,new_final_identity_certifications=0,
 previous_v240_active_and_excluded_unchanged=True,previous_v248_v249_v250_ledgers_unchanged=True,
 raw_source_TMX_PNG_and_SQLite_untouched=True,
 warning="Causal suppressor list is computed in v251 5x5 original TMX renderer draw order; a positive suppression per raw GID proves that drawing that specific sprite reduces target color difference on this canvas, not official game engine occlusion. Target-last is diagnostic only.")
(OUT/"MANIFEST.json").write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
print(json.dumps(manifest,ensure_ascii=False),flush=True)
