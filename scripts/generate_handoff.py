#!/usr/bin/env python3
"""Update only a bounded auto-summary in docs/HANDOFF.md.

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

if __name__ == "__main__":
    main()
