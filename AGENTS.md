# 좀보이드 B42 타일 정체 분석 — 고정 AI 작업 지침 (v47)

## 최우선 목표
개별 스프라이트 픽셀과 TMX 주변 5×5 조립 이미지 A/B/C/D를 직접 보고 그 물체나 구성부품을 이해한다. **타일 이름에서 정체를 추측하지 않는다.** 다칸 사물, 오염·잔해 오버레이, 벽의 방향·창 개구부, 지붕 경계 등 맥락을 직접 확인한다.

## 매 새 채팅/Work의 시작
1. `PROJECT_STATE.json`, `docs/HANDOFF.md`, `docs/ANALYSIS_RULES.md`, `analysis/imports/README_RECONCILIATION.md`를 읽는다.
2. **실제 v36·v46 DB는 GitHub에 있다.** `python3 scripts/restore_source_databases.py <outdir>`로 아카이브 조각을 복원한다. 파일을 사용자에게 다시 첨부해 달라고 하지 않는다.
3. 복구가 필요 없는 개요 작업은 `analysis/imports/merged_catalog_5409.csv` 및 `scripts/restore_merged_evidence.py`를 활용한다.
4. **검증된 관찰: 2,584/5,409(47.77%), 미관찰 2,825, 최종 인증 0.** 과거 v36 2,509과 v37~v46 477의 중복 402를 제거해 얻었다.
5. 잠정 정체 후보 감사 가능 키 2,302종은 최종 정체가 아니다. v36 과거 보고 후보 2,291종과 실제 테이블 근거 2,156종 차이 135종은 숨기지 않는다. 충돌 256종도 재검토한다.

## 판정과 보존
- 고유 키 `(tile_set_locator,local_id)`로 중복을 제거한다.
- A 원본 PNG, B TMX 같은 층 주변 조립, C 선택 배치만 제거, D 다른 위치를 사용한다.
- 이미지 직접 관찰 ≠ 잠정 정체 후보 ≠ 버전/Local ID 검증 ≠ TileZed 검증 ≠ 정체 인증.
- 이미지가 없거나 가려지면 hold; 타일셋명과 기존 v31 AI 의미 라벨을 정체 증거로 사용 금지.
- 과거 DB와 원본 Tiles/, B4220.3_MapExport_256/를 임의로 덮어쓰지 않는다.
- 공개 저장소에 개인정보·토큰·비공개 대화 원문을 올리지 않는다.
- 신규 관찰이 끝나면 체크포인트와 PROJECT_STATE.json을 갱신한다. GitHub Actions가 인수인계서를 재생성하고 DB 복원 검사를 수행한다.
