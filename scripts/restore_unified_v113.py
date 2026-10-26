#!/usr/bin/env python3
"""Restore the entire v113 SQLite with preserved historical queue and review-only exclusions."""
from pathlib import Path
import base64,hashlib,json,sqlite3,sys,zlib
ROOT=Path(__file__).resolve().parents[1]
m=json.loads((ROOT/'analysis/current/v113/MANIFEST.json').read_text('utf8'))
encoded=''.join((ROOT/p).read_text('ascii').strip() for p in m['parts'])
packed=base64.b64decode(encoded,validate=True)
assert hashlib.sha256(packed).hexdigest()==m['compressed_sha256']
raw=zlib.decompress(packed)
assert len(raw)==m['sqlite_size_bytes'] and hashlib.sha256(raw).hexdigest()==m['sqlite_sha256']
out=Path(sys.argv[1]).resolve() if len(sys.argv)>1 else Path('/tmp/tile_visual_v113_unified.sqlite')
out.parent.mkdir(parents=True,exist_ok=True);out.write_bytes(raw)
with sqlite3.connect(out) as c:
    assert c.execute('PRAGMA integrity_check').fetchone()[0]=='ok'
    d=dict(total=c.execute('SELECT count(*) FROM tile_catalog').fetchone()[0],
      observed=c.execute('SELECT count(*) FROM tile_catalog WHERE observed_any=1').fetchone()[0],
      candidate=c.execute('SELECT count(*) FROM tile_catalog WHERE provisional_candidate_any_auditable=1').fetchone()[0],
      historic=c.execute('SELECT count(*) FROM analysis_queue').fetchone()[0],
      active=c.execute('SELECT count(*) FROM v113_active_review_queue').fetchone()[0],
      excluded=c.execute("SELECT count(*) FROM v113_user_review WHERE user_action='exclude_from_active_review'").fetchone()[0],
      provisional=c.execute("SELECT count(*) FROM v113_user_review WHERE user_action='keep_provisional'").fetchone()[0],
      certified=c.execute('SELECT count(*) FROM tile_catalog WHERE identity_final_certified=1').fetchone()[0])
    assert d==dict(total=5409,observed=5400,candidate=4512,historic=9,active=1,excluded=8,provisional=1,certified=0),d
    assert c.execute('SELECT tile_set_locator,local_id FROM v113_active_review_queue').fetchall()==[('f_bushes_1',66)]
print('PASS v113 full SQLite restore and user review queue',d,out)