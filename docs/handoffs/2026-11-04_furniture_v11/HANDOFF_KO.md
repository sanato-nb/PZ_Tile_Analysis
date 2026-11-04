# 좀보이드 → 마인크래프트 맵 프로젝트 — 새 채팅 인수인계서
작성일: 2026-11-04 (KST)
대상: 같은 ChatGPT 프로젝트 「좀보이드 -> 마크 맵」의 다음 대화
저장소: https://github.com/sanato-nb/PZ_Tile_Analysis
**최우선 최신 가구 기준: v11 / PR #293 / 브랜치 work/pz-b42-exact-tile-assembly-v11-20261104**

## 0. 새 대화는 먼저 이 파일부터 읽을 것
- 최신 가구 DB PR: https://github.com/sanato-nb/PZ_Tile_Analysis/pull/293
- 최신 가구 DB 결과 폴더: https://github.com/sanato-nb/PZ_Tile_Analysis/tree/work/pz-b42-exact-tile-assembly-v11-20261104/analysis/furniture_full_b42/2026-11-04/exact_assembly_v11
- 최신 원본 + 확장 SQLite ZIP: https://github.com/sanato-nb/PZ_Tile_Analysis/blob/work/pz-b42-exact-tile-assembly-v11-20261104/analysis/furniture_full_b42/2026-11-04/exact_assembly_v11/B42_EXACT_TILE_GRID_ASSEMBLY_V11.zip
- 최신 매니페스트: https://github.com/sanato-nb/PZ_Tile_Analysis/blob/work/pz-b42-exact-tile-assembly-v11-20261104/analysis/furniture_full_b42/2026-11-04/exact_assembly_v11/MANIFEST.json
- v11 README: https://github.com/sanato-nb/PZ_Tile_Analysis/blob/work/pz-b42-exact-tile-assembly-v11-20261104/analysis/furniture_full_b42/2026-11-04/exact_assembly_v11/README_KO.md
- 원본 PZwiki 가구 정리본(기준 명부): https://github.com/sanato-nb/PZ_Tile_Analysis/blob/main/pzwiki_furniture/2026-11-03/README.md
- v9 위키 누락 11건 감사: https://github.com/sanato-nb/PZ_Tile_Analysis/tree/work/pz-b42-definition-first-furniture-v9-20261104/analysis/furniture_full_b42/2026-11-04/definition_first_v9
- v8 이미지 검수 기록: https://github.com/sanato-nb/PZ_Tile_Analysis/tree/work/pz-b42-remaining64-visual-v8-20261104/analysis/furniture_full_b42/2026-11-04/visual_completion_v8

**중요:** PR #293은 2026-11-04 확인 시 open / 미병합 상태. GitHub main 브랜치의 README, AGENTS.md, PROJECT_STATE.json에는 과거 타일분석 v240~v257의 “최신” 문구가 남아 있으므로, 가구 DB 최신을 찾을 때 main의 옛 버전을 우선하지 말 것. 새 대화에서 브랜치/PR/Actions를 먼저 재확인한다. 다른 브랜치/Work에서 나중에 더 진행됐으면 그쪽으로 최신 기준을 업데이트한다.

## 1. 프로젝트의 궁극 목표와 지금의 집중 범위
- 궁극 목표는 **프로젝트 좀보이드 Build 42의 맵과 가구·설비·수납 기능을 Minecraft에서 원본에 가깝게 재현**하는 것이다.
- 현재 단계는 Minecraft 구현이 아니라 **좀보이드의 모든 가구/설치물 목록을 정리하고, 가구별 원본 TileSet/Local ID, 방향, 다칸 구성 부품, 외형·상태 변형, 기능, 컨테이너 및 용량 속성을 보존하는 관계형 DB 완성**이다.
- 최초의 로즈우드 가구 검수에 범위를 한정하지 않는다. **Build 42 전체 가구 범위**가 목표다. 로즈우드는 향후 실제 TMX 배치 및 Minecraft 제작을 시작할 검증 지역으로 사용할 수 있다.
- PZ3D 등의 3D 변환 모드 이미지는 **완성 가구의 형태를 판단하고 유사한 Minecraft 가구 모드·Blockbench 모델을 고르는 참고 자료**다. PZ 3D 모델을 그대로 Minecraft에 수입하는 것이 기본 목표는 아니다.
- 기존 Minecraft 가구 모드뿐 아니라 마인크래프트 바닐라 블록/가구 조합도 사용 가능하나, **지금은 매칭·모델 제작을 확정하지 않는다.** Forge 1.20.1에서 Block, BlockEntity(수납), Entity 중 어떤 구현이 적절할지는 모든 가구 정보를 정리한 후 선택한다.
- 좀보이드에는 여러 타일이 모여 하나의 가구가 되는 경우와, 같은 가구의 방향별 스프라이트가 있다. **스프라이트 개수=가구 종류 수**로 세지 않는다.

## 2. 최신 v11 실제 검증 수치 (2026-11-04)
| 항목 | 수량 | 뜻 |
|---|---:|---|
| B42 원본 TileDef 고유 타일 키 | 61,418 | 전체 타일 정의의 키 수. 가구만이 아님 |
| 원본 소스 슬롯 | 73,644 | 다른 소스/중복 포함 저장 행 수 |
| 원본 속성 행 | 195,265 | source_attributes에 보존 |
| PZwiki 목록 | 1,268 | 위키 원문 행. 고유 완성 가구 1,268종을 뜻하지 않음 |
| 위키에 원본 이미지 TileSet/LocalID가 연결된 행 | 1,257 | 미연결 11행 |
| 가구 원장 레코드 | 2,231 | 위키 1,268행 + 위키 미연결 TileDef 그룹 963행 |
| 명명 기준 원본 가구 후보 그룹 | 1,852 | 실제 고유 가구 수 아님 |
| 가구 후보 원본 타일 키 | 8,219 | v11 원본 ID↔좌표 저장 타일 수 |
| 가구 레코드↔타일 연결 | 14,195 | 동일 타일의 복수 연결과 추정 확장 포함 |
| 수납 속성 연결 | 1,855 | 위키 직접/그룹추정/원본전용 링크 구분 |
| 그룹×Facing 조립 후보 | 3,840 | 완성 가구 수가 아닌 원본 템플릿 |
| 직사각형 격자가 있는 후보 | 843 | 실제 완성 가구 843종 인증 아님 |
| v11 조립 관련 경고 | 474 | 원본 근거 충돌/부족/다중 앵커 |

**GitHub Actions:** PR #293 소스 빌드가 성공. SQLite PRAGMA integrity_check=ok, ZIP CRC 및 원본/추가 테이블 행 수 검사 통과. 소스 원본 파일은 덮어쓰지 않았다. 새로 게임 내부 Moveable 객체 동일성을 공식 인증한 건수는 **0**. 실제 TMX 배치 생성 **0**, 게임 Lua 아이템 분포 로딩 **0**, Minecraft Block/Entity 선택 **미정**.

## 3. v11에서 해결한 구체적인 기술 문제
v10의 sprite ID 목록과 SpriteGridPos 목록은 **각각 별도 정렬된 문자열**이었다. 이를 zip처럼 순서대로 묶으면 타일↔그리드 좌표가 뒤섞인다.
v11은 각 TileDef **원본 타일 행에 기록된 SpriteGridPos를 직접 읽어** source_key, Facing, 정수 x/y 및 상대 x/y를 개별 저장한다.

핵심 테이블:
- v11_tile_position: 8,219개 원본 타일 키별 source_key, group_id, Facing, 원본/상대 위치, 원본 container/ContainerCapacity/ContainerPosition, Wiki 직접 ID 앵커
- v11_direction_template: 3,840개 그룹×Facing 원본 조립 후보
- v11_source_warning: 원본 그리드, Wiki 앵커, 수납 기능 충돌 474건

v11 템플릿 상태:
- COMPLETE_RECTANGLE 843
- DUPLICATE_POSITION 27
- INCOMPLETE_GRID 14
- MISSING_GRID 52
- MULTIPLE_NO_GRID 250
- SINGLE_NO_GRID 2,654
합계 3,840.

v11 경고 상태:
- 위치 중복 27 / 불완전 격자 14 / 누락 격자 52 / 다중 타일인데 격자 없음 250
- 하나의 템플릿에 여러 Wiki 직접 이미지 앵커 125
- 서로 다른 원본 ContainerCapacity 5 / 서로 다른 container 유형 1
합계 474.

**대표적 오류 예방:** Large Oak Bed, furniture_bedding_01/40..43, E방향의 원본 좌표는 /40=(0,1), /41=(1,1), /42=(0,0), /43=(1,0). 반드시 source_key↔SpriteGridPos를 한 행 단위로 연결한다.

~~~sql
SELECT source_key, relative_x, relative_y,
       source_container, source_capacity_raw
FROM v11_tile_position
WHERE group_id='FUR-000429796F297C17' AND Facing='E'
ORDER BY relative_y, relative_x;
~~~

## 4. v9~v10에서 이미 끝난 부분 (중복 작업 금지)
- v9: 전체 2,231개 목록의 출처·원본 연결 등급 분리. 14,195링크 = Wiki 이미지 원본 타일 ID 직접 연결 **1,649** + 이름/그룹 기반 미확정 확장 **7,993** + TileDef-only **4,553**.
- v9: 수납 관련 1,855링크 = 위키 직접 앵커 365 / 동일 이름 그룹 추론 1,142 / TileDef-only 348. **Wiki 수납 용량과 TileDef ContainerCapacity를 혼합하거나 여러 타일 용량을 멋대로 합산하지 말 것.**
- v9: 미연결 Wiki 11행 = 일반 목록·컬렉션명 3, 변형 이미지 누락 3, 특정 명명 물체 이미지 누락 5. 가능 후보 49개는 검증 전 참고자료이며 임의의 확정 TileDef ID를 입력하지 않았다.
- v10: 8,219개 원본 타일을 source_key→가구 원장으로 역조회하는 인덱스 구축.
- v10: 8,219키 중 위키 직접 연결 한 행 1,471 / 복수 위키 직접 89 / 명칭 그룹 추론만 2,106 / TileDef-only 4,553.
- v10: 이름 그룹에서 ContainerCapacity 서로 다른 값이 발견된 사례는 Public Mail Box, Shoddy Wall Shelves, Crate 등. 가구 하나인지 다른 상태인지 아직 미확정.
- v10: 위험 타일 3,536개를 조회용 이슈로 표기. **검토 경고의 수량을 미분류 가구 수라고 해석하지 말 것.**

## 5. 이미지 검수 및 Work 결과를 정확히 구분
- 위키 여러 항목이 같은 원본 그룹에 연결된 **129/129그룹**은 v8까지 원본 이미지 비교 및 판정 **기록**이 있다. 이것은 129개 완성 가구의 실제 3D/Moveable 동일성 확정과 다르다.
- 앞서 58그룹에서는 368개 원본 PNG 스프라이트를 추출해 접촉시트 58장과 원본 방향·부품의 시각 증거를 만들었고, v8의 나머지 64그룹까지 단계적으로 기록을 확장했다.
- 별도 Work 대화에서는 TileDef-only 963그룹 중 **수납 관련 107그룹, 원본 타일 574개를 이미지로 열람했다는 작업 기록**이 있다. 다만 그 107그룹 결과가 최신 v11 SQLite에 최종 병합·검증됐다는 근거는 아직 확인되지 않았다. 저장·검증 완료 수치와 혼합하지 말고 GitHub 해당 원장 검색 후 중복 ID 기준으로 반영한다.
- 원본 TileDef에 수납 속성이 있는 107그룹과 위키 직접 연결 1,257행은 **서로 다른 집계의 분모**다.
- 외형은 이름으로 단정하지 않는다: Wooden Bench(2부품×방향), Large Metal Trough(3부품×방향 및 수납), 원형/사각 Rain Collector Barrel, 다른 모양의 Road Cone, 성장/시듦 상태가 다른 화분, 여러 조각으로 된 러그, 가구 아닌 Trash와 Window, Air conditioner 부품 등.
- 현재 결정: **불필요한 전체 PNG 재검수를 무작정 수행하지 말고**, 원본 정의/위키의 명확한 근거로 우선 가구 DB를 완성한다. 이미지나 3D 근거는 이름 충돌·완성 모습·부품 불명확한 부분에 선택적으로 사용한다.

## 6. 인접 작업들 (서로 다른 분모와 버전, 가구 DB와 혼동 금지)
- 원본 자료 폴더: Tiles/2x/, Tiles/tiledefinitions.tiles, Tiles/newtiledefinitions.tiles, tiledef/, B4220.3_MapExport_256/tmx/.
- 더 오래된 원본 타일 분석 v31은 **일반 스프라이트 33,600개에 대한 접촉시트 기준 시각 스크리닝 범위 33,600/33,600**을 기록했고, **개별 기능·정체 인증 33,600건 완료**를 뜻하지 않는다. v31_검수결과와정확한범위.md 및 두 CSV를 프로젝트 자료에서 확인.
- 별도 TMX 타일 분석 흐름은 84개 TMX에서 관찰한 고유 타일 키 **10,042개**를 다루며, 기존 README/AGENTS.md에 v255/v256/v257 등 역사적 최신 표시가 있다. 이 수와 가구 원장 2,231, B42 원본 61,418, v31 일반 이미지 33,600은 분모가 전부 다르다.
- 로즈우드 가구 비교의 과거 결과(79종류/357 명명 스타일, 3D/Blockbench/기존 Minecraft 모드 매칭)는 초기 참고 자료다. 이전 매칭 중 오분류·보류가 많았으며 새 가구 ID가 확정되기 전에는 무조건 재사용하지 말 것. Rosewood 관련 PR #278, #279, #280 등 참고.
- Minecraft에서는 좀보이드 벽이 타일 경계선인데 Minecraft 벽은 보통 한 블록의 두께를 갖는 문제가 있다. 최종 변환 규칙은 아직 결정하지 않았고, 얇은 벽만으로 처리하는 것을 기본 목표로 삼지 않는다.

## 7. 앞으로 바로 해야 할 일 — 우선순위
1. **최신 소스 재확인:** 먼저 PR #293과 v11 MANIFEST/README/SQLite를 읽는다. 새로운 v12/Work 결과가 있다면 그 상태를 먼저 반영한다. main의 오래된 PROJECT_STATE.json만으로 가구 최신 진행도를 판단하지 않는다.
2. **v11의 474건 경고 처리:** 원본 TileDef 속성 및 원본 타일 ID별 좌표를 이용해 중복·불완전·누락 그리드, 복수 직접 Wiki 이미지 앵커 및 용량/컨테이너 충돌을 **원인별로 분류하여 수정 가능한 연결만** v12에 반영한다. 데이터 변경 전후 비교 필수.
3. **가구 개체/디자인/상태/방향/부품 DB 분리:** Wiki 이름 한 개가 여러 다른 실루엣을 가질 수 있으며, 여러 TileDef Local ID가 하나의 가구 구성일 수 있다. 객체 동일성 미확정은 REVIEW로 표시하고, 멀티타일 조립을 자동 단정하지 않는다.
4. **Wiki 미연결 11건을 출처 기반으로 해결:** 원본 ID가 없는 3개 컬렉션명과 이미지 누락 8개를 구분. 추정 후보 49개를 확정값으로 덮어쓰지 않는다.
5. **107 Work 이미지 관찰 자료 확인/반영:** GitHub에 실제 파일이 있는지 검사하고 이미 v11에 수록된 데이터와 source_key로 중복 제거. 파일 없으면 대화의 참고 관찰로만 취급.
6. **수납 기능을 사용할 수 있는 DB 정규화:** container, 원본 ContainerCapacity, Wiki 수납 용량, ContainerPosition, 가구 방향별 컨테이너 구성이 보존되어야 한다. 이후 게임 Lua의 방 유형·컨테이너별 아이템 생성 규칙과 RoomDefs를 연결하되 출처 없는 아이템을 임의 생성하지 않는다.
7. **TMX 배치 엔진 연계:** 실제 원본 GID/tileset firstgid/local_id, 층, 레이어, x/y, RoomDefs를 이용해 가구 정의/방향/부품을 실제 배치 인스턴스로 연결하고 마크 변환 검증 준비.
8. **마크 가구 구현과 모드 선정은 그 다음**: Forge 1.20.1, 바닐라 블록과 기존 모드/필요시 Blockbench를 활용하되 구현 타입은 유보.

## 8. 데이터 및 증거 판정 정책 (필수)
- **확정 근거:** 원본 TileDef의 실제 값, 원본 TileSet+Local ID, Wiki 원문 기록, 원본 PNG 픽셀 해시, 진짜 TMX 원본 위치.
- **참고/추론:** 같은 CustomName/GroupName이라는 이유만으로 연결된 다른 스프라이트, Wiki의 variant 이름을 제거하여 만든 계열, 이미지에서 보이는 완성 모습, 3D 변환 참고.
- **별도 최종 인증 필요:** 하나의 게임 Moveable 오브젝트, 물리적 가구 조립 정체, Lua 아이템 드롭/컨테이너 내용, Minecraft 구현 종류.
- 원본 정의/PNG/TMX 및 이전 DB를 **삭제하거나 덮어쓰지 말 것**. 새 버전 새 테이블·새 브랜치·증거 CSV와 검증 코드를 사용해 이력 보존.
- SQLite integrity_check, 모든 이전 핵심 테이블/행 수, 해시/ZIP CRC, 스프라이트 원본 좌표, 중복 키를 확인. 단순 자동 접촉시트 생성은 개별 사물 정체 확정으로 계산하지 않는다.
- 저장소는 공개 상태로 확인됐다. 개인 계정의 비밀번호/토큰, 사적인 채팅 전문은 업로드하지 않는다.
- 동작하지 않는 Work 중간 결과나 실패한 GitHub Actions는 **완료**로 보고하지 않는다. 열린 PR은 **main 반영**과 다르다.
- 사용자가 원하면 계속 실제 DB/코드/CSV를 만드는 작업을 수행하고, 계획만 작성하고 끝내지 않는다.

## 9. 새 채팅 첫 작업 예시
새 채팅은 아래 문구로 시작한다.

> 우리는 좀보이드 B42 → 마인크래프트 맵 프로젝트를 계속한다. GitHub sanato-nb/PZ_Tile_Analysis의 PR #293, work/pz-b42-exact-tile-assembly-v11-20261104, exact_assembly_v11 폴더를 최신 기준으로 먼저 읽어라. 이 인수인계서의 범위·주의사항을 유지하라. 지금 목표는 마크 가구 구현 결정이 아니라, 전체 가구별 원본 타일·방향·SpriteGridPos·여러 칸 부품·수납 속성 DB 완성이다. v11 474건 경고를 근거별로 재검증하고, 실제 수정 및 SQLite/CSV 검증 결과를 새 버전으로 GitHub에 기록하라. 이전 원본과 기존 DB는 보존하고, 공식 정체 미확정은 추론으로 명시하라.

---
인수인계는 **v11을 확인된 GitHub 최신 가구 DB로 지정**한다. 새 대화의 첫 단계는 GitHub에서 나중에 올라온 새 버전이나 다른 Work 미저장 결과 유무를 재확인하는 것이다.
