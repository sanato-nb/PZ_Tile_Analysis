#!/usr/bin/env python3
"""Inspect actual Minecraft 1.20.1 Forge furniture mods WITHOUT distributing jars/assets.

Queries Modrinth official API at a fixed date-compatible MC version; downloads only
to ephemeral CI; indexes actual namespaces, JSON blockstate/model files, custom
language keys, and candidate prop definitions as evidence of in-jar furniture IDs.
"""
from __future__ import annotations
from pathlib import Path
import csv,hashlib,io,json,re,time,urllib.parse,urllib.request,zipfile
from collections import Counter,defaultdict

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"analysis/rosewood_furniture/2026-10-31/minecraft_actual_mod_registry_v1"
MODS=[
 ("paladins","paladins-furniture"),
 ("macaws","macaws-furniture"),
 ("refurbished","refurbished-furniture"),
 ("decocraft","decocraft"),
 ("handcrafted","handcrafted"),
 ("immersive","immersive-furniture"),
 ("arcade","arcade-mod-reloaded")
]
TARGET="1.20.1"
USER_AGENT="Rosewood-Private-Research-Inventory/1.0 (read-only mod resource audit)"
def fetch(url,timeout=120):
    req=urllib.request.Request(url,headers={"User-Agent":USER_AGENT,"Accept":"application/json,application/octet-stream"})
    with urllib.request.urlopen(req,timeout=timeout) as r:return r.read()
def get_json(url):return json.loads(fetch(url,45).decode("utf8"))
def clean(s):
    return re.sub(r"[^a-z0-9]+","_",s.casefold()).strip("_")
def write(name,columns,rows):
    with (OUT/name).open("w",encoding="utf-8-sig",newline="") as f:
        w=csv.DictWriter(f,columns,extrasaction="ignore");w.writeheader();w.writerows(rows)
def main():
    if OUT.exists() and any(OUT.iterdir()):raise FileExistsError("No overwrite "+str(OUT))
    OUT.mkdir(parents=True,exist_ok=True)
    all_entries=[];vdata=[];models=[];errors=[]
    for label,slug in MODS:
      rec={"label":label,"modrinth_project_slug":slug,"minecraft":TARGET,"loader":"forge"}
      try:
        params=urllib.parse.urlencode({"loaders":json.dumps(["forge"]),
                 "game_versions":json.dumps([TARGET]),"include_changelog":"false"})
        versions=get_json(f"https://api.modrinth.com/v2/project/{slug}/version?{params}")
        versions=[v for v in versions if "forge" in v.get("loaders",[]) and TARGET in v.get("game_versions",[]) 
          and v.get("version_type")=="release" and v.get("date_published","")<"2026-11-02"]
        if not versions:raise RuntimeError("No matching release versions")
        versions.sort(key=lambda v:(v["date_published"],v["id"]),reverse=True)
        selected=versions[0]
        modfiles=[f for f in selected["files"] if f["filename"].endswith(".jar")]
        if not modfiles:raise RuntimeError("No .jar in Modrinth version")
        best=sorted(modfiles,key=lambda f:(not f.get("primary",False),"-sources" in f["filename"],"-dev" in f["filename"]))[0]
        jar_bytes=fetch(best["url"],180)
        sha=hashlib.sha512(jar_bytes).hexdigest()
        if sha!=best.get("hashes",{}).get("sha512",sha):raise RuntimeError("File hash mismatch")
        if len(jar_bytes)>260_000_000:raise RuntimeError("unexpected jar size")
        with zipfile.ZipFile(io.BytesIO(jar_bytes)) as archive:
          if archive.testzip():raise RuntimeError("zip CRC failure")
          names=archive.namelist()
          namespace=Counter()
          for p in names:
              if p.startswith("assets/"):
                  namespace[p.split("/")[1]]+=1
          # All blockstates and native names; bonus decode mod-specific
          # props entity lists where no JSON blockstate is shipped.
          translations={}
          langnames=[p for p in names if re.fullmatch(r"assets/[^/]+/lang/en_us\.json",p)]
          for lng in langnames:
            try:translations.update(json.loads(archive.read(lng).decode("utf8-sig")))
            except Exception:continue
          langindex=defaultdict(list)
          for k,v in translations.items():
            if isinstance(v,str):
                x=k.split(".");langindex[".".join(x[1:]) if len(x)>1 else k].append(v)
          valid={}
          for p in names:
            m=re.fullmatch(r"assets/([^/]+)/blockstates/(.+)\.json",p)
            if m:
               namespace_id,objid=m.groups()
               try:
                   obj=json.loads(archive.read(p).decode("utf8"))
                   refmodels=set()
                   def walk(x):
                       if isinstance(x,dict):
                           for kk,vv in x.items():
                               if kk=="model" and isinstance(vv,str):refmodels.add(vv)
                               else:walk(vv)
                       elif isinstance(x,list):
                           for v in x:walk(v)
                   walk(obj)
                   variants=obj.get("variants",{}) if isinstance(obj,dict) else {}
                   multi=obj.get("multipart",[]) if isinstance(obj,dict) else []
                   status="BLOCKSTATE_JSON"
                   namestring="|".join(sorted({val for kk,val in translations.items()
                       if kk.startswith(("block."+namespace_id+".","item."+namespace_id+"."))
                       and kk.split(".")[-1]==objid and isinstance(val,str)}))
                   valid[namespace_id+":"+objid]=dict(source_mod=label,namespace=namespace_id,
                       path_id=objid,registry_id=namespace_id+":"+objid,
                       display_name=namestring.replace("|"," / "),
                       evidence_path=p,evidence_type=status,variant_count=len(variants),
                       multipart_case_count=len(multi),
                       referenced_models="|".join(sorted(refmodels)[:14]),
                       model_name_count=len(refmodels),jar_version_id=selected["id"])
               except Exception as e:errors.append([label,"parse_blockstate",p,str(e)[:110]])
          # Dynamic models - Decocraft item definitions and special entities may
          # lack blockstate JSON; do not assert they are registered blocks.
          for k,v in translations.items():
            mm=re.fullmatch(r"(?:block|item)\.([^.]+)\.([^.]+)",k)
            if mm and isinstance(v,str):
                ns,n=mm.groups();id=ns+":"+n
                if id not in valid:
                    valid[id]=dict(source_mod=label,namespace=ns,path_id=n,registry_id=id,
                        display_name=v,evidence_path="assets/"+ns+"/lang/en_us.json",
                        evidence_type="LANG_ONLY_NOT_REGISTERED",variant_count=0,multipart_case_count=0,
                        referenced_models="",model_name_count=0,jar_version_id=selected["id"])
          # Basic mod file inventory to assess dynamic model assets not found through blockstates.
          asset_counts=Counter()
          for path in names:
              m=re.fullmatch(r"(assets/[^/]+/)([^/]+)/.*",path)
              if m:asset_counts[m.group(2)]+=1
          rec.update(status="DOWNLOADED_JAR_INSPECTED",version=selected["version_number"],
            version_id=selected["id"],date_published=selected["date_published"],
            download_filename=best["filename"],download_bytes=len(jar_bytes),
            sha512=sha,blockstate_json_count=sum(x["evidence_type"]=="BLOCKSTATE_JSON" for x in valid.values()),
            language_only_possible_ids=sum(x["evidence_type"]=="LANG_ONLY_NOT_REGISTERED" for x in valid.values()),
            lang_entry_total=len(translations),zip_entry_total=len(names),
            assets_json_models_count=sum(p.endswith(".json") and "/models/" in p for p in names),
            assets_source_counts=dict(asset_counts),top_asset_namespaces=dict(namespace.most_common(12)))
          all_entries+=list(valid.values())
          print(label,selected["version_number"],rec["blockstate_json_count"],"blockstate IDs",
                  rec["language_only_possible_ids"],"lang names",flush=True)
        del jar_bytes
      except Exception as e:
        rec.update(status="ERROR_OR_UNAVAILABLE",error=str(e)[:250])
        errors.append([label,"download_or_modrinth",slug,str(e)[:250]])
        print("WARN",label,str(e)[:160],flush=True)
      vdata.append(rec)
    cols=["source_mod","namespace","path_id","registry_id","display_name","evidence_path","evidence_type",
      "variant_count","multipart_case_count","referenced_models","model_name_count","jar_version_id"]
    write("REAL_MOD_ASSET_CANDIDATES.csv",cols,all_entries)
    write("ERRORS.csv",["mod","stage","path","error"],
       [{"mod":e[0],"stage":e[1],"path":e[2],"error":e[3]} for e in errors])
    (OUT/"MOD_VERSION_SOURCES.json").write_text(json.dumps(vdata,ensure_ascii=False,indent=2)+"\n",encoding="utf8")
    stats={"version":"MC_Forge1201_SourceAssetAudit_v1",
      "mods_requested":len(MODS),"mods_jar_inspected":sum(r["status"]=="DOWNLOADED_JAR_INSPECTED" for r in vdata),
      "blockstate_json_entries":sum(a["evidence_type"]=="BLOCKSTATE_JSON" for a in all_entries),
      "language_only_not_registered_entries":sum(a["evidence_type"]=="LANG_ONLY_NOT_REGISTERED" for a in all_entries),
      "errors_count":len(errors),"minecraft":"1.20.1","forge_compatibility":"release metadata only, not loaded in-game",
      "source_caution":"Actual downloaded Modrinth JAR inspected without redistribution. A blockstate JSON is an asset path, not necessarily live registered ID; verify runtime before world placement.",
      "custom_assets_note":"Decocraft and Immersive Furniture may use runtime custom model IDs; lack of blockstates does NOT mean no furniture."}
    (OUT/"MANIFEST.json").write_text(json.dumps(stats,ensure_ascii=False,indent=2)+"\n",encoding="utf8")
    (OUT/"README_KO.md").write_text(
     "# 실제 Minecraft 1.20.1 Forge 가구 모드 JAR 자산 검수\n\n"+
     "2026-11-01 기준 release 중 1.20.1+Forge 호환 메타데이터가 있는 최신 파일을 Modrinth API에서 다운로드해 **일시적으로 압축 내부 파일**을 열어 검사.\n\n"+
     f"- 요청: {len(MODS)}개, 검사 성공: {stats['mods_jar_inspected']}개\n"+
     f"- 블록 상태 JSON 이름: {stats['blockstate_json_entries']}개, 이름만 있는 후보: {stats['language_only_not_registered_entries']}개\n"+
     "- REAL_MOD_ASSET_CANDIDATES.csv: 실제 Jar의 blockstates/ 자산 경로 또는 en_us.json 이름이 있는 ID.\n"+
     "- MOD_VERSION_SOURCES.json: 검사한 정확한 모드 버전과 jar SHA512.\n"+
     "- 블록 상태 파일이 실제 게임 레지스트리에 등록되어 있다는 것을 보증하지 않으므로 추후 runtime 확인 필요.\n"+
     "- Decocraft는 모델/장식이 동적 인덱스로 들어갈 수 있으므로 위 목록에 없다고 미지원 단정 불가.\n"+
     "- 모드 JAR/텍스처/모델 JSON 전체를 사용자의 GitHub에 복제하지 않았으며 목록만 생성.\n",encoding="utf8")
    print(json.dumps(stats,ensure_ascii=False),flush=True)

if __name__=="__main__":main()
