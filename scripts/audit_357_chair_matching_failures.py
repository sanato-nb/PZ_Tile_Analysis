#!/usr/bin/env python3
from pathlib import Path
import csv,json,shutil,zipfile
from collections import Counter
D=Path(__file__).resolve().parents[1]/"analysis/rosewood_furniture/2026-10-31"
A=D/"all_357_complete_native_comparisons_v1"
B=D/"chair_candidate_native_blockbench_v1"
O=D/"chair_matching_integrity_audit_v1"
def read(p):
 with p.open(encoding="utf-8-sig",newline="") as f:return list(csv.DictReader(f))
def write(p,rows):
 with p.open("w",encoding="utf-8-sig",newline="") as f:
  w=csv.DictWriter(f,list(rows[0]));w.writeheader();w.writerows(rows)
CHANGES={
 6:("decocraft:chair_1_spruce","decocraft:diner_chair_green",
  "PZ 나무 프레임+세로 등받이+녹색 쿠션. 기존 pfm:green_arm_chair는 안락의자로 다른 구조. spruce는 등받이/목재 유사하나 녹색 쿠션 없음. diner_chair_green은 쿠션은 비슷하지만 금속 프레임.",
  "chair_1_spruce_PZ_VS_NEW_MC_CANDIDATE.jpg"),
 9:("decocraft:chair_1_spruce","decocraft:chair_1_oak",
  "기존 pfm:oak_chair_classic_black의 원본 모델 cuboids가 일부만 Blockbench에 로드되어 화면상 불완전. spruce 후보는 나무 의자 전체 형상 렌더 성공, 단 등받이 디테일 다름.",
  "chair_1_spruce_PZ_VS_NEW_MC_CANDIDATE.jpg")
}
def main():
 assert not O.exists(),"do not overwrite"
 (O/"examples").mkdir(parents=True)
 rows=read(A/"ALL_357_FULL_RENDER_MATCHING.csv")
 assert len(rows)==357
 models=json.loads((B/"NATIVE_BLOCKBENCH_PROOF.json").read_text("utf8"))
 rendered={x["id"]:x for x in models if x.get("loaded_verified") and x.get("native_model_screenshot")}
 assert len(rendered)==12
 results=[];c=Counter()
 for r in rows:
  i=int(r["index"]);g=r["render_grade"];old=r["chosen_mc_id"];pz=r["pz_name"];style=r["pz_style"]
  flags=[]
  if g=="NATIVE_BLOCKBENCH_PARTIAL_SOURCE_JSON":flags.append("INCOMPLETE_NATIVE_MODEL_IMPORT")
  if g=="LEGACY_3D_APPROXIMATION":flags.append("NON_NATIVE_FALLBACK")
  if g=="NO_REAL_MOD_ASSET":flags.append("NO_REAL_SOURCE_CANDIDATE")
  if pz=="Chair":
   if "Folding" in style and "fold" not in old:flags.append("CHAIR_FOLDING_FEATURE_MISMATCH")
   if "Rocking" in style and "rock" not in old:flags.append("CHAIR_ROCKING_FEATURE_MISMATCH")
   if ("Wooden" in style or "Dinner" in style) and "arm_chair" in old:flags.append("CHAIR_STYLE_OR_STRUCTURAL_MISMATCH")
  if pz=="Bench" and "gym_bench" in old and style!="Sports":flags.append("WRONG_BENCH_SUBTYPE")
  if r["visual_verdict"] in ("REJECT_CURRENT_MATCH","REJECT_CURRENT_CANDIDATE"):flags.append("PRIOR_MANUAL_REJECTION")
  if r["visual_verdict"]=="NOT_VISUALLY_REVIEWED":flags.append("NOT_HUMAN_VISUALLY_APPROVED")
  if i in CHANGES:
   chosen,second,why,image=CHANGES[i]
   status="CONDITIONAL_ALTERNATIVE_ONLY"
   dest=f"examples/{i:03d}_PZ_VS_NEW_CHAIR.jpg"
   shutil.copy2(B/image,O/dest)
   flags.extend(["OLD_CANDIDATE_REJECTED","NEW_MODEL_RENDERED_IN_REAL_BLOCKBENCH"])
  elif "INCOMPLETE_NATIVE_MODEL_IMPORT" in flags:
   status="UNSAFE_PARTIAL_GEOMETRY";chosen=second=why=dest=""
  elif "PRIOR_MANUAL_REJECTION" in flags:
   status="REJECTED_EXISTING_MATCH";chosen=second=why=dest=""
  elif any(x in flags for x in ("CHAIR_FOLDING_FEATURE_MISMATCH","CHAIR_ROCKING_FEATURE_MISMATCH","CHAIR_STYLE_OR_STRUCTURAL_MISMATCH","WRONG_BENCH_SUBTYPE")):
   status="SEMANTIC_MISMATCH_REVIEW";chosen=second=why=dest=""
  elif "NO_REAL_SOURCE_CANDIDATE" in flags:
   status="NO_CANDIDATE_FOUND";chosen=second=why=dest=""
  else:
   status="REQUIRES_SHAPE_COMPARISON";chosen=second=why=dest=""
  item=dict(index=i,pz_name=pz,pz_style=style,
   previous_mc_id=old,previous_render_grade=g,previous_manual_verdict=r["visual_verdict"],
   proposed_mc_id=chosen,second_choice_mc_id=second,
   new_audit_status=status,explanation=why,flags=" | ".join(flags),
   pz_size=r["pz_grid"],pz_parts=r["pz_parts"],example_image=dest,
   approved_for_game="NO",is_1to1_certified="NO")
  results.append(item);c[status]+=1
 write(O/"ALL_357_MATCH_SAFETY_AUDIT.csv",results)
 write(O/"ALL_CHAIR_BENCH_STOOL_COUCH_REVIEW.csv",[x for x in results if x["pz_name"] in ("Chair","Bench","Stool","Couch")])
 write(O/"TWO_WRONG_CHAIRS_REPLACEMENT_PROPOSALS.csv",[x for x in results if x["index"] in (6,9)])
 summary=dict(total=357,real_source_chair_candidates_rendered=len(rendered),
  two_replaced_as_conditional=2,original_mapping_changed=False,
  partial_geometry_row_count=sum(x["previous_render_grade"]=="NATIVE_BLOCKBENCH_PARTIAL_SOURCE_JSON" for x in results),
  review_status_counts=dict(c),exactly_confirmed_matches=0)
 (O/"MANIFEST.json").write_text(json.dumps(summary,indent=2,ensure_ascii=False)+"\n",encoding="utf8")
 txt="# 잘못된 로즈우드 가구 매칭 감사 및 의자 2종 수정\n\n"
 txt+="## 실제 수행\n- 12개의 Decocraft 실물 .bbmodel+원본 텍스처를 실제 Blockbench 5.2.2에서 열고 완성 모델의 원본 PZ 모습과 비교. 12/12 렌더 성공.\n"
 txt+="- Green Dinner: 기존 pfm:green_arm_chair는 안락의자라 부적합. 조건부 1순위 decocraft:chair_1_spruce, 녹색 시트 대안 decocraft:diner_chair_green. 목재와 방석을 동시에 일치시키는 후보는 아직 미확정.\n"
 txt+="- Wooden: 기존 pfm:oak_chair_classic_black은 실제로 일부 모델 부품만 불러온 오류. 조건부 decocraft:chair_1_spruce. 나무 의자로 조립되지만 등받이가 완전히 같지는 않음.\n"
 txt+="\n## 357종 전체 위험 게이트\n- 기존 매칭은 실재 모델을 이미지로 만들었다고 해서 외형이 맞는 것은 아님. 이번 파일은 모든 레코드의 이전 증거, 미완성 렌더링, 잘못된 의자 형태, 수동 검수 결여를 명시함.\n"
 txt+="- 불완전한 원본 렌더링은 승인 불가. 잘못된 팔걸이·접이식·흔들의자 구별도 별도 문제로 처리.\n"
 txt+="- 357개의 원본 매칭/아틀라스/TMX/타일 속성을 변경하지 않음. 새 대체 후보는 최종 확정 아닌 조건부 제안.\n"
 txt+="\n## 파일\n- ALL_357_MATCH_SAFETY_AUDIT.csv : 전체 승인 게이트\n- ALL_CHAIR_BENCH_STOOL_COUCH_REVIEW.csv : 앉는 가구 집중 검수 목록\n- TWO_WRONG_CHAIRS_REPLACEMENT_PROPOSALS.csv : 잘못된 두 후보 수정안\n- examples : 좀보이드 왼쪽 / 실제 Blockbench 오른쪽 비교 사진\n- 전체 새 후보 사진은 이전 폴더 chair_candidate_native_blockbench_v1 의 12개 비교 JPG.\n"
 (O/"README_KO.md").write_text(txt,encoding="utf8")
 with zipfile.ZipFile(O/"ROSEWOOD_357_MATCH_AUDIT_CHAIRS.zip","w",zipfile.ZIP_DEFLATED) as z:
  for p in O.rglob("*"):
   if p.is_file() and p.name!="ROSEWOOD_357_MATCH_AUDIT_CHAIRS.zip":z.write(p,p.relative_to(O))
 print(json.dumps(summary,ensure_ascii=False))
if __name__=="__main__":main()
