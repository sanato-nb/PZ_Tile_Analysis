# 실제 Minecraft 1.20.1 Forge 가구 모드 JAR 자산 검수

2026-11-01 기준 release 중 1.20.1+Forge 호환 메타데이터가 있는 최신 파일을 Modrinth API에서 다운로드해 **일시적으로 압축 내부 파일**을 열어 검사.

- 요청: 7개, 검사 성공: 6개
- 블록 상태 JSON 이름: 5029개, 이름만 있는 후보: 0개
- REAL_MOD_ASSET_CANDIDATES.csv: 실제 Jar의 blockstates/ 자산 경로 또는 en_us.json 이름이 있는 ID.
- MOD_VERSION_SOURCES.json: 검사한 정확한 모드 버전과 jar SHA512.
- 블록 상태 파일이 실제 게임 레지스트리에 등록되어 있다는 것을 보증하지 않으므로 추후 runtime 확인 필요.
- Decocraft는 모델/장식이 동적 인덱스로 들어갈 수 있으므로 위 목록에 없다고 미지원 단정 불가.
- 모드 JAR/텍스처/모델 JSON 전체를 사용자의 GitHub에 복제하지 않았으며 목록만 생성.
