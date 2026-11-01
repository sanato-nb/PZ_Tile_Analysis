# 로즈우드 가구 vs **실제 Blockbench 5.2.2** 모델 시각 비교 실험

## 실행 범위
- 프로그램: 저작자 JannisX11가 배포한 Blockbench 5.2.2 Linux AppImage. 실제 GitHub 공식 릴리스의 SHA256 `375fb8da33b8b9ad0f1f790836ed83020b6e987a56e23184d31d6ccf3132ac3b` 대조 통과.
- 소스: Modrinth에서 원본 JAR의 SHA512 확인 후 **Decocraft의 실제 `.bbmodel`**과 해당 블록 ID의 텍스처 변형을 메모리/임시 파일에서 읽음.
- 검수: 자동화 프로그램 자체 렌더가 아니라 실제 Blockbench Electron 5.2.2에 각각 프로젝트를 열고, 앱의 `Preview.selected.screenshot()` API로 렌더 이미지 추출. 성공 모델 4개.
- 샘플: `school_chair_gray` 37 cubes; `crt_tv` 12 cubes; `double_bed_oak_white` 36 cubes; `piano_black` 245 cubes.
- 마인크래프트 **게임 엔진 자체를 실행한 것은 아님**. 블록 연결·충돌·기능·게임 내 방향과 실제 게임 화면은 별도 검수 필요.
- Blockbench에서는 원본 `.bbmodel`의 계층 구조/큐브 회전을 그대로 처리하며, 색상 텍스처는 실제 Decocraft 블록의 `material` PNG를 해당 프로젝트의 텍스처 슬롯에 적용. 동적 변형/애니메이션/표시 위치는 게임과 다를 수 있음.
- 원본 OBJ/BBMODEL/모드 JAR/텍스처를 GitHub에 **재배포하지 않음**. 비교용 Blockbench 화면과 소스 증거(해시)만 저장.

## 완성 원본 타일 vs Blockbench 직접 렌더

| 좀보이드 완성 가구 | 좀보이드 부품 | 마크 모드 | 비교 이미지 | 외형 해석 |
|---|---:|---|---|---|
| Chair / Grey | 1 | decocraft:school_chair_gray | [좌/우 비교](school_chair_gray_PZ_VS_NATIVE_BLOCKBENCH.jpg) | 회색 의자로 기능 유사. 원본은 패브릭/쿠션이 있고 MC는 학교 의자 형상이라 **정확한 동일 모델이 아님** |
| Television / Antique | 1 | decocraft:crt_tv | [좌/우 비교](crt_tv_PZ_VS_NATIVE_BLOCKBENCH.jpg) | CRT라는 분류만 일치. PZ는 목제 수납형+안테나, MC는 검은 독립 CRT. **외형 대체 부적합** 가능성 |
| Bed / Large Oak | 4 | decocraft:double_bed_oak_white | [좌/우 비교](double_bed_oak_white_PZ_VS_NATIVE_BLOCKBENCH.jpg) | 2인용 목제 침대가 비슷하나 원본보다 높은 헤드보드/난간과 베개 패턴이 다름. **카메라 오른쪽 경계 일부 클리핑** 존재 |
| Grand Piano / Black | 6 | decocraft:piano_black | [좌/우 비교](piano_black_PZ_VS_NATIVE_BLOCKBENCH.jpg) | 검은 그랜드피아노 형태 일치. PZ 이미지에서는 덮개가 닫혀 있고 MC는 상판이 열린 모델이므로 동작/상태 차이 검증 필요 |

**위 네 개 모두 외형 1:1 최종 확정은 아님.** 기존 357종 자동 매칭표는 수정·확정하지 않았다. 동일 개체가 여러 타일일 때는 좌측 원본 **완성형** 이미지가 기준이다.

## 다운로드/파일
- `NATIVE_BLOCKBENCH_PROOF.json`: 실제 Blockbench 앱 버전, project명, 로드된 큐브·텍스처 개수, 소스 JAR 모델/텍스처 SHA256.
- `*_BLOCKBENCH_DESKTOP.png`: 실제 프로그램 데스크톱 실행 화면 (프로그램 사용 증거).
- `*_BLOCKBENCH_VIEWPORT.png`: 앱 자체 Preview 3D API의 원본 스크린샷.
- `*_PZ_VS_NATIVE_BLOCKBENCH.jpg`: 좌측 완성 PZ PNG, 우측 네이티브 Blockbench 캡처를 나란히 놓은 판. Python은 원본 캡처를 크기 조정/크롭/합성하기만 했고 가구 기하를 새로 계산하지 않았다.
- 재현 스크립트: `scripts/native_blockbench_verify_furniture.py`.
- 실행 검증 워크플로: `.github/workflows/rosewood-native-blockbench.yml`.

### 중요 결론
Blockbench로 실제 모델을 확인하니 이전 자동 357종 매칭 중 **동일 기능이지만 확실히 다른 외형인 항목(목재 CRT TV↔검정 CRT)**이 바로 드러난다. 다음 검수는 원본 스타일의 색상·재질·부품 구조·설치 폭을 기준으로 후보의 적합성을 수동 조정해야 한다.
