# v258 통합 SQLite · B42 가구 목록

2026-11-06. v257의 타일 10,042종에 가구 후보 2,197개의 분류·부품·저장소 근거를 연결했다. v257이 사용한 원본 정의는 저장소의 메인·레거시 2개 파일이다. 가구와 타일은 다대다 관계이며, 같은 타일에 여러 후보가 연결될 수 있다.

## 복원

저장소 루트에서 Python 3.9 이상으로 실행한다. v257 조각과 v258에서 바뀐 페이지를 합쳐 SHA-256과 SQLite 무결성을 검증한 뒤 단일 파일을 생성한다.

```sh
python scripts/restore_v258_master.py PZ_B42_v258.sqlite
```

## 조회

| 테이블 또는 뷰 | 내용 |
|---|---|
| v257_master_with_official | 기존 타일 10,042종과 원본 속성 |
| v258_furniture | 가구 후보 2,197개, 21개 분류, 이름·검수·저장소 판정 |
| v258_furniture_tile | 후보별 타일 ID 및 일치한 v257 키. 일치하지 않으면 source_key는 NULL |
| v258_storage_evidence | 부품별 저장소 유형·용량·연결 근거 1,855행. 간접 근거도 표시 |
| v258_tile_furniture | 일치한 타일과 가구 후보, 부품별 저장소 근거를 함께 조회 |
| v258_held | 이미지 미확보 보류 34개 |

```sql
SELECT source_key, display_name, category, link_evidence, container_type, raw_capacity
FROM v258_tile_furniture
WHERE source_key = 'industry_01/4';
```

후보별 타일 전체 일치 964개, 일부 일치 497개, 미일치 736개. 일치한 고유 타일은 3,759개다. 키 일치는 가구의 모든 방향·부품을 게임 안에서 검증했다는 뜻과 구분한다. 부품별 저장소를 해석할 때는 link_evidence로 직접·간접 연결을 구분한다.

[검증 기록과 SHA-256](MANIFEST.json) · [가구 목록·CSV와 이미지 검수](../../furniture_b42/current/README.md) · [부모 DB](../v257/MANIFEST.json)
