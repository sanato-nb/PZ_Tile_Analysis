# 로즈우드 357 스타일: 원본 가구 완성형 PNG + 실제 3D 모드 모델 연결

## 출처와 검증 범위
- 원본: 로즈우드 추출 357개 CustomName/GroupName 조합, v259 원본 PNG Tiles/2x, 원본 .tiles와 SpriteGridPos
- 3D: 공개 프로젝트 Hiro.uou/Viewpoint 0.1.19의 pack.properties, 3D 모델 선언 및 bind.타일셋_LocalID 정확 일치
- 비교할 Minecraft 모드는 별도 357개 후보표 연결; **정확한 블록 ID는 아직 0개 확정**
- 공개 3D OBJ는 권리 문제 때문에 이 결과물에 재배포하지 않고 모델 파일 URL만 남김

## 실제 생성된 근거
- 가구 이름·스타일 357개 전체의 픽셀 기반 개별 참고 이미지: 357장
- 3×4 전체 접촉시트: 30장
- 원본 SpriteGridPos를 이용한 복합 가구 임시 조립 미리보기: 96개 스타일
- 공개 Viewpoint 원본 3D 모델 선언 1128개, 실제 스프라이트 바인딩 2057행
- 3D 소스 대응 ALL_VARIANT_PARTS_3D_BOUND: 246개 스타일
- 3D 소스 대응 NO_PUBLIC_3D_BINDING: 110개 스타일
- 3D 소스 대응 SOME_VARIANT_PARTS_3D_BOUND: 1개 스타일
- 3D 모델과 대응 검토에 연결한 개별 원본 타일 ID 레코드 1347행

## 다칸 가구 안전 원칙
- 2~4칸 가구는 SpriteGridPos의 조각을 한 접촉 이미지 안에 배치해서 **완성형을 참고**하고, 단일 조각을 가구 하나로 보지 않음.
- 타일의 렌더링 순서와 isometric 배치는 가정이며 TMX 사용된 부품 세트와 실제 전체 가구 픽셀을 최종 인증하지 않음.
- 이미지가 동일한 가구의 다방향 변형을 하나의 모델로 볼지 여부는 수동 확인이 필요함.
- 원본 스프라이트가 실재해도 공개 Viewpoint 3D 모드가 해당 타일 ID에 bind를 제공하지 않으면 '미연결'로 기록.
- 같은 이름+그룹으로 서로 다른 원본 타일셋이 섞일 때 대표 한 조합만 시각 예시로 사용; 원본 타일 전체와 bind는 CSV에 보존.
- B42.20.3 자료와 Viewpoint용 B42.21+ 자료의 버전 차이로 스프라이트 ID가 달라질 수 있음.

## 파일
- ALL_357_COMPLETE_FURNITURE_3D_CROSSWALK.csv: 357개 스타일의 대표 완성형 참고 이미지·부품 목록·Viewpoint 3D asset 실제 bind·마크 모드 후보.
- ALL_SOURCE_SPRITE_TO_VIEWPOINT_3D_BINDINGS.csv: 원본 Local ID별 공개 3D bind 확인/미확인.
- contact_sheets/: 30장, 357개 스타일 완성형 시트.
- previews/: 357장 개별 가구 원본 PNG 기반 조립 예시.
- COMPLETE_FURNITURE_CONTACT_SHEETS.zip: 전체 접촉시트와 CSV, 보고서.
- **아직 아님:** 공개 3D 모델 OBJ의 실제 색상·비례 렌더 확인; 실제 Minecraft 모드 블록 3D 모델의 화면 비교/레지스트리 ID 확정.


## 3D 모델 정점/면까지 직접 읽은 대표 비교 샘플 추가

- `geometry_samples/3D_GEOMETRY_EVIDENCE.csv`: 원본 타일 부품과 실제 Viewpoint OBJ의 기하 크기·면 개수·출처(20개 가구 사례).
- 공개 OBJ 파일은 **26개 실제 로드 성공**, **17개 대표 가구의 모든 부품**을 형상 참고도로 조립해 비교. 나머지 3개(서부 피아노/PAWS 핀볼/주크박스)는 Viewpoint 0.1.19 바인딩이 없음을 확인.
- `geometry_samples/SAMPLE_SHEET_01.jpg` 등 5장은 원본 **완성형 PNG / 3D 모델 형상**을 나란히 놓은 비교판. 색상·재질이 빠진 단색 3D 투영이므로 화면에 없는 모델 디테일은 확정 불가.
- `geometry_samples/VISUAL_INSPECTION_20_FURNITURE.csv`: 형태·크기·마크 가구 후보를 개별 검토하고 미검증을 표시.
- `geometry_samples/VISUAL_INSPECTION_README_KO.md`: 자세한 한국어 조립·대응 가이드.

이 소스는 공개된 Viewpoint 3D 자료를 분석한 결과이며, **sour_kisel의 6244/6282 PZ3D 모델팩 전체를 직접 입수·대조한 것은 아니다.** 해당 팩은 별도 확보해야 실제 커버리지 확인 가능하다.
