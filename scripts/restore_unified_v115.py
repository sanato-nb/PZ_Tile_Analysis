#!/usr/bin/env python3
"""Restore full v115 SQLite after content hashes; preserve all v36..v113 historical tables."""
from pathlib import Path
import json,base64,zlib,hashlib,sqlite3,sys
R=Path(__file__).resolve().parents[1]
m=json.loads((R/'analysis/current/v115/MANIFEST.json').read_text('utf8'))
enc=''.join((R/p).read_text('ascii').strip() for p in m['parts'])
compressed=base64.b64decode(enc,validate=True)
assert hashlib.sha256(compressed).hexdigest()==m['compressed_sha256']
raw=zlib.decompress(compressed)
assert len(raw)==m['sqlite_size_bytes'] and hashlib.sha256(raw).hexdigest()==m['sqlite_sha256']
out=Path(sys.argv[1]).resolve() if len(sys.argv)>1 else Path('/tmp/tile_visual_v115_unified.sqlite')
out.parent.mkdir(parents=True,exist_ok=True);out.write_bytes(raw)
with sqlite3.connect(out) as c:
 assert c.execute('PRAGMA integrity_check').fetchone()[0]=='ok'
 results=dict(catalog=c.execute('select count(*) from tile_catalog').fetchone()[0],
  prior_observed=c.execute('select count(*) from tile_catalog where observed_any=1').fetchone()[0],
  prior_candidate=c.execute('select count(*) from tile_catalog where provisional_candidate_any_auditable=1').fetchone()[0],
  v115_review=c.execute('select count(*) from v115_ai_visual_review').fetchone()[0],
  v115_candidate=c.execute('select count(*) from v115_ai_candidate_queue').fetchone()[0],
  v115_held=c.execute('select count(*) from v115_ai_held_queue').fetchone()[0],
  old_unobserved=c.execute('select count(*) from analysis_queue').fetchone()[0],
  user_excluded=c.execute("select count(*) from v113_user_review where user_action='exclude_from_active_review'").fetchone()[0],
  active_unobserved=c.execute('select count(*) from v113_active_review_queue').fetchone()[0],
  final_certified=c.execute('select count(*) from tile_catalog where identity_final_certified=1').fetchone()[0])
 assert results==dict(catalog=5409,prior_observed=5400,prior_candidate=4512,
  v115_review=888,v115_candidate=882,v115_held=6,old_unobserved=9,user_excluded=8,
  active_unobserved=1,final_certified=0),results
 assert c.execute('select sum(mapping_verified),sum(tilezed_verified),sum(final_certified) from v115_ai_visual_review').fetchone()==(0,0,0)
print('PASS v115 all historical tables persisted, AI provisional not certified:',results,'SHA',m['sqlite_sha256'])
