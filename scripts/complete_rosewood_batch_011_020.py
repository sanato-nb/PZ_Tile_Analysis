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
E=D/"ten_batch_review/02_011_020/extra_decocraft_render"
V=D/"ten_batch_review/01_001_010/vanilla_native_render"
O=D/"ten_batch_review/batch_011_020_v1"
WAN_URL="https://modrinth.com/mod/storage-shelves"
WAN_PROMO="https://media.forgecdn.net/attachments/1271/760/shelf_render.png"
# Ratings are evidence grades, NOT fake 0-100 appearance scores.
DECISIONS=[
 {
  "i": 11,
  "method": "MOD_NATIVE",
  "asset": "decocraft:locker_gray",
  "secondary": "decocraft:locker_light_gray",
  "grade": "SEARCH_ANOTHER_MOD",
  "dimension": "1×1 footprint; 1.77 PZ source height",
  "reasons": "원본은 회색 금속 양문형 락커, Decocraft는 단문 루버 도어이고 실제 렌더에서 파란색으로 나와 색상/문 수가 다름. 최종 치환 보류. 다른 모드에서 양문형 회색 1칸 락커 검색.",
  "requirement": "gray 2-door metal locker",
  "source_file": "locker_gray_BLOCKBENCH_VIEWPORT.png",
  "source_dir": "decocraft"
 },
 {
  "i": 12,
  "method": "MOD_NATIVE",
  "asset": "decocraft:chair_1_ebony",
  "secondary": "decocraft:chair_1_spruce",
  "grade": "CONDITIONAL_WOODEN_CHAIR",
  "dimension": "1×1; game install size unverified",
  "reasons": "원본은 짙은 갈색 네 다리 세로살 등받이 목재 의자. Decocraft Ebony 실모델은 다리와 등받이 구조가 근접하나 검정에 가까운 더 어두운 색임. 기존 Paladin 모델은 부품 누락이라 반려.",
  "requirement": "dark wooden four-leg slat-back chair",
  "source_file": "chair_1_ebony_BLOCKBENCH_VIEWPORT.png",
  "source_dir": "decocraft"
 },
 {
  "i": 13,
  "method": "MOD_NATIVE",
  "asset": "decocraft:office_chair_black",
  "secondary": "decocraft:gaming_chair_black",
  "grade": "CONDITIONAL_OFFICE_CHAIR",
  "dimension": "1×1; swivel and seating function untested",
  "reasons": "바퀴·회전식 베이스는 원본과 같지만 새 Office Chair는 목재 슬랫 등받이와 팔걸이가 있고 PZ는 팔걸이가 없는 단순 패드형. 게임 의자는 과장된 고등받이라 차선.",
  "requirement": "black no-armrest compact swivel office chair",
  "source_file": "office_chair_black_BLOCKBENCH_VIEWPORT.png",
  "source_dir": "decocraft"
 },
 {
  "i": 14,
  "method": "MOD_NATIVE",
  "asset": "decocraft:trash_can",
  "secondary": "refurbished_furniture:recycle_bin",
  "grade": "CLOSE_VISUAL_FUNCTION",
  "dimension": "1×1; actual storage behavior untested",
  "reasons": "원본은 리브 무늬와 둥근 뚜껑이 있는 은회색 금속 쓰레기통. Decocraft Trash Can은 실제 렌더에서 둥근 통, 세로 주름, 윗뚜껑이 가까워 기존 불완전 Refurbished 렌더보다 낫지만 녹·손잡이 세부가 다름.",
  "requirement": "lidded corrugated metal round trash can",
  "source_file": "trash_can_BLOCKBENCH_VIEWPORT.png",
  "source_dir": "decocraft"
 },
 {
  "i": 15,
  "method": "MOD_NATIVE",
  "asset": "decocraft:filing_cabinet_white",
  "secondary": "decocraft:filing_cabinet_birch",
  "grade": "CLOSE_VISUAL_FUNCTION",
  "dimension": "1×1; real drawer interactions unverified",
  "reasons": "원본은 아이보리색 금속 세 서랍 파일 캐비닛. Decocraft Filing Cabinet White는 정확히 세 서랍과 정면 손잡이 형태를 갖췄음. 아이보리 색상/낡은 정도와 손잡이 간격은 다름. 기존 주방 수납장 반려.",
  "requirement": "off-white vertical three-drawer filing cabinet",
  "source_file": "filing_cabinet_white_BLOCKBENCH_VIEWPORT.png",
  "source_dir": "decocraft"
 },
 {
  "i": 16,
  "method": "MOD_NATIVE",
  "asset": "decocraft:wall_hood",
  "secondary": "refurbished_furniture:light_range_hood",
  "grade": "CLOSE_VISUAL_FUNCTION",
  "dimension": "1×1 wall fixture; mounting direction not checked",
  "reasons": "원본의 은색 비스듬한 배기후드에 가까운 벽걸이 모델을 확보. 다만 새 Wall Hood는 상부 덕트가 더 높고 원본의 검은 상단 띠와 구조가 다름. 이전 Refurbished 렌더는 일부 큐브만 보였음.",
  "requirement": "silver trapezoid wall extractor hood",
  "source_file": "wall_hood_BLOCKBENCH_VIEWPORT.png",
  "source_dir": "decocraft"
 },
 {
  "i": 17,
  "method": "MOD_NATIVE",
  "asset": "decocraft:rattan_armchair_white",
  "secondary": "decocraft:beach_chair_white",
  "grade": "DEFER_NEW_MOD_FOR_PLASTIC_CHAIR",
  "dimension": "1×1; postpone",
  "reasons": "PZ는 하나로 성형된 흰 플라스틱 야외 의자로 곡선 등받이와 일체형 팔걸이. 새 라탄 의자는 직조+두꺼운 방석이고 Beach Chair는 캔버스형. 둘 다 재질/구조가 달라 최종 매칭 보류. Skniro 등에서 플라스틱 성형 의자 추후 탐색.",
  "requirement": "cream plastic monobloc chair with integrated armrests",
  "source_file": "rattan_armchair_white_BLOCKBENCH_VIEWPORT.png",
  "source_dir": "decocraft"
 },
 {
  "i": 18,
  "method": "MOD_NATIVE",
  "asset": "decocraft:bottom_cabinet_1_spruce",
  "secondary": "decocraft:bottom_cabinet_1_oak",
  "grade": "CONDITIONAL_KITCHEN_COUNTER",
  "dimension": "1×1; counter height unverified",
  "reasons": "원본은 어두운 목재 2도어 하부장과 밝은 베이지색 상판. 새 Spruce 하부장은 갈색 본체+밝은 상판으로 접근하지만 위쪽 서랍 한 개와 아래 문 한 개로 원본 2도어 구조와 다르고 높이도 달라 설치 비교 필요.",
  "requirement": "dark wooden double-door counter with light stone top",
  "source_file": "bottom_cabinet_1_spruce_BLOCKBENCH_VIEWPORT.png",
  "source_dir": "decocraft"
 },
 {
  "i": 19,
  "method": "MOD_NATIVE",
  "asset": "decocraft:wall_sink_white",
  "secondary": "decocraft:round_sink_silver",
  "grade": "DEFER_PEDESTAL_SINK",
  "dimension": "1×1; floor-mounted pedestal required",
  "reasons": "PZ는 독립형 하얀 도기 세면대로 긴 받침 기둥을 가진다. 새 Wall Sink White는 수전과 물받이만 유사하며 벽에 설치되어 페데스털이 없음. Round Sink Silver도 상판 거치형. Skniro/욕실 가구 모드에서 받침 기둥 포함 모델 탐색 보류.",
  "requirement": "freestanding white ceramic pedestal basin with faucets",
  "source_file": "wall_sink_white_BLOCKBENCH_VIEWPORT.png",
  "source_dir": "decocraft"
 },
 {
  "i": 20,
  "method": "MOD_NATIVE",
  "asset": "decocraft:bottom_cabinet_1_oak",
  "secondary": "decocraft:bottom_cabinet_1_birch",
  "grade": "CONDITIONAL_WOODEN_COUNTER",
  "dimension": "1×1; finish and exact top profile unverified",
  "reasons": "원본은 꿀빛 갈색 단정한 장식 없는 카운터. 새 Oak 하부장은 따뜻한 나무색은 가까우나 흰 상판, 장식 문짝/서랍이 추가됨. 기존 Macaw Birch Counter는 회색 몸통이라 더 먼 후보. 바닐라 배럴/각목 블록도 추후 비교 가능.",
  "requirement": "plain honey-brown wood enclosed kitchen counter",
  "source_file": "bottom_cabinet_1_oak_BLOCKBENCH_VIEWPORT.png",
  "source_dir": "decocraft"
 }
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
 elif dec["source_dir"]=="official_vanilla":
  d.rounded_rectangle((714,126,1266,401),radius=12,outline=(129,147,164),width=3)
  d.text((733,200),"VANILLA BLOCK CANDIDATE",font=font(19),fill=(65,93,116))
  d.text((733,238),dec["asset"],font=font(15),fill=(65,93,116))
  d.text((733,280),"Native 1.20.1 rendering incomplete; see wiki",font=font(12),fill=(97,87,80))
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
   url+=f'<img loading="lazy" style="max-width:220px;aspect-ratio:1;object-fit:contain" src="{WAN_PROMO}" alt="Wan 모드 공식 홍보: 종이상자와 금속 프레임 선반"/>'
  if row["candidate_category"]=="VANILLA_BLOCK_OFFICIAL_NOT_RENDERED":
   u="https://minecraft.wiki/w/Chiseled_Bookshelf" if "bookshelf" in row["candidate_id"] else "https://minecraft.wiki/w/Shulker_Box"
   url+=f'<a href="{u}" target="_blank" rel="noreferrer">바닐라 블록 실제 외형과 속성 확인 (Minecraft Wiki)</a>'
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
 </style></head><body><header><h1>Rosewood complete furniture rematch — batch 011–020 / 357</h1>
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
   "mc_real_model_visual_evidence":"ACTUAL_BLOCKBENCH_RENDER" if native_source(dec) else "MOD_OFFICIAL_INFORMATION_ONLY" if dec["source_dir"]=="official_wan" else "OFFICIAL_VANILLA_ID_NOT_NATIVE_RENDERED" if dec["source_dir"]=="official_vanilla" else "NO_APPROPRIATE_RENDER",
   "mc_source_image_file":str(native_source(dec).relative_to(D)) if native_source(dec) else "",
   "official_mod_page_url":WAN_URL if dec["source_dir"]=="official_wan" else "",
   "approved_for_automatic_world_placement":"NO",
   "exact_visual_match_certified":"NO"
  }
  card(dec,orig).save(O/"cards"/f"{dec['i']:03}_PZ_vs_MC.jpg",quality=88,optimize=True)
  entries.append(record)
 save_csv(O/"BATCH_011_020_MANUAL_VISUAL_REVIEW.csv",entries)
 followups=[x for x in entries if x["manual_review_grade"].startswith("DEFER") or x["manual_review_grade"].startswith("SEARCH")]
 save_csv(O/"BATCH_011_020_FOLLOWUPS_OTHER_MODS.csv",followups)
 (O/"INDEX.html").write_text(index_html(entries),encoding="utf8")
 # Preserve prior completed 001-010 batch and mark 011-020 separately.
 groups=load_rows(D/"ten_batch_review/batch_001_010_v1/BATCHES_ALL_357_PROGRESS.csv")
 assert len(groups)==36 and groups[0]["review_status"]=="COMPLETED_CONDITIONAL_CANDIDATES"
 assert groups[1]["range"]=="011-020"
 groups[1]["review_status"]="COMPLETED_CONDITIONAL_CANDIDATES"
 groups[1]["review_file"]="batch_011_020_v1/BATCH_011_020_MANUAL_VISUAL_REVIEW.csv"
 save_csv(O/"BATCHES_ALL_357_PROGRESS.csv",groups)
 m={"total_styles":357,"batch_size":10,"total_batches":len(groups),"manually_reviewed_with_individual_rationales":len(entries),
   "batches_done":2,"batches_not_done":len(groups)-2,
   "native_source_comparison_images":sum(bool(native_source(x)) for x in DECISIONS),
   "deferred_other_mod_review":3,
   "promising_new_mod_information_only":sum(x["method"]=="NEW_MOD_OFFICIAL_INFO" for x in DECISIONS),
   "no_acceptable_equivalent":sum(x["method"]=="NO_ACCEPTABLE_SOURCE_MODEL" for x in DECISIONS),
   "exact_1to1_approved":0,"original_source_file_overwritten":False,
   "never_claim_remaining_337_as_reviewed":True}
 (O/"MANIFEST.json").write_text(json.dumps(m,ensure_ascii=False,indent=2)+"\n",encoding="utf8")
 docs=["# 로즈우드 357종 가구 10개 단위 수동 재매칭",
 "## 2차 011~020 (10/10 개별 시각 검수)",
 "기존 자동 매칭을 거부하고 011~020번 PZ 원본 완성 가구를 실제 이미지에서 관찰했다. 추가 16개의 Decocraft 원본 BBMODEL+실제 텍스처를 Blockbench 5.2.2에서 렌더해 10개를 개별 비교했다. 세 항목(011, 017, 019)은 다른 모드에서 추후 조사한다.",
 "개별 판정은 BATCH_011_020_MANUAL_VISUAL_REVIEW.csv 및 INDEX.html에 기록. MC 원본 .bbmodel/PNG와 바닐라 모델은 GitHub에 원본을 배포하지 않고 Blockbench 출력 이미지만 수록.",
 "## 10종 결과"]
 for x in entries:
  docs.append(f"- **#{x['index']:03} {x['pz_name']}/{x['pz_style']}**: {x['candidate_id'] or '대체품 미발견'} — {x['manual_review_grade']}. {x['manual_visual_review']}")
 docs+=["## 이어서 작업할 구간",
  "BATCHES_ALL_357_PROGRESS.csv에 **전체 36개 묶음**을 지정. 001~010과 011~020은 완료(최종 일치 인증 아님), 021~030이 다음이고 34개 묶음은 QUEUED 상태다.",
  "기존 357 매핑은 계속 원자료로 보존하고 매 묶음의 최종 재매핑 검수 데이터만 별도 파일로 누적한다. 설치 크기와 게임 기능 검증 전에는 월드의 실제 가구 치환에 적용 금지.",
  "## 관련 출처",
  "- 새 cardboard box와 공업용 선반은 Wan's Storage Shelves 공식 프로젝트: "+WAN_URL,
  "- Brown Shulker Box 보조 블록은 vanilla Minecraft 1.20.1 Mojang 클라이언트 JAR 파일에서 모델 근거를 재구성했다."
 ]
 (O/"README_KO.md").write_text("\n\n".join(docs)+"\n",encoding="utf8")
 with zipfile.ZipFile(O/"ROSEWOOD_BATCH_011_020_MANUAL_REVIEW.zip","w",zipfile.ZIP_DEFLATED,compresslevel=5) as z:
  for p in O.rglob("*"):
   if p.is_file() and p.name!="ROSEWOOD_BATCH_011_020_MANUAL_REVIEW.zip":
    z.write(p,p.relative_to(O))
 with zipfile.ZipFile(O/"ROSEWOOD_BATCH_011_020_MANUAL_REVIEW.zip") as z:
  assert z.testzip() is None
  assert "INDEX.html" in z.namelist()
 print("BATCH_COMPLETED",json.dumps(m,ensure_ascii=False),flush=True)
if __name__=="__main__":main()
