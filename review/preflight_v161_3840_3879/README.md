# v161 후보 구간 3840–3879 — 기존 A/B/C 근거의 메타데이터 사전 대조

> **상태: source metadata preflight only. 시각 관찰 완료 아님 / DB 승격 금지 / v161 완성 아님.**

- 기준: `main` v160, commit `20bdcbd80d615d6294b129c641a764236d4f601e`, 8,954 / 10,042종 이미지 관찰, 미관찰 1,088종, SQLite 222테이블.
- 대조한 기존 기록: `review/v119_selected_A_new4633/REPRESENTATIVE_A_4633.csv` (Git blob `2054b15a1acfbc840616c447581f52d7e875a835`), `review/v120_B_context_new4632/B_CONTEXT_4632.csv` (blob `a5570a9445356a4fa47a6fe791052a2456a04b4c`), `review/v121_C_diff_new4632/C_B_DIFFERENCE_4632.csv` (blob `afa4843417c84399584fd27d1ec039db2c568114`).
- 총 40개 **서로 다른 키**를 `(tile_set_name, local_id)`로 조인하여 기존 CSV 기록의 A RGBA SHA256 문자열, B 파일 SHA256 문자열, B/C TMX 파일명·원래 층·레이어·좌표·raw GID, C 단일 제거 여부를 **상호 대조**했다. 40/40 메타데이터 일치, B−C 변경 픽셀 수 기록 40/40 양수, B 이웃 누락 기록 0, 지도끝 잘림 기록 0.
- 원본 A CSV는 **4,633행**, B/C CSV는 각각 **4,632행**이다. A 전용 보류 항목 `overlay_graffiti_wall_02/2`가 A의 0-based 인덱스 **2163**에 있어 이후에는 A 행 번호가 B/C보다 **+1**이다. **행 번호만으로 결합하면 서로 다른 타일을 잘못 연결한다.** `METADATA_AUDIT.json`은 키 기반 조인과 A 원본 인덱스를 별도로 기록한다.
- B−C 변경이 매우 작은 3개는 **시각 검수 우선**: 인덱스 3847 `walls_exterior_roofs_09/108` (16픽셀), 3848 `walls_exterior_roofs_09/109` (11픽셀), 3864 `walls_exterior_roofs_10/5` (8픽셀). 이 수치만으로 투명·정체·보류 확정 금지.
- 40개 B 메타데이터 모두 `scene_canvas_clipping_possible=1`이며 B는 `rendered_approximate`이다. 이것은 실제 이미지의 잘림을 확인했다는 뜻이 아니고, 5×5 장면에 한계가 있을 수 있다는 경고다.
- 계산된 GID−Local ID 상수: `walls_exterior_roofs_09=29841`, `walls_exterior_roofs_10=29993` (해당 CSV 범위 내 일치, 공식 아틀라스 매핑 인증 아님).

## 이 회차에서 하지 못한 검증

현재 실행 환경에서 바이너리 원본 PNG·TMX·A/B/C 이미지·ZIP·SQLite를 열어 픽셀을 직접 관찰하거나 해시/CRC/DB 무결성을 **독립적으로 재계산하지 못했다**. 위 SHA256은 기존 CSV의 기록값을 비교했을 뿐이다. 따라서 **이번 신규 이미지 직접 관찰 0종, 신규 잠정 후보 0종, 신규 최종 인증 0종**이며, `PROJECT_STATE.json`, `AGENTS.md`, `docs/HANDOFF.md`, SQLite, 원본 TMX/PNG를 변경하지 않았다.

## 다음 실제 시각 검수에 필요한 단계

1. 먼저 `main` 최신 버전과 다른 작업 브랜치/PR을 확인해 중복을 피한다. 이 preflight 브랜치는 **분석 구간의 소유권을 예약하지 않는다**.
2. 원본 `SELECTED_A_048.jpg`, `B_5x5_048.jpg`, `C_B_DIFF_048.jpg`와 개별 원본 A/B/C/DELTA 이미지, TMX 및 Tiles PNG를 직접 열어 각 키의 외형·부분 역할·재질·연결·방향·신뢰도를 독립 관찰한다.
3. 원본 파일 SHA256, PNG RGBA 픽셀 SHA256, 실제 TMX raw GID·층·레이어·x/y, ZIP CRC 및 B/C 차이를 재계산한다. `scene_canvas_clipping_possible` 및 작은 B−C 변화 3종을 특별 점검한다.
4. 검증된 잠정 후보만 부모 SQLite를 복사하여 새 테이블에 추가하고 부모 전체 테이블·행 보존, PRAGMA integrity_check, 중복키, 새 DB 해시를 검증한다. 그때만 새 시각 분석 PR을 만들고 CI 성공 후 병합한다. 공식 Local ID/TileZed/정체 인증은 근거 없이는 0 유지.

이 보고서는 기존 근거에 대한 텍스트 대조 기록이며 이미지 분석의 대체물이 아니다.
