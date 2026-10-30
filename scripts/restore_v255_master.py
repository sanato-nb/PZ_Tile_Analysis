#!/usr/bin/env python3
"""Recover the v255 source-preserving physical SQLite from its GitHub chunked archive."""
import base64,hashlib,json,sqlite3,zlib,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
manifest=json.loads((ROOT/"analysis/current/v255/MANIFEST.json").read_text("utf-8"))
chunk="".join((ROOT/x).read_text("ascii").strip() for x in manifest["parts"])
rawz=base64.b64decode(chunk,validate=True)
sha=lambda x:hashlib.sha256(x).hexdigest()
assert sha(rawz)==manifest["zlib_sha256"],"compressed archive SHA mismatch"
raw=zlib.decompress(rawz)
assert sha(raw)==manifest["new_sqlite_sha256"] and len(raw)==manifest["new_sqlite_bytes"]
dest=Path(sys.argv[1]) if len(sys.argv)>1 else ROOT/"analysis/current/v255/PZ_latest_v255_10042.sqlite"
dest.parent.mkdir(parents=True,exist_ok=True)
if dest.exists():raise SystemExit("Refusing to overwrite existing SQLite: "+str(dest))
dest.write_bytes(raw)
with sqlite3.connect("file:"+str(dest)+"?mode=ro",uri=True) as db:
 assert db.execute("PRAGMA integrity_check").fetchone()[0]=="ok"
 tablecount=db.execute("SELECT count(*) FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%'").fetchone()[0]
 assert tablecount==260,tablecount
 assert db.execute("SELECT count(*) FROM v255_latest_preferred_10042").fetchone()[0]==10042
 assert db.execute("SELECT count(*) FROM v255_latest_held439").fetchone()[0]==439
 assert db.execute("SELECT count(*) FROM v255_user68_manual_verdict").fetchone()[0]==68
 assert db.execute("SELECT count(*) FROM v240_active_tile_master").fetchone()[0]==9587
 assert db.execute("SELECT count(*) FROM v240_excluded_archive_455").fetchone()[0]==455
 print("PASS v255 DB restore: 260 tables, 10042 keys, 439 latest, 68 users, 9587 active / 455 held")
 print("SHA256:",sha(raw));print("Path:",dest)
