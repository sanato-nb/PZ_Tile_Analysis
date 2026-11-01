#!/usr/bin/env python3
"""Tenth group (091..100) manually checked against complete PZ assets and actual
Decocraft Blockbench 5.2.2 renders. Four mismatch items remain deferred.
Persist all 36 batch statuses, never auto-approve visually unverified furniture.
"""
import csv,json,zipfile,html
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import numpy as np
D=Path(__file__).resolve().parents[1]/"analysis/rosewood_furniture/2026-10-31"
SOURCE=D/"all_357_complete_native_comparisons_v1"
PZ=D/"complete_furniture_visual_3d_v1"
B=D/"ten_batch_review"
N=B/"10_091_100/extra_decocraft_render"
N1=D/"blockbench_native_replacement_candidates_v1"
N2=B/"02_011_020/extra_decocraft_render"
OUT=B/"batch_091_100_v1"
DECISIONS=json.loads(r'''[{"i":91,"src":"new","model":"tv_old","candidate":"decocraft:tv_old","second":"decocraft:crt_tv [black plastic box without wood legs or V antenna, rejected]","status":"STRONG_VISUAL_CONDITIONAL_ANTIQUE_WOODEN_TELEVISION","shape":"Single-tile tabletop/standing 1960s wood-grain console television with tall wooden box, two angled roof V antenna rods, black screen at front left, vertical dial controls on right and four thin wood legs","size":"PZ 1×1 with visible wood shell, metal rabbit-ear V antenna, four legs; MC one source model, actual placement and antenna hitbox untested","why":"PZ 원본은 1960년대 나무 프레임, 다리 네 개, 윗면 V자 토끼귀 안테나, 전면 왼쪽 화면과 오른쪽 세로 조절부가 있는 골동품 TV다. Decocraft TV Old 원본 30큐브 모델을 실제 Blockbench로 열었더니 나무 프레임/다리/V 안테나/측면 전면 조절 노브가 모두 나타나 기존 Decocraft CRT TV(검정 플라스틱 상자)보다 훨씬 정확하다. 다만 원본 화면은 어둡고 버튼은 세로로 더 작고, MC 모델의 나무톤이 조금 더 진하고 안테나 막대 굵기/각도 차이가 있어 최종 1:1은 아니다.","followup":"MC TV Old 런타임 블록/전원/회전/높이 및 PZ 1×1 실제 부피 비교. 설치 후 화면 재현과 주변 충돌 검증."},{"i":92,"src":"new","model":"bottom_cabinet_1_birch","candidate":"","second":"minecraft:birch_planks + birch_trapdoor [vanilla assembly concept; no in-game block placement test]; decocraft:bottom_cabinet_1_oak [wrong drawer/door/white countertop]","status":"DEFER_GENERIC_SHOP_PLAIN_LIGHT_WOODEN_COUNTER","shape":"Simple pale honey-yellow/beige 1×1 single shop checkout counter with smooth blond wood rectangular top; front/side blank wood panels, no door, no drawer, no handle","size":"PZ 1×1 full counter at waist height; MC cabinet is single source model with white countertop and exposed drawer, not an exact block substitute","why":"PZ는 상판과 몸체 모두 밝은 황갈색이며 앞면에 서랍·문·손잡이가 없는 매끈한 상점용 1칸 카운터다. 기존 Macaw Acacia Counter는 상판만 주황빛, 몸체는 어두운 회색/검정이라 다름. 새 Decocraft Bottom Cabinet 1 Birch/Oak는 목재 몸체는 더 가깝지만 흰 상판과 서랍 1개+손잡이 달린 아래 문이 노출되어 원본 단순한 앞판과 불일치. Diner Counter Yellow는 배포 모델 존재는 확인했지만 이 실행에서 렌더 검증 실패하여 비교 증거로 사용하지 않음.","followup":"완전히 빈 판넬+황갈색 목제 상판인 1×1 카운터 모드 검색. 바닐라 자작나무 판자/밝은 덫문 조합은 충돌·높이·설치 순서 검증 후 도입."},{"i":93,"src":"new","model":"single_bed_black_white","candidate":"decocraft:single_bed_black_white","second":"minecraft:white_bed [vanilla narrower look; black framed head+foot absent]","status":"CONDITIONAL_SINGLE_BLACK_WOOD_WHITE_BED_CHECKER_MISMATCH","shape":"PZ 1×2 two-part single fancy bed with tall black slatted headboard and shorter matching black slatted footboard, one smooth white/cream mattress/blanket, no visible puffed pillow","size":"PZ two source sprites form 1×2 single bed; Decocraft single bed dimensions/2-block placement and head/foot collisions not runtime verified","why":"PZ는 두 개 타일의 검정 금속/목재 세로살 침대 프레임(머리판·발판)과 무늬 없는 크림빛 흰 침구로 구성된다. 기존 Decocraft Birch Black은 밝은 원목 프레임+검정 체크 침구로 색이 거꾸로였다. 새 Single Bed Black White 실제 29큐브 모델은 검정 세로살 머리판·발판, 흰 침구, 좁은 1인 침대 구조가 명확하게 일치하는 방향이다. 하지만 MC 침구가 흰 회색 체크무늬이고 커다란 흰 베개와 접힌 담요가 돌출돼, PZ의 매끈한 단색 매트리스와 차이. 1×2 타일 점유 역시 게임에서 미검증.","followup":"무늬 없는 크림/흰 침구와 검정 슬랫 프레임 조합을 찾고 Minecraft 1×2 설치, 방향 및 수면 기능 확인."},{"i":94,"src":"new","model":"bamboo_coffee_table_round_yellow","candidate":"","second":"decocraft:diner_table_round_yellow [yellow top but steel pedestal]; Benched is picnic bench, not a round table","status":"DEFER_LIGHT_WOOD_ROUND_TRIPOD_TABLE","shape":"Light honey oak round tabletop with warm brown central slender post and three splayed simple feet, 1-tile cafe table","size":"PZ 1×1 light wooden tall pedestal table; MC bamboo coffee table is low side table/4-frame understructure","why":"PZ는 밝은 나무 원형 상판 아래 갈색 중심 기둥 1개와 작게 뻗은 세 발이 있는 테이블. 기존 Macaw Acacia Coffee Table는 회색 사각 두꺼운 상판만 렌더돼 구조가 틀렸다. 새 Decocraft Bamboo Round Yellow는 밝은 노란 원형 상판이지만 높이가 낮고 옆면 십자 격자와 4개의 바깥 다리가 둘러싸기 때문에 기존 삼발이 목재 원형 식탁이 아니다. Diner Round Yellow도 금속 기둥+노란 플라스틱 상판이라 목재색과 다름.","followup":"Forge 1.20.1 원목 원형 십자/삼발이 한 기둥 카페 테이블 모드 검색. 실제 게임 설치 1×1 여부 확인."},{"i":95,"src":"new","model":"diner_table_round_yellow","candidate":"","second":"decocraft:diner_table_round_black [same metallic legs, wrong dark tabletop]","status":"DEFER_ORANGE_WOOD_ROUND_TRIPOD_TABLE","shape":"Warm medium orange/brown circular wood top with matching brown wooden center stem and 3 branching wooden feet","size":"PZ 1×1 wooden pedestal stand, source sprites 1; MC metal tripod source geometry single block","why":"PZ Round Table은 094와 구조가 거의 같지만 상판이 더 오렌지빛 갈색이며 다리도 같은 갈색 나무다. 기존 Macaw 회색 판은 유사성이 없다. 새 Decocraft Diner Table Round Yellow는 원형 상판·세발 받침이라는 기본 실루엣은 유사하지만 판은 노란 플라스틱이고 다리·기둥은 은회색 금속이라 원본 목재 재질과 오렌지톤이 맞지 않는다. 정확히 같은 가구로 승인하면 안 된다.","followup":"오렌지/갈색 목재 원형 단일기둥 테이블; 크래프트·카페 가구 모드에서 원본 3D 모델 대조."},{"i":96,"src":"new","model":"vanity_left_birch","candidate":"decocraft:vanity_left_birch","second":"decocraft:vanity_right_birch [same two drawers; mirror angle opposite], decocraft:closet_3_birch [3 drawers but NO mirror]","status":"CONDITIONAL_MIRRORED_BIRCH_VANITY_DRAWER_COUNT_MISMATCH","shape":"1×1 small light oak three-drawer chest of drawers with paired dark round knobs on EACH drawer (six knobs), thick plain wood top and tall arched vanity mirror in the same wood frame integrated above chest","size":"PZ 1×1 three-drawer vanity with attached mirror. Decocraft vanity left single source asset, mirror+two drawers; runtime footprint and mirror collision untested","why":"PZ 원본은 나무 서랍장(3단, 서랍당 검정 원형 손잡이 2개) 위에 곡선 상단의 세로 거울이 붙은 한 덩어리 화장대다. 기존 Macaw Bookshelf Drawer는 녹색 벽 판만 나온 부품 누락이고 거울이 없다. 새 Decocraft Vanity Left Birch의 실제 20큐브 원본 모델은 연목색 프레임, 큰 거울, 서랍 본체가 모두 일체형이어서 물건 유형을 올바르게 맞췄다. 다만 2단 서랍에 은색 긴 손잡이 하나씩이라 PZ의 3단/검정 손잡이 6개와 불일치, 거울 상단도 다각형이다. 더 닮은 모델을 찾기 전까지 조건부.","followup":"1×1 3단 6검정손잡이와 호형 프레임 거울의 단일 모델 추가 검색, 거울 반사·서랍 저장/크기 검증."},{"i":97,"src":"new","model":"wooden_table_white","candidate":"","second":"decocraft:cottage_coffee_table [brown low table, wrong white], vanilla smooth quartz slab+iron trapdoor/fence legs schematic untested","status":"DEFER_LOW_SMALL_WHITE_RECTANGULAR_TABLE","shape":"Compact LOW creamy ivory rectangular small coffee table with slightly inset single-layer tabletop and four short thick square ivory wooden legs; no drawers/no shelving","size":"PZ 1×1 low coffee table; MC wooden_table_white taller dining table with decorated carved legs; height/footprint differ","why":"PZ는 흰색/아이보리 낮은 사각 테이블로 윗판과 짧고 단순한 네 다리만 있다. 이전 Decocraft Bedside Table Open 1 White는 실제 파일에서 갈색 2단 서랍장이 펼쳐진 모습이라 전혀 다른 가구. 새 Decocraft Wooden Table White는 아이보리색 상판/네 다리는 있지만 **높이가 식탁급이고 굵은 장식 다리**가 있어 원본 낮은 테이블과 다르다. Cottage Coffee Table은 낮지만 짙은 갈색, Bamboo Square Yellow는 노랑 라탄 격자라 불일치.","followup":"1.20.1 Forge 하얀 사각 낮은 4다리 커피테이블 모델 검색; 바닐라 눈블록/쿼츠 반블록 조합은 1×1 높이/공간 확인이 먼저."},{"i":98,"src":"new","model":"toaster_silver","candidate":"decocraft:toaster_silver","second":"decocraft:toaster_cream [slightly lighter], refurbished_furniture:dark_toaster [wrong black and incomplete]","status":"STRONG_VISUAL_CONDITIONAL_SILVER_COMPACT_TWO_SLOT_TOASTER","shape":"Small silver/chrome freestanding rounded-top 2-slot toaster with two parallel top bread apertures and dark feet, small dark lever/side control, sits on counter","size":"PZ 1×1 tile sprite with physically small tabletop object; Decocraft toaster model is a small multi-cube prop, actual size in block units and surface placement untested","why":"PZ는 손바닥만한 은회색 크롬 빵 토스터이며 윗면에 평행한 2개의 투입 슬롯, 둥근 모서리, 어두운 받침/측면 손잡이가 있다. 기존 Refurbished Dark Toaster의 불완전 검정 상자 렌더보다, 새 Decocraft Toaster Silver의 진짜 14큐브 원본은 은색 몸체·위 2개 슬롯·받침·모서리 깎임이 일치해서 외형이 상당히 근접한다. 그래도 PZ는 전면 좌하단 둥근 패널이 있고 MC는 각진 윗모서리라 완전 1:1은 아니며 설치 위치·음식 굽기 기능 확인 전.","followup":"마크 작은 은색 토스터의 카운터 윗면 배치·16x 모델 좌표·음식 토스트 기능 검증."},{"i":99,"src":"new","model":"chair_1_cherry","candidate":"","second":"decocraft:school_chair_orange [orange but PLASTIC seat+gray metal legs], decocraft:chair_1_palm [too pale]","status":"DEFER_ORANGE_WOOD_CHAIR_SINGLE_HORIZONTAL_BACKREST","shape":"Small bright reddish/orange varnished wooden restaurant chair, plain thin straight four wood legs, smooth matching orange wood seat, narrow back posts and ONE horizontal rectangular back slat with large open space","size":"PZ 1×1 restaurant chair; Decocraft cherry chair 1-block source model, not accurate color/back","why":"PZ 식당 의자는 선명한 주황 갈색 나무 좌석/다리 네 개와 등받이에 하나의 가로 나무대가 걸친 구조다. 기존 PFM Leather Armchair 렌더는 회색 한 판뿐이었고 팔걸이부터 물건 종류가 잘못되었다. Decocraft Chair 1 Cherry는 나무 4다리 형태는 맞지만 전체가 옅은 분홍빛이고 등받이에 여러 세로살이 있어 핵심적인 주황 나무색/가로대 1개와 다르다. School Chair Orange는 색상은 비슷하지만 주황 플라스틱+회색 금속 다리여서 재질이 다르고 Diner Chair Orange는 흰 줄무늬 플라스틱이라 불가.","followup":"Forge 1.20.1 실제 PZ의 주황 목재 의자와 비슷한 Cafe/restaurant simple slat-back chair JAR 모델 검색."},{"i":100,"src":"new","model":"picnic_table","candidate":"decocraft:picnic_table","second":"Benched 1.20.1 Forge oak/spruce picnic bench (2×2 source-described; actual Java model not yet rendered)","status":"STRONG_VISUAL_CONDITIONAL_CONNECTED_PICNIC_TABLE_BENCHES","shape":"Four PZ source sprites form complete outdoor 2×2 picnic table with six broad pale honey-oak planks tabletop, TWO long side benches fixed as one integrated item, diagonal A-frame dark green painted support legs and bottom crossbar","size":"PZ 4 parts, source tile 2×2; Decocraft authentic 22-cube BBMODEL has attached two long benches and A-frame but its 2×2 actual in-game blocks footprint unverified. Benched official 2×2 explicitly verified by mod page, native model unrendered","why":"PZ 원본은 2×2 네 개 타일을 합쳐야 하는 나무 피크닉 테이블로 양쪽에 긴 좌석 두 개가 붙고 비스듬한 프레임 다리로 지지된다. 이전 Macaw Glass Table 렌더는 얇은 나무 평판 한 장이라 완전히 틀린 가구였다. 이번 Decocraft Picnic Table **실제 22큐브 BBMODEL을 전체 렌더**했더니 나무 상판+양쪽 2개 벤치+A형 경사 받침대가 함께 나타나 **완성형 전체 구조가 매우 유사**하다. 다만 PZ는 녹색 도색 금속/목재 다리인 데 반해 MC는 전부 밝은 목재이고 상판 판자 수·다리 색이 다르며, 2×2 칸을 차지하는지는 마크 게임에서 아직 검증하지 않았다. Benched 모드에도 2×2 실용 피크닉 벤치가 공식적으로 있으므로 추가 대안으로 남김.","followup":"Decocraft Picnic Table 실제 배치 좌표/2×2 충돌/bench 2명 착석 검증. https://modrinth.com/mod/benched 의 1.20.1 Forge 2×2 Oak/Spruce 2인 피크닉 벤치 모델 직접 렌더해 녹색 A형/높이/색 비교."}]''')
def rows(p):
 with p.open(encoding="utf-8-sig",newline="") as f:return list(csv.DictReader(f))
def writecsv(p,items):
 with p.open("w",encoding="utf-8-sig",newline="") as f:
  w=csv.DictWriter(f,list(items[0]),extrasaction="ignore");w.writeheader();w.writerows(items)
def font(n):
 for x in ["/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc",
 "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"]:
  if Path(x).is_file():return ImageFont.truetype(x,n)
 return ImageFont.load_default()
def cropped(img):
 a=np.array(img.convert("RGBA"))
 mask=(a[:,:,:3].max(axis=2)>10)&(a[:,:,3]>4)
 y,x=np.where(mask)
 if len(x)>20:
  m=15;img=img.crop((max(0,int(x.min())-m),max(0,int(y.min())-m),
                        min(img.width,int(x.max())+m+1),min(img.height,int(y.max())+m+1)))
 return img.convert("RGBA")
def build_card(a,original,source):
 im=Image.new("RGB",(1350,600),(248,249,251));d=ImageDraw.Draw(im)
 d.rounded_rectangle((12,44,663,464),radius=9,fill=(231,237,242))
 d.rounded_rectangle((683,44,1335,464),radius=9,fill=(235,240,245))
 name=(original["pz_name"]+" / "+original["pz_style"]).strip(" /")
 d.text((19,10),str(a["i"]).zfill(3)+"  "+name,font=font(21),fill=(33,57,79))
 d.text((25,57),"PROJECT ZOMBOID / assembled original (provisional)",font=font(13),fill=(50,75,94))
 d.text((691,57),"MINECRAFT / REAL native Blockbench 5.2.2 model",font=font(13),fill=(50,75,94))
 with Image.open(PZ/original["pz_preview"]) as z:
  z=z.convert("RGBA");z.thumbnail((581,351),Image.Resampling.LANCZOS)
  im.paste(z,(int(339-z.width/2),int(258-z.height/2)),z)
 if a["i"]==43:
  # Two real source-model module screenshots side-by-side. NOT a fabricated seamless connected render.
  for filename,cx,label in [
   ("rattan_couch_left_brown_BLOCKBENCH_VIEWPORT.png",845,"LEFT MODULE"),
   ("rattan_couch_right_brown_BLOCKBENCH_VIEWPORT.png",1173,"RIGHT MODULE")]:
   with Image.open(N/filename) as z:
    z=cropped(z);z.thumbnail((310,295),Image.Resampling.LANCZOS)
    im.paste(z,(int(cx-z.width/2),int(265-z.height/2)),z)
   d.text((cx-65,420),label,font=font(12),fill=(50,75,94))
 else:
  if source is None:
   d.rounded_rectangle((713,125,1298,394),radius=12,outline=(160,90,80),width=3)
   d.text((733,203),"NO SOURCE-VERIFIED EQUIVALENT",font=font(18),fill=(131,66,61))
   d.text((733,242),"Other mod model pending visual verification",font=font(12),fill=(121,75,68))
  else:
   with Image.open(source) as z:
    z=cropped(z);z.thumbnail((584,350),Image.Resampling.LANCZOS)
    im.paste(z,(int(1009-z.width/2),int(268-z.height/2)),z)
 d.line((19,475,1330,475),fill=(176,188,200),width=2)
 d.text((25,491),("PZ parts: "+original["pz_parts"]+"  / footprint: "+original["pz_grid"]+
   " | "+a["size"])[:125],font=font(11),fill=(46,68,83))
 label="Proposed: "+(a["candidate"] or "NO ACCEPTABLE MATCH – inspected model REJECTED")
 d.text((25,517),(label+"  / inspected "+a["model"])[:130],font=font(11),fill=(52,66,83))
 d.text((25,543),("Manual review: "+a["status"])[:128],font=font(12),fill=(131,64,59))
 d.text((25,574),"Source model image only. NOT actual Minecraft game placement or certified 1:1 visual/size equivalence.",font=font(11),fill=(125,82,72))
 return im
def htmlpage(items):
 block=[]
 for item in items:
  label=(item["pz_name"]+" / "+item["pz_style"]).strip(" /")
  block.append('<article><img loading="lazy" alt="'+html.escape(label,quote=True)+'" src="'+item["card_path"]+'">'+
   '<h2>'+html.escape(label)+'</h2>'+
   '<p><b>검수:</b> '+html.escape(item["review_status"])+'</p>'+
   '<p><b>실제 선정 후보:</b> <code>'+html.escape(item["new_candidate_id"] or "없음 — 후속 검토")+'</code></p>'+
   '<p><b>실제로 렌더해 비교한 모델:</b> '+html.escape(item["visually_inspected_model_id"])+'</p>'+
   '<p><b>다른 후보:</b> '+html.escape(item["secondary_candidate_id"])+'</p>'+
   '<p><b>크기:</b> '+html.escape(item["size_and_placement_notes"])+'</p>'+
   '<p><b>원본 외형:</b> '+html.escape(item["pz_shape_features"])+'</p>'+
   '<p><b>판정 이유:</b> '+html.escape(item["manual_review_reason"])+'</p>'+
   '<p><b>다음 조치:</b> '+html.escape(item["followup_requirement"])+'</p>'+
   '<details><summary>PZ 원본 메타데이터</summary><pre>'+html.escape(item["pz_properties_json"])+'</pre></details></article>')
 return ('''<!doctype html><html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Rosewood 10-batch group 03 091–100</title>
 <style>body{margin:0;background:#ecf1f5;color:#293f50;font:14px system-ui,'Malgun Gothic',sans-serif}
 header{position:sticky;top:0;background:white;border-bottom:1px solid #d1dce6;padding:18px 3%}
 h1{font-size:22px;margin:0 0 9px}main{display:grid;gap:18px;padding:19px 3%;grid-template-columns:repeat(auto-fit,minmax(min(100%,570px),1fr))}
 article{background:white;border:1px solid #d4dfe8;border-radius:12px;padding:12px}article img{width:100%;border-radius:8px}
 h2{font-size:17px}p{line-height:1.55;margin:7px 0}code{overflow-wrap:anywhere}
 pre{background:#f0f3f7;white-space:pre-wrap;overflow-wrap:anywhere;font-size:11px;padding:10px}
 </style></head><body><header><h1>좀보이드 가구 ↔ 마크 실제 가구 모델 — 4차 091~100</h1>
 <p>원본 좀보이드 완성 가구와 실제 Minecraft Decocraft 원본 모델을 Blockbench에서 직접 렌더해 10종을 하나씩 수동 검수함.
 모양이 틀린 오른쪽 이미지는 명확하게 거절 상태로 표시함. 2개 스프라이트로 된 욕조·탁자는 조립 및 크기 추가 검증.
 보류 항목은 신규 가구 모드나 바닐라 조합을 후속 검토하며, 자동 월드 적용 확정 0개.</p></header><main>%%%BODY%%%</main></body></html>''').replace("%%%BODY%%%","\n".join(block))
def main():
 assert not OUT.exists(),"Cannot overwrite past manual review"
 (OUT/"cards").mkdir(parents=True)
 original=rows(SOURCE/"ALL_357_FULL_RENDER_MATCHING.csv")
 assert len(original)==357
 assert [x["i"] for x in DECISIONS]==list(range(91,101))
 proofs={}
 for srcroot in (N,):
  f=srcroot/"NATIVE_BLOCKBENCH_PROOF.json"
  assert f.is_file(),f
  proofs[str(srcroot)]={
   x["id"]:x for x in json.loads(f.read_text("utf8")) if x.get("loaded_verified") and x.get("native_model_screenshot")
  }
 review=[]
 for dec in DECISIONS:
  o=original[dec["i"]-1]
  assert int(o["index"])==dec["i"]
  source={"new":N,"none":None}[dec["src"]]
  e=proofs[str(source)].get(dec["model"]) if source else None
  assert e or dec["src"]=="none",(dec,e)
  f=source/e["native_model_screenshot"] if e else None
  assert f is None or f.is_file(),f
  fn=f'cards/{dec["i"]:03d}_PZ_vs_MC.jpg'
  build_card(dec,o,f).save(OUT/fn,quality=87,optimize=True)
  review.append({
    "index":dec["i"],"pz_name":o["pz_name"],"pz_style":o["pz_style"],
    "pz_original_complete_preview":o["pz_preview"],
    "pz_parts":o["pz_parts"],"pz_footprint":o["pz_grid"],
    "pz_properties_json":o["pz_original_properties_json"],
    "previous_mc_candidate_id":o["chosen_mc_id"],
    "previous_match_needs_review":"YES",
    "new_candidate_id":dec["candidate"],
    "secondary_candidate_id":dec["second"],
    "visually_inspected_model_id":"decocraft:"+dec["model"] if e else "NO_RELEVANT_NATIVE_MODEL",
    "native_source_model_sha256":e["source_sha256"] if e else "",
    "native_source_variant_sha256":e["variant_sha256"] if e else "",
    "native_model_cubes":e["cubes"] if e else 0,
    "native_source_screenshot_path":str(f.relative_to(D)) if f else "",
    "pz_shape_features":dec["shape"],
    "size_and_placement_notes":dec["size"],
    "review_status":dec["status"],
    "manual_review_reason":dec["why"],
    "followup_requirement":dec["followup"],
    "exact_1_to_1_visual_match_approved":"NO",
    "approved_for_minecraft_world_replacement":"NO",
    "card_path":fn
  })
 writecsv(OUT/"BATCH_091_100_MANUAL_VISUAL_REVIEW.csv",review)
 deferred=[x for x in review if x["review_status"].startswith("DEFER")]
 assert [x["index"] for x in deferred]==[92,94,95,97,99]
 writecsv(OUT/"BATCH_091_100_DEFERRED_OTHER_MODS.csv",deferred)
 groups=rows(B/"batch_081_090_v1/BATCHES_ALL_357_PROGRESS.csv")
 assert len(groups)==36
 assert [x["range"] for x in groups[:10]]==["001-010","011-020","021-030","031-040","041-050","051-060","061-070","071-080","081-090","091-100"]
 assert all(x["review_status"]=="COMPLETED_CONDITIONAL_CANDIDATES" for x in groups[:9])
 groups[9]["review_status"]="COMPLETED_CONDITIONAL_CANDIDATES"
 groups[9]["review_file"]="batch_091_100_v1/BATCH_091_100_MANUAL_VISUAL_REVIEW.csv"
 writecsv(OUT/"BATCHES_ALL_357_PROGRESS.csv",groups)
 (OUT/"INDEX.html").write_text(htmlpage(review),encoding="utf8")
 manifest={"scope":"091-100","total_pz_styles":357,"total_batches":36,
  "batches_reviewed":10,"batches_unreviewed":26,"individual_items_checked_this_batch":10,
  "unique_decocraft_models_rerendered":len(proofs[str(N)]),
  "native_model_pz_comparison_cards":len(review),
  "conditional_match_proposals":len(review)-len(deferred),
  "deferred_other_mod_or_vanilla_search":len(deferred),
  "exact_1_to_1_matches_certified":0,
  "minecraft_game_install_collision_verified":0,
  "source_tables_overwritten":False}
 (OUT/"MANIFEST.json").write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+"\n",encoding="utf8")
 lines=[
 "# 로즈우드 357종 — 10차 091~100번 실제 가구 매칭 개별 시각 검수",
 "PZ B42 원본 완성 가구 10종의 형상/모델 구성/원본 속성 및 크기 vs Minecraft Java 1.20.1 Forge Decocraft 원본 BBMODEL 31개를 Blockbench 5.2.2로 실제 열어 비교. 31개 시도 중 30개 정상 원본·텍스처 해시 및 실제 3D 렌더 인증, diner_counter_yellow 1개는 실패해 판단 증거 제외.",
 "조건부 후보 5건(091,093,096,098,100), 부적합/미검증 5건(092,094,095,097,099). 1:1 인증 0, 마크 인게임 설치·충돌·기능 인증 0. PZ 원본 PNG/357 자동 결과/TMX/SQLite 변경 없음.",
 "## 개별 이미지 판정"
 ]
 for a in review:
  lines.append("- **%03d %s / %s** → %s | %s. %s"%(a["index"],a["pz_name"],a["pz_style"],
   a["new_candidate_id"] or "정확한 후보 미발견",a["review_status"],a["manual_review_reason"]))
 lines.extend([
 "## 새로운 후보 및 추가 검증 조건",
 "100 Picnic Table: Decocraft 'picnic_table' 실제 22큐브 원본 Blockbench 모델에서는 완성된 상판과 양쪽 벤치+A형 프레임 확인. https://modrinth.com/mod/benched 공식 자료에도 Forge 1.20.1 호환 2×2 Bench가 있다고 명시됨. 현재 Benched 개별 자바 소스 모델은 이 패키지에서 아직 렌더링하지 않았고, Decocraft 모델의 2×2 실제 설치도 확인 전이다.",
 "091 Antique Television: Decocraft 'tv_old' 실제 30큐브 원목 TV+V 안테나+조절 노브+4다리. 이전 'crt_tv'는 플라스틱 검정 모니터라 정확하지 않다.",
 "093 Fancy Bed: Decocraft 'single_bed_black_white'는 1인용 검정 슬랫 프레임과 흰 침구가 맞지만 MC 체크 이불과 돌출 베개는 PZ와 다르다.",
 "096 Mirror and Drawers: Decocraft 'vanity_left_birch' 원본 모델은 거울+2단 서랍 일체형, PZ는 거울+3단 각 2개 손잡이여서 조건부; 단순 거울이나 서랍장만 설치하는 대안은 최종 승인하지 않는다.",
 "098 Chrome Toaster: Decocraft 'toaster_silver' 진짜 14큐브 모형에서 은색 둥근 корпус과 두 슬롯 확인; 카운터 위 설치 및 사용 기능 미검증.",
 "092 Generic Shop Counter: 기존 Macaw Counter는 큰 어두운 원통처럼 보이고 Decocraft 'bottom_cabinet_1_birch'는 흰 상판·서랍/문이 있어서 빈 판넬과 같은 계열 상판을 가진 PZ와 불일치. 실패한 diner_counter_yellow는 정상 렌더 수에 포함하지 않음.",
 "094/095 나무 원형 삼발이: Decocraft 카페 금속 다리/뱀부 라탄 장식과 재질·지지 구조 차이가 커서 보류.",
 "097 흰색 낮은 테이블: 기존 Decocraft 협탁은 서랍장, 새 White Wooden Table은 식탁 높이와 장식 다리로 높이 차이.",
 "099 오렌지 목재 4다리 의자: 새 Cherry Chair는 분홍색 여러 세로살, Orange School Chair는 플라스틱/금속이라 원본의 단순 가로대+오렌지 원목 구조 부적합.",
 "## 진행 현황 및 파일",
 "총 36묶음 중 10개(001~100) 총 100/357개 원본 가구 스타일 개별 검수 완료. 26묶음 QUEUED. 다음 101~110.",
 "- INDEX.html 및 cards/: PZ 완성 가구 이미지·원본 Blockbench 모델 좌우 비교 10개",
 "- BATCH_091_100_MANUAL_VISUAL_REVIEW.csv: 원본 타일/기존 후보/신규 렌더 후보/소스 해시/형태·크기·작동 판정",
 "- BATCH_091_100_DEFERRED_OTHER_MODS.csv: 5건 후속 다른 모드/바닐라 검색 목록",
 "- BATCHES_ALL_357_PROGRESS.csv: 누적 36묶음 작업 현황",
 "- ten_batch_review/10_091_100/extra_decocraft_render/: 전체 시도 31개 중 source-backed native Blockbench 30개 검증, 실패 1개.",
 "- 게임 실제 설치 및 인게임 화면 캡처가 아니라 원본 BBMODEL을 Blockbench로 열어 렌더링한 자료. 모드 JAR 원본 파일 자체는 재배포하지 않는다."
 ])
 (OUT/"README_KO.md").write_text("\n\n".join(lines)+"\n",encoding="utf8")
 name="ROSEWOOD_BATCH_091_100_MANUAL_REVIEW.zip"
 with zipfile.ZipFile(OUT/name,"w",zipfile.ZIP_DEFLATED,compresslevel=4) as z:
  for p in OUT.rglob("*"):
   if p.is_file() and p.name!=name:z.write(p,p.relative_to(OUT))
 with zipfile.ZipFile(OUT/name) as z:
  assert z.testzip() is None
  assert "INDEX.html" in z.namelist()
 print("BATCH10_VALIDATED",json.dumps(manifest,ensure_ascii=False),flush=True)
if __name__=="__main__":main()
