# 로즈우드 357종 원본 완성 가구 ↔ 실제 Minecraft 1.20.1 Forge 모델: 이미지/크기/속성

## 보고서 보는 법
1. ZIP을 다운로드한 뒤 INDEX.html을 브라우저에서 열면 357개 항목 검색/비교.
2. 카드 왼쪽은 원본 좀보이드 PNG를 복원한 *완성 가구 예시*.
3. 카드 오른쪽은 실제 모드 JAR의 blockstates/model JSON + PNG 원본 텍스처를 읽고 투영한 연구용 3D 그림.
4. 실제 원본 JSON/텍스처와 런타임 로더를 해석할 수 없는 가구는 미렌더 표시하고 **비슷해 보이는 이미지를 만들지 않음**.
5. PZ 크기: SpriteGridPos 합친 타일 설치 영역 및 공개 Viewpoint 3D 바운딩박스(있는 경우). MC 크기: 단일 blockstate 모델 기준 JSON 기하 경계, 게임 실제 충돌 박스 아님.
6. PZ 속성: v259 원본 .tiles source_attributes에서 실제 정의된 값만 표시; MC 속성: 블록 상태 JSON variants에 나온 속성 후보만. 수납, 앉기, 작동 여부는 실행 검증 없이 단정하지 않음.

- 전체 카드: 357장, 2×2 접촉시트: 90장.
- NO_MC_ASSET_SELECTED: 22장
- NO_MODEL_GEOMETRY_IN_CURRENT_RENDERER: 117장
- REAL_MOD_TEXTURED_JSON_ELEMENTS: 93장
- REAL_MOD_UNTEXTURED_JSON_ELEMENTS: 125장

**검증 한계:** 이전의 357종 중 335종 소스 블록 후보가 있다는 것과 실제 크기/외형 매칭 확정은 전혀 다름. 정확한 대응값은 아직 0종 인증.
