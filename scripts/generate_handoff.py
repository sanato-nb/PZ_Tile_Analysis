#!/usr/bin/env python3
"""Update bounded auto-summaries in docs/HANDOFF.md and README.md.

Do not discard any user-authored corrections or prior analysis.
The legacy generator assumed observed_percent which current states omit.
"""
from pathlib import Path
import json
from validate_project import validate

ROOT = Path(__file__).resolve().parents[1]
START = "<!-- AUTO_CHECKPOINT_START -->"
END = "<!-- AUTO_CHECKPOINT_END -->"

def render(state):
    cp = state["latest_checkpoint"]
    db = state["unified_database"]
    observed = int(cp["expanded_unique_observed"])
    remaining = int(cp["expanded_unique_unobserved"])
    total = int(cp["expanded_84_tmx_unique_total"])
    assert observed + remaining == total
    version = cp["version"]
    assert db["version"] == version
    percent = 100.0 * observed / total
    return (
        f"{START}\n"
        f"## 자동 확인된 최신 진행 상태 ({version})\n\n"
        f"- TMX 고유 {total:,}종, 이미지 관찰 기록 {observed:,}종 "
        f"({percent:.2f}%), 미관찰 {remaining:,}종.\n"
        f"- 정체는 잠정 후보. 공식 PNG↔Local ID 매핑 "
        f"{cp.get('mapping_verified',0)}종, TileZed 검증 "
        f"{cp.get('tilezed_verified',0)}종, 최종 인증 "
        f"{cp.get('approved_final_certifications',0)}종.\n"
        f"- 물리 SQLite: {db['repo_manifest']}, "
        f"{db['table_count']}테이블, SHA256 {db['sqlite_sha256']}.\n"
        f"- 기존 사용자 수동 80종, 제외 14종, 보류 D 2종과 "
        f"JUMBO 20종 및 원본 PNG/TMX는 보존.\n"
        f"- D는 동일 (tile_set_name, local_id)의 다른 A를 "
        f"원래 B TMX의 동일 좌표·층·레이어에 치환한 비교임. "
        f"과거 두 번째 TMX 위치·인접격자 D는 인증되지 않음.\n"
        f"- 아래 버전별 상세 인수인계는 그대로 보존.\n"
        f"{END}\n"
    )

def update_document(old, section):
    if old.count(START) != old.count(END) or old.count(START) > 1:
        raise ValueError("Invalid bounded auto-checkpoint markers")
    if START in old:
        prefix, rest = old.split(START, 1)
        _, suffix = rest.split(END, 1)
        return prefix + section + "\n" + suffix.lstrip("\n")
    index = old.find("\n")
    if index < 0:
        raise ValueError("Missing HANDOFF heading")
    return old[:index + 1] + "\n" + section + "\n" + old[index + 1:].lstrip("\n")


README_START = "<!-- AUTO_README_START -->"
README_END = "<!-- AUTO_README_END -->"


def render_readme(state):
    """Render a small bounded README status section from authoritative fields only."""
    cp = state["latest_checkpoint"]
    db = state["unified_database"]
    version = cp["version"]
    if db["version"] != version:
        raise ValueError("README checkpoint/SQLite version mismatch")
    observed = int(cp["expanded_unique_observed"])
    total = int(cp["expanded_84_tmx_unique_total"])
    remaining = int(cp["expanded_unique_unobserved"])
    if observed + remaining != total:
        raise ValueError("README expanded observation total mismatch")
    evidence = state.get(f"latest_{version}_evidence", {})
    new = evidence.get("source_verified_provisional", db.get(f"{version}_visual_review_rows", "증거 참고"))
    excluded = evidence.get("excluded_unverified", "증거 참고")
    evidence_csv = cp["evidence_repo_path"]
    evidence_dir = evidence_csv.rsplit("/", 1)[0]
    return (
        f"{README_START}\\n"
        f"> **최신 검증 체크포인트: {version} ({cp['date']})** — 원본 이미지 관찰과 잠정 정체 후보 기록이며, 최종 정체 인증과 다릅니다.\\n\\n"
        "| 최신 진행 항목 | 확인된 수치 |\\n"
        "|---|---:|\\n"
        f"| 84개 TMX의 고유 타일 | **{total:,}종** |\\n"
        f"| 이미지 관찰 기록 | **{observed:,}종 ({100*observed/total:.2f}%)** |\\n"
        f"| 미관찰 타일 | **{remaining:,}종** |\\n"
        f"| 이번 {version} 신규 잠정 기록 | **{new}종** (160종 검토 중 {excluded}종 제외) |\\n"
        f"| 물리 SQLite | **{db['table_count']}테이블** |\\n"
        f"| 공식 PNG↔Local ID / TileZed / 최종 정체 인증 | **{cp.get('mapping_verified',0)} / {cp.get('tilezed_verified',0)} / {cp.get('approved_final_certifications',0)}종** |\\n\\n"
        f"- [최신 시각 관찰 CSV]({evidence_csv}) · [이미지 증거 및 검수 결과]({evidence_dir}/) · [최신 SQLite 매니페스트]({db['repo_manifest']})\\n"
        f"- SQLite SHA-256: \`{db['sqlite_sha256']}\`. **기존 결과·사용자 수동 80종·제외 14종·원본 PNG/TMX는 보존**하며, 보류 항목을 완료에 합산하지 않습니다.\\n"
        f"{README_END}"
    ).replace("\\n", "\n")


def update_readme(old, section):
    if old.count(README_START) != 1 or old.count(README_END) != 1:
        raise ValueError("README must contain exactly one bounded auto-summary block")
    prefix, rest = old.split(README_START, 1)
    _, suffix = rest.split(README_END, 1)
    return prefix + section + suffix

def main():
    state = json.loads((ROOT / "PROJECT_STATE.json").read_text(encoding="utf8"))
    errors = validate(state)
    if errors:
        raise RuntimeError("; ".join(errors))
    path = ROOT / "docs/HANDOFF.md"
    original = path.read_text(encoding="utf8")
    updated = update_document(original, render(state))
    if updated != original:
        path.write_text(updated, encoding="utf8")
        print("Handoff bounded summary safely updated")
    else:
        print("Handoff summary already current")

    readme = ROOT / "README.md"
    previous = readme.read_text(encoding="utf-8")
    current = update_readme(previous, render_readme(state))
    if current != previous:
        readme.write_text(current, encoding="utf-8")
        print("README bounded summary updated from PROJECT_STATE.json")
    else:
        print("README summary already current")

if __name__ == "__main__":
    main()
