#!/usr/bin/env python3
"""Sixth group (051..060) manually checked against complete PZ assets and actual
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
N=B/"06_051_060/extra_decocraft_render"
N1=D/"blockbench_native_replacement_candidates_v1"
N2=B/"02_011_020/extra_decocraft_render"
OUT=B/"batch_051_060_v1"
DECISIONS=json.loads(r'''[{"i":51,"src":"new","model":"diner_table_round_black","candidate":"decocraft:diner_table_round_black","second":"decocraft:bamboo_coffee_table_round_yellow","status":"CONDITIONAL_ROUND_TRIPOD_MATERIAL_MISMATCH","shape":"Small brown circular wooden tabletop, single central dark wood pole, three/four-foot splayed pedestal base","size":"PZ 1×1; MC single base table source model; height and gameplay placement not verified","why":"PZ는 진갈색 목제 원형 상판+중앙 기둥과 갈라진 다리다. 실제 Decocraft Diner Table Round Black(21 cubes)은 원형/중앙 기둥/삼발이 구조가 비슷하지만 검정 상판·회색 금속 지지대여서 목재 재질은 불일치. Bamboo Round Yellow는 노란 4다리 격자라 하부형태가 더 멀다. 기존 Macaw 모델은 정사각 두꺼운 석판처럼 렌더되어 반려.","followup":"짙은 목재 원형 삼발이 식탁 찾기. 카페·빈티지 가구 모드 또는 목재 텍스처 변형 확인."},{"i":52,"src":"new","model":"cottage_coffee_table_long","candidate":"","second":"decocraft:cottage_coffee_table_long [rejected: too low and wooden legs]","status":"DEFER_LONG_TABLE_TWO_TILE_IRON_TRESTLES","shape":"Two-tile completed long light honey-wood high tabletop with thin black metal folding/trestle leg supports","size":"PZ 2×1, 2 original tiles; inspected source is low coffee table with placement dimensions unverified","why":"PZ는 길이 2칸 밝은 나무 높은 테이블, 철제 검정 접이식 가대형 다리이다. 새 Cottage Coffee Table Long은 단색 어두운 갈색이고 높이가 낮고 얇은 나무다리라 형태/재질/높이가 전부 달라 정답으로 승인하지 않는다. 기존 Decocraft Table Setting Double은 아예 접시·컵 세트였으므로 완전 반려.","followup":"2×1 나무 상판+철제 검정 다리의 학교/접이식 테이블 모드 검색. 바닐라 트랩도어/슬랩+철창은 실제 같은 칸 충돌/높이 검증 전까지 아이디어만."},{"i":53,"src":"new","model":"cottage_coffee_table","candidate":"decocraft:cottage_coffee_table","second":"decocraft:cottage_coffee_table_oval","status":"CONDITIONAL_LOW_DARK_WOOD_TABLE","shape":"Low dark red-brown small rectangular/square coffee table, beveled top and four elegant curved/slanted legs","size":"PZ 1×1; MC table nominal single model; tabletop height unknown","why":"PZ는 어두운 갈색 모서리 가공 상판과 바깥으로 휘는 네 다리가 있는 작은 낮은 탁자. 새 Cottage Coffee Table 실제 원본 33 cubes 모델은 목재 색감·낮은 상판·네 다리 형태가 유사해 기존 Macaw 회색 두꺼운 석판보다 낫다. 다만 원본은 더 작고 다리는 더 장식적이므로 정확한 일치가 아니다.","followup":"실제 1칸 크기·상판 높이·다리 각도/색상 비교 후 적용 여부 결정."},{"i":54,"src":"none","model":"","candidate":"","second":"Cardboard box mod (Forge 1.20.1), Shipping; concrete 3D model ID unverified","status":"DEFER_DENTED_TAPED_CARDBOARD_BOX","shape":"Small crushed uneven light-brown taped cardboard parcel, wrinkled flaps and torn upper opening","size":"PZ 1×1 small parcel; new cardboard mod nominal block footprint not verified","why":"PZ는 찌그러진 옅은 갈색 종이박스로, 테이프와 찢어지거나 구겨진 윗부분이 중요하다. 기존 Refurbished Mail Box는 불완전한 큰 목제 기둥 형태로 아예 종류가 틀리다. 실제 Decocraft 25개 후보 목록에는 닮은 종이상자가 없어서 우측에 없는 모델의 가상 렌더를 만들지 않는다. Forge 1.20.1 호환 Cardboard box 모드와 Shipping은 배포처 확인까지만 했다.","followup":"https://modrinth.com/mod/cardboard-box (Forge 1.20.1) 원본 JAR의 Cardboard Box/Sealed Box 모델 렌더링, 뚜껑/찌그러진 정도 확인. https://modrinth.com/mod/shipping 도 추가 검토."},{"i":55,"src":"new","model":"double_bed_oak_white","candidate":"decocraft:double_bed_oak_white","second":"minecraft:white_bed ×2 side by side [vanilla schematic, not proper joined double-bed]","status":"CONDITIONAL_FULL_WHITE_DOUBLE_BED_WITH_FOOTBOARD","shape":"Four-tile PZ completed 2×2 oak-framed double bed, cream-white single mattress, solid horizontal plank headboard, little or no footboard","size":"PZ original 2×2 four parts. MC double-bed model nominal custom footprint unknown; actual 2×2 placement not verified","why":"PZ 원본은 큰 연한 참나무 침대 틀에 연속된 흰 침구, 등받이는 넓은 수평 나무판, 발치에는 낮은 나무 프레임. Decocraft Oak White는 36 cubes로 정상 렌더되며 원목 프레임·흰 침구는 가까우나 흰 회색 체크 패턴, 분리된 베개, 세로살 머리판·발치 난간이 원본과 명확히 다르다. 기존 매칭은 조건부였으나 외형을 재평가해 조건부 유지.","followup":"MC 원본 JSON 블록 경계와 실제 게임 2×2 차지 여부 확인. Vanilla white bed 2개 나란히는 seam 발생하므로 동일 2×2로 인정 금지."},{"i":56,"src":"new","model":"stove","candidate":"decocraft:stove","second":"refurbished_furniture:light_stove [native import broken; not approved]","status":"STRONG_VISUAL_CONDITIONAL_FOUR_BURNER_OVEN","shape":"Freestanding gray-silver modern kitchen electric oven/stove with four circular black burners, four front knobs, black oven glass window, black rear backsplash","size":"PZ 1×1 freestanding stove; MC stove single model source, runtime recipes/hitbox untested","why":"PZ는 4개의 검은 둥근 화구·은회색 오븐 본체·전면 제어 노브·검정 오븐창·높은 검정 뒷판을 가진다. Decocraft Stove 실제 98큐브 모델은 4구 상판·노브·은회색 전면/검정 창을 모두 갖춰 기존 Paladin Gray Stove의 단일 막대 누락 모델보다 훨씬 정확하다. 다만 화구는 사각 격자, 검정 뒷판 생략, 손잡이/도어 높이 차이. 게임에서 요리 기능은 별도로 확인해야 한다.","followup":"추가 검증: PZ 스토브 후면 검정 뒷판, Decocraft 음식 조리 가능 여부, 1×1 배치, 오븐 문 방향."},{"i":57,"src":"new","model":"pedal_trash_can","candidate":"","second":"Skart's Decorations Wheelie Bins (Forge 1.20.1; mod presence confirmed but actual model unverified)","status":"DEFER_GREEN_WHEELED_WASTE_BIN","shape":"Tall dark green rectangular outdoor wheelie bin with hinged lid, rear push handle and two black wheels","size":"PZ 1×1 tall bin; Decocraft pedal bin 1-block model lacks wheels; alternate mod placement unverified","why":"PZ는 초록색 긴 본체, 상단 양쪽 덮개, 뒤쪽 손잡이와 밑바퀴 2개가 있는 이동식 쓰레기통. 기존 Refurbished recycle bin은 회색 일반 통으로 뚜껑/바퀴가 없고 부품도 불완전하다. 새 Decocraft Pedal Trash Can은 직육면체에 덮개는 있으나 회색이며 작은 바닥 페달뿐이어서 колес wheelie bin과 전혀 다름. Skart's Decorations 0.3 1.20.1 Forge에 Wheelie Bins 추가 이력이 있으나 모델 ID/초록 변형 실제 렌더 필요.","followup":"https://www.curseforge.com/minecraft/mc-mods/skarts-decorations/files/5112417 에 Wheelie Bins 존재. 1.20.1 JAR에서 색상별 모델/바퀴/손잡이/배치 렌더링."},{"i":58,"src":"new","model":"diner_chair_gray","candidate":"","second":"decocraft:school_chair_gray (not equivalent hand-hole)","status":"DEFER_GREY_MOLDED_PLASTIC_CHAIR","shape":"Grey/lilac one-piece molded plastic back and seat, oval/rounded handle cut-out in lower back, slender black curved metal four-leg frame","size":"PZ 1×1, low lightweight school-type chair; MC source model one block, geometry mismatch","why":"PZ는 한 몸체로 굽어진 회보라 플라스틱 좌석과 등받이, 가운데 손잡이 구멍, 검정 얇은 금속 다리. 새 Diner Chair Gray는 색상과 금속다리가 비슷하나 등받이가 납작한 사각판에 굵은 흰 줄무늬가 있고 구멍이 없다. School Chair Gray도 판형 등받이와 금속 직선다리라 동일한 성형 의자가 아니다. 기존 PFM Gray Arm Chair는 안락의자 블록 형태로 구조 불일치.","followup":"Forge 1.20.1 학교 의자/플라스틱 방문객 의자 모드에서 등받이 손잡이 구멍이 실제 모델에 있는지 확인. 바닐라 계단은 구멍/다리 부재로 비권장."},{"i":59,"src":"new","model":"piano_bench_spruce","candidate":"","second":"Just Outdoor Stuffs (1.20.1 Forge) two-player bench / Blockables Chairs bench with back (unverified actual model)","status":"DEFER_TWO_TILE_WOODEN_PARK_BENCH","shape":"PZ 1×2 or rotated 2×1 wooden outdoor park bench, 2 long horizontal slat backrails, two plank seat boards and brown bent metal legs, full two-tile assembly","size":"PZ 2 original tiles, 1×2 source orientation; MC bench must fit 2 adjacent tiles/seat two; exact placement not tested","why":"PZ는 목제 2줄 등받이+긴 이중 나무판 좌석+얇은 갈색 철제 받침다리로 구성되는 길쭉한 공원 벤치다. 기존 Decocraft Gym Bench는 헬스장 운동 기구였고 새 Piano Bench Spruce는 등받이도 없고 폭도 1칸인 피아노 의자라 둘 다 불합격. Just Outdoor Stuffs는 1.20.1 Forge 지원과 2인 벤치 기능까지 공식 소개에서 확인됐지만 실제 모델과 PZ처럼 2칸인지 아직 확인하지 않았다.","followup":"https://modrinth.com/project/6hCfRrRD (Forge 1.20.1)와 https://modrinth.com/mod/movables-chairs/ 의 bench with back 원본 모델/등받이/2칸 배치를 직접 검증."},{"i":60,"src":"new","model":"filing_cabinet_white","candidate":"","second":"decocraft:modular_desk_drawers_white [two drawers, source preview verified]","status":"DEFER_WHITE_WOODEN_THREE_DRAWER_DRESSER","shape":"Ivory painted wood chest of three drawers, each with two small round black knobs (six knobs total), thick top, slightly distressed plinth","size":"PZ 1×1 compact 3-drawer dresser; MC filing cabinet 1-block model, wrong use and handles","why":"PZ는 크림 흰색 목제 3단 서랍장이며 서랍마다 검정 동그란 손잡이 2개(총 6개). 새로운 Decocraft Filing Cabinet White는 실제 렌더에서 3단이긴 하나 흰 철제 문서 보관함으로 각 서랍마다 긴 금속 손잡이와 라벨 칸이 있다. Modular Desk Drawers White는 흰색 목제에 가깝지만 2단만 있어 둘 다 완성형으로는 맞지 않는다. 기존 Macaw BookShelf Drawer 렌더는 초록 판 한 장이라 무효.","followup":"Furnitury/Skniro/추가 Forge 1.20.1 가구 모드에서 3단 서랍+6개 검정 둥근 손잡이를 갖는 목제 dresser 모델 확인."}]''')
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
 d.text((25,574),"Source-backed render, not actual connected gameplay/size verification. Multipart sofa modules shown separately.",font=font(11),fill=(125,82,72))
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
 return ('''<!doctype html><html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Rosewood 10-batch group 03 051–060</title>
 <style>body{margin:0;background:#ecf1f5;color:#293f50;font:14px system-ui,'Malgun Gothic',sans-serif}
 header{position:sticky;top:0;background:white;border-bottom:1px solid #d1dce6;padding:18px 3%}
 h1{font-size:22px;margin:0 0 9px}main{display:grid;gap:18px;padding:19px 3%;grid-template-columns:repeat(auto-fit,minmax(min(100%,570px),1fr))}
 article{background:white;border:1px solid #d4dfe8;border-radius:12px;padding:12px}article img{width:100%;border-radius:8px}
 h2{font-size:17px}p{line-height:1.55;margin:7px 0}code{overflow-wrap:anywhere}
 pre{background:#f0f3f7;white-space:pre-wrap;overflow-wrap:anywhere;font-size:11px;padding:10px}
 </style></head><body><header><h1>좀보이드 가구 ↔ 마크 실제 가구 모델 — 4차 051~060</h1>
 <p>원본 좀보이드 완성 가구와 실제 Minecraft Decocraft 원본 모델을 Blockbench에서 직접 렌더해 10종을 하나씩 수동 검수함.
 모양이 틀린 오른쪽 이미지는 명확하게 거절 상태로 표시함. 2개 스프라이트로 된 욕조·탁자는 조립 및 크기 추가 검증.
 보류 항목은 신규 가구 모드나 바닐라 조합을 후속 검토하며, 자동 월드 적용 확정 0개.</p></header><main>%%%BODY%%%</main></body></html>''').replace("%%%BODY%%%","\n".join(block))
def main():
 assert not OUT.exists(),"Cannot overwrite past manual review"
 (OUT/"cards").mkdir(parents=True)
 original=rows(SOURCE/"ALL_357_FULL_RENDER_MATCHING.csv")
 assert len(original)==357
 assert [x["i"] for x in DECISIONS]==list(range(51,61))
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
 writecsv(OUT/"BATCH_051_060_MANUAL_VISUAL_REVIEW.csv",review)
 deferred=[x for x in review if x["review_status"].startswith("DEFER")]
 assert [x["index"] for x in deferred]==[52,54,57,58,59,60]
 writecsv(OUT/"BATCH_051_060_DEFERRED_OTHER_MODS.csv",deferred)
 groups=rows(B/"batch_041_050_v1/BATCHES_ALL_357_PROGRESS.csv")
 assert len(groups)==36
 assert [x["range"] for x in groups[:5]]==["001-010","011-020","021-030","031-040","041-050","051-060"]
 assert all(x["review_status"]=="COMPLETED_CONDITIONAL_CANDIDATES" for x in groups[:5])
 groups[5]["review_status"]="COMPLETED_CONDITIONAL_CANDIDATES"
 groups[5]["review_file"]="batch_051_060_v1/BATCH_051_060_MANUAL_VISUAL_REVIEW.csv"
 writecsv(OUT/"BATCHES_ALL_357_PROGRESS.csv",groups)
 (OUT/"INDEX.html").write_text(htmlpage(review),encoding="utf8")
 manifest={"scope":"051-060","total_pz_styles":357,"total_batches":36,
  "batches_reviewed":6,"batches_unreviewed":30,"individual_items_checked_this_batch":10,
  "unique_decocraft_models_rerendered":len(proofs[str(N)]),
  "native_model_pz_comparison_cards":len(review),
  "conditional_match_proposals":len(review)-len(deferred),
  "deferred_other_mod_or_vanilla_search":len(deferred),
  "exact_1_to_1_matches_certified":0,
  "minecraft_game_install_collision_verified":0,
  "source_tables_overwritten":False}
 (OUT/"MANIFEST.json").write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+"\n",encoding="utf8")
 lines=[
 "# 로즈우드 357종 — 6차 051~060번 완성 가구 수동 재검수",
 "이번 10건은 PZ 1~4개 스프라이트가 만드는 완성 가구를 확인한 뒤 Minecraft Decocraft 1.20.1 Forge의 원본 .bbmodel + PNG 후보 25종을 Blockbench 5.2.2에서 렌더링하여 판정함.",
 "조건부 대안 4개, 다른 모드/바닐라 후속 검토 6개. 동일 기능·형태 1:1 최종 인증 0. 기존 357 원자료, PZ PNG, SQLite/TMX는 변경하지 않음.",
 "## 개별 판정"
 ]
 for a in review:
  lines.append("- **%03d %s / %s** → %s | %s. %s"%(a["index"],a["pz_name"],a["pz_style"],
   a["new_candidate_id"] or "정확한 후보 미발견",a["review_status"],a["manual_review_reason"]))
 lines.extend([
 "## 외부 모드 검증 전까지 보류",
 "054 찌그러진 종이상자: Cardboard Box 1.20.1 Forge(https://modrinth.com/mod/cardboard-box), Shipping(https://modrinth.com/mod/shipping). 공식 배포 확인됐으나 모델 로드/찌그러진 외형 검증 전.",
 "057 초록색 바퀴 달린 쓰레기통: Skart's Decorations Wheelie Bins 1.20.1 Forge(https://www.curseforge.com/minecraft/mc-mods/skarts-decorations/files/5112417) 모델·녹색 변형 필요.",
 "059 등받이 있는 목재 2인 공원 벤치: Just Outdoor Stuffs 1.20.1 Forge(https://modrinth.com/project/6hCfRrRD) 및 Blockables Chairs bench with back (https://modrinth.com/mod/movables-chairs/) 후보 형태 검증 전.",
 "052 긴 2칸 금속다리 테이블, 058 손잡이 구멍 플라스틱 의자, 060 아이보리 3단 6개 손잡이 서랍장은 현 후보와 구조 차이가 커서 보류.",
 "바닐라 대안은 장식적 배치 가능성만 제안하고 실제 블록 설치/충돌·2칸 크기 검증 전에는 매칭 완료 처리하지 않음.",
 "## 진행",
 "전체 36묶음 중 6묶음(001~060) 개별 검수 / 총 60/357. 나머지 30묶음 QUEUED. 다음 구간은 061~070.",
 "## 파일",
 "- INDEX.html 및 cards/: 왼쪽 PZ 완성 가구와 오른쪽 원본 Minecraft 모델 또는 검증된 대체품 미발견 상태를 분리한 10종 비교 카드",
 "- BATCH_051_060_MANUAL_VISUAL_REVIEW.csv: 10건 개별 속성·기존 후보·새 후보·원본 모델 SHA-256·형태·크기·보류 이유",
 "- BATCH_051_060_DEFERRED_OTHER_MODS.csv: 후속 검색 6종",
 "- BATCHES_ALL_357_PROGRESS.csv: 누적 36묶음 진행 현황",
 "- 새로운 25개 원본 Blockbench 모델 렌더는 ten_batch_review/06_051_060/extra_decocraft_render/에 별도 저장."
 ])
 (OUT/"README_KO.md").write_text("\n\n".join(lines)+"\n",encoding="utf8")
 name="ROSEWOOD_BATCH_051_060_MANUAL_REVIEW.zip"
 with zipfile.ZipFile(OUT/name,"w",zipfile.ZIP_DEFLATED,compresslevel=4) as z:
  for p in OUT.rglob("*"):
   if p.is_file() and p.name!=name:z.write(p,p.relative_to(OUT))
 with zipfile.ZipFile(OUT/name) as z:
  assert z.testzip() is None
  assert "INDEX.html" in z.namelist()
 print("BATCH06_VALIDATED",json.dumps(manifest,ensure_ascii=False),flush=True)
if __name__=="__main__":main()
