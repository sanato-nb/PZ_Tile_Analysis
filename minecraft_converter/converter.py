#!/usr/bin/env python3
"""B42 TMX -> conservative Minecraft Java preview. No external pip dependencies.
World is a temporary 1.20.1 compatibility preview, NOT a verified final conversion.
Original map and v259 are read-only. Every nonzero source tile is preserved.
"""
import argparse, base64, bisect, collections, csv, gzip, hashlib, json, re, shutil, struct, zipfile, zlib
from pathlib import Path
import xml.etree.ElementTree as ET
from floor_stair_stage import audit_source_floors, audit_pzw_basements, BASE_FLOOR_Y, LEVEL_HEIGHT
from road_terrain_stage import collect_surface_overlays, write_world_road_resource_pack

SURFACE={
 "blends_natural_01":"minecraft:grass_block",
 "blends_street_01":"minecraft:gray_concrete",
 "floors_exterior_street_01":"minecraft:stone",
 "floors_interior_tilesandwood_01":"minecraft:oak_planks",
 "floors_interior_carpet_01":"minecraft:light_gray_wool",
}
# Tile-index mappings below were confirmed by inspecting the repository's
# original Tiles/2x/blends_natural_01.png, blends_street_01.png,
# and vegetation_farm_01.png, not inferred from tileset names.
def surface_block(key,family):
    ix=int(key.split("/")[-1])
    # Source tile PNG was examined for these exact IDs. Preview vanilla materials.
    if family=="floors_interior_tilesandwood_01":
        if ix==5:return "minecraft:polished_diorite"  # white checkered
        if ix==12:return "minecraft:smooth_sandstone"  # pale tiled
        if ix==41:return "minecraft:dark_oak_planks"
        if ix==42:return "minecraft:birch_planks"
        if ix==43:return "minecraft:spruce_planks"
        if ix==50:return "minecraft:oak_planks"
    if family=="floors_interior_carpet_01":
        if ix==2:return "minecraft:gray_wool"
        if ix==47:return "minecraft:brown_wool"
    if family=="blends_natural_01":
        if 16<=ix<=23:return "minecraft:grass_block"
        if 32<=ix<=39:return "minecraft:moss_block"  # darker green ground
        if 48<=ix<=55:return "minecraft:podzol"  # yellow/olive dry grass proxy
        if 64<=ix<=71:return "minecraft:coarse_dirt"  # exposed dark brown soil
        if 80<=ix<=87:return "minecraft:farmland[moisture=7]" # furrowed dirt
    if family=="blends_street_01":
        if 16<=ix<=23:return "minecraft:gravel"  # gravel/beige
        if 32<=ix<=39:return "minecraft:andesite" # gray paving
        if 48<=ix<=55:return "minecraft:smooth_sandstone" # beige paving
        if 64<=ix<=87:return "minecraft:gray_concrete" # asphalt
    return SURFACE.get(family,"minecraft:magenta_concrete")

def crop_kind(key):
    if not key.startswith("vegetation_farm_01/"):return None
    ix=int(key.split("/")[-1])
    if 0<=ix<=5:return "ripe_wheat"
    if 32<=ix<=39:return "dry_stalk"
    return None

# Floor material choices are proxies; original TMX sprite IDs remain in raw log.
def tag(name,t,data):
    raw=name.encode("utf-8")
    return bytes([t])+struct.pack(">H",len(raw))+raw+value(t,data)
def value(t,x):
    if t==1:return struct.pack(">b",int(x))
    if t==3:return struct.pack(">i",int(x))
    if t==4:return struct.pack(">q",int(x))
    if t==8:
        x=x.encode("utf-8")
        return struct.pack(">H",len(x))+x
    if t==10:return b"".join(tag(k,*v) for k,v in x.items())+b"\0"
    if t==9:
        sub,items=x
        return bytes([sub])+struct.pack(">i",len(items))+b"".join(value(sub,i) for i in items)
    if t==12:
        return struct.pack(">i",len(x))+b"".join(struct.pack(">Q",i&((1<<64)-1)) for i in x)
    raise ValueError("NBT kind "+str(t))
def root(x):return tag("",10,x)
def section_blocks(blocks):
    palette=sorted(set(blocks))
    if not palette:palette=["minecraft:air"]
    pal={name:i for i,name in enumerate(palette)}
    def entry(blockstate):
        if "[" not in blockstate:return {"Name":(8,blockstate)}
        block,properties=blockstate.rstrip("]").split("[",1)
        return {"Name":(8,block),
                "Properties":(10,{k:(8,v) for k,v in
                    (piece.split("=",1) for piece in properties.split(","))})}
    state={"palette":(9,(10,[entry(name) for name in palette]))}
    if len(palette)>1:
        bits=max(4,(len(palette)-1).bit_length())
        slots=64//bits
        longs=[]
        for start in range(0,4096,slots):
            n=0
            for offset in range(min(slots,4096-start)):
                n |= pal[blocks[start+offset]] << (offset*bits)
            longs.append(n)
        state["data"]=(12,longs)
    return state
def chunk(cx,cz,placed,data_version):
    syblocks={}
    for (x,y,z),name in placed.items():
        assert x//16==cx and z//16==cz and -64<=y<=319
        sy=y//16
        if sy not in syblocks:syblocks[sy]=["minecraft:air"]*4096
        syblocks[sy][(y%16)*256+(z%16)*16+x%16]=name
    sections=[]
    for sy in range(-4,20):
        blocks=syblocks.get(sy,["minecraft:air"]*4096)
        sections.append({
            "Y":(1,sy),"block_states":(10,section_blocks(blocks)),
            "biomes":(10,{"palette":(9,(8,["minecraft:plains"]))}),
        })
    return root({
        "DataVersion":(3,data_version),"xPos":(3,cx),"yPos":(3,-4),"zPos":(3,cz),
        "Status":(8,"minecraft:full"),"LastUpdate":(4,0),
        "InhabitedTime":(4,0),"isLightOn":(1,0),
        "sections":(9,(10,sections)),
        "block_entities":(9,(10,[])),
        "fluid_ticks":(9,(10,[])),
        "block_ticks":(9,(10,[])),
        "PostProcessing":(9,(9,[])),
        "structures":(10,{"starts":(10,{}),"References":(10,{})}),
    })
def region_merge(path,new):
    path.parent.mkdir(parents=True,exist_ok=True)
    existing={};times=bytes(4096)
    if path.exists():
        raw=path.read_bytes()
        if len(raw)<8192:raise ValueError("Corrupt region")
        times=raw[4096:8192]
        for slot in range(1024):
            ent=int.from_bytes(raw[4*slot:4*slot+4],"big")
            sector,number=ent>>8,ent&255
            if not sector or not number:continue
            at=sector*4096
            length=int.from_bytes(raw[at:at+4],"big")
            if length<1 or at+4+length>len(raw):raise ValueError("Bad region slot")
            existing[slot]=raw[at:at+4+length]
    for (cx,cz),nbt in new.items():
        rec=b"\x02"+zlib.compress(nbt,6)
        existing[(cx%32)+(cz%32)*32]=struct.pack(">I",len(rec))+rec
    header=bytearray(8192);header[4096:]=times
    buffer=bytearray(8192);sector=2
    for slot in sorted(existing):
        rec=existing[slot];count=(len(rec)+4095)//4096
        if count>255:raise ValueError("Chunk exceeds region sector capacity")
        header[4*slot:4*slot+4]=(sector*256+count).to_bytes(4,"big")
        buffer.extend(rec);buffer.extend(bytes(count*4096-len(rec)));sector+=count
    buffer[:8192]=header
    tmp=path.with_suffix(".mca.tmp")
    tmp.write_bytes(buffer);tmp.replace(path)

def level_dat(world,seed,spawn_x,spawn_z,data_version,level_name="PZ B42 31_46 PREVIEW"):
    flat={"type":(8,"minecraft:flat"),
          "settings":(10,{"biome":(8,"minecraft:plains"),"features":(1,0),"lakes":(1,0),
          "layers":(9,(10,[{"height":(3,1),"block":(8,"minecraft:air")}]))})}
    worldgen={"bonus_chest":(1,0),"generate_features":(1,0),"seed":(4,seed),
              "dimensions":(10,{"minecraft:overworld":(10,{
                   "type":(8,"minecraft:overworld"),"generator":(10,flat)})})}
    data={
       "DataVersion":(3,data_version),"version":(3,19133),
       "LevelName":(8,level_name),"GameType":(3,1),
       "hardcore":(1,0),"allowCommands":(1,1),"initialized":(1,1),
       "SpawnX":(3,spawn_x),"SpawnY":(3,65),"SpawnZ":(3,spawn_z),
       "Time":(4,6000),"DayTime":(4,6000),"raining":(1,0),
       "thundering":(1,0),"clearWeatherTime":(3,999999),
       "Difficulty":(1,1),"DifficultyLocked":(1,1),
       "WorldGenSettings":(10,worldgen),
       "DataPacks":(10,{"Enabled":(9,(8,["vanilla"])),"Disabled":(9,(8,[]))}),
       "GameRules":(10,{"doMobSpawning":(8,"false"),
         "doDaylightCycle":(8,"false"),"doWeatherCycle":(8,"false"),
         "doPatrolSpawning":(8,"false"),"doTraderSpawning":(8,"false"),
         "randomTickSpeed":(8,"0")}),
    }
    (world/"level.dat").write_bytes(gzip.compress(root({"Data":(10,data)}),mtime=0))
    (world/"session.lock").write_bytes(struct.pack(">q",0))

def load_v259(path):
    if path is None:return {"defs":{},"tiles":{},"candidates":{}}
    raw=path.read_text(encoding="utf-8")
    m=re.search(r'const FURNITURE_B64="([A-Za-z0-9+/=]+)";',raw)
    if not m:raise ValueError("Missing v259 candidate catalog")
    obj=json.loads(gzip.decompress(base64.b64decode(m.group(1))))
    if len(obj["defs"])!=10042 or len(obj["candidates"])!=2197:
        raise ValueError("Unexpected v259 catalog size")
    return obj

def original_origin(pzw,filename):
    r=ET.parse(pzw).getroot()
    origin=r.find(".//GenerateLots/worldOrigin")
    if r.get("cellFormat")!="native-256" or origin is None or origin.get("origin")!="0,0":
        raise ValueError("Global coordinate system must be independently verified")
    cells=[x for x in r.findall(".//cell") if Path(x.get("map","")).name==filename]
    if len(cells)!=1:raise ValueError("TMX must correspond to one PZW cell")
    x=int(cells[0].get("x"));z=int(cells[0].get("y"))
    return x*256,z*256,{"x":x,"y":z,"origin":"0,0","format":"native-256"}

def parse_tmx(path,gx,gz,catalog):
    raw=path.read_bytes()
    tree=ET.fromstring(raw)
    if (tree.get("width"),tree.get("height"),tree.get("orientation"))!=("256","256","levelisometric"):
        raise ValueError("Unsupported TMX dimensions/orientation")
    tilesets=sorted((int(n.get("firstgid")),n.get("name")) for n in tree.findall("tileset"))
    first=[x[0] for x in tilesets]
    records=[];layers=[];floor={};furniture=[];warnings=[]
    for layer in tree.iter("layer"):
        lvl=int(layer.get("level",layer.get("z","0")))
        name=layer.get("name","")
        data=layer.find("data")
        if data is None or data.get("encoding")!="csv":raise ValueError("Expected CSV layer")
        values=[int(n) for n in (data.text or "").replace("\r","").replace("\n","").split(",") if n.strip()]
        if len(values)!=65536:raise ValueError("Layer length invalid: "+name)
        used=0
        for i,rawgid in enumerate(values):
            gid=rawgid&0x1fffffff
            if not gid:continue
            ix=bisect.bisect_right(first,gid)-1
            if ix<0:raise ValueError("Unknown GID "+str(gid))
            family=tilesets[ix][1]
            key=family+"/"+str(gid-first[ix])
            lx,lz=i%256,i//256
            x,z=gx+lx,gz+lz
            ids=catalog["tiles"].get(key,[])
            prop=catalog["defs"].get(key,{})
            record={"x":x,"z":z,"local_x":lx,"local_y":lz,
                "level":lvl,"floor_y":64+4*lvl,"layer":name,
                "gid":gid,"flip":rawgid&~0x1fffffff,"source_key":key,
                "candidate_ids":ids,"tile_properties":prop}
            records.append(record);used+=1
            if lvl==0 and name=="Floor":
                if (lx,lz) in floor:raise ValueError("Duplicate floor cell")
                floor[lx,lz]=(key,family)
                if family not in SURFACE:
                    warnings.append({"severity":"warning","reason":"unverified_ground","x":x,"z":z,
                                      "level":lvl,"layer":name,"source_key":key})
            elif ids:
                # v259 candidates also include vegetation, outdoor installations and openings.
                # Furniture markers are restricted to known furniture/appliance tile families.
                # Every excluded source record remains in the lossless source archive.
                if family.startswith(("furniture_","appliances_","fixtures_counters_",
                                      "fixtures_bathroom_","fixtures_sinks_")):
                    furniture.append(record)
                    if len(ids)>1:
                        warnings.append({"severity":"warning","reason":"ambiguous_furniture",
                         "x":x,"z":z,"level":lvl,"layer":name,"source_key":key})
        layers.append({"name":name,"level":lvl,"nonzero":used})
    return raw,tilesets,records,layers,floor,furniture,warnings

def execute(args):
    out=args.output;out.mkdir(parents=True,exist_ok=True)
    gx,gz,cell=original_origin(args.pzw,args.tmx.name)
    catalog=load_v259(args.v259_html)
    raw,tilesets,records,layers,floor,furniture,warnings=parse_tmx(args.tmx,gx,gz,catalog)
    structures=audit_source_floors(records)
    basements=audit_pzw_basements(args.pzw,cell["x"],cell["y"],gx,gz)
    # Only source-confirmed floors become physical blocks. In this sample,
    # Levels 1–6 are roofs/ceiling/tower/tank pieces, NOT second stories.
    structure_audit={
       **structures["audit"],
       "level0_original_floor_count":len(floor),
       "basement_metadata_objects":basements,
       "basement_physical_floor_generated":0,
       "converted_stair_runs":0,
       "stair_action":"No fixture stair sprites or connected source-backed upper landing; build none",
       "unresolved_geometry":[
        "PZW basement zone is not a rendered underground TMX floor",
        "Upper-level ceiling/roof tiles do not authorize walkable floors",
        "Stairwell headroom requires a verified connected pair of floor levels",
       ],
    }
    (out/"floor_stair_audit.json").write_text(
        json.dumps(structure_audit,ensure_ascii=False,indent=2),encoding="utf-8")
    crop_points={}
    for rec in records:
        if rec["level"]!=0:continue
        kind=crop_kind(rec["source_key"])
        if kind is None:continue
        position=(rec["local_x"],rec["local_y"])
        if position in crop_points:
            raise ValueError("Overlapping crop at "+str(position))
        crop_points[position]=kind
    crop_counts=dict(collections.Counter(crop_points.values()))
    # Original Level-0 overlays and sprite-index evidence. Roof and upper-level
    # pieces never imply ground surfaces or low vegetation.
    road_decals, small_plants, terrain_source_audit = collect_surface_overlays(
        records, floor, surface_block)
    # Original PNG confirms vegetation_trees_01/8..11 are conifer sprites,
    # vegetation_foliage_01/8..14 are bushes.
    tree_records=[r for r in records if r["level"]==0 and
                  r["source_key"] in {f"vegetation_trees_01/{k}" for k in range(8,12)}]
    shrub_records=[r for r in records if r["level"]==0 and
                   r["source_key"] in {f"vegetation_foliage_01/{k}" for k in range(8,15)}]
    # No jumbo_tree_01 original PNG is available in this repository snapshot;
    # preserve these coordinates, but never guess their geometry.
    jumbo_records=[r for r in records if r["level"]==0 and
                   r["source_key"].startswith("jumbo_tree_01/")]
    with (out/"source_placements.jsonl.gz").open("wb") as fd:
        with gzip.GzipFile(fileobj=fd,mode="wb",mtime=0) as comp:
            for row in records:
                comp.write((json.dumps(row,ensure_ascii=False,separators=(",",":"))+"\n").encode("utf-8"))
    (out/"furniture_parts.json").write_text(json.dumps(furniture,ensure_ascii=False,indent=2),encoding="utf-8")
    with (out/"warnings.csv").open("w",encoding="utf-8-sig",newline="") as fd:
        fields=["severity","reason","x","z","level","layer","source_key"]
        writer=csv.DictWriter(fd,fieldnames=fields);writer.writeheader();writer.writerows(warnings)
    edges={n:[] for n in ["north","south","west","east"]}
    for (lx,lz),(key,fam) in floor.items():
        if lz==0:edges["north"].append({"offset":lx,"key":key})
        if lz==255:edges["south"].append({"offset":lx,"key":key})
        if lx==0:edges["west"].append({"offset":lz,"key":key})
        if lx==255:edges["east"].append({"offset":lz,"key":key})
    (out/"edges.json").write_text(json.dumps(edges,ensure_ascii=False,indent=2),encoding="utf-8")
    report={"source":args.tmx.name,"sha256":hashlib.sha256(raw).hexdigest(),
       "global_origin":{"x":gx,"z":gz},"cell":cell,
       "tileset_count":len(tilesets),"layers":layers,
       "placed_tiles":len(records),"floor_cells":len(floor),
       "furniture_source_parts":len(furniture),"warnings":len(warnings),
       "floor_stair_stage":{"confirmed_upper_lower_floor_positions":
          structures["audit"]["confirmed_upper_lower_floor_total"],
          "physical_stair_sprite_parts":len(structures["source_stair_parts"]),
          "pzw_basement_metadata_regions":len(basements)},
       "verified_crop_positions":crop_counts,
       "verified_small_tree_sprites":len(tree_records),
       "verified_shrub_sprites":len(shrub_records),
       "jumbo_tree_unrendered":len(jumbo_records),
       "preview_materials":SURFACE,
       "road_terrain_stage":{"source":terrain_source_audit},
       "limitations":["Preview floor families are not certified sprite-level identities",
          "Furniture model grouping not inferred from per-part matches",
          "Water, exact road-marking contours, multi-floor floors, stairs, unidentified jumbo trees and walls remain unverified",
          "World-local road texture pack is a top-down 1.20.1 preview; vanilla fallback blocks remain visible without it",
          "This is a disposable Java preview, not the final mod/loader version"]}
    if args.preview_world:
        # Java 1.20.1 disposable compatibility target ONLY. No final version selected.
        world=out/"31_46_preview_world"
        chunkmap=collections.defaultdict(dict)
        for (lx,lz),(key,family) in floor.items():
            x,z=gx+lx,gz+lz
            top=surface_block(key,family)
            crop=crop_points.get((lx,lz))
            if crop=="ripe_wheat":
                top="minecraft:farmland[moisture=7]"
            if crop=="dry_stalk":
                top="minecraft:coarse_dirt"
            for y,material in [(64,top),(63,"minecraft:dirt"),(62,"minecraft:dirt"),
              (61,"minecraft:stone"),(60,"minecraft:stone"),(59,"minecraft:stone"),
              (58,"minecraft:stone"),(57,"minecraft:stone")]:
                chunkmap[(x//16,z//16)][x,y,z]=material
            if crop=="ripe_wheat":
                chunkmap[(x//16,z//16)][x,65,z]="minecraft:wheat[age=7]"
            elif crop=="dry_stalk":
                chunkmap[(x//16,z//16)][x,65,z]="minecraft:dead_bush"
        additional_floor_blocks=0
        for (level,x,z),r in sorted(structures["floors"].items()):
            floor_y=BASE_FLOOR_Y+LEVEL_HEIGHT*level
            if not -64<=floor_y<=319:
                raise ValueError("Floor beyond Minecraft build height")
            blocks=chunkmap[(x//16,z//16)]
            if level<0:
                # Preserve the original underground space instead of filling
                # two dirt + five stone blocks through confirmed basement cells.
                for clear_y in range(floor_y+1,min(floor_y+4,64)):
                    blocks.pop((x,clear_y,z),None)
            if (x,floor_y,z) in blocks and blocks[(x,floor_y,z)]!= "minecraft:air":
                raise ValueError("Confirmed structural floors collide with existing blocks")
            blocks[(x,floor_y,z)]=surface_block(
                r["source_key"],r["source_key"].split("/")[0])
            additional_floor_blocks+=1
        # Road paint replaces ONLY the Level-0 ground Y=64 block, so the
        # roadway remains flush. World-local resources.zip paints thin lines
        # on dedicated unused vanilla block aliases.
        road_marked_blocks=0
        for (lx,lz),(block,source_key) in sorted(road_decals.items()):
            x,z=gx+lx,gz+lz
            chunkmap[(x//16,z//16)][x,64,z]=block
            road_marked_blocks+=1
        write_world_road_resource_pack(world)
        markers=0
        for item in furniture:
            if item["layer"]=="Floor" or len(item["candidate_ids"])!=1:continue
            x,z,y=item["x"],item["z"],item["floor_y"]+1
            if not (-64<=y<=319):continue
            solid=str(item["tile_properties"].get("solid","")).lower()
            marker="minecraft:light_blue_carpet" if solid in ("false","0","no") else "minecraft:light_blue_stained_glass"
            blocks=chunkmap[(x//16,z//16)]
            if (x,y,z) not in blocks:blocks[(x,y,z)]=marker;markers+=1
        tree_trunks=0
        tree_leaves=0
        bush_blocks=0
        tree_conflicts=0
        leaf_clipped=0
        valid_tree_locations={}
        for item in tree_records:
            lx,lz=item["local_x"],item["local_y"]
            location=(lx,lz)
            base=floor.get(location)
            if base is None or base[1]!="blends_natural_01" or location in crop_points:
                tree_conflicts+=1
                continue
            x,z=item["x"],item["z"]
            if (x,65,z) in chunkmap[(x//16,z//16)]:
                tree_conflicts+=1
                continue
            sprite=int(item["source_key"].split("/")[-1])
            height=5 if sprite==10 else 7
            valid_tree_locations[location]=(height,x,z)
        # Write trunks first so leaves from neighboring trees cannot overwrite them.
        for (lx,lz),(height,x,z) in sorted(valid_tree_locations.items()):
            for j in range(height):
                p=(x,65+j,z)
                if p not in chunkmap[(x//16,z//16)]:
                    chunkmap[(x//16,z//16)][p]="minecraft:spruce_log"
                    tree_trunks+=1
        for (lx,lz),(height,x,z) in sorted(valid_tree_locations.items()):
            for y_offset in range(1,height+1):
                if y_offset==height:radius=0
                elif y_offset>=height-2:radius=1
                else:radius=2 if y_offset%2==0 else 1
                for dx in range(-radius,radius+1):
                    for dz in range(-radius,radius+1):
                        if radius and abs(dx)==radius and abs(dz)==radius:continue
                        tx,tz=x+dx,z+dz
                        txlocal,tzlocal=lx+dx,lz+dz
                        ground=floor.get((txlocal,tzlocal))
                        # Respect map boundary, roads, indoor floors and wheat fields.
                        if ground is None or ground[1]!="blends_natural_01" or (txlocal,tzlocal) in crop_points:
                            leaf_clipped+=1
                            continue
                        p=(tx,65+y_offset,tz)
                        chunk_blocks=chunkmap[(tx//16,tz//16)]
                        if p not in chunk_blocks:
                            chunk_blocks[p]="minecraft:spruce_leaves[persistent=true]"
                            tree_leaves+=1
        for item in shrub_records:
            lx,lz=item["local_x"],item["local_y"]
            ground=floor.get((lx,lz))
            if ground is None or ground[1]!="blends_natural_01" or (lx,lz) in crop_points:
                continue
            x,z=item["x"],item["z"]
            p=(x,65,z)
            blocks=chunkmap[(x//16,z//16)]
            if p not in blocks:
                blocks[p]="minecraft:oak_leaves[persistent=true]"
                bush_blocks+=1
        # Place source-backed low grasses only AFTER furniture/crops/trees/
        # bushes; occupied Y65 cells must never be overwritten.
        small_plant_counts=collections.Counter()
        small_plant_occupied=0
        for (lx,lz),(block,source_key,kind) in sorted(small_plants.items()):
            x,z=gx+lx,gz+lz
            dest=chunkmap[(x//16,z//16)]
            pos=(x,65,z)
            if pos in dest:
                small_plant_occupied+=1
                continue
            dest[pos]=block
            small_plant_counts[kind]+=1
        groups=collections.defaultdict(dict)
        for (cx,cz),blocks in sorted(chunkmap.items()):
            groups[(cx//32,cz//32)][cx,cz]=chunk(cx,cz,blocks,args.data_version)
        for (rx,rz),chunks in groups.items():
            region_merge(world/"region"/("r."+str(rx)+"."+str(rz)+".mca"),chunks)
        blocked={(x["local_x"],x["local_y"]) for x in furniture}
        blocked.update(crop_points)
        blocked.update(valid_tree_locations)
        blocked.update((r["local_x"],r["local_y"]) for r in shrub_records)
        walkable=[c for c in floor if c not in blocked]
        if not walkable:raise ValueError("Cannot find safe spawn")
        lx,lz=min(walkable,key=lambda p:(p[0]-128)**2+(p[1]-128)**2)
        level_dat(world,args.seed,gx+lx,gz+lz,args.data_version)
        archive=out/"31_46_preview_world.zip"
        with zipfile.ZipFile(archive,"w",zipfile.ZIP_DEFLATED) as zf:
            for path in sorted(world.rglob("*")):
                if path.is_file():zf.write(path,world.name+"/"+str(path.relative_to(world)))
        report.update({"world_archive":str(archive.name),"chunks":len(chunkmap),
                       "placeholder_parts":markers,
                       "confirmed_upper_lower_floor_blocks":additional_floor_blocks,
                       "source_stair_parts":len(structures["source_stair_parts"]),
                       "pzw_basement_regions":len(basements),
                       "crop_blocks":sum(crop_counts.values()),
                       "tree_trunk_blocks":tree_trunks,
                       "tree_leaves_blocks":tree_leaves,
                       "shrub_blocks":bush_blocks,
                       "road_marked_blocks":road_marked_blocks,
                       "low_vegetation_blocks":sum(small_plant_counts.values()),
                       "low_vegetation_counts":dict(sorted(small_plant_counts.items())),
                       "low_vegetation_skipped_occupied":small_plant_occupied,
                       "world_local_road_resource_pack":"resources.zip",
                       "tree_conflicts":tree_conflicts,
                       "clipped_leaves":leaf_clipped,
                       "data_version":args.data_version})
    terrain_world = {k:report.get(k) for k in (
        "road_marked_blocks","low_vegetation_blocks",
        "low_vegetation_counts","low_vegetation_skipped_occupied",
        "world_local_road_resource_pack") if k in report}
    (out/"road_terrain_audit.json").write_text(json.dumps({
        "source":args.tmx.name,
        "source_sha256":report["sha256"],
        "source_counters":terrain_source_audit,
        "world_preview":terrain_world,
        "notes":[
            "Original Level 0 TMX keys and PNG sprite shapes checked",
            "Top-down road paint is an approximation, not exact sprite projection",
            "Enable world-local resources.zip to see the road markings correctly",
            "Unmapped natural transitions, water, and 45 jumbo trees are deferred",
        ],
    },ensure_ascii=False,indent=2),encoding="utf-8")
    (out/"report.json").write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding="utf-8")
    print(json.dumps({k:v for k,v in report.items() if k in
        ("placed_tiles","floor_cells","warnings","chunks","placeholder_parts",
         "confirmed_upper_lower_floor_blocks","source_stair_parts","pzw_basement_regions",
         "crop_blocks","tree_trunk_blocks","shrub_blocks","world_archive")},indent=2))

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--tmx",type=Path,required=True)
    p.add_argument("--pzw",type=Path,required=True)
    p.add_argument("--v259-html",type=Path)
    p.add_argument("--output",type=Path,required=True)
    p.add_argument("--seed",type=int,default=310046)
    p.add_argument("--data-version",type=int,default=3465)
    p.add_argument("--preview-world",action="store_true")
    execute(p.parse_args())
if __name__=="__main__":main()
