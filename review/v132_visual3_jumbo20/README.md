# v132: 실제 이미지·TMX 23종 감사 (v131 이력 완전 보존)

기준 `main`: `5bae2a6ef593b074f8731a19c48ad0bff5a5eff1`. 작업 실행 및 증거: `scripts/v132_visual3_jumbo20_audit.py`, [Actions 성공 실행](https://github.com/sanato-nb/PZ_Tile_Analysis/actions/runs/40460201283).

## 검수 범위
- **3종** `vegetation_foliage_01/{0,1,3}`: 서로 다른 원본 PNG 이미지, 기존 A/B/C/D 비교 패널 직접 관찰, 원본 PNG 픽셀 SHA-256 및 원래 TMX의 GID/층/레이어/위치 대조 통과. **`provisional_candidate`이며 Local ID 매핑 인증은 아님.** `VISUAL_OBSERVATIONS_3.csv`, `VISUAL_3_ABCDE.jpg`.
- **20종** JUMBO A3: 원본 PNG 바이트/선정 RGBA 픽셀 SHA와 TMX의 배치 GID 실제 검증; 2장 접촉시트에 나온 크롭을 직접 관찰. 그중 **7종은 상하 반복/복수 프레임 의심**. 20종 모두 `held`이며 정확한 A3 아틀라스 Local ID는 여전히 미검증. `JUMBO_AUDIT_20.csv`, `JUMBO_VISUAL_FINDINGS.md`, `JUMBO_20_sheet_{0,1}.jpg`.
- 기존 우선 검수 예외의 **271행 큐**: B−C 픽셀 변화 0의 215행, B 이웃 누락 8행, 지도 경계 잘림 48행. 서로 다른 고유 타일 271종이란 뜻이 아니며 해당 항목을 모두 신규 육안 검수했다는 뜻도 아님. `PRIORITY_271_EXCEPTIONS.csv`.
- 15×15 전화기/전선 확대 검수 및 원본 TileZed 정의에 의한 공식 매핑은 이번 범위에서 **미완료**.

## 새로운 SQLite
`analysis/current/v132/MANIFEST.json`의 물리 DB는 기존 **v131 193테이블/기존 행 수 전부 보존**하고, `v132_visual3_jumbo20` 23행만 append해서 총 **194테이블**. `PRAGMA integrity_check=ok`. 복원: `python3 scripts/restore_unified_v132.py /tmp/pz_v132.sqlite`.

모든 `mapping_verified=0`, `tilezed_verified=0`, `certified=0`. 이미지 관찰/소스 검증/정체 후보를 최종 인증으로 혼동하지 말 것. 기존 5,409종, 수동 80종, 사용자 제외14종과 `Tiles/`, `B4220.3_MapExport_256/`, 모든 과거 SQLite 및 증거는 무변경.
