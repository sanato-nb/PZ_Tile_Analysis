# 로즈우드 대표 가구 20개 — 완성 이미지와 3D 형상 직접 대조 기록

공개 저작자 **Hiro.uou**의 Viewpoint 3D OBJ (commit `318753b6`)를 실제 읽고 **26개 OBJ의 정점/면 구조를 검사**했다. 20개 예제 중 17개는 원본 PNG와 3D 형상 도식의 양쪽을 대조할 수 있었고, 3개는 공개 3D 바인딩이 없어 PNG만 확인 대상으로 남았다. 원본 OBJ/텍스처 파일을 이 프로젝트에 재배포하지 않는다.

| 좀보이드 완성 가구 | 원본 부품 | 공개 3D 대응 | 우선 Minecraft 후보 | 핵심 검수 |
|---|---:|---|---|---|
| Large Oak Bed | 4칸 | 본체 4 OBJ | Paladin's / Macaw's | 2×2 크기와 헤드보드 |
| Blue Rattan Couch | 2칸 | 소파 2 OBJ | Paladin's | 라탄 팔걸이와 쿠션 |
| Large Metal Shelves | 2칸 | 금속랙 좌·우 OBJ | Decocraft / 직접 제작 | 나무 선반과 다른 금속 3단랙 |
| Large Oak Table | 2칸 | 테이블 2 OBJ | Macaw's | 목재 상판·연결 폭 |
| Oak Wardrobe | 2칸 | 옷장 2 OBJ | Macaw's | 2칸 너비·높이 |
| White Fridge | 1칸 | 1 OBJ | Refurbished | 옛날식 상하 2도어 |
| Antique Television | 1칸 | 1 OBJ | Refurbished / 직접 제작 | CRT+안테나, 현대 TV 대체 금지 |
| Desktop Computer | 1칸 | 1 OBJ | Refurbished / 직접 제작 | CRT와 수평형 본체 |
| PAWS Pinball | 2칸 | **없음 (이 3D 자료 기준)** | Arcade Reloaded / 직접 제작 | 해당 게임 기계의 형상이 중요 |
| Western Piano | 2칸 | **없음 (이 3D 자료 기준)** | Decocraft / 직접 제작 | 다른 3D 소스 추가 탐색 |

`3D_GEOMETRY_EVIDENCE.csv`에 20개 모두의 원본 Local ID, 실제 OBJ 모델명, 바운딩박스, 면 수, 판정 보류 사유를 기록했다.

**주의:** 3D 형상도는 원본 모델의 텍스처를 제외한 단색 투영이며 최종 게임 엔진 렌더가 아니다. `VISUALLY_CONSISTENT_BASIC_SHAPE`는 대략적인 윤곽이 비슷하다는 정성적 검토이고, `minecraft_exact_model_match_confirmed`는 **전부 NO**다. 원본 PNG 합성은 iso 오프셋 가정으로 만든 잠정 참고 형상이다.
