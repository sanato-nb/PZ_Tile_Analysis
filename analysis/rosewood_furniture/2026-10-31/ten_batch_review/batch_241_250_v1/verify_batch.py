#!/usr/bin/env python3
"""Verify Rosewood lane C batch 241-250 without modifying original files."""
import csv, hashlib, io, json, pathlib, zipfile
ROOT = pathlib.Path(__file__).resolve().parent
M = json.loads((ROOT / "MANIFEST.json").read_text(encoding="utf-8"))
assert M["range"] == [241, 250]
rows = list(csv.DictReader((ROOT / "BATCH_241_250_MANUAL_VISUAL_REVIEW.csv").open(encoding="utf-8", newline="")))
assert [int(x["index"]) for x in rows] == list(range(241,251))
assert all(x["verdict"] == "DEFERRED_VISUAL_MISMATCH" and x["game_1to1_certified"] == "false" for x in rows)
checks = list(csv.DictReader((ROOT / "SOURCE_SHA256.csv").open(encoding="utf-8", newline="")))
assert len(checks) == 20
for x in checks:
    f = ROOT / x["path"]
    assert f.is_file(), f
    b = f.read_bytes()
    assert hashlib.sha256(b).hexdigest() == x["sha256"], f
    assert hashlib.sha1(b"blob " + str(len(b)).encode() + b"\0" + b).hexdigest() == x["git_blob_sha1"], f
zip_path = ROOT / "ROSEWOOD_BATCH_241_250_REVIEW.zip"
with zipfile.ZipFile(zip_path) as z:
    assert z.testzip() is None
    expected = set(M["zip_entries"])
    assert set(z.namelist()) == expected, (len(z.namelist()), len(expected))
    for n in expected:
        assert z.read(n) == (ROOT / n).read_bytes(), n
assert hashlib.sha256(zip_path.read_bytes()).hexdigest() == (ROOT / "ZIP_SHA256.txt").read_text().split()[0]
print(f"PASS: {len(rows)} reviewed, {len(checks)} image hashes, {len(M['zip_entries'])} ZIP members and CRC32; no in-game certification")
