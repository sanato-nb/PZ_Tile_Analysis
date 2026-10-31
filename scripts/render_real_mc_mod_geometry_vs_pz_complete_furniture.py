#!/usr/bin/env python3
"""Render neutral shape diagrams of REAL Minecraft JAR models for manually matched
Rosewood furniture; compare to complete Project Zomboid sprite assembly references.
This does not reproduce or distribute copyrighted mod textures/meshes.
"""
import csv,io,json,math,re,urllib.request,zipfile
from pathlib import Path
from collections import defaultdict
from PIL import Image,ImageDraw,ImageFont

D=Path(__file__).resolve().parents[1]/"analysis/rosewood_furniture/2026-10-31"
C=D/"minecraft_real_furniture_matches_v2/ROSEWOOD_357_PZ_TO_REAL_MINECRAFT_BLOCKSTATE_MATCH.csv"
PREV=D/"complete_furniture_visual_3d_v1"
SRC=D/"minecraft_actual_mod_registry_v2/MOD_VERSION_SOURCES.json"
OUT=D/"minecraft_model_geometry_comparison_v1"
LABELS=[
("Bed","Large Oak"),("Couch","Blue Rattan"),("Chair","Grey"),
("Table","Large Oak"),("Fridge","White"),("Oven","Modern"),
("Toilet","Fancy"),("Wardrobe","Oak"),("Computer","Desktop"),
("Television","Antique"),("Microwave","Chrome"),("Bath","Large Deluxe"),
("Jukebox","Oldies"),("Piano","Western"),("Grand Piano","Black"),
("Shelves","Large Metal"),("Counter","Steel"),("Machine","PAWS Pinball")
]
def read(p):
 with p.open(encoding="utf-8-sig",newline="") as f:return list(csv.DictReader(f))
def write(p,rows):
 with p.open("w",encoding="utf-8-sig",newline="") as f:
  w=csv.DictWriter(f,list(rows[0]),extrasaction="ignore");w.writeheader();w.writerows(rows)
def font(n=15):
 p="/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
 return ImageFont.truetype(p,n) if Path(p).exists() else ImageFont.load_default()
def get(url):
 req=urllib.request.Request(url,headers={"User-Agent":"RosewoodFurnitureCompare/1.0"})
 with urllib.request.urlopen(req,timeout=180) as r:return r.read()
def jar_for(mod,info):
 if mod=="refurbished":
  return get("https://mediafilez.forgecdn.net/files/7110/922/refurbished_furniture-forge-1.20.1-1.0.20.jar")
 v=next(x for x in info if x["label"]==mod)
 metadata=json.loads(get("https://api.modrinth.com/v2/version/"+v["version_id"]).decode("utf-8"))
 files=sorted([f for f in metadata["files"] if f["filename"]==v["download_filename"]],key=lambda f:not f.get("primary",False))
 if not files:raise RuntimeError("Version JAR not found "+mod)
 return get(files[0]["url"])
def json_obj(z,path):
 try:return json.loads(z.read(path).decode("utf8"))
 except Exception:return None
def box_triangles(x1,y1,z1,x2,y2,z2):
 v=[(x1,y1,z1),(x2,y1,z1),(x2,y2,z1),(x1,y2,z1),
    (x1,y1,z2),(x2,y1,z2),(x2,y2,z2),(x1,y2,z2)]
 faces=[(0,1,2),(0,2,3),(4,6,5),(4,7,6),
        (0,5,1),(0,4,5),(1,6,2),(1,5,6),
        (2,7,3),(2,6,7),(3,4,0),(3,7,4)]
 return [tuple(v[i] for i in f) for f in faces]
def render(tris,size=(380,340)):
 if not tris:return None,None
 coords=[p for f in tris for p in f]
 xs=[p[0] for p in coords];ys=[p[1] for p in coords];zs=[p[2] for p in coords]
 bbox=[round(max(xs)-min(xs),3),round(max(ys)-min(ys),3),round(max(zs)-min(zs),3)]
 projected=[]
 for tri in tris:
  uv=[((x-y)*.866,(x+y)*.5-z*1.15) for x,y,z in tri]
  a,b,c=tri;nx=(b[1]-a[1])*(c[2]-a[2])-(b[2]-a[2])*(c[1]-a[1])
  ny=(b[2]-a[2])*(c[0]-a[0])-(b[0]-a[0])*(c[2]-a[2])
  nz=(b[0]-a[0])*(c[1]-a[1])-(b[1]-a[1])*(c[0]-a[0])
  norm=math.sqrt(nx*nx+ny*ny+nz*nz) or 1
  light=abs((nx*(-.32)+ny*(-.38)+nz*.86)/norm)
  g=int(99+125*light)
  projected.append(((sum(x+y+z*.4 for x,y,z in tri))/3,uv,(g,g,g)))
 minx=min(x for _,ps,_ in projected for x,y in ps);maxx=max(x for _,ps,_ in projected for x,y in ps)
 miny=min(y for _,ps,_ in projected for x,y in ps);maxy=max(y for _,ps,_ in projected for x,y in ps)
 scale=min((size[0]-26)/max(0.01,maxx-minx),(size[1]-26)/max(.01,maxy-miny),185)
 w=(maxx-minx)*scale;h=(maxy-miny)*scale
 im=Image.new("RGB",size,(232,235,238));d=ImageDraw.Draw(im)
 def xy(p):return (int((p[0]-minx)*scale+(size[0]-w)/2),int((p[1]-miny)*scale+(size[1]-h)/2))
 for _,pts,col in sorted(projected,key=lambda x:x[0]):d.polygon([xy(p) for p in pts],fill=col)
 return im,bbox
def obj_triangles(z,path):
 if path not in z.namelist():return []
 verts=[];faces=[]
 for line in z.read(path).decode("utf8",errors="replace").splitlines():
  if line.startswith("v "):
   ar=line.split()
   if len(ar)>=4:
    try:verts.append(tuple(float(x) for x in ar[1:4]))
    except Exception:pass
  elif line.startswith("f "):
   fields=line.split()[1:]
   try:
    ids=[int(t.split("/")[0])-1 for t in fields]
    for j in range(1,len(ids)-1):
     if all(0<=idx<len(verts) for idx in (ids[0],ids[j],ids[j+1])):
      faces.append(tuple(verts[i] for i in (ids[0],ids[j],ids[j+1])))
   except Exception:pass
 return faces
def resolve_models(z,namespace,reference,seen=None,depth=0):
 if seen is None:seen=set()
 if depth>=10 or not reference:return [],"RECURSION_LIMIT_OR_NONE"
 # model reference "modid:block/subfolder/x" or "block/x"
 ns,rel=(reference.split(":",1) if ":" in reference else (namespace,reference))
 path=f"assets/{ns}/models/{rel}.json"
 if path in seen:return [],"RECURSION"
 seen.add(path)
 model=json_obj(z,path)
 if model is None:
  if ns=="minecraft" and rel in ("block/cube_all","block/cube"):
   return box_triangles(0,0,0,1,1,1),"VANILLA_UNIT_CUBE_FALLBACK"
  return [],"MISSING_MODEL_JSON:"+path
 tris=[];reason="JSON_CUBOID_ELEMENTS"
 # Model JSON uses x,z horizontal; y vertical. output as x,y,z where z=height
 if isinstance(model.get("elements"),list):
  for e in model["elements"]:
   a=e.get("from",[]);b=e.get("to",[])
   if len(a)==3 and len(b)==3:
    tris+=box_triangles(a[0]/16,a[2]/16,a[1]/16,
                        b[0]/16,b[2]/16,b[1]/16)
 if not tris and model.get("loader","").lower().endswith("obj"):
  ref=model.get("model","")
  if ref:
   o_ns,o_rel=(ref.split(":",1) if ":" in ref else (ns,ref))
   target=f"assets/{o_ns}/models/{o_rel}"
   if not target.endswith(".obj"):target+=".obj"
   tris=obj_triangles(z,target);reason="RAW_OBJ_GEOMETRY"
 if not tris and model.get("parent"):
  tris,reason=resolve_models(z,ns,model["parent"],seen,depth+1)
 return tris,reason if tris else "NO_RESOLVED_GEOMETRY"
def blockstate_models(z,blockstate):
 state=json_obj(z,blockstate)
 if not state:return [],"MISSING_BLOCKSTATE"
 models=[]
 if isinstance(state.get("variants"),dict):
  variants=state["variants"]
  options=sorted(variants.items(),key=lambda p:(len(p[0]),p[0]))
  for key,variant in options:
   if any(w in key for w in ("open=true","powered=true","waterlogged=true")):continue
   vals=variant if isinstance(variant,list) else [variant]
   models.extend((v.get("model","") for v in vals if isinstance(v,dict)))
   if models:break
 elif isinstance(state.get("multipart"),list):
  for part in state["multipart"][:4]:
   values=part.get("apply",{})
   models.extend(v.get("model","") for v in (values if isinstance(values,list) else [values]) if isinstance(v,dict))
 return models[:9],"STATE_REFERENCE"
def parse_mc(z,id):
 ns,name=id.split(":",1)
 bs=f"assets/{ns}/blockstates/{name}.json"
 refs,state=blockstate_models(z,bs)
 tris=[];reasons=[]
 for ref in refs:
  v,reason=resolve_models(z,ns,ref)
  tris.extend(v);reasons.append(reason)
 return tris,refs,"|".join(reasons) if reasons else state
def main():
 if OUT.exists() and any(OUT.iterdir()):raise FileExistsError("do not overwrite")
 OUT.mkdir(parents=True,exist_ok=True)
 rows=read(C);selected=[]
 for name,group in LABELS:
  r=next((r for r in rows if r["pz_model_name"]==name and r["pz_model_style"]==group),None)
  if r:selected.append(r)
 assert len(selected)>=15
 info=json.loads(SRC.read_text("utf8"))
 needed=sorted({x["mc_primary_mod"] for x in selected if x["mc_primary_mod"]})
 jars={}
 for mod in needed:
  raw=jar_for(mod,info)
  jars[mod]=zipfile.ZipFile(io.BytesIO(raw))
  print("loaded temporary mod zip",mod,len(raw),flush=True)
 outputs=[]
 for i,r in enumerate(selected,1):
  source_id=r["mc_primary_blockstate_id"]
  img=None;bbox=None;modelrefs=[];reason="NO_MC_ASSET_SELECTED";tri_count=0
  if source_id and r["mc_primary_mod"] in jars:
   tris,modelrefs,reason=parse_mc(jars[r["mc_primary_mod"]],source_id)
   tri_count=len(tris)
   img,bbox=render(tris)
  card=Image.new("RGB",(1250,450),(246,248,249));dr=ImageDraw.Draw(card)
  title=r["pz_model_name"]+" / "+r["pz_model_style"]
  dr.text((18,10),title,fill=(22,34,46),font=font(24))
  dr.text((18,42),"PZ completed original sprites + PZ3D (left) vs real MC mod model block geometry (right)",
          fill=(50,66,77),font=font(14))
  source_png=r["pz_3d_geometry_png"]
  if source_png and (PREV/"geometry_samples"/source_png).is_file():
   with Image.open(PREV/"geometry_samples"/source_png) as orig:
    orig=orig.convert("RGB");orig.thumbnail((822,354));card.paste(orig,(4,78))
  else:
   with Image.open(PREV/r["pz_complete_png_path"]) as orig:
    orig=orig.convert("RGB");orig.thumbnail((360,320));card.paste(orig,(40,90))
  if img:card.paste(img,(857,78))
  else:dr.text((880,220),"NO RECONSTRUCTED MC GEOMETRY",font=font(15),fill=(136,71,63))
  dr.text((18,428),"MC asset: "+(source_id or "none")+" | "+reason[:110],fill=(86,44,39),font=font(13))
  fname=f"{i:02d}_"+re.sub(r"[^a-z0-9]+","_",title.lower()).strip("_")+".png"
  card.save(OUT/fname,optimize=True)
  outputs.append(dict(pz_name=r["pz_model_name"],pz_style=r["pz_model_style"],
   pz_parts=r["pz_original_sprite_parts"],pz_3d_reference=r["pz_3d_geometry_bbox_xyz"],
   mc_mod=r["mc_primary_mod"],mc_blockstate_id=source_id,
   mc_rendered_triangles=tri_count,mc_model_references="|".join(modelrefs),
   mc_model_shape_resolution=reason,mc_derived_geometry_xyz="|".join(map(str,bbox)) if bbox else "",
   comparison_image=fname,actual_texture_compared="NO",
   pz_full_3d_vs_mc_full_3d_certified="NO",requires_manual_view="YES"))
 for z in jars.values():z.close()
 write(OUT/"REAL_MC_MODEL_GEOMETRY_COMPARISONS.csv",outputs)
 sheets=[]
 for st in range(0,len(outputs),4):
  pg=Image.new("RGB",(2500,900),(250,250,250))
  for ix,row in enumerate(outputs[st:st+4]):
   with Image.open(OUT/row["comparison_image"]) as im:
    pg.paste(im,((ix%2)*1250,(ix//2)*450))
  name=f"MC_REAL_MODEL_COMPARE_{st//4+1:02d}.jpg"
  pg.save(OUT/name,quality=83,optimize=True);sheets.append(name)
 manifest={"samples":len(outputs),"mc_actual_json_model_geometry_rendered":
   sum(int(x["mc_rendered_triangles"])>0 for x in outputs),
  "model_without_renderable_mesh":sum(int(x["mc_rendered_triangles"])==0 for x in outputs),
  "source_jars_temporary":needed,
  "model_textures_redistributed":False,
  "notes":"Derived neutral-shaded model elements, without mod textures; not engine-quality or exact geometry equivalence."}
 (OUT/"MANIFEST.json").write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+"\n",encoding="utf8")
 (OUT/"README_KO.md").write_text("# 로즈우드 원본 완성 가구와 실제 Minecraft 1.20.1 Forge 모델 비교\n\n"+
  "실제 배포된 모드의 blockstates JSON을 열고 연결된 블록 모델의 큐보이드 기하를 복원한 무텍스처 형상도와 좀보이드 완성 가구 PNG/PZ3D를 비교하는 증거 자료다.\n"+
  f"\n- {len(outputs)}개 샘플, 모델 요소 기하 복원 성공 {manifest['mc_actual_json_model_geometry_rendered']}개\n"+
  "- 실제 Minecraft 게임 내 렌더링(블록 방향/이웃 연결/동작)은 미검증.\n"+
  "- PZ 쪽 다칸 가구 부품은 앞서 완성형 이미지로 조립된 것을 비교한다.\n"+
  "- JAR/OBJ/원본 텍스처는 재배포하지 않고 사용자 연구용 무텍스처 도식만 제공.\n"+
  "- 실제 가구 외형 1:1 확정값이 아니라 수동 시각 검수를 위한 근거다.\n",encoding="utf8")
 with zipfile.ZipFile(OUT/"MC_REAL_GEOMETRY_COMPARISON_SHEETS.zip","w",zipfile.ZIP_DEFLATED,compresslevel=6) as pack:
  for p in OUT.iterdir():
   if p.name!="MC_REAL_GEOMETRY_COMPARISON_SHEETS.zip":pack.write(p,p.name)
 print("RESULT",json.dumps(manifest,ensure_ascii=False),flush=True)
if __name__=="__main__":main()
