# v86 독립 이미지 판독·보류 감사 기록

- 기준: v85 물리 통합 SQLite `analysis_queue` 미관찰 1,772종에서 신규 12종.
- GitHub 원본 PNG 및 두 TMX를 사용해 A 원본, B 동일 층 5×5, C 선택 배치 하나 제거, D 다른 실제 사용 위치, 비교판을 생성하고 **12개 비교판을 직접 열어 육안 판독**함.
- 이미지 직접 관찰 12종, 잠정 후보 7종, 보류 5종. 모든 Local ID 공식 매핑·TileZed 정합·최종 인증은 미완료(0종).
- B-C 변화가 0~4픽셀인 바닥·러그 5종은 A의 패턴만 보고 정체를 단정하지 않고 보류함.
- 이 증거는 TileZed 렌더가 아닌 근사 조립이며 모든 PNG는 `height_mismatch`로 표시되어 있음.
- 기존 v85 이하 DB, 이전 체크포인트 및 사용자 수동 검수 80종을 변경하지 않음.

## furniture_tables_low_01/1 — candidate

- 관찰: A에 직사각형 갈색 나뭇결 상판과 짧은 다리, 아래 가로판이 보인다. B 소파 앞 낮은 탁자가 C에서 사라지며 D에서도 좌석 사이에 같은 낮은 탁자가 배치된다.
- 잠정 정체: 갈색 낮은 목제 커피 테이블
- 부품 역할: 거실 탁자 단일 조각
- 신뢰도: high; B-C 4055px; TMX 31_45.tmx 층 0 (52,235); 주변 PNG 누락 B=0.
- 증거: `checkpoints/v86_preview/furniture_tables_low_01__001_ABCD.jpg`

## floors_interior_tilesandwood_01/31 — candidate

- 관찰: A에 짙은 갈색과 올리브색이 교대로 놓인 네 칸 사각 타일이 보인다. B 주방 바닥의 같은 체크 무늬 한 칸이 C에서 제거되어 밝은 빈 부분이 생기며 D의 주방에도 이어진다.
- 잠정 정체: 갈색·올리브색 2×2 체크 주방 바닥 타일
- 부품 역할: 바닥 한 칸을 채우는 반복 패턴
- 신뢰도: medium; B-C 1146px; TMX 31_45.tmx 층 0 (102,9); 주변 PNG 누락 B=0.
- 증거: `checkpoints/v86_preview/floors_interior_tilesandwood_01__031_ABCD.jpg`

## floors_interior_tilesandwood_01/32 — candidate

- 관찰: A에 붉은 갈색 정사각 타일과 가는 어두운 격자선이 보인다. B 주방 바닥에 반복 배치되고 C에서 한 칸이 빠진다. D에서는 가구와 벽에 가려 전체 무늬가 제한적으로 보인다.
- 잠정 정체: 붉은 갈색 소형 격자 바닥 타일
- 부품 역할: 주방 바닥 반복 단위
- 신뢰도: medium; B-C 566px; TMX 31_45.tmx 층 0 (98,39); 주변 PNG 누락 B=1.
- 증거: `checkpoints/v86_preview/floors_interior_tilesandwood_01__032_ABCD.jpg`

## floors_interior_tilesandwood_01/35 — candidate

- 관찰: A에 베이지색 작은 정사각 격자가 촘촘히 보인다. B 주방 바닥에 이어지며 C에서 냉장고 옆 한 칸이 사라져 흰 바닥이 드러난다. D에서도 같은 계열 타일이 보인다.
- 잠정 정체: 베이지색 작은 격자 주방 바닥 타일
- 부품 역할: 주방 바닥 반복 패턴 한 칸
- 신뢰도: medium; B-C 905px; TMX 31_45.tmx 층 0 (240,117); 주변 PNG 누락 B=0.
- 증거: `checkpoints/v86_preview/floors_interior_tilesandwood_01__035_ABCD.jpg`

## floors_interior_tilesandwood_01/44 — held

- 관찰: A에는 따뜻한 갈색의 긴 목재 판재들이 평행하게 놓인 바닥 조각이 보인다. B와 C 차이는 4픽셀로 거의 구분되지 않고 D에서도 다른 바닥과 가구가 겹쳐 선택 배치 기여를 특정하기 어렵다.
- 잠정 정체: 보류
- 부품 역할: 갈색 판재형 바닥 텍스처로 보이나 배치 대응 보류
- 신뢰도: low; B-C 4px; TMX 31_45.tmx 층 0 (97,9); 주변 PNG 누락 B=0.
- 증거: `checkpoints/v86_preview/floors_interior_tilesandwood_01__044_ABCD.jpg`

## floors_interior_tilesandwood_01/47 — held

- 관찰: A에 짙은 갈색 목재 마루 판재의 길이 방향 이음선이 보인다. B의 실내 바닥과 D의 유사 바닥은 확인되지만 B-C 차이가 2픽셀에 불과해 대상 한 칸의 실제 가시 기여를 분리할 수 없다.
- 잠정 정체: 보류
- 부품 역할: 짙은 갈색 목재 마루 한 칸으로 추정하되 보류
- 신뢰도: low; B-C 2px; TMX 31_45.tmx 층 0 (118,123); 주변 PNG 누락 B=0.
- 증거: `checkpoints/v86_preview/floors_interior_tilesandwood_01__047_ABCD.jpg`

## floors_interior_tilesandwood_01/49 — held

- 관찰: A에는 밝은 황갈색 직사각 목재 블록들이 교차 배열된 패턴이 보인다. B와 C가 0픽셀 차이이고 D 주방 바닥의 유사 패턴도 선택 배치와 직접 연결해 검증하지 못했다.
- 잠정 정체: 보류
- 부품 역할: 밝은 목재 블록형 바닥 패턴으로 보이나 배치 기여 불명
- 신뢰도: low; B-C 0px; TMX 31_45.tmx 층 0 (51,231); 주변 PNG 누락 B=0.
- 증거: `checkpoints/v86_preview/floors_interior_tilesandwood_01__049_ABCD.jpg`

## floors_interior_tilesandwood_01/50 — candidate

- 관찰: A에 진한 황갈색 직사각 목재 블록이 교차한 패턴이 보인다. B의 식탁 주변 마루와 C의 제거 자리에 차이가 나타나며 D에도 비슷한 목재 블록형 바닥이 있다.
- 잠정 정체: 황갈색 직사각 블록형 목재 마루
- 부품 역할: 실내 바닥 반복 단위
- 신뢰도: medium; B-C 757px; TMX 31_46.tmx 층 0 (78,120); 주변 PNG 누락 B=0.
- 증거: `checkpoints/v86_preview/floors_interior_tilesandwood_01__050_ABCD.jpg`

## floors_rugs_01/0 — candidate

- 관찰: A에 어두운 청록색 직물 면과 옅은 녹회색 이중 테두리가 한쪽으로 꺾이는 부분이 보인다. B의 가구 뒤 카펫 가장자리는 벽에 가려 변화가 작지만 C에서 일부 변화가 있고 D 거실에서 큰 직사각 러그의 테두리 연결을 확인한다.
- 잠정 정체: 청록색 직사각 테두리 러그의 모서리 조각
- 부품 역할: 큰 러그의 한쪽 테두리·모서리
- 신뢰도: low; B-C 151px; TMX 31_45.tmx 층 0 (193,47); 주변 PNG 누락 B=0.
- 증거: `checkpoints/v86_preview/floors_rugs_01__000_ABCD.jpg`

## floors_rugs_01/1 — held

- 관찰: A에는 짙은 청록색 직물과 안쪽 직각 테두리, 바깥쪽 옅은 녹색 띠가 보인다. B에서는 벽에 가려지고 C와 차이가 0픽셀이다. D에는 비슷한 러그가 있으나 개별 조각의 가시 기여는 확인되지 않는다.
- 잠정 정체: 보류
- 부품 역할: 테두리 러그의 분할 모서리로 추정하되 보류
- 신뢰도: low; B-C 0px; TMX 31_45.tmx 층 0 (194,47); 주변 PNG 누락 B=0.
- 증거: `checkpoints/v86_preview/floors_rugs_01__001_ABCD.jpg`

## floors_rugs_01/2 — candidate

- 관찰: A에 청록색 직물 바탕과 한쪽 가장자리를 따라 길게 뻗은 옅은 녹색 테두리 두 줄이 보인다. B 거실 러그의 길쭉한 부분이 C에서 사라지고 D에도 큰 직사각 러그의 가장자리로 사용된다.
- 잠정 정체: 청록색 테두리 러그의 긴 변 조각
- 부품 역할: 직사각 러그의 가장자리 분할
- 신뢰도: medium; B-C 2460px; TMX 31_45.tmx 층 0 (193,46); 주변 PNG 누락 B=0.
- 증거: `checkpoints/v86_preview/floors_rugs_01__002_ABCD.jpg`

## floors_rugs_01/3 — held

- 관찰: A에 청록색 직물과 대각 방향으로 놓인 녹회색 테두리 띠가 보인다. B의 가구·벽 아래에 겹치고 C와 차이가 0픽셀이다. D에서도 같은 부분의 기여를 단독으로 분리할 수 없다.
- 잠정 정체: 보류
- 부품 역할: 청록색 러그 가장자리 분할로 추정하되 보류
- 신뢰도: low; B-C 0px; TMX 31_45.tmx 층 0 (194,46); 주변 PNG 누락 B=0.
- 증거: `checkpoints/v86_preview/floors_rugs_01__003_ABCD.jpg`

