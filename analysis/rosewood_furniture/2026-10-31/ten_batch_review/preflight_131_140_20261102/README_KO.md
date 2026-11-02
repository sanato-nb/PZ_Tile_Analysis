# 로즈우드 131~140번 사전 이미지 검수 — 2026-11-02

## 구분
- 이 파일은 10차(091~100) 이후 **11~13차 검수 예약과는 독립적인 사전 시각 판독 기록**이다.
- 대상 10종 모두 GitHub에 이미 저장된 **PZ 원본 완성형 + 과거 MC 후보 좌우 비교 JPG**를 직접 확인했다.
- 이번 기록에서 원본 Minecraft 모드 BBMODEL을 새로 로드/렌더링하지 않았다. 따라서 **'131~140 개별 정밀 재매칭 검수 완료'라고 집계하면 안 된다.**
- 확정 일치 0, 새 후보 검증 0. 기존 후보 9건은 구조상 부적합, 134번만 구조적 4구 오븐 조건부 대안이며 색상 미일치.
- 원본 TMX·PNG·기존 SQLite·최종 357종 카탈로그·누적 진행표를 변경하지 않았다.
- 별도 예약 작업 레인 A에서 131~140번 최종 원본 모델 실렌더를 할 때 중복 이미지 관찰을 줄이는 참고 자료다.

## 중요한 오류
- **131 Chest Freezer**: 상부에서 여는 흰색 수평형. 기존 dark_freezer는 세로형으로 다름.
- **132 Build-in Trailer Fridge**: 목재 언더카운터 안 은색 냉장고. 기존 dark_fridge는 분홍/검정 세로형 블록.
- **133 Black Fancy Chair**: 진한 갈색 천 쿠션과 둥근 높은 등받이, 팔걸이. 기존 black arm chair는 검은 직육면체 좌석.
- **134 Green Oven**: 4구 은회색 Decocraft Stove와 기본 구조는 같아 색상 및 둥근 화구·후방 뒷판을 별도 재검토해야 한다.
- **135 Simple Bed**: 2개의 PZ 타일로 이루어진 낮은 1인 침대. 기존 bunk bed는 2층 침대라 종류가 틀리다.
- **136 Birchwood Bench**: 2타일 길이의 등받이 없는 긴 평벤치와 금속 지지대 3개. 기존 birch bench 1인 등받이 의자와 다르다.
- **137 White Lazy Chair**: 크림 쿠션 1인 소파. 기존 oak chair 렌더는 구조 일부만 보임.
- **138 Low Toilet**: 뚜껑/물통 대신 금속 노출 밸브와 낮은 세면기 모양 변기. 기존 basic toilet은 대형 후방 물통형.
- **139 Floating Trailer Counter**: 갈색 목제 양문형 벽걸이 수납장. 기존 acacia counter는 색상·문/손잡이 누락.
- **140 Blue Comfy Couch**: 2타일 청록 둥근 소파(현재 뒷면이 잘 보임). 기존 blue_couch 한 칸 모양과 배치/둥근 요소가 다르다.

증거는 `analysis/rosewood_furniture/2026-10-31/all_357_complete_native_comparisons_v1/cards/131_PZ_MC.jpg`부터 `140_PZ_MC.jpg`까지.
다음 단계: 각 PZ 완성형 원본을 인접/방향별 확인하고 새 모드 실제 소스 BBMODEL과 텍스처를 렌더링, 10장의 새 비교 카드와 상세 검수 결과를 별도 브랜치에 저장할 것.
