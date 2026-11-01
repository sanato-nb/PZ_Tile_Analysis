#!/usr/bin/env python3
"""Read REAL Minecraft 1.20.1 Forge JAR blockstate JSON + inherited block models
and original PNG textures, convert their cuboids into a TEMPORARY Blockbench free
project for native Blockbench 5.2 screenshot rendering.

No JAR, model JSON, or source textures are redistributed. The output is only
Blockbench's own 3D viewport screenshot and source evidence manifest.
"""
import csv,io,os,json,hashlib,base64,urllib.request,zipfile,uuid,re,subprocess,time,signal
from collections import OrderedDict,Counter,defaultdict
from pathlib import Path
from playwright.sync_api import sync_playwright
from PIL import Image
D=Path(__file__).resolve().parents[1]/"analysis/rosewood_furniture/2026-10-31"
TEMP=Path("/tmp/rosewood_real_blockbench_models")
VERSION=json.loads((D/"minecraft_actual_mod_registry_v2/MOD_VERSION_SOURCES.json").read_text("utf8"))
REF=D/"pz_mc_furniture_357_rematch_v3/REVISED_357_PZ_MC_MATCHES.csv"
OUT=D/"native_real_mod_models_remaining_v1"
APP="/tmp/blockbench-app/squashfs-root/AppRun"
def csvrows(path):
 with path.open(encoding="utf-8-sig",newline="") as f:return list(csv.DictReader(f))
def fetch(url):
 req=urllib.request.Request(url,headers={"User-Agent":"PZRealFurnitureModelValidator/1.0"})
 return urllib.request.urlopen(req,timeout=180).read()
def sourcezip(mod):
 v=next(x for x in VERSION if x["label"]==mod)
 if mod=="refurbished":url="https://mediafilez.forgecdn.net/files/7110/922/refurbished_furniture-forge-1.20.1-1.0.20.jar"
 else:
  j=json.loads(fetch("https://api.modrinth.com/v2/version/"+v["version_id"]).decode("utf8"))
  url=next(x["url"] for x in j["files"] if x["filename"]==v["download_filename"])
 data=fetch(url)
 assert hashlib.sha512(data).hexdigest()==v["sha512"],"JAR mismatch "+mod
 return zipfile.ZipFile(io.BytesIO(data))
def readjson(z,path):
 try:return json.loads(z.read(path).decode("utf8"))
 except Exception:return None
def references(z,ns,id):
 state=readjson(z,f"assets/{ns}/blockstates/{id}.json")
 if not state:return [],["MISSING_BLOCKSTATE"]
 refs=[];tags=[]
 if isinstance(state.get("variants"),dict):
  keys=list(state["variants"])
  # prefer plain closed north solid body, not head/wall/upper state
  keys.sort(key=lambda x:(
   int("facing=north" not in x and "facing=east" not in x),
   int("part=head" in x or "half=upper" in x or "type=right" in x),
   int("open=true" in x or "powered=true" in x or "waterlogged=true" in x),
   len(x)))
  k=keys[0];value=state["variants"][k]
  refs=value if isinstance(value,list) else [value]
  tags.append("state_selection:"+k)
 elif isinstance(state.get("multipart"),list):
  for x in state["multipart"]:
   when=x.get("when")
   # include unconditional and base north/closed/water state; exclude open/upper
   if isinstance(when,dict):
    if any(k in ("open","powered","waterlogged") and v in ("true",True) for k,v in when.items()):continue
    if "facing" in when and when["facing"] not in ("north","east"):continue
    if any(k in ("half","part","type") and v in ("upper","head","right") for k,v in when.items()):continue
   apply=x.get("apply",[])
   refs.extend(apply if isinstance(apply,list) else [apply])
  tags.append("multipart_heuristic")
 refs=[x for x in refs if isinstance(x,dict) and x.get("model")]
 return refs[:40],tags
def resolve(z,namespace,model,seen=None,vanilla=None):
 ns,path=model.split(":",1) if ":" in model else (namespace,model)
 full=f"assets/{ns}/models/{path}.json"
 seen=set() if seen is None else set(seen)
 if full in seen:return None,{},[],["model_cycle"]
 seen.add(full)
 obj=readjson(z,full)
 if obj is None and vanilla is not None:obj=readjson(vanilla,full)
 if obj is None:return None,{},[],["missing:"+full]
 textures={};elems=None;roots=[]
 if obj.get("parent"):
  _,base,elems,roots=resolve(z,ns,obj["parent"],seen,vanilla)
  textures.update(base)
 textures.update(obj.get("textures",{}))
 if isinstance(obj.get("elements"),list):elems=obj["elements"]
 roots.append(full)
 return obj,textures,elems,roots
def unalias(key,tex):
 val=key
 for _ in range(12):
  if not isinstance(val,str):return None
  if not val.startswith("#"):return val
  val=tex.get(val[1:])
 return None
def source_texture(z,ns,key,texmap,vanilla,cache):
 val=unalias(key,texmap)
 if not val:return None,None
 tns,rel=val.split(":",1) if ":" in val else (ns,val)
 if rel.startswith("textures/"):rel=rel[9:]
 full=f"assets/{tns}/textures/{rel}.png"
 zips=[z,vanilla] if vanilla else [z]
 if full in cache:return cache[full],full
 for file in zips:
  if file is not None and full in file.namelist():
   raw=file.read(full)
   cache[full]=raw;return raw,full
 cache[full]=None
 return None,None
def vanilla_client_zip():
 # Mojang source hashes from version manifest; used only for source vanilla block texture.
 manifest=json.loads(fetch("https://piston-meta.mojang.com/mc/game/version_manifest_v2.json"))
 url=next(v["url"] for v in manifest["versions"] if v["id"]=="1.20.1")
 version=json.loads(fetch(url))
 release=version["downloads"]["client"]
 raw=fetch(release["url"])
 assert hashlib.sha1(raw).hexdigest()==release["sha1"],"Mojang client jar mismatch"
 return zipfile.ZipFile(io.BytesIO(raw))
def convert(z,mod,blockid,vanilla):
 ns,name=blockid.split(":",1)
 refs,tags=references(z,ns,name)
 elements=[];texture_map=OrderedDict();source_files=[];missing=[]
 cache={}
 for i,ref in enumerate(refs):
  model,aliases,cubes,source=resolve(z,ns,ref["model"],vanilla=vanilla)
  source_files.extend(source)
  if not cubes:
   missing.append("no_vanilla_cuboids:"+ref["model"])
   continue
  for j,e in enumerate(cubes):
   if not isinstance(e,dict) or "from" not in e or "to" not in e:continue
   faces={}
   for side,face in e.get("faces",{}).items():
    if side not in ("north","south","east","west","up","down"):continue
    raw,path=source_texture(z,ns,face.get("texture",""),aliases,vanilla,cache)
    if raw is None:
     missing.append("missing_texture:"+str(face.get("texture"))+":"+ref["model"]);continue
    if path not in texture_map:texture_map[path]=raw
    p=e["from"];q=e["to"];x,y,zz=p;X,Y,Z=q
    if side in ("north","south"):default=[x,16-Y,X,16-y]
    elif side in ("east","west"):default=[zz,16-Y,Z,16-y]
    else:default=[x,zz,X,Z]
    faces[side]={"uv":face.get("uv",default),"texture":list(texture_map).index(path),
       "rotation":int(face.get("rotation",0))}
   if not faces:continue
   angle=float(e.get("rotation",{}).get("angle",0))
   rot_axis=e.get("rotation",{}).get("axis","y")
   angles=[0,0,0]
   if rot_axis in ("x","y","z"):angles[("x","y","z").index(rot_axis)]=angle
   # Free model BB format coordinates are Minecraft block cuboids in units of pixels.
   uid=str(uuid.uuid5(uuid.NAMESPACE_URL,blockid+str(i)+"-"+str(j)))
   cube=dict(name=f"source_{i}_{j}",type="cube",uuid=uid,box_uv=False,
    from_=list(e["from"]),to=list(e["to"]),origin=e.get("rotation",{}).get("origin",[8,8,8]),
    rotation=angles,faces=faces)
   cube["from"]=cube.pop("from_")
   if all(abs(x)<0.01 for x in angles):cube.pop("rotation")
   elements.append(cube)
 if not elements:return None,dict(mod=mod,blockstate_id=blockid,reason="NO_RENDERABLE_CUBOIDS",source_models=source_files,missing=missing[:12],refs=refs[:3])
 textures=[]
 for i,(path,raw) in enumerate(texture_map.items()):
  with Image.open(io.BytesIO(raw)) as im:
   w,h=im.size
  textures.append(dict(name=f"tex_{i}.png",id=str(i),uuid=str(uuid.uuid5(uuid.NAMESPACE_URL,path)),
   source="data:image/png;base64,"+base64.b64encode(raw).decode("ascii"),
   width=w,height=h,uv_width=16,uv_height=16,relative_path=f"tex_{i}.png",
   internal=True,visible=True))
 model=dict(meta={"format_version":"5.0","model_format":"free","box_uv":False},
  name=name,resolution={"width":16,"height":16},
  elements=elements,outliner=[x["uuid"] for x in elements],textures=textures)
 return model,dict(mod=mod,blockstate_id=blockid,cuboids=len(elements),
  textures=len(textures),source_models=source_files[:25],
  source_texture_paths=list(texture_map)[:60],missing=missing[:30],
  state_refs=refs[:10],selection_tags=tags,
  source_model_sha256=hashlib.sha256(json.dumps(model,sort_keys=True).encode("utf8")).hexdigest())
def open_native(project,idx):
 port=9430+idx
 args=["xvfb-run","-a","-s","-screen 0 1600x1000x24",APP,
  "--no-sandbox","--disable-dev-shm-usage","--use-gl=angle",
  "--use-angle=swiftshader","--enable-unsafe-swiftshader",
  "--remote-debugging-port="+str(port),"--remote-allow-origins=*",
  "--user-data-dir=/tmp/rosewood-bb-furniture-"+str(idx),str(project)]
 proc=subprocess.Popen(args,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL,
   start_new_session=True)
 try:
  with sync_playwright() as p:
   b=None
   for attempt in range(24):
    try:b=p.chromium.connect_over_cdp(f"http://127.0.0.1:{port}",timeout=4000);break
    except Exception:time.sleep(1)
   if not b:return {"error":"CDP_NOT_OPEN"}
   page=None
   for attempt in range(24):
    for ctx in b.contexts:
     for candidate in ctx.pages:
      try:
       test=candidate.evaluate("() => ({bb:typeof Blockbench, cubes:typeof Cube==='undefined'?0:Cube.all.length})")
       if test["bb"]=="object":page=candidate;break
      except Exception:continue
     if page:break
    if page:break
    time.sleep(1)
   if not page:
    b.close();return {"error":"NO_BLOCKBENCH_PAGE"}
   info={}
   for attempt in range(20):
    info=page.evaluate("""() => ({version:Blockbench.version,
       project:Project?.name||'', format:Project?.format?.id||'',
       cubes:Cube?.all?.length||0,textures:Texture?.all?.length||0,
       preview:!!Preview.selected})""")
    if info.get("cubes",0)>0:break
    time.sleep(.7)
   if info.get("cubes",0)==0:
    b.close();return {**info,"error":"NO_LOADED_CUBES"}
   # Reframe viewport using camera center rather than page screenshot of UI.
   page.evaluate("""() => {
     const p=Preview.selected,cubes=Cube.all,lo=[Infinity,Infinity,Infinity],hi=[-Infinity,-Infinity,-Infinity];
     for(const c of cubes)for(const point of [c.from,c.to])for(let i=0;i<3;i++){
      lo[i]=Math.min(lo[i],point[i]);hi[i]=Math.max(hi[i],point[i]);
     }
     const center=lo.map((v,i)=>(v+hi[i])/2);
     const span=Math.max(...lo.map((v,i)=>hi[i]-v));
     const cam=p.camera,tar=(p.controls?.target?.clone?.()||new THREE.Vector3());
     const direction=cam.position.clone().sub(tar).normalize();
     const dist=Math.max(28,span*1.7);
     if(p.controls?.target)p.controls.target.set(...center);
     cam.position.set(center[0]+direction.x*dist,center[1]+direction.y*dist,center[2]+direction.z*dist);
     cam.lookAt(...center);
     if(cam.isOrthographicCamera){cam.zoom=Math.min(cam.zoom,13/Math.max(12,span));cam.updateProjectionMatrix();}
     p.controls?.update?.();p.render?.();
   }""")
   time.sleep(.4)
   result=page.evaluate("""async () => await new Promise((resolve,reject) => {
    try{Preview.selected.screenshot({width:850,height:680,crop:false},v=>{
      if(typeof v==='string')resolve(v);else if(v?.toDataURL)resolve(v.toDataURL('image/png'));
      else reject(new Error('bad screen type'));});
      setTimeout(()=>reject(Error('timeout')),10000);
    }catch(e){reject(e);}
   })""")
   b.close()
   if not isinstance(result,str) or not result.startswith("data:image/png;base64,"):
    return {**info,"error":"NOT_PNG"}
   img=base64.b64decode(result.split(",",1)[1])
   return {**info,"png_bytes":img}
 finally:
  try:os.killpg(proc.pid,signal.SIGTERM)
  except Exception:pass
  try:proc.wait(timeout=3)
  except Exception:
   try:os.killpg(proc.pid,signal.SIGKILL)
   except Exception:pass
def main():
 import sys
 mode=sys.argv[1] if len(sys.argv)>1 else "PROBE"
 LIMIT=int(os.getenv("PROBE_LIMIT","4"))
 TEMP.mkdir(parents=True,exist_ok=True)
 assert Path(APP).exists()
 refs=csvrows(REF)
 targets=OrderedDict()
 for r in refs:
  key=r["reviewed_replacement_mc_id"] or r["mc_id"]
  mod=r["mod"]
  if r["reviewed_replacement_mc_id"]:mod="decocraft"
  if not key or mod=="decocraft":continue
  targets.setdefault(key,mod)
 if mode=="PROBE":
  preferred=["pfm:basic_toilet","mcwfurnitures:blue_couch","refurbished_furniture:computer","handcrafted:acacia_shelf"]
  targets=OrderedDict((k,targets[k]) for k in preferred if k in targets)
  assert targets,targets
  targets=OrderedDict(list(targets.items())[:LIMIT])
 elif mode in ("paladins","macaws","refurbished","handcrafted"):
  targets=OrderedDict((k,m) for k,m in targets.items() if m==mode)
 else:raise RuntimeError("use PROBE or mod label")
 assert len(targets)>0
 OUT.mkdir(parents=True,exist_ok=True)
 meta=[];failed=[];success=0
 zips={}
 vanilla=vanilla_client_zip()
 for idx,(key,mod) in enumerate(targets.items()):
  ns,name=key.split(":",1)
  print("RENDER",mode,idx+1,"/",len(targets),key,flush=True)
  try:
   if mod not in zips:zips[mod]=sourcezip(mod)
   model,evidence=convert(zips[mod],mod,key,vanilla)
   if model is None:
    print("NO_GEOMETRY",key,evidence.get("reason"),evidence.get("missing",[])[:3],flush=True)
    meta.append(evidence);failed.append(key);continue
   obj=TEMP/(mod+"_"+name+".bbmodel")
   obj.write_text(json.dumps(model,ensure_ascii=False),encoding="utf8")
   rv=open_native(obj,idx)
   pic=rv.pop("png_bytes",None)
   if pic:
    filename=mod+"__"+name+".png"
    (OUT/filename).write_bytes(pic);rv["image"]=filename
    success+=1
   else:
    print("NATIVE_ERROR",key,rv.get("error"),flush=True)
    failed.append(key)
   meta.append({**evidence,**rv})
   try:obj.unlink()
   except Exception:pass
  except Exception as e:
   print("RENDER_FAILURE",key,repr(e)[:400],flush=True)
   meta.append({"mod":mod,"blockstate_id":key,"error":repr(e)[:350]});failed.append(key)
  if (idx+1)%5==0:print("SUMMARY",success,idx+1,flush=True)
 (OUT/("PROOF_"+mode+".json")).write_text(json.dumps(meta,ensure_ascii=False,indent=2)+"\n",encoding="utf8")
 print("FINAL_RENDER",mode,"success",success,"total",len(targets),"failed",failed,flush=True)
 if mode=="PROBE":assert success>=2,(success,failed)
 else:assert success>=max(1,int(.7*len(targets))),(success,len(targets))
if __name__=="__main__":main()
