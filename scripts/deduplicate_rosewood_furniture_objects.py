#!/usr/bin/env python3
"""Rosewood furniture: strict duplicate instances vs repeatable models.

Original 2026-10-31 object reconstructions are source candidate counts.
Never remove distinct furniture just because it is the same style/model.
"""
import csv, json, sqlite3, zipfile
from pathlib import Path
from collections import defaultdict, Counter

ROOT=Path(__file__).resolve().parents[1]/"analysis/rosewood_furniture/2026-10-31"
SRC=ROOT/"furniture_object_counts_v1"/"OBJECT_INSTANCES.csv"
OUT=ROOT/"furniture_dedup_v1"
ALL_COLUMNS=["id","zone","world_x","world_y","z","x_extent","y_extent",
 "tile_set","CustomName","GroupName","facing","category","tier","scope",
 "kind","sprite_part_count","transform","source_tile_ids","layers","tmx","room_bbox_hint"]
PRIORITY_SCOPES=("CORE_FURNITURE","NAMED_SPECIAL_FURNITURE")
def cleaned(x):return " ".join(str(x or "").strip().split()).casefold()
def as_csv(path,fields,records):
    with path.open("w",encoding="utf-8-sig",newline="") as f:
        w=csv.DictWriter(f,fields,extrasaction="ignore")
        w.writeheader();w.writerows(records)
def is_furniture(row):return row["scope"] in PRIORITY_SCOPES
def coordkey(r):
    return (r["zone"],r["scope"],int(r["world_x"]),int(r["world_y"]),int(r["z"]))
def exactkey(r):
    # Includes assembly origin, exact model and source tile set, facing and size.
    # Deliberately ignores original layer because redundant export layers may
    # duplicate the same object. Does not conflate different adjacent chairs.
    return (coordkey(r),r["tile_set"],cleaned(r["CustomName"]),cleaned(r["GroupName"]),
      cleaned(r["facing"]),int(r["x_extent"]),int(r["y_extent"]),
      r["kind"],tuple(sorted((r["source_tile_ids"] or "").split("|"))))
def semantic_footprintkey(r):
    # Diagnostic only! Never automatically dedup different asset ids,
    # orientation, or assembly states at the same anchor.
    return (coordkey(r),r["tile_set"],cleaned(r["CustomName"]),cleaned(r["GroupName"]),
       int(r["x_extent"]),int(r["y_extent"]))
def modelkey(r):
    return (r["tile_set"],cleaned(r["CustomName"]),cleaned(r["GroupName"]),r["category"])
def unnamedkey(r):
    return (r["tile_set"],tuple(sorted((r["source_tile_ids"] or "").split("|"))),
        int(r["x_extent"]),int(r["y_extent"]))
def main():
    if OUT.exists() and any(OUT.iterdir()):
        raise FileExistsError(f"Never overwrite {OUT}")
    OUT.mkdir(parents=True,exist_ok=True)
    with SRC.open(encoding="utf-8-sig",newline="") as f:
        objects=list(csv.DictReader(f))
    if len(objects)!=24363: # 5302 + 19061
        raise ValueError("Unexpected original object source rows: "+str(len(objects)))
    assert all(set(ALL_COLUMNS)<=set(r) for r in objects)
    for r in objects:
        for k in ["world_x","world_y","z","x_extent","y_extent","sprite_part_count"]:
            r[k]=int(r[k])
    src_counts=Counter((r["zone"],r["scope"]) for r in objects)
    exact=defaultdict(list);foot=defaultdict(list);model=defaultdict(list)
    for r in objects:
        exact[exactkey(r)].append(r)
        foot[semantic_footprintkey(r)].append(r)
    keep=[];suppressed=[];groups=[]
    for k,records in exact.items():
        # Prefer record with non-empty room and source provenance but no
        # other transformation of the metadata.
        records.sort(key=lambda r:(not bool(r["room_bbox_hint"]),not bool(r["layers"]),int(r["id"])))
        canonical=records[0]
        keep.append(canonical)
        if len(records)>1:
            groups.append(dict(zone=canonical["zone"],scope=canonical["scope"],
                z=canonical["z"],x=canonical["world_x"],y=canonical["world_y"],
                tile_set=canonical["tile_set"],name=canonical["CustomName"],
                group=canonical["GroupName"],facing=canonical["facing"],
                canonical_id=canonical["id"],removed=len(records)-1,
                all_original_ids="|".join(r["id"] for r in records),
                all_layers="|".join(sorted({x for r in records for x in r["layers"].split("|") if x})),
                reason="EXACT_IDENTICAL_ORIGIN_AND_SOURCE_PART_SET"))
        for r in records[1:]:
            suppressed.append(dict(source_id=r["id"],canonical_id=canonical["id"],
                zone=r["zone"],scope=r["scope"],world_x=r["world_x"],world_y=r["world_y"],
                z=r["z"],name=r["CustomName"],group=r["GroupName"],
                reason="STRICT_EXACT_DUPLICATE"))
    # Separate diagnostic of model collisions that are NOT provable duplicates.
    conflicts=[]
    for k,rs in foot.items():
        uniq={exactkey(r) for r in rs}
        if len(uniq)<2:continue
        if not any(is_furniture(r) for r in rs):continue
        conflicts.append(dict(zone=rs[0]["zone"],scope=rs[0]["scope"],
            world_x=rs[0]["world_x"],world_y=rs[0]["world_y"],z=rs[0]["z"],
            tile_set=rs[0]["tile_set"],name=rs[0]["CustomName"],group=rs[0]["GroupName"],
            variants=len(uniq),source_ids="|".join(sorted({r["source_tile_ids"] for r in rs})),
            facing="|".join(sorted({r["facing"] for r in rs})),
            object_ids="|".join(r["id"] for r in rs),
            reason="SAME_ANCHOR_NAME_BUT_DIFFERENT_PARTS_OR_FACING;NOT_AUTO_REMOVED"))
    named_models=defaultdict(list);nameless=defaultdict(list);names=defaultdict(list)
    for r in keep:
        if not is_furniture(r):continue
        if r["CustomName"].strip():
            named_models[(r["zone"],r["scope"],*modelkey(r))].append(r)
            names[(r["zone"],r["scope"],cleaned(r["CustomName"]))].append(r)
        else:
            nameless[(r["zone"],r["scope"],*unnamedkey(r))].append(r)
    modelrows=[]
    for k,rs in named_models.items():
        zone,scope,tile_set,name,group,category=k
        a=rs[0]
        modelrows.append(dict(zone=zone,scope=scope,tileset=tile_set,CustomName=a["CustomName"],
           GroupName=a["GroupName"],category=category,placed_objects=len(rs),
           multipart_objects=sum(x["kind"]=="FULL_MULTI_SPRITE_GRID" for x in rs),
           one_sprite_provisional=sum(x["kind"]=="PROVISIONAL_NO_GRID_SINGLE" for x in rs),
           facing_variants="|".join(sorted({x["facing"] for x in rs if x["facing"]})),
           sample_source_ids="|".join(sorted({x["source_tile_ids"] for x in rs})[:5])))
    modelrows.sort(key=lambda x:(x["zone"],x["scope"],-x["placed_objects"],x["CustomName"],x["GroupName"]))
    namelessrows=[]
    for k,rs in nameless.items():
        zone,scope,tile_set,parts,w,h=k
        namelessrows.append(dict(zone=zone,scope=scope,tile_set=tile_set,
            source_tile_ids="|".join(parts),width=w,height=h,
            placed_sprite_objects=len(rs),
            note="UNKNOWN_MODEL: source name absent, asset-ID groups are not validated models"))
    namelessrows.sort(key=lambda x:(x["zone"],x["scope"],-x["placed_sprite_objects"]))
    zonestats=[]
    for zone in ["CORE","BUFFER"]:
        scopes=["CORE_FURNITURE","NAMED_SPECIAL_FURNITURE","DECOR_OR_FIXTURE","UNCLASSIFIED_SPECIAL","NOT_FURNITURE","UNCLASSIFIED"]
        for scope in scopes:
            orig=src_counts[zone,scope]
            records=[r for r in keep if r["zone"]==zone and r["scope"]==scope]
            if not orig and not records:continue
            named=[r for r in records if r["CustomName"].strip()]
            unnamed=[r for r in records if not r["CustomName"].strip()]
            known_model_keys={modelkey(r) for r in named}
            rows=dict(zone=zone,scope=scope,original_provisional_objects=orig,
              exact_duplicate_removed=orig-len(records),deduplicated_placed_object_candidates=len(records),
              deduplicated_multi_assembly_candidates=sum(r["kind"]=="FULL_MULTI_SPRITE_GRID" for r in records),
              deduplicated_single_sprite_provisional=sum(r["kind"]=="PROVISIONAL_NO_GRID_SINGLE" for r in records),
              deduplicated_named_object_candidates=len(named),
              deduplicated_unnamed_object_candidates=len(unnamed),
              distinct_named_model_keys=len(known_model_keys),
              distinct_named_furniture_names=len({cleaned(r["CustomName"]) for r in named}),
              unresolved_unnamed_asset_keys=len({unnamedkey(r) for r in unnamed}),
              model_collision_location_groups=sum(x["zone"]==zone and x["scope"]==scope for x in conflicts))
            zonestats.append(rows)
    as_csv(OUT/"OBJECT_INSTANCES_DEDUPLICATED.csv",ALL_COLUMNS,keep)
    as_csv(OUT/"REMOVED_EXACT_DUPLICATE_OBJECTS.csv",
        ["source_id","canonical_id","zone","scope","world_x","world_y","z","name","group","reason"],suppressed)
    as_csv(OUT/"EXACT_DUPLICATE_GROUPS.csv",
        ["zone","scope","z","x","y","tile_set","name","group","facing","canonical_id",
         "removed","all_original_ids","all_layers","reason"],groups)
    as_csv(OUT/"SAME_LOCATION_MODEL_CONFLICTS_FOR_REVIEW.csv",
        ["zone","scope","world_x","world_y","z","tile_set","name","group","variants",
         "source_ids","facing","object_ids","reason"],conflicts)
    as_csv(OUT/"DISTINCT_NAMED_MODELS.csv",
        ["zone","scope","tileset","CustomName","GroupName","category","placed_objects",
         "multipart_objects","one_sprite_provisional","facing_variants","sample_source_ids"],modelrows)
    as_csv(OUT/"UNNAMED_ASSET_KEYS_NOT_VALIDATED_MODELS.csv",
        ["zone","scope","tile_set","source_tile_ids","width","height","placed_sprite_objects","note"],namelessrows)
    as_csv(OUT/"DEDUP_COUNTS_BY_SCOPE_ZONE.csv",list(zonestats[0]),zonestats)
    m={
      "basis":"Existing reconstructed Rosewood OBJECT_INSTANCES from source-grounded original TMX, v259 SpriteGridPos. No original file changed.",
      "dedup_scope":"Exact same z/x/y, TMX zone, object scope, same tileset/name/group/facing, same footprint, same source part set; ignore drawing layer.",
      "non_dedup_policy":"Never remove instances in different positions or collapse different source asset sets and orientations even at same coordinate.",
      "original_object_instance_records":len(objects),
      "deduplicated_instance_records":len(keep),
      "exact_duplicate_removed":len(suppressed),
      "same_location_unproven_collision_groups":len(conflicts),
      "named_model_rows":len(modelrows),
      "unnamed_asset_rows":len(namelessrows),
      "counts_by_zone_scope":zonestats,
      "source_count_check":{str(k):v for k,v in sorted(src_counts.items())},
      "warnings":["15,957 center primary furniture figure is provisional, not a certified complete-object count.",
                  "Original unnamed tile elements are not a verified model category.",
                  "Model keys exclude Facing intentionally; orientation variants represent the same model.",
                  "Unique model keys are not unique object instances.",
                  "Same-position differing sprite part IDs are review conflicts, not proven duplicates.",
                  "Model style group can be empty; equal CustomName in different sheets might mean different design.",
                  "Original core zone is a rectangular TMX proxy; buffer contains prison/fringes."]
    }
    (OUT/"MANIFEST.json").write_text(json.dumps(m,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    # Indexed SQLite to access complete instance data and model aggregation.
    con=sqlite3.connect(OUT/"ROSEWOOD_DEDUP_OBJECTS.sqlite")
    con.execute("""CREATE TABLE objects (
        original_id INTEGER PRIMARY KEY, zone TEXT, scope TEXT, z INTEGER,
        world_x INTEGER, world_y INTEGER, tileset TEXT, custom_name TEXT, group_name TEXT,
        facing TEXT, category TEXT, object_kind TEXT, part_count INTEGER,
        source_tile_ids TEXT, source_layers TEXT
    )""")
    con.executemany("INSERT INTO objects VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",[
      (r["id"],r["zone"],r["scope"],r["z"],r["world_x"],r["world_y"],
       r["tile_set"],r["CustomName"],r["GroupName"],r["facing"],r["category"],r["kind"],
       r["sprite_part_count"],r["source_tile_ids"],r["layers"]) for r in keep])
    con.execute("CREATE INDEX idx_objects_zone_scope ON objects(zone,scope)")
    con.execute("CREATE INDEX idx_objects_position ON objects(zone,z,world_x,world_y)")
    con.commit();assert con.execute("PRAGMA integrity_check").fetchone()[0]=="ok";con.close()
    lines=[
    "# 로즈우드 가구 중복 제외 집계 (2026-10-31)",
    "",
    "중복에는 **동일 가구를 여러 타일로 나눴을 때의 부품 중복**과 **여러 레이어에 반복된 똑같은 완성 후보 기록**이 있다.",
    "첫 번째는 앞선 v1에서 이미 SpriteGridPos 기준 결합했고, 이번 분석은 두 번째 중복을 찾는다.",
    "",
    "## 위치별 객체 중복 제외",
    "| 지역 | 범위 | 기존 가구 후보 수 | 동일 위치·원본부품 정확 중복 제외 | 중복 제외 가구 후보 수 | 고유 이름 있는 모델 키 |",
    "|---|---|---:|---:|---:|---:|",
    ]
    for r in zonestats:
        if r["scope"] in PRIORITY_SCOPES:
            lines.append("| "+r["zone"]+" | "+r["scope"]+" | "+str(r["original_provisional_objects"])+
                " | "+str(r["exact_duplicate_removed"])+" | "+str(r["deduplicated_placed_object_candidates"])+
                " | "+str(r["distinct_named_model_keys"])+" |")
    lines +=["","## 중복 제외 규칙","",
       "- 동일 가구 모델이 서로 다른 집·좌표에 놓인 경우는 **각각 독립 가구**로 보존.",
       "- 동일 x/y/z이면서 같은 원본 타일셋·Local ID 부품 집합·이름/그룹·방향·크기·범주인 경우에만 확정 중복으로 하나만 보존.",
       "- 다중 부품 2~4칸 가구는 기존 조립 상태를 그대로 유지하고, 구성 타일을 다시 별도의 가구로 계산하지 않음.",
       "- 같은 위치라도 다른 타일 ID나 가구 방향이 붙으면 무조건 삭제하지 않고 SAME_LOCATION_MODEL_CONFLICTS_FOR_REVIEW.csv로 따로 보존.",
       "- 고유 종류는 이름+스타일(GroupName)+원본 타일셋으로 분류하며 E/S/W/N 방향만 다른 경우 모델 종류 수를 중복 계산하지 않음.",
       "- 원본 이름 없는 항목은 고유 물체 이름/모델을 확정하지 않고 별도 불확실 자산 키로 관리.",
       "",
       "## 원본과의 구분",
       "이 결과는 원본 격자와 위치 기반 자동 잠정 집계다. 별개 가구를 잘못 병합할 위험을 피하기 위해 의심 중복은 제거하지 않았다.",
       "배치된 가구의 개수와 서로 다른 가구 종류 수를 서로 혼용하지 말아야 한다.",
       "",
       "## 결과 파일",
       "- OBJECT_INSTANCES_DEDUPLICATED.csv — 중복 제거된 가구/비품 개별 위치 원장",
       "- DISTINCT_NAMED_MODELS.csv — 방향 변형을 합친 원본 이름+그룹별 모델/종류",
       "- DEDUP_COUNTS_BY_SCOPE_ZONE.csv — 구역/범위별 정량적 결과",
       "- SAME_LOCATION_MODEL_CONFLICTS_FOR_REVIEW.csv — 같은 좌표라도 근거 부족해 삭제하지 않은 충돌",
       "- REMOVED_EXACT_DUPLICATE_OBJECTS.csv — 실제 제거된 레코드와 원본 ID 대응",
       "- UNNAMED_ASSET_KEYS_NOT_VALIDATED_MODELS.csv — 이름없는 타일로 인한 종류 미확정",
       "- ROSEWOOD_DEDUP_OBJECTS.sqlite / ROSEWOOD_DEDUP_FURNITURE.zip — 조회용 데이터베이스와 전체 결과."
    ]
    (OUT/"README_KO.md").write_text("\n".join(lines)+"\n",encoding="utf-8")
    with zipfile.ZipFile(OUT/"ROSEWOOD_DEDUP_FURNITURE.zip","w",zipfile.ZIP_DEFLATED,compresslevel=6) as z:
        for path in OUT.iterdir():
            if path.name!="ROSEWOOD_DEDUP_FURNITURE.zip":z.write(path,path.name)
    print("DEDUP_RESULT",json.dumps(m,ensure_ascii=False),flush=True)

if __name__=="__main__":main()
