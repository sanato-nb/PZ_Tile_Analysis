# 로즈우드 가구 32차 — 341~350 독립 시각 검수

2026-11-02: PZ 완성형 원본 10종과 기존 Minecraft 모델 렌더/부재 표시를 개별 육안 대조. 원본 Blockbench 렌더를 새로 실행하지 않았으며 기존 증거를 재사용했다.

- 조건부 1종: 346 검정 그랜드 피아노 (동일 물체 종류이지만 뚜껑 닫힘/열림, 형태 비율, 2×3 설치 미확인).
- 보류 9종: 341~345, 347~350. 342/343/344/347은 검증된 Minecraft 모델 부재, 345는 부분 JSON 렌더, 349는 레거시 근사 이미지.
- 350 수제 단층 침대에 2층 침대가 매칭된 심각한 오매칭, 349 4×1 가로 세탁소 간판에 세로 버스정류장 표지판이 매칭된 문제를 확인.
- Minecraft Forge 1.20.1 인게임 설치, 충돌·기능 및 정확한 1:1 승인: 0종.

## 증거 및 출처

- cards/: PZ 원본 PNG와 기존 Minecraft 비교 JPG를 바탕으로 생성한 판정 카드 10장
- BATCH_341_350_MANUAL_VISUAL_REVIEW.csv: 10종 개별 판정, 재질/형태/멀티타일 관찰, 후속 검증
- BATCH_341_350_DEFERRED_OTHER_MODS.csv: 보류 9종
- BATCH_341_350_SHA256_PROVENANCE.csv: PZ PNG, 기존 비교 JPG, 새 JPG SHA-256. 기존 모델 해시가 있는 경우 재해시가 아닌 과거 기록임
- MANIFEST.json, INDEX.html, ZIP: 독립 결과물
- 원본 TMX/PNG/SQLite, 타 레인 작업, 기존 누적표는 변경하지 않음. Draft PR은 자동 병합하지 않음.

## 개별 판정

- 341 Counter / White Floating Corner — DEFER: PZ는 밝은 아이보리색의 ㄱ자 형태로 한쪽에 파인 홈이 있으며 금속 줄무늬가 없다. Decocraft 후보는 청록색 금속 띠가 둘러진 검정 바닥 받침형 카운터로 색상, 표면, 설치 높이와 구조가 모두 다르다.
- 342 CustomName / Premium Technologies Ham — DEFER: PZ Premium Technologies Ham은 작은 회색 직육면체 본체와 검정 유선 핸드마이크가 연결된 탁상형 무전기다. Minecraft 측은 원본 검증 모델이 없어 형상·재질·기능 비교 자체가 불가능하다.
- 343 CustomName / US ARMY COMM. Ham — DEFER: PZ US ARMY COMM. Ham은 짙은 올리브색 군용 통신기 본체와 검정 유선 마이크를 갖는다. 원본 검증된 Minecraft 모델이 없으며 342번 회색 민간용과 색상·외형이 다르다.
- 344 CustomName / ValuTech — DEFER: PZ ValuTech는 작은 검정/회색 휴대용 라디오이며 상부 안테나와 전면 다이얼/표시부가 있다. Minecraft 후보 모델이 비어 있어 정확한 모델 비교가 불가능하다.
- 345 Generator / Old — DEFER: PZ Old 발전기는 원형 황색 부품과 노출된 엔진을 금속 파이프 프레임이 감싼 구조다. 기존 Minecraft 렌더는 검정 통풍구가 있는 막힌 직육면체로 원형 엔진·파이프 프레임이 없다. 또한 JSON 렌더는 부분 증거여서 전체 모델도 미확인.
- 346 Grand Piano / Black — CONDITIONAL: PZ와 Decocraft 후보는 모두 검정 그랜드 피아노이고 건반·페달·다리가 확인돼 물체 종류는 잘 맞는다. 그러나 PZ는 닫힌 둥근 곡면 상판인 반면 후보는 뚜껑이 열려 내부 현과 악보대가 드러난다. 다리 수·몸통 비율·2×3 배치와 기능은 확인되지 않았다.
- 347 HK533p / Imekagi — DEFER: PZ HK533p Imekagi는 높은 삼각대에 설치된 크림색/검정 카메라로 상부 뷰파인더와 렌즈/손잡이가 보인다. Minecraft 후보가 없어서 삼각대와 카메라 구조를 비교할 수 없다.
- 348 Shelves / Hardwood Wall Corner — DEFER: PZ Hardwood Wall Corner는 벽 모서리에 걸린 두 개의 얇은 ㄱ자 선반 판이며 하부가 완전히 열려 있다. Minecraft Handcrafted acacia_shelf 렌더는 큰 육면체 상자에 두 개의 검은 전면 틈이 있는 구조로 ㄱ자 판, 벽 코너 결합, 개방성이 재현되지 않는다.
- 349 Sign / Laundromat — DEFER: PZ는 가로로 네 타일 이어지는 세탁소 간판이다. 기존 후보는 세로형 파란 버스정류장 표지판으로 문구, 방향, 길이, 설치 방식이 전혀 다르며 기존 렌더도 LEGACY_3D_APPROXIMATION 등급이다.
- 350 Bed / Crafted — DEFER: PZ Crafted Bed는 낮은 단층 침대 1개로 갈색 목재 프레임과 흰 매트리스가 보인다. Minecraft 후보는 밝은 목재 사다리·난간이 있는 2층 침대여서 층수, 높이, 프레임 색상, 1×2 구조가 다르다.
