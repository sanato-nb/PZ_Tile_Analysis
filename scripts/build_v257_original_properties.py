#!/usr/bin/env python3
"""v257 additive original .tiles evidence. No historical table or manual verdict is changed."""
import argparse, base64, hashlib, json, sqlite3, struct, subprocess, sys, tempfile, zipfile, zlib
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PARENT_SHA = "25df5bcd9ef1f332bc1178ae711ec09f43e070bbf8cc3c33b4e822a0a1766791"
CANONICAL_ZIP_SHA = "ffba6f55e178ef0c4622906bfdd670c6a7cae779cf6dbe4e7d4b0dce45c18171"
OUT = ROOT / "analysis/current/v257"
PRIORITY = {"tiledefinitions_noiseworks.patch.tiles": 50, "newtiledefinitions.tiles": 40,
            "tiledefinitions_erosion.tiles": 30, "tiledefinitions_overlays.tiles": 20,
            "tiledefinitions_b42chunkcaching.tiles": 15, "jumbo_trees_big.tiles": 10,
            "jumbo_trees.tiles": 10}

def sha(raw):
    return hashlib.sha256(raw).hexdigest()

def parse_tiles(raw):
    if raw[:4] != b"tdef":
        raise ValueError("Bad tdef magic")
    version, count = struct.unpack_from("<II", raw, 4)
    pos = 12
    def line():
        nonlocal pos
        end = raw.find(b"\n", pos)
        if end < 0:
            raise ValueError("Unterminated tile definition string")
        value = raw[pos:end].decode("utf-8")
        pos = end + 1
        return value
    for _ in range(count):
        name, image = line(), line()
        width, height, tileset_id, slots = struct.unpack_from("<IIII", raw, pos)
        pos += 16
        if width < 1 or height < 1 or slots > 100000 or slots < 1:
            raise ValueError("Invalid tileset dimensions")
        for local_id in range(slots):
            propcount, = struct.unpack_from("<I", raw, pos)
            pos += 4
            if propcount > 500:
                raise ValueError("Invalid property count")
            props = {}
            for __ in range(propcount):
                k, v = line(), line()
                if k in props:
                    raise ValueError("Duplicate property in a single source tile")
                props[k] = v
            yield version, name, image, width, height, tileset_id, local_id, props
    if pos != len(raw):
        raise ValueError(f"Trailing bytes in .tiles file: {len(raw)-pos}")

def sources(zip_path):
    if zip_path:
        path = Path(zip_path)
        if sha(path.read_bytes()) != CANONICAL_ZIP_SHA:
            raise ValueError("Not the expected user-uploaded B42 tiledef.zip SHA256")
        with zipfile.ZipFile(path) as z:
            names = [n for n in z.namelist() if n.endswith(".tiles")]
            if len(names) != 7:
                raise ValueError("Canonical B42 archive must have exactly seven .tiles files")
            return {n: z.read(n) for n in names}, "canonical_user_zip_seven_sources"
    paths = [ROOT / "Tiles/newtiledefinitions.tiles", ROOT / "Tiles/tiledefinitions.tiles"]
    if not all(p.is_file() for p in paths):
        raise FileNotFoundError("Missing GitHub repository main/legacy .tiles source")
    return {p.name: p.read_bytes() for p in paths}, "repository_main_plus_legacy_NOT_canonical"

def create(args):
    src, source_status = sources(args.source_zip)
    # An earlier repo-only one-file artifact on THIS working branch may be
    # superseded by the richer two-file repo-only artifact. Never overwrite
    # any canonical seven-source release, nor any unrecognized existing files.
    if OUT.exists():
        previous = OUT / "MANIFEST.json"
        extra = [p for p in OUT.iterdir() if p.name != "README.md"]
        if extra:
            if not previous.is_file():
                raise FileExistsError("Unrecognized v257 files, refusing overwrite")
            meta = json.loads(previous.read_text("utf-8"))
            if not (meta.get("source_status")=="repository_main_only_NOT_canonical"
                    and source_status=="repository_main_plus_legacy_NOT_canonical"):
                raise FileExistsError("Refusing to overwrite an existing v257 release")
            expected = {previous.name}|{Path(p).name for p in meta["parts"]}
            if {p.name for p in extra}!=expected:
                raise FileExistsError("Unexpected files in v257 output directory")
            for p in extra:
                p.unlink()
    with tempfile.TemporaryDirectory(prefix="pz_v257_") as td:
        td = Path(td)
        parent = td/"v255.sqlite"
        subprocess.run([sys.executable, str(ROOT/"scripts/restore_v255_master.py"), str(parent)],
                       check=True)
        if sha(parent.read_bytes()) != PARENT_SHA:
            raise AssertionError("v255 parent hash changed")
        prev = sqlite3.connect(f"file:{parent}?mode=ro", uri=True)
        old = {name: (sql, prev.execute('SELECT COUNT(*) FROM "'+name.replace('"','""')+'"').fetchone()[0])
               for name, sql in prev.execute("SELECT name,sql FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%'")}
        if len(old) != 260:
            raise AssertionError("Expected 260 original tables")
        assert prev.execute("SELECT count(*) FROM v255_latest_preferred_10042").fetchone()[0] == 10042
        dbpath = td/"v257.sqlite"
        with sqlite3.connect(dbpath) as db:
            prev.backup(db)
            db.executescript("""
CREATE TABLE v257_source_file (filename TEXT PRIMARY KEY, sha256 TEXT, file_size INTEGER, tdef_version INTEGER, source_mode TEXT);
CREATE TABLE v257_source_slot (tileset TEXT, local_id INTEGER, source_file TEXT, image TEXT, width INTEGER, height INTEGER, tileset_id INTEGER,
 PRIMARY KEY(tileset,local_id,source_file));
CREATE TABLE v257_source_property (tileset TEXT, local_id INTEGER, prop_key TEXT, prop_value TEXT, source_file TEXT,
 PRIMARY KEY(tileset,local_id,prop_key,source_file));
CREATE TABLE v257_property_candidate (tileset TEXT,local_id INTEGER,prop_key TEXT,prop_value TEXT,preferred_source TEXT,source_count INTEGER,value_conflict INTEGER,
 PRIMARY KEY(tileset,local_id,prop_key));
CREATE TABLE v257_conflict (tileset TEXT,local_id INTEGER,prop_key TEXT,raw_variants_json TEXT,
 PRIMARY KEY(tileset,local_id,prop_key));
CREATE TABLE v257_v255_join (source_key TEXT PRIMARY KEY,match_status TEXT,source_count INTEGER,
 prop_count INTEGER,custom_name TEXT,group_name TEXT,facing TEXT,sprite_grid_pos TEXT,
 container_type TEXT,container_capacity TEXT,material TEXT,material_type TEXT,solid TEXT,
 official_mapping_certified INTEGER NOT NULL DEFAULT 0 CHECK(official_mapping_certified=0),
 identity_certified INTEGER NOT NULL DEFAULT 0 CHECK(identity_certified=0));
CREATE TABLE v257_manifest_kv (key TEXT PRIMARY KEY,value_json TEXT);
CREATE INDEX idx_v257_slot ON v257_source_slot(tileset,local_id);
CREATE INDEX idx_v257_prop ON v257_source_property(tileset,local_id,prop_key);
""")
            all_props = defaultdict(list)
            file_stats = {}
            for filename, raw in sorted(src.items()):
                seen = 0
                for version, name, image, width, height, tileset_id, local_id, props in parse_tiles(raw):
                    db.execute("INSERT INTO v257_source_slot VALUES(?,?,?,?,?,?,?)",
                               (name,local_id,filename,image,width,height,tileset_id))
                    for k,v in props.items():
                        db.execute("INSERT INTO v257_source_property VALUES(?,?,?,?,?)",
                                   (name,local_id,k,v,filename))
                        all_props[(name,local_id,k)].append((filename,v))
                    seen += 1
                db.execute("INSERT INTO v257_source_file VALUES(?,?,?,?,?)",
                           (filename,sha(raw),len(raw),version,source_status))
                file_stats[filename] = {"bytes":len(raw),"sha256":sha(raw),"slots":seen}
            for (name,local,k), variants in all_props.items():
                items = sorted(variants, key=lambda x: (-PRIORITY.get(x[0],0),x[0]))
                distinct = {v for _,v in items}
                db.execute("INSERT INTO v257_property_candidate VALUES(?,?,?,?,?,?,?)",
                           (name,local,k,items[0][1],items[0][0],len(items),int(len(distinct)>1)))
                if len(distinct)>1:
                    db.execute("INSERT INTO v257_conflict VALUES(?,?,?,?)",
                               (name,local,k,json.dumps(items,ensure_ascii=False)))
            props_lookup = defaultdict(dict)
            for n,i,k,v in db.execute("SELECT tileset,local_id,prop_key,prop_value FROM v257_property_candidate"):
                props_lookup[(n,i)][k] = v
            slot_sources = defaultdict(set)
            for n,i,s in db.execute("SELECT tileset,local_id,source_file FROM v257_source_slot"):
                slot_sources[(n,i)].add(s)
            rows = list(db.execute("SELECT source_key,tile_set_name,local_id FROM v255_latest_preferred_10042"))
            if len(rows)!=10042 or len({x[0] for x in rows})!=10042:
                raise AssertionError("Nonunique v255 keys")
            for key,name,lid in rows:
                sourceset = slot_sources.get((name,int(lid)),set())
                p = props_lookup.get((name,int(lid)),{})
                db.execute("INSERT INTO v257_v255_join(source_key,match_status,source_count,prop_count,custom_name,group_name,facing,sprite_grid_pos,container_type,container_capacity,material,material_type,solid) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?)",
                           (key,"slot_found" if sourceset else "not_found",len(sourceset),len(p),
                            p.get("CustomName"),p.get("GroupName"),p.get("Facing"),p.get("SpriteGridPos"),
                            p.get("container"),p.get("ContainerCapacity"),p.get("Material"),p.get("MaterialType"),p.get("solid")))
            db.executescript("""
CREATE VIEW v257_master_with_official AS
SELECT m.*, o.match_status AS v257_source_match, o.source_count AS v257_source_count,
o.prop_count AS v257_original_property_count, o.custom_name AS v257_original_custom_name,
o.group_name AS v257_original_group_name, o.facing AS v257_original_facing,
o.sprite_grid_pos AS v257_original_sprite_grid_pos, o.container_type AS v257_original_container,
o.container_capacity AS v257_original_container_capacity, o.material AS v257_original_material,
o.official_mapping_certified AS v257_official_mapping_certified,
o.identity_certified AS v257_final_identity_certified
FROM v255_latest_preferred_10042 m
JOIN v257_v255_join o ON m.source_key=o.source_key;
""")
            stats = {
              "version":"v257",
              "source_status":source_status,
              "canonical_full_source":source_status.startswith("canonical_"),
              "parent_sha256":PARENT_SHA,"parent_tables_preserved":260,
              "tile_keys":len(rows),
              "matched_keys":db.execute("SELECT count(*) FROM v257_v255_join WHERE match_status='slot_found'").fetchone()[0],
              "unmatched_keys":db.execute("SELECT count(*) FROM v257_v255_join WHERE match_status='not_found'").fetchone()[0],
              "source_slot_rows":db.execute("SELECT count(*) FROM v257_source_slot").fetchone()[0],
              "source_property_rows":db.execute("SELECT count(*) FROM v257_source_property").fetchone()[0],
              "multipart_slots":db.execute("SELECT count(*) FROM v257_property_candidate WHERE prop_key='SpriteGridPos'").fetchone()[0],
              "conflicting_attributes":db.execute("SELECT count(*) FROM v257_conflict").fetchone()[0],
              "files":file_stats,
              "official_id_certifications_added":0,"identity_certifications_added":0,
              "v255_held_439":db.execute("SELECT count(*) FROM v255_latest_held439").fetchone()[0],
              "v255_user_68":db.execute("SELECT count(*) FROM v255_user68_manual_verdict").fetchone()[0],
              "active":db.execute("SELECT count(*) FROM v240_active_tile_master").fetchone()[0],
              "excluded":db.execute("SELECT count(*) FROM v240_excluded_archive_455").fetchone()[0],
              "patch_precedence":"candidate_only_not_engine_verified",
            }
            for k,v in stats.items():
                db.execute("INSERT INTO v257_manifest_kv VALUES(?,?)",(k,json.dumps(v,ensure_ascii=False)))
            db.commit()
            after = {name:(sql,db.execute('SELECT COUNT(*) FROM "'+name.replace('"','""')+'"').fetchone()[0])
                     for name,sql in db.execute("SELECT name,sql FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%'") if name in old}
            assert old==after,"Historical 260-table schema/rowcount changed"
            assert stats["v255_held_439"]==439 and stats["v255_user_68"]==68
            assert stats["active"]==9587 and stats["excluded"]==455
            assert db.execute("SELECT count(*) FROM v257_master_with_official").fetchone()[0]==10042
            assert db.execute("PRAGMA integrity_check").fetchone()[0]=="ok"
        prev.close()
        packed=zlib.compress(dbpath.read_bytes(),6)
        enc=base64.b64encode(packed).decode("ascii")
        OUT.mkdir(parents=True,exist_ok=True)
        parts=[]
        for i,offset in enumerate(range(0,len(enc),3000000)):
            part=OUT/f"v257.part{i:03d}.b64"
            part.write_text(enc[offset:offset+3000000]+"\n",encoding="ascii")
            parts.append(str(part.relative_to(ROOT)))
        manifest = {**stats,"sqlite_bytes":dbpath.stat().st_size,"sqlite_sha256":sha(dbpath.read_bytes()),
                    "zlib_sha256":sha(packed),"parts":parts,"sqlite_integrity":"ok",
                    "source_warning":"Repository main/legacy .tiles differ from the canonical seven-source user ZIP; repo-only build is provisional" if not args.source_zip else ""}
        (OUT/"MANIFEST.json").write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+"\n",encoding="utf8")
        print(json.dumps({k:v for k,v in manifest.items() if k!="files"},ensure_ascii=False,indent=2))
def main():
    p=argparse.ArgumentParser()
    p.add_argument("--source-zip",help="Canonical user-uploaded tiledef.zip, SHA-256 checked. Omit to run repo single-source preview")
    a=p.parse_args()
    create(a)
if __name__=="__main__":
    main()
