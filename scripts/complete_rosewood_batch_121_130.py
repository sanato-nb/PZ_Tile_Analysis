#!/usr/bin/env python3
"""Produce source-evidenced 121-130 furniture visual review, never auto-certify.
Read human-authored decision JSON; compare assembled PZ PNG and native Blockbench
model screenshots, preserve source SHA-256, build cards CSV README ZIP.
"""
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import csv,json,hashlib,zipfile,html,io
ROOT=Path(__file__).resolve().parents[1]
D=ROOT/"analysis/rosewood_furniture/2026-10-31"
PZ=D/"complete_furniture_visual_3d_v1"
B=D/"ten_batch_review"
N=B/"13_121_130/extra_decocraft_render"
OUT=B/"batch_121_130_v1"
DEC=ROOT/"scripts/rosewood_batch13_121_130_decisions.json"
SRC=D/"all_357_complete_native_comparisons_v1/ALL_357_FULL_RENDER_MATCHING.csv"
def rows(p):
 with p.open("r",encoding="utf-8-sig",newline="") as f:return list(csv.DictReader(f))
def writecsv(p,rs):
 assert rs
 with p.open("w",encoding="utf-8-sig",newline="") as f:
  w=csv.DictWriter(f,fieldnames=list(rs[0]),extrasaction="ignore");w.writeheader();w.writerows(rs)
def sha256(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def font(n):
 for x in ["/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc","/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"]:
  if Path(x).is_file():return ImageFont.truetype(x,n)
 return ImageFont.load_default()
def cropped(img):
 # Black Blockbench viewport is not the source model; crop its bright actual model pixels.
 import numpy as np
 a=np.array(img.convert("RGBA"))
 mask=(a[:,:,:3].max(axis=2)>12)&(a[:,:,3]>4)
 yy,xx=np.where(mask)
 if len(xx)>20:
  pad=12;img=img.crop((max(0,int(xx.min())-pad),max(0,int(yy.min())-pad),min(img.width,int(xx.max())+pad+1),min(img.height,int(yy.max())+pad+1)))
 return img.convert("RGBA")
def card(dec,o,images):
 im=Image.new("RGB",(1440,660),(247,249,252));d=ImageDraw.Draw(im)
 d.rounded_rectangle((12,43,708,527),radius=10,fill=(230,236,242))
 d.rounded_rectangle((730,43,1427,527),radius=10,fill=(233,239,245))
 d.text((22,8),f"{dec['index']:03d} {o['pz_name']} / {o['pz_style']}",font=font(22),fill=(33,54,75))
 d.text((24,54),"PROJECT ZOMBOID / B42 assembled original (provisional)",font=font(13),fill=(45,69,87))
 d.text((740,54),"MINECRAFT / verified source model in native Blockbench 5.2.2",font=font(13),fill=(45,69,87))
 with Image.open(PZ/o["pz_preview"]) as a:
  a=a.convert("RGBA");a.thumbnail((650,405),Image.Resampling.LANCZOS)
  im.paste(a,(int(360-a.width/2),int(299-a.height/2)),a)
 if images:
  w=625//len(images)
  for k,(label,p) in enumerate(images):
   with Image.open(p) as a:
    a=cropped(a);a.thumbnail((w-15,385),Image.Resampling.LANCZOS)
    x=int(735+k*w+w/2-a.width/2);y=int(294-a.height/2)
    im.paste(a,(x,y),a)
   d.text((740+k*w,478),label[:40],font=font(12),fill=(50,72,89))
 else:
  d.rounded_rectangle((769,154,1393,411),radius=12,outline=(148,81,75),width=3)
  d.text((806,240),"NO SOURCE-VERIFIED EQUIVALENT",font=font(19),fill=(145,74,66))
  d.text((805,283),"Do not auto-approve an unverified model",font=font(13),fill=(120,80,75))
 d.line((22,536,1417,536),fill=(179,190,200),width=2)
 d.text((24,545),f"PZ: {o['pz_parts']} sprite parts / {o['pz_grid']} footprint | {dec['size']}"[:165],font=font(12),fill=(47,69,85))
 d.text((24,573),("Proposal: "+(dec["candidate"] or "DEFER — no acceptable candidate")+" | inspected: "+",".join(dec["inspected_models"]))[:165],font=font(12),fill=(53,66,83))
 d.text((24,600),("REVIEW: "+dec["status"])[:160],font=font(13),fill=(143,73,65))
 d.text((24,636),"Native model comparison, NOT in-game placement, functional verification, or certified 1:1 match.",font=font(12),fill=(126,80,73))
 return im
def page(items):
 chunks=[]
 for x in items:
  title=f"{x['index']:03d} {x['pz_name']} / {x['pz_style']}"
  chunks.append(f'<article><img loading="lazy" src="{html.escape(x["card_path"],quote=True)}" alt="{html.escape(title,quote=True)}"><h2>{html.escape(title)}</h2><p><b>{html.escape(x["review_status"])}</b> — {html.escape(x["new_candidate_id"] or "보류")}</p><p>{html.escape(x["manual_review_reason"])}</p></article>')
 return '<!doctype html><html lang="ko"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Rosewood batch13 121-130</title><style>body{font:14px/1.55 system-ui;background:#eef2f6;color:#26384a;margin:20px auto;max-width:1250px}header{padding:20px}article{background:white;border-radius:12px;padding:12px;margin:16px 0}img{width:100%;height:auto}h2{font-size:18px}p{margin:8px 0}</style><header><h1>로즈우드 13차 — 111~120 원본 가구 모델 비교</h1><p>원본 모델 스크린샷만 사용. 1:1 및 인게임 배치 승인 0건.</p></header>'+''.join(chunks)+'</html>'
def main():
 assert not OUT.exists(),"Cannot overwrite an earlier review"
 allrows=rows(SRC)
 assert len(allrows)==357
 decisions=json.loads(DEC.read_text("utf8"))
 assert [x["index"] for x in decisions]==list(range(121,131))
 proofpath=N/"NATIVE_BLOCKBENCH_PROOF.json"
 proofs={x["id"]:x for x in json.loads(proofpath.read_text("utf8"))}
 (OUT/"cards").mkdir(parents=True)
 results=[]
 for dec in decisions:
  o=allrows[dec["index"]-1]
  assert int(o["index"])==dec["index"]
  shots=[];hashes=[];texhash=[];paths=[];details=[]
  for model in dec["inspected_models"]:
   evidence=proofs.get(model)
   if evidence and evidence.get("loaded_verified") and evidence.get("native_model_screenshot"):
    f=N/evidence["native_model_screenshot"]
    assert f.is_file()
    shots.append((model,f));hashes.append(evidence["source_sha256"]);texhash.append(evidence["variant_sha256"]);paths.append(str(f.relative_to(D)))
    details.append({"id":model,"source_model":evidence["source_model_path"],"source_texture":evidence["variant_texture_path"],"cubes":evidence.get("cubes"),"source_sha256":evidence["source_sha256"],"texture_sha256":evidence["variant_sha256"],"screenshot_sha256":sha256(f)})
  if dec["candidate"]:
   assert dec["candidate"].startswith("decocraft:") and dec["candidate"].split(":",1)[1] in [x[0] for x in shots],(dec["index"],dec["candidate"],[x[0] for x in shots])
  if dec["status"].startswith("CONDITIONAL"):assert shots
  name=f'cards/{dec["index"]:03d}_PZ_vs_MC.jpg'
  card(dec,o,shots).save(OUT/name,quality=88,optimize=True)
  pzfile=PZ/o["pz_preview"]
  results.append({"index":dec["index"],"pz_name":o["pz_name"],"pz_style":o["pz_style"],"pz_original_complete_preview":o["pz_preview"],"pz_preview_sha256":sha256(pzfile),"pz_parts":o["pz_parts"],"pz_footprint":o["pz_grid"],"pz_properties_json":o["pz_original_properties_json"],"previous_mc_candidate_id":o["chosen_mc_id"],"previous_match_needs_review":"YES","new_candidate_id":dec["candidate"],"secondary_candidate_id":dec["secondary"],"visually_inspected_model_ids":"|".join("decocraft:"+x[0] for x in shots),"native_source_model_sha256":"|".join(hashes),"native_source_variant_sha256":"|".join(texhash),"native_source_screenshot_paths":"|".join(paths),"native_model_provenance_json":json.dumps(details,ensure_ascii=False),"pz_shape_features":dec["shape"],"size_and_placement_notes":dec["size"],"review_status":dec["status"],"manual_review_reason":dec["why"],"followup_requirement":dec["followup"],"exact_1_to_1_visual_match_approved":"NO","approved_for_minecraft_world_replacement":"NO","card_path":name})
 writecsv(OUT/"BATCH_121_130_MANUAL_VISUAL_REVIEW.csv",results)
 deferred=[x for x in results if x["review_status"].startswith("DEFER")]
 writecsv(OUT/"BATCH_121_130_DEFERRED_OTHER_MODS.csv",deferred)
 alt=json.loads((ROOT/"scripts/rosewood_batch13_other_mod_research.json").read_text("utf8"))
 assert all(121<=int(x["index"])<=130 and x["visual_status"]=="NOT_DOWNLOADED_NOT_RENDERED" for x in alt)
 writecsv(OUT/"BATCH_121_130_OTHER_MOD_RESEARCH.csv",alt)
 # Standalone status overlay; never mutate the shared all-357 progress on parallel branches.
 state={"batch":"13","scope":"121-130","base":"work/rosewood-manual-batch10-091-100-20261101","previous_verified_scope":"001-100","this_scope_reviewed":[x["index"] for x in results],"conditional":[x["index"] for x in results if x["review_status"].startswith("CONDITIONAL")],"deferred":[x["index"] for x in deferred],"approved_for_world":[],"merged_into_global_progress":False}
 (OUT/"BATCH13_STANDALONE_PROGRESS.json").write_text(json.dumps(state,ensure_ascii=False,indent=2)+"\n",encoding="utf8")
 manifest={"scope":"121-130","total_pz_styles":357,"total_batches":36,"previous_batches_reviewed":10,"this_batch_reviewed":1,"individual_items_checked_this_batch":len(results),"unique_decocraft_models_rerendered":sum(bool(x.get("loaded_verified") and x.get("native_model_screenshot")) for x in proofs.values()),"attempted_decocraft_models":len(proofs),"native_model_pz_comparison_cards":len(results),"conditional_match_proposals":len(results)-len(deferred),"deferred_other_mod_or_vanilla_search":len(deferred),"exact_1_to_1_matches_certified":0,"minecraft_game_install_collision_verified":0,"source_tables_overwritten":False,"parallel_group_progress_overwritten":False,"alternative_mod_links_researched":len(alt),"alternative_mod_models_visually_verified":0}
 source_versions=json.loads((D/"minecraft_actual_mod_registry_v2/MOD_VERSION_SOURCES.json").read_text("utf8"))
 decocraft=next(x for x in source_versions if x["label"]=="decocraft")
 assert decocraft["minecraft"]=="1.20.1" and decocraft["loader"]=="forge"
 assert len(decocraft["sha512"])==128
 manifest.update({"source_mod_name":"Decocraft","source_mod_version":decocraft["version"],"source_mod_jar_sha512":decocraft["sha512"],"source_mod_version_url":"https://modrinth.com/mod/decocraft/version/"+decocraft["version_id"]})
 (OUT/"MANIFEST.json").write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+"\n",encoding="utf8")
 notes=["# 로즈우드 357종 — 13차 111~120번 원본 가구 개별 시각 검수",f"111~120 원본 PZ 가구 10종을 독립 검토. Decocraft JAR 원본 BBMODEL/텍스처 {len(proofs)}개 렌더 시도 중 {manifest['unique_decocraft_models_rerendered']}개 Blockbench 5.2.2 소스 이미지 성공. 실제 Minecraft 1.20.1 Forge 게임 설치/충돌/상호작용 테스트 및 1:1 최종 인증은 0건.",f"조건부 {manifest['conditional_match_proposals']}건, 보류 {len(deferred)}건. 11차 101~110 및 12차 111~120의 진행 CSV를 덮어쓰지 않기 위해 독립 JSON만 생성.","외부 모드 공식 호환성 자료 8건은 별도 CSV에 보존하며, 해당 모델의 3D 렌더·외형 검증이 완료된 것으로 간주하지 않음.","## 10종 검수 근거"]
 notes.append(f"검증된 모드 원본: Decocraft {decocraft['version']} Forge 1.20.1, JAR SHA-512: {decocraft['sha512']}, https://modrinth.com/mod/decocraft/version/{decocraft['version_id']}")
 for x in results:notes.append(f"### {x['index']:03d} {x['pz_name']} / {x['pz_style']}\n판정: {x['review_status']} / 제안: {x['new_candidate_id'] or '보류'}\n\n{x['manual_review_reason']}\n\n후속 검증: {x['followup_requirement']}\n\nPZ 이미지 SHA-256: `{x['pz_preview_sha256']}`\nMC 원본 모델 SHA-256: `{x['native_source_model_sha256'] or '해당 없음'}`")
 notes+=["## 출처·검증 범위","- PZ: 기존 B42 원본 Tiles PNG 및 TMX/.tiles 기반 조립 미리보기 (시각 조립은 잠정이며 인게임 모델이 아님)","- Minecraft: 검증된 Decocraft Forge 1.20.1 JAR에서 BBMODEL과 선택 텍스처를 읽어 원본 해시를 기록하고 Blockbench 5.2.2 데스크톱 화면 캡처","- 원본 모드 JAR, 텍스처 및 BBMODEL 자체는 재배포하지 않음. 비교 이미지·해시·출처만 보관.","- 실제 마인크래프트 설치 시 방향, 크기, 멀티블록, 충돌/상호작용은 별도 테스트 전까지 승인하지 않음.","## 파일","- cards/ : 111~120 원본 PZ 대 Minecraft 원본 모델 비교 10장","- BATCH_121_130_MANUAL_VISUAL_REVIEW.csv : 상세 10종 및 SHA-256","- BATCH_121_130_DEFERRED_OTHER_MODS.csv : 보류 후속 목록","- BATCH_121_130_OTHER_MOD_RESEARCH.csv : 공식 Forge 1.20.1 호환성 링크 (모델 미검증)","- BATCH13_STANDALONE_PROGRESS.json : 병렬 작업 충돌 방지 독립 진행 상태","- INDEX.html : 비교 이미지 열람기","- MANIFEST.json : 범위 및 검증 수치","- ROSEWOOD_BATCH_121_130_MANUAL_REVIEW.zip : 전체 결과"]
 (OUT/"README_KO.md").write_text("\n\n".join(notes)+"\n",encoding="utf8")
 (OUT/"INDEX.html").write_text(page(results),encoding="utf8")
 zpath=OUT/"ROSEWOOD_BATCH_121_130_MANUAL_REVIEW.zip"
 with zipfile.ZipFile(zpath,"w",zipfile.ZIP_DEFLATED,compresslevel=5) as z:
  for f in OUT.rglob("*"):
   if f.is_file() and f!=zpath:z.write(f,f.relative_to(OUT))
 with zipfile.ZipFile(zpath) as z:
  assert z.testzip() is None and len([x for x in z.namelist() if x.startswith("cards/") and x.endswith(".jpg")])==10
 print("BATCH13_VALIDATED",json.dumps(manifest,ensure_ascii=False),flush=True)
if __name__=="__main__":main()
