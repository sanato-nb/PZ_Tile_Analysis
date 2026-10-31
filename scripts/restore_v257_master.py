#!/usr/bin/env python3
"""Restore v257 repo-source append-only SQLite with content hash and historical checks."""
import argparse, base64, hashlib, json, os, sqlite3, tempfile, zlib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "analysis/current/v257/MANIFEST.json"

def sha(data):
    return hashlib.sha256(data).hexdigest()

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("output", type=Path, help="New target SQLite path (must not already exist)")
    args = ap.parse_args()
    target = args.output.expanduser().resolve()
    if target.exists():
        raise SystemExit("Refusing to overwrite existing file: " + str(target))
    manifest = json.loads(MANIFEST.read_text("utf-8"))
    assert manifest["parent_tables_preserved"] == 260
    assert manifest["tile_keys"] == 10042
    assert manifest["matched_keys"] + manifest["unmatched_keys"] == 10042
    chunks = []
    for part in manifest["parts"]:
        path = (ROOT / part).resolve()
        if not path.is_relative_to(ROOT.resolve()):
            raise ValueError("Unsafe shard path")
        chunks.append(path.read_text("ascii").strip())
    packed = base64.b64decode("".join(chunks), validate=True)
    if sha(packed) != manifest["zlib_sha256"]:
        raise ValueError("Compressed v257 SHA-256 mismatch")
    raw = zlib.decompress(packed)
    if sha(raw) != manifest["sqlite_sha256"] or len(raw) != manifest["sqlite_bytes"]:
        raise ValueError("Restored v257 SQLite hash or size mismatch")
    target.parent.mkdir(parents=True, exist_ok=True)
    temporary = None
    try:
        with tempfile.NamedTemporaryFile(prefix=".pz_v257_", suffix=".sqlite",
                                         dir=target.parent, delete=False) as f:
            temporary = Path(f.name)
            f.write(raw)
        with sqlite3.connect(f"file:{temporary}?mode=ro", uri=True) as db:
            assert db.execute("PRAGMA integrity_check").fetchone()[0] == "ok"
            count = db.execute("SELECT count(*) FROM v257_master_with_official").fetchone()[0]
            assert count == 10042
            assert db.execute("SELECT count(*) FROM v255_latest_held439").fetchone()[0] == 439
            assert db.execute("SELECT count(*) FROM v255_user68_manual_verdict").fetchone()[0] == 68
            assert db.execute("SELECT count(*) FROM v240_active_tile_master").fetchone()[0] == 9587
            assert db.execute("SELECT count(*) FROM v240_excluded_archive_455").fetchone()[0] == 455
        os.link(temporary, target)
    finally:
        if temporary is not None and temporary.exists():
            temporary.unlink()
    print("PASS v257 restored:",target)
    print("SOURCE STATUS:",manifest["source_status"])
    if not manifest["canonical_full_source"]:
        print("WARNING: This contains repo main + legacy definitions, NOT all 7 user ZIP binaries.")
    print("SQLITE SHA-256:",manifest["sqlite_sha256"])

if __name__ == "__main__":
    main()
