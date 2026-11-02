#!/usr/bin/env python3
"""Independent image-based audit of Rosewood 251-260. Existing source-backed model screenshots only."""
from pathlib import Path
import csv, json, hashlib, zipfile, html, textwrap
from PIL import Image, ImageDraw, ImageFont, ImageOps
ROOT=Path(__file__).resolve().parents[1]
D=ROOT/"analysis/rosewood_furniture/2026-10-31"
BASE=D/"all_357_complete_native_comparisons_v1"
PZ=D/"complete_furniture_visual_3d_v1"
OUT=D/"ten_batch_review/batch_251_260_v1"
DEC=ROOT/"scripts/rosewood_batch23_251_260_decisions.json"
def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def font(sz,bold=False):
    paths=["/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
           "/usr/share/fonts/truetype/liberation2/LiberationSans-Regular.ttf"]
    for p in paths:
        if Path(p).is_file(): return ImageFont.truetype(p,sz)
    return ImageFont.load_default()
def csvwrite(path,rows,fields):
    with path.open("w",encoding="utf-8-sig",newline="") as f:
        w=csv.DictWriter(f,fieldnames=fields,extrasaction="ignore")
        w.writeheader();w.writerows(rows)
def build_card(row,decision,src_card,pz_file):
    idx=int(row["index"])
    out=Image.new("RGB",(1500,740),(246,249,252))
    dr=ImageDraw.Draw(out)
    dr.text((24,18),f"{idx:03d}  {row['pz_name']} / {row['pz_style']}",font=font(25,True),fill=(28,48,65))
    for x in (18,766): dr.rounded_rectangle((x,65,x+716,550),radius=14,fill=(226,235,242))
    dr.text((34,82),"PROJECT ZOMBOID | original assembled preview",font=font(16),fill=(46,66,81))
    dr.text((780,82),"MINECRAFT | previously captured source model",font=font(15),fill=(46,66,81))
    with Image.open(pz_file) as p:
        p=p.convert("RGBA");p=ImageOps.contain(p,(650,415),Image.Resampling.LANCZOS)
        out.paste(p,(376-p.width//2,326-p.height//2),p)
    with Image.open(src_card) as b:
        b=b.convert("RGB")
        mc=b.crop((max(0,b.width//2+8),110,b.width-17,max(113,b.height-122)))
        mc=ImageOps.contain(mc,(655,420),Image.Resampling.LANCZOS)
        out.paste(mc,(1124-mc.width//2,329-mc.height//2))
    dr=ImageDraw.Draw(out)
    color=(37,100,72) if decision["status"]=="CONDITIONAL" else (151,65,55)
    dr.line((18,565,1482,565),fill=(165,181,194),width=2)
    dr.text((28,580),"VISUAL VERDICT: "+decision["status"],font=font(20,True),fill=color)
    dr.text((28,613),"Candidate: "+decision["candidate"],font=font(17),fill=(45,66,83))
    for j,line in enumerate(textwrap.wrap(decision["short"],width=100)[:2]):
        dr.text((28,646+j*22),line,font=font(16),fill=(62,71,81))
    dr.text((28,708),"Prior source render only; no fresh Blockbench, in-game installation, collision or 1:1 certification.",font=font(12),fill=(100,75,68))
    target=OUT/"cards"/f"{idx:03d}_PZ_vs_MC.jpg"
    out.save(target,format="JPEG",quality=90,subsampling=0,optimize=True)
    return target
def main():
    decisions=json.loads(DEC.read_text(encoding="utf-8"))["decisions"]
    assert [x["index"] for x in decisions]==list(range(251,261))
    assert sum(x["status"]=="CONDITIONAL" for x in decisions)==2
    assert sum(x["status"]=="DEFER" for x in decisions)==8
    with (BASE/"ALL_357_FULL_RENDER_MATCHING.csv").open(encoding="utf-8-sig",newline="") as f:
        source={int(r["index"]):r for r in csv.DictReader(f)}
    assert all(i in source for i in range(251,261))
    OUT.mkdir(parents=True,exist_ok=True);(OUT/"cards").mkdir(exist_ok=True)
    rows=[];deferred=[];evidence=[]
    allowed={"ACTUAL_NATIVE_BLOCKBENCH_SOURCE_BBMODEL","ACTUAL_NATIVE_BLOCKBENCH_FULL_SOURCE_JSON","NATIVE_BLOCKBENCH_PARTIAL_SOURCE_JSON"}
    for d in decisions:
        idx=d["index"];r=source[idx]
        assert r["chosen_mc_id"]==d["candidate"],(idx,r["chosen_mc_id"])
        original=BASE/r["card_path"];pz=PZ/r["pz_preview"]
        assert original.is_file() and pz.is_file(),(original,pz)
        grade=r["render_grade"];assert grade in allowed,(idx,grade)
        mcmeta=json.loads(r.get("mc_import_evidence_json") or "{}")
        card=build_card(r,d,original,pz)
        assert card.stat().st_size>10000
        row={
          "index":idx,"pz_name":r["pz_name"],"pz_style":r["pz_style"],
          "pz_parts":r["pz_parts"],"pz_footprint":r["pz_grid"],
          "pz_preview_path":r["pz_preview"],"pz_preview_sha256":sha(pz),
          "previous_mc_candidate_id":r["chosen_mc_id"],
          "review_status":d["status"],"manual_review_reason":d["why"],
          "pz_shape_features":d["shape"],"followup_requirement":d["followup"],
          "existing_model_render_grade":grade,
          "source_model_paths_from_baseline":" | ".join(mcmeta.get("source_models",[])),
          "source_model_sha256_from_baseline":mcmeta.get("source_model_sha256",""),
          "prior_v3_decocraft_bbmodel_path":d.get("prior_v3_source_bbmodel_path",""),
          "prior_v3_decocraft_texture_path":d.get("prior_v3_source_texture_path",""),
          "prior_v3_decocraft_bbmodel_sha256":d.get("prior_v3_source_bbmodel_sha256",""),
          "prior_v3_decocraft_texture_sha256":d.get("prior_v3_source_texture_sha256",""),
          "baseline_comparison_path":r["card_path"],"baseline_comparison_sha256":sha(original),
          "new_comparison_card_path":f"cards/{idx:03d}_PZ_vs_MC.jpg",
          "new_comparison_card_sha256":sha(card),
          "fresh_native_blockbench_render_this_run":"NO",
          "exact_1_to_1_visual_match_approved":"NO",
          "approved_for_minecraft_world_replacement":"NO",
          "game_install_collision_function_verified":"NO"}
        rows.append(row)
        evidence.append({k:row[k] for k in ("index","pz_preview_path","pz_preview_sha256","baseline_comparison_path","baseline_comparison_sha256","existing_model_render_grade","source_model_paths_from_baseline","source_model_sha256_from_baseline","prior_v3_decocraft_bbmodel_path","prior_v3_decocraft_texture_path","prior_v3_decocraft_bbmodel_sha256","prior_v3_decocraft_texture_sha256","new_comparison_card_path","new_comparison_card_sha256")})
        if d["status"]=="DEFER":
            deferred.append({k:row[k] for k in ("index","pz_name","pz_style","previous_mc_candidate_id","manual_review_reason","followup_requirement")})
    csvwrite(OUT/"BATCH_251_260_MANUAL_VISUAL_REVIEW.csv",rows,list(rows[0]))
    csvwrite(OUT/"BATCH_251_260_DEFERRED_OTHER_MODS.csv",deferred,list(deferred[0]))
    csvwrite(OUT/"BATCH_251_260_SHA256_PROVENANCE.csv",evidence,list(evidence[0]))
    counts={g:sum(r["existing_model_render_grade"]==g for r in rows) for g in sorted(allowed)}
    assert sum(len(r["prior_v3_decocraft_bbmodel_sha256"])==64 and len(r["prior_v3_decocraft_texture_sha256"])==64 for r in rows)==4
    manifest={"scope":"251-260","lane":"A","total_pz_styles":357,
       "this_batch_individual_image_reviews":10,"new_comparison_cards":10,
       "conditional_candidates":2,"deferred_other_mods_or_vanilla":8,
       "fresh_native_blockbench_renders_this_run":0,
       "preexisting_source_render_grade_counts":counts,
       "prior_v3_recorded_decocraft_bbmodel_and_texture_hashes":4,
       "certified_1_to_1_matches":0,"minecraft_game_install_collision_verified":0,
       "source_tables_overwritten":False,"parallel_group_progress_overwritten":False,
       "review_method":"Independent visual comparison of PZ previews against preexisting Minecraft Blockbench/JSON screenshot evidence; annotated cards generated with Pillow.",
       "baseline_branch":"work/rosewood-manual-batch10-091-100-20261101",
       "limitations":["No new original mod BBMODEL opened in Blockbench this run.","Two existing source JSON screenshots are partial.","No Minecraft Forge 1.20.1 installation or collision/function testing.","Independent Draft PR; global progress not merged."]}
    (OUT/"MANIFEST.json").write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    (OUT/"BATCH23_STANDALONE_PROGRESS.json").write_text(json.dumps({"lane":"A","scope":"251-260","batch":"23","individually_reviewed":10,"merged_into_global_progress":False,"next_lane_A_scope":"281-290"},ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    readme=[
       "# 로즈우드 가구 23차 — 251~260 독립 시각 검수","",
       "원본 PZ 완성형 미리보기 10종과 기존 저장소의 Minecraft 원본 소스 기반 Blockbench/JSON 비교 이미지를 이번 실행에서 개별 시각 대조했다.",
       "이번 실행은 기존 렌더 이미지를 재사용했다. Blockbench를 새로 실행하거나 원본 모델을 새로 렌더링했다고 주장하지 않는다.","",
       "- 조건부: 253 청색 냉장고, 254 적색 냉장고 (색상·문 분할·손잡이 불일치).",
       "- 보류: 251, 252, 255~260 (8종).",
       "- 252·260은 기존 JSON 렌더가 부분적이므로 완성 모델 확인 불가.",
       "- 255·259·260은 PZ 다중 타일 조립 구조를 후보 1블록/불완전 모델이 재현하지 못함.",
       "- 실제 Minecraft Java 1.20.1 Forge 설치, 기능, 충돌, 정확한 1:1 승인: 0종.","",
       "## 증거","",
       "- cards/: 원본 PZ 미리보기와 기존 Minecraft 원본 소스 비교 이미지에서 새로 구성한 판정 카드 10장",
       "- BATCH_251_260_MANUAL_VISUAL_REVIEW.csv: 개별 외형·색상·재질·조립/기능 한계 및 후속 조건",
       "- BATCH_251_260_DEFERRED_OTHER_MODS.csv: 보류 8종과 대체 모드 재검색 요구",
       "- BATCH_251_260_SHA256_PROVENANCE.csv: 원본 PZ 이미지·기존 비교 카드·새 카드의 SHA-256 및 과거 v3에서 기록된 Decocraft 원본 BBMODEL/텍스처 SHA-256 (이번 실행에서 재해시한 값 아님)",
       "- MANIFEST.json, INDEX.html, ZIP: 독립 검수 결과와 검증 가능 파일 묶음","",
       "기존 기준 브랜치 원본 PNG/TMX/SQLite/357종 누적표, 다른 레인 결과는 변경하지 않았다. Draft PR을 자동 병합하지 않는다.","",
       "## 개별 판정",""]
    for r in rows: readme.append(f"- {int(r['index']):03d} {r['pz_name']} / {r['pz_style']} — {r['review_status']}: {r['manual_review_reason']}")
    (OUT/"README_KO.md").write_text("\n".join(readme)+"\n",encoding="utf-8")
    blocks=[]
    for r in rows:
        idx=int(r["index"])
        blocks.append(f'<article><h2>{idx:03d} {html.escape(r["pz_name"])} / {html.escape(r["pz_style"])} — {r["review_status"]}</h2><img src="cards/{idx:03d}_PZ_vs_MC.jpg" loading="lazy" width="100%"><p>{html.escape(r["manual_review_reason"])}</p></article>')
    (OUT/"INDEX.html").write_text(
        '<!doctype html><html lang="ko"><meta charset="utf-8"><title>Rosewood 251-260 manual review</title><style>body{max-width:1200px;margin:auto;font:16px sans-serif;background:#f5f7fa;color:#263444}article{background:white;padding:18px;margin:24px 0;border-radius:12px}img{height:auto}</style><h1>Rosewood 251–260 · lane A</h1><p>2 conditional, 8 deferred. Existing source render evidence only; no new native render or in-game certification.</p>'+"\n".join(blocks)+"</html>",encoding="utf-8")
    z=OUT/"ROSEWOOD_BATCH_251_260_MANUAL_REVIEW.zip"
    with zipfile.ZipFile(z,"w",compression=zipfile.ZIP_DEFLATED,compresslevel=7) as f:
        for p in sorted(OUT.rglob("*")):
            if p.is_file() and p!=z: f.write(p,p.relative_to(OUT).as_posix())
    with zipfile.ZipFile(z) as f:
        assert f.testzip() is None
        assert len([n for n in f.namelist() if n.startswith("cards/") and n.endswith(".jpg")])==10
    print("BATCH23_MANUAL_VISUAL_REVIEW_OK",json.dumps(manifest,ensure_ascii=False))
if __name__=="__main__": main()
