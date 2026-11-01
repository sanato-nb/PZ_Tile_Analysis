# 4차 묶음 031~040 — 기존 5개 모드 밖 추가 검색 근거

이 파일은 **기존 10건 검수표에 포함된 후속 미매칭 목록을 대체하지 않는다.** 추가로 공개 배포처를 확인해 둔 외부 모드 검색 우선순위다. 정확한 블록 레지스트리 ID·.json/.bbmodel·설치 블록 수·게임 작동을 확인하기 전에는 확정하지 않는다.

| PZ 번호 | PZ 원본 완성 외형 | 새 모드 후보 | 확인한 사실 | 아직 확인할 것 | 상태 |
|---|---|---|---|---|---|
| 032 X-press/Coffee | 검은 플라스틱 드립 커피머신·컵 받침, 탁자 위 소형 | [CoffeeCraft](https://modrinth.com/mod/coffeecraft) | 공식 Modrinth에서 **Minecraft Java 1.20.1 Forge**, 커피 관련 블록을 제공하는 모드임을 확인. [공식 CurseForge](https://www.curseforge.com/minecraft/mc-mods/coffeecraft-by-blockbrothers)도 동일한 버전을 명시한다. | Coffee Maker Black 블록의 실제 ID·PNG/3D 기하를 JAR에서 열어 원본 형태·높이·설치면적 대조 | 모델 미검증 |
| 035 Bench/Oakwood | **2타일로 이어진** 긴 갈색 등받이 없는 목재 벤치 | [Furnitury — Vanilla Styled Furniture, Forge 1.20.1 2.2305](https://modrinth.com/mod/furnitury/version/2.2305-forge-1.20.1) | 버전 변경 이력에 **Bench Without Back (all wood variants)** 신설 명시. 현재까지 검토한 피아노 의자·운동 벤치보다 기능 분류가 적합하다. | 모드 원본 JSON·텍스처 직접 열람, 2칸 연결 가능 여부·실제 길이·다리/색상 대조 | 모델 미검증 |
| 039 Drawers/Bedroom | 위 **서랍 1개**, 아래 문 없는 열린 수납칸, 밝은 목재 | [Furniture Expanded 1.2 Forge 1.20.1](https://modrinth.com/mod/furniture-expanded/version/52REfgdO) | Forge 1.20.1 버전 변경 이력에 **Nightstand, Bedside Table** 추가 명시. Architectury API 의존성도 표시됨. | 원본 모델/텍스처 직접 가져와 위 한 서랍·아래 개방 공간 구조 확인 | 모델 미검증 |

**기타 보류:** 036 벽걸이 핸드드라이어는 검증된 Forge 1.20.1 정확 대응 소스가 아직 없다. 일반 세탁건조기와 혼동하지 않는다. 038 흰색 3단 개방 책장은 유리 찬장/장식 접시 선반 대신 **문 없는 1×1 세로 선반**을 따로 찾는다.

**원본 이미지에 대한 주의:** 035는 이전 두 스프라이트 조립 상태가 provisional이며 마크 1×1 벤치를 무조건 2×1 완성체로 간주하지 않는다. 바닐라 계단·덫문·울타리 조합은 겹치는 셀의 실제 배치 가능 여부가 검증돼야만 제안한다.

진행 기록: 4차 배치의 공식 우선 검수 기록은 `BATCH_031_040_MANUAL_VISUAL_REVIEW.csv` 및 `MANIFEST.json`이고, 정확한 1:1 매칭 승인 수는 0이다.
