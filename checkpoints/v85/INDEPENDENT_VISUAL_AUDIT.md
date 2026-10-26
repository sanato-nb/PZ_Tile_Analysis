# v85 독립 시각 검수 기록

- 기준: v84 통합 SQLite `analysis_queue` 미관찰 1,820종 중 신규 48종.
- A 원본 PNG, B 같은 층 TMX 5×5, C 대상 배치 한 건 제거, D 다른 실제 사용 위치, 별도 비교판을 48종 모두 직접 열어 판독함.
- 직접 관찰 48, 잠정 후보 33, 보류 15. 공식 Local ID 매핑·TileZed 검증·최종 인증은 모두 0.
- 특히 B-C 0픽셀 또는 극소 변화가 있는 타일은 A에 형태가 보이더라도 후보로 확정하지 않고 보류함.
- TMX와 PNG의 높이 차이 및 근사 렌더러 한계로 모든 정체는 잠정적임.

## furniture_storage_02/33 — candidate

- 관찰: A에 짙은 갈색 곡선 장식 상판, 유리 진열문 한쪽, 하단 문짝·서랍이 있는 세로형 목재 수납장 조각이 보인다. B와 C의 실내 진열장 해당 반쪽이 달라지며 D에도 유사 진열장 배치가 있다.
- 잠정 정체: 갈색 유리 진열 수납장 반쪽
- 부품 역할: 곡선 상판·유리문·하단 수납부의 한쪽 세로 조각
- 신뢰도: high; B-C 변화: 4498px; TMX: 31_45.tmx 층0 (196,71); 누락 B=0.
- 증거: `checkpoints/v85_preview/furniture_storage_02__033_ABCD.jpg`

## furniture_storage_02/34 — candidate

- 관찰: A에 굽은 갈색 상판과 양면 유리처럼 보이는 좁은 진열장, 하단 수납문·서랍이 보인다. B-C에서 벽 옆 진열장 한 부분이 제거되고 D에서도 가구에 결합된다.
- 잠정 정체: 갈색 목제 유리 진열장 방향별 반쪽
- 부품 역할: 장식 상판과 유리문·하단 수납부의 반대 방향 조각
- 신뢰도: high; B-C 변화: 5063px; TMX: 31_45.tmx 층1 (155,9); 누락 B=0.
- 증거: `checkpoints/v85_preview/furniture_storage_02__034_ABCD.jpg`

## furniture_storage_02/35 — candidate

- 관찰: A에 갈색 곡선 상판·유리문 두 짝·내부 선반·아래 서랍과 수납문을 갖춘 높은 장이 보인다. B-C에서 거실 진열장 본체가 크게 사라진다.
- 잠정 정체: 갈색 2문 유리 진열장
- 부품 역할: 진열장 전체 또는 주된 본체 방향형
- 신뢰도: high; B-C 변화: 11202px; TMX: 31_45.tmx 층1 (156,9); 누락 B=0.
- 증거: `checkpoints/v85_preview/furniture_storage_02__035_ABCD.jpg`

## furniture_storage_02/42 — candidate

- 관찰: A에 누런 베이지색 세로 수납장 한쪽 문짝과 검은 손잡이, 상단·옆면이 열린 분할 모습. B-C에서 시설 내부의 장 일부가 제거된다.
- 잠정 정체: 베이지색 높은 수납장 반쪽
- 부품 역할: 높은 캐비닛의 한쪽 문·측판 분할
- 신뢰도: high; B-C 변화: 2868px; TMX: 31_45.tmx 층0 (191,107); 누락 B=0.
- 증거: `checkpoints/v85_preview/furniture_storage_02__042_ABCD.jpg`

## furniture_storage_02/43 — candidate

- 관찰: A에 얼룩진 크림색의 키 큰 수납장과 세로 문·측판·검은 손잡이가 보인다. B-C에서 매장 카운터 뒤 수납장 본체가 사라진다.
- 잠정 정체: 낡은 크림색 키 큰 수납장
- 부품 역할: 2문 수납장의 한 방향 완성형 또는 주된 본체
- 신뢰도: high; B-C 변화: 12691px; TMX: 31_45.tmx 층0 (156,25); 누락 B=0.
- 증거: `checkpoints/v85_preview/furniture_storage_02__043_ABCD.jpg`

## furniture_storage_02/46 — held

- 관찰: A에 누런 크림색 수납장 세로 판과 위쪽 돌출 상판이 보이나 B와 C가 동일하고 외벽 기둥에 가려 실제 기여를 확인하지 못한다.
- 잠정 정체: 보류
- 부품 역할: 키 큰 캐비닛 분할 부품으로 보이나 배치상 대응 불명
- 신뢰도: low; B-C 변화: 0px; TMX: 31_45.tmx 층0 (97,76); 누락 B=0.
- 증거: `checkpoints/v85_preview/furniture_storage_02__046_ABCD.jpg`

## furniture_storage_02/47 — held

- 관찰: A에 낡은 크림색 장의 직사각형 상판·측판이 보인다. B-C 변화 0으로 주어진 TMX 위치에서 실제 수납장 기여가 분리되지 않는다.
- 잠정 정체: 보류
- 부품 역할: 수납장 방향별 조각으로 추정되지만 장면 근거 보류
- 신뢰도: low; B-C 변화: 0px; TMX: 31_45.tmx 층0 (146,31); 누락 B=0.
- 증거: `checkpoints/v85_preview/furniture_storage_02__047_ABCD.jpg`

## furniture_tables_low_01/0 — candidate

- 관찰: A에 갈색 직사각형 목재 상판과 네 모서리의 짧고 굵은 다리가 보인다. B-C에서 거실 소파 앞의 낮은 탁자가 빠지고 D에서도 소파 사이 탁자다.
- 잠정 정체: 낮은 갈색 목제 커피 테이블
- 부품 역할: 거실용 단일 낮은 탁자
- 신뢰도: high; B-C 변화: 4872px; TMX: 31_45.tmx 층0 (52,236); 누락 B=0.
- 증거: `checkpoints/v85_preview/furniture_tables_low_01__000_ABCD.jpg`

## d_plants_1/36 — candidate

- 관찰: A에 가는 회갈색 줄기 세 개와 마디마다 달린 길쭉한 녹색 잎이 보인다. B-C에서 흙 화단의 한 식물 덩어리가 줄고 D에서는 건물 외벽 아래 잡초로 배치된다.
- 잠정 정체: 곧게 자란 녹색 잡초 줄기 묶음
- 부품 역할: 야외 화단·외벽 하단의 키 큰 풀 3포기
- 신뢰도: high; B-C 변화: 2974px; TMX: 31_45.tmx 층0 (246,175); 누락 B=4.
- 증거: `checkpoints/v85_preview/d_plants_1__036_ABCD.jpg`

## d_plants_1/37 — candidate

- 관찰: A는 땅에 낮게 모인 진녹색 다엽 식물 덩어리. B-C에서 흙밭의 한 포기만 제거되며 D에도 화단에 배치된다.
- 잠정 정체: 낮고 둥근 잎의 덤불형 잡초
- 부품 역할: 화단의 낮은 관목·풀 군락
- 신뢰도: high; B-C 변화: 5276px; TMX: 31_45.tmx 층0 (246,170); 누락 B=3.
- 증거: `checkpoints/v85_preview/d_plants_1__037_ABCD.jpg`

## d_plants_1/53 — candidate

- 관찰: A에 연녹색 좁은 잎이 여러 갈래 솟은 낮은 풀 무더기가 보인다. B-C에서 보도 옆 길쭉한 화단 일부가 제거된다.
- 잠정 정체: 길쭉한 잎의 작은 잡초 덤불
- 부품 역할: 보도변 화단을 채우는 녹색 풀 포기
- 신뢰도: high; B-C 변화: 3859px; TMX: 31_45.tmx 층0 (228,51); 누락 B=0.
- 증거: `checkpoints/v85_preview/d_plants_1__053_ABCD.jpg`

## d_plants_1/54 — candidate

- 관찰: A에 초록색 줄기와 가늘고 긴 잎이 낮게 뒤섞인 식물 포기가 보인다. B-C에서 보도변 화단의 한 조각이 사라진다.
- 잠정 정체: 작은 잎이 빽빽한 잡초 포기
- 부품 역할: 보도 경계 화단의 낮은 풀 군락
- 신뢰도: high; B-C 변화: 4224px; TMX: 31_45.tmx 층0 (220,51); 누락 B=0.
- 증거: `checkpoints/v85_preview/d_plants_1__054_ABCD.jpg`

## d_wallcracks_1/18 — held

- 관찰: A에 아주 작은 회색 점·가느다란 갈라진 선 두 조각이 떨어져 보인다. B-C는 25픽셀 차이에 그쳐 돌담에서 어떤 균열이 실제로 사라졌는지 구분하기 어렵다.
- 잠정 정체: 보류
- 부품 역할: 회색 벽면 균열·긁힘 오버레이처럼 보이나 장면 근거 부족
- 신뢰도: low; B-C 변화: 25px; TMX: 31_45.tmx 층-1 (139,52); 누락 B=0.
- 증거: `checkpoints/v85_preview/d_wallcracks_1__018_ABCD.jpg`

## d_wallcracks_1/46 — candidate

- 관찰: A에 서로 떨어진 세 군데 회색 나뭇가지형 선이 있고 가운데는 세로로 분기한다. B-C에서 지하 석조벽의 가는 금 모양이 변한다.
- 잠정 정체: 석조벽에 얹는 회색 갈라짐 자국
- 부품 역할: 벽면 손상·균열 오버레이의 여러 갈래 조각
- 신뢰도: medium; B-C 변화: 1012px; TMX: 31_45.tmx 층-1 (139,56); 누락 B=1.
- 증거: `checkpoints/v85_preview/d_wallcracks_1__046_ABCD.jpg`

## d_wallcracks_1/51 — candidate

- 관찰: A에 위쪽 Y자형 가는 회색 선과 아래쪽으로 긴 갈라진 선, 작은 파편이 보인다. B-C에서 석조벽 일부에 가는 금이 제거된다.
- 잠정 정체: 분기된 회색 벽 균열 무늬
- 부품 역할: 석조벽 표면 손상 장식 오버레이
- 신뢰도: medium; B-C 변화: 826px; TMX: 31_45.tmx 층-1 (143,61); 누락 B=2.
- 증거: `checkpoints/v85_preview/d_wallcracks_1__051_ABCD.jpg`

## d_wallcracks_1/52 — candidate

- 관찰: A에 상단의 짧은 회색 가지형 선, 중간의 세로 금과 하단의 여러 가느다란 갈라짐이 분리돼 보인다. B-C에서 석조벽 손상선이 달라진다.
- 잠정 정체: 여러 갈래의 회색 석조벽 금
- 부품 역할: 벽 균열·파손 오버레이의 방향별 조각
- 신뢰도: medium; B-C 변화: 858px; TMX: 31_45.tmx 층-1 (146,62); 누락 B=1.
- 증거: `checkpoints/v85_preview/d_wallcracks_1__052_ABCD.jpg`

## f_wallvines_1/25 — candidate

- 관찰: A에 잎이 전혀 없는 갈색 가는 줄기 여러 개가 위로 얽혀 뻗는다. B-C에서 벽돌 외벽 옆 마른 가지 한 덩어리가 사라진다.
- 잠정 정체: 잎 없는 마른 덩굴
- 부품 역할: 외벽을 타고 자란 갈색 잔가지의 세로 오버레이
- 신뢰도: high; B-C 변화: 3201px; TMX: 31_45.tmx 층0 (205,89); 누락 B=1.
- 증거: `checkpoints/v85_preview/f_wallvines_1__025_ABCD.jpg`

## f_wallvines_1/30 — candidate

- 관찰: A에 길고 가는 갈색 가지 세 무리가 겹치며 위쪽으로 갈라진다. B-C에서 울타리와 벽돌벽에 기대 선 마른 줄기 일부가 제거된다.
- 잠정 정체: 길게 자란 마른 벽덩굴
- 부품 역할: 외벽·울타리 세로 방향의 여러 줄기 조합
- 신뢰도: high; B-C 변화: 4325px; TMX: 31_45.tmx 층0 (205,90); 누락 B=1.
- 증거: `checkpoints/v85_preview/f_wallvines_1__030_ABCD.jpg`

## f_wallvines_1/33 — candidate

- 관찰: A에 갈색 잔가지가 세로로 얽혀 있고 밑부분은 여러 줄기로 나뉜다. B-C에서 출입문 옆 벽돌벽 하단의 가는 가지가 빠진다.
- 잠정 정체: 잎 없는 세로 덩굴 줄기
- 부품 역할: 외벽 하부에서 올라오는 마른 덩굴 분할 조각
- 신뢰도: high; B-C 변화: 2756px; TMX: 31_45.tmx 층0 (123,86); 누락 B=2.
- 증거: `checkpoints/v85_preview/f_wallvines_1__033_ABCD.jpg`

## f_wallvines_1/39 — candidate

- 관찰: A에 긴 갈색 줄기와 촘촘한 Y자 분지가 두 갈래로 서 있다. B-C에서 흰 외벽과 벽돌 모서리에 붙은 가지 무리가 제거된다.
- 잠정 정체: 잎 없는 마른 덩굴 군락
- 부품 역할: 외벽 높이 방향의 다중 줄기 오버레이
- 신뢰도: high; B-C 변화: 3850px; TMX: 31_45.tmx 층0 (120,86); 누락 B=0.
- 증거: `checkpoints/v85_preview/f_wallvines_1__039_ABCD.jpg`

## floors_interior_carpet_01/0 — candidate

- 관찰: A는 전체가 균일한 어두운 청회색 직물 질감의 평면 마름모 바닥 조각. B-C에서 탁자 밑 파란 바닥의 한 칸이 사라진다.
- 잠정 정체: 청회색 실내 카펫 바닥
- 부품 역할: 실내 바닥 한 칸을 덮는 단색 카펫
- 신뢰도: high; B-C 변화: 1050px; TMX: 31_45.tmx 층0 (220,28); 누락 B=0.
- 증거: `checkpoints/v85_preview/floors_interior_carpet_01__000_ABCD.jpg`

## floors_interior_carpet_01/8 — candidate

- 관찰: A에 진한 적갈색의 촘촘한 평행 가로줄이 있는 평면 마름모가 보인다. B-C에서 라커 앞 바닥 한 칸이 하얗게 빠지며 D에도 같은 실내 바닥 무늬가 있다.
- 잠정 정체: 진갈색 줄무늬 실내 바닥재
- 부품 역할: 갈색 선형 패턴 바닥 한 칸; 직물인지 판재인지 미확정
- 신뢰도: medium; B-C 변화: 2248px; TMX: 31_45.tmx 층-1 (142,21); 누락 B=0.
- 증거: `checkpoints/v85_preview/floors_interior_carpet_01__008_ABCD.jpg`

## floors_interior_carpet_01/9 — candidate

- 관찰: A에 미세한 결이 있는 붉은 갈색 단색 바닥 마름모가 보인다. B-C에서 침실 바닥 일부가 바뀐다.
- 잠정 정체: 적갈색 실내 카펫 바닥
- 부품 역할: 실내 바닥의 단색 붉은 카펫 한 칸
- 신뢰도: high; B-C 변화: 208px; TMX: 31_45.tmx 층1 (147,41); 누락 B=0.
- 증거: `checkpoints/v85_preview/floors_interior_carpet_01__009_ABCD.jpg`

## floors_interior_carpet_01/10 — held

- 관찰: A는 연한 노란 베이지색 직물 질감의 마름모 바닥 조각이다. B-C 변화 0으로 선택 위치의 바닥 기여가 다른 레이어에 가려져 분리되지 않는다.
- 잠정 정체: 보류
- 부품 역할: 연노랑 실내 바닥재로 보이나 장면 근거 부족
- 신뢰도: low; B-C 변화: 0px; TMX: 31_45.tmx 층0 (110,36); 누락 B=0.
- 증거: `checkpoints/v85_preview/floors_interior_carpet_01__010_ABCD.jpg`

## floors_interior_carpet_01/13 — candidate

- 관찰: A는 검갈색 바닥 마름모에 촘촘한 평행 세로줄과 섬유 질감이 보인다. B-C에서 사무실 책상 밑 한 칸이 사라진다.
- 잠정 정체: 짙은 갈색 줄무늬 카펫 바닥
- 부품 역할: 사무실용 어두운 줄무늬 바닥 한 칸
- 신뢰도: high; B-C 변화: 973px; TMX: 31_45.tmx 층0 (149,41); 누락 B=0.
- 증거: `checkpoints/v85_preview/floors_interior_carpet_01__013_ABCD.jpg`

## floors_interior_carpet_01/33 — candidate

- 관찰: A는 올리브색 바탕에 어두운 녹색 평행 줄무늬가 있는 마름모 바닥. B-C에서 녹색 벽 앞 바닥 한 칸이 빠진다.
- 잠정 정체: 올리브 녹색 줄무늬 카펫
- 부품 역할: 실내 카펫 바닥 한 칸
- 신뢰도: high; B-C 변화: 3840px; TMX: 31_45.tmx 층0 (70,0); 누락 B=0.
- 증거: `checkpoints/v85_preview/floors_interior_carpet_01__033_ABCD.jpg`

## floors_interior_carpet_01/36 — candidate

- 관찰: A는 연갈색·황토색 평행 결을 가진 바닥 조각. B-C에서 주황 소파 앞 거실 바닥 한 칸이 사라진다.
- 잠정 정체: 황갈색 줄무늬 실내 카펫
- 부품 역할: 거실용 황갈색 바닥 한 칸
- 신뢰도: high; B-C 변화: 1443px; TMX: 31_45.tmx 층0 (7,0); 누락 B=0.
- 증거: `checkpoints/v85_preview/floors_interior_carpet_01__036_ABCD.jpg`

## floors_interior_carpet_01/37 — candidate

- 관찰: A는 청회색 바탕에 옅은 푸른 줄무늬가 촘촘한 마름모. B-C에서 침실 침대 옆 바닥 한 칸이 제거된다.
- 잠정 정체: 파란색 줄무늬 카펫
- 부품 역할: 침실 바닥의 푸른 카펫 한 칸
- 신뢰도: high; B-C 변화: 1116px; TMX: 31_45.tmx 층1 (240,111); 누락 B=0.
- 증거: `checkpoints/v85_preview/floors_interior_carpet_01__037_ABCD.jpg`

## floors_interior_carpet_01/40 — candidate

- 관찰: A는 청록색 바탕에 어두운 녹색의 가는 평행 줄이 보인다. B-C에서 사무실 바닥 한 칸이 빠진다.
- 잠정 정체: 청록색 줄무늬 카펫
- 부품 역할: 실내 사무실 바닥 한 칸
- 신뢰도: high; B-C 변화: 1194px; TMX: 31_45.tmx 층0 (137,36); 누락 B=0.
- 증거: `checkpoints/v85_preview/floors_interior_carpet_01__040_ABCD.jpg`

## floors_interior_carpet_01/42 — candidate

- 관찰: A는 자주빛·보라색 바탕에 검붉은 평행 직물 줄무늬가 있다. B-C에서 서랍장과 의자 사이 바닥 한 칸이 사라진다.
- 잠정 정체: 자주색 줄무늬 카펫
- 부품 역할: 보라색 실내 카펫 한 칸
- 신뢰도: high; B-C 변화: 1736px; TMX: 31_45.tmx 층1 (150,36); 누락 B=0.
- 증거: `checkpoints/v85_preview/floors_interior_carpet_01__042_ABCD.jpg`

## floors_interior_carpet_01/43 — candidate

- 관찰: A는 어두운 와인색 바탕에 선명한 갈색·적갈색 평행 줄이 있다. B-C에서 침실 침대 옆 바닥 한 칸이 제거된다.
- 잠정 정체: 와인색 줄무늬 카펫
- 부품 역할: 침실용 적갈색 카펫 한 칸
- 신뢰도: high; B-C 변화: 569px; TMX: 31_45.tmx 층1 (9,4); 누락 B=0.
- 증거: `checkpoints/v85_preview/floors_interior_carpet_01__043_ABCD.jpg`

## floors_interior_carpet_01/44 — candidate

- 관찰: A는 회색 바탕에 옅은 회백색 평행 직물 줄무늬가 있다. B-C에서 연회색 거실 바닥 한 칸이 사라진다.
- 잠정 정체: 회색 줄무늬 카펫
- 부품 역할: 실내 회색 카펫 바닥 한 칸
- 신뢰도: high; B-C 변화: 631px; TMX: 31_45.tmx 층2 (146,32); 누락 B=0.
- 증거: `checkpoints/v85_preview/floors_interior_carpet_01__044_ABCD.jpg`

## floors_interior_carpet_01/45 — candidate

- 관찰: A는 회갈색 바탕에 짙은 보라색 평행 줄무늬가 있는 바닥 마름모. B-C에서 당구대가 있는 방의 바닥 한 칸이 사라진다.
- 잠정 정체: 회갈색·보라색 줄무늬 카펫
- 부품 역할: 실내 오락실 바닥 한 칸
- 신뢰도: high; B-C 변화: 2588px; TMX: 31_45.tmx 층1 (7,0); 누락 B=0.
- 증거: `checkpoints/v85_preview/floors_interior_carpet_01__045_ABCD.jpg`

## floors_interior_carpet_01/46 — held

- 관찰: A에 진갈색 줄무늬 마름모 바닥 조각이 보이지만 B-C 변화 0이다. 계단 아래 라커 공간에서 해당 배치의 독립적인 노출이 확인되지 않는다.
- 잠정 정체: 보류
- 부품 역할: 진갈색 카펫/바닥재 한 칸처럼 보이나 실제 기여 미확인
- 신뢰도: low; B-C 변화: 0px; TMX: 31_45.tmx 층-1 (118,29); 누락 B=0.
- 증거: `checkpoints/v85_preview/floors_interior_carpet_01__046_ABCD.jpg`

## floors_interior_carpet_01/47 — candidate

- 관찰: A는 황갈색 바탕에 얇은 짙은 갈색 평행 선을 지닌 바닥 마름모. B-C에서 거실 TV 앞의 바닥 한 칸이 제거된다.
- 잠정 정체: 황갈색 줄무늬 카펫
- 부품 역할: 거실·침실의 갈색 실내 바닥 한 칸
- 신뢰도: high; B-C 변화: 1680px; TMX: 31_45.tmx 층0 (65,221); 누락 B=0.
- 증거: `checkpoints/v85_preview/floors_interior_carpet_01__047_ABCD.jpg`

## floors_interior_tilesandwood_01/1 — held

- 관찰: A는 검푸른색과 아이보리색이 교대로 놓인 격자형 사각 타일이다. B-C 변화 0으로 화장실 바닥의 한 배치가 다른 층과 중첩됐을 가능성을 배제할 수 없다.
- 잠정 정체: 보류
- 부품 역할: 흑백 체크 바닥 타일로 보이나 이 위치에서 직접 기여 미확인
- 신뢰도: low; B-C 변화: 0px; TMX: 31_45.tmx 층0 (154,76); 누락 B=0.
- 증거: `checkpoints/v85_preview/floors_interior_tilesandwood_01__001_ABCD.jpg`

## floors_interior_tilesandwood_01/2 — held

- 관찰: A에 하늘색과 흰색 사각 타일이 바둑판처럼 배열되어 있다. B-C 변화 0이며 욕실 바닥의 선택 배치가 다른 타일에 가려진다.
- 잠정 정체: 보류
- 부품 역할: 청백 체크 바닥 타일로 보이나 배치 분리 보류
- 신뢰도: low; B-C 변화: 0px; TMX: 31_45.tmx 층0 (10,6); 누락 B=0.
- 증거: `checkpoints/v85_preview/floors_interior_tilesandwood_01__002_ABCD.jpg`

## floors_interior_tilesandwood_01/4 — held

- 관찰: A는 회색과 거의 검은색의 정사각 격자 타일 4×4 형태. B-C 변화 0으로 공중화장실의 타일 한 칸에 대한 기여가 확인되지 않는다.
- 잠정 정체: 보류
- 부품 역할: 흑회색 체크 바닥 타일로 보이나 장면 증거 불충분
- 신뢰도: low; B-C 변화: 0px; TMX: 31_45.tmx 층0 (193,22); 누락 B=0.
- 증거: `checkpoints/v85_preview/floors_interior_tilesandwood_01__004_ABCD.jpg`

## floors_interior_tilesandwood_01/7 — candidate

- 관찰: A에는 검정·흰색이 번갈아 놓인 네 개의 큰 사각 타일이 보인다. B-C에서 소파 사이 바닥의 일부가 사라지고 D도 실내 체크 바닥으로 쓰인다.
- 잠정 정체: 흑백 대형 체크 타일 바닥
- 부품 역할: 실내 바닥 한 칸의 2×2 체크 패턴
- 신뢰도: high; B-C 변화: 638px; TMX: 31_45.tmx 층0 (239,161); 누락 B=0.
- 증거: `checkpoints/v85_preview/floors_interior_tilesandwood_01__007_ABCD.jpg`

## floors_interior_tilesandwood_01/9 — held

- 관찰: A는 밝은 노란색 작은 사각 타일의 격자 바닥 조각이다. B-C 변화 0이므로 매장/욕실에 보이는 바닥이 이 배치의 결과인지 확인되지 않는다.
- 잠정 정체: 보류
- 부품 역할: 노란색 정사각 타일 바닥처럼 보이나 기여 미확인
- 신뢰도: low; B-C 변화: 0px; TMX: 31_45.tmx 층0 (183,76); 누락 B=0.
- 증거: `checkpoints/v85_preview/floors_interior_tilesandwood_01__009_ABCD.jpg`

## floors_interior_tilesandwood_01/10 — held

- 관찰: A는 베이지색 작은 정사각 타일들이 촘촘한 줄눈으로 구획된 바닥이다. B-C 변화 0으로 복도와 화장실 앞 선택 배치의 직접 노출을 확인할 수 없다.
- 잠정 정체: 보류
- 부품 역할: 작은 베이지 타일 바닥으로 보이나 배치 기여 미확인
- 신뢰도: low; B-C 변화: 0px; TMX: 31_45.tmx 층0 (142,32); 누락 B=0.
- 증거: `checkpoints/v85_preview/floors_interior_tilesandwood_01__010_ABCD.jpg`

## floors_interior_tilesandwood_01/15 — held

- 관찰: A에 연회색 큰 타일 네 장과 중앙의 작은 녹회색 정사각 장식이 보인다. B-C 변화 0이고 다른 층 바닥과 겹친다.
- 잠정 정체: 보류
- 부품 역할: 회백색 장식 바닥 타일처럼 보이나 장면 근거 보류
- 신뢰도: low; B-C 변화: 0px; TMX: 31_45.tmx 층0 (243,111); 누락 B=1.
- 증거: `checkpoints/v85_preview/floors_interior_tilesandwood_01__015_ABCD.jpg`

## floors_interior_tilesandwood_01/16 — held

- 관찰: A는 옅은 회베이지색 미세 결의 거의 단색 바닥 마름모. B-C 변화 0이어서 세탁실·복도 바닥에서 독립적인 변화를 관찰하지 못했다.
- 잠정 정체: 보류
- 부품 역할: 밝은 단색 바닥 타일처럼 보이나 검증 보류
- 신뢰도: low; B-C 변화: 0px; TMX: 31_45.tmx 층0 (116,135); 누락 B=0.
- 증거: `checkpoints/v85_preview/floors_interior_tilesandwood_01__016_ABCD.jpg`

## floors_interior_tilesandwood_01/21 — held

- 관찰: A는 녹회색 두 칸과 크림색 두 칸이 교차한 2×2 바닥 타일이다. B-C 변화 0으로 지하 계단 옆 바닥에 대한 단일 배치 기여가 없다.
- 잠정 정체: 보류
- 부품 역할: 회녹색·아이보리색 체크 타일로 보이나 기여 미확인
- 신뢰도: low; B-C 변화: 0px; TMX: 31_45.tmx 층0 (144,43); 누락 B=0.
- 증거: `checkpoints/v85_preview/floors_interior_tilesandwood_01__021_ABCD.jpg`

## floors_interior_tilesandwood_01/22 — candidate

- 관찰: A는 진한 남보라색과 회보라색이 교차한 2×2 바닥 타일이다. B-C에서 카페 탁자 아래 바닥 한 칸이 사라지고 D도 동일한 바닥 무늬다.
- 잠정 정체: 남보라·회보라 체크 바닥 타일
- 부품 역할: 상업 공간 바닥 한 칸의 2×2 체크 패턴
- 신뢰도: high; B-C 변화: 3045px; TMX: 31_45.tmx 층0 (181,22); 누락 B=0.
- 증거: `checkpoints/v85_preview/floors_interior_tilesandwood_01__022_ABCD.jpg`

## floors_interior_tilesandwood_01/25 — held

- 관찰: A에는 네 개의 흰색 큰 사각 타일이 중앙과 모서리의 적갈색 작은 사각 장식으로 만난다. B-C 변화 0이어서 욕실 바닥 기여를 확인할 수 없다.
- 잠정 정체: 보류
- 부품 역할: 흰색·붉은 장식 타일 바닥처럼 보이나 해당 배치 근거 부족
- 신뢰도: low; B-C 변화: 0px; TMX: 31_45.tmx 층0 (98,34); 누락 B=0.
- 증거: `checkpoints/v85_preview/floors_interior_tilesandwood_01__025_ABCD.jpg`

## floors_interior_tilesandwood_01/26 — held

- 관찰: A는 흰색 큰 타일 네 개의 교차점마다 청회색 작은 사각 장식이 들어간 패턴. B-C 변화 0으로 욕실의 다른 타일과 중첩된다.
- 잠정 정체: 보류
- 부품 역할: 흰색·파란 장식 타일로 보이나 실제 기여 미확인
- 신뢰도: low; B-C 변화: 0px; TMX: 31_45.tmx 층1 (147,25); 누락 B=0.
- 증거: `checkpoints/v85_preview/floors_interior_tilesandwood_01__026_ABCD.jpg`

## floors_interior_tilesandwood_01/27 — candidate

- 관찰: A에 흰색 큰 타일 네 장과 교차점의 작은 검은 정사각 장식이 보인다. B-C에서 실내 테이블 아래 한 칸이 빠지고 D에서도 흰색·검은 점 타일이다.
- 잠정 정체: 흰색 바닥의 검은 점 장식 타일
- 부품 역할: 흰색 사각 바닥 타일 4분할·검정 작은 사각 접점
- 신뢰도: high; B-C 변화: 3180px; TMX: 31_45.tmx 층0 (73,0); 누락 B=0.
- 증거: `checkpoints/v85_preview/floors_interior_tilesandwood_01__027_ABCD.jpg`
