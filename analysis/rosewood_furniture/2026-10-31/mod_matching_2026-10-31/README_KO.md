# 로즈우드 357개 원본 가구 이름·스타일 → Minecraft 모드 후보 대조

기준 데이터: `furniture_dedup_v1/FURNITURE_MODELS_DEDUP_NAME_GROUP.csv`, 로즈우드 중심 지역, 원본 CustomName + GroupName 중복 제거 **357행**.

## 이 대조표가 검증한 것

- 모델 이름·스타일 357개 각각에 **현재 배포 중인 Forge 1.20.1 모드의 '용도별 후보'**를 1~2개 연결.
- 원본 가구 배치 수, 부품 수, 원본 타일셋·분류는 그대로 보존.
- 각 행의 `confidence`는 **가구 범주가 맞을 가능성**이지 원본 좀보이드와 실제 모델이 일치한다는 수치가 아님.
- `mod_block_id=UNVERIFIED`, `exact_visual_match=NOT_REVIEWED`: 모드의 실제 레지스트리, 회전·2~4칸 크기, 상호작용과 텍스처를 아직 1:1 검사하지 않았음.
- 다칸 가구는 **이미지 1조각을 Minecraft 가구 1개로 변환하면 안 됨**. 기존 조립 원장 `assembled_count_v2`의 실제 인스턴스 풋프린트와 별도 연결해야 함.

## 추천 순서

1. Paladin's Furniture — 주방·욕실·의자·침대 및 기본 가구 (1.20.1 Forge: https://modrinth.com/mod/paladins-furniture/version/1.20.1-v1.3-forge)
2. Macaw's Furniture — 나무가구/서랍장/책장/옷장 (1.20.1 Forge: https://modrinth.com/mod/macaws-furniture/version/jQcvCX79)
3. MrCrayfish's Furniture: Refurbished — 오븐/냉장고/컴퓨터 등 전자기기 (1.20.1 Forge: https://www.curseforge.com/minecraft/mc-mods/refurbished-furniture/files/all?page=1&version=1.20.1). 별도 Framework 필요.
4. Decocraft — 상점·사무실·특수 소품, 기타 장식 대량 탐색 (1.20.1 Forge: https://www.curseforge.com/minecraft/mc-mods/decocraft/files/7092533)
5. Immersive Furniture — 위 모드에 없는 고유 가구 직접 제작 및 라이브러리 활용 (1.20.1 Forge: https://www.curseforge.com/minecraft/mc-mods/immersive-furniture/files/all)

## 분류별 후보 수

- **Paladin's Furniture**: 174개 스타일을 우선 탐색 (범주 유사 고 170, 중 4, 낮음/미확인 0). 이는 실제 블록 매칭 성공률이 아님.
- **Macaw's Furniture**: 103개 스타일을 우선 탐색 (범주 유사 고 98, 중 5, 낮음/미확인 0). 이는 실제 블록 매칭 성공률이 아님.
- **MrCrayfish Refurbished**: 44개 스타일을 우선 탐색 (범주 유사 고 29, 중 15, 낮음/미확인 0). 이는 실제 블록 매칭 성공률이 아님.
- **Decocraft**: 31개 스타일을 우선 탐색 (범주 유사 고 0, 중 8, 낮음/미확인 23). 이는 실제 블록 매칭 성공률이 아님.
- **Immersive Furniture (custom)**: 5개 스타일을 우선 탐색 (범주 유사 고 0, 중 0, 낮음/미확인 5). 이는 실제 블록 매칭 성공률이 아님.

## 주의

원본 "357종"은 세밀한 시각 모델 확정치가 아닌 CustomName+GroupName 조합이다. 소파의 방향·색상을 줄일 수 있고, 상점의 냉장고 진열대·산업 특수 설비는 따로 제작해야 할 수 있다. 라이선스에 따라 기존 모드 모델/텍스처를 추출해 사용자 배포물에 재포함하는 것은 제한될 수 있다.

**다음 검수:** 목표 Forge 버전에서 각 모드를 실제 로딩하고 블록/아이템 레지스트리와 대표 PNG/가구를 대조해야만 `mod_block_id`, `facing`, `footprint` 및 신뢰도를 확정할 수 있다. 이 단계 전에는 자동 완성 월드 변환을 실행하지 말 것.
