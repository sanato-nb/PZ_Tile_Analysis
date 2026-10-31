#!/usr/bin/env python3
"""Full PNG-cell catalog, grounded in seven unmodified B42 .tiles files."""
import csv, hashlib, json, sqlite3, struct, zipfile
from pathlib import Path
from collections import Counter, defaultdict

ROOT=Path(__file__).resolve().parents[1]
TILES=ROOT/"Tiles"
TDEF=ROOT/"tiledef/tiledef.zip"
V255=ROOT/"review/v255_latest_integrated_10042_2026-10-30/MASTER_ALL_10042_LATEST_PREFERRED.csv"
OUT=ROOT/"analysis/current/v258"
ZIP_SHA="ffba6f55e178ef0c4622906bfdd670c6a7cae779cf6dbe4e7d4b0dce45c18171"
PRIOR={"tiledefinitions_noiseworks.patch.tiles":50,"newtiledefinitions.tiles":40,
       "tiledefinitions_erosion.tiles":30,"tiledefinitions_overlays.tiles":20,
       "tiledefinitions_b42chunkcaching.tiles":15,"jumbo_trees_big.tiles":10,
       "jumbo_trees.tiles":10}
STRUCT={"WallN","WallW","WallNW","WallSE","wall","DoorWallN","DoorWallW",
        "WindowN","WindowW","solid","solidtrans","solidfloor","PhysicsMesh",
        "BlocksPlacement","IsMoveAble","collideN","collideW"}
def sha(data):return hashlib.sha256(data).hexdigest()
def parse(raw,filename,layouts,original,values):
    if raw[:4]!=b"tdef":raise ValueError("tdef magic: "+filename)
    version,count=struct.unpack_from("<II",raw,4)
    pos=12; nslot=nprop=0
    def line():
        nonlocal pos
        e=raw.find(b"\n",pos)
        if e<0:raise ValueError("unterminated string")
        s=raw[pos:e].decode("utf8");pos=e+1;return s
    for _ in range(count):
        name,image=line(),line()
        w,h,tid,slots=struct.unpack_from("<IIII",raw,pos);pos+=16
        if slots!=w*h or slots>100000:raise ValueError("invalid layout: "+name)
        layouts[name].append((filename,w,h,image,tid))
        for i in range(slots):
            num,=struct.unpack_from("<I",raw,pos);pos+=4
            original[(name,i)].add(filename)
            for j in range(num):
                k,v=line(),line()
                values[(name,i,k)].append((filename,v))
            nprop+=num;nslot+=1
    if pos!=len(raw):raise ValueError("trailing bytes: "+filename)
    return dict(file=filename,version=version,sha256=sha(raw),tilesets=count,slots=nslot,properties=nprop,bytes=len(raw))
def img_size(path):
    with path.open("rb") as f:h=f.read(33)
    if h[:8]!=b"\x89PNG\r\n\x1a\n" or h[12:16]!=b"IHDR":raise ValueError("bad PNG "+str(path))
    return struct.unpack_from(">II",h,16)
def csv_write(path,header,rows):
    with path.open("w",encoding="utf-8-sig",newline="") as f:
        w=csv.writer(f);w.writerow(header);w.writerows(rows)
def main():
    if sha(TDEF.read_bytes())!=ZIP_SHA:raise ValueError("canonical tiledef.zip hash does not match")
    if not V255.exists():raise FileNotFoundError(V255)
    if OUT.exists() and any(OUT.iterdir()):raise FileExistsError("Refusing to overwrite existing v258")
    OUT.mkdir(parents=True,exist_ok=True)
    layouts=defaultdict(list); original=defaultdict(set);values=defaultdict(list)
    with zipfile.ZipFile(TDEF) as z:
        if z.testzip():raise ValueError("invalid source ZIP CRC")
        src=sorted(n for n in z.namelist() if n.endswith(".tiles"))
        if len(src)!=7:raise ValueError("expected seven original binary definitions")
        stats=[parse(z.read(n),n,layouts,original,values) for n in src]
    prior={}
    with V255.open(encoding="utf-8-sig",newline="") as f:
        for r in csv.DictReader(f):
            k=(r["tile_set_name"],int(r["local_id"]))
            if k in prior:raise ValueError("duplicate v255 key "+str(k))
            prior[k]=r
    if len(prior)!=10042:raise ValueError("v255 does not have 10042 keys")
    choices={}
    collisions=[]
    for k,versions in values.items():
        ordered=sorted(versions,key=lambda x:(-PRIOR.get(x[0],0),x[0]))
        choices[k]=ordered[0][1]
        if len({v for f,v in versions})>1:
            collisions.append((k[0],k[1],k[2],json.dumps(ordered,ensure_ascii=False)))
    pngs=sorted(TILES.rglob("*.png"))
    if not pngs:raise ValueError("no PNG source files")
    names=defaultdict(list)
    for n in layouts:names[n.casefold()].append(n)
    try:
        from PIL import Image
        pillow=True
    except ImportError:
        Image=None;pillow=False
    db=OUT/"PZ_v258_all_png_tile_definitions.sqlite"
    con=sqlite3.connect(db)
    con.executescript("""
    CREATE TABLE source_files(file TEXT PRIMARY KEY, version INT, sha256 TEXT, tilesets INT, slots INT, properties INT, bytes INT);
    CREATE TABLE source_tilesets(name TEXT,source_file TEXT,columns_count INT,rows_count INT,image TEXT,tile_set_id INT,PRIMARY KEY(name,source_file));
    CREATE TABLE source_slots(name TEXT,local_id INT,source_file TEXT,PRIMARY KEY(name,local_id,source_file));
    CREATE TABLE source_attributes(name TEXT,local_id INT,attribute TEXT,value TEXT,source_file TEXT,PRIMARY KEY(name,local_id,attribute,source_file));
    CREATE TABLE image_atlases(png_path TEXT PRIMARY KEY,width INT,height INT,cell_width INT,cell_height INT,columns_count INT,rows_count INT,grid_cells INT,tileset TEXT,link_status TEXT,pixel_scan_status TEXT);
    CREATE TABLE image_cells(png_path TEXT,grid_id INT,column_index INT,row_index INT,has_visible_pixels INT,tileset TEXT,local_id INT,link_status TEXT,source_files TEXT,properties_json TEXT,custom_name TEXT,group_name TEXT,facing TEXT,sprite_grid_pos TEXT,material TEXT,material_type TEXT,structural_properties TEXT,v255_identity_candidate TEXT,v255_visual_candidate TEXT,v255_user_choice TEXT,v255_held INT,conflicting_attributes TEXT,PRIMARY KEY(png_path,grid_id));
    CREATE INDEX ix_cells_local ON image_cells(tileset,local_id);
    CREATE INDEX ix_cells_state ON image_cells(link_status);
    CREATE INDEX ix_props ON source_attributes(name,local_id);
    """)
    con.executemany("INSERT INTO source_files VALUES(:file,:version,:sha256,:tilesets,:slots,:properties,:bytes)",stats)
    con.executemany("INSERT INTO source_tilesets VALUES(?,?,?,?,?,?)",
      ((name,f,w,h,image,tid) for name,parts in layouts.items() for f,w,h,image,tid in parts))
    con.executemany("INSERT INTO source_slots VALUES(?,?,?)",
      ((name,i,f) for (name,i),ss in original.items() for f in sorted(ss)))
    con.executemany("INSERT INTO source_attributes VALUES(?,?,?,?,?)",
      ((name,i,attr,val,f) for (name,i,attr),pairs in values.items() for f,val in pairs))
    headers=["png_path","grid_id","grid_x","grid_y","has_visible_pixels","tile_set_name",
      "local_id","link_status","definition_sources","property_count","CustomName","GroupName",
      "Facing","SpriteGridPos","Material","MaterialType","structure_properties","v255_identity_candidate",
      "v255_visual_candidate","v255_user_choice","v255_held","all_properties_json","source_conflict_attributes"]
    counters=Counter();audits=[]
    master=OUT/"ALL_PNG_GRID_CELLS.csv"
    with master.open("w",encoding="utf-8-sig",newline="") as f:
      csvout=csv.writer(f);csvout.writerow(headers)
      for index,path in enumerate(pngs,1):
        rel=path.relative_to(ROOT).as_posix();stem=path.stem
        w,h=img_size(path)
        tw,th=(128,256) if path.relative_to(TILES).parts[0].lower()=="2x" else (64,128)
        nc,nr=w//tw,h//th
        if nc<1 or nr<1:raise ValueError("undersized atlas "+rel)
        same=names.get(stem.casefold(),[])
        name=stem if stem in same else (same[0] if len(same)==1 else "")
        sources=layouts.get(name,[])
        shapes={(a,b) for f,a,b,img,tid in sources}
        if not name:status="NO_SOURCE_TILESET_NAME"
        elif len(shapes)!=1:status="CONFLICTING_SOURCE_GRID"
        elif shapes.pop()!=(nc,nr):status="GRID_DIMENSION_MISMATCH"
        elif w%tw or h%th:status="PARTIAL_PNG_EDGE"
        else:status="MATCHED_TILESET_AND_GRID"
        scan="not_checked";alpha=None
        if pillow:
            try:
                with Image.open(path) as img:
                    if img.size!=(w,h):raise ValueError("PNG dimensions changed during scan")
                    if img.mode in ("RGBA","LA") or "transparency" in img.info:
                        alpha=img.convert("RGBA").getchannel("A");scan="alpha_checked"
                    else:scan="image_without_alpha"
            except Exception as e:
                scan="decode_error";counters["image_decode_errors"]+=1
                print("WARN PNG decode",rel,str(e)[:130],flush=True)
        con.execute("INSERT INTO image_atlases VALUES(?,?,?,?,?,?,?,?,?,?,?)",
                    (rel,w,h,tw,th,nc,nr,nc*nr,name,status,scan))
        counters["image_files"]+=1;counters["grid_cells_total"]+=nc*nr
        counters["atlas_"+status]+=1
        audits.append([rel,path.stat().st_size,w,h,tw,th,nc,nr,nc*nr,name,status,scan])
        for i in range(nc*nr):
            gx,gy=i%nc,i//nc
            visible=None if scan in ("not_checked","decode_error") else 1
            if alpha is not None:
                visible=int(alpha.crop((gx*tw,gy*th,(gx+1)*tw,(gy+1)*th)).getbbox() is not None)
            counters["pixels_transparent" if visible==0 else "pixels_opaque_or_visible" if visible==1 else "pixels_unknown"]+=1
            if status=="MATCHED_TILESET_AND_GRID" and (name,i) in original:
                linked=True;state="SOURCE_SLOT_LINKED_GRID_VERIFIED"
            elif status=="MATCHED_TILESET_AND_GRID":
                linked=False;state="CELL_WITHOUT_DEFINITION_SLOT"
            else:
                linked=False;state="LOCAL_ID_MAPPING_NOT_VERIFIED"
            counters["cell_"+state]+=1
            props={a:choices[(name,i,a)] for (n,j,a) in []} if False else {}
            if linked:
                # Preserve all source values in SQLite; this is the display-preferred projection only.
                props={attr:val for (n,j,attr),val in choices.items() if n==name and j==i}
            old=prior.get((name,i),{}) if status=="MATCHED_TILESET_AND_GRID" else {}
            if old:counters["v255_image_cells_linked"]+=1
            files="|".join(sorted(original[(name,i)])) if linked else ""
            structure="|".join(sorted(STRUCT.intersection(props)))
            conflicting="|".join(sorted(c for n,j,c,other in collisions if n==name and j==i))
            pp=json.dumps(props,ensure_ascii=False,sort_keys=True,separators=(",",":"))
            held=int(old.get("latest_held_provisional_only","0")=="1")
            csvout.writerow([rel,i,gx,gy,visible if visible is not None else "",name,i if linked else "",
                state,files,len(props),props.get("CustomName",""),props.get("GroupName",""),
                props.get("Facing",""),props.get("SpriteGridPos",""),props.get("Material",""),
                props.get("MaterialType",""),structure,old.get("object_identity_candidate",""),
                old.get("latest_visual_candidate_KO",""),old.get("latest_user_choice",""),held,pp,conflicting])
            con.execute("INSERT INTO image_cells VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
                (rel,i,gx,gy,visible,name,i if linked else None,state,files,pp,
                 props.get("CustomName",""),props.get("GroupName",""),props.get("Facing",""),
                 props.get("SpriteGridPos",""),props.get("Material",""),props.get("MaterialType",""),
                 structure,old.get("object_identity_candidate",""),old.get("latest_visual_candidate_KO",""),
                 old.get("latest_user_choice",""),held,conflicting))
        if alpha is not None:alpha.close()
        if index%40==0:
            con.commit();print("processed image",index,"/",len(pngs),flush=True)
    csv_write(OUT/"PNG_FILE_GRID_AUDIT.csv",
        ["png_path","file_bytes","image_width","image_height","cell_width","cell_height",
         "columns","rows","grid_cells","matched_source_tileset","link_status","pixel_scan_status"],audits)
    csv_write(OUT/"SOURCE_PROPERTY_CONFLICTS.csv",
        ["tileset","local_id","property","source_values_json"],collisions)
    linkedkeys=set(con.execute("SELECT DISTINCT tileset,local_id FROM image_cells WHERE link_status='SOURCE_SLOT_LINKED_GRID_VERIFIED'"))
    missing=[]
    for key,files in original.items():
        if key in linkedkeys:continue
        vals={a:choices[(key[0],key[1],a)] for a in
              ("CustomName","GroupName","Facing","SpriteGridPos") if (key[0],key[1],a) in choices}
        missing.append([key[0],key[1],"|".join(sorted(files)),vals.get("CustomName",""),
                        vals.get("GroupName",""),vals.get("Facing",""),vals.get("SpriteGridPos","")])
    csv_write(OUT/"SOURCE_SLOTS_NOT_LINKED_TO_PNG.csv",
      ["tileset","local_id","source_files","CustomName","GroupName","Facing","SpriteGridPos"],
      sorted(missing))
    absent=[]
    for key,r in prior.items():
        if key not in original:
            absent.append([r["source_key"],key[0],key[1],"no exact source key in original seven"])
    csv_write(OUT/"V255_KEYS_ABSENT_FROM_TILEDEF.csv",
      ["source_key","tileset","local_id","reason"],absent)
    con.commit()
    integrity=con.execute("PRAGMA integrity_check").fetchone()[0]
    tables={t:con.execute("SELECT COUNT(*) FROM "+t).fetchone()[0] for t in
            ("source_files","source_tilesets","source_slots","source_attributes","image_atlases","image_cells")}
    if integrity!="ok" or tables["image_cells"]!=counters["grid_cells_total"]:
        raise AssertionError("SQLite failure or row count mismatch")
    con.close()
    if len(absent)!=3:raise AssertionError("Original source discrepancy vs v255 changed")
    summary={"version":"v258","basis":"all PNG image grid cells + seven original .tiles sources",
      "source_zip_sha256":ZIP_SHA,"source_file_stats":stats,"counters":dict(sorted(counters.items())),
      "source_unique_keys":len(original),"original_unlinked_to_verified_image":len(missing),
      "v255_keys":len(prior),"v255_source_keys_missing":len(absent),
      "source_conflict_instances":len(collisions),"sqlite_row_counts":tables,
      "sqlite_sha256":sha(db.read_bytes()),"sqlite_integrity":integrity,
      "limitations":["PNG grid cell is not necessarily a discrete visible object",
        "PNG-to-Local-ID link is based on exact name and grid, not engine-level certification",
        "Partial PNG grid or inconsistent definition dimensions are not force-mapped",
        "Legacy v255 predictions remain unmodified and are never overwritten by original names",
        "No previous data or source images were modified"]}
    (OUT/"MANIFEST.json").write_text(json.dumps(summary,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    (OUT/"README.md").write_text(
      "# v258 original definition PNG tile catalog\n\n"+
      "Input: all original Tiles PNG files, seven .tiles in tiledef/tiledef.zip, historical v255 master CSV.\n\n"+
      "ALL_PNG_GRID_CELLS.csv: one row per PNG grid cell, including transparent cells and unmapped cells.\n"+
      "PNG_FILE_GRID_AUDIT.csv: PNG dimensions, grid sizes, match status.\n"+
      "SOURCE_SLOTS_NOT_LINKED_TO_PNG.csv: original slot records without safe image mapping.\n"+
      "SOURCE_PROPERTY_CONFLICTS.csv: all raw conflicting property values.\n"+
      "V255_KEYS_ABSENT_FROM_TILEDEF.csv: previous map keys without an exact original key.\n"+
      "PZ_v258_all_png_tile_definitions.sqlite: searchable complete source attributes and image cells.\n"+
      "MANIFEST.json: counts and file checks.\n\n"+
      "Matched name and grid do not establish official sprite/ID certification. Original properties "+
      "describe game behavior and metadata, not necessarily the exact object or component. "+
      "Historical user decisions and held statuses are preserved.\n",encoding="utf-8")
    with zipfile.ZipFile(OUT/"PZ_v258_full_CSV.zip","w",zipfile.ZIP_DEFLATED,compresslevel=6) as z:
        for p in sorted(OUT.glob("*.csv")):z.write(p,p.name)
        z.write(OUT/"MANIFEST.json","MANIFEST.json")
        z.write(OUT/"README.md","README.md")
    with zipfile.ZipFile(OUT/"PZ_v258_full_SQLite.zip","w",zipfile.ZIP_DEFLATED,compresslevel=6) as z:
        z.write(db,db.name)
    print(json.dumps(summary,ensure_ascii=False,indent=2),flush=True)
    print("CSV ZIP MB",round((OUT/"PZ_v258_full_CSV.zip").stat().st_size/1e6,2),
          "DB ZIP MB",round((OUT/"PZ_v258_full_SQLite.zip").stat().st_size/1e6,2),flush=True)
if __name__=="__main__":main()
