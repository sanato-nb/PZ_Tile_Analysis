#!/usr/bin/env python3
"""Restore merged SQLite from tracked zlib-base64; confirm SQLite integrity."""
from pathlib import Path
import zlib,base64,sqlite3,sys
ROOT=Path(__file__).resolve().parents[1]
s=(ROOT/'analysis/imports/merged_evidence_v47.sqlite.zlib.b64').read_text(encoding='ascii').strip()
out=Path(sys.argv[1]).resolve() if len(sys.argv)>1 else ROOT/'analysis/imports/merged_evidence_v47.sqlite'
out.parent.mkdir(parents=True,exist_ok=True)
out.write_bytes(zlib.decompress(base64.b64decode(s)))
with sqlite3.connect(out) as c:assert c.execute('PRAGMA integrity_check').fetchone()[0]=='ok'
print(out)