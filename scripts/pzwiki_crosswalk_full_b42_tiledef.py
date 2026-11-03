#!/usr/bin/env python3
"""Join PZwiki image filename sprite IDs to ALL B42 v259 TileDef source slots.
This complements the Rosewood USED-TILE crosswalk, not a game-object approval.
"""
import csv,json,sqlite3,collections,hashlib
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT/"analysis/rosewood_furniture/2026-10-31/furniture_pzwiki_crosswalk_20261103"
DB=ROOT/"analysis/current/v259/PZ_v259_all_png_tile_definitions.sqlite"
OUT=BASE/"global_tiledef"
def read(p):
 with p.open(encoding="utf-8-sig",newline="") as f:return list(csv.DictReader(f))
def write(p,rows):
 if not rows:raise ValueError("no rows "+str(p))
 with p.open("w",encoding="utf-8-sig",newline="") as f:
  w=csv.DictWriter(f,fieldnames=list(rows[0]),extrasaction="ignore")
  w.writeheader();w.writerows(rows)
def sorted_join(items):return "|".join(sorted(set(x for x in items if x)))
def main():
 assert DB.is_file() and not OUT.exists()
 OUT.mkdir()
 wiki=read(BASE/"WIKI_TO_ROSEWOOD_ALL_1268.csv")
 assert len(wiki)==1268
 con=sqlite3.connect(f"file:{DB}?mode=ro",uri=True)
 con.row_factory=sqlite3.Row
 c=con.execute("PRAGMA integrity_check").fetchone()[0]
 assert c=="ok",c
 # Union all 7 preserved original .tiles sources; no priority override.
 originals=collections.defaultdict(set)
 for name,id,src in con.execute("SELECT name,local_id,source_file FROM source_slots"):
  originals[(str(name).casefold(),str(id))].add(src)
 assert len(originals)>=61000
 attrs=collections.defaultdict(lambda:collections.defaultdict(set))
 attrnames=("CustomName","GroupName","Facing","SpriteGridPos","CustomItem","IsoType","Material","MaterialType")
 for name,id,attr,val,file in con.execute("SELECT name,local_id,attribute,value,source_file FROM source_attributes"):
  if attr in attrnames and val:
   attrs[(str(name).casefold(),str(id))][attr].add(val)
 image=collections.defaultdict(list)
 for name,id,path,vis,status in con.execute("SELECT tileset,local_id,png_path,has_visible_pixels,link_status FROM image_cells WHERE tileset IS NOT NULL AND local_id IS NOT NULL"):
  image[(str(name).casefold(),str(id))].append((path,int(vis or 0),status))
 result=[];detail=[];states=collections.Counter()
 for w in wiki:
  original_keys=(w["위키_이미지_원본타일키"] or "").split("|")
  original_keys=[x for x in original_keys if x]
  parsed=[tuple(x.rsplit("/",1)) for x in original_keys if "/" in x]
  found=[x for x in parsed if x in originals]
  png_ids=[x for x in parsed if x in image]
  visible_ids=[x for x in parsed if any(record[1] for record in image.get(x,[]))]
  if not parsed:state="NO_WIKI_IMAGE_SPRITE_ID"
  elif len(found)==0:state="NO_ID_IN_FULL_B42_ORIGINAL_TILEDEF"
  elif len(found)<len(parsed):state="PARTIAL_IDS_IN_FULL_B42_ORIGINAL_TILEDEF"
  elif len(png_ids)<len(parsed):state="ALL_TILEDEF_IDS_NOT_ALL_LINKED_TO_PNG"
  else:state="ALL_IDS_IN_FULL_TILEDEF_AND_PNG_CELLS"
  values={field:set() for field in attrnames}
  for key in found:
   for field in attrnames:values[field].update(attrs[key].get(field,set()))
  multi_named=len(values["CustomName"])>1 or len(values["GroupName"])>1
  if multi_named:note="MULTIPLE_SOURCE_NAMES_IN_IMAGE_IDS_REVIEW"
  elif len(found)==0:note="NOT_IN_THIS_B42_TILEDEF_NOT_PROOF_FURNITURE_NONEXISTENT"
  else:note="SOURCE_ID_ONLY_NOT_3D_OBJECT_IDENTITY"
  item=dict(w)
  item.update(full_tiledef_status=state,
   full_tiledef_source_ids="|".join(k[0]+"/"+k[1] for k in found),
   full_original_source_files=sorted_join(src for k in found for src in originals[k]),
   full_png_cell_ids="|".join(k[0]+"/"+k[1] for k in png_ids),
   full_visible_png_ids="|".join(k[0]+"/"+k[1] for k in visible_ids),
   original_CustomName_values=sorted_join(values["CustomName"]),
   original_GroupName_values=sorted_join(values["GroupName"]),
   original_Facing_values=sorted_join(values["Facing"]),
   original_SpriteGridPos_values=sorted_join(values["SpriteGridPos"]),
   original_CustomItem_values=sorted_join(values["CustomItem"]),
   original_IsoType_values=sorted_join(values["IsoType"]),
   original_Material_values=sorted_join(values["Material"]),
   original_MaterialType_values=sorted_join(values["MaterialType"]),
   full_definition_name_conflict="YES" if multi_named else "NO",
   comparison_note=note,
   b42_game_object_identity_verified="NO")
  result.append(item);states[state]+=1
  for key in parsed:
   detail.append(dict(wiki_id=w["목록ID"],wiki_name=w["가구명_원문"],
    source_key=key[0]+"/"+key[1],source_slot_in_full_tiledef="YES" if key in originals else "NO",
    original_files=sorted_join(originals.get(key,set())),
    original_name=sorted_join(attrs[key].get("CustomName",set())),
    original_group=sorted_join(attrs[key].get("GroupName",set())),
    facing=sorted_join(attrs[key].get("Facing",set())),
    grid_pos=sorted_join(attrs[key].get("SpriteGridPos",set())),
    png_count=len(image.get(key,[])),
    visible_png_count=sum(bool(y[1]) for y in image.get(key,[]))))
 write(OUT/"WIKI_1268_GLOBAL_ORIGINAL_TILEDEF.csv",result)
 write(OUT/"WIKI_IMAGE_SPRITE_ORIGINAL_PROPERTIES.csv",detail)
 unmatched=[r for r in result if r["교차검증_상태"]=="NO_SOURCE_ID_IN_ROSEWOOD_USED_4248" and r["full_tiledef_status"].startswith(("ALL_","PARTIAL_"))]
 if unmatched:write(OUT/"WIKI_OUTSIDE_ROSEWOOD_BUT_IN_ORIGINAL_TILEDEF.csv",unmatched)
 absent=[r for r in result if r["full_tiledef_status"]=="NO_ID_IN_FULL_B42_ORIGINAL_TILEDEF"]
 if absent:write(OUT/"WIKI_IDS_NOT_FOUND_IN_FULL_TILEDEF.csv",absent)
 inconsistent=[r for r in result if r["full_definition_name_conflict"]=="YES"]
 if inconsistent:write(OUT/"MULTIPART_NAME_DISAGREEMENT.csv",inconsistent)
 global_only=collections.Counter(r["full_tiledef_status"] for r in result if r["교차검증_상태"]=="NO_SOURCE_ID_IN_ROSEWOOD_USED_4248")
 manifest=dict(wiki_rows=len(wiki),full_original_unique_keys=len(originals),
  original_database_integrity=c,original_database_sha256=hashlib.sha256(DB.read_bytes()).hexdigest(),
  source_full_original_tiles="analysis/current/v259/PZ_v259_all_png_tile_definitions.sqlite",
  all_wiki_rows_global_status_counts=dict(states),
  wiki_not_used_in_rosewood_by_global_status=dict(global_only),
  wiki_rows_not_used_in_rosewood_but_found_in_all_tiledefs=len(unmatched),
  global_source_sprite_records=len(detail),
  multipart_images_with_different_original_names=len(inconsistent),
  original_tiledef_attributes_preserved=True,
  3d_geometry_verified=0,game_object_identity_certified=0,original_rosewood_catalog_modified=False)
 (OUT/"MANIFEST.json").write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
 text=["# PZwiki 가구 전체 목록과 B42 전체 원본 TileDef 대조",
 "이 대조는 원래 로즈우드에 사용된 4,248개 타일만 분석한 표의 한계를 보완하는 작업이야.",
 "기존 v259 원본 7개 .tiles 정의의 모든 원본 타일 키와 실제 PNG 논리 셀 자료를 사용했어.",
 "## 실제 결과"]
 for k,n in sorted(states.items(),key=lambda x:-x[1]):text.append("- "+k+": "+str(n)+" 위키 행")
 text.extend(["로즈우드에서 사용되지 않은 위키 행 가운데 **"+str(len(unmatched))+"개**는 B42 전체 원본 정의에서 이미지 파일명의 일부/모든 타일 키를 확인했어. 사용되지 않았다고 해서 게임에 없는 가구가 아님.",
 "## 추가 자료",
 "- WIKI_1268_GLOBAL_ORIGINAL_TILEDEF.csv : 1,268개 원본 위키 행에 전체 TileDef 정의 연결 상태, 원본 이름, GroupName, Facing, SpriteGridPos, Material, IsoType 추가.",
 "- WIKI_IMAGE_SPRITE_ORIGINAL_PROPERTIES.csv : 한 장 위키 이미지에 여러 번호가 들어 있을 때 번호별 원본 정의를 분리해서 표시.",
 "- WIKI_OUTSIDE_ROSEWOOD_BUT_IN_ORIGINAL_TILEDEF.csv : 로즈우드 맵에는 등장하지 않았지만 B42 전체 원본에는 존재하는 이미지 ID.",
 "- WIKI_IDS_NOT_FOUND_IN_FULL_TILEDEF.csv : 현재 버전 타일 정의에서 일치하지 않는 위키 이미지 ID. 없는 가구라 단정하지 않음.",
 "- MULTIPART_NAME_DISAGREEMENT.csv : 같은 위키 이미지 여러 부품에서 원본 이름/그룹이 다른 검수 대상.",
 "## 판정 제한",
 "명칭/그룹이 동일하거나 타일 ID가 일치하는지 여부는 가구의 3D 형상·게임 Moveable 시스템·설치 기능을 보증하지 않아. 게임 버전 차이와 위키 원본 추출 누락 가능성을 보존하고, 어떠한 모델도 자동 병합하거나 원본을 덮어쓰지 않았어."])
 (OUT/"README_KO.md").write_text("\n\n".join(text)+"\n",encoding="utf8")
 print("PZWIKI_GLOBAL_SOURCE_JOIN_DONE",json.dumps(manifest,ensure_ascii=False),flush=True)
if __name__=="__main__":main()
