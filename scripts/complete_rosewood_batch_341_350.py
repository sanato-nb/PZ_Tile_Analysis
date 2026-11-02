#!/usr/bin/env python3
"""Independent image-based audit of Rosewood 341-350. Existing source-backed model screenshots only."""
from pathlib import Path
import csv, json, hashlib, zipfile, html, textwrap
from PIL import Image, ImageDraw, ImageFont, ImageOps
ROOT=Path(__file__).resolve().parents[1]
D=ROOT/"analysis/rosewood_furniture/2026-10-31"
BASE=D/"all_357_complete_native_comparisons_v1"
PZ=D/"complete_furniture_visual_3d_v1"
OUT=D/"ten_batch_review/batch_341_350_v1"
DEC=ROOT/"scripts/rosewood_batch32_341_350_decisions.json"
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
    assert [x["index"] for x in decisions]==list(range(341,351))
    assert sum(x["status"]=="CONDITIONAL" for x in decisions)==1
    assert sum(x["status"]=="DEFER" for x in decisions)==9
    with (BASE/"ALL_357_FULL_RENDER_MATCHING.csv").open(encoding="utf-8-sig",newline="") as f:
        source={int(r["index"]):r for r in csv.DictReader(f)}
    assert all(i in source for i in range(341,351))
    OUT.mkdir(parents=True,exist_ok=True);(OUT/"cards").mkdir(exist_ok=True)
    rows=[];deferred=[];evidence=[]
    allowed={"ACTUAL_NATIVE_BLOCKBENCH_SOURCE_BBMODEL","ACTUAL_NATIVE_BLOCKBENCH_FULL_SOURCE_JSON","NATIVE_BLOCKBENCH_PARTIAL_SOURCE_JSON","NO_REAL_MOD_ASSET","LEGACY_3D_APPROXIMATION"}
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
    csvwrite(OUT/"BATCH_341_350_MANUAL_VISUAL_REVIEW.csv",rows,list(rows[0]))
    csvwrite(OUT/"BATCH_341_350_DEFERRED_OTHER_MODS.csv",deferred,list(deferred[0]))
    csvwrite(OUT/"BATCH_341_350_SHA256_PROVENANCE.csv",evidence,list(evidence[0]))
    counts={g:sum(r["existing_model_render_grade"]==g for r in rows) for g in sorted(allowed)}
    assert all(r["exact_1_to_1_visual_match_approved"]=="NO" for r in rows)
    manifest={"scope":"341-350","lane":"A","total_pz_styles":357,
       "this_batch_individual_image_reviews":10,"new_comparison_cards":10,
       "conditional_candidates":1,"deferred_other_mods_or_vanilla":9,
       "fresh_native_blockbench_renders_this_run":0,
       "preexisting_source_render_grade_counts":counts,
       "prior_v3_recorded_decocraft_bbmodel_and_texture_hashes":0,
       "certified_1_to_1_matches":0,"minecraft_game_install_collision_verified":0,
       "source_tables_overwritten":False,"parallel_group_progress_overwritten":False,
       "review_method":"Independent visual comparison of 10 PZ previews against preexisting Minecraft source renders or explicitly missing/legacy evidence; annotated cards generated with Pillow.",
       "baseline_branch":"work/rosewood-manual-batch10-091-100-20261101",
       "limitations":["No new original mod BBMODEL opened in Blockbench this run.","342/343/344/347 have no source-verified Minecraft model; 345 has a partial JSON render and 349 a legacy approximation.","No Minecraft Forge 1.20.1 installation or collision/function testing.","Independent Draft PR; global progress not merged."]}
    (OUT/"MANIFEST.json").write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    (OUT/"BATCH32_STANDALONE_PROGRESS.json").write_text(json.dumps({"lane":"A","scope":"341-350","batch":"32","individually_reviewed":10,"merged_into_global_progress":False,"next_lane_A_scope":"complete"},ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    readme=[
       "# 로즈우드 가구 32차 — 341~350 독립 시각 검수","",
       "2026-11-02: PZ 완성형 원본 10종과 기존 Minecraft 모델 렌더/부재 표시를 개별 육안 대조. 원본 Blockbench 렌더를 새로 실행하지 않았으며 기존 증거를 재사용했다.","",
       "- 조건부 1종: 346 검정 그랜드 피아노 (동일 물체 종류이지만 뚜껑 닫힘/열림, 형태 비율, 2×3 설치 미확인).",
       "- 보류 9종: 341~345, 347~350. 342/343/344/347은 검증된 Minecraft 모델 부재, 345는 부분 JSON 렌더, 349는 레거시 근사 이미지.",
       "- 350 수제 단층 침대에 2층 침대가 매칭된 심각한 오매칭, 349 4×1 가로 세탁소 간판에 세로 버스정류장 표지판이 매칭된 문제를 확인.",
       "- Minecraft Forge 1.20.1 인게임 설치, 충돌·기능 및 정확한 1:1 승인: 0종.","",
       "## 증거 및 출처","",
       "- cards/: PZ 원본 PNG와 기존 Minecraft 비교 JPG를 바탕으로 생성한 판정 카드 10장",
       "- BATCH_341_350_MANUAL_VISUAL_REVIEW.csv: 10종 개별 판정, 재질/형태/멀티타일 관찰, 후속 검증",
       "- BATCH_341_350_DEFERRED_OTHER_MODS.csv: 보류 9종",
       "- BATCH_341_350_SHA256_PROVENANCE.csv: PZ PNG, 기존 비교 JPG, 새 JPG SHA-256. 기존 모델 해시가 있는 경우 재해시가 아닌 과거 기록임",
       "- MANIFEST.json, INDEX.html, ZIP: 독립 결과물",
       "- 원본 TMX/PNG/SQLite, 타 레인 작업, 기존 누적표는 변경하지 않음. Draft PR은 자동 병합하지 않음.","",
       "## 개별 판정",""]
    for r in rows: readme.append(f"- {int(r['index']):03d} {r['pz_name']} / {r['pz_style']} — {r['review_status']}: {r['manual_review_reason']}")
    (OUT/"README_KO.md").write_text("\n".join(readme)+"\n",encoding="utf-8")
    blocks=[]
    for r in rows:
        idx=int(r["index"])
        blocks.append(f'<article><h2>{idx:03d} {html.escape(r["pz_name"])} / {html.escape(r["pz_style"])} — {r["review_status"]}</h2><img src="cards/{idx:03d}_PZ_vs_MC.jpg" loading="lazy" width="100%"><p>{html.escape(r["manual_review_reason"])}</p></article>')
    (OUT/"INDEX.html").write_text(
        '<!doctype html><html lang="ko"><meta charset="utf-8"><title>Rosewood 341-350 manual review</title><style>body{max-width:1200px;margin:auto;font:16px sans-serif;background:#f5f7fa;color:#263444}article{background:white;padding:18px;margin:24px 0;border-radius:12px}img{height:auto}</style><h1>Rosewood 341–350 · lane A</h1><p>1 conditional, 9 deferred. Existing source render evidence only; no new native render or in-game certification.</p>'+"\n".join(blocks)+"</html>",encoding="utf-8")
    z=OUT/"ROSEWOOD_BATCH_341_350_MANUAL_REVIEW.zip"
    with zipfile.ZipFile(z,"w",compression=zipfile.ZIP_DEFLATED,compresslevel=7) as f:
        for p in sorted(OUT.rglob("*")):
            if p.is_file() and p!=z: f.write(p,p.relative_to(OUT).as_posix())
    with zipfile.ZipFile(z) as f:
        assert f.testzip() is None
        assert len([n for n in f.namelist() if n.startswith("cards/") and n.endswith(".jpg")])==10
    print("BATCH32_MANUAL_VISUAL_REVIEW_OK",json.dumps(manifest,ensure_ascii=False))
if __name__=="__main__": main()
