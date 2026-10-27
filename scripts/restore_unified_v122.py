#!/usr/bin/env python3
"""Restore full historical v122 SQLite with SHA-256 and PRAGMA integrity_check."""
from pathlib import Path
import base64,hashlib,json,sqlite3,sys,zlib
R=Path(__file__).resolve().parents[1]
m=json.loads((R/'analysis/current/v122/MANIFEST.json').read_text('utf8'))
payload=''.join((R/p).read_text('ascii').strip() for p in m['parts'])
data=base64.b64decode(payload,validate=True)
assert hashlib.sha256(data).hexdigest()==m['compressed_sha256']
raw=zlib.decompress(data)
assert hashlib.sha256(raw).hexdigest()==m['sqlite_sha256']
assert len(raw)==m['sqlite_size_bytes']
out=Path(sys.argv[1] if len(sys.argv)>1 else '/tmp/pz_v122.sqlite')
out.parent.mkdir(parents=True,exist_ok=True)
out.write_bytes(raw)
with sqlite3.connect(out) as db:
    assert db.execute('PRAGMA integrity_check').fetchone()[0]=='ok'
    assert db.execute('SELECT count(*) FROM tile_catalog').fetchone()[0]==5409
    assert db.execute('SELECT count(*) FROM tile_catalog WHERE observed_any=1').fetchone()[0]==5400
    assert db.execute('SELECT count(*) FROM v121_abcd_evidence').fetchone()[0]==160
    assert db.execute('SELECT count(*) FROM v122_ai_visual_review_160').fetchone()[0]==160
    assert db.execute('SELECT count(*) FROM tile_catalog WHERE identity_final_certified=1').fetchone()[0]==0
print('PASS full v122 historical DB',out,m['sqlite_sha256'])
