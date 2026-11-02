#!/usr/bin/env python3
"""Independent visual review 321-330 using preexisting PZ and native-source MC screenshots.
No new Blockbench or Minecraft in-game validation is claimed.
"""
from pathlib import Path
import csv
import hashlib
import html
import json
import textwrap
import zipfile
from PIL import Image, ImageDraw, ImageFont, ImageOps

ROOT = Path(__file__).resolve().parents[1]
BASE_DIR = ROOT / "analysis/rosewood_furniture/2026-10-31"
SOURCE = BASE_DIR / "all_357_complete_native_comparisons_v1"
PZ_DIR = BASE_DIR / "complete_furniture_visual_3d_v1"
OUT = BASE_DIR / "ten_batch_review/batch_321_330_v1"
DECISIONS = ROOT / "scripts/rosewood_batch33_321_330_decisions.json"

def sha256(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()

def git_sha1(path):
    data = Path(path).read_bytes()
    return hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()

def font(size, bold=False):
    names = ["/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
             "/usr/share/fonts/truetype/liberation2/LiberationSans-Regular.ttf"]
    for name in names:
        if Path(name).is_file():
            return ImageFont.truetype(name, size)
    return ImageFont.load_default()

def write_csv(path, rows, fields):
    with path.open("w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fields, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)

def make_card(r, decision, original, pz_path):
    index = int(r["index"])
    result = Image.new("RGB", (1500, 780), (246, 249, 252))
    draw = ImageDraw.Draw(result)
    draw.text((28, 17), f"{index:03d}  {r['pz_name']} / {r['pz_style']}", font=font(26, True), fill=(29, 47, 65))
    draw.rounded_rectangle((18, 67, 734, 575), radius=13, fill=(225, 234, 241))
    draw.rounded_rectangle((766, 67, 1482, 575), radius=13, fill=(225, 234, 241))
    draw.text((36, 84), "PROJECT ZOMBOID  |  provisional assembled preview", font=font(15), fill=(43, 65, 80))
    draw.text((784, 84), "MINECRAFT  |  preexisting source-based render", font=font(15), fill=(43, 65, 80))
    with Image.open(pz_path) as p:
        p = p.convert("RGBA")
        if p.width > 100 and p.height > 180:
            p = p.crop((14, 76, p.width - 14, p.height - 51))
        p = ImageOps.contain(p, (660, 435), Image.Resampling.LANCZOS)
        result.paste(p, (376 - p.width // 2, 338 - p.height // 2), p)
    with Image.open(original) as m:
        m = m.convert("RGB")
        m = m.crop((m.width // 2 + 18, 84, m.width - 25, m.height - 109))
        m = ImageOps.contain(m, (660, 435), Image.Resampling.LANCZOS)
        result.paste(m, (1124 - m.width // 2, 339 - m.height // 2))
    draw = ImageDraw.Draw(result)
    draw.line((18, 588, 1482, 588), fill=(160, 180, 195), width=2)
    draw.text((29, 605), "VISUAL VERDICT: DEFER / NOT APPROVED", font=font(23, True), fill=(146, 62, 53))
    draw.text((29, 647), "Prior candidate: " + (decision["candidate"] or "NO VERIFIED MODEL"), font=font(17), fill=(43, 65, 82))
    for j, line in enumerate(textwrap.wrap(decision["short"], 102)[:2]):
        draw.text((29, 680 + j * 23), line, font=font(17), fill=(55, 67, 81))
    draw.text((29, 746), "Existing screenshots only; NO fresh Blockbench, in-game test, or 1:1 certification.", font=font(14), fill=(111, 73, 66))
    output = OUT / "cards" / f"{index:03d}_PZ_vs_MC.jpg"
    result.save(output, "JPEG", quality=91, optimize=True, subsampling=0)
    return output

def main():
    info = json.loads(DECISIONS.read_text(encoding="utf-8"))
    decisions = info["decisions"]
    assert info["scope"] == "321-330" and info["lane"] == "B"
    assert [x["index"] for x in decisions] == list(range(321, 331))
    assert len({x["index"] for x in decisions}) == 10
    assert all(x["status"] == "DEFER" for x in decisions)
    with (SOURCE / "ALL_357_FULL_RENDER_MATCHING.csv").open(encoding="utf-8-sig", newline="") as f:
        source = {int(r["index"]): r for r in csv.DictReader(f)}
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "cards").mkdir(exist_ok=True)
    reviews, deferred, evidence = [], [], []
    for decision in decisions:
        index = decision["index"]
        r = source[index]
        assert r["chosen_mc_id"] == decision["candidate"], (index, r["chosen_mc_id"], decision["candidate"])
        pz = PZ_DIR / r["pz_preview"]
        original = SOURCE / r["card_path"]
        assert pz.is_file() and original.is_file(), (index, pz, original)
        card = make_card(r, decision, original, pz)
        assert card.stat().st_size > 10000
        meta = json.loads(r.get("mc_import_evidence_json") or "{}")
        row = {
            "index": index,
            "pz_name": r["pz_name"],
            "pz_style": r["pz_style"],
            "pz_parts": r["pz_parts"],
            "pz_footprint": r["pz_grid"],
            "pz_shape_features_observed": decision["shape"],
            "previous_mc_candidate_id": decision["candidate"],
            "manual_review_status": "DEFER",
            "manual_visual_reason": decision["why"],
            "followup_other_mods_or_vanilla": decision["followup"],
            "previous_model_render_grade": r["render_grade"],
            "baseline_source_model_paths": " | ".join(meta.get("source_models", [])),
            "baseline_model_sha256_if_recorded": meta.get("source_model_sha256", ""),
            "pz_preview_path": r["pz_preview"],
            "pz_preview_sha256": sha256(pz),
            "pz_preview_git_blob_sha1": git_sha1(pz),
            "baseline_comparison_path": r["card_path"],
            "baseline_comparison_sha256": sha256(original),
            "baseline_comparison_git_blob_sha1": git_sha1(original),
            "new_comparison_card_path": f"cards/{index:03d}_PZ_vs_MC.jpg",
            "new_comparison_card_sha256": sha256(card),
            "fresh_native_blockbench_render_this_run": "NO",
            "exact_1_to_1_visual_match_approved": "NO",
            "approved_for_minecraft_world_replacement": "NO",
            "game_install_collision_function_verified": "NO",
        }
        reviews.append(row)
        deferred.append({k: row[k] for k in (
            "index", "pz_name", "pz_style", "previous_mc_candidate_id",
            "manual_visual_reason", "followup_other_mods_or_vanilla")})
        evidence.append({k: row[k] for k in (
            "index", "pz_preview_path", "pz_preview_sha256", "pz_preview_git_blob_sha1",
            "baseline_comparison_path", "baseline_comparison_sha256",
            "baseline_comparison_git_blob_sha1", "previous_model_render_grade",
            "baseline_source_model_paths", "baseline_model_sha256_if_recorded",
            "new_comparison_card_path", "new_comparison_card_sha256")})
    write_csv(OUT / "BATCH_321_330_MANUAL_VISUAL_REVIEW.csv", reviews, list(reviews[0]))
    write_csv(OUT / "BATCH_321_330_DEFERRED_OTHER_MODS.csv", deferred, list(deferred[0]))
    write_csv(OUT / "SOURCE_SHA256.csv", evidence, list(evidence[0]))
    grades = {grade: sum(r["previous_model_render_grade"] == grade for r in reviews)
              for grade in sorted({r["previous_model_render_grade"] for r in reviews})}
    manifest = {
        "scope": "321-330", "lane": "B", "total_pz_styles": 357,
        "this_batch_individual_image_reviews": 10, "new_comparison_cards": 10,
        "conditional_candidates": 0, "deferred_other_mods_or_vanilla": 10,
        "fresh_native_blockbench_renders_this_run": 0,
        "preexisting_source_render_grade_counts": grades,
        "certified_1_to_1_matches": 0,
        "minecraft_game_install_collision_verified": 0,
        "source_tables_overwritten": False,
        "parallel_group_progress_overwritten": False,
        "merged_into_global_progress": False,
        "baseline_branch": "work/rosewood-manual-batch10-091-100-20261101",
        "review_method": "Assistant visually inspected ten baseline PZ/MC cards 321-330 and annotated ten new cards. Existing source-backed renders reused; no new Blockbench run.",
        "limitations": [
            "PZ 321 has 3x1 SpriteGridPos; other provisional 1x1 footprints and rotations require verification.",
            "323 shows an incomplete native JSON model import; not proof of complete 3D geometry.",
            "322 has no verified Minecraft source model; placeholder is not an actual render.",
            "No fresh native BBMODEL or texture rendering in this run.",
            "No Minecraft Java 1.20.1 Forge installation, collision, interaction, multi-tile placement or 1:1 certification.",
            "This is an independent draft PR, not a global merge."
        ]
    }
    (OUT / "MANIFEST.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (OUT / "BATCH33_STANDALONE_PROGRESS.json").write_text(json.dumps({
        "lane": "B", "scope": "321-330", "batch": 33, "individually_reviewed": 10,
        "conditional": 0, "deferred": 10, "merged_into_global_progress": False,
        "next_lane_B_scope": "351-357"}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    readme = [
        "# 로즈우드 B 레인 33차 — 321~330 개별 시각 검수", "",
        "PZ 원본 완성형 조립 미리보기 10종과 기존 Minecraft 원본 소스 기반 비교 JPG 10개를 실제로 열어 각각 관찰했다.",
        "이번 실행에서 Blockbench를 새로 구동한 것은 아니며, 기존 원본 소스 기반 렌더를 재사용했다.",
        "원본 PZ 미리보기는 임시 조립 상태일 수 있어 구조적 불일치 판정의 제한을 함께 기록한다.", "",
        "- 개별 검수 10종 / 조건부 0종 / 보류 10종 / 1:1 인증 0종.",
        "- 323번의 Minecraft JSON 스크린샷은 부분 렌더이므로 완성 모델의 외형 증거로 승인하지 않는다.",
        "- 322에는 검증된 MC 모델이 없으며 우측은 안내 카드이므로 실제 모델 비교가 아니다.",
        "- 325·326·327은 서로 다른 색상의 L자 코너 카운터인데 동일한 검정·은색 줄무늬 카운터가 후보로 지정돼 있다.",
        "- Minecraft Forge 1.20.1 설치·충돌·방향·기능 검증은 수행되지 않았다.", "",
        "## 검증 자료", "",
        "- cards/: 기존 이미지로부터 새로 제작한 개별 좌우 비교 JPG 10장.",
        "- BATCH_321_330_MANUAL_VISUAL_REVIEW.csv: 10개 외형·재질·색상·구조·점유·한계 판정.",
        "- BATCH_321_330_DEFERRED_OTHER_MODS.csv: 다른 모드 또는 바닐라 재검색 대상 10종.",
        "- SOURCE_SHA256.csv: PZ PNG, 기존 MC 비교 JPG, 새 JPG의 SHA-256 및 기존 Git blob SHA-1.",
        "- MANIFEST.json / BATCH33_STANDALONE_PROGRESS.json / INDEX.html / ZIP / ZIP_SHA256.txt.",
        "- 원본 TMX, PNG, SQLite, 357종 전체 표, 다른 레인의 브랜치는 수정하지 않았다.",
        "- 별도 Draft PR이며 임의 병합하지 않는다.", "", "## 개별 관찰", ""
    ]
    for r in reviews:
        readme.append(f"- {int(r['index']):03d} {r['pz_name']} / {r['pz_style']} ↔ {r['previous_mc_candidate_id']}: {r['manual_visual_reason']}")
    (OUT / "README_KO.md").write_text("\n".join(readme) + "\n", encoding="utf-8")
    sections = []
    for r in reviews:
        index = int(r["index"])
        sections.append(
            f'<article><h2>{index:03d} {html.escape(r["pz_name"])} / {html.escape(r["pz_style"])} — DEFER</h2>'
            f'<img src="cards/{index:03d}_PZ_vs_MC.jpg" width="100%" loading="lazy">'
            f'<p>{html.escape(r["manual_visual_reason"])}</p></article>')
    (OUT / "INDEX.html").write_text(
        '<!doctype html><html lang="ko"><meta charset="utf-8"><title>Rosewood 321–330 visual review</title>'
        '<style>body{max-width:1200px;margin:auto;font:16px sans-serif;background:#f5f7fa;color:#263444}'
        'article{background:white;padding:18px;margin:24px 0;border-radius:12px}img{height:auto}</style>'
        '<h1>Rosewood 321–330 · Lane B</h1><p>10 deferred. Prior source screenshots only; no new native render or in-game certification.</p>'
        + "\n".join(sections) + "</html>\n", encoding="utf-8")
    archive = OUT / "ROSEWOOD_BATCH_321_330_MANUAL_REVIEW.zip"
    with zipfile.ZipFile(archive, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=7) as z:
        for path in sorted(OUT.rglob("*")):
            if path.is_file() and path != archive and path.name != "ZIP_SHA256.txt":
                z.write(path, path.relative_to(OUT).as_posix())
    with zipfile.ZipFile(archive) as z:
        assert z.testzip() is None
        assert len([x for x in z.namelist() if x.startswith("cards/") and x.endswith(".jpg")]) == 10
    (OUT / "ZIP_SHA256.txt").write_text(sha256(archive) + "  " + archive.name + "\n", encoding="utf-8")
    print("ROSEWOOD_321_330_GENERATED", json.dumps(manifest, ensure_ascii=False))
if __name__ == "__main__":
    main()
