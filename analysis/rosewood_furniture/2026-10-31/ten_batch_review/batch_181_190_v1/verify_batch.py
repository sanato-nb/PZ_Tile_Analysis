#!/usr/bin/env python3
"""Verify independent Rosewood batch 181-190 without claiming in-game certification."""
import csv
import hashlib
import json
from pathlib import Path
import zipfile

ROOT = Path(__file__).resolve().parent
EXPECTED = list(range(181, 191))

def read_csv(name):
    with (ROOT / name).open("r", encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))

def main():
    review = read_csv("BATCH_181_190_MANUAL_VISUAL_REVIEW.csv")
    deferred = read_csv("BATCH_181_190_DEFERRED_OTHER_MODS.csv")
    hashes = read_csv("SOURCE_SHA256.csv")
    manifest = json.loads((ROOT / "MANIFEST.json").read_text(encoding="utf-8"))
    assert [int(r["index"]) for r in review] == EXPECTED, "review range/duplicate error"
    assert [int(r["index"]) for r in deferred] == EXPECTED, "deferred range/duplicate error"
    assert all(r["review_status"].startswith("DEFER") for r in review), "incorrect approval"
    assert all(r["exact_1to1_approved"] == "NO" and r["approved_for_world_replacement"] == "NO" for r in review)
    assert manifest["count"] == 10 and manifest["deferred"] == 10 and manifest["in_game_1to1_certified"] == 0
    assert manifest["new_blockbench_renders"] == 0
    assert len(list((ROOT / "cards").glob("*_PZ_MC.jpg"))) == 10
    assert len(list((ROOT / "pz_previews").glob("*.png"))) == 10
    assert (ROOT / "alternatives/189_macaws_dark_oak_double_wardrobe.png").is_file()
    assert len(hashes) == 11
    for row in hashes:
        path = ROOT / row["path"]
        assert path.is_file(), row["path"]
        data = path.read_bytes()
        assert len(data) == int(row["size_bytes"]), row["path"]
        assert hashlib.sha256(data).hexdigest() == row["sha256"], row["path"]
    archive = ROOT / "ROSEWOOD_BATCH_181_190_REVIEW.zip"
    with zipfile.ZipFile(archive) as z:
        assert len(z.namelist()) == 16
        assert z.testzip() is None, "CRC failure"
        for name in z.namelist():
            assert z.read(name) == (ROOT / name).read_bytes(), name
    print("PASS: 10/10 reviewed, 10/10 deferred, 11/11 SHA-256, 16/16 ZIP CRC, 0 game approvals")

if __name__ == "__main__":
    main()
