#!/usr/bin/env python3
"""Build robust Rosewood furniture *object-instance* estimates.

Source is the already-verified 94,073 original TMX furniture/fixtures sprite
placements. Never count two-piece/four-piece furniture once per sprite.
Only a complete, unique SpriteGridPos footprint is certified as one assembled
template. Where metadata cannot prove an object, retain explicitly unresolved
sprite placements rather than pretending a complete object count.
"""
import csv,gzip,json,math,sqlite3,zipfile
from pathlib import Path
from collections import Counter,defaultdict

ROOT=Path(__file__).resolve().parents[1]
SRC=ROOT/"analysis/rosewood_furniture/2026-10-31"
OUT=SRC/"furniture_object_counts_v1"
GROUP_SOURCE=SRC/"FURNITURE_ASSEMBLY_TEMPLATE_CANDIDATES.csv"
PRIORITIES=SRC/"MINECRAFT_MATCH_PRIORITY.csv"
PLACEMENTS=SRC/"FURNITURE_PLACEMENTS.csv.gz"

# Original source name & group are evidence of family, not conclusive object ID.
CORE_TIERS={"FURNITURE_BLOCK_PRIORITY"}
SUPPLEMENT_TIERS={"INTERIOR_DECOR","INDOOR_LIGHT_FIXTURE","SWITCH_WALL_CONTROL"}
EXCLUDE_TIERS={"UTILITY_NOT_FURNITURE","OUTDOOR_LIGHT_INFRASTRUCTURE","ROOF_EQUIPMENT","SPORTS_FLOOR_SURFACE"}
# An explicit original object CustomName in special location/industry sheets can
# be an actual furnishing. Do NOT include mixed-use "Floor"/"Wall" etc.
FURNITURE_NAMES={
 "desk","table","chair","couch","sofa","bed","beds","shelves","shelf",
 "bookcase","locker","counter","cabinet","cupboard","wardrobe","dresser",
 "fridge","refrigerator","oven","microwave","television","computer","sink",
 "toilet","bath","bathtub","shower","bench","stool","nightstand","washing machine",
 "washer","dryer","filing cabinet","cash register","display case","vending machine",
 "washingmachine","coffeemachine","espresso machine","water cooler","pool table",
 "stove","freezer","bookshelf","furniture","drawers","drawercabinet","desk lamp"
}
SHAPES=[
 ("IDENTITY",1,0,0,1),("INVERT_Y",1,0,0,-1),
 ("INVERT_X",-1,0,0,1),("ROTATE_180",-1,0,0,-1),
 ("SWAP_XY",0,1,1,0),("ROTATE_90",0,-1,1,0),
 ("ROTATE_270",0,1,-1,0),("SWAP_NEG",-0,-1,-1,0)
]

def table(path):
    with path.open("r",encoding="utf-8-sig",newline="") as f:
        return list(csv.DictReader(f))

def save_csv(path,fields,rows):
    with path.open("w",encoding="utf-8-sig",newline="") as f:
        w=csv.DictWriter(f,fieldnames=fields,extrasaction="ignore")
        w.writeheader();w.writerows(rows)

def classify_scope(tier,custom):
    if tier in CORE_TIERS:return "CORE_FURNITURE"
    if tier in SUPPLEMENT_TIERS:return "DECOR_OR_FIXTURE"
    if tier in EXCLUDE_TIERS:return "NOT_FURNITURE"
    if tier=="SPECIAL_MANUAL_REVIEW":
        c=(custom or "").lower().strip()
        if c in FURNITURE_NAMES:
            return "NAMED_SPECIAL_FURNITURE"
        return "UNCLASSIFIED_SPECIAL"
    return "UNCLASSIFIED"

def reading():
    priorities={}
    for r in table(PRIORITIES):
        priorities[r["source_key"]]=r
    families={}
    for r in table(GROUP_SOURCE):
        # use name/group/facing/tileset to avoid merging distinct orientations
        key=(r["tile_set_name"],r["CustomName"],r["GroupName"],r["Facing"])
        if key in families:raise ValueError("Duplicated family "+str(key))
        parts=set(int(x) for x in r["used_local_ids"].split("|"))
        xy={}
        # position per local ID retrieved from priority metadata? only groupped
        # CSV only has a set of positions, so get exact per-ID from each placement.
        families[key]=dict(status=r["pattern_status"],expected=int(r["required_rectangle_positions"]),
             positions=int(r["grid_positions_present"]),keys=parts,raw=r)
    return priorities,families

def anchor(row,shape):
    _,a,b,c,d=shape
    px,py=row["gridpos"]
    wx,wy=row["x"],row["y"]
    return wx-a*px-b*py,wy-c*px-d*py

def assemble_family(rows,template):
    """Returns (chosen shape, unambiguous complete groups, leftover placement records, scores).

    Only an unambiguous family footprint, with no duplicate per anchor/position
    and full set of offsets, is counted. A best transform is selected, but a
    transform tie means orientation is not externally verified.
    """
    expected_positions=set(row["gridpos"] for row in rows)
    per_key_pos={}
    for r in rows:
        per_key_pos.setdefault(r["tile_key"],r["gridpos"])
        if per_key_pos[r["tile_key"]]!=r["gridpos"]:
            raise ValueError("Local ID contradicts source SpriteGridPos")
    # derive desired positions FROM SOURCE TILE IDs, not just placements. This
    # refuses counting a partially represented 2- or 4-part object as complete.
    expected_positions=set()
    for keyid in template["keys"]:
        if keyid not in per_key_pos:
            return None,[],rows,dict(reason="TEMPLATE_PART_NOT_SEEN_IN_PLACEMENTS")
        expected_positions.add(per_key_pos[keyid])
    if not expected_positions:
        return None,[],rows,dict(reason="NO_EXPECTED_POSITIONS")
    if template["status"]!="POSITION_COVERAGE_COMPLETE_ONE_ID_PER_POSITION":
        return None,[],rows,dict(reason="SOURCE_TEMPLATE_AMBIGUOUS",expected=len(expected_positions))
    if len(expected_positions)<2:
        return None,[],rows,dict(reason="ONE_POSITION_IN_TEMPLATE")
    all_shapes=[]
    for shape in SHAPES:
        clusters=defaultdict(list)
        for r in rows:
            x,y=anchor(r,shape)
            clusters[(r["z"],x,y)].append(r)
        accepted=[]
        for k,rr in clusters.items():
            ps=[r["gridpos"] for r in rr]
            # duplicates and extras indicate overlapping alternatives or
            # corrupted associations: never silently swallow them.
            if len(ps)==len(expected_positions) and set(ps)==expected_positions:
                accepted.append((k,rr))
        all_shapes.append((len(accepted),shape,accepted))
    all_shapes.sort(key=lambda x:-x[0])
    count,best,complete=all_shapes[0]
    tied=sum(sc==count for sc,_,_ in all_shapes)>1
    consumed=set(r["index"] for _,rr in complete for r in rr)
    leftovers=[r for r in rows if r["index"] not in consumed]
    return best,complete,leftovers,dict(
        complete=count,transform=best[0],transform_tied=tied,
        runnerup=all_shapes[1][0],expected_positions=len(expected_positions),
        source_expected=template["expected"],source_status=template["status"])

def main():
    if OUT.exists() and any(OUT.iterdir()):
        raise FileExistsError("Do not overwrite prior object count audit")
    OUT.mkdir(parents=True,exist_ok=True)
    pri,templates=reading()
    all_rows=[];famrows=defaultdict(list);single=[];unknown=[]
    # 94k GID records. Zone determined from each exact world coordinate.
    with gzip.open(PLACEMENTS,"rt",encoding="utf-8-sig",newline="") as f:
        for i,r in enumerate(csv.DictReader(f)):
            source_key=r["tileset"]+"/"+r["local_id"]
            p=pri.get(source_key)
            if p is None:raise ValueError("Missing prior source row "+source_key)
            field=(r.get("SpriteGridPos") or "").strip()
            pt=None
            if field:
                v=field.split(",")
                if len(v)==2:
                    try:pt=(int(v[0]),int(v[1]))
                    except ValueError:pass
            row=dict(index=i,source_key=source_key,tile_key=int(r["local_id"]),
                     tileset=r["tileset"],x=int(r["world_x"]),y=int(r["world_y"]),
                     z=int(r["z"]),layer=r["layer"],tmx=r["tmx"],zone=r["zone"],
                     room=r["room_bbox_name"],gridpos=pt,
                     name=r["CustomName"] or "",group=r["GroupName"] or "",
                     facing=r["Facing"] or "",category=r["category"],tier=p["match_tier"],
                     scope=classify_scope(p["match_tier"],r["CustomName"]))
            all_rows.append(row)
            if pt is None:unknown.append(row)
            else:famrows[(row["tileset"],row["name"],row["group"],row["facing"])].append(row)
    assert len(all_rows)==94073,len(all_rows)
    object_rows=[];unresolved=[];family_summary=[]
    def zone_of(loc):
        x,y=loc
        cellx,celly=x//256,y//256
        return "CORE" if 30<=cellx<=33 and 43<=celly<=48 else "BUFFER"
    def push_object(kind,rr,transform="",source_key=""):
        # One distinct object instance, whether single sprite or full multi-sprite.
        first=rr[0]
        x0=min(x["x"] for x in rr);y0=min(x["y"] for x in rr)
        z=first["z"]
        if any(x["z"]!=z for x in rr):raise AssertionError("mixed level")
        zone=zone_of((x0,y0))
        n=len(rr)
        kset=sorted(set(x["source_key"] for x in rr))
        layers=sorted(set(x["layer"] for x in rr))
        id_=len(object_rows)+1
        object_rows.append(dict(id=id_,zone=zone,world_x=x0,world_y=y0,z=z,
          x_extent=max(x["x"] for x in rr)-x0+1,y_extent=max(x["y"] for x in rr)-y0+1,
          tile_set=first["tileset"],CustomName=first["name"],GroupName=first["group"],
          facing=first["facing"],category=first["category"],tier=first["tier"],
          scope=first["scope"],kind=kind,sprite_part_count=n,
          transform=transform,source_tile_ids="|".join(kset),
          layers="|".join(layers),tmx=first["tmx"],room_bbox_hint=first["room"]))
    def unresolved_row(r,why):
        unresolved.append(dict(zone=r["zone"],source_key=r["source_key"],
          world_x=r["x"],world_y=r["y"],z=r["z"],layer=r["layer"],
          CustomName=r["name"],GroupName=r["group"],Facing=r["facing"],
          SpriteGridPos="" if r["gridpos"] is None else ",".join(map(str,r["gridpos"])),
          tier=r["tier"],scope=r["scope"],reason=why))
    for family,rows in sorted(famrows.items()):
        t=templates.get(family)
        if t is None:
            for r in rows:unresolved_row(r,"NO_TEMPLATE")
            family_summary.append(dict(tile_set=family[0],CustomName=family[1],
              GroupName=family[2],Facing=family[3],pattern="NO_TEMPLATE",
              transform="",complete_instances=0,orphan_parts=len(rows),source_parts=0,tied=""))
            continue
        shape,complete,leftovers,debug=assemble_family(rows,t)
        for (z,ax,ay),rr in complete:
            push_object("FULL_MULTI_SPRITE_GRID",rr,shape[0])
        for r in leftovers:unresolved_row(r,debug.get("reason","INCOMPLETE_OR_OVERLAPPED_GRID"))
        family_summary.append(dict(tile_set=family[0],CustomName=family[1],
          GroupName=family[2],Facing=family[3],pattern=t["status"],
          transform=debug.get("transform",""),complete_instances=len(complete),
          orphan_parts=len(leftovers),source_parts=len(t["keys"]),
          tied=str(debug.get("transform_tied",""))))
    # No SpriteGridPos: source cannot establish a multi-sprite footprint.
    # Count as provisional single-slot furniture only for scope CORE_FURNITURE,
    # other categories retain uncertainty. A one-slot graphic may be overlay.
    for r in unknown:
        if r["scope"] in ("CORE_FURNITURE","NAMED_SPECIAL_FURNITURE"):
            push_object("PROVISIONAL_NO_GRID_SINGLE", [r])
        else:
            unresolved_row(r,"NO_SPRITE_GRIDPOS_AND_NOT_PRIMARY_FURNITURE")
    if sum(x["sprite_part_count"] for x in object_rows)+len(unresolved)!=len(all_rows):
        raise AssertionError("Lost or duplicate sprite placements")
    objects=Counter();partCounts=Counter();examples=defaultdict(list)
    for obj in object_rows:
        key=(obj["zone"],obj["scope"],obj["kind"],obj["category"])
        objects[key]+=1
        partCounts[(obj["zone"],obj["scope"],obj["kind"])]+=obj["sprite_part_count"]
        if len(examples[(obj["scope"],obj["category"])])<6:
            examples[(obj["scope"],obj["category"])].append(dict(
                type=obj["CustomName"],group=obj["GroupName"],source=obj["source_tile_ids"],
                z=obj["z"],pos=[obj["world_x"],obj["world_y"]],parts=obj["sprite_part_count"]))
    orphanCounts=Counter((r["zone"],r["scope"],r["reason"]) for r in unresolved)
    save_csv(OUT/"OBJECT_INSTANCES.csv",
       ["id","zone","world_x","world_y","z","x_extent","y_extent","tile_set",
        "CustomName","GroupName","facing","category","tier","scope","kind",
        "sprite_part_count","transform","source_tile_ids","layers","tmx","room_bbox_hint"],object_rows)
    save_csv(OUT/"UNRESOLVED_SPRITE_PARTS.csv",
       ["zone","source_key","world_x","world_y","z","layer","CustomName",
        "GroupName","Facing","SpriteGridPos","tier","scope","reason"],unresolved)
    save_csv(OUT/"GRID_TEMPLATE_ASSEMBLY_RESULTS.csv",
       ["tile_set","CustomName","GroupName","Facing","pattern","transform",
        "complete_instances","orphan_parts","source_parts","tied"],family_summary)
    counts=dict(
       total_sprite_placements=len(all_rows),
       reconstructed_full_multisprite_instances=sum(o["kind"]=="FULL_MULTI_SPRITE_GRID" for o in object_rows),
       provisional_single_sprite_instances=sum(o["kind"]=="PROVISIONAL_NO_GRID_SINGLE" for o in object_rows),
       unresolved_sprite_parts=len(unresolved),
       primary_furniture_objects=sum(o["scope"]=="CORE_FURNITURE" for o in object_rows),
       primary_full_multisprite_objects=sum(o["scope"]=="CORE_FURNITURE" and o["kind"]=="FULL_MULTI_SPRITE_GRID" for o in object_rows),
       primary_provisional_single_objects=sum(o["scope"]=="CORE_FURNITURE" and o["kind"]=="PROVISIONAL_NO_GRID_SINGLE" for o in object_rows),
       primary_unresolved_sprite_parts=sum(r["scope"]=="CORE_FURNITURE" for r in unresolved),
       core_primary_count=sum(o["zone"]=="CORE" and o["scope"]=="CORE_FURNITURE" for o in object_rows),
       buffer_primary_count=sum(o["zone"]=="BUFFER" and o["scope"]=="CORE_FURNITURE" for o in object_rows),
       named_special_furniture_objects=sum(o["scope"]=="NAMED_SPECIAL_FURNITURE" for o in object_rows),
       primary_plus_named_special_objects=sum(o["scope"] in ("CORE_FURNITURE","NAMED_SPECIAL_FURNITURE") for o in object_rows),
       decoration_and_fixture_objects=sum(o["scope"]=="DECOR_OR_FIXTURE" for o in object_rows),
       assembly_families=len(family_summary),
       assembly_complete_families=sum(x["complete_instances"]>0 for x in family_summary),
       transform_tie_families=sum(x["tied"]=="True" for x in family_summary),
       full_assembly_parts_consumed=sum(o["sprite_part_count"] for o in object_rows if o["kind"]=="FULL_MULTI_SPRITE_GRID"))
    report=dict(
      type="source-grounded object-instance count with explicit uncertainty",
      source_placements="analysis/rosewood_furniture/2026-10-31/FURNITURE_PLACEMENTS.csv.gz",
      input_rows=len(all_rows),
      counts=counts,
      objects_by_zone_scope_kind_category=[dict(zone=z,scope=s,kind=k,category=cat,objects=qty) for (z,s,k,cat),qty in objects.most_common()],
      unresolved_by_zone_scope_reason=[dict(zone=z,scope=s,reason=why,parts=qty) for (z,s,why),qty in orphanCounts.most_common()],
      examples={scope+' | '+cat: examples[(scope,cat)] for scope,cat in examples},
      known_limits=[
       "Counts are not an exact complete-game physical furniture inventory. Rectangular TMX cell survey is a Rosewood core proxy plus buffer.",
       "Source SpriteGridPos only yields an anchored coordinate candidate; best of eight transforms selected via complete support, which needs visual checks.",
       "PROVISIONAL_NO_GRID_SINGLE is one sprite placement treated provisionally as one object, NOT certified furniture instance.",
       "No automatic cross-family grouping of furniture parts without original source identity.",
       "Multi-grid templates with repeated position variants or incomplete coordinate groups are not counted as complete objects.",
       "Original RoomDefs rectangular room labels are not precise TBX mask geometry.",
       "Tilesets and original CustomName overlap with utility/floor/decor; excluded and unknown categories are separately preserved.",
       "No original TMX/PNG/previous analysis file modified."
      ])
    (OUT/"MANIFEST.json").write_text(json.dumps(report,ensure_ascii=False,indent=2,default=list)+"\n",encoding="utf-8")
    db=sqlite3.connect(OUT/"ROSEWOOD_FURNITURE_OBJECTS.sqlite")
    db.executescript("""CREATE TABLE objects(id INTEGER PRIMARY KEY,zone TEXT,x INTEGER,y INTEGER,z INTEGER,
      width INTEGER,height INTEGER,tileset TEXT,custom_name TEXT,group_name TEXT,facing TEXT,
      scope TEXT,category TEXT,kind TEXT,parts INTEGER,source_keys TEXT);
      CREATE INDEX ix_objects_scope_zone ON objects(scope,zone);
      CREATE INDEX ix_objects_named ON objects(custom_name,group_name);
      """)
    db.executemany("INSERT INTO objects VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
       [(o["id"],o["zone"],o["world_x"],o["world_y"],o["z"],o["x_extent"],
         o["y_extent"],o["tile_set"],o["CustomName"],o["GroupName"],o["facing"],
         o["scope"],o["category"],o["kind"],o["sprite_part_count"],o["source_tile_ids"]) for o in object_rows])
    db.commit();ck=db.execute("PRAGMA integrity_check").fetchone()[0]
    if ck!="ok":raise AssertionError(ck)
    assert db.execute("SELECT COUNT(*) FROM objects").fetchone()[0]==len(object_rows)
    db.close()
    with zipfile.ZipFile(OUT/"ROSEWOOD_OBJECT_COUNTS_COMPLETE.zip","w",zipfile.ZIP_DEFLATED,compresslevel=6) as z:
        for p in OUT.iterdir():
            if p.name.endswith((".csv",".json",".sqlite")):z.write(p,p.name)
    print(json.dumps(dict(counts=counts,types=report["objects_by_zone_scope_kind_category"][:25],
         unresolved=report["unresolved_by_zone_scope_reason"][:25],
         examples={str(k):v for k,v in list(examples.items())[:10]}),ensure_ascii=False,indent=2))
if __name__=="__main__":main()
