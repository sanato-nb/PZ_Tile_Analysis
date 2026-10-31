#!/usr/bin/env python3
"""357 completed Project Zomboid furniture objects vs REAL published Minecraft mod assets.

Each comparison card: LEFT source PZ completed pixels (not a disconnected sprite),
RIGHT render of actual mod blockstate model elements with extracted original textures,
or explicitly UNRENDERABLE/UNMATCHED status. Native files not redistributed.
No runtime collision box/function invented. Minecraft model JSON/variants inspected.
"""
from __future__ import annotations
import csv,io,json,re,sqlite3,html,hashlib,math,urllib.request,zipfile
from collections import Counter,defaultdict
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont,ImageOps,ImageStat
import numpy as np
import cv2

ROOT=Path(__file__).resolve().parents[1]
D=ROOT/"analysis/rosewood_furniture/2026-10-31"
OUT=D/"visual_pz_vs_mc_357_v1"
SOURCE=D/"minecraft_real_furniture_matches_v4/ROSEWOOD_357_PZ_TO_REAL_MINECRAFT_BLOCKSTATE_MATCH.csv"
PZIMG=D/"complete_furniture_visual_3d_v1"
CROSS=D/"complete_furniture_visual_3d_v1/ALL_357_COMPLETE_FURNITURE_3D_CROSSWALK.csv"
DB=ROOT/"analysis/current/v259/PZ_v259_all_png_tile_definitions.sqlite"
VER=D/"minecraft_actual_mod_registry_v2/MOD_VERSION_SOURCES.json"
SHEET=OUT/"cards"
BG=(239,243,247)
MCBG=(228,235,241)
def readcsv(p):
 with p.open(encoding="utf-8-sig",newline="") as f:return list(csv.DictReader(f))
def writecsv(p,rows):
 with p.open("w",encoding="utf-8-sig",newline="") as f:
  w=csv.DictWriter(f,list(rows[0]),extrasaction="ignore");w.writeheader();w.writerows(rows)
def get(u):
 req=urllib.request.Request(u,headers={"User-Agent":"Rosewood-SideBySide-Compare/1.0"})
 with urllib.request.urlopen(req,timeout=160) as response:return response.read()
def downloadjar(v):
 if v["label"]=="refurbished":
  url="https://mediafilez.forgecdn.net/files/7110/922/refurbished_furniture-forge-1.20.1-1.0.20.jar"
 else:
  j=json.loads(get("https://api.modrinth.com/v2/version/"+v["version_id"]).decode("utf8"))
  a=next((x for x in j.get("files",[]) if x["filename"]==v["download_filename"]),None)
  if not a:raise RuntimeError("missing original file "+v["label"])
  url=a["url"]
 data=get(url)
 if hashlib.sha512(data).hexdigest()!=v["sha512"]:
  raise RuntimeError("JAR changed! "+v["label"])
 return zipfile.ZipFile(io.BytesIO(data))
def font(n=18):
 for p in ["/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
           "/usr/share/fonts/truetype/liberation2/LiberationSans-Regular.ttf"]:
  if Path(p).exists():return ImageFont.truetype(p,n)
 return ImageFont.load_default()
def font_ko(n=18):
 for p in ["/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc",
           "/usr/share/fonts/truetype/nanum/NanumGothic.ttf"]:
  if Path(p).exists():return ImageFont.truetype(p,n,index=1 if p.endswith(".ttc") else 0)
 return font(n)
def assetjson(jar,path):
 try:return json.loads(jar.read(path).decode("utf8"))
 except Exception:return None
def state_refs(jar,ns,name):
 obj=assetjson(jar,f"assets/{ns}/blockstates/{name}.json")
 if not isinstance(obj,dict):return [],{},{}
 observed={}
 refs=[]
 if isinstance(obj.get("variants"),dict):
  variants=obj["variants"]
  for key in variants:
   for pair in key.split(","):
    if "=" in pair:
     k,v=pair.split("=",1)
     observed.setdefault(k,set()).add(v)
  keys=sorted(variants,key=lambda s:(
    int("facing=north" not in s and "facing=east" not in s),
    int("part=head" in s or "type=right" in s or "half=upper" in s),
    int("open=true" in s or "powered=true" in s or "waterlogged=true" in s),
    len(s)))
  if keys:
   options=variants[keys[0]]
   refs=[x for x in (options if isinstance(options,list) else [options]) if isinstance(x,dict) and x.get("model")]
 elif isinstance(obj.get("multipart"),list):
  for part in obj["multipart"]:
   w=part.get("when")
   if isinstance(w,dict) and any(v in ("true","upper","right") for v in w.values() if isinstance(v,str)):continue
   a=part.get("apply",{})
   refs.extend(x for x in (a if isinstance(a,list) else [a]) if isinstance(x,dict) and x.get("model"))
 return refs,observed,obj
def resolve_model(z,base_ns,model,seen=None):
 if seen is None:seen=set()
 ns,path=model.split(":",1) if ":" in model else (base_ns,model)
 full=f"assets/{ns}/models/{path}.json"
 if full in seen:return None,{},[],["loop:"+full]
 seen.add(full)
 data=assetjson(z,full)
 if not isinstance(data,dict):
  return None,{},[],["missing_model:"+full]
 parent=data.get("parent","")
 textures={}
 elements=None
 origin=[]
 if parent:
  p,tex,ele,orig=resolve_model(z,ns,parent,seen)
  textures.update(tex)
  elements=ele
  origin+=orig
 textures.update(data.get("textures",{}) if isinstance(data.get("textures"),dict) else {})
 if isinstance(data.get("elements"),list):elements=data["elements"]
 origin.append(full)
 return data,textures,elements,origin
def texture(z,ns,texkey,texmap,cache):
 value=texkey
 for _ in range(12):
  if not isinstance(value,str):return None,None
  if not value.startswith("#"):break
  new=texmap.get(value[1:])
  if new is None or new==value:return None,None
  value=new
 if value.startswith("#"):return None,None
 tns,rel=(value.split(":",1) if ":" in value else (ns,value))
 if rel.startswith("textures/"):rel=rel[9:]
 path=f"assets/{tns}/textures/{rel}.png"
 if path not in cache:
  try:
   raw=z.read(path)
   with Image.open(io.BytesIO(raw)) as im:cache[path]=im.convert("RGBA")
  except Exception:cache[path]=None
 return cache[path],path
def rotate_elem(point,rotation):
 if not rotation:return point
 axis=rotation.get("axis","y");angle=float(rotation.get("angle",0))*math.pi/180
 origin=rotation.get("origin",[8,8,8])
 x,y,z=[point[i]-origin[i] for i in range(3)]
 c=math.cos(angle);s=math.sin(angle)
 if axis=="x":y,z=c*y-s*z,s*y+c*z
 elif axis=="y":x,z=c*x+s*z,-s*x+c*z
 elif axis=="z":x,y=c*x-s*y,s*x+c*y
 return tuple(v+o for v,o in zip((x,y,z),origin))
def faces_for_element(e):
 p=e.get("from",[]);q=e.get("to",[])
 if not(len(p)==len(q)==3):return []
 x,y,z=map(float,p);X,Y,Z=map(float,q)
 vertices={
  "north":[(x,y,z),(X,y,z),(X,Y,z),(x,Y,z)],
  "south":[(X,y,Z),(x,y,Z),(x,Y,Z),(X,Y,Z)],
  "west":[(x,y,Z),(x,y,z),(x,Y,z),(x,Y,Z)],
  "east":[(X,y,z),(X,y,Z),(X,Y,Z),(X,Y,z)],
  "up":[(x,Y,z),(X,Y,z),(X,Y,Z),(x,Y,Z)],
  "down":[(x,y,Z),(X,y,Z),(X,y,z),(x,y,z)],
 }
 def defaultuv(d):
  if d in ("north","south"):return [x,16-Y,X,16-y]
  if d in ("east","west"):return [z,16-Y,Z,16-y]
  return [x,z,X,Z]
 out=[]
 for direction,face in e.get("faces",{}).items():
  if direction not in vertices or not isinstance(face,dict):continue
  a=face.get("uv",defaultuv(direction))
  if not isinstance(a,list) or len(a)!=4:continue
  coords=[rotate_elem(v,e.get("rotation")) for v in vertices[direction]]
  out.append((coords,face,a,direction))
 return out
def project(p):
 x,y,z=p
 return ((x-z)*.866,(x+z)*.50-y*1.15)
def render_model(z,ns,id,cache):
 refs,properties,state=state_refs(z,ns,id)
 triples=[];origins=[];textures_evidence=[];missing=[]
 for ref in refs[:9]:
  model=ref["model"];pathmodel,texmap,elements,chain=resolve_model(z,ns,model)
  origins.extend(chain)
  if not elements:
   missing.append("no_element_geometry:"+model)
   continue
  for element in elements:
   for coords,face,uv,direction in faces_for_element(element):
    im,path=texture(z,ns,face.get("texture",""),texmap,cache)
    if path:textures_evidence.append(path)
    triples.append((coords,im,uv,direction,face.get("rotation",0)))
 if len(triples)>1500:
  triples=triples[:1500];missing.append("faces_truncated_at_1500")
 dims={}
 dims["possible_blockstate_properties"]={k:sorted(v)[:18] for k,v in properties.items()}
 dims["blockstate_variants"]=len(state.get("variants",{})) if isinstance(state.get("variants"),dict) else 0
 dims["blockstate_multipart_cases"]=len(state.get("multipart",[])) if isinstance(state.get("multipart"),list) else 0
 dims["model_sources"]=list(dict.fromkeys(origins))[:25]
 dims["texture_sources"]=list(dict.fromkeys(textures_evidence))[:25]
 dims["missing_geometry"]=missing[:20]
 dims["sample_model_references"]=[r["model"] for r in refs][:9]
 if not triples:return None,None,"NO_MODEL_GEOMETRY_IN_CURRENT_RENDERER",dims
 bounds=[p for coords,*others in triples for p in coords]
 spans=[(max(x[i] for x in bounds)-min(x[i] for x in bounds))/16 for i in range(3)]
 # Canvas fixed; screen axes x,vertical y,depth z
 SIZE=(470,330);rect=(24,24,446,306)
 projected=[(project(p),p) for p in bounds]
 umin=min(a[0] for a,p in projected);umax=max(a[0] for a,p in projected)
 vmin=min(a[1] for a,p in projected);vmax=max(a[1] for a,p in projected)
 scale=min((rect[2]-rect[0])/max(1,umax-umin),(rect[3]-rect[1])/max(1,vmax-vmin))
 ox=(SIZE[0]-(umax-umin)*scale)/2-umin*scale
 oy=(SIZE[1]-(vmax-vmin)*scale)/2-vmin*scale
 def pix(p):
  a,b=project(p);return (a*scale+ox,b*scale+oy)
 # sort far to near for painter's algorithm
 triples.sort(key=lambda r:sum(p[0]+p[2]+p[1]*.12 for p in r[0])/4)
 canvas=np.zeros((SIZE[1],SIZE[0],3),dtype=np.uint8)
 canvas[:]=np.array(MCBG,dtype=np.uint8)[::-1]
 true_textured=0
 for coords,tex,uv,direction,rot in triples:
  dst=np.array([pix(p) for p in coords],dtype=np.float32)
  if not np.isfinite(dst).all():continue
  if np.max(dst[:,0])-np.min(dst[:,0])<.6 or np.max(dst[:,1])-np.min(dst[:,1])<.6:continue
  normal=None
  a=np.array(coords[1])-np.array(coords[0])
  b=np.array(coords[2])-np.array(coords[0])
  n=np.cross(a,b);nlen=np.linalg.norm(n)
  light=abs(float(np.dot(n,np.array([-0.25,0.9,-0.4]))/(nlen or 1)))
  brightness=0.70+0.30*light
  if tex is None:
   cv2.fillConvexPoly(canvas,dst.astype(np.int32),tuple([int(150*brightness)]*3),lineType=cv2.LINE_AA)
   continue
  # Actual source texture atlas, UV mapped onto the cuboid face (no texture redistribution).
  tw,th=tex.size
  u0,v0,u1,v1=[float(q) for q in uv]
  src=np.array([(u0/16*tw,v0/16*th),(u1/16*tw,v0/16*th),
      (u1/16*tw,v1/16*th),(u0/16*tw,v1/16*th)],dtype=np.float32)
  # Model face rotation in 90-degree increments.
  k=(int(rot)//90)%4
  src=np.roll(src,k,axis=0)
  texarr=cv2.cvtColor(np.array(tex),cv2.COLOR_RGBA2BGRA)
  xmin=max(0,int(np.floor(np.min(dst[:,0]))));xmax=min(SIZE[0],int(np.ceil(np.max(dst[:,0]))+1))
  ymin=max(0,int(np.floor(np.min(dst[:,1]))));ymax=min(SIZE[1],int(np.ceil(np.max(dst[:,1]))+1))
  if xmin>=xmax or ymin>=ymax:continue
  local=dst-np.array([xmin,ymin],dtype=np.float32)
  matrix=cv2.getPerspectiveTransform(src,local)
  w,h=xmax-xmin,ymax-ymin
  warped=cv2.warpPerspective(texarr,matrix,(w,h),flags=cv2.INTER_NEAREST,
            borderMode=cv2.BORDER_CONSTANT,borderValue=(0,0,0,0))
  mask=np.zeros((h,w),dtype=np.uint8)
  cv2.fillConvexPoly(mask,local.astype(np.int32),255)
  alpha=(warped[:,:,3].astype(np.float32)/255.0)*(mask.astype(np.float32)/255.0)
  src_bgr=(warped[:,:,:3].astype(np.float32)*brightness).clip(0,255)
  target=canvas[ymin:ymax,xmin:xmax]
  target[:]=(src_bgr*alpha[:,:,None]+target*(1-alpha[:,:,None])).astype(np.uint8)
  true_textured+=1
 out=Image.fromarray(cv2.cvtColor(canvas,cv2.COLOR_BGR2RGB))
 dims["texture_mapped_faces"]=true_textured
 dims["geometry_face_count"]=len(triples)
 return out,spans,("REAL_MOD_TEXTURED_JSON_ELEMENTS" if true_textured else "REAL_MOD_UNTEXTURED_JSON_ELEMENTS"),dims
def pzprops(con,representative):
 accum=defaultdict(set)
 ids=representative.get("representative_source_tile_ids","").split("|")
 for raw in ids:
  if "/" not in raw:continue
  til,sid=raw.rsplit("/",1)
  try:n=int(sid)
  except ValueError:continue
  for key,val in con.execute("SELECT attribute,value FROM source_attributes WHERE name=? AND local_id=?",(til,n)):
   accum[key].add(val)
 return {k:sorted(v) for k,v in sorted(accum.items())}
def gridbbox(data):
 pos=[]
 for val in data.split("|"):
  m=re.fullmatch(r"\s*(-?\d+),\s*(-?\d+)\s*",val)
  if m:pos.append(tuple(map(int,m.groups())))
 if not pos:return None
 return [max(x for x,y in pos)-min(x for x,y in pos)+1,max(y for x,y in pos)-min(y for x,y in pos)+1]
def card(left,right,record,n):
 canvas=Image.new("RGB",(1170,535),(247,249,251));d=ImageDraw.Draw(canvas)
 f1=font_ko(23);f2=font_ko(15);f3=font_ko(14)
 title=f"{n:03d}  {record['pz_name']} / {record['pz_style']}"
 d.text((22,11),title[:78],font=f1,fill=(26,39,54))
 d.rounded_rectangle((20,52,567,435),radius=12,fill=(233,237,241))
 d.rounded_rectangle((598,52,1149,435),radius=12,fill=(229,234,240))
 d.text((38,67),"PROJECT ZOMBOID  |  Complete furniture",font=f2,fill=(44,68,92))
 d.text((615,67),"MINECRAFT  |  Actual mod model render",font=f2,fill=(44,68,92))
 if left is not None:
  im=left.copy().convert("RGBA")
  im.thumbnail((495,322),Image.Resampling.LANCZOS)
  canvas.paste(im,(int(293-im.width/2),int(249-im.height/2)),mask=im.getchannel("A"))
 else:d.text((96,210),"PZ PNG unavailable",font=f2,fill=(140,55,60))
 if right is not None:
  canvas.paste(right,(int(873-right.width/2),int(249-right.height/2)))
 else:
  d.text((652,191),"MC image not renderable from JSON",font=f2,fill=(157,53,54))
  d.text((633,228),"Mod asset ID is known, but geometry",font=f3,fill=(99,69,66))
  d.text((633,251),"cannot be verified by this renderer.",font=f3,fill=(99,69,66))
 d.line((22,454,1149,454),width=2,fill=(182,196,207))
 def fit(s,n=90):return s if len(s)<=n else s[:n-3]+"..."
 d.text((22,464),fit("PZ tiles: "+record["pz_size_tiles"]+" | 3D dims: "+record["pz_3d_bbox_blocks"]+
              "    MC model: "+record["mc_model_dims"]),font=f3,fill=(36,55,72))
 d.text((22,489),fit("MC: "+(record["mc_asset_id"] or "NO MATCH")+" | "+
              record["mc_render_status"],130),font=f3,fill=(76,62,60))
 d.text((22,509),"Dimensions are model geometry bounds, not collision or placement footprint.",font=font(12),fill=(109,75,69))
 return canvas
def safe(x):return re.sub(r"[^a-z0-9_-]","_",x.lower())[:50]
def build_html(rows):
 cards=[]
 for r in rows:
  title=r["pz_name"]+(" / "+r["pz_style"] if r["pz_style"] else "")
  status=r["mc_render_status"]
  item=(
   '<article class="tile" data-search="'+html.escape((title+" "+r["mc_mod"]+" "+r["mc_asset_id"]).lower(),quote=True)+
   '" data-state="'+html.escape(status,quote=True)+'">'
   '<img src="'+html.escape(r["card_path"],quote=True)+'" loading="lazy" alt="'+html.escape(title,quote=True)+'">'
   '<div class="details"><h2>'+html.escape(title)+'</h2>'
   '<p><b>좀보이드:</b> '+html.escape(r["pz_size_tiles"])+
   ' 칸 / 조각 '+html.escape(r["pz_parts"])+
   '개 / 3D 추정 폭·깊이·높이 '+html.escape(r["pz_3d_bbox_blocks"])+
   '</p><p><b>마크:</b> '+html.escape(r["mc_mod"] or "없음")+
   ' / <code>'+html.escape(r["mc_asset_id"] or "미매칭")+
   '</code> / 모델 경계치 '+html.escape(r["mc_model_dims"])+'</p>'+
   '<p><b>방향:</b> '+html.escape(r["pz_facing"])+
   ' | <b>마크 블록 상태:</b> '+html.escape(r["mc_blockstate_properties_display"][:250])+'</p>'+
   '<p><b>상태:</b> '+html.escape(status)+
   ' | <b>원본 타일 속성:</b> '+html.escape(r["pz_property_highlights"][:240])+'</p>'+
   '<details><summary>전체 원본 속성·모델 근거 보기</summary>'+
   '<pre>'+html.escape(json.dumps({"pz":json.loads(r["pz_properties_json"]),
                          "mc":json.loads(r["mc_properties_json"]),
                          "shape":r["mc_render_status"],
                          "source_tiled_ids":r["source_ids"]},ensure_ascii=False,indent=2))+'</pre>'+
   '</details></div></article>')
  cards.append(item)
 template='''<!DOCTYPE html><html lang="ko"><head><meta charset="utf-8">
 <meta name="viewport" content="width=device-width,initial-scale=1">
 <title>로즈우드 357개 완성 가구 vs 마크 가구 모드 실물 비교</title>
 <style>body{margin:0;background:#edf1f5;color:#172b3f;font:15px system-ui,"Noto Sans CJK KR",sans-serif}
 header{position:sticky;top:0;z-index:10;background:#f9fbfc;padding:18px 3vw;border-bottom:2px solid #d4dde5}
 h1{font-size:23px;margin:0 0 8px}p{line-height:1.55}aside{font-size:13px;max-width:1000px}
 .search{display:flex;gap:12px;flex-wrap:wrap}input,select{font:inherit;border:1px solid #becdd8;border-radius:8px;padding:11px}
 input{flex:1;min-width:230px}main{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,530px),1fr));gap:18px;padding:22px 3vw}
 .tile{background:white;border:1px solid #d5dfe8;border-radius:12px;padding:12px;box-shadow:0 3px 9px #152c4a12}
 img{width:100%;border-radius:7px;display:block;object-fit:contain;background:#f6f8fa}
 .details{padding:5px 10px}.details h2{font-size:17px;margin:10px 0}
 .details p{margin:5px 0;font-size:13px;line-height:1.55}details{margin-top:12px}
 pre{white-space:pre-wrap;overflow-wrap:anywhere;background:#f3f5f7;padding:10px;font-size:11px}
 footer{padding:16px;text-align:center}</style></head><body>
 <header><h1>프로젝트 좀보이드 로즈우드 ↔ 마인크래프트 가구 대조 — 357개</h1>
 <p>왼쪽: 실제 좀보이드 PNG 조합 완성 가구 │ 오른쪽: 설치 파일 내 블록 모델 원본 텍스처 렌더(가능한 경우).</p>
 <aside>⚠ 블록 자산 경로의 존재는 게임 런타임 레지스트리·실제 상호작용·시각적 1:1 일치를 의미하지 않습니다.
 비표준 동적 렌더/모델은 오른쪽 미렌더로 표시됩니다. PZ 타일 여러 장을 합친 예시는 시점·정렬 가정이 포함됩니다.
 크기는 PZ 공개 3D 좌표 경계치/원본 SpriteGridPos, MC 모델 요소 경계치를 별도로 표기합니다. 충돌 박스와 혼동하지 마세요.</aside>
 <div class="search"><input id="q" placeholder="가구명·모드·블록 ID 검색" aria-label="검색">
 <select id="filter"><option value="">전체</option><option value="REAL_MOD_TEXTURED_JSON_ELEMENTS">원본 텍스처 3D 렌더 성공</option>
 <option value="NO_MODEL_GEOMETRY_IN_CURRENT_RENDERER">3D 렌더 미지원</option>
 <option value="NO_MATCH">매칭 없음</option></select>
 <span id="count"></span></div></header><main id="main">__CONTENT__</main>
 <footer>소스: private PZ_Tile_Analysis; Java 1.20.1 Forge 모드 JAR 검사; Copyright belongs to original mod authors.</footer>
 <script>const cards=[...document.querySelectorAll(".tile")];const q=document.getElementById("q"),f=document.getElementById("filter"),c=document.getElementById("count");
 function sync(){let n=0;for(const x of cards){const show=x.dataset.search.includes(q.value.trim().toLowerCase())&&
 (!f.value||(f.value==="NO_MATCH"?x.dataset.state==="NO_MC_ASSET_SELECTED":x.dataset.state===f.value));
 x.style.display=show?"":"none";if(show)n++}c.textContent=n+" / "+cards.length+"개"}q.oninput=sync;f.onchange=sync;sync()</script></body></html>'''
 return template.replace("__CONTENT__","".join(cards))
def main():
 if OUT.exists() and any(OUT.iterdir()):raise FileExistsError("Never overwrite")
 SHEET.mkdir(parents=True,exist_ok=True)
 matches=readcsv(SOURCE);source=readcsv(CROSS)
 assert len(matches)==len(source)==357
 lookup={(x["CustomName"],x["GroupName"]):x for x in source}
 versions=json.loads(VER.read_text("utf8"))
 modes={r["mc_primary_mod"] for r in matches if r["mc_primary_mod"]}
 jars={}
 for mod in sorted(modes):
  v=next(x for x in versions if x["label"]==mod)
  jars[mod]=downloadjar(v)
  print("downloaded verified mod jar",mod,flush=True)
 con=sqlite3.connect("file:"+str(DB.resolve())+"?mode=ro",uri=True)
 texcache_by_mod=defaultdict(dict)
 images_cache={};records=[];statuses=Counter();mcrenders={}
 for i,row in enumerate(matches,1):
  ky=row["pz_model_name"],row["pz_model_style"]
  src=lookup[ky];prop=pzprops(con,src)
  footprint=gridbbox(src["representative_sprite_grid_positions"])
  widthheight=(f"{footprint[0]}×{footprint[1]}" if footprint else "1×1 (임시)")
  leftpath=PZIMG/row["pz_complete_png_path"]
  with Image.open(leftpath) as loaded:left=loaded.convert("RGBA")
  mod=row["mc_primary_mod"];rid=row["mc_primary_blockstate_id"]
  key=(mod,rid)
  if rid and mod in jars:
   if key not in mcrenders:
    ns,name=rid.split(":",1)
    mcrenders[key]=render_model(jars[mod],ns,name,texcache_by_mod[mod])
   right,bbox,state,mcprops=mcrenders[key]
  else:right,bbox,state,mcprops=None,None,"NO_MC_ASSET_SELECTED",{}
  propstr=", ".join(k+"="+",".join(v[:2]) for k,v in prop.items()
   if k in {"CustomName","GroupName","Facing","Material","MaterialType","IsMoveAble",
          "container","ContainerCapacity","solid","solidtrans","bed","surface","CanScrap","IsTable","IsLow","PhysicsMesh","BlocksPlacement"})
  pzbbox=row["pz_3d_geometry_bbox_xyz"]
  mcspans=("×".join(f"{float(x):.2f}" for x in bbox)+" (x×y높이×z 깊이)" if bbox else "미측정")
  allprops=json.dumps(prop,ensure_ascii=False,sort_keys=True)
  mcdata=json.dumps(mcprops,ensure_ascii=False,sort_keys=True)
  fname=f"{i:03d}_{safe(row['pz_model_name'])}_{safe(row['pz_model_style'])}.jpg"
  rec=dict(index=i,pz_name=row["pz_model_name"],pz_style=row["pz_model_style"],
   pz_parts=row["pz_original_sprite_parts"],pz_facing=src["representative_facing"],
   pz_size_tiles=widthheight,pz_3d_bbox_blocks=pzbbox or "미측정",
   pz_property_highlights=propstr,pz_properties_json=allprops,
   source_ids=src["representative_source_tile_ids"],
   mc_asset_id=rid,mc_mod=mod,mc_render_status=state,
   mc_model_dims=mcspans,mc_properties_json=mcdata,
   mc_blockstate_properties_display=", ".join(k+"="+"/".join(v[:6]) for k,v in mcprops.get("possible_blockstate_properties",{}).items()) or "미기재",
   mc_3d_model_elements=mcprops.get("geometry_face_count",0),
   mc_true_texture_faces=mcprops.get("texture_mapped_faces",0),
   mc_source_model_files="|".join(mcprops.get("model_sources",[])),
   mc_source_texture_files="|".join(mcprops.get("texture_sources",[])),
   mc_functional_capabilities="NOT_VERIFIED_BY_RUNTIME",
   pz_original_to_mc_visual_match="NOT_CERTIFIED",
   pz_source_preview=row["pz_complete_png_path"],
   card_path="cards/"+fname)
  card(left,right,rec,i).save(SHEET/fname,quality=85,optimize=True,subsampling=0)
  records.append(rec);statuses[state]+=1
  if i%35==0:print("rendered PZ vs MC",i,"/",len(matches),dict(statuses),flush=True)
 con.close()
 for z in jars.values():z.close()
 writecsv(OUT/"ALL_357_PZ_MC_VISUAL_SIZE_PROPERTIES.csv",records)
 (OUT/"INDEX.html").write_text(build_html(records),encoding="utf8")
 # 2 columns by 2 rows contact sheets, one card each at original size.
 contact=OUT/"contact_sheets";contact.mkdir()
 for i in range(0,len(records),4):
  page=Image.new("RGB",(2340,1070),(250,251,252))
  for j,row in enumerate(records[i:i+4]):
   with Image.open(OUT/row["card_path"]) as im:
    page.paste(im,((j%2)*1170,(j//2)*535))
  page.save(contact/f"COMPARE_{i//4+1:03d}.jpg",quality=79,optimize=True)
 manifest={"project":"Rosewood PZ finished sprite vs actual MC mod model",
  "total_pz_style_comparison_cards":len(records),"source_PZ_previews":len(records),
  "source_MC_mod_JARs":len(jars),"distinct_mod_blockstates_render_attempted":len(mcrenders),
  "render_state_counts":dict(statuses),"contact_sheet_count":len(list(contact.glob("*.jpg"))),
  "source_tile_properties":"v259 SQLite source_attributes raw attribute-values",
  "source_pz_bbox":"Original public Viewpoint 3D sample bbox if available; not collision size",
  "source_mc_bbox":"Sampled JSON cuboid elements bounding box; model-local, not collision shape or whole multi-part block footprint",
  "no_false_claims":["Textures used only when actual source texture path resolved",
   "Minecraft non-JSON loaders cannot be rendered accurately by simple JSON element renderer",
   "Original PZ multi-tile completed visual subject to provisional isometric assumptions",
   "PZ properties and MC game runtime interaction states not interchangeable",
   "No 1:1 visual identical match certified",
   "JAR textures/models not redistributed, derived research comparison contact cards only"],
  "mc_version":"1.20.1 Forge"}
 (OUT/"MANIFEST.json").write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+"\n",encoding="utf8")
 (OUT/"README_KO.md").write_text(
  "# 로즈우드 357종 원본 완성 가구 ↔ 실제 Minecraft 1.20.1 Forge 모델: 이미지/크기/속성\n\n"+
  "## 보고서 보는 법\n"+
  "1. ZIP을 다운로드한 뒤 INDEX.html을 브라우저에서 열면 357개 항목 검색/비교.\n"+
  "2. 카드 왼쪽은 원본 좀보이드 PNG를 복원한 *완성 가구 예시*.\n"+
  "3. 카드 오른쪽은 실제 모드 JAR의 blockstates/model JSON + PNG 원본 텍스처를 읽고 투영한 연구용 3D 그림.\n"+
  "4. 실제 원본 JSON/텍스처와 런타임 로더를 해석할 수 없는 가구는 미렌더 표시하고 **비슷해 보이는 이미지를 만들지 않음**.\n"+
  "5. PZ 크기: SpriteGridPos 합친 타일 설치 영역 및 공개 Viewpoint 3D 바운딩박스(있는 경우). MC 크기: 단일 blockstate 모델 기준 JSON 기하 경계, 게임 실제 충돌 박스 아님.\n"+
  "6. PZ 속성: v259 원본 .tiles source_attributes에서 실제 정의된 값만 표시; MC 속성: 블록 상태 JSON variants에 나온 속성 후보만. 수납, 앉기, 작동 여부는 실행 검증 없이 단정하지 않음.\n\n"+
  f"- 전체 카드: {len(records)}장, 2×2 접촉시트: {manifest['contact_sheet_count']}장.\n"+
  "\n".join("- "+k+": "+str(v)+"장" for k,v in sorted(statuses.items()))+
  "\n\n**검증 한계:** 이전의 357종 중 335종 소스 블록 후보가 있다는 것과 실제 크기/외형 매칭 확정은 전혀 다름. 정확한 대응값은 아직 0종 인증.\n",encoding="utf8")
 with zipfile.ZipFile(OUT/"ROSEWOOD_357_SIDE_BY_SIDE_SIZE_PROPERTIES.zip","w",zipfile.ZIP_DEFLATED,compresslevel=4) as z:
  for p in OUT.rglob("*"):
   if p.is_file() and p.name!="ROSEWOOD_357_SIDE_BY_SIDE_SIZE_PROPERTIES.zip":
    z.write(p,p.relative_to(OUT))
 with zipfile.ZipFile(OUT/"ROSEWOOD_357_SIDE_BY_SIDE_SIZE_PROPERTIES.zip") as z:
  assert z.testzip() is None
  assert "INDEX.html" in z.namelist()
 print("RESULT",json.dumps(manifest,ensure_ascii=False),flush=True)
if __name__=="__main__":main()
