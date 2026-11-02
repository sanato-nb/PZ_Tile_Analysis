# 로즈우드 B 레인 31차 — 291~300 개별 시각 검수

PZ 원본 완성형 조립 미리보기 10종과 기존 Minecraft 원본 소스 기반 비교 JPG 10개를 실제로 열어 각각 관찰했다.
이번 실행에서 Blockbench를 새로 구동한 것은 아니며, 기존 원본 소스 기반 렌더를 재사용했다.
원본 PZ 미리보기는 임시 조립 상태일 수 있어 구조적 불일치 판정의 제한을 함께 기록한다.

- 개별 검수 10종 / 조건부 0종 / 보류 10종 / 1:1 인증 0종.
- 296·297의 Minecraft JSON 스크린샷은 부분 렌더이므로 완성 모델의 외형 증거로 승인하지 않는다.
- 294·295에는 검증된 MC 모델이 없으며 우측은 안내 카드이므로 실제 모델 비교가 아니다.
- 298·299는 서로 반대 방향의 유리 진열 코너인데 동일한 불투명 검정 카운터가 후보로 지정돼 있다.
- Minecraft Forge 1.20.1 설치·충돌·방향·기능 검증은 수행되지 않았다.

## 검증 자료

- cards/: 기존 이미지로부터 새로 제작한 개별 좌우 비교 JPG 10장.
- BATCH_291_300_MANUAL_VISUAL_REVIEW.csv: 10개 외형·재질·색상·구조·점유·한계 판정.
- BATCH_291_300_DEFERRED_OTHER_MODS.csv: 다른 모드 또는 바닐라 재검색 대상 10종.
- SOURCE_SHA256.csv: PZ PNG, 기존 MC 비교 JPG, 새 JPG의 SHA-256 및 기존 Git blob SHA-1.
- MANIFEST.json / BATCH31_STANDALONE_PROGRESS.json / INDEX.html / ZIP / ZIP_SHA256.txt.
- 원본 TMX, PNG, SQLite, 357종 전체 표, 다른 레인의 브랜치는 수정하지 않았다.
- 별도 Draft PR이며 임의 병합하지 않는다.

## 개별 관찰

- 291 Ottoman / Orange ↔ decocraft:cottage_footstool: PZ는 무늬 없는 주황색 작은 발받침이지만 MC 원본 cottage_footstool은 흰 바탕에 꽃무늬가 반복되는 두꺼운 발받침이다. 용도만 같고 색상·무늬·비례가 다르다.
- 292 Oven / Antique ↔ decocraft:pizza_oven: PZ는 검정 철제 장작난로와 가는 금속 연통이지만 MC pizza_oven은 붉은 벽돌 바닥과 넓은 돔 화실·굵은 벽돌 굴뚝의 야외 피자 화덕이다. 재질·실루엣·기능이 다르다.
- 293 Shelves / Big Wall Corner ↔ handcrafted:acacia_shelf: PZ는 직각으로 꺾인 개방형 3단 코너 선반인데 MC acacia_shelf는 단일 목재 상자형 덩어리처럼 보이고 열린 L자 코너와 세 선반 층이 보이지 않는다.
- 294 Speaker Cabinet / Guitar ↔ : PZ는 검정 세로형 기타 스피커 캐비닛이지만 기존 모드 조사에서 대응 MC 원본 모델이 확인되지 않았다. 오른쪽은 미검증 안내판으로 실제 MC 모델 렌더가 아니다.
- 295 Speaker Cabinet / Wood ↔ : PZ는 두 원형 드라이버가 노출된 목재 스피커인데 기존 MC 원본 후보가 없고 오른쪽은 안내판이다. 실제 모델 비교가 없어 승인 불가다.
- 296 Terminal / CeroSec ↔ refurbished_furniture:computer: PZ는 버튼과 디스플레이가 다수 있는 경사형 보안 콘솔이지만 MC computer 비교는 베이지색 단순 상자형 부분 JSON 렌더다. 화면·키패드·경사 제어판이 보이지 않고 완성 모델도 검증되지 않았다.
- 297 Chair / Exceptionally crafted ↔ pfm:arm_chair_leather: PZ는 팔걸이 없는 목재 의자지만 MC arm_chair_leather는 가죽 안락의자 종류이며 기존 Blockbench JSON 화면도 회색 판형 부분 렌더다. 종류·재질·등받이 구조가 불일치한다.
- 298 Counter / Corner A ↔ decocraft:diner_counter_corner_black: PZ는 금속/유리 코너 진열대와 투명 가림막이지만 MC는 검정 몸체와 회색 줄무늬의 불투명 카운터다. 유리·진열홈·상부 프레임이 없다.
- 299 Counter / Corner B ↔ decocraft:diner_counter_corner_black: PZ는 298번과 프레임 방향이 반대인 유리 진열 코너인데 MC는 298과 동일한 불투명 검정 카운터를 재사용한다. 유리와 상단 구조도 없고 회전별 차이도 입증되지 않았다.
- 300 Counter / Fossoil ↔ mcwfurnitures:acacia_counter: PZ는 크림색 몸체와 파란 상판의 주유소 카운터인데 MC acacia_counter는 주황색 아카시아 상판과 회색/갈색 나무껍질 질감 몸체다. 색상·재질·패널이 불일치한다.
