#!/usr/bin/env python3
"""Count geometrically assembled Rosewood furniture without counting parts as objects."""
import csv,gzip,json,re,zipfile
from pathlib import Path
from collections import Counter,defaultdict

D=Path(__file__).resolve().parents[1]/"analysis/rosewood_furniture/2026-10-31"
O=D/"assembled_count_v2"
TRANS={
"xy":lambda x,y:(x,y),"x-y":lambda x,y:(x,-y),
"-xy":lambda x,y:(-x,y),"-x-y":lambda x,y:(-x,-y),
"yx":lambda x,y:(y,x),"y-x":lambda x,y:(y,-x),
"-yx":lambda x,y:(-y,x),"-y-x":lambda x,y:(-y,-x)}
def read(name):
    with (D/name).open(encoding="utf-8-sig",newline="") as f:return list(csv.DictReader(f))
def xy(s):
    m=re.fullmatch(r"\s*(\d+)\s*,\s*(\d+)\s*",s or "")
    return tuple(map(int,m.groups())) if m else None
def write(name,fields,rows):
    with (O/name).open("w",encoding="utf-8-sig",newline="") as f:
        w=csv.writer(f);w.writerow(fields);w.writerows(rows)
def main():
    if O.exists() and any(O.iterdir()):raise ValueError("Do not overwrite prior audit")
    O.mkdir(parents=True,exist_ok=True)
    prior=read("MINECRAFT_MATCH_PRIORITY.csv")
    tiles=read("ALL_FURNITURE_TILE_IDS.csv")
    priority={(r["tile_set_name"],int(r["local_id"])):r["match_tier"] for r in prior}
    definition={(r["tile_set_name"],int(r["local_id"])):r for r in tiles}
    assert len(definition)==4248 and len(priority)==4248
    fam=defaultdict(list)
    for k,r in definition.items():
        pos=xy(r["SpriteGridPos"])
        if pos and r["CustomName"] and priority[k]=="FURNITURE_BLOCK_PRIORITY":
            fam[(r["tile_set_name"],r["CustomName"],r["GroupName"],r["Facing"])].append((k,pos))
    valid={}; partmap={};rejected=[]
    for family,parts in fam.items():
        xs=[q[0] for k,q in parts];ys=[q[1] for k,q in parts]
        positions=set(q for k,q in parts)
        area=(max(xs)-min(xs)+1)*(max(ys)-min(ys)+1)
        if len(parts)==len(positions)==area and 2<=area<=9:
            valid[family]=parts
            for k,pos in parts:partmap[k]=(family,pos)
        else:
            rejected.append((family,len(parts),len(positions),area))
    placements=[];rawcounts=Counter()
    with gzip.open(D/"FURNITURE_PLACEMENTS.csv.gz","rt",encoding="utf-8-sig",newline="") as f:
        for r in csv.DictReader(f):
            k=(r["tileset"],int(r["local_id"]))
            tier=priority.get(k,"UNCLASSIFIED")
            rawcounts[(r["zone"],tier)]+=1
            if tier!="FURNITURE_BLOCK_PRIORITY":continue
            p=dict(index=len(placements),zone=r["zone"],tmx=r["tmx"],layer=r["layer"],
                z=int(r["z"]),x=int(r["world_x"]),y=int(r["world_y"]),key=k,
                room=r["room_bbox_name"],category=r["category"],name=r["CustomName"])
            placements.append(p)
    assert sum(rawcounts.values())==94073 and len(placements)==25212
    family_items=defaultdict(list)
    for p in placements:
        if p["key"] in partmap:family_items[partmap[p["key"]][0]].append((p,partmap[p["key"]][1]))
    def match(items,n,transform):
        func=TRANS[transform];grp=defaultdict(list)
        for p,pos in items:
            dx,dy=func(*pos)
            k=(p["zone"],p["z"],p["x"]-dx,p["y"]-dy)
            grp[k].append((p,pos))
        out={}
        for anchor,parts in grp.items():
            if len(parts)!=n or len({pos for p,pos in parts})!=n:continue
            k=frozenset(p["index"] for p,pos in parts)
            if len(k)==n:out[k]=(anchor,parts)
        return out
    accepted=[];used=set();ambiguous=set();diagnostics=[]
    for family,parts in sorted(valid.items()):
        n=len(parts);items=family_items.get(family,[])
        options={k:match(items,n,k) for k in TRANS}
        sc={k:len(v) for k,v in options.items()}
        best=max(sc.values());besttrans=[k for k,v in sc.items() if v==best]
        common=set.intersection(*(set(options[k]) for k in besttrans)) if best else set()
        candidates=set.union(*(set(options[k]) for k in besttrans)) if best else set()
        ambiguous.update(*(ids for ids in candidates-common))
        for ids in sorted(common,key=lambda x:min(x)):
            if ids&used:continue
            anchor,parts_here=options[besttrans[0]][ids]
            used.update(ids)
            sample=parts_here[0][0]
            accepted.append(dict(
                instance_id="ROSEWOOD_MULTI_"+str(len(accepted)+1).zfill(7),
                zone=anchor[0],z=anchor[1],layer="|".join(sorted({p["layer"] for p,pos in parts_here})),
                anchor_x=min(p["x"] for p,pos in parts_here),
                anchor_y=min(p["y"] for p,pos in parts_here),
                tile_set_name=family[0],CustomName=family[1],
                GroupName=family[2],Facing=family[3],
                category=sample["category"],part_count=n,
                part_ids="|".join(str(p["key"][1]) for p,pos in sorted(parts_here,key=lambda t:t[1])),
                part_xy="|".join(str(p["x"])+":"+str(p["y"]) for p,pos in sorted(parts_here,key=lambda t:t[1])),
                source_tmx="|".join(sorted({p["tmx"] for p,pos in parts_here})),
                evidence="COMPLETE_GRID_SAME_LEVEL_CROSS_LAYER_ALLOWED",
                note="Geometry only; object fidelity not certified"
            ))
        diagnostics.append([*family,n,len(items),best,len(common),len(candidates-common),
                            "|".join(besttrans),json.dumps(sc,sort_keys=True)])
    assert len(used)==sum(i["part_count"] for i in accepted)
    states=[];counts=Counter();category=Counter()
    for p in placements:
        r=definition[p["key"]];pos=xy(r["SpriteGridPos"])
        if p["index"] in used:state="ASSEMBLED_COMPONENT"
        elif p["index"] in ambiguous:state="AMBIGUOUS_COMPONENT_MATCH"
        elif p["key"] in partmap:state="UNMATCHED_MULTIPART_COMPONENT"
        elif pos:state="SOURCE_GRID_TEMPLATE_NOT_SAFE_TO_ASSEMBLE"
        elif r["CustomName"]:state="NAMED_SINGLE_SPRITE_POSSIBLE_OBJECT"
        else:state="UNNAMED_SPRITE_UNRESOLVED"
        counts[(p["zone"],state)]+=1
        category[(p["zone"],p["category"],state)]+=1
        states.append([p["zone"],p["tmx"],p["z"],p["layer"],p["x"],p["y"],*p["key"],
                       r["CustomName"],r["GroupName"],r["Facing"],r["SpriteGridPos"],p["room"],state])
    for a in accepted:
        counts[(a["zone"],"ASSEMBLED_OBJECT_CANDIDATES")]+=1
        category[(a["zone"],a["category"],"ASSEMBLED_OBJECT_CANDIDATES")]+=1
    write("ASSEMBLED_MULTI_FURNITURE_INSTANCES.csv",list(accepted[0]) if accepted else ["instance_id"],
          [[a[k] for k in accepted[0]] for a in accepted] if accepted else [])
    write("ALL_PRIORITY_FURNITURE_PART_STATUSES.csv",
          ["zone","tmx","z","layer","x","y","tileset","local_id","CustomName","GroupName","Facing","SpriteGridPos","room","status"],states)
    write("ASSEMBLY_GEOMETRY_DIAGNOSTICS.csv",
          ["tileset","CustomName","GroupName","Facing","template_parts","observed_parts","best_transform_objects",
           "accepted_objects","ambiguous_object_candidates","optimal_transforms","transform_scores"],diagnostics)
    write("ZONE_ASSEMBLY_COUNTS.csv",["zone","status","count"],[[*k,v] for k,v in sorted(counts.items())])
    write("CATEGORY_ASSEMBLY_COUNTS.csv",["zone","category","status","count"],[[*k,v] for k,v in sorted(category.items())])
    write("SOURCE_TEMPLATE_EXCLUSIONS.csv",
          ["tileset","CustomName","GroupName","Facing","local_ids","unique_positions","rectangular_area"],
          [[*f,n,p,a] for f,n,p,a in rejected])
    report={"basis":"v259 original SpriteGridPos + actual Rosewood TMX placements",
        "scope":{"CORE":"TMX X30-33 Y43-48","BUFFER":"remainder TMX X28-34 Y42-49"},
        "source_total_candidate_sprite_parts":sum(rawcounts.values()),
        "priority_furniture_sprite_parts":len(placements),
        "source_full_multipart_template_families":len(valid),
        "source_excluded_template_families":len(rejected),
        "assembled_candidate_objects":len(accepted),
        "assembled_parts_consumed":len(used),
        "priority_tile_counts":{"CORE":sum(counts["CORE",s] for s in set(s for z,s in counts) if s!="ASSEMBLED_OBJECT_CANDIDATES"),
                                "BUFFER":sum(counts["BUFFER",s] for s in set(s for z,s in counts) if s!="ASSEMBLED_OBJECT_CANDIDATES")},
        "counts_by_zone":{z:{s:v for (zz,s),v in counts.items() if z==zz} for z in ["CORE","BUFFER"]},
        "by_category":[dict(zone=z,category=cat,status=s,count=n) for (z,cat,s),n in sorted(category.items())],
        "top_assembled_names":[[name,group,n] for (name,group),n in
             Counter((a["CustomName"],a["GroupName"]) for a in accepted).most_common(50)],
        "limitations":["Same level and source sprite position required; the different TMX layers are preserved for subsequent verification",
          "The original SpriteGridPos and observed XY must form an entire grid; 8 transform ties must agree on identical part IDs",
          "Does not certify every group as a whole movable object; source custom names may be shared",
          "Unmatched multipart parts are never counted as whole objects",
          "Named single-sprite placements are candidate objects, not certified whole objects",
          "Furniture-only priority subset excludes decoration, switches, rooftop utility, and special industries",
          "Core rectangle is a town proxy, buffer includes nearby non-Rosewood places"]}
    assert len(states)==len(placements)
    (O/"MANIFEST.json").write_text(json.dumps(report,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    doc=["# 로즈우드 다칸 가구 조립 기반 개수 검수","",
         "전수 타일 배치 94,073건을 가구 수라고 부르지 않는다. 건물 내 가구 우선분류 타일 25,212건을 대상으로 원본 SpriteGridPos 조립을 검토했다.",""]
    for z in ["CORE","BUFFER"]:
        c=report["counts_by_zone"][z]
        doc.extend(["## "+z,
           "- 가구 후보 타일 배치: "+str(report["priority_tile_counts"][z]),
           "- 원본 격자와 실제 좌표가 맞아 조립된 다칸 가구 후보: "+str(c.get("ASSEMBLED_OBJECT_CANDIDATES",0)),
           "- 그 가구에 사용된 부품 타일: "+str(c.get("ASSEMBLED_COMPONENT",0)),
           "- 이름이 있는 단일 스프라이트 배치 후보(독립 가구 인증 아님): "+str(c.get("NAMED_SINGLE_SPRITE_POSSIBLE_OBJECT",0)),
           "- 정체/조립 미확정 나머지 부품: "+str(sum(v for s,v in c.items() if s not in ("ASSEMBLED_OBJECT_CANDIDATES","ASSEMBLED_COMPONENT","NAMED_SINGLE_SPRITE_POSSIBLE_OBJECT"))),""])
    doc.extend(["원본 레이어·층과 격자 위치가 일치하는 완전 조립 패턴만 묶었다. 조립 실패 부품을 개별 가구라고 세지 않았다.",
                "이것은 높은 신뢰도의 조립 후보 집계이며, TBX 내부 마스크·완성 가구 경계·수납·실제 PNG 형상과의 최종 검수는 별개다.",
                "파일: ASSEMBLED_MULTI_FURNITURE_INSTANCES.csv (조립 후보 1행당 1개); ALL_PRIORITY_FURNITURE_PART_STATUSES.csv; CATEGORY_ASSEMBLY_COUNTS.csv; ASSEMBLY_GEOMETRY_DIAGNOSTICS.csv; SOURCE_TEMPLATE_EXCLUSIONS.csv; MANIFEST.json.",""])
    (O/"README_KO.md").write_text("\n".join(doc),encoding="utf-8")
    with zipfile.ZipFile(O/"ROSEWOOD_ASSEMBLY_COUNT.zip","w",zipfile.ZIP_DEFLATED,compresslevel=6) as z:
        for f in sorted(O.iterdir()):
            if f.name!="ROSEWOOD_ASSEMBLY_COUNT.zip":z.write(f,f.name)
    print(json.dumps(report,ensure_ascii=False,indent=2),flush=True)
if __name__=="__main__":
    main()
