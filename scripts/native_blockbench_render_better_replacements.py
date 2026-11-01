#!/usr/bin/env python3
"""Use the ACTUAL Blockbench 5.2.2 Electron desktop renderer to inspect authored
Decocraft bbmodel resources. All native .bbmodel and texture files are ephemeral
in Actions runner; only model screenshots + provenance are committed.
"""
from pathlib import Path
import hashlib,base64,csv,io,json,os,re,subprocess,time,urllib.request,zipfile
from PIL import Image
from playwright.sync_api import sync_playwright
D=Path(__file__).resolve().parents[1]/"analysis/rosewood_furniture/2026-10-31"
O=D/"blockbench_native_replacement_candidates_v1"
TEMP=Path("/tmp/blockbench_pz_mc_source")
MOD="decocraft"
VERS=json.loads((D/"minecraft_actual_mod_registry_v2/MOD_VERSION_SOURCES.json").read_text("utf8"))
def get_tests():
 matches=D/"minecraft_real_furniture_matches_v4/ROSEWOOD_357_PZ_TO_REAL_MINECRAFT_BLOCKSTATE_MATCH.csv"
 with matches.open(encoding="utf-8-sig",newline="") as f:
  rows=list(csv.DictReader(f))
 unique={}
 for row in rows:
  if row["mc_primary_mod"]=="decocraft" and row["mc_primary_blockstate_id"]:
   key=row["mc_primary_blockstate_id"].split(":",1)[1]
   unique.setdefault(key,(key,row["pz_model_name"],row["pz_model_style"]))
 assert len(unique)==51,len(unique)
 return list(unique.values())
TESTS=[
 ("single_bed_birch_black","Bed","Fancy"),
 ("single_bed_birch_blue","Bed","Blue"),
 ("crib_oak","Bed","Oak"),
 ("pool_rack","Stand","Pool Cue"),
 ("treadmill","Hamster Wheel","Human"),
 ("bottom_cabinet_1_white","Counter","White"),
 ("bottom_cabinet_corner_outer_1_white","Counter","White Corner"),
 ("stove","Oven","Green"),
]
def fetch(url):
 req=urllib.request.Request(url,headers={"User-Agent":"RosewoodBlockbenchVerifier/1.0"})
 return urllib.request.urlopen(req,timeout=170).read()
def prepare():
 v=next(x for x in VERS if x["label"]==MOD)
 data=json.loads(fetch("https://api.modrinth.com/v2/version/"+v["version_id"]).decode("utf8"))
 release=next(x for x in data["files"] if x["filename"]==v["download_filename"])
 raw=fetch(release["url"])
 assert hashlib.sha512(raw).hexdigest()==v["sha512"]
 TEMP.mkdir(parents=True,exist_ok=True)
 objects=[]
 with zipfile.ZipFile(io.BytesIO(raw)) as z:
  for key,pzname,pzstyle in TESTS:
   source=f"assets/decocraft/models/{key}.json"
   if source not in z.namelist():
    refs=[f for f in z.namelist() if f.endswith("/"+key+".json") and "/models/" in f]
    if refs:source=refs[0]
   wrapper=json.loads(z.read(source))
   if wrapper.get("loader")!="decocraft:bbmodel":
    print("NON_BBMODEL",key,wrapper.get("loader",""),flush=True)
    objects.append(dict(id=key,pz_name=pzname,pz_style=pzstyle,
       error="NOT_DECOCRAFT_BBMODEL",source_model_path=source))
    continue
   n,path=wrapper["model"].split(":",1)
   bbpath="assets/"+n+"/"+path
   obj=json.loads(z.read(bbpath))
   material=wrapper["material"]
   mn,mp=material.split(":",1)
   texpath="assets/"+mn+"/textures/"+mp+".png"
   original=z.read(texpath)
   # Variant textures are chosen by the Decocraft loader, while the original
   # embedded BBModel textures are often for a different color variation.
   # For this native preview we explicitly switch all atlas slots to the
   # selected variant's actual source PNG, preserving UVs and group hierarchy.
   patched=0
   for tex in obj.get("textures",[]):
    if isinstance(tex,dict):
     tex["source"]="data:image/png;base64,"+base64.b64encode(original).decode("ascii")
     tex["name"]=key+".png"
     tex["relative_path"]=key+".png"
     tex.pop("path",None)
     patched+=1
   obj["name"]=key
   path=TEMP/(key+".bbmodel")
   path.write_text(json.dumps(obj,ensure_ascii=False),encoding="utf8")
   objects.append(dict(id=key,pz_name=pzname,pz_style=pzstyle,
       source_model_path=bbpath,variant_texture_path=texpath,
       patch_texture_slot_count=patched,model_elements=len(obj.get("elements",[])),
       source_sha256=hashlib.sha256(z.read(bbpath)).hexdigest(),
       variant_sha256=hashlib.sha256(original).hexdigest(),
       temp_path=str(path)))
 return objects
def run_model(obj,app,idx):
 port=9250+idx
 args=["xvfb-run","-a","-s","-screen 0 1600x1000x24",app,
       "--no-sandbox","--disable-dev-shm-usage","--use-gl=angle",
       "--use-angle=swiftshader","--enable-unsafe-swiftshader",
       "--remote-debugging-port="+str(port),
       "--remote-allow-origins=*","--user-data-dir=/tmp/bb-profile-"+str(idx),
       obj["temp_path"]]
 proc=subprocess.Popen(args,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,
          start_new_session=True,text=True)
 try:
  with sync_playwright() as p:
   browser=None
   last_error=""
   for t in range(30):
    try:
     browser=p.chromium.connect_over_cdp("http://127.0.0.1:"+str(port),timeout=3000)
     break
    except Exception as e:
     last_error=str(e)
     time.sleep(2)
   if browser is None:return dict(error="CDP_CONNECT_FAILED "+last_error[:180])
   windows=[page for ctx in browser.contexts for page in ctx.pages]
   page=None
   for t in range(30):
    for w in windows:
     try:
      result=w.evaluate("() => ({title:document.title, bb:typeof Blockbench, project:typeof Project, count:typeof Outliner!=='undefined'?Outliner.elements.length:-1})")
      if result["bb"]=="object":page=w;break
     except Exception:pass
    if page:break
    time.sleep(1)
    windows=[q for ctx in browser.contexts for q in ctx.pages]
   if page is None:return dict(error="BLOCKBENCH_PAGE_NOT_READY",urls=[w.url for w in windows])
   info={}
   for t in range(30):
    info=page.evaluate("""() => ({
       title:document.title,version:Blockbench.version,
       project:Project?.name||'',format:Project?.format?.id||'',
       cubes:Cube?.all?.length||0,
       textures:Texture?.all?.length||0,
       element_count:Outliner?.elements?.length||0,
       preview:typeof Preview!=='undefined'&&!!Preview.selected
     })""")
    if info.get("cubes",0)>4:break
    time.sleep(1)
   # Frame the WHOLE authored object in Blockbench's own camera, especially
   # models larger than one Minecraft block (beds, pianos).
   try:
    info["camera"] = page.evaluate("""() => {
     const p=Preview.selected, cubes=Cube.all;
     let lo=[Infinity,Infinity,Infinity],hi=[-Infinity,-Infinity,-Infinity];
     for(const c of cubes)for(const pt of [c.from,c.to])for(let i=0;i<3;i++){
       lo[i]=Math.min(lo[i],pt[i]);hi[i]=Math.max(hi[i],pt[i]);
     }
     const center=lo.map((v,i)=>(v+hi[i])/2);
     const span=Math.max(...lo.map((v,i)=>hi[i]-v));
     const distance=Math.max(28,span*1.65);
     const cam=p.camera;
     const oldTarget=(p.controls?.target?.clone?.()||new THREE.Vector3(0,0,0));
     const direction=cam.position.clone().sub(oldTarget).normalize();
     if(p.controls?.target?.set)p.controls.target.set(...center);
     cam.position.set(center[0]+direction.x*distance,center[1]+direction.y*distance,center[2]+direction.z*distance);
     cam.lookAt(...center);
     if(cam.isOrthographicCamera){
       cam.zoom=Math.min(cam.zoom, 13/Math.max(12,span));
       cam.updateProjectionMatrix();
     }
     if(p.controls?.update)p.controls.update();
     if(p.render)p.render();
     return {center,span,distance,camera_type:cam.type};
    }""")
    time.sleep(1)
   except Exception as e:info["camera_frame_error"]=str(e)[:240]
   # Verified image is from native Electron Blockbench app viewport, never from our Python rasterizer.
   page.screenshot(path=str(O/f"{obj['id']}_BLOCKBENCH_DESKTOP.png"),full_page=False)
   result=None
   if info.get("cubes",0)>4:
    try:
     result=page.evaluate("""async () => await new Promise((resolve,reject) => {
      try {
       Preview.selected.screenshot({width:950,height:750,crop:false}, image => {
        if(typeof image==='string')resolve({type:'dataurl',image});
        else if(image?.toDataURL)resolve({type:'canvas',image:image.toDataURL('image/png')});
        else resolve({type:typeof image,image:String(image).slice(0,100)});
       });
       setTimeout(()=>reject(new Error('capture callback missing')),15000);
      } catch(e){reject(e);}
     })""")
     if isinstance(result,dict) and result.get("image","").startswith("data:image/png;base64,"):
      (O/f"{obj['id']}_BLOCKBENCH_VIEWPORT.png").write_bytes(base64.b64decode(result["image"].split(",",1)[1]))
    except Exception as e:info["screenshot_api_error"]=str(e)[:220]
   browser.close()
   return dict(**info,viewport_screenshot_type=(result or {}).get("type",""),
       native_desktop_screenshot=f"{obj['id']}_BLOCKBENCH_DESKTOP.png",
       native_model_screenshot=f"{obj['id']}_BLOCKBENCH_VIEWPORT.png" if (O/f"{obj['id']}_BLOCKBENCH_VIEWPORT.png").exists() else "",
       loaded_verified=info.get("cubes",0)>4)
 finally:
  import signal
  try:os.killpg(proc.pid,signal.SIGTERM)
  except ProcessLookupError:pass
  try:proc.communicate(timeout=4)
  except Exception:
   try:os.killpg(proc.pid,signal.SIGKILL)
   except ProcessLookupError:pass
def main():
 O.mkdir(parents=True,exist_ok=False)
 objs=prepare()
 app="/tmp/blockbench-app/squashfs-root/AppRun"
 assert Path(app).exists(),app
 report=[]
 for i,obj in enumerate(objs):
  print("BLOCKBENCH_NATIVE_OPEN",obj["id"],flush=True)
  try:
   proof=run_model(obj,app,i) if obj.get("temp_path") else dict(error=obj.get("error","NO_TEMP_MODEL"))
  except Exception as e:
   proof=dict(error="NATIVE_EXECUTION_ERROR "+repr(e)[:250])
  row={**obj,**proof}
  row.pop("temp_path",None)
  report.append(row)
  print("BLOCKBENCH_NATIVE_RESULT",json.dumps({k:v for k,v in row.items() if k in ["id","version","project","format","cubes","textures","error","native_model_screenshot","loaded_verified"]},ensure_ascii=False),flush=True)
 (O/"NATIVE_BLOCKBENCH_PROOF.json").write_text(json.dumps(report,ensure_ascii=False,indent=2)+"\n",encoding="utf8")
 assert any(x.get("loaded_verified") for x in report), "No verified native Blockbench model open; refuse claiming success"
 print("SUCCESS_NATIVE_BLOCKBENCH",sum(bool(x.get("loaded_verified")) for x in report),flush=True)
if __name__=="__main__":main()
