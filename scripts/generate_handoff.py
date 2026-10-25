#!/usr/bin/env python3
"""Generate the human handoff from PROJECT_STATE.json, without guessing progress."""
from pathlib import Path
import json
from validate_project import validate

ROOT=Path(__file__).resolve().parents[1]
def render(s):
 r=s["reconciliation"];b=s["baselines"];v=lambda n:f"{n:,}"
 tasks="\n".join(f"{i}. {q}" for i,q in enumerate(s["next_actions"],1))
 return f"""# 프로젝트 좀보이드 B42 타일 정체 분석 — 자동 인수인계

> GitHub 기준일: {s["status_date"]}. **이 문서는 PROJECT_STATE.json에서 자동 생성됩니다.**

## 최우선 목표

이름 추측이 아닌 **원본 PNG의 실제 이미지**를 TMX 주변 5×5 타일과 조립해 관찰하고, 분할된 사물의 부품 역할과 오염·벽·지붕·가구 구성 요소를 구별한다. A=원본, B=조립, C=선택 배치 제거, D=다른 위치. TileZed와의 정합 검증 없이 확정 금지.

## 기준 범위

- TMX 원본: {", ".join(s["scope"]["tmx_sources"])}
- TMX 고유 사용 타일: **{v(s["scope"]["unique_tiles"])}종**, 전체 배치 {v(s["scope"]["total_tile_placements"])}건.

## 실제 원본 SQLite로 중복 제거 완료 (v47)

| 범위 | 수량 |
|---|---:|
| v36 기존 이미지 관찰 | **{v(b["v36"]["observation_records"])}종** |
| v37~v46 별도 기록 | **{v(b["v37_to_v46"]["observation_records"])}종** |
| 두 계보의 중복 키 | **{v(r["v36_v46_overlap_count"])}종** |
| v37~v46 중 진짜 신규 | **{v(r["new_unique_observed_v37_to_v46"])}종** |
| **통합 이미지 관찰** | **{v(r["merged_unique_observed"])}종 / {v(s["scope"]["unique_tiles"])}종 ({r["merged_observation_percent"]:.2f}%)** |
| 미관찰 | **{v(r["remaining_unobserved"])}종** |
| 최종 정체 인증 | **{r["approved_final_certifications"]}종** |

두 실제 DB에서 (tile_set_locator, local_id) 합집합을 계산해 **{v(r["merged_unique_observed"])}종**으로 검증 완료. 보고 수치 2,986을 그대로 합하지 않는다.

## 잠정 후보 수량 주의

- v36의 과거 문서 보고: {v(r["v36_reported_candidates"])}종; v36 시각 증거 테이블에서 실제 키와 후보를 재검증한 수: **{v(r["v36_auditable_candidate_keys"])}종**. 차이 {r["v36_reported_candidate_discrepancy"]}종은 보고 및 증거 키 간 불일치로 남긴다.
- v46 직접 확인 후보: **{v(r["v46_auditable_candidates"])}종**.
- 감사 가능한 잠정 후보 키 합집합: **{v(r["merged_unique_candidates"])}종**. **정체 확정 수가 아니다.**
- 두 기록이 다른 단어로 후보를 표시한 동일 키 **{v(r["source_candidate_wording_conflicts"])}종**: 두 가설 모두 보존, 이미지 재검토 전 자동 병합 불가.

## 원본 DB와 재현

- GitHub 복구 스크립트: `python3 scripts/restore_source_databases.py /tmp/pz_originals`
- 이 스크립트가 `analysis/archive/v36/`, `analysis/archive/v46/`의 분할 파일을 읽고 SHA-256 검증 뒤 두 원본 SQLite를 복원한다.
- 병합 경량 SQLite 복원: `python3 scripts/restore_merged_evidence.py /tmp/pz_merged.sqlite`
- 통합 표: `{r["merged_csv_repo_path"]}`
- 상세 증거·후보 충돌: `analysis/imports/all_observation_records.csv`, `analysis/imports/conflicting_candidates.csv`
- SQL 원본·CSV·증거를 혼동하지 말 것. 경량 병합 DB는 모든 과거 보조 테이블을 복제한 원본 DB가 아니다.

## 다음 실제 작업

{tasks}

## 불변 원칙

- 이미지 직접 관찰, 추론 후보, PNG-TMX Local ID 검증, TileZed 렌더 검증, 최종 인증을 분리한다.
- 역사적 v31 AI 분류를 증거로 삼지 않는다.
- 기존 `Tiles/`와 `B4220.3_MapExport_256/`의 원본은 절대로 수정하지 않는다.
- 모든 작업 종료마다 PROJECT_STATE.json과 checkpoints/를 기록하고 GitHub Actions 검증 결과를 확인한다.
"""
def main():
 s=json.loads((ROOT/"PROJECT_STATE.json").read_text(encoding="utf8"))
 errors=validate(s)
 if errors:raise RuntimeError("; ".join(errors))
 p=ROOT/"docs/HANDOFF.md"
 p.write_text(render(s),encoding="utf8")
 print("Handoff generated:",p)
if __name__=="__main__":main()
