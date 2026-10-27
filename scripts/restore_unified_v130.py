#!/usr/bin/env python3
"""Restore full historical v130 SQLite with SHA-256 and PRAGMA integrity_check."""
from pathlib import Path
import base64,hashlib,json,sqlite3,sys,zlib
R=Path(__file__).resolve().parents[1]
m=json.loads((R/'analysis/current/v130/MANIFEST.json').read_text('utf8'))
payload=''.join((R/p).read_text('ascii').strip() for p in m['parts'])
data=base64.b64decode(payload,validate=True)
assert hashlib.sha256(data).hexdigest()==m['compressed_sha256']
raw=zlib.decompress(data)
assert hashlib.sha256(raw).hexdigest()==m['sqlite_sha256']
assert len(raw)==m['sqlite_bytes']
out=Path(sys.argv[1] if len(sys.argv)>1 else '/tmp/pz_v130.sqlite')
out.parent.mkdir(parents=True,exist_ok=True)
out.write_bytes(raw)
with sqlite3.connect(out) as db:
    assert db.execute('PRAGMA integrity_check').fetchone()[0]=='ok'
    assert db.execute('SELECT count(*) FROM tile_catalog').fetchone()[0]==5409
    assert db.execute('SELECT count(*) FROM tile_catalog WHERE observed_any=1').fetchone()[0]==5400
    assert db.execute('SELECT count(*) FROM v121_abcd_evidence').fetchone()[0]==160
    assert db.execute('SELECT count(*) FROM v122_ai_visual_review_160').fetchone()[0]==160
    assert db.execute("SELECT count(*) FROM v123_abcd_evidence_next160").fetchone()[0]==160
    assert db.execute("SELECT count(*) FROM v124_d_placement_4472").fetchone()[0]==4472
    assert db.execute("SELECT count(*) FROM v124_d_placement_4472 WHERE d_status='actual_second_placement'").fetchone()[0]==2791
    assert db.execute("SELECT count(*) FROM v124_d_placement_4472 WHERE d_status='actual_second_placement' AND d_level=0").fetchone()[0]>0
    assert db.execute('SELECT count(*) FROM v125_ai_visual_spotcheck_20').fetchone()[0]==20
    assert db.execute('SELECT count(*) FROM v126_alt_A_B_160').fetchone()[0]==160
    assert db.execute('SELECT count(*) FROM v127_d_candidate_catalog_4633').fetchone()[0]==4633
    assert db.execute("SELECT count(*) FROM v127_d_candidate_catalog_4633 WHERE search_status='held_no_source_PNG'").fetchone()[0]==1
    assert db.execute('SELECT count(*) FROM v128_D_source_variant_B_3').fetchone()[0]==3
    assert db.execute('SELECT count(*) FROM v128_D_source_variant_B_3 WHERE B_D_changed_pixels > 0').fetchone()[0]==3
    assert db.execute('SELECT count(*) FROM v129_alt_A_B_320').fetchone()[0]==320
    assert db.execute('SELECT count(*) FROM v130_alt_A_B_320').fetchone()[0]==320
    assert db.execute('SELECT count(*) FROM v129_alt_A_B_320 WHERE B_D_changed_pixels > 0').fetchone()[0]==316
    assert db.execute('SELECT count(*) FROM v130_alt_A_B_320 WHERE B_D_changed_pixels > 0').fetchone()[0]==291
    assert len({r[0] for r in db.execute("SELECT name FROM sqlite_master WHERE type='table'")})==192
    assert db.execute('SELECT count(*) FROM tile_catalog WHERE identity_final_certified=1').fetchone()[0]==0
print('PASS full v130 historical DB',out,m['sqlite_sha256'])
