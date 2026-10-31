# v95 신규 고유 타일 12종 독립 이미지 판독

- 기준: v94 통합 SQLite 미관찰 대기열 1,095종.
- A 원본 PNG, B 동일 층 5×5 근사 조립, C 동일 레이어 배치 한 건 제거, D **다른 실제 TMX 좌표**를 12종 각각 직접 이미지로 확인함.
- 실제 시각 확인: 2개 접촉 검수판과 12개 A/B/C/D 비교판 모두 확인.
- 잠정 후보 7종, 보류 5종, 신규 12종, 중복 0종(최신 DB 대조는 통합 빌드에서 다시 검증).
- **주의**: D 12종 전부 같은 TMX에서 맨해튼 1~3칸 떨어진 근접 사용 위치. 독립 현장 검증이 아니므로 신뢰도는 최대 low, 최종 인증 0.
- 모든 12종 PNG 아틀라스 물리 높이 불일치. 공식 Local ID 및 TileZed 정합 검증 없음.
- 보류: appliances_cooking_01/14(0px), appliances_refrigeration_01/37(0px), fixtures_bathroom_01/44(0px), furniture_bedding_01/70(28px), furniture_seating_indoor_03/58(221px).
- 후보: carpentry_03/19(753px), fixtures_counters_01/57(4687px), fixtures_doors_02/12(7792px), fixtures_windows_curtains_01/6(4608px), fixtures_windows_curtains_02/16(2763px), fixtures_windows_metal/27(4805px), fixtures_windows_white/27(4678px).
- 원본·좌표·SHA-256·B-C 변화·증거 경로는 observations.tsv와 EVIDENCE_MANIFEST.json에 별도 보존.
- 기존 v36~v94 원본 데이터베이스, 체크포인트, 사용자 수동 검수 80종과 재검수 계보는 수정하지 않음.
