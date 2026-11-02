# 로즈우드 가구 26차 — 281~290 독립 시각 검수 (레인 A)

2026-11-02. PZ 완성형 원본 이미지와 Minecraft 소스 기반 기존 비교 JPG 10종을 이번 실행에서 **실제로 열어 개별 육안 대조**했다. **기존 비교 JPG 10장을 바이트 그대로 재사용**했고, 신규 Blockbench 렌더는 0건이다. PNG 10장도 기존 Git blob을 재사용한다. 판정 CSV와 보류 목록은 이번 실행에 새로 작성했다.

**조건부 1건(290), 보류 9건(281~289), 인게임 1:1 승인 0건.**

- 281 Counter / Pizzawhirled — **DEFER**: PZ는 빨강/흰 타일 패널·짙은 갈색 상판. 후보는 주황 상판·회흑색 통나무 큐브. 색상·전면 타일 패턴 불일치. 후속: 붉은/흰 타일 카운터 실제 모델 확인.
- 282 Counter / Quality Crafted — **DEFER**: PZ는 갈색 세로 목재 판넬·판재 상판. 후보는 검은 나무껍질 측면·주황 상판. 패널 구조와 색조 불일치. 후속: 판넬형 목재 카운터 원본 모델 확인.
- 283 Counter / Rounded Glass Display — **DEFER**: PZ는 곡면 투명 유리·2단 진열 선반·2칸 목재 쇼케이스. 후보는 불투명 단일 큐브. 후속: 곡면 유리 2×1 쇼케이스 및 연결 구조 검증.
- 284 Counter / Theater — **DEFER**: PZ는 흰 상판·파란 본체·청록 가로띠. 후보는 주황/회흑 나무 큐브. 후속: 극장용 청색 카운터 원본 모델 확인.
- 285 Locker / Military — **DEFER**: PZ는 카키색 철망 4문 군용 로커. 후보는 파란색 단일 철문·환기구 로커. 문 개수·망사·색상 불일치. 후속: 카키색 4문 망사 군용 로커 원본 모델 확인.
- 286 Table / Large Bleached — **DEFER**: PZ는 밝은 목재 1×2 식탁·4개 다리. 후보는 컵·접시·수저 식기 소품뿐이며 테이블 본체 없음. 후속: 밝은 목재 1×2 네 다리 식탁 검색; 바닐라 조립은 미검증.
- 287 Table / Pizza Dinner — **DEFER**: PZ는 진한 상판·붉은 테두리·중앙 받침기둥의 2×1 식탁. 후보는 얇은 평면만 렌더된 부분 JSON. 후속: 2×1 상판·페데스털 전체 원본 모델 렌더.
- 288 Wardrobe / Open — **DEFER**: PZ는 양끝 밝은 목재 기둥과 노출된 가로 옷걸이 봉의 3칸 행거. 후보는 닫힌 어두운 1칸 옷장 일부. 후속: 3×1 오픈 행거 및 연결 부품 실제 모델 확인.
- 289 Amplifier / Guitar — **DEFER**: PZ는 황토색 기타 앰프·상단 조작 노브·검은 전면 그릴. Minecraft 실제 모델 후보가 없어 비교 불가. 후속: 실제 기타 앰프 모드 블록·모델·텍스처 확보 또는 별도 제작.
- 290 Dishwasher / Brown — **CONDITIONAL**: 양쪽 모두 회색 직육면체 전면도어 식기세척기. PZ는 긴 검은 상단 조작판·낮고 넓은 비율, 후보는 작은 손잡이형 조작부와 다른 문 테두리. 후속: 설치 높이·전면 조작부·문 분할·기능·충돌 검증 후 승인.

## 검증 범위 및 한계

- `cards/`: 기존 비교 JPEG 10장 동일 바이트 복사. `pz_previews/`: 기존 PZ 원본 PNG 10장 동일 바이트 복사.
- `BATCH_281_290_MANUAL_VISUAL_REVIEW.csv`: 새 육안 판정. `BATCH_281_290_DEFERRED_OTHER_MODS.csv`: 9건 보류. `BATCH_281_290_SHA256_PROVENANCE.csv`: 이번에 JPEG 바이트 재해시, PNG는 Git blob SHA-1, 원본 모델 SHA-256은 기존 기록을 인용(재해시 아님).
- 287번 기존 JSON 렌더는 부분 렌더이며 289번은 Minecraft 실제 모델 부재.
- Minecraft Java 1.20.1 Forge 설치, 충돌, 작동, 1:1 시각 인증 모두 미실시. 조건부는 승인 아님.
- ZIP에는 JPG 10장과 텍스트 검수 기록이 포함된다. 원본 PZ PNG 10장은 GitHub 디렉터리에서 별도 제공.
- 원본 TMX/PNG/SQLite/357종 기준 원장 및 B/C 레인 파일은 변경하지 않는다. Draft PR은 미병합으로 유지한다.

출처: `work/rosewood-all-357-real-render-20261101`의 `all_357_complete_native_comparisons_v1/cards` 및 `complete_furniture_visual_3d_v1/previews`. 다음 A 레인: 311~320.
