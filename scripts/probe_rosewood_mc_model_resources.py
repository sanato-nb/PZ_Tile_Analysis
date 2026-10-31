#!/usr/bin/env python3
"""Inspect Decocraft custom model + Paladin texture paths; metadata only."""
import json,urllib.request,zipfile,io
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
p=ROOT/"analysis/rosewood_furniture/2026-10-31/minecraft_actual_mod_registry_v2/MOD_VERSION_SOURCES.json"
out=ROOT/"analysis/rosewood_furniture/2026-10-31/visual_pz_vs_mc_357_v1/MODEL_DIAGNOSTICS.json"
data=json.loads(p.read_text("utf8"))
targets={"decocraft":["double_bed_oak_white","piano_black","school_chair_gray","crt_tv"],
"paladins":["white_fridge","basic_toilet"],
"refurbished":["computer"]}
evidence=[]
def grab(url):
 req=urllib.request.Request(url,headers={"User-Agent":"RosewoodModelFileInspector/1.0"})
 return urllib.request.urlopen(req,timeout=140).read()
for label,ids in targets.items():
 ver=next(v for v in data if v["label"]==label)
 if label=="refurbished":
  url="https://mediafilez.forgecdn.net/files/7110/922/refurbished_furniture-forge-1.20.1-1.0.20.jar"
 else:
  v=json.loads(grab("https://api.modrinth.com/v2/version/"+ver["version_id"]).decode("utf8"))
  url=next(f["url"] for f in v["files"] if f["filename"]==ver["download_filename"])
 with zipfile.ZipFile(io.BytesIO(grab(url))) as z:
  files=z.namelist()
  ns={"decocraft":"decocraft","paladins":"pfm","refurbished":"refurbished_furniture"}[label]
  all_filetypes={ext:sum(name.lower().endswith(ext) for name in files) for ext in (".obj",".mtl",".png",".json",".gltf",".glb",".txt",".dcm",".zip")}
  for id in ids:
   candidates=[name for name in files if
     (name.startswith("assets/"+ns+"/models/") or name.startswith("assets/"+ns+"/textures/"))
       and (id in name)][:40]
   blockstate=("assets/"+ns+"/blockstates/"+id+".json")
   modelpath="assets/"+ns+"/models/"+id+".json"
   hints=[n for n in files if n.startswith("assets/"+ns+"/models/") and id in n]
   modeltext=""
   if modelpath in files:modeltext=z.read(modelpath).decode("utf8","replace")[:4000]
   if modeltext:
    try:
     model=json.loads(modeltext)
     parent=model.get("parent")
     if parent:
      root,relative=parent.split(":",1) if ":" in parent else (ns,parent)
      parentpath="assets/"+root+"/models/"+relative+".json"
      if parentpath in files:
       modeltext+="\nPARENT "+parentpath+"\n"+z.read(parentpath).decode("utf8","replace")[:2500]
    except Exception:pass
   evidence.append(dict(mod=label,id=id,filetype_counts=all_filetypes,
     modelpath=modelpath,modelcontent=modeltext,substrings=candidates,
     blockstate_exists=blockstate in files))
out.parent.mkdir(parents=True,exist_ok=True)
out.write_text(json.dumps(evidence,ensure_ascii=False,indent=2)+"\n",encoding="utf8")
print("MODEL_PROBE_RECORDS",len(evidence))
