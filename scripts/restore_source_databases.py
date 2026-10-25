#!/usr/bin/env python3
"""Rebuild source SQLite databases from text shards in this public GitHub repo."""
from pathlib import Path
import sys, json, base64, lzma, hashlib, sqlite3
ROOT=Path(__file__).resolve().parents[1]
MAN=json.loads((ROOT/'analysis/imports/SOURCE_ARCHIVES_MANIFEST.json').read_text('utf8'))
def restore(name, output_dir):
 m=MAN[name];encoded=''.join((ROOT/x).read_text('ascii').strip() for x in m['parts'])
 xz=base64.b64decode(encoded,validate=True)
 assert hashlib.sha256(xz).hexdigest()==m['xz_sha256'],name+' compressed hash mismatch'
 raw=lzma.decompress(xz)
 assert hashlib.sha256(raw).hexdigest()==m['sqlite_sha256'],name+' DB hash mismatch'
 output_dir.mkdir(parents=True,exist_ok=True);dst=output_dir/(f'tile_visual_{name}.sqlite')
 dst.write_bytes(raw)
 with sqlite3.connect(dst) as db:assert db.execute('PRAGMA integrity_check').fetchone()[0]=='ok'
 print('Restored',name,dst,len(raw),'bytes')
if __name__=='__main__':
 output=Path(sys.argv[1]).resolve() if len(sys.argv)>1 else ROOT/'restored_sources'
 for key in sorted(MAN):restore(key,output)