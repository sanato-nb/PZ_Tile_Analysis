#!/usr/bin/env python3
"""Restore immutable-parent v132 PZ SQLite from committed b64/zlib parts.

v132 preserves all 193 v131 physical tables and appends one 23-row review
table; observations are provisional, not Local ID or TileZed-certified.
"""
from pathlib import Path
import base64, hashlib, json, sqlite3, sys, zlib

ROOT = Path(__file__).resolve().parents[1]
manifest = json.loads((ROOT / "analysis/current/v132/MANIFEST.json").read_text(encoding="utf-8"))
assert manifest["version"] == "v132" and manifest["parent"] == "v131"
assert manifest["parent_tables_preserved"] == 193 and manifest["table_count"] == 194
encoded = "".join((ROOT / part).read_text(encoding="ascii").strip() for part in manifest["parts"])
compressed = base64.b64decode(encoded, validate=True)
assert hashlib.sha256(compressed).hexdigest() == manifest["compressed_sha256"]
raw = zlib.decompress(compressed)
assert len(raw) == manifest["sqlite_bytes"]
assert hashlib.sha256(raw).hexdigest() == manifest["sqlite_sha256"]
target = Path(sys.argv[1] if len(sys.argv) > 1 else "/tmp/pz_v132.sqlite")
target.parent.mkdir(parents=True, exist_ok=True)
if target.exists():
    raise FileExistsError(f"Refusing to overwrite existing SQLite: {target}")
target.write_bytes(raw)
with sqlite3.connect(target) as db:
    assert db.execute("PRAGMA integrity_check").fetchone()[0] == "ok"
    tables = {row[0] for row in db.execute("SELECT name FROM sqlite_master WHERE type='table'")}
    assert len(tables) == 194
    assert db.execute("SELECT count(*) FROM tile_catalog").fetchone()[0] == 5409
    assert db.execute("SELECT count(*) FROM tile_catalog WHERE observed_any=1").fetchone()[0] == 5400
    assert db.execute("SELECT count(*) FROM v131_D_full_4633").fetchone()[0] == 4633
    assert db.execute("SELECT count(*) FROM v132_visual3_jumbo20").fetchone()[0] == 23
    assert db.execute("SELECT count(*) FROM v132_visual3_jumbo20 WHERE observed=1 AND status='provisional_candidate'").fetchone()[0] == 3
    assert db.execute("SELECT count(*) FROM v132_visual3_jumbo20 WHERE observed=0 AND status='held'").fetchone()[0] == 20
    assert db.execute("SELECT count(*) FROM v132_visual3_jumbo20 WHERE mapping_verified != 0 OR tilezed_verified != 0 OR certified != 0").fetchone()[0] == 0
    assert db.execute("SELECT count(*) FROM tile_catalog WHERE identity_final_certified=1").fetchone()[0] == 0
print("PASS v132 physical SQLite restored:", str(target), manifest["sqlite_sha256"])
