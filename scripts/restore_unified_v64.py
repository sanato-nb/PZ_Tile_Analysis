#!/usr/bin/env python3
"""GitHub v64 압축 조각 SHA-256·SQLite 무결성·누적 수치 검증 복원."""
from pathlib import Path
import base64,hashlib,json,sqlite3,sys,zlib
root=Path(__file__).resolve().parents[1]
m=json.loads((root/'analysis/current/v64/MANIFEST.json').read_text('utf8'))
encoded=''.join((root/p).read_text('ascii').strip() for p in m['parts'])
packed=base64.b64decode(encoded,validate=True)
assert hashlib.sha256(packed).hexdigest()==m['compressed_sha256']
raw=zlib.decompress(packed)
assert hashlib.sha256(raw).hexdigest()==m['sqlite_sha256']
target=Path(sys.argv[1]).resolve() if len(sys.argv)>1 else root/'analysis/current/tile_visual_v64_unified.sqlite'
target.parent.mkdir(parents=True,exist_ok=True);target.write_bytes(raw)
with sqlite3.connect(target) as c:
 assert c.execute('PRAGMA integrity_check').fetchone()[0]=='ok'
 checks={'all':c.execute('select count(*) from tile_catalog').fetchone()[0],
  'observed':c.execute('select count(*) from tile_catalog where observed_any=1').fetchone()[0],
  'candidate':c.execute('select count(*) from tile_catalog where provisional_candidate_any_auditable=1').fetchone()[0],
  'remaining':c.execute('select count(*) from analysis_queue').fetchone()[0],
  'v64review':c.execute('select count(*) from v64_visual_review').fetchone()[0],
  'final':c.execute('select count(*) from tile_catalog where identity_final_certified=1').fetchone()[0]}
 assert checks=={'all':5409,'observed':3072,'candidate':2656,'remaining':2337,'v64review':12,'final':0},checks
print('PASS SHA256/SQLite v64',str(target),len(raw),'bytes',checks)
