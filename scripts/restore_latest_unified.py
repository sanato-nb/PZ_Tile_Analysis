#!/usr/bin/env python3
"""Safely restore the SQLite version selected by PROJECT_STATE.json.

Checks compressed and decompressed SHA256, byte length, SQLite integrity,
physical table count and legacy catalog count. Never overwrites an output.
Original PNG, TMX and historical version data remain untouched.
"""
from __future__ import annotations
import argparse
import base64
import hashlib
import json
from pathlib import Path
import shutil
import sqlite3
import tempfile
import zlib

ROOT = Path(__file__).resolve().parents[1]


def sha256(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def repo_file(relative: str) -> Path:
    root = ROOT.resolve()
    path = (root / relative).resolve()
    if not path.is_relative_to(root):
        raise ValueError(f"Path escapes repository: {relative}")
    return path


def restore(target: Path) -> dict:
    state = json.loads(repo_file("PROJECT_STATE.json").read_text(encoding="utf-8"))
    cp = state["latest_checkpoint"]
    db_state = state["unified_database"]
    version = cp["version"]
    if db_state["version"] != version:
        raise ValueError("Canonical state has mismatched DB/checkpoint versions")

    manifest = json.loads(repo_file(db_state["repo_manifest"]).read_text(encoding="utf-8"))
    if manifest["version"] != version or manifest["sqlite_sha256"] != db_state["sqlite_sha256"]:
        raise ValueError("Physical manifest does not match canonical project state")
    encoded = "".join(repo_file(p).read_text(encoding="ascii").strip() for p in manifest["parts"])
    compressed = base64.b64decode(encoded, validate=True)
    if sha256(compressed) != manifest["compressed_sha256"]:
        raise ValueError("Compressed SQLite SHA-256 mismatch")
    raw = zlib.decompress(compressed)
    if len(raw) != manifest["sqlite_bytes"] or sha256(raw) != manifest["sqlite_sha256"]:
        raise ValueError("SQLite bytes or SHA-256 mismatch")

    target = target.expanduser().resolve()
    if target.exists():
        raise FileExistsError(f"Refusing to overwrite: {target}")
    target.parent.mkdir(parents=True, exist_ok=True)
    tmp_path = None
    try:
        with tempfile.NamedTemporaryFile(prefix=".pz_verified_", suffix=".sqlite", dir=target.parent, delete=False) as f:
            tmp_path = Path(f.name)
            f.write(raw)
        with sqlite3.connect(f"file:{tmp_path}?mode=ro", uri=True) as conn:
            if conn.execute("PRAGMA integrity_check").fetchone()[0] != "ok":
                raise ValueError("SQLite integrity_check failed")
            count = conn.execute("SELECT COUNT(*) FROM sqlite_master WHERE type='table'").fetchone()[0]
            if count != manifest["table_count"] or count != db_state["table_count"]:
                raise ValueError(f"Physical SQLite table count mismatch: {count}")
            original = conn.execute("SELECT COUNT(*) FROM tile_catalog").fetchone()[0]
            if original != 5409:
                raise ValueError(f"Historical 5409-key catalog changed: {original}")
            current_review = f"{version}_visual_review"
            if db_state.get(f"{version}_visual_review_rows") is not None:
                rows = conn.execute(f'SELECT COUNT(*) FROM "{current_review}"').fetchone()[0]
                if rows != db_state[f"{version}_visual_review_rows"]:
                    raise ValueError("Latest review row count mismatch")
        # Open output exclusively only after all checks have passed.
        with target.open("xb") as output, tmp_path.open("rb") as source:
            shutil.copyfileobj(source, output)
        if sha256(target.read_bytes()) != manifest["sqlite_sha256"]:
            target.unlink(missing_ok=True)
            raise ValueError("Restored output SHA-256 differs from canonical bytes")
    finally:
        if tmp_path is not None:
            tmp_path.unlink(missing_ok=True)
    return {"version": version, "table_count": manifest["table_count"], "sha256": manifest["sqlite_sha256"], "path": str(target)}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Restore the latest verified physical SQLite without overwriting files")
    parser.add_argument("output", type=Path, help="New output SQLite path; must not exist")
    args = parser.parse_args()
    print("PASS", json.dumps(restore(args.output), ensure_ascii=False))
