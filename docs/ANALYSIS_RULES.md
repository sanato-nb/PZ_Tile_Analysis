# 시각 판독 및 데이터 품질 규칙

> **다음 이미지 분석 표준(v242):** [실패에서 배운 전체 매뉴얼](SPRITE_VISUAL_ANALYSIS_PLAYBOOK.md) · [한 장 빠른 판정표](SPRITE_ANALYSIS_QUICK_REFERENCE.md) · [키별 기록 JSON](SPRITE_REVIEW_RECORD_TEMPLATE.json) · [재사용 시작 요청](SPRITE_VISUAL_NEXT_CHAT_PROMPT.md). **A 직접 픽셀 관찰을 B/C의 완성 장면에 앞세우고, 형태·부품·방향·오버레이·가림·정체 인증을 분리한다.**

## 독립적인 관찰 증거

1. TMX에서 `source_tmx, level, x, y, layer, raw_gid`와 타일셋·Local ID를 확보한다.
2. 원본 PNG 아틀라스의 해당 조각을 **실제 픽셀로** 추출한다. 투명/격자 범위 외/PNG 누락을 별도로 기록한다.
3. 같은 층 주변 타일로 5×5 영역을 조립한다. 렌더러와 TileZed 간 차이가 있으면 명시한다.
4. A 원본, B 조립, C 해당 배치만 제거를 비교한다. **사용자 정의 D는 동일 (tile_set_name, Local ID)에 공식적으로 대응한다고 독립 검증된 다른 A 이미지가 있을 때, 원래 B와 동일한 TMX 좌표·층·레이어에서 해당 이미지 한 개만 바꿔서 비교하는 단계다. 공식 대체 A가 없으면 D는 미수행이다.** 과거 v124 '다른 TMX 사용 위치'는 별도 부가 색인이며 현행 D 정답으로 보지 않는다. 주변 이미지 누락 수를 저장한다.
5. 타일셋명·과거 AI 후보를 가려 놓고 외형을 자연어로 설명한다.
6. 사물의 종류, 부품 역할, `confidence`, `review_status` 및 검증 상태를 별도 기록한다.

## 허용되는 분류

- 직접 이미지 관찰: `observed`
- 외형으로 잠정 추론: `provisional_candidate`
- 외형 부족/대응 실패: `held`
- 원본 PNG–TMX Local ID 정합 검증: `mapping_verified`
- 최종 정체 검증: `certified`

`observed` 또는 `provisional_candidate`는 절대로 `certified`를 의미하지 않는다.

## 불일치와 중복

- 서로 다른 아틀라스 버전의 높이/행 수가 다르면 동일 Local ID 대응을 자동으로 신뢰하지 않는다.
- `(tile_set_locator, local_id)`가 같은 두 관찰은 별도 증거가 될 수 있지만 고유 타일 수는 한 건이다.
- v36과 v37~v46에 대해 **각각의 레코드 키를 추출하고 교집합을 계산하기 전**에는 총 진행률을 합산하지 않는다.
- 과거 대화에 있던 판정 수치는 `reported`로 구분하고, 실제 DB에서 재계산한 수치만 `verified`로 표기한다.

## 출력 및 검수

- CSV + SQLite와 함께 위치·소스 해시·비교 이미지를 보존한다.
- HTML 검수기에는 이미지 상대 경로 오류를 피하도록 데이터 URI 또는 검증된 번들 경로를 사용한다.
- 압축 파일, SQLite, HTML의 무결성을 검사한 결과를 체크포인트에 적는다.
- 이미지가 존재한다는 것과 실제 육안 분석을 수행했다는 사실을 혼동하지 않는다.

## v127 전수 후보 탐색의 인증 경계

원본 v119 A에 대해 A1/A2/A3의 다른 크롭이 보이지 않는 경우, 다른 격자 칸 PNG 조각은 별도의 Local ID일 가능성이 있으므로 **검증된 다른 A가 아니다**. 같은 이름의 다른 PNG 파일을 확인하더라도 TMX/TileZed 대응을 인증하기 전까지는 후보로만 유지한다. 검색을 완료한 것과 D/B 이미지 재조립 또는 정체 검수를 완료한 것은 별도 집계한다.
