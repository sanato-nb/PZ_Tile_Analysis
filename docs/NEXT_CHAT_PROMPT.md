# 새 채팅 / Work에서 이어가기 (v47 기준)

> 이 GitHub 저장소 `sanato-nb/PZ_Tile_Analysis`에서 **AGENTS.md, PROJECT_STATE.json, docs/HANDOFF.md, docs/ANALYSIS_RULES.md**를 먼저 읽어.
>
> v36와 v46 원본 SQLite는 `analysis/archive/v36/`, `analysis/archive/v46/`에 **압축 분할 보존**되어 있어. 나에게 파일 재첨부를 요구하지 말고 `scripts/restore_source_databases.py`로 SHA-256 검증 복구해. 이미 검증된 통합 이미지 직접 관찰은 **2,584/5,409종(47.77%)**, 미관찰 **2,825종**, 최종 정체 인증 **0종**이야. 중복 402종을 검사해 계산한 결과야.
>
> 잠정 후보 2,302종은 증거로 감사 가능한 후보 키 수이지 정체 확정이 아냐. v36 과거 후보 보고 2,291종과 실제 후보 키 2,156종 사이의 차이 135종, 두 계보의 후보명 충돌 256종은 보류하고 증거를 확인해.
>
> 원본 PNG 픽셀과 실제 TMX 주변 타일을 합성해 A/B/C/D를 관찰해 정체/부품 역할을 기록하고, 불확실한 Local ID·TileZed 정합은 절대 확정하지 마. 완료 후 GitHub에 체크포인트·PROJECT_STATE.json을 갱신해.
