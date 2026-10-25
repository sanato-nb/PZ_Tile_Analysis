# PZ Tile Analysis — AI/Work 작업 지침

이 저장소는 프로젝트 좀보이드 B42의 TMX와 원본 타일셋 PNG를 **시각적으로** 분석하는 프로젝트다. 최종적으로 마인크래프트 맵에 건물과 사물을 재현하기 위한 개별 타일 정의를 구축한다.

## 새 채팅마다 첫 행동

1. `PROJECT_STATE.json`, `docs/HANDOFF.md`, `docs/ANALYSIS_RULES.md`를 읽는다.
2. 저장소에서 최신 DB·증거가 **실제로 존재하는지** 확인한다. 경로가 없으면 없다고 말한다.
3. v36 (2,509 관찰)과 별도 v37~v46 (477 관찰)은 **서로 중복 제거하기 전까지 절대 합산하지 않는다**.
4. 원본 `Tiles/`, `B4220.3_MapExport_256/`는 보존한다.

## 판독 방법

- 타일 이름이나 텍스트 라벨이 아니라 **원본 스프라이트 픽셀과 TMX 주변 배치의 실제 조립 이미지**를 관찰한다.
- 한 물체를 구성하는 여러 칸(침대·소파·지붕·울타리 등), 벽 모서리/창·문 개구부, 흙/피/낙서/오염 오버레이를 인접 장면으로 비교한다.
- 기본 비교 증거: A=원본 PNG, B=동일 층의 주변 5×5 합성, C=선택한 배치만 제거, D=다른 사용 위치. D가 없으면 없음을 표시한다.
- 근사 아이소메트릭 렌더링은 **TileZed 공식 검증이 아니다**. TMX와 PNG 높이/버전이 어긋나면 Local ID의 정체로 확정하지 않는다.
- `observed`, `provisional_candidate`, `mapping_verified`, `certified`는 별도 상태다. 빈 증거·자동 카드 생성은 직접 검수로 세지 않는다.
- 과거 v31의 AI 라벨을 새로운 이미지 판독의 근거로 재사용하지 않는다.

## 데이터와 안전

- 유일 키: `(tile_set_locator, local_id)`; 맵 좌표 및 층/레이어는 증거에 보존.
- 이름이 애매하면 후보를 낮은 신뢰도로 표시하거나 보류한다. 수치만 올리기 위한 임의 분류 금지.
- 공개 저장소이므로 비밀키, 개인 데이터, 비공개 대화 내역 게시 금지.
- 사용자 동의 없이 기존 분석 파일 덮어쓰기/삭제/원본 변형 금지.
- Git에 큰 DB를 반복 직접 올리기보다 LFS/릴리스/외부 연결 저장소를 결정하고 SHA-256을 함께 기록한다.

## 인수인계 자동화

- 주 상태: `PROJECT_STATE.json`.
- 상태가 달라지면 `python scripts/validate_project.py`로 검사하고 `python scripts/generate_handoff.py`로 `docs/HANDOFF.md`를 갱신.
- `.github/workflows/sync-handoff.yml`은 main 푸시 시 검증과 인수인계 갱신을 시도한다. 작업 성공 여부는 Actions에서 확인.
- `docs/NEXT_CHAT_PROMPT.md`에 새 채팅 시작 지침이 있다.
