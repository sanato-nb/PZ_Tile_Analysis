# v250 — 보류 112종 A 우선 개별 검수

v248의 다른 진짜 TMX 위치가 있는 251종 중, v247~249에서 이미 개별 상세 판독한 139종을 제외한 **112종**을 원본 A 기반으로 재판독했다. 다른 실제 배치가 없는 역사적 제외 **188종은 재검수하지 않았다**.

## 실제 완료 범위

- 원본 A lossless PNG와 전체 RGBA 픽셀 SHA 재검증 **112/112**. 보존 ZIP 샤드 해시 **7/7**. 원본 전체 아틀라스 SHA를 이번에 새로 계산하지는 않았다.
- A 단독 형태와 부품/사물의 잠정 설명 **112행**. 실제 v248 다른 TMX B/C를 재사용해 비교판 **7장**을 직접 열어 봤다.
- 기존 개별 판독 139종과 새112종의 키 교집합 0. 따라서 **251/251종에 개별 A 형태 설명**이 생겼다.
- B−C 변화 100픽셀 미만인 **27종**은 주변 장면의 물체를 개별 A에 귀속하지 않았다.
- **이번에 새 B/C 렌더 0건, 공식 Local ID/TileZed/최종 정체 인증 0건**.

## 실제 A에서 구분한 사례

`location_business_office_generic_01/93`은 밝은 상판과 갈색 지지판의 책상형 몸체. `location_entertainment_theatre_01/9`는 흰 윗면을 가진 파란 캐비닛형 기기. `walls_exterior_roofs_30_04/13,16`은 좌우 경사 벽돌 박공 끝판. `walls_exterior_roofs_30_19/0,1`은 연청회색 삼각 패널이며 유리인지 확정하지 않았다. `walls_interior_bathroom_01/74,75`는 타일 무늬의 빈 문틀, `walls_interior_house_01/88,89`는 청회색 줄무늬 창형 개구부다.

## 근거 파일

- [112종 개별 A 형태·잠정 정체·원본 SHA·다른 TMX](ALL112_DETAILED.csv)
- [원래 A PNG/RGBA SHA 근거](A_ORIGINAL_112_SHA_VERIFIED.csv)
- [정확한 이전 미상세 112키 선정](EXACT_PENDING_112_KEY_CROSSWALK.csv)
- 원본 A와 다른 실제 TMX 장면 비교: [00](A_ORIGINAL_VS_ALT_B_00.png) · [01](A_ORIGINAL_VS_ALT_B_01.png) · [02](A_ORIGINAL_VS_ALT_B_02.png) · [03](A_ORIGINAL_VS_ALT_B_03.png) · [04](A_ORIGINAL_VS_ALT_B_04.png) · [05](A_ORIGINAL_VS_ALT_B_05.png) · [06](A_ORIGINAL_VS_ALT_B_06.png)

A를 보기 쉽도록 임시 확대했을 뿐 원본 크롭 RGBA/해시·좌표는 그대로 보존했다. 기존 v240 총10,042·활성9,587·비활성455, 기존 사용자 판정, PNG/TMX/SQLite는 변경하지 않았다. **모든 정체명은 잠정 후보**이며 공식 게임 이름이나 Minecraft 블록 확정이 아니다.
