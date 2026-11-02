#!/usr/bin/env python3
"""Verify batch 271-280 evidence bytes and review archive; no in-game certification."""
from __future__ import annotations
import csv
import hashlib
import json
from pathlib import Path
from zipfile import ZipFile

ROOT = Path(__file__).resolve().parent
MANIFEST = json.loads((ROOT / "MANIFEST.json").read_text(encoding="utf-8"))
assert MANIFEST["range"] == [271, 280]
assert MANIFEST["reviewed_count"] == 10
assert MANIFEST["deferred_count"] == 10
assert MANIFEST["game_certified_count"] == 0

with (ROOT / "SOURCE_SHA256.csv").open(encoding="utf-8-sig", newline="") as fh:
    records = list(csv.DictReader(fh))
assert len(records) == 20, len(records)
for record in records:
    source = ROOT / record["path_in_batch"]
    actual = hashlib.sha256(source.read_bytes()).hexdigest()
    assert actual == record["sha256"], (source, actual, record["sha256"])
    assert source.stat().st_size == int(record["size_bytes"])

zip_path = ROOT / "ROSEWOOD_BATCH_271_280_MANUAL_REVIEW.zip"
with ZipFile(zip_path) as z:
    assert z.testzip() is None, "ZIP CRC error"
    names = z.namelist()
    assert len(names) == 25 and len(set(names)) == 25, names
    assert sum(x.endswith(".jpg") for x in names) == 10
    assert sum(x.endswith(".png") for x in names) == 10
    assert set(names) == set(MANIFEST["zip_entries"])
    for record in records:
        path = record["path_in_batch"]
        assert hashlib.sha256(z.read(path)).hexdigest() == record["sha256"]

with (ROOT / "BATCH_271_280_MANUAL_VISUAL_REVIEW.csv").open(encoding="utf-8-sig", newline="") as fh:
    reviews = list(csv.DictReader(fh))
assert [int(x["index"]) for x in reviews] == list(range(271, 281))
assert all(x["review_status"] == "DEFERRED_VISUAL_MISMATCH" for x in reviews)
assert all(x["game_1to1_certified"] == "NO" for x in reviews)
print("PASS: 10 review records, 20 SHA-256 files, 25 ZIP CRC entries, no game approvals")
