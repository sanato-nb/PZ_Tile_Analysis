#!/usr/bin/env python3
"""Complete, source-grounded 357 Rosewood PZ furniture to Minecraft mod images.
337? Never invent evidence: source file native render, prior approximate fallback,
or a fully filled visual 'NO TRUSTWORTHY MOD MATCH' status instead of blanks.

The report is for actual mod matching decisions: rejects from prior manual audit
are not silently reapproved merely because a rendering was produced.
"""
import csv,collections,json,math,html,re,zipfile,io
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont,ImageOps
import numpy as np

D=Path(__file__).resolve().parents[1]/"analysis/rosewood_furniture/2026-10-31"
SOURCE=D/"pz_mc_furniture_357_rematch_v3"
NATIVE=D/"blockbench_native_357_rematch_v1"
NEW=D/"blockbench_native_replacement_candidates_v1"
OTHERS=D/"native_real_mod_models_remaining_v1"
PZ=D/"complete_furniture_visual_3d_v1"
OUT=D/"all_357_complete_native_comparisons_v1"
SIZ=(1350,590)
def csvread(p):
 with p.open(encoding="utf-8-sig",newline="") as f:return list(csv.DictReader(f))
def csvwrite(p,rows):
 if not rows:return
 with p.open("w",encoding="utf-8-sig",newline="") as f:
  w=csv.DictWriter(f,list(rows[0]),extrasaction="ignore");w.writeheader();w.writerows(rows)
def font(size):
 paths=["/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc",
        "/usr/share/fonts/truetype/nanum/NanumGothic.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"]
 for p in paths:
  if Path(p).exists():return ImageFont.truetype(p,size)
 return ImageFont.load_default()
def cut_pz(p):
 # Original renderer preview consists of title+panel+small finished sprite.
 # Crop to actual sprite area, rejecting nearly-uniform panel background.
 rgb=np.array(p.convert("RGB"))
 w,h=p.size
 im=rgb[112:min(h-48,413),28:min(w-26,525),:]
 hh,ww=im.shape[:2]
 if ww<10 or hh<10:return p.convert("RGBA")
 # Infer panel RGB from border, avoid assuming specific PZ palette.
 bg=np.median(np.concatenate((im[:7,:].reshape(-1,3),im[-7:,:].reshape(-1,3),
                               im[:,:7].reshape(-1,3),im[:,-7:].reshape(-1,3)),axis=0).astype(np.int16),axis=0)
 residual=np.max(np.abs(im.astype(np.int16)-bg),axis=2)
 mask=residual>24
 mask[:6,:]=False;mask[-6:,:]=False;mask[:,:6]=False;mask[:,-6:]=False
 iy,ix=np.where(mask)
 if len(ix)<22:return p.convert("RGBA")
 left=max(0,int(np.quantile(ix,.005))-12);top=max(0,int(np.quantile(iy,.005))-12)
 right=min(ww,int(np.quantile(ix,.995))+13);bottom=min(hh,int(np.quantile(iy,.995))+13)
 out=Image.fromarray(im).convert("RGBA")
 # Keep original pixels and panel for traceability; avoid fake geometry.
 return out.crop((left,top,right,bottom))
def cut_mc(im):
 orig=np.array(im.convert("RGBA"))
 # Native Blockbench source screenshot returns transparent black background.
 bright=(orig[:,:,:3].max(axis=2)>9)&(orig[:,:,3]>3)
 ys,xs=np.where(bright)
 if len(xs)>30:
  pad=14;bound=(max(0,int(xs.min())-pad),max(0,int(ys.min())-pad),
         min(im.width,int(xs.max())+pad+1),min(im.height,int(ys.max())+pad+1))
  im=im.crop(bound)
  a=np.array(im.convert("RGBA"))
  n=(a[:,:,:3].max(axis=2)>9)
  a[:,:,3]=np.minimum(a[:,:,3],np.where(n,255,0)).astype("uint8")
  return Image.fromarray(a,"RGBA")
 return im.convert("RGBA")
def get_visual(record,proof):
 model=record["reviewed_replacement_mc_id"] or record["mc_id"]
 if not model:return None,"NO_REAL_MOD_ASSET","No candidate model matched from the inspected JARs",{}
 ns,name=model.split(":",1)
 if ns=="decocraft":
  if record["reviewed_replacement_mc_id"]:
   p=NEW/(name+"_BLOCKBENCH_VIEWPORT.png")
   if p.exists():
    return p,"ACTUAL_NATIVE_BLOCKBENCH_SOURCE_BBMODEL","Original source Decocraft bbmodel variant (new candidate)",{}
  p=NATIVE/(name+"_BLOCKBENCH_VIEWPORT.png")
  if p.exists():
   return p,"ACTUAL_NATIVE_BLOCKBENCH_SOURCE_BBMODEL","Original source Decocraft bbmodel from verified JAR",{}
  return None,"NATIVE_BLOCKBENCH_MODEL_UNAVAILABLE","Original Decocraft native model could not be rendered",{}
 mods={"pfm":"paladins","mcwfurnitures":"macaws","refurbished_furniture":"refurbished","handcrafted":"handcrafted"}
 mod=mods.get(ns)
 if mod is None:return None,"NO_CONFIGURED_JAR_RENDERER","Mod namespace not found in inspected source registry",{}
 info=proof.get(model)
 if info and info.get("image"):
  p=OTHERS/info["image"]
  if p.exists():
   n=int(info.get("cuboids",0));loaded=int(info.get("cubes",0))
   quality="ACTUAL_NATIVE_BLOCKBENCH_FULL_SOURCE_JSON" if (loaded>=n or not n) else "NATIVE_BLOCKBENCH_PARTIAL_SOURCE_JSON"
   return p,quality,"Actual source mod blockstate JSON and texture PNG imported to native Blockbench",info
 return None,"REAL_MODEL_IMPORT_FAILED","Source model/JAR exists but a trustworthy 3D screenshot could not be produced",info or {}
def get_pz_source(r):
 return PZ/r["pz_preview"]
def provenance_short(grade):
 return {
 "ACTUAL_NATIVE_BLOCKBENCH_SOURCE_BBMODEL":"원본 .bbmodel의 Blockbench 렌더",
 "ACTUAL_NATIVE_BLOCKBENCH_FULL_SOURCE_JSON":"원본 모델 JSON·텍스처의 Blockbench 렌더",
 "NATIVE_BLOCKBENCH_PARTIAL_SOURCE_JSON":"일부 부품만 로드된 Blockbench 렌더",
 "LEGACY_3D_APPROXIMATION":"이전 비공식 자체 렌더 (대체 검증 아님)",
 "NO_REAL_MOD_ASSET":"적합한 마크 모드 모델 미발견",
 "REAL_MODEL_IMPORT_FAILED":"실제 모델 변환 실패 (검수 필요)",
 "NATIVE_BLOCKBENCH_MODEL_UNAVAILABLE":"Blockbench에서 해당 모델 로드 실패",
 }.get(grade,grade)
def render_panel(row,mcfile,legacyfile):
 full=Image.new("RGB",SIZ,(247,249,251))
 d=ImageDraw.Draw(full)
 d.rounded_rectangle((15,48,663,466),radius=10,fill=(226,234,240))
 d.rounded_rectangle((684,48,1332,466),radius=10,fill=(232,239,243))
 f=font(18);sub=font(14);tiny=font(12)
 name=f"{row['index']:03d}   {row['pz_name']}" + (" / "+row["pz_style"] if row["pz_style"] else "")
 d.text((22,10),name[:85],font=f,fill=(31,55,77))
 d.text((29,61),"PROJECT ZOMBOID   |   완성 가구 (원본 타일 조립)",font=sub,fill=(54,80,101))
 d.text((699,61),"MINECRAFT MOD   |   "+provenance_short(row["render_grade"]),font=sub,fill=(55,82,102))
 with Image.open(get_pz_source(row)) as src:
  left=cut_pz(src.convert("RGB"))
  left.thumbnail((585,337),Image.Resampling.LANCZOS)
  if left.width>0 and left.height>0:
   scale=min(2.6,580/max(1,left.width),330/max(1,left.height))
   if scale>1:
    left=left.resize((round(left.width*scale),round(left.height*scale)),Image.Resampling.NEAREST)
   full.paste(left,(int(339-left.width/2),int(263-left.height/2)),left)
 if mcfile:
  with Image.open(mcfile) as src:
   right=cut_mc(src)
   right.thumbnail((594,347),Image.Resampling.LANCZOS)
   full.paste(right,(int(1007-right.width/2),int(266-right.height/2)),right)
 elif legacyfile and legacyfile.exists():
  with Image.open(legacyfile) as src:
   img=src.convert("RGB")
   # Previous card contains source image left, old model projection right;
   # old projection is never represented as a true Blockbench screenshot.
   right=img.crop((600,86,1158,425))
   right.thumbnail((580,332),Image.Resampling.LANCZOS)
   full.paste(right,(int(1007-right.width/2),int(264-right.height/2)))
 else:
  d.rounded_rectangle((724,131,1296,399),radius=11,outline=(152,168,184),width=3,fill=(241,244,247))
  no=(row["unmatched_reason"] or "실제 모드의 일치 모델이 없음")
  d.text((750,205),"MOD FURNITURE NOT VERIFIED",font=font(20),fill=(126,59,60))
  d.text((750,247),"원본과 맞는 가구를 찾지 못함",font=font(17),fill=(115,76,76))
  d.text((750,284),"임의 가구로 채우지 않음 · 제작/추가 검색 필요",font=font(13),fill=(113,78,77))
 d.line((22,477,1327,477),fill=(172,187,201),width=2)
 d.text((25,488),("PZ "+row["pz_parts"]+" tiles / footprint "+row["pz_grid"]+
      "  |  Original bbox "+row["pz_bbox"])[:122],font=tiny,fill=(40,60,80))
 d.text((25,511),("MC block ID: "+(row["chosen_mc_id"] or "[NO VERIFIED MOD MATCH]"))[:130],font=tiny,fill=(49,61,79))
 d.text((25,535),("Inspection: "+row["visual_verdict"]+"  |  evidence: "+row["render_grade"])[:130],font=tiny,fill=(119,65,60))
 d.text((25,562),"NOTE: Game placement/collision and 1-to-1 likeness are NOT certified. Missing or partial cases are explicitly labelled.",font=font(11),fill=(121,83,75))
 return full
def csv_html(rows):
 parts=[]
 for r in rows:
  name=r["pz_name"]+(" / "+r["pz_style"] if r["pz_style"] else "")
  key=(name+" "+r["chosen_mc_id"]+" "+r["render_grade"]+" "+r["visual_verdict"]+" "+r["risk_flags"]).lower()
  parts.append(
   '<article class="card" data-search="'+html.escape(key,quote=True)+'" data-grade="'+html.escape(r["render_grade"])+'">'
   '<img alt="'+html.escape(name,quote=True)+'" loading="lazy" src="'+html.escape(r["card_path"],quote=True)+'">'
   '<div class="meta"><h2>'+html.escape(name)+'</h2>'+
   '<p><b>선정 모델:</b> <code>'+html.escape(r["chosen_mc_id"] or "적합 후보 미발견")+'</code></p>'+
   '<p><b>이미지 근거:</b> '+html.escape(provenance_short(r["render_grade"]))+'</p>'+
   '<p><b>기존 검수:</b> '+html.escape(r["visual_verdict"])+'</p>'+
   '<p><b>크기:</b> PZ '+html.escape(r["pz_grid"])+' / 부품 '+r["pz_parts"]+
   '개; MC 모델 '+html.escape(r["mc_model_bound"])+'</p>'+
   '<p><b>속성 차이 경고:</b> '+html.escape(r["risk_flags"][:420])+'</p>'+
   '<p><b>다음 조치:</b> '+html.escape(r["next_action"])+'</p>'+
   '<details><summary>원본 타일·모드 모델 속성 상세보기</summary><pre>'+
   html.escape(json.dumps({"original_PZ":json.loads(r["pz_original_properties_json"]),
    "MC_sources":json.loads(r["mc_import_evidence_json"]),
    "MC_selected_id":r["chosen_mc_id"],
    "model_verification":r["render_grade"],
    "visual_approved":r["is_1to1_approved"]},ensure_ascii=False,indent=2))+
    '</pre></details></div></article>'
  )
 return """<!DOCTYPE html><html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
 <title>로즈우드 357종 원본 vs 마크 모드 실제 렌더링 전체 대조</title>
 <style>body{margin:0;font:14px system-ui,'Malgun Gothic',sans-serif;color:#26394c;background:#eaf0f4}
 header{position:sticky;top:0;background:white;border-bottom:1px solid #cfdae2;padding:16px 3%;z-index:3}
 h1{font-size:23px;margin:0 0 10px}header p{margin:5px 0;max-width:1160px}
 .controls{display:flex;gap:9px;flex-wrap:wrap;margin-top:10px}input,select{font:inherit;padding:10px;border:1px solid #c1ccd4;border-radius:7px}
 input{flex:1;min-width:240px}main{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,600px),1fr));gap:18px;padding:18px 3%}
 .card{background:white;border:1px solid #d4dfe7;border-radius:12px;box-shadow:0 3px 9px #1a2b4712;padding:10px}
 .card img{width:100%;border-radius:8px}.meta{padding:6px 10px}.meta h2{font-size:18px}
 .meta p{font-size:13px;line-height:1.5;margin:6px 0}.meta code{overflow-wrap:anywhere}
 pre{white-space:pre-wrap;overflow-wrap:anywhere;background:#f0f3f6;padding:12px;font-size:11px}
 details{margin-top:9px}summary{cursor:pointer}</style></head><body>
 <header><h1>프로젝트 좀보이드 완성 가구 357종 ↔ 마크 가구 모델 전체 재대조</h1>
 <p>오른쪽 이미지는 모드 원본 .bbmodel 또는 JAR의 실제 JSON·PNG를 Blockbench 5.2.2에서 불러온 결과. 모델 import 실패나 원본 매칭이 없는 항목은 별도 표시합니다.
 실제 Minecraft 게임 스크린샷이 아니며, 1:1 외형/기능/설치 크기를 전부 인증한 자료는 아닙니다.</p>
 <div class="controls"><input id="q" placeholder="가구명·모드 ID·속성 검색"><select id="filter">
 <option value="">전체</option><option value="ACTUAL_NATIVE_BLOCKBENCH_SOURCE_BBMODEL">원본 .bbmodel 실제 Blockbench</option>
 <option value="ACTUAL_NATIVE_BLOCKBENCH_FULL_SOURCE_JSON">원본 JSON 모든 부품 Blockbench</option>
 <option value="NATIVE_BLOCKBENCH_PARTIAL_SOURCE_JSON">원본 JSON 일부 부품</option>
 <option value="LEGACY_3D_APPROXIMATION">구형 근사 렌더</option>
 <option value="NO_REAL_MOD_ASSET">대체품 미발견</option>
 </select><span id="count"></span></div></header><main>__BODY__</main>
 <script>let cards=[...document.querySelectorAll('article')],q=document.getElementById('q'),f=document.getElementById('filter'),n=document.getElementById('count');
 function show(){let v=q.value.trim().toLowerCase(),c=0;for(const x of cards){let a=x.dataset.search.includes(v)&&(!f.value||x.dataset.grade===f.value);x.style.display=a?'':'none';c+=a?1:0}n.textContent=c+' / '+cards.length+'개'}q.oninput=f.onchange=show;show();</script></body></html>""".replace("__BODY__","\n".join(parts))
def main():
 assert not OUT.exists()
 (OUT/"cards").mkdir(parents=True)
 rows=csvread(SOURCE/"REVISED_357_PZ_MC_MATCHES.csv")
 assert len(rows)==357
 proofs={}
 mods={"pfm":"paladins","mcwfurnitures":"macaws","refurbished_furniture":"refurbished","handcrafted":"handcrafted"}
 for mod in set(mods.values()):
  evidence=OTHERS/("PROOF_"+mod+".json")
  if not evidence.exists():raise RuntimeError("Source proof missing for "+mod)
  for x in json.loads(evidence.read_text("utf8")):
   proofs[x["blockstate_id"]]=x
 summary=collections.Counter();out=[];unmatched=[]
 for i,raw in enumerate(rows,1):
  key=raw["reviewed_replacement_mc_id"] or raw["mc_id"]
  mc,grade,note,proof=get_visual(raw,proofs)
  no_match=not key
  old_img=SOURCE/raw["card"]
  legacy=(old_img if old_img.exists() and key and mc is None else None)
  if legacy:
   grade="LEGACY_3D_APPROXIMATION"
   note="Only previous approximate image available; actual mod JAR source native render missing"
  if no_match:
   unmatched.append({"index":i,"pz_name":raw["pz_name"],"pz_style":raw["pz_style"],
       "pz_parts":raw["pz_parts"],"original_status":raw["old_match_class"],
       "reason":"No faithful blockstate model in seven inspected mod jars"})
  nextaction=("LOOK_FOR_ADDITIONAL_MOD_OR_CREATE_BLOCKBENCH_MODEL" if no_match
        else "RENDER_SOURCE_MODEL_WITH_CORRECT_LOADER" if legacy
        else "REVIEW_PARTIAL_IMPORT" if grade=="NATIVE_BLOCKBENCH_PARTIAL_SOURCE_JSON"
        else "COMPARE_VISUAL_SHAPE_AND_MINECRAFT_PLACEMENT")
  record=dict(index=i,pz_name=raw["pz_name"],pz_style=raw["pz_style"],
   pz_preview=raw["pz_preview"],pz_parts=raw["pz_parts"],
   pz_grid=raw["pz_tiles"],pz_bbox=raw["pz_3d_bbox"],
   pz_original_properties_json=raw["pz_properties_json"],
   original_mc_id=raw["mc_id"],
   chosen_mc_id=key,
   mc_mod=raw["mod"],mc_model_bound=raw["mc_bbox"],
   mc_import_evidence_json=json.dumps(proof,ensure_ascii=False),
   render_grade=grade,note=note,
   visual_verdict=raw["new_match_status"],
   risk_flags=raw["warnings"],
   planned_custom_model= "YES" if no_match else "NO",
   is_1to1_approved="NO",native_renderer_is_game="NO",
   unmatched_reason="Unable to find faithful match in 7 inspected mod files" if no_match else "",
   next_action=nextaction,
   card_path="cards/"+f"{i:03d}_PZ_MC.jpg")
  render_panel(record,mc,legacy).save(OUT/record["card_path"],quality=84,optimize=True,subsampling=0)
  out.append(record);summary[grade]+=1
  if i%60==0:print("COMPLETED_REVIEW_CARDS",i,"out of 357",dict(summary),flush=True)
 csvwrite(OUT/"ALL_357_FULL_RENDER_MATCHING.csv",out)
 csvwrite(OUT/"UNMATCHED_NEEDS_REAL_FURNITURE_MOD_OR_CUSTOM_MODEL.csv",unmatched)
 (OUT/"INDEX.html").write_text(csv_html(out),encoding="utf8")
 # 4 comparison cards per sheet; no auto skipping or hidden placeholders.
 sheet=OUT/"contact_sheets";sheet.mkdir()
 for start in range(0,len(out),4):
  img=Image.new("RGB",(2700,1180),(248,249,252))
  for k,row in enumerate(out[start:start+4]):
   with Image.open(OUT/row["card_path"]) as source:
    img.paste(source,((k%2)*1350,(k//2)*590))
  img.save(sheet/f"COMPLETE_{start//4+1:03d}.jpg",quality=78,optimize=True)
 summary=dict(sorted(summary.items()))
 manifest={"pz_style_count":len(out),
  "total_full_size_side_by_side_cards":len(out),
  "all_original_PZ_complete_previews_present":len(out),
  "actual_Minecraft_5_mods_rendered_source_image_count":sum(v for k,v in summary.items() if k.startswith("ACTUAL_NATIVE") or k=="NATIVE_BLOCKBENCH_PARTIAL_SOURCE_JSON"),
  "minecraft_missing_or_unverified_match_count":len(unmatched),
  "native_model_evidence_grades":summary,
  "contact_sheets":len(list(sheet.glob("*.jpg"))),
  "previous_50_native_visual_review_and_8_replacements_kept":True,
  "certified_1to1_matching_count":0,
  "game_engine_runtime_placements_verified":0,
  "mod_asset_sources":"Original 5 Minecraft Forge mod JAR with original model and texture; 2 other mods listed but no matched IDs in current 357.",
  "no_fake_mod_models":"Unmatched sources explicitly marked; no invented object substituted."}
 (OUT/"MANIFEST.json").write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+"\n",encoding="utf8")
 note="# 로즈우드 357종 완성 가구 ↔ Minecraft 가구 모드 실제 3D 이미지 전체 재대조\n\n"
 note+="**이번 수정:** 이전 221개의 구형 근사 그림을 대체할 수 있도록 Decocraft 이외 4개 모드의 원본 Minecraft Java 모델 JSON/PNG를 Blockbench 5.2.2로 변환·실제 캡처했다. 원본 PZ는 357개 모두 원래 조립된 완성 가구를 사용한다.\n\n"
 note+="## 증거 수준별 수량\n"
 for k,v in summary.items():note+=f"- {k}: {v}개\n"
 note+="\n## 정확한 한계\n- 22개는 7개 모드 JAR의 초기 검수에서 대응 모드 가구를 찾지 못한 항목. 비어 보이는 오른쪽 패널 대신 **명시적인 불일치/추가 모드 탐색 또는 직접 모델 제작** 표시. 가짜 모델을 넣어 매칭 완료로 위장하지 않음.\n"
 note+="- 다른 모드에서 원본 JSON cuboids를 Blockbench 자유 모델로 재조립한 경우 원본 게임의 동적 blockstate, connected textures, custom loader, shape rotation은 추후 검수 필요. 일부 부품 누락은 PARTIAL로 표시.\n"
 note+="- 원본 JAR이나 텍스처 원본은 저장/배포하지 않음. 비교용 캡처와 출처 해시만 남김.\n"
 note+="- 357개를 실제 Minecraft 게임에서 배치 확인하지 않았고, 1:1 형상·기능 최종 인증은 0개.\n"
 note+="\n## 파일\n- ZIP 압축 해제 후 INDEX.html 검색/필터로 전체 확인.\n- ALL_357_FULL_RENDER_MATCHING.csv에 크기, PZ 속성, 실제 모델 ID, 이미지 근거, 원본 50건 수동 판정과 8건 개선 매칭, 남은 쟁점 보관.\n- UNMATCHED_NEEDS_REAL_FURNITURE_MOD_OR_CUSTOM_MODEL.csv: 모드 모델을 찾지 못한 대상.\n"
 (OUT/"README_KO.md").write_text(note,encoding="utf8")
 with zipfile.ZipFile(OUT/"ROSEWOOD_ALL_357_FURNITURE_SOURCE_NATIVE_VISUAL_COMPARISONS.zip","w",zipfile.ZIP_DEFLATED,compresslevel=4) as z:
  for f in OUT.rglob("*"):
   if f.is_file() and f.name!="ROSEWOOD_ALL_357_FURNITURE_SOURCE_NATIVE_VISUAL_COMPARISONS.zip":
    z.write(f,f.relative_to(OUT))
 with zipfile.ZipFile(OUT/"ROSEWOOD_ALL_357_FURNITURE_SOURCE_NATIVE_VISUAL_COMPARISONS.zip") as z:
  assert z.testzip() is None
  assert "INDEX.html" in z.namelist()
 print("RESULT",json.dumps(manifest,ensure_ascii=False),flush=True)
if __name__=="__main__":main()
