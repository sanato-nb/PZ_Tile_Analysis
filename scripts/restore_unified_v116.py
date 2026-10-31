#!/usr/bin/env python3
"""SHA-256 restore full historical v116 SQLite; six source-unavailable excluded active only."""
from pathlib import Path
import json,base64,zlib,hashlib,sqlite3,sys
R=Path(__file__).resolve().parents[1]
m=json.loads((R/'analysis/current/v116/MANIFEST.json').read_text('utf8'))
enc=''.join((R/p).read_text('ascii').strip() for p in m['parts'])
packed=base64.b64decode(enc,validate=True)
assert hashlib.sha256(packed).hexdigest()==m['compressed_sha256']
raw=zlib.decompress(packed)
assert len(raw)==m['sqlite_size_bytes'] and hashlib.sha256(raw).hexdigest()==m['sqlite_sha256']
out=Path(sys.argv[1]).resolve() if len(sys.argv)>1 else Path('/tmp/tile_visual_v116_unified.sqlite')
out.parent.mkdir(parents=True,exist_ok=True);out.write_bytes(raw)
with sqlite3.connect(out) as c:
    assert c.execute('PRAGMA integrity_check').fetchone()[0]=='ok'
    count=lambda query:c.execute(query).fetchone()[0]
    d=dict(catalog=count('SELECT count(*) FROM tile_catalog'),
       observed=count('SELECT count(*) FROM tile_catalog WHERE observed_any=1'),
       prior_auditable_candidate=count('SELECT count(*) FROM tile_catalog WHERE provisional_candidate_any_auditable=1'),
       v115_ai_candidates=count('SELECT count(*) FROM v115_ai_candidate_queue'),
       v115_historical_held=count('SELECT count(*) FROM v115_ai_held_queue'),
       v116_user_excluded=count('SELECT count(*) FROM v116_user_excluded_missing_image'),
       v116_active_held=count('SELECT count(*) FROM v116_active_v115_held_queue'),
       v116_active_review=count('SELECT count(*) FROM v116_active_v115_review_queue'),
       v113_user_excluded=count("SELECT count(*) FROM v113_user_review WHERE user_action='exclude_from_active_review'"),
       v113_active_unobserved=count('SELECT count(*) FROM v113_active_review_queue'),
       original_unobserved=count('SELECT count(*) FROM analysis_queue'),
       final_certified=count('SELECT count(*) FROM tile_catalog WHERE identity_final_certified=1'))
    assert d==dict(catalog=5409,observed=5400,prior_auditable_candidate=4512,
      v115_ai_candidates=882,v115_historical_held=6,v116_user_excluded=6,
      v116_active_held=0,v116_active_review=882,v113_user_excluded=8,
      v113_active_unobserved=1,original_unobserved=9,final_certified=0),d
    assert c.execute('SELECT sum(official_transparent_certified) FROM v116_user_excluded_missing_image').fetchone()[0]==0
    assert c.execute('SELECT sum(mapping_verified),sum(tilezed_verified),sum(final_certified) FROM v115_ai_visual_review').fetchone()==(0,0,0)
print('PASS full v116 physical SQLite and user six excluded active (historical 6 kept)',d,m['sqlite_sha256'])
