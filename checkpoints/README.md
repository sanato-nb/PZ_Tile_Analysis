# 체크포인트 규칙

각 분석 배치가 **실제로 완료된 경우에만** `checkpoints/vNN.json`과 이미지 증거/CSV를 기록한다. 한 타일셋·Local ID는 고유 타일 한 건으로 집계한다.

체크포인트 예시:
```json
{
  "version": "v47",
  "date": "YYYY-MM-DD",
  "input_database_sha256": "실제 SHA-256",
  "new_observed_unique": 0,
  "new_provisional_unique": 0,
  "held": 0,
  "overlap_with_baseline": null,
  "mapping_verified_unique": 0,
  "certified_unique": 0,
  "evidence_paths": [],
  "status": "not_started"
}
```

파일 작성 후 실제 DB와 대조해 `PROJECT_STATE.json`에 근거 있는 수치만 반영한다. GitHub Actions는 `PROJECT_STATE.json` 변경 후 인수인계 텍스트 재생성을 수행하도록 설정돼 있다.
