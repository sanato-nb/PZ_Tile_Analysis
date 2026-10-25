#!/usr/bin/env python3
"""SHA-verified reconstruction of the ONE physically integrated v49 SQLite."""
import base64,hashlib,json,sqlite3,zlib,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
m=json.loads((ROOT/"analysis/current/v49/MANIFEST.json").read_text("utf8"))
b64="".join((ROOT/p).read_text("ascii").strip() for p in m["parts"])
packed=base64.b64decode(b64,validate=True)
assert hashlib.sha256(packed).hexdigest()==m["compressed_sha256"]
raw=zlib.decompress(packed)
assert hashlib.sha256(raw).hexdigest()==m["sqlite_sha256"]
out=Path(sys.argv[1]).resolve() if len(sys.argv)>1 else ROOT/"analysis/current/tile_visual_v49_unified.sqlite"
out.parent.mkdir(parents=True,exist_ok=True)
out.write_bytes(raw)
with sqlite3.connect(out) as c:
 assert c.execute("pragma integrity_check").fetchone()[0]=="ok"
 def n(sql):return c.execute(sql).fetchone()[0]
 assert n("select count(*) from tile_catalog")==5409
 assert n("select count(*) from tile_catalog where observed_any=1")==2614
 assert n("select count(*) from tile_catalog where provisional_candidate_any_auditable=1")==2325
 assert n("select count(*) from analysis_queue")==2795
 assert n("select count(*) from v36_full_scope")==5409
 assert n("select count(*) from v48__review_checkpoint")==30
print("RESTORE PASS:",out,len(raw),"bytes; observed 2614/5409; SHA",m["sqlite_sha256"])
