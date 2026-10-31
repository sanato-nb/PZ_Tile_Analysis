#!/usr/bin/env python3
"""Research-only geometry inspection of authored Viewpoint OBJ bindings.

Reads publicly accessible OBJ vertices/faces at pinned commit. Outputs low-res
neutral-color shape diagrams (NOT original textures or model files), plus
dimensions and coverage. Shapes are provisional; mesh rotation conventions
and PZ display offsets require manual in-game confirmation.
"""
from __future__ import annotations
import csv,io,json,re,math,urllib.request,zipfile,concurrent.futures
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont

ROOT=Path(__file__).resolve().parents[1]/"analysis/rosewood_furniture/2026-10-31/complete_furniture_visual_3d_v1"
OUT=ROOT/"geometry_samples"
COMMIT="318753b6811176cc4b303f4c38d59eb5fda4d834"
BASE="https://raw.githubusercontent.com/Hirouou/project-viewpoint/"+COMMIT+"/Scripts/Interiors/mod/42/media/modelpacks/furniturefix/"
REQUESTED=[
 ("Bed","Large Oak"),("Couch","Blue Rattan"),("Shelves","Large Metal"),
 ("Chair","Grey"),("Table","Large Oak"),("Fridge","White"),("Oven","Modern"),
 ("Toilet","Fancy"),("Bath","Large Deluxe"),("Wardrobe","Oak"),
 ("Computer","Desktop"),("Television","Antique"),("Sink","White"),
 ("Counter","Steel"),("Bench","Oakwood"),("Piano","Western"),
 ("Machine","PAWS Pinball"),("Jukebox","Oldies"),("Microwave","Chrome"),
 ("Locker","Metal")]
def rows(path):
 with path.open(encoding="utf-8-sig",newline="") as f:return list(csv.DictReader(f))
def write(path,fields,data):
 with path.open("w",encoding="utf-8-sig",newline="") as f:
  w=csv.DictWriter(f,fieldnames=fields);w.writeheader();w.writerows(data)
def font(size):
 for p in ["/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"]:
  if Path(p).exists():return ImageFont.truetype(p,size)
 return ImageFont.load_default()
def get(url):
 req=urllib.request.Request(url,headers={"User-Agent":"PZResearch/0.1"})
 return urllib.request.urlopen(req,timeout=55).read().decode("utf-8-sig")
def obj_parse(s):
 verts=[];faces=[]
 for line in s.splitlines():
  if line.startswith("v "):
   a=line.split()
   if len(a)>=4:verts.append(tuple(float(v) for v in a[1:4]))
  elif line.startswith("f "):
   refs=[t.split("/")[0] for t in line.split()[1:]]
   try:
    ids=[int(i)-1 if int(i)>0 else len(verts)+int(i) for i in refs]
   except ValueError:continue
   if len(ids)>=3:
    for q in range(1,len(ids)-1):
     if all(0<=i<len(verts) for i in (ids[0],ids[q],ids[q+1])):
      faces.append((ids[0],ids[q],ids[q+1]))
 return verts,faces
def fetch(url):
 try:
  s=get(url);v,f=obj_parse(s)
  if not v or not f:raise ValueError("No geometry")
  return v,f,""
 except Exception as e:return [],[],str(e)[:140]
def render_geom(pieces,size=(460,390)):
 tris=[];coords=[]
 for part in pieces:
  vertices,faces,grid,angle,offset,scale=part
  a=angle*math.pi/180;cos=math.cos(a);sin=math.sin(a)
  transformed=[]
  for x,y,z in vertices:
   x*=scale;y*=scale;z*=scale
   transformed.append((cos*x-sin*y+grid[0]+offset[0],
      sin*x+cos*y+grid[1]+offset[1],z+offset[2]))
  coords.extend(transformed)
  for inds in faces:
   p=[transformed[j] for j in inds]
   # Project onto a 2D 3/4 iso camera; neutral color means no actual PZ texture used.
   u=[(x-y)*0.866 for x,y,z in p]
   v=[(x+y)*0.50-z*1.20 for x,y,z in p]
   a,b,c=p
   norm=((b[1]-a[1])*(c[2]-a[2])-(b[2]-a[2])*(c[1]-a[1]),
          (b[2]-a[2])*(c[0]-a[0])-(b[0]-a[0])*(c[2]-a[2]),
          (b[0]-a[0])*(c[1]-a[1])-(b[1]-a[1])*(c[0]-a[0]))
   mag=math.sqrt(sum(x*x for x in norm)) or 1.
   lighting=abs((norm[0]*(-0.30)+norm[1]*(-0.43)+norm[2]*0.85)/mag)
   val=int(110+112*lighting)
   tris.append(((sum(x+y+z*.2 for x,y,z in p)/3),list(zip(u,v)),(val,val,val)))
 if not tris:return None,None
 U=[u for _,poly,_ in tris for u,v in poly];V=[v for _,poly,_ in tris for u,v in poly]
 xmin=min(U);xmax=max(U);ymin=min(V);ymax=max(V)
 scale=min((size[0]-38)/max(.01,xmax-xmin),(size[1]-38)/max(.01,ymax-ymin),210)
 def toimage(point):
  x,y=point
  return (int((x-xmin)*scale+(size[0]-(xmax-xmin)*scale)/2),
          int((y-ymin)*scale+(size[1]-(ymax-ymin)*scale)/2))
 im=Image.new("RGB",size,(238,242,245));draw=ImageDraw.Draw(im)
 for _,poly,color in sorted(tris,key=lambda x:x[0]):
  draw.polygon([toimage(p) for p in poly],fill=color)
 if not coords:return im,None
 lo=[min(x[i] for x in coords) for i in range(3)]
 hi=[max(x[i] for x in coords) for i in range(3)]
 return im,[round(hi[i]-lo[i],5) for i in range(3)]
def main():
 if OUT.exists() and any(OUT.iterdir()):raise FileExistsError(OUT)
 OUT.mkdir(parents=True,exist_ok=True)
 cross=rows(ROOT/"ALL_357_COMPLETE_FURNITURE_3D_CROSSWALK.csv")
 bindtext=get("https://raw.githubusercontent.com/Hirouou/project-viewpoint/"+COMMIT+
  "/Scripts/Interiors/mod/42/media/modelpacks/furniturefix/pack.properties")
 maps={};models={}
 for line in bindtext.splitlines():
  if "=" not in line:continue
  k,v=line.split("=",1)
  if k.startswith("bind."):maps[k[5:]]=v.split(",")
  if k.startswith("model."):models[k[6:]]=v.strip()
 selected=[]
 for name,group in REQUESTED:
  matches=[r for r in cross if r["CustomName"]==name and r["GroupName"]==group]
  if len(matches)==1:selected.append(matches[0])
  else:print("Missing exact model request",name,group,flush=True)
 needed={}
 for r in selected:
  for key in r["representative_source_tile_ids"].split("|"):
   if not key:continue
   til,id=key.rsplit("/",1);b=maps.get(til+"_"+id)
   if b and b[0] in models:
    needed[b[0]]=BASE+models[b[0]]
 # Public source file download is only used for metadata and neutral shape review;
 # never saved/redistributed as native 3D meshes or texture files.
 geometries={}
 with concurrent.futures.ThreadPoolExecutor(max_workers=7) as pool:
  futures={pool.submit(fetch,url):asset for asset,url in needed.items()}
  for f in concurrent.futures.as_completed(futures):
   geometries[futures[f]]=f.result()
 evidence=[]
 for i,r in enumerate(selected,1):
  pieces=[];geonames=[];miss=[];sourcekeys=r["representative_source_tile_ids"].split("|")
  positions=r["representative_sprite_grid_positions"].split("|")
  for p,k in enumerate(sourcekeys):
   if not k:continue
   tileset,id=k.rsplit("/",1);b=maps.get(tileset+"_"+id)
   if not b or b[0] not in geometries:
    miss.append(k+":NO_3D_MAPPING");continue
   vert,face,error=geometries[b[0]]
   if error or not vert or not face:
    miss.append(k+":"+error);continue
   pos=(0,0)
   if p<len(positions) and re.fullmatch(r"-?\d+,-?\d+",positions[p]):
    pos=tuple(map(int,positions[p].split(",")))
   try:
    angle=float(b[1]) if len(b)>1 else 0
    offset=tuple(float(b[j]) if len(b)>j else 0 for j in (2,3,4))
    scale=float(b[5]) if len(b)>5 else 1.
   except (ValueError,IndexError):angle=0;offset=(0.,0.,0.);scale=1.
   pieces.append((vert,face,pos,angle,offset,scale))
   geonames.append(b[0])
  img,extent=render_geom(pieces)
  fname=f"{i:02d}_{re.sub(r'[^a-zA-Z0-9]+','_',r['CustomName']+'_'+r['GroupName'])}.png"
  canvas=Image.new("RGB",(960,470),(247,249,250))
  draw=ImageDraw.Draw(canvas)
  draw.text((24,9),r["CustomName"]+" / "+r["GroupName"],fill=(20,24,31),font=font(25))
  draw.text((24,42),"Left: assembled original PZ PNG   |   Right: untextured authored 3D OBJ geometry schematic",fill=(70,82,99),font=font(15))
  if img:
   canvas.paste(img,(495,68))
  else:draw.text((565,258),"PUBLIC 3D MESH NOT AVAILABLE",fill=(161,65,54),font=font(16))
  try:
   original=Image.open(ROOT/r["preview_path"]).convert("RGB")
   original.thumbnail((460,390))
   canvas.paste(original,(15,68))
  except Exception as e:pass
  draw.text((25,451),"PROVISIONAL geometry; not a Minecraft exact model match",fill=(128,42,37),font=font(13))
  canvas.save(OUT/fname,optimize=True)
  ev=dict(CustomName=r["CustomName"],GroupName=r["GroupName"],number_of_parts_expected=len(sourcekeys),
    source_parts_with_rendered_3d_meshes=len(pieces),source_parts_missing_3d_meshes=len(miss),
    source_local_ids=r["representative_source_tile_ids"],facing=r["representative_facing"],
    source_spritegrid_positions=r["representative_sprite_grid_positions"],
    source_obj_model_ids="|".join(geonames),raw_model_bbox_xyz=("|".join(map(str,extent)) if extent else ""),
    triangles=sum(len(mesh[1]) for mesh in (geometries[m] for m in geonames)),
    missing="|".join(miss),side_by_side_preview=fname,
    geometry_status="ALL_PARTS_RENDERED" if pieces and not miss else "PARTIAL_OR_MISSING",
    caution="3D source mod OBJ author geometry rendered without its original textures; model offsets may differ from engine result")
  evidence.append(ev)
 # Aggregate 4 sample pairs per contact sheet.
 names=[x["side_by_side_preview"] for x in evidence]
 for j in range(0,len(names),4):
  sheet=Image.new("RGB",(1920,940),(250,250,250))
  for idx,file in enumerate(names[j:j+4]):
   with Image.open(OUT/file) as im:
    sheet.paste(im,((idx%2)*960,(idx//2)*470))
  sheet.save(OUT/f"SAMPLE_SHEET_{j//4+1:02d}.jpg",quality=84,optimize=True)
 write(OUT/"3D_GEOMETRY_EVIDENCE.csv",list(evidence[0]),evidence)
 manifest={"count":len(evidence),"3d_meshes_fetched":len(geometries),
     "3d_meshes_fetched_ok":sum(bool(v) and bool(f) and not e for v,f,e in geometries.values()),
     "all_parts_rendered_samples":sum(x["geometry_status"]=="ALL_PARTS_RENDERED" for x in evidence),
     "3d_source_commit":COMMIT,"note":"Research-only neutral illustrative mesh rendering; original geometry and textures never stored"}
 (OUT/"MANIFEST.json").write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
 md=f"""# 3D 모델 실제 기하 비교 샘플 {len(evidence)}개

357개 완성형 PNG 원본 조합 중 대표 {len(evidence)}개를 골라 **실제 공개 Viewpoint 3D OBJ의 vertex/face 데이터를 읽고** 저해상도 무텍스처 형상도로 비교했다.

- 실제 파일(OBJ)을 읽어 복원한 부품 전부 성공: {manifest["all_parts_rendered_samples"]}/{len(evidence)}개 사례.
- 공개 3D OBJ 원본 파일이나 텍스처는 결과물에 포함하지 않음. 저작권자 Hiro.uou의 모델 라이선스를 준수.
- 회전/offset/scale은 pack.properties의 원본 bind를 읽어 사용했고, SpriteGridPos를 부품별로 배치함.
- 모델과 타일 연계는 실제 소스 키 기반이지만 렌더링 카메라/색상·모델 애니메이션은 PZ 게임 화면과 같지 않음.
- 사용자의 B42.20.3 .tiles과 해당 3D 모드의 B42.21+ 차이도 보류.
- 중요한 구분: **3D 소스가 있다는 것과 정확한 Minecraft 모드 블록이 있다는 것은 별개**.
- 확인 파일: 3D_GEOMETRY_EVIDENCE.csv, SAMPLE_SHEET_01~.jpg, 개별 PNG. 
"""
 (OUT/"README_KO.md").write_text(md,encoding="utf8")
 with zipfile.ZipFile(OUT/"3D_GEOMETRY_REVIEW_SAMPLE.zip","w",zipfile.ZIP_DEFLATED,compresslevel=6) as z:
  for file in sorted(OUT.iterdir()):
   if file.name!="3D_GEOMETRY_REVIEW_SAMPLE.zip":z.write(file,file.name)
 print(json.dumps(manifest,ensure_ascii=False),flush=True)
if __name__=="__main__":main()
