#!/usr/bin/env python3
"""Generate evidence-based Rosewood 221-230 manual review cards from PZ source previews
and verified native Blockbench 5.2.2 screenshots. Never treat partial previews or
an absent source model as an approved Minecraft world replacement.
"""
from pathlib import Path
import csv, json, hashlib, zipfile, html, io
from PIL import Image, ImageDraw, ImageFont, ImageOps
ROOT=Path(__file__).resolve().parents[1]
D=ROOT/"analysis/rosewood_furniture/2026-10-31"
OUT=D/"ten_batch_review/batch_221_230_v1"
NATIVE=D/"ten_batch_review/22_221_230/extra_decocraft_render"
BASE=D/"all_357_complete_native_comparisons_v1"
PREVIEW=D/"complete_furniture_visual_3d_v1"
DECISIONS=ROOT/"scripts/rosewood_batch22_221_230_decisions.json"

def sha(path):
 return hashlib.sha256(Path(path).read_bytes()).hexdigest()
def read_csv(path):
 with path.open("r",encoding="utf-8-sig",newline="") as f:return list(csv.DictReader(f))
def save_csv(path,rows,cols):
 with path.open("w",encoding="utf-8-sig",newline="") as f:
  w=csv.DictWriter(f,fieldnames=cols,extrasaction="ignore");w.writeheader();w.writerows(rows)
def font(size,bold=False):
 paths=["/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf","/usr/share/fonts/truetype/liberation2/LiberationSans-Regular.ttf"]
 for p in paths:
  if Path(p).exists():return ImageFont.truetype(p,size)
 return ImageFont.load_default()
def make_card(row,decision,proof):
 idx=int(row["index"])
 pz=PREVIEW/row["pz_preview"]
 assert pz.is_file(),pz
 native_file=NATIVE/(proof.get("native_model_screenshot") or "__MISSING__")
 use_native=bool(proof.get("loaded_verified") and native_file.is_file())
 baseline=BASE/row["card_path"]
 W,H=1500,680
 out=Image.new("RGB",(W,H),(244,247,250))
 dr=ImageDraw.Draw(out)
 dr.text((24,16),f"{idx:03d}  {row['pz_name']} / {row['pz_style']}",font=font(25,True),fill=(25,49,71))
 dr.rounded_rectangle((18,60,734,553),radius=12,fill=(224,232,239))
 dr.rounded_rectangle((766,60,1482,553),radius=12,fill=(224,232,239))
 dr.text((32,75),"PROJECT ZOMBOID | original assembled sprite",font=font(16),fill=(44,65,81))
 dr.text((782,75),"MINECRAFT | native source model / fallback evidence",font=font(16),fill=(44,65,81))
 with Image.open(pz) as im:
  im=ImageOps.contain(im.convert("RGBA"),(650,430),Image.Resampling.LANCZOS)
  out.paste(im,(376-im.width//2,323-im.height//2),im)
 evidence="NO_VERIFIED_MOD_ASSET"
 if use_native:
  with Image.open(native_file) as im:
   im=im.convert("RGB")
   # Crop black background around actual model; never fabricate or replace source geometry.
   import numpy as np
   a=np.asarray(im)
   mask=a.max(axis=2)>13
   yy,xx=np.where(mask)
   if len(xx)>40:
    box=(max(0,int(xx.min())-18),max(0,int(yy.min())-18),min(im.width,int(xx.max())+19),min(im.height,int(yy.max())+19))
    im=im.crop(box)
   im=ImageOps.contain(im,(660,430),Image.Resampling.LANCZOS)
   # Black background is from native Blockbench viewport, not generated geometry.
   out.paste(im,(1124-im.width//2,323-im.height//2))
  evidence="NATIVE_BLOCKBENCH_5_2_2_VERIFIED_SOURCE_BBMODEL"
 elif baseline.is_file():
  with Image.open(baseline) as im:
   im=im.convert("RGB").crop((max(0,im.width//2),88,im.width,max(89,im.height-110)))
   im=ImageOps.contain(im,(650,430),Image.Resampling.LANCZOS)
   out.paste(im,(1124-im.width//2,323-im.height//2))
  evidence="LEGACY_BASELINE_FALLBACK_NOT_NEW_NATIVE_VERIFIED"
 else:
  dr.rounded_rectangle((810,175,1436,438),outline=(145,82,76),width=3,radius=14)
  dr.text((842,256),"NO VERIFIED MINECRAFT MODEL",font=font(22,True),fill=(148,58,52))
 dr.line((18,567,1482,567),fill=(152,169,184),width=2)
 label=decision["status"]
 if label.startswith("CONDITIONAL") and not use_native:label="DEFER_NO_NATIVE_EVIDENCE_THIS_RUN"
 dr.text((26,582),"Review: "+label,font=font(17),fill=(143,54,46) if label.startswith("DEFER") else (36,92,66))
 dr.text((26,614),"Minecraft source: "+(decision["candidate"] or ("decocraft:"+decision["model"] if decision["model"] else "[none]")),font=font(15),fill=(45,67,84))
 dr.text((26,643),"No in-game installation / collision / 1:1 equivalence certified. Evidence: "+evidence,font=font(12),fill=(92,76,69))
 dest=OUT/"cards"/f"{idx:03d}_PZ_vs_MC.jpg"
 out.save(dest,quality=91,subsampling=0,optimize=True)
 return dest,evidence,label,(native_file if use_native else None),(baseline if not use_native and baseline.exists() else None)

def main():
 decisions=json.loads(DECISIONS.read_text("utf8"))
 assert [x["index"] for x in decisions]==list(range(221,231))
 source=read_csv(BASE/"ALL_357_FULL_RENDER_MATCHING.csv")
 mapping={int(x["index"]):x for x in source}
 assert all(i in mapping for i in range(221,231))
 proofs=json.loads((NATIVE/"NATIVE_BLOCKBENCH_PROOF.json").read_text("utf8"))
 by_model={x["id"]:x for x in proofs}
 assert len(proofs)==10
 OUT.mkdir(parents=True,exist_ok=False)
 (OUT/"cards").mkdir()
 rows=[];deferred=[];provenance=[]
 for dec in decisions:
  idx=dec["index"];orig=mapping[idx];model=dec["model"]
  proof=by_model.get(model,{})
  card,evidence,status,native_file,baseline=make_card(orig,dec,proof)
  pzfile=PREVIEW/orig["pz_preview"]
  native_sha=sha(native_file) if native_file else ""
  baseline_sha=sha(baseline) if baseline else ""
  row={
   "index":idx,"pz_name":orig["pz_name"],"pz_style":orig["pz_style"],
   "pz_parts":orig["pz_parts"],"pz_footprint":orig["pz_grid"],
   "pz_preview_path":orig["pz_preview"],"pz_preview_sha256":sha(pzfile),
   "previous_mc_candidate_id":orig["original_mc_id"],"previous_mc_chosen_id":orig["chosen_mc_id"],
   "native_inspected_model_id":("decocraft:"+model if model else ""),
   "new_conditional_candidate_id":dec["candidate"] if status.startswith("CONDITIONAL") else "",
   "review_status":status,"manual_review_reason":dec["why"],
   "pz_shape_features":dec["shape"],"followup_requirement":dec["followup"],
   "native_model_provenance":evidence,
   "native_source_model_path":proof.get("source_model_path",""),
   "native_source_texture_path":proof.get("variant_texture_path",""),
   "native_source_model_sha256":proof.get("source_sha256",""),
   "native_source_texture_sha256":proof.get("variant_sha256",""),
   "native_model_screenshot_sha256":native_sha,
   "legacy_comparison_sha256_if_fallback":baseline_sha,
   "new_comparison_card_sha256":sha(card),"card_path":"cards/"+card.name,
   "native_loaded_verified":str(bool(native_file)).upper(),
   "exact_1_to_1_visual_match_approved":"NO",
   "approved_for_minecraft_world_replacement":"NO",
   "game_install_collision_function_verified":"NO"
  }
  rows.append(row)
  if status.startswith("DEFER"):deferred.append({k:row[k] for k in ("index","pz_name","pz_style","review_status","pz_shape_features","manual_review_reason","followup_requirement","native_inspected_model_id")})
  provenance.append({"index":idx,"model":model,"source_model":proof.get("source_model_path",""),"model_sha256":proof.get("source_sha256",""),"texture":proof.get("variant_texture_path",""),"texture_sha256":proof.get("variant_sha256",""),"viewport_sha256":native_sha,"pz_sha256":sha(pzfile),"card_sha256":sha(card),"evidence":evidence})
 save_csv(OUT/"BATCH_221_230_MANUAL_VISUAL_REVIEW.csv",rows,list(rows[0]))
 save_csv(OUT/"BATCH_221_230_DEFERRED_OTHER_MODS.csv",deferred,list(deferred[0]))
 save_csv(OUT/"BATCH_221_230_SHA256_PROVENANCE.csv",provenance,list(provenance[0]))
 cond=[r["index"] for r in rows if r["review_status"].startswith("CONDITIONAL")]
 defer=[r["index"] for r in rows if r["review_status"].startswith("DEFER")]
 assert len(cond)+len(defer)==10
 source_versions=json.loads((D/"minecraft_actual_mod_registry_v2/MOD_VERSION_SOURCES.json").read_text("utf8"))
 decocraft=next(x for x in source_versions if x["label"]=="decocraft")
 manifest={
  "scope":"221-230","total_pz_styles":357,"previous_verified_individual_scope":"001-210 (independent draft PRs, not merged; 211-220 belongs to lane C)"",
  "this_batch_individual_reviews":10,"attempted_original_decocraft_models":len(proofs),
  "successful_native_blockbench_viewports":sum(bool(x.get("loaded_verified") and x.get("native_model_screenshot") and (NATIVE/x["native_model_screenshot"]).is_file()) for x in proofs),
  "new_comparison_cards":len(list((OUT/"cards").glob("*_PZ_vs_MC.jpg"))),
  "conditional_candidates":len(cond),"deferred_other_mods_or_vanilla":len(defer),
  "certified_1_to_1_matches":0,"minecraft_game_install_collision_verified":0,
  "source_tables_overwritten":False,"parallel_group_progress_overwritten":False,
  "source_mod":"Decocraft","source_mod_version":decocraft["version"],
  "source_mod_jar_sha512":decocraft["sha512"],
  "source_mod_url":"https://modrinth.com/mod/decocraft/version/"+decocraft["version_id"],
  "source_3d_render":"official Blockbench 5.2.2 via existing source-authentic rendering script",
  "native_image_fallback_count":sum(r["native_model_provenance"]!="NATIVE_BLOCKBENCH_5_2_2_VERIFIED_SOURCE_BBMODEL" for r in rows)
 }
 (OUT/"MANIFEST.json").write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+"\n",encoding="utf8")
 progress={"batch":"22","scope":"221-230","lane":"A","this_scope_reviewed":list(range(221,231)),"conditional":cond,"deferred":defer,"approved_for_world":[],"merged_into_global_progress":False}
 (OUT/"BATCH21_STANDALONE_PROGRESS.json").write_text(json.dumps(progress,ensure_ascii=False,indent=2)+"\n",encoding="utf8")
 notes=["# 로즈우드 가구 22차 221~230번 개별 시각 검수",
 "PZ B42 원본 완성형 미리보기 10장과 이전 Minecraft 원본 Blockbench 비교판 10장을 실제로 육안 검수했다. 별도 GitHub Actions는 Decocraft 3.0.4-1.20.1 Forge 원본 BBMODEL/텍스처를 검증한 뒤 Blockbench 5.2.2로 새로 렌더해 추가 대조한다.",
 "이전 A 레인 131~140, 161~170 및 191~200번은 별도 Draft PR로 보존했으며, 이번 221~230번만 독립 검수했다. 다른 레인과 원본 파일은 건드리지 않았다.",
 f"원본 Decocraft JAR SHA-512: {decocraft['sha512']} | https://modrinth.com/mod/decocraft/version/{decocraft['version_id']}",
 f"검수 10종: 조건부 {len(cond)}종, 보류 {len(defer)}종. 네이티브 Blockbench 캡처 {manifest['successful_native_blockbench_viewports']}/{len(proofs)}개 모델. 비교 JPG 10장. 인게임 1:1 확정 0종.",
 "일부 원본 스프라이트의 SpriteGridPos 조립과 마크 모델의 동적 블록 상태는 잠정이다. 1×1/2×1/1×2 점유·방향·충돌·상호작용·색상/재질은 인게임 미검증. 부분 모델 캡처는 완성형으로 승인하지 않는다.",
 "## 개별 근거"]
 for r in rows:
  notes.append(f"### {r['index']} {r['pz_name']} / {r['pz_style']}\n판정: **{r['review_status']}**. 후보: {r['new_conditional_candidate_id'] or '보류'}\n\nPZ 형태: {r['pz_shape_features']}\n\n수동 비교: {r['manual_review_reason']}\n\n추가 검증: {r['followup_requirement']}\n\nPZ SHA-256: `{r['pz_preview_sha256']}`\nMC 모델 SHA-256: `{r['native_source_model_sha256'] or '미검증'}`\n비교 이미지 SHA-256: `{r['new_comparison_card_sha256']}`\n")
 notes+=["## 산출물","- cards/ : PZ 원본 완성형과 실제 소스 모델(또는 명시적 미검증 화면) 비교 JPG 10장",
 "- BATCH_221_230_MANUAL_VISUAL_REVIEW.csv : 상세 수동 판정, 기존 자동 매칭의 오차, 모델 출처와 SHA",
 "- BATCH_221_230_DEFERRED_OTHER_MODS.csv : 다른 모드·바닐라·신규 모델 후속 검토 목록",
 "- BATCH_221_230_SHA256_PROVENANCE.csv : 원본 PZ/BBMODEL/텍스처/Blockbench 캡처/카드 해시",
 "- MANIFEST.json / BATCH21_STANDALONE_PROGRESS.json : 독립 검수 범위·상태",
 "- INDEX.html : 10개 비교판 탐색",
 "- ROSEWOOD_BATCH_221_230_MANUAL_REVIEW.zip : 카드·CSV·README·인덱스 일괄 보관",
 "원본 게임 TMX/PNG/SQLite와 기존 357종 누적 검수 CSV, 다른 레인 결과를 수정하지 않는다."]
 (OUT/"README_KO.md").write_text("\n\n".join(notes)+"\n",encoding="utf8")
 cards="\n".join(f'<article><h2>{r["index"]} {html.escape(r["pz_name"])} / {html.escape(r["pz_style"])}</h2><p>{html.escape(r["review_status"])} | {html.escape(r["new_conditional_candidate_id"] or "DEFER")}</p><img src="{html.escape(r["card_path"])}" loading="lazy" alt="PZ vs Minecraft comparison"/><p>{html.escape(r["manual_review_reason"])}</p></article>' for r in rows)
 page=f'<!doctype html><html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Rosewood 221-230 manual review</title><style>body{{font-family:system-ui,sans-serif;background:#f1f4f8;color:#183044;max-width:1250px;margin:0 auto;padding:25px}}article{{background:white;border-radius:14px;margin:25px 0;padding:18px;box-shadow:0 2px 12px #0001}}img{{width:100%;height:auto;border-radius:10px}}p{{line-height:1.7}}</style></head><body><h1>로즈우드 221~230 개별 검수</h1><p>조건부 {len(cond)} · 보류 {len(defer)} · 인게임 최종 인증 0</p>{cards}</body></html>'
 (OUT/"INDEX.html").write_text(page,encoding="utf8")
 z=OUT/"ROSEWOOD_BATCH_221_230_MANUAL_REVIEW.zip"
 with zipfile.ZipFile(z,"w",zipfile.ZIP_DEFLATED,compresslevel=5) as archive:
  for f in sorted(OUT.rglob("*")):
   if f.is_file() and f!=z:archive.write(f,f.relative_to(OUT))
 with zipfile.ZipFile(z) as archive:
  assert archive.testzip() is None
  assert len([x for x in archive.namelist() if x.startswith("cards/") and x.endswith(".jpg")])==10
 assert [int(r["index"]) for r in rows]==list(range(221,231))
 assert all(r["exact_1_to_1_visual_match_approved"]=="NO" and r["approved_for_minecraft_world_replacement"]=="NO" for r in rows)
 print("BATCH21_VALIDATED",json.dumps(manifest,ensure_ascii=False),flush=True)
if __name__=="__main__":main()
