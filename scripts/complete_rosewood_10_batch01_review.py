#!/usr/bin/env python3
"""Manual-review batch 001-010, with Minecraft vanilla candidates permitted.
All other groups remain QUEUED, not silently approved.
Renders only source-backed model screenshots previously generated using native Blockbench.
"""
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
from collections import Counter
import csv,json,zipfile,html,re,math
D=Path(__file__).resolve().parents[1]/"analysis/rosewood_furniture/2026-10-31"
SRC=D/"all_357_complete_native_comparisons_v1"
PZ=D/"complete_furniture_visual_3d_v1"
E=D/"ten_batch_review/01_001_010/extra_decocraft_render"
V=D/"ten_batch_review/01_001_010/vanilla_native_render"
O=D/"ten_batch_review/batch_001_010_v1"
WAN_URL="https://modrinth.com/mod/storage-shelves"
WAN_PROMO="https://media.forgecdn.net/attachments/1271/760/shelf_render.png"
# Ratings are evidence grades, NOT fake 0-100 appearance scores.
DECISIONS=[
 dict(i=1,method="MOD_NATIVE",asset="decocraft:school_chair_gray",secondary="decocraft:diner_chair_gray",
    grade="VISUALLY_COMPARED_CONDITIONAL",dimension="1x1 candidate; runtime unverified",
    reasons="금속 다리·등받이·어두운 시트라는 특징은 공통이지만 원본 등받이와 좌면 두께·지지대 모양이 다름. 이전 school chair도 무조건 확정하지 않음.",
    requirement="metal frame; backrest; 4 legs; dark padded seat",
    source_file="school_chair_gray_BLOCKBENCH_VIEWPORT.png",source_dir="decocraft"),
 dict(i=2,method="MOD_NATIVE",asset="decocraft:toilet_white",secondary="pfm:basic_toilet",
    grade="VISUALLY_COMPARED_CONDITIONAL",dimension="1x1 candidate; actual water plumbing unverified",
    reasons="흰 도기·뒤 물탱크·둥근 변기 볼 구조를 재확인. 이전 Paladin 모드는 일부 부품만 렌더됐으며 Decocraft 흰 변기는 실제 완성 모델을 로드. 뚜껑/탱크 비율이 다름.",
    requirement="white flush toilet with tank & basin; plumbing/water interaction",
    source_file="toilet_white_BLOCKBENCH_VIEWPORT.png",source_dir="decocraft"),
 dict(i=3,method="NEW_MOD_OFFICIAL_INFO",asset="Wan's Storage Shelves / Small Cardboard Box",secondary="minecraft:brown_shulker_box",
    grade="PROMISING_NOT_YET_BLOCKBENCH_VERIFIED",dimension="1x1 footprint to verify in game",
    reasons="기존 크레용 상자는 완전히 부적합. Wan 모드의 작은 종이상자는 마크 1.20.1 Forge 지원 및 25칸 수납이 공식 소개로 확인됨; PZ 원본도 ContainerCapacity 25. 상자 단독 바닥 배치와 모델 블록 ID는 추가 검증해야 함. 바닐라 갈색 셜커 상자는 27칸으로 기능 대안이지만 테이프 표현은 없음.",
    requirement="taped plain brown cardboard box; 25 storage capacity",
    source_file="",source_dir="official_wan"),
 dict(i=4,method="NO_ACCEPTABLE_SOURCE_MODEL",asset="",secondary="Blockables Chairs / folding stool (NOT equivalent)",
    grade="NO_APPROPRIATE_MATCH_YET",dimension="1x1; full chair with folded X frame",
    reasons="기존 가죽 안락의자는 접이식 의자와 형태·용도가 다름. Blockables - Chairs의 folding stool은 등받이가 없어 동일하지 않음. 제시한 모드 및 바닐라 블록 조합만으로 1x1 안에 X자 금속 프레임/좌석/등받이를 정확 재현한 후보는 미검증. 별도 모드 탐색 또는 Blockbench 커스텀 필요.",
    requirement="portable folding chair with crossed tubular metal legs and backrest",
    source_file="",source_dir="none"),
 dict(i=5,method="MOD_NATIVE",asset="decocraft:waste_basket_black",secondary="minecraft:cauldron",
    grade="VISUALLY_COMPARED_CONDITIONAL",dimension="1x1 candidate, compare depth and rim height",
    reasons="PZ는 검은색 원통형 솔리드 쓰레기통. 새 Decocraft 검정 원통형 쓰레기바구니는 실물 형태 유사하나 그물망 격자가 보여 재질 불일치; 바닐라 가마솥은 입구가 열려 있지만 네모 형태라 차선책.",
    requirement="open-top round black solid-body bin, 10 capacity",
    source_file="waste_basket_black_BLOCKBENCH_VIEWPORT.png",source_dir="decocraft"),
 dict(i=6,method="MOD_NATIVE",asset="decocraft:chair_1_spruce",secondary="decocraft:diner_chair_green",
    grade="VISUALLY_COMPARED_CONDITIONAL",dimension="1x1",
    reasons="Green Dinner는 목재 프레임·세로 등받이 살·녹색 방석. 기존 초록 안락의자는 기각. Spruce 의자는 목재 프레임과 등받이가 비슷하지만 녹색 방석이 없고, diner_chair_green은 방석 색상은 비슷하나 금속 프레임이어서 최종 승인 보류.",
    requirement="brown wooden 4-leg dining chair, vertical slat back, green cushion",
    source_file="chair_1_spruce_BLOCKBENCH_VIEWPORT.png",source_dir="decocraft"),
 dict(i=7,method="VANILLA_NATIVE",asset="minecraft:chiseled_bookshelf",secondary="Wan's Storage Shelves / Oak Shelf",
    grade="VANILLA_ALTERNATIVE_NEEDS_VISUAL_PLACEMENT",dimension="1x1 vanilla full block; placement height approximate",
    reasons="기존 Handcrafted acacia_shelf는 렌더가 막힌 진열장처럼 보여 원본의 빈 3단 목제 개방형 선반과 다름. 바닐라 빈 조각된 책장은 2열x3행 슬롯을 제공해 선반 구획·재질이 더 가까우나 PZ는 가로로 긴 3개 층이고 임의 물품 수납 기능도 다름. 새 모드의 오크 선반 모델 재검증 가능.",
    requirement="open oak-brown storage bookshelf with 3 shelves, 40 capacity",
    source_file="vanilla__chiseled_bookshelf.png",source_dir="vanilla"),
 dict(i=8,method="NEW_MOD_OFFICIAL_INFO",asset="Wan's Storage Shelves / Modular Metal-frame Shelf",secondary="minecraft:iron_trapdoor + iron_bars [SCHEMATIC ONLY]",
    grade="PROMISING_NOT_YET_BLOCKBENCH_VERIFIED",dimension="PZ complete 2x1, ~2-block tall; modular 2x1 installation unverified",
    reasons="원본은 두 스프라이트로 조립된 폭 2칸, 높이 약 2칸 금속 3단랙. Wan 공식 이미지에는 검정/남색 금속 프레임과 3단 선반이 있어 기존 빈칸보다는 좋은 후보. 다만 나무판 재질·모듈의 실제 연결 폭은 달라서 2칸 배치/적재 가능 여부 확인 전 최종 확정 금지. 바닐라 철 덫문+쇠창살 조합은 같은 블록공간을 공유하기 어려워 외형 대안 검증 전.",
    requirement="2x1 steel industrial 3-tier warehouse rack, no doors, support struts",
    source_file="",source_dir="official_wan"),
 dict(i=9,method="MOD_NATIVE",asset="decocraft:chair_1_spruce",secondary="decocraft:chair_1_oak",
    grade="VISUALLY_COMPARED_CONDITIONAL",dimension="1x1",
    reasons="기존 Paladin oak_chair_classic_black은 좌석/등받이 등 일부가 사라진 부품 불완전 렌더라 반려. Decocraft spruce 실제 Blockbench 완성 모델은 어두운 갈색 나무의자 4다리지만 PZ는 상단 가로판 위주인 간단한 등받이여서 유사도 미완벽.",
    requirement="plain dark wood 4-leg dining chair; simple curved top backrest",
    source_file="chair_1_spruce_BLOCKBENCH_VIEWPORT.png",source_dir="decocraft"),
 dict(i=10,method="VANILLA_NATIVE",asset="minecraft:light_gray_shulker_box",secondary="minecraft:iron_block [visual fallback]; CUSTOM_BLOCKBENCH_MAY_BE_NEEDED",
    grade="VANILLA_FALLBACK_NOT_EXACT",dimension="1x1 vanilla block, but legs/cabinet doors missing",
    reasons="PZ는 낮은 철제 2도어 카운터와 4개의 다리, 하부 공간. 기존 적합 후보 미발견. 실버/라이트그레이 셜커 상자는 금속 느낌·1x1 크기·수납이라는 점에서 실용적 임시대체지만 정면 문 두 개와 다리를 표현하지 못함. Decocraft 하부장은 목재 상판이라 재질 차이가 큼. 정확 외형 유지하려면 별도 철제 카운터 모델 탐색/제작.",
    requirement="short stainless steel two-door cabinet with four legs and open bottom, 1x1 footprint",
    source_file="vanilla__light_gray_shulker_box.png",source_dir="vanilla")
]
def load_rows(path):
 with path.open(encoding="utf-8-sig",newline="") as f:return list(csv.DictReader(f))
def save_csv(p,rows):
 with p.open("w",encoding="utf-8-sig",newline="") as f:
  w=csv.DictWriter(f,fieldnames=list(rows[0]),extrasaction="ignore");w.writeheader();w.writerows(rows)
def font(sz):
 for p in ("/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc",
   "/usr/share/fonts/truetype/nanum/NanumGothic.ttf",
   "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"):
  if Path(p).exists():return ImageFont.truetype(p,sz)
 return ImageFont.load_default()
def crop_native(im):
 p=im.convert("RGBA")
 import numpy as np
 a=np.array(p);m=(a[:,:,:3].max(axis=2)>9)&(a[:,:,3]>3)
 ys,xs=np.where(m)
 if len(xs)>20:
  pad=14
  p=p.crop((max(0,int(xs.min())-pad),max(0,int(ys.min())-pad),
      min(p.width,int(xs.max())+pad+1),min(p.height,int(ys.max())+pad+1)))
 return p
def native_source(dec):
 if dec["source_dir"]=="decocraft":
  file=E/dec["source_file"]
 elif dec["source_dir"]=="vanilla":file=V/dec["source_file"]
 else:return None
 if file.exists():return file
 return None
def card(dec,orig):
 im=Image.new("RGB",(1320,610),(247,249,252))
 d=ImageDraw.Draw(im)
 d.rounded_rectangle((13,47,644,471),radius=9,fill=(231,237,241))
 d.rounded_rectangle((676,47,1308,471),radius=9,fill=(235,240,244))
 title=f"{dec['i']:03} {orig['pz_name']} / {orig['pz_style']}"
 d.text((21,8),title,font=font(21),fill=(29,51,72))
 d.text((25,57),"PROJECT ZOMBOID: original completed furniture",font=font(13),fill=(48,71,92))
 d.text((690,57),"MINECRAFT: "+dec["method"],font=font(13),fill=(48,71,92))
 # Preserve full original PZ sprite preview: no novel geometry generation.
 f=PZ/orig["pz_preview"]
 with Image.open(f) as src:
  left=src.convert("RGBA");left.thumbnail((580,355),Image.Resampling.LANCZOS)
  im.paste(left,(int(329-left.width/2),int(263-left.height/2)),left)
 path=native_source(dec)
 if path is not None:
  with Image.open(path) as src:
   right=crop_native(src)
   right.thumbnail((590,360),Image.Resampling.LANCZOS)
   im.paste(right,(int(991-right.width/2),int(271-right.height/2)),right)
 elif dec["source_dir"]=="official_wan":
  d.rounded_rectangle((714,126,1266,401),radius=12,fill=(247,247,247),outline=(126,139,151))
  d.text((739,178),"Wan's Storage Shelves (Forge 1.20.1)",font=font(18),fill=(50,70,89))
  d.text((739,223),"Official mod gallery; model not locally loaded",font=font(14),fill=(68,85,102))
  d.text((739,255),"See URL in HTML review page / CSV",font=font(13),fill=(70,85,101))
 else:
  d.rounded_rectangle((714,126,1266,401),radius=12,outline=(169,106,99),width=3)
  d.text((733,210),"NO EQUIVALENT MATCH VERIFIED",font=font(19),fill=(143,67,61))
  d.text((733,250),"Do not substitute a random chair/block.",font=font(13),fill=(111,68,59))
 d.line((18,483,1302,483),fill=(174,184,195),width=2)
 d.text((25,490),("PZ footprint "+orig["pz_grid"]+" / sprite parts "+orig["pz_parts"]+
        " | MC installation: "+dec["dimension"])[:130],font=font(12),fill=(53,69,84))
 d.text((25,514),("PICK: "+(dec["asset"] or "NO ACCEPTABLE MATCH"))[:120],font=font(12),fill=(53,69,84))
 d.text((25,538),("STATUS: "+dec["grade"])[:120],font=font(12),fill=(117,65,62))
 d.text((25,572),"Only model image files marked NATIVE are authentic Blockbench renders; no in-game size/function equivalence certified.",font=font(11),fill=(115,80,73))
 return im
def index_html(report):
 sections=[]
 for row in report:
  heading=f"{row['index']}. {row['pz_name']} / {row['pz_style']}".strip(" /")
  pic="cards/"+str(row["index"]).zfill(3)+"_PZ_vs_MC.jpg"
  url=(f'<a href="{WAN_URL}" target="_blank" rel="noreferrer">Wan’s Storage Shelves 공식 모드 및 갤러리</a>'
       if row["candidate_category"]=="NEW_MOD_OFFICIAL_INFO" else "")
  if url:
   url+=f'<p><a href="{WAN_PROMO}" target="_blank">공식 홍보 이미지 확인(게임 화면이 아닌 합성 홍보 이미지)</a></p>'
  sections.append('<article><img loading="lazy" src="'+pic+'" alt="'+html.escape(heading)+'">'+
   '<h2>'+html.escape(heading)+'</h2><p><b>새 후보:</b> '+html.escape(row["candidate_id"] or "일치품 없음")+'</p>'+
   '<p><b>보조 후보:</b> '+html.escape(row["secondary_id"])+'</p>'+
   '<p><b>판정:</b> '+html.escape(row["manual_review_grade"])+'</p>'+
   '<p><b>원본 형태:</b> '+html.escape(row["shape_requirement"])+'</p>'+
   '<p><b>크기:</b> PZ '+html.escape(row["pz_grid"])+' / '+html.escape(row["minecraft_placement_size"])+'</p>'+
   '<p><b>이유:</b> '+html.escape(row["manual_visual_review"])+'</p>'+url+
   '<details><summary>원본 타일 속성</summary><pre>'+html.escape(row["original_pz_properties_json"])+'</pre></details></article>')
 return ("""<!doctype html><html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
 <title>Rosewood manual rematch batch 001-010</title><style>
 body{background:#ebf0f3;color:#273c4c;font:14px system-ui,'Malgun Gothic',sans-serif;margin:0}
 header{position:sticky;top:0;background:white;border-bottom:1px solid #cbd5dd;padding:14px 3%;z-index:2}
 h1{font-size:22px;margin:0 0 8px}header p{line-height:1.55}
 main{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,570px),1fr));gap:16px;padding:18px 3%}
 article{background:white;border-radius:12px;border:1px solid #d1dce5;padding:12px}
 article img{width:100%;border-radius:7px}h2{font-size:18px}p{line-height:1.5;margin:7px 0}
 pre{white-space:pre-wrap;overflow-wrap:anywhere;font-size:10px;background:#eef2f6;padding:9px}
 </style></head><body><header><h1>Rosewood complete furniture rematch — batch 001–010 / 357</h1>
 <p>기존 매칭 모두 미확정. 이번 묶음은 PZ 완성 가구를 눈으로 보고 Decocraft 실제 BBMODEL, Mojang 바닐라 실제 Blockbench 모델, Wan 공식 모드 소개 이미지/설명을 비교해 10개를 개별 판정함.
 공식 소개만 확인한 신규 모드는 JAR 모델과 게임 설치 크기를 검증한 것이 아니다. 1:1 완전 일치 인증은 없음. 나머지는 10종 단위로 QUEUED.</p></header><main>__BODY__</main></body></html>""").replace("__BODY__","\n".join(sections))
def main():
 assert not O.exists(),"must not overwrite"
 (O/"cards").mkdir(parents=True)
 base=load_rows(SRC/"ALL_357_FULL_RENDER_MATCHING.csv")
 assert len(base)==357
 entries=[]
 for dec in DECISIONS:
  orig=base[dec["i"]-1]
  assert int(orig["index"])==dec["i"]
  record={
   "index":dec["i"],"pz_name":orig["pz_name"],"pz_style":orig["pz_style"],
   "pz_grid":orig["pz_grid"],"pz_parts":orig["pz_parts"],
   "original_pz_properties_json":orig["pz_original_properties_json"],
   "old_candidate_id":orig["chosen_mc_id"],"old_render_grade":orig["render_grade"],
   "old_candidate_decision":"REJECT" if dec["i"] in [3,4,6,7,8,9,10] else "HOLD_NOT_APPROVED",
   "candidate_category":dec["method"],"candidate_id":dec["asset"],
   "secondary_id":dec["secondary"],
   "manual_review_grade":dec["grade"],
   "minecraft_placement_size":dec["dimension"],
   "shape_requirement":dec["requirement"],
   "manual_visual_review":dec["reasons"],
   "mc_real_model_visual_evidence":"ACTUAL_BLOCKBENCH_RENDER" if native_source(dec) else "MOD_OFFICIAL_INFORMATION_ONLY" if dec["source_dir"]=="official_wan" else "NO_APPROPRIATE_RENDER",
   "mc_source_image_file":str(native_source(dec).relative_to(D)) if native_source(dec) else "",
   "official_mod_page_url":WAN_URL if dec["source_dir"]=="official_wan" else "",
   "approved_for_automatic_world_placement":"NO",
   "exact_visual_match_certified":"NO"
  }
  card(dec,orig).save(O/"cards"/f"{dec['i']:03}_PZ_vs_MC.jpg",quality=88,optimize=True)
  entries.append(record)
 save_csv(O/"BATCH_001_010_MANUAL_VISUAL_REVIEW.csv",entries)
 (O/"INDEX.html").write_text(index_html(entries),encoding="utf8")
 # Future groups are explicitly QUEUED; they are NOT auto-approved by style text.
 groups=[]
 for n in range(math.ceil(len(base)/10)):
  start=n*10+1;end=min(357,start+9)
  groups.append({"batch_number":n+1,"range":f"{start:03}-{end:03}",
    "first_index":start,"last_index":end,"count":end-start+1,
    "review_status":"COMPLETED_CONDITIONAL_CANDIDATES" if n==0 else "QUEUED_FOR_MANUAL_IMAGE_REVIEW",
    "source_original_range":"all_357_complete_native_comparisons_v1/ALL_357_FULL_RENDER_MATCHING.csv",
    "review_file":"batch_001_010_v1/BATCH_001_010_MANUAL_VISUAL_REVIEW.csv" if n==0 else ""})
 save_csv(O/"BATCHES_ALL_357_PROGRESS.csv",groups)
 m={"total_styles":357,"batch_size":10,"total_batches":len(groups),"manually_reviewed_with_individual_rationales":len(entries),
   "batches_done":1,"batches_not_done":len(groups)-1,
   "native_source_comparison_images":sum(bool(native_source(x)) for x in DECISIONS),
   "promising_new_mod_information_only":sum(x["method"]=="NEW_MOD_OFFICIAL_INFO" for x in DECISIONS),
   "no_acceptable_equivalent":sum(x["method"]=="NO_ACCEPTABLE_SOURCE_MODEL" for x in DECISIONS),
   "exact_1to1_approved":0,"original_source_file_overwritten":False,
   "never_claim_remaining_347_as_reviewed":True}
 (O/"MANIFEST.json").write_text(json.dumps(m,ensure_ascii=False,indent=2)+"\n",encoding="utf8")
 docs=["# 로즈우드 357종 가구 10개 단위 수동 재매칭",
 "## 1차 001~010 (10/10 개별 시각 검수)",
 "기존 자동 매칭을 정답으로 사용하지 않고 PZ 원본 완성 가구의 구조, 색상, 재질, 설치 공간, 기능을 다시 관찰하고 실제 Decocraft/바닐라 모델을 검토했다. 신규 Wan 모드는 공식 소개/이미지만 확인한 조건부 후보, JAR 모델과 배치 면적은 검증 전이다.",
 "개별 판정은 BATCH_001_010_MANUAL_VISUAL_REVIEW.csv 및 INDEX.html에 기록. MC 원본 .bbmodel/PNG와 바닐라 모델은 GitHub에 원본을 배포하지 않고 Blockbench 출력 이미지만 수록.",
 "## 10종 결과"]
 for x in entries:
  docs.append(f"- **#{x['index']:03} {x['pz_name']}/{x['pz_style']}**: {x['candidate_id'] or '대체품 미발견'} — {x['manual_review_grade']}. {x['manual_visual_review']}")
 docs+=["## 이어서 작업할 구간",
  "BATCHES_ALL_357_PROGRESS.csv에 **전체 36개 묶음**을 지정. 002번 묶음은 011~020번이고 끝은 351~357번 7종. 1차 외 35개 묶음은 현재 QUEUED로 명시하여 검수하지 않은 것을 완료라고 표시하지 않는다.",
  "기존 357 매핑은 계속 원자료로 보존하고 매 묶음의 최종 재매핑 검수 데이터만 별도 파일로 누적한다. 설치 크기와 게임 기능 검증 전에는 월드의 실제 가구 치환에 적용 금지.",
  "## 관련 출처",
  "- 새 cardboard box와 공업용 선반은 Wan's Storage Shelves 공식 프로젝트: "+WAN_URL,
  "- Brown Shulker Box 보조 블록은 vanilla Minecraft 1.20.1 Mojang 클라이언트 JAR 파일에서 모델 근거를 재구성했다."
 ]
 (O/"README_KO.md").write_text("\n\n".join(docs)+"\n",encoding="utf8")
 with zipfile.ZipFile(O/"ROSEWOOD_BATCH_001_010_MANUAL_REVIEW.zip","w",zipfile.ZIP_DEFLATED,compresslevel=5) as z:
  for p in O.rglob("*"):
   if p.is_file() and p.name!="ROSEWOOD_BATCH_001_010_MANUAL_REVIEW.zip":
    z.write(p,p.relative_to(O))
 with zipfile.ZipFile(O/"ROSEWOOD_BATCH_001_010_MANUAL_REVIEW.zip") as z:
  assert z.testzip() is None
  assert "INDEX.html" in z.namelist()
 print("BATCH_COMPLETED",json.dumps(m,ensure_ascii=False),flush=True)
if __name__=="__main__":main()
