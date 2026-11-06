"""Restore the published v258 furniture database from its pinned parent and page delta."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import sqlite3
import struct
import subprocess
import sys
import tempfile
import zlib

ROOT = Path(__file__).resolve().parents[1]
RELEASE = ROOT / "analysis/current/v258"


def checksum(path):
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def restore(output):
    manifest = json.loads((RELEASE / "MANIFEST.json").read_text(encoding="utf-8"))
    output.parent.mkdir(parents=True, exist_ok=True)
    if output.exists():
        raise FileExistsError(output)
    delta_path = RELEASE / "v258.pages.zlib"
    if checksum(delta_path) != manifest["delta_sha256"]:
        raise ValueError("Invalid v258 delta hash")
    with tempfile.TemporaryDirectory(dir=output.parent) as directory:
        database = Path(directory) / "working.sqlite"
        subprocess.run([sys.executable, str(ROOT / "scripts/restore_v257_master.py"),
                        str(database)], check=True)
        if checksum(database) != manifest["parent_sha256"]:
            raise ValueError("Invalid parent database hash")
        delta = zlib.decompress(delta_path.read_bytes())
        size = manifest["block_size"]
        stride = size + 4
        if len(delta) != stride * manifest["changed_blocks"]:
            raise ValueError("Invalid delta length")
        with database.open("r+b") as stream:
            stream.truncate(manifest["sqlite_bytes"])
            for start in range(0, len(delta), stride):
                block_number = struct.unpack_from(">I", delta, start)[0]
                stream.seek(block_number * size)
                stream.write(delta[start + 4:start + stride])
        if checksum(database) != manifest["sqlite_sha256"]:
            raise ValueError("Invalid v258 database hash")
        with sqlite3.connect(database) as connection:
            if connection.execute("PRAGMA integrity_check").fetchone() != ("ok",):
                raise ValueError("Database integrity check failed")
            if connection.execute("PRAGMA foreign_key_check").fetchone():
                raise ValueError("Foreign key violation")
        connection.close()
        os.link(database, output)
    print("Verified v258:", output)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("output", type=Path)
    restore(parser.parse_args().output.expanduser().resolve())
