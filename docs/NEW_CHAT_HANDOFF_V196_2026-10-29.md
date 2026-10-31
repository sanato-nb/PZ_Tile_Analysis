# 좀보이드 B42 → 마인크래프트 맵 — 새 채팅 핵심 인수인계 (2026-10-29, v196)

> **이 문서를 새 채팅에서 가장 먼저 읽고, `main`의 `PROJECT_STATE.json`, `AGENTS.md`, `docs/HANDOFF.md`, `docs/ANALYSIS_RULES.md`와 해당 실제 `MANIFEST.json`을 다시 대조하라.**
> 이 문서는 사용자 지시·과거 대화 요약/열람 가능한 원문·프로젝트 증거를 연결하는 길잡이다. **ChatGPT 과거 대화 전체의 글자 단위 완전 원문은 API에서 복원할 수 없다.** 원문 미확보 부분은 지어내지 말 것.

## 1. 가장 중요한 최신 확정 상태

- 연결된 GitHub: https://github.com/sanato-nb/PZ_Tile_Analysis
- 인수인계 작성 당시 `main` 커밋: `5b9d970fca1bd8ea8e4b7d13af816d274139a7b7` ; 최신 병합 PR **#162**, v196.
- **전체 84 TMX 실제 고유 타일 10,042종** = 이전 원본 집합 5,409종 + 신규 4,633종.
- **잠정 이미지 관찰 기록 10,007/10,042 = 99.65146385%**. 상태 기록상 미관찰 35 = 실제 별도 키 33 + 과거 집계 불일치 2건. **이는 최종 물체/부품 정체 인증률이 아니다**.
- 공식 `mapping_verified=0`, `tilezed_verified=0`, `certified=0`. 최종 정체 인증 **0종**. 33종의 사용자 검수가 이 수치를 바꾸지는 않았다.
- 최신 통합 물리 SQLite **v196 / 256테이블**, 위치 `analysis/current/v196/`. SHA-256 `d006c491097d2370dc3e965264632d161c6da1fd997348238bf0f1b5a5c1a424`; `PRAGMA integrity_check=ok`; 부모 v195 **254개 테이블 전부 보존**.
- **v196 사용자 수동판정 33종** (원본 CSV SHA-256 `14671a09bf43d6273e53d56cfc4521fb092551499909793c90200770b4a441ef`):
  - `잠정 후보` **23종**, 사용자의 자유입력 문구와 확신도 그대로 보존, 사용자 직접 해석이므로 *공식 인증 아님*.
  - `미판정` **10종**, 사용자 최신 지시: **활성 검수 대상에서 전부 제외**. **원본/DB/10,042종 범위에서 삭제하지 말고 투명 인증 금지**. 과거 사용자 수동80종·제외14종 유지.
  - **현재 사용자 수동 검수 활성 대기 0종**, 23종은 별도의 **A 이미지 우선 의미 재검증 가능**; 역사적 잠정 관찰 10,007/10,042 불변.
  - 원본: `review/v196_user_manual33/USER_UPLOADED_33_VERBATIM.csv`, `review/v196_user_manual33/MANIFEST.json`; PR #162 https://github.com/sanato-nb/PZ_Tile_Analysis/pull/162

## 2. 사용자 지시의 최신 우선순위 — 절대 놓치지 말 것

1. **목적:** B42 각 개별 타일의 사물/부품 정체, 외형, 재질, 방향, 다칸 결합, 벽·건물 연결, 오염·혈흔·손상 변형을 원본 증거에서 식별한 뒤 마인크래프트 세계로 재구성한다. 일부만 조립한 2D 도면·계획서가 목표가 아님.
2. **원본 A를 먼저 실제 눈으로 보고 설명**: 픽셀 자체, 실루엣, 표면, 부품 형태를 기록. **B(실제 TMX 주변 장면), C(정확히 해당 타일 한 GID 제거), D(같은 키의 다른 공식 A를 원래 B 동일 위치에 대입)**는 보조 교차 근거. **B/C 합성 장면에서 보이는 완성 물체의 정체를 A 단일 타일의 확정 정체로 역투사하지 말 것**.
3. **B−C가 0이어도 타일 자체가 투명·없는 것이라고 단정 금지**: 상위 레이어 가림/지도 경계/소스 누락/작은 픽셀 차이/잘못된 대응 가능. 실제 A만 명확하면 원본 A 기반 낮은 신뢰도의 잠정 해석 가능하되 **실제 지도에서 노출되었다는 주장 금지**.
4. 이름, `.tiles`, 레이어/방 이름, 과거 AI 레이블을 근거로만 사물명을 지어내지 말 것. PZwiki 타일 목록 https://pzwiki.net/wiki/PZwiki:Tile_list 는 **Moveables/Script 명칭 참고**만; 현재 B42 공식 PNG↔TMX LocalID 대응 증거로 취급 금지.
5. `observed`, `provisional_candidate`, `held`, `mapping_verified`, `tilezed_verified`, `certified`를 분리. **잠정 관찰(99.65%) != 최종 정체 확정(0%)**.
6. 기존 이미지·원본 84 TMX/PNG·SQLite의 과거 전체 테이블/행/값, 수동80종, 원래 제외14종, v36 이후 누적 DB/모든 PR 및 사용자 D 실험 제약을 **절대로 덮어쓰거나 삭제하지 말 것**. 새 레코드는 append-only 식의 버전별 테이블/증거. SQLite `PRAGMA integrity_check`, 원본 SHA256, 이미지 ZIP CRC, 고유키 중복 및 전후 모든 부모 행 비교.
7. 사용자 선호: **마인크래프트는 한 블록 두께 벽을 우선**하고, 얇은 벽 모드를 섣불리 유일한 해결책으로 권하지 말 것. TMX에서 벽이 선인 점과 1블록 재현 충돌은 미해결 설계 문제.
8. 도중 중단/새 채팅에서도 실제 데이터·GitHub PR/상태문서로 이어갈 것. 워크/예약 실행 횟수 제한을 피해 불필요한 작은 배치·중복 검증을 양산하지 말고, **실제 A 시각분석에 많은 시간을 배분**.

## 3. 최신 재감사 작업과 다음 진짜 할 일

- **v194 / PR #160**: 사용자가 **두 번째 신규 배치 이후 결과가 A가 아니라 B/C만 보고 분류된 것 같다**고 지적. 신규 A 인덱스 160–319 160종을 다시 A 중심으로 감사, **위험 25개** `review/v194_Afirst_second160_319/MANUAL_A_REASSESSMENT_FLAGS.json`에 기록. 기존 결과는 아직 자동 삭제/정정하지 않음.
- **v195 / PR #161**: `v133`의 32종 + `v134` A 인덱스 180–215 36종을 독립 2차 A 육안 의견 **68종**으로 검사(일부 v194와 중복). 외형 대체로 일치 58, B/C 전체물 맥락 과잉 2, 모호 3, 역할 충돌 1, 기존 제외4. **중복을 신규 검수 고유수로 더하지 말 것**.
- **아직 전체 과거 후보 A 우선 재감사는 완료된 게 아님.** 새 채팅의 작업 핵심: v194의 25개 주의 항목 재검증, v195 미해결 6개, v133 이후 나머지 대규모 후보를 A 자체 우선으로 재검수하면서 과거 B/C 맥락 과잉 해석을 별도 표시. 가능하면 타일셋 연속 프레임/인접 A 실제 RGB·알파를 대조; 공식 매핑 없는 다른 아틀라스 칸은 타일 정답으로 단정 금지.
- 반례: `camping_01/52`을 '장작더미 윗판'으로 단정하는 설명은 A에서 부족. `camping_03/16`의 '화덕'은 A에서 석재 원형 테두리+걸이 구조가 보여 우물형일 가능성까지 열어둬야 함. `camping_02/72`의 천깔개·정확한 재질 주장 근거 약함. 해당 항목은 **재검토 표식이지 원래 DB 자동 정정 완료가 아님**.
- v193 https://github.com/sanato-nb/PZ_Tile_Analysis/pull/159 에서 33종 오프라인 수동 검수기를 제공했으며 사용자가 그 결과 CSV를 업로드. v196에서 **10개 미판정 활성 제외를 이미 실제 반영**. 이를 반복 요청하거나 사라진 항목을 복원하지 말 것.
- 최신 기록상 남은35를 '활성 검수35개'로 답하면 틀림: 사용자 수동 활성 대기0이고, 23개는 잠정/추가 의미검증, 10개는 사용자 제외, 2는 실제 타일 ID 없는 역사적 집계 차이.

## 4. 정확한 증거/도구 찾기

- 중앙 상태: `PROJECT_STATE.json`
- 분석 규칙: `docs/ANALYSIS_RULES.md`; 중앙 지시: `AGENTS.md`; 장기 이력: `docs/HANDOFF.md`
- 최신 DB: `analysis/current/v196/MANIFEST.json`
- 사용자 수동 33: `review/v196_user_manual33/`
- v191 원본 A 142개 확대·132개 판독: `review/v191_reopen142_A_first/`
- v192 A+진짜 TMX B/C 교차검토 142행: `review/v192_image_first_TMX_BC_142/`
- v193 오프라인 HTML/ZIP: `review/v193_manual33_offline_review/`
- v194 문제 25개: `review/v194_Afirst_second160_319/`
- v195 독립 의견 68개: `review/v195_A_first_independent_reaudit/`
- 이전 v133/v134 증거: `review/v133_visual32/`, `review/v134_visual_180_319/`
- 원본 A 색인/시트: `review/v119_selected_A_new4633/`; 진짜 B/C: `review/v182_occlusion202/` 및 `review/v120_B_context_new4632/`, `review/v121_C_diff_new4632/`.
- 과거 D(정의 혼동 주의): `review/v127_D_A_candidates_full4633/`, `review/v131_D_remaining_3832/`
- 원본 84 TMX: `B4220.3_MapExport_256/tmx/`; 원본 PNG: `Tiles/`
- v31은 **과거 원본/참고 데이터로 보존**하되 옛 v31 AI 정체 추론을 새 공식 정답으로 다시 사용하지 않는다. 과거 5,409종/수동80/제외14종 보존.
- Google Drive 폴더: `Tiles` https://drive.google.com/drive/folders/19V52CC8FYNeIm6GIibAi_RBBNiZqIagi ; 과거 v31 https://drive.google.com/drive/folders/1AXibVUJPRas3o_PTGVHu1TBrSmAN0gMF.
- GitHub PR #1–#90 색인은 과거 인수인계 패키지에, **#91–#162** 색인은 이 저장소의 `docs/PR_91-162_2026-10-29.md`에 별도 저장.
- 전체 진행률에 대한 과거 v31 '33,600 시트 검토율', v120 5,409, 최신 10,042 고유키 관찰률을 서로 섞지 말 것.

## 5. 인수인계의 대화 보존 범위

이번 새 채팅 인수인계는 GitHub의 버전 문서/PR 근거와 함께 사용자가 올린 과거 `v131 전체 인수인계 패키지` 및 이번 대화에서 열람 가능한 사용자 발화 원문·작업 회차 요약을 연결한다. **직접 볼 수 없는 과거 모든 메시지의 원문 전문은 작성할 수 없으므로** '완전한 축어록'이라고 표시하지 않는다. 추가 상세 대화 연대기는 `docs/NEW_CHAT_CONVERSATION_CHRONOLOGY_2026-10-29.md`에 있다.

## 6. 시작 명령

```text
'좀보이드 -> 마크 맵' 프로젝트를 이어간다. GitHub sanato-nb/PZ_Tile_Analysis 의 main 최신 PROJECT_STATE.json / AGENTS.md / docs/HANDOFF.md / docs/ANALYSIS_RULES.md / docs/NEW_CHAT_HANDOFF_V196_2026-10-29.md 와 v196 DB MANIFEST, v194/v195 A 우선 재감사 기록, v196 사용자 CSV를 먼저 실제 확인해. 33종 중 잠정23은 원문 보존, 미판정10은 활성 제외, 역사적 관찰10007/10042와 최종인증0은 구분한다. 두 번째 신규 배치(v133 이후)부터 과거 B/C 맥락 과잉을 원본 A 자체 시각관찰 우선으로 재검수하고 PZwiki는 용어 참고로만 사용해. 원본/과거 DB/수동80/제외14는 변경 금지. 이미 완료한 내용을 다시 만들지 말고 실물 A PNG와 정확한 TMX 키의 근거가 있는 새 검수 결과만 보수적으로 추가해.
```
