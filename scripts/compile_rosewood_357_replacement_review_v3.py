#!/usr/bin/env python3
"""Source evidence only: add eight new Blockbench-verified improved model candidates
to conservative v2 source-to-model comparison, preserving all old candidates.
"""
import csv,json,zipfile,shutil,html
from pathlib import Path
from collections import Counter
ROOT=Path(__file__).resolve().parents[1]
D=ROOT/"analysis/rosewood_furniture/2026-10-31"
S=D/"pz_mc_furniture_357_rematch_v2"
E=D/"blockbench_native_replacement_candidates_v1"
O=D/"pz_mc_furniture_357_rematch_v3"
IMPROVED={
 ("Bed","Fancy"):("decocraft:single_bed_birch_black","단층 침대 형태로 이전 2층 침대보다 적합; PZ 검정 프레임과 MC 밝은 목재 프레임 차이","BETTER_FUNCTION_SHAPE_BUT_MATERIAL_DIFF"),
 ("Bed","Blue"):("decocraft:single_bed_birch_blue","단층 파란 침대 형태로 이전 2층 침대보다 적합; 침대 머리/발판 및 색감 다름","BETTER_FUNCTION_SHAPE_BUT_STRUCTURE_DIFF"),
 ("Bed","Oak"):("decocraft:crib_oak","참나무 아기침대로 기존 2층 침대보다 분명히 적합; 마크 모델 상단 장난감 모빌 차이","BETTER_FUNCTION_SHAPE_EXTRA_DECOR"),
 ("Stand","Pool Cue"):("decocraft:pool_rack","당구 큐대 보관대이므로 기존 옷걸이보다 기능과 형태가 적합; 선반 및 크기 차이","BETTER_FUNCTION_SHAPE_SIZE_REVIEW"),
 ("Hamster Wheel","Human"):("decocraft:treadmill","원본은 사람용 러닝머신이므로 기존 카지노 룰렛 후보보다 훨씬 정확한 종류","BETTER_FUNCTION_SHAPE_SIZE_REVIEW"),
 ("Counter","White"):("decocraft:bottom_cabinet_1_white","흰색 하부 수납장으로 기존 세면대 카운터보다 닫힌 외형에 가까움; 상판 나무색 차이","BETTER_FUNCTION_SHAPE_MATERIAL_REVIEW"),
 ("Counter","White Corner"):("decocraft:bottom_cabinet_corner_outer_1_white","흰색 모서리 하부장으로 기존 청록 식당 카운터보다 색상/종류가 적합; 방향 및 코너 완성배치 확인 필요","BETTER_FUNCTION_SHAPE_CORNER_REVIEW"),
 ("Oven","Green"):("decocraft:stove","가정용 가스레인지/오븐으로 기존 벽돌 피자 화덕보다 구조가 적합; 원본 초록색 대비 후보 회색","BETTER_FUNCTION_SHAPE_COLOR_REVIEW"),
}
def readcsv(path):
 with path.open(encoding="utf-8-sig",newline="") as f:return list(csv.DictReader(f))
def savecsv(path,rows):
 with path.open("w",encoding="utf-8-sig",newline="") as f:
  w=csv.DictWriter(f,list(rows[0]),extrasaction="ignore");w.writeheader();w.writerows(rows)
def render_html(rows):
 parts=[]
 for r in rows:
  old=r["mc_id"] or "(no source asset)"
  new=r["reviewed_replacement_mc_id"] or "(unchanged / not reviewed)"
  search=(r["pz_name"]+" "+r["pz_style"]+" "+old+" "+new+" "+r["new_match_status"]).lower()
  parts.append('<article data-search="'+html.escape(search,quote=True)+'" data-grade="'+r["new_match_status"]+'">'+
   '<img loading="lazy" src="'+html.escape(r["card"],quote=True)+'" alt="'+html.escape(r["pz_name"],quote=True)+'">'+
   '<h2>'+html.escape(r["pz_name"]+" / "+r["pz_style"])+'</h2>'+
   '<p>기존 후보: <code>'+html.escape(old)+'</code></p>'+
   '<p>새로 제안한 후보: <code>'+html.escape(new)+'</code></p>'+
   '<p><b>상태: '+html.escape(r["new_match_status"])+'</b> · '+html.escape(r["new_match_memo"])+'</p>'+
   '<p>크기: PZ '+r["pz_tiles"]+'칸 / 타일 부품 '+r["pz_parts"]+
   '개, 기존 MC 모델 경계 '+html.escape(r["mc_bbox"])+' (새 후보 실제 설치 크기 미측정)</p>'+
   '<p>검수 경고: '+html.escape(r["warnings"])+'</p>'+
   '</article>')
 return ("""<!doctype html><html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
 <title>로즈우드 357종 Blockbench 실물 외형 재대조 v3</title>
 <style>body{margin:0;background:#eef1f4;color:#27394a;font:14px system-ui,'Malgun Gothic',sans-serif}
 header{position:sticky;top:0;z-index:2;background:white;border-bottom:1px solid #d0dbe2;padding:18px 3%}
 h1{font-size:21px}main{padding:22px 3%;display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,535px),1fr));gap:18px}
 article{border-radius:12px;border:1px solid #d4dfe8;padding:12px;background:white}article img{width:100%}
 h2{font-size:17px}p{font-size:13px;line-height:1.5}code{overflow-wrap:anywhere}
 input,select{font:inherit;padding:10px;border:1px solid #bbc9d4;border-radius:7px}
 #q{flex:1;min-width:200px}.tools{display:flex;gap:10px;flex-wrap:wrap}
 </style></head><body><header><h1>완성 좀보이드 가구 357종 ↔ 마크 모드 가구: Blockbench 재대조</h1>
 <p>실제 Blockbench 렌더 50개 고유 Decocraft 모델을 110종 원본 스타일에 연결했고,
 대표 가구 50종을 직접 이미지 비교했어. 기존 부적합 8종에 대해 실제 Blockbench로 대체 후보 8개를 추가 검토했어.
 외형 정확 일치 인증은 없으며 다른 모드는 비네이티브 근사 이미지 또는 이미지 부재로 표시해.
 마크 게임 실제 설치·충돌·상호작용은 미검증.</p>
 <div class="tools"><input id="q" placeholder="가구명, 후보 ID 검색"><select id="t"><option value="">전체</option>
 <option value="REPLACEMENT_VISUALLY_REVIEWED_CONDITIONAL">새 대체 후보 8종</option>
 <option value="OLD_CANDIDATE_REJECTED">기존 후보 부적합</option>
 <option value="STILL_UNCERTAIN">기존 대조 유지</option></select><span id="num"></span></div></header><main>__CONTENT__</main>
 <script>const cards=[...document.querySelectorAll('article')],q=document.getElementById('q'),t=document.getElementById('t'),n=document.getElementById('num');
 function update(){let count=0;for(const x of cards){let yes=x.dataset.search.includes(q.value.toLowerCase().trim())&&
 (!t.value||(t.value==='STILL_UNCERTAIN'?!x.dataset.grade.startsWith('REPLACEMENT'):t.value==='OLD_CANDIDATE_REJECTED'?x.dataset.grade==='REJECT_CURRENT_MATCH':x.dataset.grade===t.value));
 x.style.display=yes?'':'none';if(yes)count++}n.textContent=count+' / '+cards.length+'종'}q.oninput=t.onchange=update;update();</script></body></html>""").replace("__CONTENT__","\n".join(parts))
def main():
 assert not O.exists()
 (O/"cards").mkdir(parents=True);(O/"better").mkdir()
 original=readcsv(S/"ALL_357_REMATCH_REVIEW.csv")
 proof=json.loads((E/"NATIVE_BLOCKBENCH_PROOF.json").read_text("utf8"))
 verified={x["id"]:x for x in proof if x.get("loaded_verified") and x.get("native_model_screenshot")}
 assert len(verified)==8,len(verified)
 report=[];better=[]
 for r in original:
  row=r.copy()
  row["reviewed_replacement_mc_id"]=""
  row["new_match_status"]=r["visual_verdict"]
  row["new_match_memo"]=r["manual_memo"]
  row["new_mc_game_placement_tested"]="NO"
  row["new_candidate_game_collision_tested"]="NO"
  key=(r["pz_name"],r["pz_style"])
  suggestion=IMPROVED.get(key)
  if suggestion:
   asset,note,category=suggestion
   id=asset.split(":",1)[-1]
   evidence=verified.get(id)
   assert evidence and (E/(id+"_PZ_VS_NEW_MC_CANDIDATE.jpg")).exists(),key
   row["reviewed_replacement_mc_id"]=asset
   row["new_match_status"]="REPLACEMENT_VISUALLY_REVIEWED_CONDITIONAL"
   row["new_match_memo"]=note
   row["proposed_improvement_type"]=category
   row["new_mc_model_source_sha256"]=evidence["source_sha256"]
   row["new_mc_texture_source_sha256"]=evidence["variant_sha256"]
   row["old_comparison_card"]=r["card"]
   row["card"]="better/"+id+"_PZ_VS_NEW_MC_CANDIDATE.jpg"
   shutil.copy2(E/(id+"_PZ_VS_NEW_MC_CANDIDATE.jpg"),O/row["card"])
   better.append(row.copy())
  else:
   shutil.copy2(S/r["card"],O/r["card"])
  report.append(row)
 assert len(report)==357 and len(better)==8
 savecsv(O/"REVISED_357_PZ_MC_MATCHES.csv",report)
 savecsv(O/"EIGHT_BLOCKBENCH_VERIFIED_IMPROVED_CANDIDATES.csv",better)
 (O/"INDEX.html").write_text(render_html(report),encoding="utf8")
 src_manifest=json.loads((S/"MANIFEST.json").read_text("utf8"))
 m={**src_manifest,"additional_new_native_replacement_models":8,
    "new_replacement_candidates_visually_reviewed":8,
    "recommended_asset_ids_changed_in_proposals_only":8,
    "original_357_data_overwritten":0,
    "new_replacement_model_in_game_verified":0,
    "new_replacement_visual_exact_match_verified":0}
 (O/"MANIFEST.json").write_text(json.dumps(m,ensure_ascii=False,indent=2)+"\n",encoding="utf8")
 notes=["# 로즈우드 가구 357종 Blockbench 기반 재매칭 v3",
 "실제 Blockbench 5.2.2에서 기존 고유 Decocraft 모델 50개를 로딩해 110개 PZ 스타일 이미지에 붙임.",
 "그중 50개 대표 완성 가구를 이미지로 대조해 28개 부적합, 12개 조건부, 5개 색상 불확실, 5개 형태 대체 필요로 판정.",
 "나머지 307개 스타일은 육안 확정이 아니며 실제 마크 게임의 설치 크기/충돌/상호작용은 미검증.",
 "## 신규 대체 후보 8개 (각각 원본 .bbmodel과 variant source 해시 존재)",
 "초기 모드 매치 결과를 덮어쓰지 않고 추천 변경 후보로만 별도 기록."]
 for r in better:
  notes.append("- "+r["pz_name"]+" / "+r["pz_style"]+": "+r["mc_id"]+" → "+r["reviewed_replacement_mc_id"]+" — "+r["new_match_memo"])
 notes +=["## 파일","- INDEX.html: 왼쪽 PZ 원본 / 오른쪽 실제 Blockbench (또는 미확인 구분) 가구 검색",
 "- REVISED_357_PZ_MC_MATCHES.csv: 전체 357종 개선 추천 및 형상 검수 상태",
 "- EIGHT_BLOCKBENCH_VERIFIED_IMPROVED_CANDIDATES.csv: 새 8개 검수 비교와 모델 원본 해시",
 "- cards 및 better 폴더: 각각 기존 349개 비교와 새 Blockbench 대체 비교 8개",
 "- ZIP을 풀고 INDEX.html 열기. Blockbench 렌더는 마인크래프트 게임 스크린샷이 아니야.",
 "원본 좀보이드 TMX/PNG/SQLite와 기존 357개 매칭 파일은 변경하지 않음."]
 (O/"README_KO.md").write_text("\n\n".join(notes)+"\n",encoding="utf8")
 with zipfile.ZipFile(O/"ROSEWOOD_357_BLOCKBENCH_REMATCH_V3.zip","w",zipfile.ZIP_DEFLATED,compresslevel=4) as z:
  for p in O.rglob("*"):
   if p.is_file() and p.name!="ROSEWOOD_357_BLOCKBENCH_REMATCH_V3.zip":z.write(p,p.relative_to(O))
 with zipfile.ZipFile(O/"ROSEWOOD_357_BLOCKBENCH_REMATCH_V3.zip") as z:
  assert z.testzip() is None
  assert "INDEX.html" in z.namelist()
 print("NEW_REPLACEMENTS",len(better), "357_TOTAL",len(report),json.dumps(m,ensure_ascii=False),flush=True)
if __name__=="__main__":main()
