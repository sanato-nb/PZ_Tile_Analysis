#!/usr/bin/env python3
"""Restore the verified v240 10,042 tile SQLite from committed zlib+base64 parts."""
import argparse,base64,hashlib,json,sqlite3,zlib
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def digest(b):return hashlib.sha256(b).hexdigest()
def restore(destination):
    m=json.loads((ROOT/"analysis/current/v240/MANIFEST.json").read_text("utf8"))
    encoded="".join((ROOT/p).read_text("ascii").strip() for p in m["v240_parts"])
    packed=base64.b64decode(encoded,validate=True)
    assert digest(packed)==m["v240_zlib_sha256"],"compressed file SHA mismatch"
    data=zlib.decompress(packed)
    assert len(data)==m["v240_sqlite_bytes"] and digest(data)==m["v240_sqlite_sha256"],"database SHA mismatch"
    destination.parent.mkdir(parents=True,exist_ok=True)
    destination.write_bytes(data)
    with sqlite3.connect("file:"+str(destination.resolve())+"?mode=ro",uri=True) as con:
        assert con.execute("PRAGMA integrity_check").fetchone()[0]=="ok"
        assert con.execute("SELECT COUNT(*) FROM v240_tile_master_10042").fetchone()[0]==10042
        assert con.execute("SELECT COUNT(*) FROM v240_active_tile_master").fetchone()[0]==9587
        assert con.execute("SELECT COUNT(*) FROM v240_excluded_archive_455").fetchone()[0]==455
        assert con.execute("SELECT COUNT(*) FROM tile_catalog").fetchone()[0]==5409
        assert con.execute("SELECT COUNT(*) FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%'").fetchone()[0]==258
    print("PASS: v240 restored",destination,"sha256",digest(data))
if __name__=="__main__":
    p=argparse.ArgumentParser()
    p.add_argument("output",nargs="?",default="PZ_Tile_Analysis_v240_MASTER_10042.sqlite")
    a=p.parse_args()
    restore(Path(a.output).resolve())
