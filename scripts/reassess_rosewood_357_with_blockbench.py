#!/usr/bin/env python3
"""Evidence-graded Rosewood 357 PZ furniture vs real MC model rematch.
Never equate Blockbench render existence with a human visual approval.
"""
from pathlib import Path
from collections import Counter,defaultdict
from PIL import Image,ImageDraw,ImageFont
import csv,json,re,html,zipfile
import numpy as np

D=Path(__file__).resolve().parents[1]/"analysis/rosewood_furniture/2026-10-31"
O=D/"pz_mc_furniture_357_rematch_v2"
P=D/"complete_furniture_visual_3d_v1"
M=D/"minecraft_real_furniture_matches_v4"
V=D/"visual_pz_vs_mc_357_v3"
N=D/"blockbench_native_357_rematch_v1"
MANUAL={
 ("Chair","Grey"):("NEEDS_BETTER_SHAPE","회색 학교의자는 색상이 맞지만 PZ 의자 쿠션과 등받이 구조가 달라 동일 외형 대체품으로 확정 불가"),
 ("Television","Antique"):("REJECT_CURRENT_MATCH","좀보이드는 나무 케이스·안테나·다리가 달린 TV인데 Decocraft는 검은 CRT형 TV여서 외형 불일치"),
 ("Bed","Large Oak"):("CONDITIONAL_MATCH","둘 다 목제 침대지만 헤드보드/발판/침구와 크기가 달라 설치 모습 재검증 필요"),
 ("Grand Piano","Black"):("CONDITIONAL_MATCH","검은 그랜드 피아노로 형태가 유사하지만 좀보이드는 상판 닫힘, Decocraft는 상판 열림"),
}
MANUAL_INDEX={
 3:("REJECT_CURRENT_MATCH","원본은 갈색 종이상자, 후보는 알록달록 크레용 상자로 물체 용도가 다름"),
 11:("NEEDS_COLOR_VERIFICATION","금속 사물함 형태는 비슷하나 Blockbench 화면이 파란색으로 보여 회색 재질 변형 적용 검증 필요"),
 25:("NEEDS_BETTER_SHAPE","원본은 간단한 흰색 수납장형 카운터, 후보는 상판 및 개방형 선반과 구조가 다름"),
 32:("REJECT_CURRENT_MATCH","원본 X-press 커피머신인데 후보는 초록 원형 대나무 테이블"),
 35:("REJECT_CURRENT_MATCH","원본 목제 야외 벤치와 후보 검정 체육용 벤치는 구조 및 재료가 다름"),
 36:("REJECT_CURRENT_MATCH","원본 소형 송풍기/공기장치, 후보 가정용 의류 건조기"),
 38:("REJECT_CURRENT_MATCH","원본 높은 흰색 수납선반, 후보 접시용 진열 거치대"),
 40:("REJECT_CURRENT_MATCH","원본 작은 목재 테이블, 후보 높고 장식적인 검정 철제 테이블"),
 49:("NEEDS_COLOR_VERIFICATION","노란 벽면 사물함이지만 Blockbench 화면은 파란 사물함; 변형 텍스처 적용부터 검증"),
 52:("REJECT_CURRENT_MATCH","원본 나무 탁자, 후보는 흰색 디너 테이블 세팅 물체로 형태가 다름"),
 64:("REJECT_CURRENT_MATCH","원본 무광 회색 철제 모서리 카운터인데 후보 검정 줄무늬 식당 카운터와 구조 및 소재 다름"),
 67:("REJECT_CURRENT_MATCH","원본 낮은 직사각 목재 테이블, 후보 등나무 재질의 높은 사각 협탁"),
 75:("NEEDS_COLOR_VERIFICATION","컨테이너형 쓰레기통 형태는 유사하나 원본 주황색, 표시 후보 파란색으로 텍스처 변형 재확인"),
 88:("REJECT_CURRENT_MATCH","원본 파란색 세탁건조기 일체형, 후보는 별도 세탁기 모델로 기계 구성 다름"),
 90:("REJECT_CURRENT_MATCH","원본 어두운 목제 일반 침대와 후보 검정 체크 패턴 2인용 침대는 프레임 차이"),
 93:("REJECT_CURRENT_MATCH","원본 검정 단층 침대인데 후보는 밝은 2층 침대"),
 97:("REJECT_CURRENT_MATCH","원본 낮은 흰색 탁자, 후보 갈색 수납 서랍 협탁"),
 109:("CONDITIONAL_MATCH","둘 다 목재 업라이트 피아노지만 색상과 전면 패널, 악보대 세부 차이"),
 128:("REJECT_CURRENT_MATCH","원본 흰색 모서리 카운터인데 후보 청록색 줄무늬 식당 카운터"),
 134:("REJECT_CURRENT_MATCH","원본 녹색 가정용 레인지, 후보 벽돌 굴뚝형 피자 화덕"),
 142:("NEEDS_BETTER_SHAPE","둘 다 녹색 카운터이지만 원본은 평평한 박스형, 후보는 장식 줄무늬 식당 카운터"),
 143:("REJECT_CURRENT_MATCH","원본 가로로 긴 산업용 덤프스터인데 후보 세로형 바퀴 달린 쓰레기통"),
 160:("CONDITIONAL_MATCH","둘 다 초록 당구대이나 수평 2칸 및 큐·공 구성과 실제 설치 크기 확인 필요"),
 161:("REJECT_CURRENT_MATCH","원본 사람용 러닝머신, 후보는 카지노 행운의 룰렛 휠"),
 162:("CONDITIONAL_MATCH","파란 단문 사물함 형태 유사하지만 설치 방향과 치수는 아직 불명확"),
 168:("REJECT_CURRENT_MATCH","원본 파란 단층 침대, 후보 목제 2층 침대"),
 186:("NEEDS_COLOR_VERIFICATION","초록 사물함 원본에 파란 모델 색상이 표시됨. 변형 텍스처 정확 적용 여부 미검증"),
 193:("CONDITIONAL_MATCH","복고풍 주크박스의 기본 형태가 비슷하지만 색상·전면 패턴은 다름"),
 198:("REJECT_CURRENT_MATCH","원본 큐대 보관 거치대와 후보 목제 옷걸이는 다른 가구"),
 211:("REJECT_CURRENT_MATCH","원본 위성 안테나 접시이고 후보는 접시 수납 선반으로 의미가 다름"),
 213:("CONDITIONAL_MATCH","양쪽 모두 키 큰 냉장고지만 원본은 검정 단문, 후보는 회색 양문형으로 차이 큼"),
 214:("CONDITIONAL_MATCH","스탠드와 마이크 형태 유사하나 하단 받침과 마이크 크기 차이 확인"),
 228:("REJECT_CURRENT_MATCH","원본 낮은 검정 큐브 테이블과 후보는 높고 넓은 식당 테이블"),
 233:("REJECT_CURRENT_MATCH","원본 녹색 매달린 다중 램프, 후보는 길쭉한 단일 스탠드/기초 조명"),
 243:("CONDITIONAL_MATCH","둘 다 세로 벽거울이지만 원본은 단순 직사각, 후보 아치형 검정 프레임"),
 253:("CONDITIONAL_MATCH","작은 청색 레트로 냉장고 형태 유사. 곡률·손잡이/색상은 약간 다름"),
 254:("CONDITIONAL_MATCH","빨간 레트로 냉장고 형태 유사. 두 문 분할과 손잡이 차이 검토"),
 269:("NEEDS_COLOR_VERIFICATION","원본 빨간 킥 드럼 구성, 후보 검정 드럼 세트로 모델 형태는 유사하나 색상 차이"),
 272:("NEEDS_BETTER_SHAPE","원본 소형 노란 측면 장식 아케이드 기계 vs 후보 큰 검정 팩맨 게임기"),
 285:("REJECT_CURRENT_MATCH","군용 철망 구조 녹색 사물함과 일반 학교용 파란 철제 사물함은 구조 차이"),
 290:("CONDITIONAL_MATCH","양쪽 모두 소형 식기세척기이나 원본 갈색 빌트인 외형과 후보 회색 기계는 차이"),
 291:("REJECT_CURRENT_MATCH","원본 주황색 심플 오토만과 후보 꽃무늬 흰색 각진 발받침은 외형 차이"),
 309:("REJECT_CURRENT_MATCH","원본 볼링 기구 랙과 후보 알록달록 의류 진열 랙으로 기능이 다름"),
 315:("NEEDS_BETTER_SHAPE","두 게임기 모두 아케이드 캐비닛이지만 전면 디자인 및 게임 아트가 다름"),
 321:("REJECT_CURRENT_MATCH","원본 긴 흰색 낮은 테이블, 후보 작고 높은 목재 주방 테이블"),
 336:("REJECT_CURRENT_MATCH","원본 참나무 아기 침대/요람형 프레임, 후보 2층 침대"),
}
CATS={
 "chair":["chair","stool","seat"],"sofa":["sofa","couch"],"table":["table","desk"],
 "counter":["counter"],"shelf":["shelf","shelving","rack"],"bed":["bed","bunk"],
 "wardrobe":["wardrobe","closet"],"cabinet":["cabinet","drawer"],
 "toilet":["toilet"],"bath":["bath","tub"],"sink":["sink"],
 "fridge":["fridge","refrigerator","freezer"],"oven":["oven","stove"],
 "microwave":["microwave"],"piano":["piano"],"tv":["television","tv"],
 "bin":["trashcan","trash","bin","dumpster"],"arcade":["pinball","arcade"],
 "locker":["locker"],"computer":["computer","pc"],"washer":["washer"],
 "dryer":["dryer"],"jukebox":["jukebox"],"mirror":["mirror"],
 "lamp":["lamp","light"]
}
COLORS={"grey":["grey","gray"],"gray":["gray","grey"],"white":["white"],"black":["black"],
 "red":["red"],"blue":["blue"],"green":["green"],"yellow":["yellow"],"brown":["brown"],
 "orange":["orange"],"cyan":["cyan"],"pink":["pink"],"purple":["purple"]}
def readcsv(p):
 with p.open(encoding="utf-8-sig",newline="") as f:return list(csv.DictReader(f))
def writecsv(p,rows):
 if not rows:return
 with p.open("w",encoding="utf-8-sig",newline="") as f:
  w=csv.DictWriter(f,fieldnames=list(rows[0]),extrasaction="ignore");w.writeheader();w.writerows(rows)
def cat(s):
 s=" "+s.lower().replace("_"," ")+" "
 for k,words in CATS.items():
  if any(re.search(r"(?<![a-z])"+re.escape(w)+r"(?![a-z])",s) for w in words):
   return k
 return ""
def problems(pz,style,asset,parts,duplicate):
 phrase=(pz+" "+style).lower();mid=asset.split(":",1)[-1].lower()
 pcat,mcat=cat(pz),cat(mid)
 notes=[]
 if not asset:notes.append("NO_SOURCE_MC_ASSET")
 elif pcat and not mcat:notes.append("UNRECOGNIZED_MC_FURNITURE_FUNCTION")
 elif pcat and mcat and pcat!=mcat and {pcat,mcat} not in [
  {"chair","sofa"},{"shelf","cabinet"},{"wardrobe","cabinet"},{"table","counter"}]:
  notes.append("FUNCTION_CATEGORY_MISMATCH")
 if "folding" in phrase and "folding" not in mid:notes.append("FOLDING_FEATURE_MISSING")
 if "rattan" in phrase and "rattan" not in mid:notes.append("RATTAN_MATERIAL_NOT_CONFIRMED")
 if ("metal" in phrase or "steel" in phrase) and not any(x in mid for x in ["iron","steel","metal"]):
  notes.append("METAL_STYLE_NOT_CONFIRMED")
 for color,words in COLORS.items():
  if re.search(r"\b"+color+r"\b",phrase):
   exists=[c for c in COLORS if any(re.search(r"(?:^|_)"+re.escape(v)+r"(?:_|$)",mid) for v in COLORS[c])]
   if exists and color not in exists and not ("grey" in exists and color=="gray") and not ("gray" in exists and color=="grey"):
    notes.append("COLOR_CONFLICT_"+color+"_"+exists[0])
   break
 if int(parts or "1")>1:notes.append("MULTIPART_INSTALL_FOOTPRINT_UNVERIFIED")
 if duplicate>=6:notes.append("MANY_DISTINCT_PZ_STYLES_SHARE_SAME_MC_MODEL")
 return notes
def rankscore(pz,style,asset,old):
 if not asset:return -999
 a=cat(pz);b=cat(asset.split(":",1)[-1])
 score=float(old or 0)*.035
 if a:
  score+=(15 if a==b else 2 if {a,b} in [{"shelf","cabinet"},{"wardrobe","cabinet"}] else -20)
 for word,vals in COLORS.items():
  if re.search(r"\b"+word+r"\b",(pz+" "+style).lower()):
   if any(v in asset.lower() for v in vals):score+=7
   elif any(v in asset.lower() for v in COLORS):score-=8
   break
 for word in ["folding","rattan","metal","steel","glass","oak","birch","black","wood","grand","corner"]:
  if re.search(r"\b"+word+r"\b",(pz+" "+style).lower()):
   if word in asset.lower():score+=2
   elif word in ("folding","rattan","steel","metal"):score-=6
 return round(score,2)
def crop_bb(img):
 a=np.array(img.convert("RGBA"))
 bright=a[:,:,:3].max(axis=2)>11
 bright &= a[:,:,3]>4
 ys,xs=np.where(bright)
 if len(xs)>15:
  d=17;box=(max(0,int(xs.min())-d),max(0,int(ys.min())-d),
              min(img.width,int(xs.max())+d+1),min(img.height,int(ys.max())+d+1))
  img=img.crop(box)
 return img.convert("RGBA")
def makecard(rec,old):
 im=Image.new("RGB",(1170,530),(247,249,252))
 draw=ImageDraw.Draw(im)
 fonts="/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
 if Path("/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc").exists():
  fonts="/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc"
 ft=ImageFont.truetype(fonts,17);sm=ImageFont.truetype(fonts,11)
 draw.rounded_rectangle((12,43,571,432),radius=9,fill=(226,233,239))
 draw.rounded_rectangle((600,43,1157,432),radius=9,fill=(232,238,243))
 draw.text((20,10),str(rec["index"])+"  "+rec["pz_name"]+" / "+rec["pz_style"],font=ft,fill=(31,51,71))
 draw.text((24,56),"PROJECT ZOMBOID / complete furniture",font=sm,fill=(57,83,102))
 draw.text((614,56),"MINECRAFT / "+rec["render_label"],font=sm,fill=(57,83,102))
 src=P/rec["pz_preview"]
 with Image.open(src) as raw:
  p=raw.convert("RGBA");p.thumbnail((516,320),Image.Resampling.LANCZOS)
  im.paste(p,(int(292-p.width/2),int(247-p.height/2)),p)
 right=None
 if rec["image_evidence"]=="NATIVE_BLOCKBENCH_5_2_2":
  src=N/(rec["mc_id"].split(":",1)[-1]+"_BLOCKBENCH_VIEWPORT.png")
  if src.exists():
   with Image.open(src) as w:right=crop_bb(w)
 elif rec["image_evidence"]=="OLD_RENDER_APPROX":
  src=V/old["card_path"]
  with Image.open(src) as w:right=w.crop((595,93,1149,435)).convert("RGBA")
 if right:
  right.thumbnail((530,319),Image.Resampling.LANCZOS)
  im.paste(right,(int(874-right.width/2),int(247-right.height/2)),right)
 else:draw.text((678,234),"No verified model image",font=ft,fill=(151,76,68))
 draw.text((20,449),"PZ tiles: "+rec["pz_tiles"]+" / original parts "+rec["pz_parts"]+"  | MC model bound: "+rec["mc_bbox"][:48],font=sm,fill=(50,64,81))
 draw.text((20,468),"MC model ID: "+(rec["mc_id"] or "[none]")[:108],font=sm,fill=(50,64,81))
 draw.text((20,487),"Review: "+rec["visual_verdict"]+" | warnings: "+rec["warnings"][:105],font=sm,fill=(112,62,54))
 draw.text((20,506),"Native Blockbench source or clearly labelled old approximation; neither is a Minecraft in-game screenshot.",font=sm,fill=(118,76,61))
 return im
def page(rows):
 cards=[]
 for r in rows:
  title=r["pz_name"]+" / "+r["pz_style"]
  query=(title+" "+r["mc_id"]+" "+r["mod"]+" "+r["warnings"]).lower()
  cards.append('<article data-search="'+html.escape(query,quote=True)+'" data-grade="'+r["image_evidence"]+
   '" data-verdict="'+r["visual_verdict"]+'"><img loading="lazy" src="'+r["card"]+'">'+
   '<h2>'+html.escape(title)+'</h2><p>실제 MC 자산: <code>'+html.escape(r["mc_id"])+'</code></p>'+
   '<p>재검수: '+html.escape(r["visual_verdict"])+' · '+html.escape(r["manual_memo"])+'</p>'+
   '<p>PZ 완성 크기 '+r["pz_tiles"]+'칸 / 원본 부품 '+r["pz_parts"]+
   '개 · MC 모델 경계: '+html.escape(r["mc_bbox"])+'</p>'+
   '<p>대체 검토 후보: <code>'+html.escape(r["alternative_suggestion"] or "없음")+'</code> (자동 추천만)</p>'+
   '<p>검수 경고: '+html.escape(r["warnings"])+'</p>'+
   '<details><summary>원본 속성·모델 근거</summary><pre>'+html.escape(json.dumps({
   "PZ":json.loads(r["pz_properties_json"]),"MC":json.loads(r["mc_properties_json"]),
   "Blockbench_sha256":r["mc_native_model_sha256"]},ensure_ascii=False,indent=2))+
   '</pre></details></article>')
 return ("""<!doctype html><html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
 <title>357종 좀보이드 ↔ Blockbench 마크 가구 재대조</title>
 <style>body{margin:0;background:#edf1f5;color:#223b4e;font:14px system-ui,'Malgun Gothic',sans-serif}
 header{position:sticky;top:0;background:white;padding:16px 3%;border-bottom:1px solid #cad3dc;z-index:3}
 h1{font-size:22px}p{line-height:1.5}main{padding:18px 3%;display:grid;gap:18px;grid-template-columns:repeat(auto-fit,minmax(min(100%,540px),1fr))}
 article{background:white;border:1px solid #d5dfe6;border-radius:12px;padding:12px;box-shadow:0 2px 6px #1113}
 article img{display:block;width:100%;border-radius:7px}h2{font-size:17px}article p{font-size:13px;margin:6px 0}
 input,select{font:inherit;border:1px solid #b7c6d2;border-radius:7px;padding:9px}
 input{min-width:180px;flex:1}.tools{display:flex;flex-wrap:wrap;gap:8px}
 pre{white-space:pre-wrap;overflow-wrap:anywhere;font-size:11px;background:#eff4f7;padding:9px}</style></head><body>
 <header><h1>로즈우드 PZ 완성 가구 357종 ↔ 실제 마크 모드 파일 재대조</h1>
 <p><b>주의:</b> 오른쪽은 Decocraft만 Blockbench 5.2.2 원본 모델 직접 렌더. 나머지는 이전 비네이티브 근사 이미지이거나 미표시.
 357종 모두를 사람 눈으로 검수한 것이 아니며, 직접 시각 판정 4종 외에는 보류. 게임 내 배치·충돌·기능은 검증되지 않음.</p>
 <div class="tools"><input id="q" placeholder="가구/모드/블록ID/경고 검색">
 <select id="f"><option value="">이미지 전체</option><option value="NATIVE_BLOCKBENCH">실제 Blockbench</option>
 <option value="OLD_RENDER">비네이티브 근사</option><option value="NO_VISUAL">미렌더</option></select>
 <select id="v"><option value="">판정 전체</option><option value="REJECT_CURRENT_MATCH">기존 매칭 부적합</option>
 <option value="CONDITIONAL_MATCH">조건부</option><option value="NEEDS_COLOR_VERIFICATION">색상 변형 미확정</option><option value="NEEDS_BETTER_SHAPE">다른 형태 필요</option>
 <option value="NOT_VISUALLY_REVIEWED">추가 육안 검수 필요</option></select>
 <span id="count"></span></div></header><main>__CARDS__</main>
 <script>let cards=[...document.querySelectorAll('article')],q=document.getElementById('q'),f=document.getElementById('f'),v=document.getElementById('v'),c=document.getElementById('count');
 function show(){let n=0;for(const r of cards){let yes=r.dataset.search.includes(q.value.toLowerCase().trim())&&
 (!f.value||r.dataset.grade.includes(f.value))&&(!v.value||r.dataset.verdict===v.value);
 r.style.display=yes?'':'none';if(yes)n++}c.textContent=n+' / '+cards.length+'종'}q.oninput=f.onchange=v.onchange=show;show();</script></body></html>""").replace("__CARDS__","\n".join(cards))
def main():
 assert not O.exists()
 (O/"cards").mkdir(parents=True)
 initial=readcsv(M/"ROSEWOOD_357_PZ_TO_REAL_MINECRAFT_BLOCKSTATE_MATCH.csv")
 ranked=readcsv(M/"ALL_RANKED_MATCHED_MC_BLOCKSTATE_IDS.csv")
 details=readcsv(V/"ALL_357_PZ_MC_VISUAL_SIZE_PROPERTIES.csv")
 native=json.loads((N/"NATIVE_BLOCKBENCH_PROOF.json").read_text("utf8"))
 native_ids={x["id"]:x for x in native if x.get("loaded_verified") and x.get("native_model_screenshot") and (N/x["native_model_screenshot"]).exists()}
 assert len(initial)==len(details)==357
 detail_by={(r["pz_name"],r["pz_style"]):r for r in details}
 options=defaultdict(list)
 for c in ranked:options[(c["pz_name"],c["pz_style"])].append(c)
 reuse=Counter(r["mc_primary_blockstate_id"] for r in initial if r["mc_primary_blockstate_id"])
 stats=Counter();out=[];newrank=[]
 for i,r in enumerate(initial,1):
  pz,style=r["pz_model_name"],r["pz_model_style"]
  d=detail_by[(pz,style)]
  mid=r["mc_primary_blockstate_id"];mod=r["mc_primary_mod"]
  key=mid.split(":",1)[1] if mid else ""
  nativee=native_ids.get(key) if mod=="decocraft" else None
  if nativee:grade="NATIVE_BLOCKBENCH_5_2_2";label="actual native Blockbench 5.2.2"
  elif not mid or d["mc_render_status"].startswith("NO_"):
   grade="NO_VISUAL_MC_MODEL";label="NO REAL MODEL IMAGE"
  else:grade="OLD_RENDER_APPROX";label="OLD NON-BLOCKBENCH approximation"
  raw=sorted(options[(pz,style)],key=lambda c:rankscore(pz,style,c["blockstate_id"],c["score"]),reverse=True)
  for c in raw:
   newrank.append({"pz_name":pz,"pz_style":style,"source_mc_id":mid,
    "review_only_candidate_id":c["blockstate_id"],
    "prior_rank":c["rank"],"text_function_style_hint_score":rankscore(pz,style,c["blockstate_id"],c["score"]),
    "external_visual_equivalence_verified":"NO","may_replace_automatically":"NO"})
  sug=raw[0]["blockstate_id"] if raw and raw[0]["blockstate_id"]!=mid else ""
  manual=MANUAL.get((pz,style)) or MANUAL_INDEX.get(i)
  verdict=manual[0] if manual else "NOT_VISUALLY_REVIEWED"
  memo=manual[1] if manual else "자동 데이터 대조만 완료. 외형 일치는 검수자가 확인해야 함."
  flags=problems(pz,style,mid,r["pz_original_sprite_parts"],reuse[mid] if mid else 0)
  row={
   "index":i,"pz_name":pz,"pz_style":style,
   "pz_preview":r["pz_complete_png_path"],"pz_parts":r["pz_original_sprite_parts"],
   "pz_tiles":d["pz_size_tiles"],"pz_3d_bbox":d["pz_3d_bbox_blocks"],
   "pz_properties_json":d["pz_properties_json"],"mod":mod,"mc_id":mid,
   "mc_bbox":d["mc_model_dims"],"mc_properties_json":d["mc_properties_json"],
   "image_evidence":grade,"render_label":label,
   "mc_native_cubes":nativee["cubes"] if nativee else "",
   "mc_native_model_sha256":nativee["source_sha256"] if nativee else "",
   "mc_native_variant_texture_sha256":nativee["variant_sha256"] if nativee else "",
   "visual_verdict":verdict,"manual_memo":memo,
   "warnings":" | ".join(flags),
   "alternative_suggestion":sug,
   "old_match_class":r["match_class"],
   "auto_reprioritization_is_3d_appearance_review":"NO",
   "exact_same_furniture_appearance_confirmed":"NO",
   "native_is_minecraft_game_screenshot":"NO",
   "card":"cards/"+f"{i:03d}_{re.sub('[^a-z0-9_-]','_',key)[:45] if key else 'unmatched'}.jpg"
  }
  makecard(row,d).save(O/row["card"],quality=84,optimize=True)
  out.append(row);stats[grade]+=1;stats[verdict]+=1
  if i%60==0:print("REASSESS",i,dict(stats),flush=True)
 # Small contact sheets let the reviewer actually inspect different native models
 # without confusing the same MC asset repeated across PZ variants.
 contacts=O/"contact_sheets";contacts.mkdir()
 seen=set();native_unique=[]
 for row in out:
  if row["image_evidence"]!="NATIVE_BLOCKBENCH_5_2_2" or row["mc_id"] in seen:continue
  seen.add(row["mc_id"]);native_unique.append(row)
 for start in range(0,len(native_unique),6):
  group=native_unique[start:start+6]
  sheet=Image.new("RGB",(1920,920),(248,250,252))
  for k,row in enumerate(group):
   with Image.open(O/row["card"]) as src:
    a=src.convert("RGB");a.thumbnail((630,445),Image.Resampling.LANCZOS)
    sheet.paste(a,((k%3)*640+5,(k//3)*460+5))
  sheet.save(contacts/("NATIVE_BLOCKBENCH_REVIEW_%02d.jpg"%(start//6+1)),quality=85)
 writecsv(O/"ALL_357_REMATCH_REVIEW.csv",out)
 writecsv(O/"ALL_881_CANDIDATES_REPRIORITIZED_REVIEW_ONLY.csv",newrank)
 writecsv(O/"VISUALLY_REVIEWED_50.csv",[r for r in out if r["visual_verdict"]!="NOT_VISUALLY_REVIEWED"])
 (O/"INDEX.html").write_text(page(out),encoding="utf8")
 manifest=dict(total_pz_styles=len(out),native_unique_decocraft_models=len(native_ids),
    native_blockbench_style_cards=stats["NATIVE_BLOCKBENCH_5_2_2"],
    previous_approximation_only_cards=stats["OLD_RENDER_APPROX"],
    no_visual_mc_model_cards=stats["NO_VISUAL_MC_MODEL"],
    manually_reassessed_representative_styles=sum(r["visual_verdict"]!="NOT_VISUALLY_REVIEWED" for r in out),
    other_styles_not_manually_approved=stats["NOT_VISUALLY_REVIEWED"],
    visually_rejected=stats["REJECT_CURRENT_MATCH"],visually_conditional=stats["CONDITIONAL_MATCH"],visually_color_variant_uncertain=stats["NEEDS_COLOR_VERIFICATION"],
    visually_needs_better=stats["NEEDS_BETTER_SHAPE"],original_mc_candidates_replaced_automatically=0,
    exact_pz_to_mc_3d_matches_certified=0,
    mc_in_game_screenshots=0,all_candidate_rows=len(newrank))
 assert manifest["total_pz_styles"]==357
 assert manifest["manually_reassessed_representative_styles"]==50
 assert sum(stats[g] for g in ["NATIVE_BLOCKBENCH_5_2_2","OLD_RENDER_APPROX","NO_VISUAL_MC_MODEL"])==357
 (O/"MANIFEST.json").write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+"\n",encoding="utf8")
 (O/"README_KO.md").write_text(
 "# 로즈우드 357종 마인크래프트 가구 Blockbench 근거 기반 재대조\n\n"+
 "## 실제 새로 수행한 작업\n"+
 "이번에는 원본 마크 Decocraft 모드의 bbmodel 및 색상 텍스처를 실제 Blockbench 데스크톱에서 열어 스크린샷으로 비교했어.\n"+
 "오른쪽 Blockbench 이미지가 있는 건 확정된 가구가 아니라 실재하는 형상을 볼 수 있는 후보라는 뜻이야.\n"+
 "나머지 모드의 이미지는 기존 근사 모델로 **확실히 구분**했고, 검증됐다고 표시하지 않았어.\n\n"+
 "## 검증 상태\n"+ "\n".join(f"- {k}: {v}" for k,v in manifest.items())+
 "\n\n## 직접 육안 비교한 대표 4건\n"+
 "\n".join(f"- {k[0]}/{k[1]}: {v[0]} — {v[1]}" for k,v in MANUAL.items())+
 "\n\n## 대체 후보 주의\n"+
 "후보 재정렬 점수는 이름·기능·색상 일치 단서일 뿐 외형 비교 점수가 아니야. 기존 모델을 자동 교체하지 않았어.\n"+
 "색상 변형은 Blockbench에서 .bbmodel 내 내장 기본 텍스처와 각 JAR material 텍스처 적용의 일치가 확인되지 않아 별도 미확정으로 기록했어.\n정확한 충돌박스, 멀티블록 배치 및 게임 내 기능은 실행 검증 전이야.\n\n"+
 "## 열기\nZIP 압축 해제 후 INDEX.html을 열어 357개 가구를 검색하고, 원본 속성·크기를 확인해.\n",
 encoding="utf8")
 with zipfile.ZipFile(O/"ROSEWOOD_357_BLOCKBENCH_REMATCH.zip","w",zipfile.ZIP_DEFLATED,compresslevel=4) as z:
  for p in sorted(O.rglob("*")):
   if p.is_file() and p.name!="ROSEWOOD_357_BLOCKBENCH_REMATCH.zip":z.write(p,p.relative_to(O))
 with zipfile.ZipFile(O/"ROSEWOOD_357_BLOCKBENCH_REMATCH.zip") as z:
  assert z.testzip() is None
  assert "INDEX.html" in z.namelist()
 print("REASSESS_COMPLETE",json.dumps(manifest,ensure_ascii=False),flush=True)
if __name__=="__main__":main()
