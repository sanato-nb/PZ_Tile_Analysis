"""Source-conservative floor and stair planning for Zomboid → Minecraft.

No roof/ceiling tile may be silently promoted to a walkable upper floor.
No PZW 'Basement' zone may be treated as a physical basement room.
Only a source-verified 3-step run with a confirmed landing may be built.
"""
from collections import Counter, defaultdict
from pathlib import Path
import xml.etree.ElementTree as ET

LEVEL_HEIGHT=4
BASE_FLOOR_Y=64

def classify_floor(rec):
    """Return true ONLY when an original tile represents structural flooring."""
    key=rec["source_key"]
    family=key.split("/")[0]
    layer=rec["layer"]
    if rec["level"]==0:
        return layer=="Floor"
    if key.startswith(("ceilings_","roofs_","walls_exterior_roofs_",
                       "overlay_grime_floor_","floors_rugs_")):
        return False
    # A floor sheet directly identifies a walkable floor tile; a rug does not.
    if family.startswith(("floors_interior_","floors_exterior_")):
        return True
    if layer=="Floor" and family.startswith(("blends_natural_","blends_street_")):
        return True
    return False

def audit_source_floors(records):
    """Extract source-backed *upper/lower* floors without claiming roofs are floors."""
    confirmed={}
    source_stair_parts=[]
    nonfloor=Counter()
    level_layers=Counter()
    competing=[]
    for r in records:
        lev=r["level"]
        level_layers[(lev,r["layer"])]+=1
        family=r["source_key"].split("/")[0]
        if family=="fixtures_stairs_01" or family=="fixtures_escalators_01":
            source_stair_parts.append({
                "x":r["x"],"z":r["z"],"local_x":r["local_x"],
                "local_y":r["local_y"],"level":lev,"layer":r["layer"],
                "source_key":r["source_key"],
                "facing":r["tile_properties"].get("facing"),
                "sprite_grid_pos":r["tile_properties"].get("sprite_grid_pos")})
        if lev==0:continue
        if classify_floor(r):
            loc=(lev,r["x"],r["z"])
            if loc in confirmed and confirmed[loc]["source_key"]!=r["source_key"]:
                competing.append({"position":list(loc),
                    "keys":[confirmed[loc]["source_key"],r["source_key"]]})
            else:
                confirmed[loc]=r
        else:
            cat=("ceiling" if family.startswith("ceilings_") else
                 "roof" if family.startswith(("roofs_","walls_exterior_roofs_")) else
                 "other")
            nonfloor[(lev,cat)]+=1
    by_level=Counter(lev for lev,_,_ in confirmed)
    exclusions={}
    for (lev,cat),n in sorted(nonfloor.items()):
        exclusions.setdefault(str(lev),{})[cat]=n
    return {
        "floors":confirmed, "source_stair_parts":source_stair_parts,
        "competing_floors":competing,
        "audit":{
            "confirmed_nonzero_floor_tiles_by_level":{str(k):v for k,v in sorted(by_level.items())},
            "confirmed_upper_lower_floor_total":len(confirmed),
            "upper_tiles_by_family":dict(sorted(Counter(
                r["source_key"].split("/")[0] for r in confirmed.values()).items())),
            "nonfloor_tiles_by_level":exclusions,
            "stair_sprite_parts":len(source_stair_parts),
            "level0_base_floor_is_separate":True,
            "policy":"Structural floors only: never promote roofs, ceilings, grime, or rugs to upper floors."
        }
    }

def audit_pzw_basements(pzw_path, cell_x, cell_z, global_x, global_z):
    world=ET.parse(pzw_path).getroot()
    target=[c for c in world.findall(".//cell") if
            c.get("x")==str(cell_x) and c.get("y")==str(cell_z)]
    if len(target)!=1:
        raise ValueError("Expected exactly one PZW cell matching TMX")
    basements=[]
    for obj in target[0].findall("object"):
        if obj.get("group")!="Basement":continue
        props={p.get("name"):p.get("value") for p in obj.findall("./property")}
        lx,lz=int(obj.get("x")),int(obj.get("y"))
        stair_dx=int(props["StairX"]) if "StairX" in props else None
        stair_dz=int(props["StairY"]) if "StairY" in props else None
        basements.append({
            "local_rect":{"x":lx,"z":lz,"width":int(obj.get("width","0")),
                          "depth":int(obj.get("height","0"))},
            "world_rect":{"x":global_x+lx,"z":global_z+lz,
                          "width":int(obj.get("width","0")),
                          "depth":int(obj.get("height","0"))},
            "stair_hint_global":({
                "x":global_x+lx+stair_dx,"z":global_z+lz+stair_dz,
                "direction":props.get("StairDirection"),
                "access":props.get("Access")
            } if stair_dx is not None and stair_dz is not None else None),
            "source_properties":props,
            "status":"metadata_only_no_negative_tmx_floor",
            "is_verified_physical_basement":False,
        })
    return basements

DIRECTION={"N":(0,-1),"S":(0,1),"W":(-1,0),"E":(1,0)}
def plan_three_step_run(floor_positions,part_positions,level,x,z,direction):
    """Validate a confirmed 3-original-tile stair plus 1 confirmed landing.

    floor_positions: set[(level, x, z)] of source-confirmed walkable flooring.
    part_positions: set[(level, x, z)] of source-confirmed stair tile pieces.
    Never call with invented source coordinates for a production map.
    """
    if direction not in DIRECTION:raise ValueError("Unknown stair direction")
    dx,dz=DIRECTION[direction]
    parts=[(level,x+dx*i,z+dz*i) for i in range(3)]
    landing=(level+1,x+dx*3,z+dz*3)
    if not all(p in part_positions for p in parts):
        raise ValueError("Original TMX does not confirm all three stair pieces")
    if landing not in floor_positions:
        raise ValueError("No confirmed upper floor landing")
    if any((level+1,sx,sz) in floor_positions for _,sx,sz in parts):
        raise ValueError("Confirmed upper flooring conflicts with stairwell opening")
    y=BASE_FLOOR_Y+LEVEL_HEIGHT*level
    return {"level":level,"direction":direction,
            "start":{"x":x,"y":y,"z":z},
            "parts":[{"x":sx,"y":y+1+i,"z":sz} for i,(_,sx,sz) in enumerate(parts)],
            "landing":{"x":landing[1],"y":y+4,"z":landing[2]},
            "vertical_difference":4,"source_confirmed":True,
            "walkability":"geometry_prechecked_gameplay_not_verified"}

def write_stair_run(blocks,plan,material="minecraft:oak"):
    """Write solid supports and three vanilla stair blocks into one global-block map.

    An explicit landing floor must already exist. No other structures are erased.
    """
    facing=plan["direction"].lower()
    p=plan["landing"]
    landing_key=(p["x"],p["y"],p["z"])
    if landing_key not in blocks or blocks[landing_key]=="minecraft:air":
        raise ValueError("Landing must be a real existing upper floor")
    placements={}
    for i,point in enumerate(plan["parts"]):
        x,y,z=point["x"],point["y"],point["z"]
        for support_y in range(y-i,y):
            pos=(x,support_y,z)
            if blocks.get(pos,"minecraft:air") not in ("minecraft:air",material+"_planks"):
                raise ValueError("Support collides with an existing block")
            placements[pos]=material+"_planks"
        key=(x,y,z)
        if blocks.get(key,"minecraft:air")!="minecraft:air":
            raise ValueError("Stair occupies a blocked coordinate")
        placements[key]=material+"_stairs[facing="+facing+",half=bottom,shape=straight,waterlogged=false]"
        # Vertical collision check against the two-height movement corridor.
        # Potential floor at Y+4 under the stairway must have been excluded.
        for head_y in (y+1,y+2):
            head=(x,head_y,z)
            if blocks.get(head,"minecraft:air")!="minecraft:air":
                raise ValueError("Insufficient headroom above stair")
    blocks.update(placements)
    return len(placements)
