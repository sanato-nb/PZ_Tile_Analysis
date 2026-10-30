#!/usr/bin/env python3
"""v251: reconstruct genuine B/C of each held key with only ONE actual occurrence.
A is original source atlas crop verified by raw RGBA SHA, no novel fake A or D.
"""
from pathlib import Path
from functools import lru_cache
from collections import Counter,defaultdict
import csv,json,re,bisect,xml.etree.ElementTree as ET,hashlib,sys,io,os
from PIL import Image,ImageDraw,ImageChops,ImageEnhance,ImageFont
ROOT=Path(__file__).resolve().parents[1]
MAPS=ROOT/"B4220.3_MapExport_256/tmx"
GROUP=int(os.environ.get("V251_GROUP","0"));GROUPS=4
assert 0<=GROUP<GROUPS
OUT=ROOT/"review/v251_held188_single_location_Afirst_2026-10-30"/"real_BC"/f"g{GROUP}"
OUT.mkdir(parents=True,exist_ok=True)
W,H=800,580
# Prioritize representative equipment, multipart furniture, decals, wall corners and previously missing imagery.
SELECTED=[] # populated exactly from v251 A source verified 188 list
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
original=readcsv(ROOT/"review/v251_held188_single_location_Afirst_2026-10-30/A_ORIGINAL_188_SHA_AND_ONLY_REAL_TMX.csv")
assert len(original)==188 and len({r["source_key"] for r in original})==188
selected=[x for i,x in enumerate(sorted(original,key=lambda r:int(r["source_index"]))) if i%GROUPS==GROUP]
assert len(selected)==47
SELECTED=[int(r["source_index"]) for r in selected]
chosen=[]
for row in selected:
  chosen.append(dict(source_index=row["source_index"],source_key=row["source_key"],
    tmx=row["only_real_TMX"],level=row["only_real_level"],layer_index=row["only_real_layer_index"],
    x=row["only_real_x"],y=row["only_real_y"],raw_gid=row["only_real_raw_gid"],rank="0",
    same_cell_higher_layers="unassessed"))
assert len(chosen)==47
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
rows=[]
try:font=ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",15)
except OSError:font=ImageFont.load_default()
for i,r in enumerate(chosen):
 l=loc(r);m=mapread(l["tmx"])
 k=(l["tile_set_name"],l["local_id"])
 A=sprite(k)
 assert A is not None
 selectedA=selected[i]
 assert sha(A.tobytes())==selectedA["A_RGBA_SHA256"],("A exact RGBA",k)
 B,missingB=scene(m,l)
 C,missingC=scene(m,l,deleted=True)
 throughB,missingTB=scene(m,l,through=l["layer_index"])
 throughC,missingTC=scene(m,l,through=l["layer_index"],deleted=True)
 full,diff=difference(B,C)
 target,thru_diff=difference(throughB,throughC)
 source_alpha=sum(v>0 for v in A.getchannel("A").getdata())
 assert source_alpha==int(selectedA["A_nontransparent_alpha_pixels"])
 name=f'{int(r["source_index"]):04d}_SINGLE_REAL_BC.png'
 row=dict(source_index=int(r["source_index"]),source_key=r["source_key"],
  actual_original_TMX=l["tmx"],TMX_sha256=tsha[l["tmx"]],original_level=l["level"],
  original_layer=l["layer_index"],x=l["x"],y=l["y"],actual_raw_gid=l["raw_gid"],
  A_sha256=sha(A.tobytes()),A_nontransparent_pixels=source_alpha,
  original_full_BC_diff=full,through_target_layer_BC_diff=target,
  original_scene_missing_sprite_B=missingB.get("missing_source",0),
  original_scene_missing_sprite_C=missingC.get("missing_source",0),
  original_canvas_clipping_B=missingB.get("outside_canvas",0),
  original_canvas_clipping_C=missingC.get("outside_canvas",0),
  original_scene_tmx_boundary_5x5_incomplete=int(l["x"]<2 or l["y"]<2 or l["x"]>m["w"]-3 or l["y"]>m["h"]-3),
  original_genuine_scene_used_only=1,second_original_TMX_site_found=0,
  evidence_panel=f"real_BC/g{GROUP}/{name}",
  source_key_official_identity_certified=0)
 rows.append(row)
 sheet=Image.new("RGB",(1600,620),(245,248,251));d=ImageDraw.Draw(sheet)
 d.text((12,9),f'SINGLE REAL TMX: {r["source_key"]} | {l["tmx"]} L{l["level"]} layer{l["layer_index"]} @{l["x"]},{l["y"]} GID{l["raw_gid"]}',font=font,fill="#263f56")
 d.text((12,36),f'A alpha {source_alpha} | original B-C={full} | through-layer={target} | missing={row["original_scene_missing_sprite_B"]} | border-truncated={row["original_scene_tmx_boundary_5x5_incomplete"]}',font=font,fill="#264458")
 for j,(title,img) in enumerate([("SOURCE A (RGBA)",A),("TRUE B single site",B),("TRUE C target removed",C),("B-C DIFFERENCE",ImageEnhance.Contrast(diff).enhance(6).convert("RGB"))]):
  d.text((j*400+10,66),title,font=font,fill="#32465b")
  pic=img.copy();pic.thumbnail((394,518),Image.Resampling.NEAREST)
  x=j*400+(400-pic.width)//2; y=89+(518-pic.height)//2
  if pic.mode=="RGBA":sheet.paste(pic,(x,y),pic)
  else:sheet.paste(pic,(x,y))
 sheet.save(OUT/name,optimize=True)
 print("rendered single-use",i+1,"/",len(chosen),r["source_key"],"BC",full,"through",target,flush=True)
with (OUT/"SINGLE_47_TRUE_BC.csv").open("w",encoding="utf-8-sig",newline="") as f:
 w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
# Smaller contact sheets (A and B) make image-only visual screening feasible
for page in range(3):
 pool=rows[page*16:(page+1)*16]
 board=Image.new("RGB",(480*4,350*4),(236,242,247));d=ImageDraw.Draw(board)
 for ii,row in enumerate(pool):
  x=(ii%4)*480;y=(ii//4)*350
  d.rectangle((x+3,y+3,x+477,y+347),fill="#fff",outline="#a9bbc8")
  d.text((x+12,y+10),f'{row["source_index"]} {row["source_key"][:40]}',font=font,fill="#253d4e")
  A=sprite(tuple([row["source_key"].rsplit("/",1)[0],int(row["source_key"].rsplit("/",1)[1])]))
  ab=A.getchannel("A").getbbox()
  cut=A.crop((max(0,ab[0]-3),max(0,ab[1]-3),min(A.width,ab[2]+3),min(A.height,ab[3]+3)))
  cut.thumbnail((222,272),Image.Resampling.NEAREST)
  # scale small A without changing source; only for visual diagnostic
  factor=min((220/max(1,cut.width)),(270/max(1,cut.height)),5)
  if factor>1:cut=cut.resize((max(1,int(cut.width*factor)),max(1,int(cut.height*factor))),Image.Resampling.NEAREST)
  with Image.open(OUT/f'{int(row["source_index"]):04d}_SINGLE_REAL_BC.png') as panel:
   B=panel.convert("RGB").crop((400,90,800,605))
  B.thumbnail((240,272),Image.Resampling.NEAREST)
  d.text((x+8,y+32),"A pixels",font=font,fill="#657a8b");d.text((x+250,y+32),"B original",font=font,fill="#657a8b")
  board.paste(cut,(x+8+(226-cut.width)//2,y+56+(272-cut.height)//2),cut)
  board.paste(B,(x+238+(240-B.width)//2,y+56+(272-B.height)//2))
  d.text((x+12,y+324),f'BC {row["original_full_BC_diff"]} | LAYER {row["through_target_layer_BC_diff"]} | missing {row["original_scene_missing_sprite_B"]}',font=font,fill="#176955" if row["original_full_BC_diff"]>0 else "#a65b2c")
 board.save(OUT/f"SINGLE47_A_B_CONTACT_{page:02d}.png",optimize=True)
manifest=dict(version="v251",group=GROUP,scope_188=188,verified_original_single_site_keys=len(rows),
 source_A_RGBA_hash_matched=47,original_TMX_SHA_verified=True,
 B_C_true_single_site_rendered=len(rows),
 B_C_nonzero=sum(x["original_full_BC_diff"]>0 for x in rows),
 B_C_zero=sum(x["original_full_BC_diff"]==0 for x in rows),
 source_neighbor_missing_some=sum(x["original_scene_missing_sprite_B"]>0 for x in rows),
 map_boundary_5x5_partial=sum(x["original_scene_tmx_boundary_5x5_incomplete"] for x in rows),
 upper_layer_delta_greater=sum(x["through_target_layer_BC_diff"]>x["original_full_BC_diff"] for x in rows),
 contact_A_B_pages=3,official_certification=0)
(OUT/"MANIFEST.json").write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+"\n",encoding="utf8")
print(json.dumps(manifest),flush=True)
