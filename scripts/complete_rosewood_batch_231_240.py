#!/usr/bin/env python3
"""Evidence-only independent review of Rosewood B lane 231-240.
Build 10 PZ-vs-verified-Minecraft comparisons, never auto-approve.
"""
from pathlib import Path
from PIL import Image, ImageOps, ImageDraw, ImageFont
import csv, json, hashlib, zipfile, html, textwrap, shutil
ROOT=Path(__file__).resolve().parents[1]
D=ROOT/"analysis/rosewood_furniture/2026-10-31"
BASE=D/"all_357_complete_native_comparisons_v1"
PREVIEW=D/"complete_furniture_visual_3d_v1"
NATIVE=D/"ten_batch_review/24_231_240/extra_decocraft_render"
OUT=D/"ten_batch_review/batch_231_240_v1"
DECISIONS=ROOT/"scripts/rosewood_batch24_231_240_decisions.json"
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def read_csv(p):
 with p.open(encoding="utf-8-sig",newline="") as f:return list(csv.DictReader(f))
def write_csv(p,rows):
 assert rows
 with p.open("w",encoding="utf-8-sig",newline="") as f:
  w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
def font(size,bold=False):
 for p in ("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf","/usr/share/fonts/truetype/liberation2/LiberationSans-Regular.ttf"):
  if Path(p).is_file():return ImageFont.truetype(p,size)
 return ImageFont.load_default()
def card(idx,src,decision,proof):
 pz=PREVIEW/src["pz_preview"]
 assert pz.is_file(),pz
 native=NATIVE/proof.get("native_model_screenshot","__NO_NATIVE__")
 verified=bool(proof.get("loaded_verified") and native.is_file() and proof.get("source_sha256") and proof.get("variant_sha256"))
 legacy=BASE/src["card_path"]
 W,H=1500,690
 out=Image.new("RGB",(W,H),(246,248,251));dr=ImageDraw.Draw(out)
 dr.text((25,17),f"{idx:03d} {src['pz_name']} / {src['pz_style']}",font=font(25,True),fill=(29,49,66))
 for x in (18,768):dr.rounded_rectangle((x,60,x+714,555),radius=13,fill=(226,234,241))
 dr.text((30,76),"PROJECT ZOMBOID | assembled original PZ preview",font=font(15),fill=(38,66,83))
 dr.text((780,76),"MINECRAFT | verified native source / fallback",font=font(15),fill=(38,66,83))
 with Image.open(pz) as im:
  # Crop the preview's header, footer and empty template, retaining only
  # source pixels. Never redraw or alter the PZ sprite geometry.
  import numpy as np
  inner=im.convert("RGBA").crop((35,115,515,397))
  rgb=np.asarray(inner.convert("RGB")).astype("int16")
  bg=rgb[0,0,:]
  ys,xs=np.where(np.max(np.abs(rgb-bg),axis=2)>25)
  if len(xs)>15:
   inner=inner.crop((max(0,int(xs.min())-22),max(0,int(ys.min())-22),
                     min(inner.width,int(xs.max())+23),min(inner.height,int(ys.max())+23)))
  im=ImageOps.contain(inner,(670,430),Image.Resampling.LANCZOS)
  out.paste(im,(375-im.width//2,326-im.height//2),im)
 evidence="NO_VERIFIED_NATIVE_SOURCE"
 if verified:
  with Image.open(native) as im:
   im=im.convert("RGB")
   import numpy as np
   a=np.asarray(im);ys,xs=np.where(a.max(axis=2)>13)
   if len(xs)>40:im=im.crop((max(0,int(xs.min())-15),max(0,int(ys.min())-15),min(im.width,int(xs.max())+16),min(im.height,int(ys.max())+16)))
   im=ImageOps.contain(im,(670,430),Image.Resampling.LANCZOS)
   out.paste(im,(1125-im.width//2,326-im.height//2))
  evidence="NATIVE_BLOCKBENCH_5_2_2_VERIFIED_SOURCE_BBMODEL_CROPPED" if idx==238 else "NATIVE_BLOCKBENCH_5_2_2_VERIFIED_SOURCE_BBMODEL"
 elif legacy.is_file():
  with Image.open(legacy) as im:
   im=im.convert("RGB").crop((im.width//2,86,im.width,max(87,im.height-110)))
   im=ImageOps.contain(im,(650,430),Image.Resampling.LANCZOS)
   out.paste(im,(1125-im.width//2,326-im.height//2))
  evidence="LEGACY_FALLBACK_NOT_NEW_NATIVE_VERIFIED"
 else:
  dr.text((820,280),"NO VERIFIED MC MODEL",font=font(24,True),fill=(151,51,45))
 dr.line((18,566,1480,566),fill=(155,169,185),width=2)
 status=decision["status"]
 if not verified and status.startswith("CONDITIONAL"):status="DEFER_MISSING_NATIVE_EVIDENCE"
 dr.text((26,582),"Review: "+status,font=font(16,True),fill=(141,57,47) if status.startswith("DEFER") else (34,103,68))
 dr.text((26,615),"Inspected candidate: decocraft:"+decision["model"],font=font(15),fill=(45,67,84))
 dr.text((26,645),"Evidence: "+evidence+" | Game install / 1:1 visual equivalence NOT certified",font=font(12),fill=(101,76,68))
 dest=OUT/"cards"/f"{idx:03d}_PZ_vs_MC.jpg"
 out.save(dest,quality=91,subsampling=0,optimize=True)
 return dest,status,evidence,native if verified else None,legacy if not verified and legacy.is_file() else None
def main():
 decisions=json.loads(DECISIONS.read_text("utf8"))
 assert [x["index"] for x in decisions]==list(range(231,241))
 assert len({x["model"] for x in decisions})==10
 source={int(x["index"]):x for x in read_csv(BASE/"ALL_357_FULL_RENDER_MATCHING.csv")}
 assert all(i in source for i in range(231,241))
 proofs=json.loads((NATIVE/"NATIVE_BLOCKBENCH_PROOF.json").read_text("utf8"))
 assert len(proofs)==10
 by_model={x["id"]:x for x in proofs}
 assert all(d["model"] in by_model for d in decisions)
 if OUT.exists():
  import os
  assert os.environ.get("ROSEWOOD_BATCH24_REBUILD")=="1","Existing review must not be overwritten without explicit rebuild flag"
  shutil.rmtree(OUT)  # Only this independent batch_231_240_v1 directory
 (OUT/"cards").mkdir(parents=True)
 shutil.copyfile(NATIVE/"NATIVE_BLOCKBENCH_PROOF.json",OUT/"NATIVE_BLOCKBENCH_PROOF.json")
 rows=[];deferred=[];provenance=[]
 for dec in decisions:
  idx=dec["index"];orig=source[idx];proof=by_model[dec["model"]]
  dest,status,evidence,native,legacy=card(idx,orig,dec,proof)
  pz=PREVIEW/orig["pz_preview"]
  row={
   "index":idx,"pz_name":orig["pz_name"],"pz_style":orig["pz_style"],
   "pz_parts":orig["pz_parts"],"pz_footprint":orig["pz_grid"],
   "pz_preview_path":orig["pz_preview"],"pz_preview_sha256":sha(pz),
   "previous_mc_candidate_id":orig["original_mc_id"],"previous_mc_chosen_id":orig["chosen_mc_id"],
   "native_inspected_model_id":"decocraft:"+dec["model"],
   "new_conditional_candidate_id":dec.get("candidate","") if status.startswith("CONDITIONAL") else "",
   "review_status":status,"pz_shape_features":dec["shape"],
   "manual_review_reason":dec["why"],"followup_requirement":dec["followup"],
   "native_model_provenance":evidence,
   "native_source_model_path":proof.get("source_model_path",""),
   "native_source_texture_path":proof.get("variant_texture_path",""),
   "native_source_model_sha256":proof.get("source_sha256",""),
   "native_source_texture_sha256":proof.get("variant_sha256",""),
   "native_model_screenshot_sha256":sha(native) if native else "",
   "legacy_comparison_sha256_if_fallback":sha(legacy) if legacy else "",
   "new_comparison_card_sha256":sha(dest),"card_path":"cards/"+dest.name,
   "native_loaded_verified":"TRUE" if native else "FALSE",
   "full_native_model_in_frame_verified":"NO" if idx==238 else ("YES" if native else "NO"),
   "exact_1_to_1_visual_match_approved":"NO",
   "approved_for_minecraft_world_replacement":"NO",
   "game_install_collision_function_verified":"NO"
  }
  rows.append(row)
  if status.startswith("DEFER"):
   deferred.append({k:row[k] for k in ("index","pz_name","pz_style","review_status","pz_shape_features","manual_review_reason","followup_requirement","native_inspected_model_id")})
  provenance.append({
   "index":idx,"source_pz_preview":str(pz.relative_to(ROOT)),"pz_sha256":sha(pz),
   "mc_model":dec["model"],"mc_source_model":proof.get("source_model_path",""),
   "mc_source_sha256":proof.get("source_sha256",""),
   "mc_source_texture":proof.get("variant_texture_path",""),
   "mc_texture_sha256":proof.get("variant_sha256",""),
   "native_viewport_sha256":sha(native) if native else "",
   "baseline_fallback_sha256":sha(legacy) if legacy else "",
   "new_card_sha256":sha(dest),"evidence_type":evidence})
 write_csv(OUT/"BATCH_231_240_MANUAL_VISUAL_REVIEW.csv",rows)
 write_csv(OUT/"BATCH_231_240_DEFERRED_OTHER_MODS.csv",deferred)
 write_csv(OUT/"BATCH_231_240_SHA256_PROVENANCE.csv",provenance)
 versions=json.loads((D/"minecraft_actual_mod_registry_v2/MOD_VERSION_SOURCES.json").read_text("utf8"))
 mod=next(x for x in versions if x["label"]=="decocraft")
 cond=[x["index"] for x in rows if x["review_status"].startswith("CONDITIONAL")]
 defer=[x["index"] for x in rows if x["review_status"].startswith("DEFER")]
 manifest={
  "scope":"231-240","lane":"B","total_pz_styles":357,
  "this_batch_individual_reviews":10,"attempted_original_decocraft_models":10,
  "successful_native_blockbench_viewports":sum(x["native_loaded_verified"]=="TRUE" for x in rows),
  "new_comparison_cards":10,"conditional_candidates":len(cond),
  "full_native_model_visible_viewports":sum(x["full_native_model_in_frame_verified"]=="YES" for x in rows),
  "cropped_native_viewports":[238],
  "deferred_other_mods_or_vanilla":len(defer),
  "certified_1_to_1_matches":0,"minecraft_game_install_collision_verified":0,
  "source_tables_overwritten":False,"parallel_group_progress_overwritten":False,
  "source_mod":"Decocraft","source_mod_version":mod["version"],
  "source_mod_jar_sha512":mod["sha512"],
  "source_mod_url":"https://modrinth.com/mod/decocraft/version/"+mod["version_id"],
  "source_3d_render":"official Blockbench 5.2.2 on actual source BBMODEL and verified texture",
  "native_image_fallback_count":sum(x["native_loaded_verified"]!="TRUE" for x in rows),
  "previous_verified_individual_scope":"001-230 (separate draft PRs; some work not merged), 251-260 lane A; 241-250 lane C pending"
 }
 (OUT/"MANIFEST.json").write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+"\n",encoding="utf8")
 progress={"batch":"24","scope":"231-240","lane":"B","this_scope_reviewed":list(range(231,241)),
  "conditional":cond,"deferred":defer,"approved_for_world":[],"merged_into_global_progress":False}
 (OUT/"BATCH24_STANDALONE_PROGRESS.json").write_text(json.dumps(progress,ensure_ascii=False,indent=2)+"\n",encoding="utf8")
 notes=[
  "# 로즈우드 가구 24차: B 레인 231~240번 독립 수동 시각 검수",
  "PZ B42 완성형 원본 10개와 기존 비교판을 직접 육안 대조했다. 이번 후보는 Decocraft 3.0.4-1.20.1 공식 배포 JAR의 원본 BBMODEL 및 텍스처를 SHA512/SHA256 검증한 뒤 Blockbench 5.2.2에서 재렌더했다.",
  "본 결과는 10개 고유 가구에 대한 외형 판정이다. 모드 실제 게임 설치, 1:1 동일성, 충돌/상호작용/방향, PZ 멀티타일 재조립 정확성은 인증하지 않았다.",
  "기존 001~230번 및 A/C 레인의 독립 Draft PR은 병합하거나 덮어쓰지 않았다. 원본 TMX/PNG/SQLite 및 글로벌 357행 매칭표는 변경하지 않았다.",
  f"검수 {len(rows)}종: 조건부 {len(cond)}, 보류 {len(defer)}. 네이티브 Blockbench 원본 로드 {manifest['successful_native_blockbench_viewports']}/10, 전체 캡처 {manifest['full_native_model_visible_viewports']}/10 (238번 잘림), 비교 JPG 10장, 인게임 1:1 인증 0종.",
  f"Decocraft 원본 JAR SHA512: \`{mod['sha512']}\` / https://modrinth.com/mod/decocraft/version/{mod['version_id']}",
  "## 개별 검수"
 ]
 for x in rows:
  notes.append(f"### {x['index']} {x['pz_name']} / {x['pz_style']}\n\n판정: **{x['review_status']}**. 검토 후보: {x['native_inspected_model_id']}.\n\nPZ 형태: {x['pz_shape_features']}\n\n육안 비교 및 오매칭 원인: {x['manual_review_reason']}\n\n추가 확인: {x['followup_requirement']}\n\n원본 PZ SHA256: \`{x['pz_preview_sha256']}\`\n\n원본 MC 모델 SHA256: \`{x['native_source_model_sha256'] or '미검증'}\`\n\n비교 카드 SHA256: \`{x['new_comparison_card_sha256']}\`\n")
 notes+=["## 산출물",
 "cards/ : 231~240 PZ 대 실제 원본 Minecraft 모델(미확인 시 구형 참고 이미지로 명시) JPG 10장",
 "BATCH_231_240_MANUAL_VISUAL_REVIEW.csv : 검수 판정·형태·이전 오매칭·후속 확인",
 "BATCH_231_240_DEFERRED_OTHER_MODS.csv : 다른 모드 또는 바닐라 재검색 목록",
 "BATCH_231_240_SHA256_PROVENANCE.csv : 원본·텍스처·렌더·카드 SHA256",
 "NATIVE_BLOCKBENCH_PROOF.json / MANIFEST.json / BATCH24_STANDALONE_PROGRESS.json : 원본 렌더 증빙 및 범위",
 "INDEX.html / ROSEWOOD_BATCH_231_240_MANUAL_REVIEW.zip : 갤러리와 묶음 산출물"]
 (OUT/"README_KO.md").write_text("\n\n".join(notes)+"\n",encoding="utf8")
 items="\n".join(f'<article><h2>{r["index"]} {html.escape(r["pz_name"])} / {html.escape(r["pz_style"])}</h2><p>{html.escape(r["review_status"])} | {html.escape(r["native_inspected_model_id"])}</p><img src="{r["card_path"]}" alt="PZ versus native Minecraft Blockbench model" loading="lazy"/><p>{html.escape(r["manual_review_reason"])}</p></article>' for r in rows)
 page=f'<!doctype html><html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Rosewood 231-240 manual review</title><style>body{{font-family:system-ui,sans-serif;background:#f1f4f8;color:#183044;max-width:1250px;margin:0 auto;padding:25px}}article{{background:white;border-radius:14px;margin:25px 0;padding:18px;box-shadow:0 2px 12px #0001}}img{{width:100%;height:auto;border-radius:10px}}p{{line-height:1.7}}</style></head><body><h1>로즈우드 231~240 개별 검수</h1><p>조건부 {len(cond)} · 보류 {len(defer)} · 인게임 인증 0</p>{items}</body></html>'
 (OUT/"INDEX.html").write_text(page,encoding="utf8")
 z=OUT/"ROSEWOOD_BATCH_231_240_MANUAL_REVIEW.zip"
 with zipfile.ZipFile(z,"w",zipfile.ZIP_DEFLATED,compresslevel=5) as archive:
  for f in sorted(OUT.rglob("*")):
   if f.is_file() and f!=z:archive.write(f,f.relative_to(OUT))
 with zipfile.ZipFile(z) as archive:
  assert archive.testzip() is None
  assert len([x for x in archive.namelist() if x.startswith("cards/") and x.endswith(".jpg")])==10
 assert [x["index"] for x in rows]==list(range(231,241))
 assert len(cond)+len(defer)==10
 assert all(x["approved_for_minecraft_world_replacement"]=="NO" for x in rows)
 print("BATCH24_VALIDATED",json.dumps(manifest,ensure_ascii=False),flush=True)
if __name__=="__main__":main()
