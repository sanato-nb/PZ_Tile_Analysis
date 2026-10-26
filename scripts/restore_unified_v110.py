#!/usr/bin/env python3
"""Restore v110 physical SQLite without promoting any unresolved keys."""
from pathlib import Path
import base64,hashlib,json,sqlite3,sys,zlib
ROOT=Path(__file__).resolve().parents[1]
m=json.loads((ROOT/'analysis/current/v110/MANIFEST.json').read_text('utf8'))
encoded=''.join((ROOT/x).read_text('ascii').strip() for x in m['parts'])
packed=base64.b64decode(encoded,validate=True)
assert hashlib.sha256(packed).hexdigest()==m['compressed_sha256']
raw=zlib.decompress(packed)
assert len(raw)==m['sqlite_size_bytes'] and hashlib.sha256(raw).hexdigest()==m['sqlite_sha256']
out=Path(sys.argv[1]) if len(sys.argv)>1 else Path('/tmp/tile_visual_v110_unified.sqlite')
out.parent.mkdir(parents=True,exist_ok=True);out.write_bytes(raw)
with sqlite3.connect(out) as c:
    assert c.execute('PRAGMA integrity_check').fetchone()[0]=='ok'
    checks=dict(all=c.execute('SELECT count(*) FROM tile_catalog').fetchone()[0],
      observed=c.execute('SELECT count(*) FROM tile_catalog WHERE observed_any=1').fetchone()[0],
      candidate=c.execute('SELECT count(*) FROM tile_catalog WHERE provisional_candidate_any_auditable=1').fetchone()[0],
      remaining=c.execute('SELECT count(*) FROM analysis_queue').fetchone()[0],
      audit=c.execute('SELECT count(*) FROM v110_unresolved_queue_audit').fetchone()[0],
      final=c.execute('SELECT count(*) FROM tile_catalog WHERE identity_final_certified=1').fetchone()[0])
    assert checks==dict(all=5409,observed=5358,candidate=4475,remaining=51,audit=51,final=0),checks
print('PASS restored v110 diagnostic physical sqlite',out,checks)