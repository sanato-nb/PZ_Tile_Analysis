# 로즈우드 357종 완성 가구 ↔ Minecraft 가구 모드 실제 3D 이미지 전체 재대조

**이번 수정:** 이전 221개의 구형 근사 그림을 대체할 수 있도록 Decocraft 이외 4개 모드의 원본 Minecraft Java 모델 JSON/PNG를 Blockbench 5.2.2로 변환·실제 캡처했다. 원본 PZ는 357개 모두 원래 조립된 완성 가구를 사용한다.

## 증거 수준별 수량
- ACTUAL_NATIVE_BLOCKBENCH_FULL_SOURCE_JSON: 110개
- ACTUAL_NATIVE_BLOCKBENCH_SOURCE_BBMODEL: 110개
- LEGACY_3D_APPROXIMATION: 4개
- NATIVE_BLOCKBENCH_PARTIAL_SOURCE_JSON: 111개
- NO_REAL_MOD_ASSET: 22개

## 정확한 한계
- 22개는 7개 모드 JAR의 초기 검수에서 대응 모드 가구를 찾지 못한 항목. 비어 보이는 오른쪽 패널 대신 **명시적인 불일치/추가 모드 탐색 또는 직접 모델 제작** 표시. 가짜 모델을 넣어 매칭 완료로 위장하지 않음.
- 다른 모드에서 원본 JSON cuboids를 Blockbench 자유 모델로 재조립한 경우 원본 게임의 동적 blockstate, connected textures, custom loader, shape rotation은 추후 검수 필요. 일부 부품 누락은 PARTIAL로 표시.
- 원본 JAR이나 텍스처 원본은 저장/배포하지 않음. 비교용 캡처와 출처 해시만 남김.
- 357개를 실제 Minecraft 게임에서 배치 확인하지 않았고, 1:1 형상·기능 최종 인증은 0개.

## 파일
- ZIP 압축 해제 후 INDEX.html 검색/필터로 전체 확인.
- ALL_357_FULL_RENDER_MATCHING.csv에 크기, PZ 속성, 실제 모델 ID, 이미지 근거, 원본 50건 수동 판정과 8건 개선 매칭, 남은 쟁점 보관.
- UNMATCHED_NEEDS_REAL_FURNITURE_MOD_OR_CUSTOM_MODEL.csv: 모드 모델을 찾지 못한 대상.
