# v257 — B42 원본 .tiles 속성 결합 (기존 10,042종 누적 분석 보존)

## 명확한 완료 범위

- 기준 부모: `analysis/current/v255/MANIFEST.json` (260개 물리 테이블, SHA256 `25df5bcd9ef1f332bc1178ae711ec09f43e070bbf8cc3c33b4e822a0a1766791`).
- 기존 v256 평면도·84개 TMX·Tiles 원본 이미지·사용자68·보류439·활성9587·비활성455 **수정하지 않음**.
- 신규 스크립트: [build_v257_original_properties.py](../../../scripts/build_v257_original_properties.py).
- 자동 검증: [build-v257-original-properties.yml](../../../.github/workflows/build-v257-original-properties.yml).
- 프로그램은 원본 .tiles에 있는 모든 슬롯과 속성을 새 출처별 테이블에 넣고, 10,042개 `source_key`에 대응시켜 `v257_master_with_official` 조회 뷰를 생성함.
- `SpriteGridPos`는 다칸 후보 좌표에 관한 속성이며, **완성 물체 인스턴스/인증이 아님**. 공식 PNG ↔ Local ID 및 정체 인증 추가 수는 0.
- 과거 추정이나 사용자 수동 검수를 공식 이름으로 덮어쓰지 않음. 패치와 메인에서 다른 값은 `v257_conflict`에 원문 보존, 패치 우선 표시는 잠정 후보에 한정.

## 반드시 구분할 두 종류의 입력

현재 GitHub 저장소의 `Tiles/newtiledefinitions.tiles` 크기는 **2,973,137바이트**이고, 2026-10-31 채팅에서 사용자가 전달한 `tiledef.zip` 내부의 `newtiledefinitions.tiles` 크기는 **2,972,120바이트**야. **동일한 파일로 간주하면 안 된다.**

- **현재 GitHub 소스만 이용한 빌드:** `repository_main_only_NOT_canonical`. 기존 누적 DB에 GitHub 메인 타일 정의 *한 파일*의 속성을 추가한 미완전 통합. `canonical_full_source=false`.
- **사용자가 올린 정확한 ZIP을 GitHub에도 추가한 빌드:** `Tiles/B42_2026_09_29_tiledef.zip`에 바이너리 그대로 추가. ZIP SHA256은 `ffba6f55e178ef0c4622906bfdd670c6a7cae779cf6dbe4e7d4b0dce45c18171`이어야 함. 이 7개 .tiles 파일을 모두 사용해 완전한 원본 정의층 생성. `canonical_full_source=true`.

**이 README가 있다고 해서 최종 물리 병합이 이미 완료되었다는 뜻은 아니다.** GitHub Action이 실행되어 `analysis/current/v257/MANIFEST.json`을 게시하고 SHA 및 `integrity_check`를 통과해야 완료 상태가 된다. 어떤 소스로 빌드됐는지는 반드시 그 매니페스트의 `source_status`를 확인할 것.

## 검증·보존 조건

1. 기존 v255 압축 조각 8개를 복원해 원본 SHA-256을 확인.
2. 기존 260개 테이블 스키마와 행 수를 복사 전후 비교.
3. v255의 10,042개 키, 사용자 68건, 보류439, 활성9587, 비활성455 보존.
4. 별도 `v257_source_file` / `v257_source_slot` / `v257_source_property` / `v257_property_candidate` / `v257_conflict` / `v257_v255_join` 테이블 추가.
5. 완성된 SQLite를 zlib+base64 조각으로 보존하고 SHA-256·SQLite 무결성 재검증.
6. 기존 루트 `PROJECT_STATE.json`과 `restore_latest_unified.py`는 검증 완료 전 변경하지 않음.

### 로컬 실행

```bash
python3 scripts/build_v257_original_properties.py --source-zip Tiles/B42_2026_09_29_tiledef.zip
```

ZIP이 없으면 GitHub 메인 파일만으로 테스트할 수 있지만, 그것은 **정식 전체 7종 입력 병합이 아님**.

빌드가 끝나면 `analysis/current/v257/MANIFEST.json`과 `v257.part*.b64`로 결과를 확인한다.
