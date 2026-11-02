#!/usr/bin/env python3
"""Independent image-based audit of Rosewood 331-340. Existing source-backed model screenshots only."""
from pathlib import Path
import csv, json, hashlib, zipfile, html, textwrap
from PIL import Image, ImageDraw, ImageFont, ImageOps
ROOT=Path(__file__).resolve().parents[1]
D=ROOT/"analysis/rosewood_furniture/2026-10-31"
BASE=D/"all_357_complete_native_comparisons_v1"
PZ=D/"complete_furniture_visual_3d_v1"
OUT=D/"ten_batch_review/batch_331_340_v1"
DEC=ROOT/"scripts/rosewood_batch33_331_340_decisions.json"
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
    color=(37,100,72) if decision["decision"]=="CONDITIONAL" else (151,65,55)
    dr.line((18,565,1482,565),fill=(165,181,194),width=2)
    dr.text((28,580),"VISUAL VERDICT: "+decision["decision"],font=font(20,True),fill=color)
    dr.text((28,613),"Candidate: "+row["chosen_mc_id"],font=font(17),fill=(45,66,83))
    for j,line in enumerate(textwrap.wrap(row["pz_name"],width=100)[:2]):
        dr.text((28,646+j*22),line,font=font(16),fill=(62,71,81))
    dr.text((28,708),"Prior source render only; no fresh Blockbench, in-game installation, collision or 1:1 certification.",font=font(12),fill=(100,75,68))
    target=OUT/"cards"/f"{idx:03d}_PZ_vs_MC.jpg"
    out.save(target,format="JPEG",quality=90,subsampling=0,optimize=True)
    return target
def main():
    decisions=json.loads(DEC.read_text(encoding="utf-8"))["decisions"]
    assert [x["index"] for x in decisions]==list(range(331,341))
    assert sum(x["decision"]=="CONDITIONAL" for x in decisions)==1
    assert sum(x["decision"]=="DEFER" for x in decisions)==9
    with (BASE/"ALL_357_FULL_RENDER_MATCHING.csv").open(encoding="utf-8-sig",newline="") as f:
        source={int(r["index"]):r for r in csv.DictReader(f)}
    assert all(i in source for i in range(331,341))
    OUT.mkdir(parents=True,exist_ok=True);(OUT/"cards").mkdir(exist_ok=True)
    rows=[];deferred=[];evidence=[]
    allowed={"ACTUAL_NATIVE_BLOCKBENCH_SOURCE_BBMODEL","ACTUAL_NATIVE_BLOCKBENCH_FULL_SOURCE_JSON","NATIVE_BLOCKBENCH_PARTIAL_SOURCE_JSON","NO_REAL_MOD_ASSET"}
    for d in decisions:
        idx=d["index"];r=source[idx]
        assert idx in source
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
          "review_status":d["decision"],"manual_review_reason":d["reason"],
          "pz_shape_features":d["pz_shape"],"followup_requirement":d["next_action"],
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
        if d["decision"]=="DEFER":
            deferred.append({k:row[k] for k in ("index","pz_name","pz_style","previous_mc_candidate_id","manual_review_reason","followup_requirement")})
    csvwrite(OUT/"BATCH_331_340_MANUAL_VISUAL_REVIEW.csv",rows,list(rows[0]))
    csvwrite(OUT/"BATCH_331_340_DEFERRED_OTHER_MODS.csv",deferred,list(deferred[0]))
    csvwrite(OUT/"BATCH_331_340_SHA256_PROVENANCE.csv",evidence,list(evidence[0]))
    counts={g:sum(r["existing_model_render_grade"]==g for r in rows) for g in sorted(allowed)}
    assert all(r["exact_1_to_1_visual_match_approved"]=="NO" for r in rows)
    manifest={"scope":"331-340","lane":"C","total_pz_styles":357,
       "this_batch_individual_image_reviews":10,"new_comparison_cards":10,
       "conditional_candidates":1,"deferred_other_mods_or_vanilla":9,
       "fresh_native_blockbench_renders_this_run":0,
       "preexisting_source_render_grade_counts":counts,
       "prior_v3_recorded_decocraft_bbmodel_and_texture_hashes":0,
       "certified_1_to_1_matches":0,"minecraft_game_install_collision_verified":0,
       "source_tables_overwritten":False,"parallel_group_progress_overwritten":False,
       "review_method":"Independent visual comparison of PZ previews against preexisting Minecraft Blockbench/JSON screenshot evidence; annotated cards generated with Pillow.",
       "baseline_branch":"work/rosewood-manual-batch10-091-100-20261101",
       "limitations":["No fresh Blockbench model render this run.","334 and 335 are partial JSON renders; 336 has extra crib mobile and unverified footprint.","No Minecraft Forge 1.20.1 installation or collision/function testing.","Independent Draft PR; global progress not merged."]}
    (OUT/"MANIFEST.json").write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    (OUT/"BATCH33_STANDALONE_PROGRESS.json").write_text(json.dumps({"lane":"C","scope":"331-340","batch":"30","individually_reviewed":10,"merged_into_global_progress":False,"next_lane_C_scope":"final_index_and_integrity_QA"},ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    readme=[
      "# 로즈우드 가구 C 레인 — 331~340 독립 시각 검수","",
      "PZ 완성형 10종과 기존 소스 기반 Minecraft 비교 이미지 10종을 직접 판독했다. 새 Blockbench 렌더는 없으며 게임 설치 인증은 0건이다.","",
      "- 331~332: 낮은 2단 밝은 오픈 선반에 짙은 아카시아 상자형 선반이 잘못 대응.",
      "- 333: 4×1 목재 3단 상점 선반을 1×1 닫힌 상자형 모델로 매칭.",
      "- 334: 길고 가는 목재 벤치에 스툴의 평판 부분 렌더만 존재.",
      "- 335: 1×2 금속 부검대/수도꼭지에 아카시아 유리 탁자의 평판 부분 렌더만 존재.",
      "- 336: 참나무 아기 침대와 Decocraft crib_oak는 난간과 형태가 유사해 조건부. 상부 모빌 추가·크기·점유·기능 미검증.",
      "- 337~338: 줄무늬/크림색 곡선 빅토리아 소파와 검정 직각 소파 오매칭.",
      "- 339~340: 나무/금속 벽걸이 코너 상부장에 검정·은색 바닥형 다이너 카운터 오매칭.",
      "- 조건부 1종, 보류 9종, Forge 1.20.1 설치·충돌·기능 검증 0종.","",
      "## 근거와 한계","",
      "- PZ 원본 미리보기 10개와 기존 실제 소스 기반 Minecraft 렌더 10개를 사용해 비교 JPG를 생성한다.",
      "- baseline source_model_sha256은 이전 기록의 값으로, 이번에 모델 원본을 재해시하지 않았다.",
      "- PZ 원본, baseline JPG, 새 JPG의 SHA-256은 이번 실행에서 파일 바이트로 계산한다.",
      "- 부분 JSON 렌더는 완전한 외형 인증 근거로 사용하지 않는다.",
      "- 원본 TMX·PNG·SQLite, 다른 레인 브랜치와 전체 누적 진행표는 수정하지 않는다.",
      "- Draft PR을 자동 병합하지 않는다.","",
      "## 개별 판정",""]
    for r in rows: readme.append(f"- {int(r['index']):03d} {r['pz_name']} / {r['pz_style']} — {r['review_status']}: {r['manual_review_reason']}")
    (OUT/"README_KO.md").write_text("\n".join(readme)+"\n",encoding="utf-8")
    blocks=[]
    for r in rows:
        idx=int(r["index"])
        blocks.append(f'<article><h2>{idx:03d} {html.escape(r["pz_name"])} / {html.escape(r["pz_style"])} — {r["review_status"]}</h2><img src="cards/{idx:03d}_PZ_vs_MC.jpg" loading="lazy" width="100%"><p>{html.escape(r["manual_review_reason"])}</p></article>')
    (OUT/"INDEX.html").write_text(
        '<!doctype html><html lang="ko"><meta charset="utf-8"><title>Rosewood 331-340 manual review</title><style>body{max-width:1200px;margin:auto;font:16px sans-serif;background:#f5f7fa;color:#263444}article{background:white;padding:18px;margin:24px 0;border-radius:12px}img{height:auto}</style><h1>Rosewood 301–310 · lane A</h1><p>1 conditional, 9 deferred. Existing source render evidence only; no new native render or in-game certification.</p>'+"\n".join(blocks)+"</html>",encoding="utf-8")
    z=OUT/"ROSEWOOD_BATCH_331_340_MANUAL_REVIEW.zip"
    with zipfile.ZipFile(z,"w",compression=zipfile.ZIP_DEFLATED,compresslevel=7) as f:
        for p in sorted(OUT.rglob("*")):
            if p.is_file() and p!=z: f.write(p,p.relative_to(OUT).as_posix())
    with zipfile.ZipFile(z) as f:
        assert f.testzip() is None
        assert len([n for n in f.namelist() if n.startswith("cards/") and n.endswith(".jpg")])==10
    print("BATCH33_MANUAL_VISUAL_REVIEW_OK",json.dumps(manifest,ensure_ascii=False))
if __name__=="__main__": main()
