#!/usr/bin/env python3
"""Extract every furniture or fixture candidate directly from Rosewood TMX GIDs."""
import bisect,csv,gzip,json,re,sqlite3,xml.etree.ElementTree as ET,zipfile
from pathlib import Path
from collections import defaultdict,Counter

ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT/"B4220.3_MapExport_256/tmx"
DB=ROOT/"analysis/current/v259/PZ_v259_all_png_tile_definitions.sqlite"
OLD=ROOT/"review/v255_latest_integrated_10042_2026-10-30/MASTER_ALL_10042_LATEST_PREFERRED.csv"
OUT=ROOT/"analysis/rosewood_furniture/2026-10-31"
FAMILY=[
 ("furniture_","가구","DIRECT"),("appliances_","가전","DIRECT"),
 ("fixtures_bathroom_","욕실설비","DIRECT"),("fixtures_sinks_","싱크대","DIRECT"),
 ("fixtures_counters_","카운터","DIRECT"),("fixtures_fireplaces_","벽난로","DIRECT"),
 ("fixtures_windows_curtains_","커튼","DIRECT"),("lighting_","조명","DIRECT"),
 ("trashcontainers_","쓰레기통","DIRECT"),("recreational_","오락용 가구","DIRECT"),
 ("rooftop_furniture","옥상 가구","DIRECT"),("vegetation_indoor_","실내용 화분","DIRECT"),
 ("walls_decoration_","벽 장식","DIRECT"),
 ("constructedobjects_","제작 물체","SPECIAL"),("carpentry_","목공 물체","SPECIAL"),
 ("crafting_","제작 설비","SPECIAL"),("camping_","캠핑 물품","SPECIAL"),
 ("security_","보안 설비","SPECIAL"),("industry_","산업 시설·설비","SPECIAL"),
 ("location_","특수 건물 비품","SPECIAL"),("street_decoration_","가로 시설","SPECIAL"),
 ("signs_","간판","SPECIAL"),("papernotices_","안내문","SPECIAL")
]
PRIORITY={"tiledefinitions_noiseworks.patch.tiles":50,"newtiledefinitions.tiles":40,
 "tiledefinitions_erosion.tiles":30,"tiledefinitions_overlays.tiles":20,
 "tiledefinitions_b42chunkcaching.tiles":15,"jumbo_trees_big.tiles":10,"jumbo_trees.tiles":10}

def classify(n):
    for pref,cat,mode in FAMILY:
        if n.startswith(pref):return cat,mode
    return "비가구·배경·구조","EXCLUDED"

def write_csv(path,header,rows):
    with path.open("w",encoding="utf-8-sig",newline="") as f:
        w=csv.writer(f);w.writerow(header);w.writerows(rows)

def metadata():
    c=sqlite3.connect("file:"+str(DB.resolve())+"?mode=ro",uri=True)
    vals=defaultdict(dict)
    best={}
    for name,local,attr,value,source in c.execute(
        "SELECT name,local_id,attribute,value,source_file FROM source_attributes"):
        k=(name,local,attr)
        score=PRIORITY.get(source,0)
        if score>best.get(k,(-1,""))[0]:
            best[k]=(score,source)
            vals[(name,local)][attr]=value
    pixels=defaultdict(set)
    for name,local,pix in c.execute(
        "SELECT tileset,local_id,has_visible_pixels FROM image_cells WHERE link_status='SOURCE_SLOT_LINKED_GRID_VERIFIED'"):
        if pix is not None:pixels[(name,local)].add(pix)
    c.close()
    prior={}
    with OLD.open(encoding="utf-8-sig",newline="") as f:
        for r in csv.DictReader(f):
            prior[(r["tile_set_name"],int(r["local_id"]))]=r
    if len(prior)!=10042:raise ValueError("Unexpected v255 prior size")
    return vals,pixels,prior

def rooms_for(root):
    result=defaultdict(list)
    details=[]
    for objgroup in root.findall("objectgroup"):
        if objgroup.get("name")!="RoomDefs":continue
        z=int(objgroup.get("level","0"))
        for ob in objgroup.findall("object"):
            x=int(float(ob.get("x","0"))/64);y=int(float(ob.get("y","0"))/32)
            w=int(round(float(ob.get("width","0"))/64))
            h=int(round(float(ob.get("height","0"))/32))
            if w<1 or h<1:continue
            name=ob.get("name","");tbx=ob.get("type","")
            details.append((z,name,x,y,w,h,tbx))
            for iy in range(max(y,0),min(y+h,256)):
                for ix in range(max(x,0),min(x+w,256)):
                    result[z,ix,iy].append((name,tbx))
    return result,details

def main():
    if OUT.exists() and any(OUT.iterdir()):raise FileExistsError("Refuse overwrite "+str(OUT))
    OUT.mkdir(parents=True,exist_ok=True)
    originals,pixels,prior=metadata()
    paths=[BASE/(str(x)+"_"+str(y)+".tmx") for x in range(28,35) for y in range(42,50)]
    if not all(p.exists() for p in paths):
        raise FileNotFoundError("Missing TMX: "+str([p.name for p in paths if not p.exists()]))
    detail={};all_tile_counts=Counter();category_counts=Counter();room_counts=Counter()
    file_audit=[];room_refs=[];tot=Counter()
    def get_definition(name,local):
        return originals.get((name,local),{})
    with gzip.open(OUT/"FURNITURE_PLACEMENTS.csv.gz","wt",encoding="utf-8-sig",newline="",compresslevel=6) as output:
        writer=csv.writer(output)
        writer.writerow(["zone","tmx","layer","world_x","world_y","z","room_bbox_name","room_tbx",
             "tileset","local_id","clean_gid","category","mode","CustomName","GroupName",
             "Facing","SpriteGridPos","Material","MaterialType","prior_visual_candidate","pixel_status"])
        for num,path in enumerate(paths,1):
            cx,cy=map(int,path.stem.split("_"))
            zone="CORE" if 30<=cx<=33 and 43<=cy<=48 else "BUFFER"
            root=ET.parse(path).getroot()
            if root.get("width")!="256" or root.get("height")!="256":
                raise ValueError("TMX width not 256: "+path.name)
            tilesets=sorted((int(t.get("firstgid")),t.get("name") or "") for t in root.findall("tileset"))
            starts=[s for s,name in tilesets]
            if not starts:raise ValueError("Empty tilesets "+path.name)
            roommap,rms=rooms_for(root)
            for z,name,x,y,w,h,tbx in rms:
                room_refs.append([path.name,z,name,cx*256+x,cy*256+y,w,h,tbx])
            counts=Counter()
            for layer in root.iter("layer"):
                el=layer.find("data")
                if el is None:continue
                if el.get("encoding")!="csv":raise ValueError("Unsupported TMX data encoding in "+path.name)
                nums=re.findall(r"\d+",el.text or "")
                if len(nums)!=65536:raise ValueError("Bad layer length "+path.name+"/"+str(layer.get("name")))
                counts["layers"]+=1;tot["layers"]+=1
                z=int(layer.get("level","0"));lname=layer.get("name","")
                memo={}
                for idx,raw in enumerate(nums):
                    if raw=="0":continue
                    gid=int(raw)&0x1fffffff
                    if not gid:continue
                    kt=memo.get(gid)
                    if kt is None:
                        j=bisect.bisect_right(starts,gid)-1
                        if j<0:
                            counts["bad_gid"]+=1;continue
                        name=tilesets[j][1];local=gid-starts[j]
                        cat,mode=classify(name);kt=(name,local,cat,mode);memo[gid]=kt
                    name,local,cat,mode=kt
                    all_tile_counts[(zone,name,local)]+=1
                    counts["all_gid"]+=1;tot["all_gid"]+=1
                    if mode=="EXCLUDED":continue
                    counts["furniture_gid"]+=1;tot["furniture_gid"]+=1
                    category_counts[(zone,mode,cat)]+=1
                    key=(name,local);d=detail.get(key)
                    if d is None:
                        props=get_definition(name,local)
                        old=prior.get(key,{})
                        px=pixels.get(key,set())
                        d={"name":name,"local":local,"cat":cat,"mode":mode,"props":props,
                           "prior":old.get("latest_visual_candidate_KO","") or old.get("object_identity_candidate",""),
                           "pixel":"VISIBLE" if 1 in px else "TRANSPARENT" if px=={0} else "NOT_VERIFIED",
                           "core":0,"buffer":0,"example":None}
                        detail[key]=d
                    d["core" if zone=="CORE" else "buffer"]+=1
                    xx,yy=idx%256,idx//256
                    wx,wy=cx*256+xx,cy*256+yy
                    rooms=roommap.get((z,xx,yy),[])
                    room,tbx=rooms[0] if rooms else ("","")
                    if d["example"] is None:d["example"]=(path.name,lname,wx,wy,z,room)
                    p=d["props"]
                    writer.writerow([zone,path.name,lname,wx,wy,z,room,tbx,name,local,gid,cat,mode,
                       p.get("CustomName",""),p.get("GroupName",""),p.get("Facing",""),
                       p.get("SpriteGridPos",""),p.get("Material",""),p.get("MaterialType",""),
                       d["prior"],d["pixel"]])
                    room_counts[(zone,room or "OUTSIDE_OR_UNKNOWN",cat)]+=1
            file_audit.append([path.name,zone,len(rms),counts["layers"],counts["all_gid"],
                               counts["furniture_gid"],counts["bad_gid"],path.stat().st_size])
            if num%7==0:print("TMX",num,"/",len(paths),"tagged placements",tot["furniture_gid"],flush=True)
    heads=["source_key","tile_set_name","local_id","category","mode","CustomName","GroupName",
        "Facing","SpriteGridPos","Material","MaterialType","source_has_properties",
        "pixel_status","v255_candidate","core_sprite_placements","buffer_sprite_placements",
        "total_sprite_placements","sample_tmx","sample_layer","sample_world_x","sample_world_y",
        "sample_z","sample_room","original_properties_json","minecraft_mod","minecraft_block_id"]
    rows=[]
    for (name,local),d in sorted(detail.items()):
        p=d["props"]
        rows.append([name+"/"+str(local),name,local,d["cat"],d["mode"],p.get("CustomName",""),
             p.get("GroupName",""),p.get("Facing",""),p.get("SpriteGridPos",""),
             p.get("Material",""),p.get("MaterialType",""),int(bool(p)),d["pixel"],d["prior"],
             d["core"],d["buffer"],d["core"]+d["buffer"],*d["example"],
             json.dumps(p,ensure_ascii=False,sort_keys=True,separators=(",",":")),"",""])
    write_csv(OUT/"ALL_FURNITURE_TILE_IDS.csv",heads,rows)
    write_csv(OUT/"ALL_USED_TILES_SUMMARY.csv",["zone","tileset","local_id","placements"],
        [[*k,v] for k,v in sorted(all_tile_counts.items())])
    write_csv(OUT/"ROOM_FURNITURE_COUNTS.csv",["zone","room_bbox","category","sprite_placements"],
        [[*k,v] for k,v in sorted(room_counts.items())])
    write_csv(OUT/"ROOMDEFS_TBX_REFERENCES.csv",
        ["tmx","z","room","world_x","world_y","width","height","tbx"],room_refs)
    write_csv(OUT/"TMX_AUDIT.csv",["tmx","zone","RoomDefs","layers","all_GIDs","furniture_GIDs","bad_GIDs","bytes"],file_audit)
    write_csv(OUT/"CATEGORY_SUMMARY.csv",
        ["zone","mode","category","sprite_placements","unique_tile_ids"],
        [[*k,v,len({(n,i) for (n,i),d in detail.items() if d["mode"]==k[1] and d["cat"]==k[2]
                    and (d["core"] if k[0]=="CORE" else d["buffer"])>0})]
          for k,v in sorted(category_counts.items())])
    db=sqlite3.connect(OUT/"ROSEWOOD_FURNITURE.sqlite")
    db.executescript("""
    CREATE TABLE furniture_tiles(source_key TEXT PRIMARY KEY,tileset TEXT,local_id INTEGER,category TEXT,
      mode TEXT,custom_name TEXT,group_name TEXT,facing TEXT,material TEXT,core_placements INTEGER,
      buffer_placements INTEGER,prior_candidate TEXT,properties_json TEXT);
    CREATE TABLE rooms(tmx TEXT,z INTEGER,name TEXT,world_x INTEGER,world_y INTEGER,width INTEGER,height INTEGER,tbx TEXT);
    CREATE INDEX room_name_index ON rooms(name);
    """)
    db.executemany("INSERT INTO furniture_tiles VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?)",
        [(n+"/"+str(i),n,i,d["cat"],d["mode"],d["props"].get("CustomName",""),
         d["props"].get("GroupName",""),d["props"].get("Facing",""),
         d["props"].get("Material",""),d["core"],d["buffer"],d["prior"],
         json.dumps(d["props"],ensure_ascii=False,sort_keys=True))
         for (n,i),d in sorted(detail.items())])
    db.executemany("INSERT INTO rooms VALUES(?,?,?,?,?,?,?,?)",room_refs)
    db.commit();integrity=db.execute("PRAGMA integrity_check").fetchone()[0];db.close()
    if integrity!="ok":raise ValueError("SQLite error")
    stats={
      "basis":"original 56 TMX files, GID->tileset/local ID, v259 raw 7-source .tiles and v255 names",
      "survey_tiles_x":[28,34],"survey_tiles_y":[42,49],
      "core_tiles_x":[30,33],"core_tiles_y":[43,48],
      "boundary_caution":"Only the CORE rectangle is treated as a Rosewood town-core proxy; BUFFER contains nearby buildings/forest/prison and is reported separately.",
      "counts":{"scanned_tmx":len(paths),"scanned_layers":tot["layers"],
        "all_gid_placements":tot["all_gid"],"selected_sprite_part_placements":tot["furniture_gid"],
        "unique_selected_tile_ids":len(detail),"unique_direct_ids":sum(d["mode"]=="DIRECT" for d in detail.values()),
        "unique_special_review_ids":sum(d["mode"]=="SPECIAL" for d in detail.values()),
        "core_selected_placements":sum(d["core"] for d in detail.values()),
        "buffer_selected_placements":sum(d["buffer"] for d in detail.values()),
        "roomdefs_object_refs":len(room_refs),
        "original_named_tile_ids":sum(bool(d["props"].get("CustomName")) for d in detail.values()),
        "old_visual_candidate_ids":sum(bool(d["prior"]) for d in detail.values())},
      "groups":[{"zone":z,"mode":m,"category":cat,"sprite_placements":v}
                for (z,m,cat),v in category_counts.most_common()],
      "limits":["A TMX tile GID equals a sprite part, not a complete furniture object.",
                "RoomDefs rectangle may overassign irregular rooms; TBX masks not reconstructed.",
                "Source CustomName is game object category, not exact Minecraft block mapping.",
                "Broad location and industry families include nonfurniture; SPECIAL mode preserves uncertainty.",
                "Buffer survey rectangle includes sites not formally Rosewood town."]
    }
    (OUT/"MANIFEST.json").write_text(json.dumps(stats,ensure_ascii=False,indent=2)+"\n",encoding="utf8")
    p=[(d["core"],n,i,d["props"].get("CustomName") or d["props"].get("GroupName") or d["prior"] or "(unnamed)")
       for (n,i),d in detail.items() if d["mode"]=="DIRECT"]
    p.sort(reverse=True)
    text=["# 로즈우드 가구 및 설비 TMX 전체 추출 결과","",
          "원본 TMX 56개를 직접 읽어 Local ID별/배치 위치별로 정리했다.","",
          "중심 영역: TMX X30..33, Y43..48. 주변 완충 조사 영역: X28..34, Y42..49.",
          "완충 영역은 로즈우드 행정 경계로 확정할 수 없으며 결과에서는 별도 집계한다.",
          "","## 검증 수치"]+[("- "+k+": "+str(v)) for k,v in stats["counts"].items()]+[
          "","## 중심 지역의 상위 가구 타일(동일 가구의 여러 부품은 각각 기록)","",
          "| 원본 타일 | 스프라이트 배치수 | 원본 이름/후보 |","|---|---:|---|"]
    text += [("| "+n+"/"+str(i)+" | "+str(cnt)+" | "+name.replace("|","/")+" |") for cnt,n,i,name in p[:75]]
    text += ["","## 전체 파일",
          "- ALL_FURNITURE_TILE_IDS.csv: 각 원본 타일 ID별 1행, 모드 블록 ID 대응용 빈 열 포함.",
          "- FURNITURE_PLACEMENTS.csv.gz: 실제 가구 후보의 모든 좌표, 층, 레이어, 사각 RoomDefs 방, TBX 경로.",
          "- CATEGORY_SUMMARY.csv: 가구 계열별 종류/배치 수.",
          "- ROOM_FURNITURE_COUNTS.csv: 방 유형별 후보 타일 수.",
          "- ALL_USED_TILES_SUMMARY.csv: 가구에 포함하지 않은 원본 GID도 검수 가능하도록 모두 집계.",
          "- ROOMDEFS_TBX_REFERENCES.csv: 사용된 방 오브젝트의 참조 파일.",
          "- ROSEWOOD_FURNITURE.sqlite: 가구 타일·방 원장.",
          "","## 판독 한계","- 완성된 가구 개수를 세지 않았으며, GID 배치 기록은 가구의 개별 스프라이트 부품이다.",
          "- 산업·특수 건물 등은 실제 가구와 구조물이 혼재하여 SPECIAL_REVIEW로 따로 분리해야 한다.",
          "- RoomDefs는 TBX 내부 방 마스크가 아닌 TMX 사각 영역에 근거하므로 방 이름은 근사치다.",
          "- 가구 모드 대응 블록 ID와 마인크래프트 최종 블록 배치는 미확정이다.",""]
    (OUT/"README_KO.md").write_text("\n".join(text),encoding="utf8")
    with zipfile.ZipFile(OUT/"ROSEWOOD_FURNITURE_CSV.zip","w",zipfile.ZIP_DEFLATED,compresslevel=6) as z:
        for path in OUT.glob("*.csv"):z.write(path,path.name)
        for name in ("FURNITURE_PLACEMENTS.csv.gz","MANIFEST.json","README_KO.md"):z.write(OUT/name,name)
    with zipfile.ZipFile(OUT/"ROSEWOOD_FURNITURE_SQLITE.zip","w",zipfile.ZIP_DEFLATED,compresslevel=6) as z:
        z.write(OUT/"ROSEWOOD_FURNITURE.sqlite","ROSEWOOD_FURNITURE.sqlite")
    print(json.dumps({"counts":stats["counts"],"groups":stats["groups"][:30],
         "example_top_direct":p[:20],
         "files":[[f.name,f.stat().st_size] for f in OUT.iterdir()]},
         ensure_ascii=False,indent=2),flush=True)

if __name__=="__main__":main()
