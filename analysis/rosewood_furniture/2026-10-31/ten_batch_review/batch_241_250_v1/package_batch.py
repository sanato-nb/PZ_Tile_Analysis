#!/usr/bin/env python3
"""Generate reproducible image hashes, manifest and review ZIP for lane C 241-250."""
import csv, hashlib, io, json, pathlib, zipfile
ROOT = pathlib.Path(__file__).resolve().parent
DATA = json.loads((ROOT / "REVIEW_DATA.json").read_text(encoding="utf-8"))
assert DATA["range"] == [241, 250]
rows = DATA["items"]
assert [x["index"] for x in rows] == list(range(241,251))
assets = []
for row in rows:
    for pathkey, hashkey, sourcekey, kind in [
        ("card", "card_blob_sha1", "source_card", "PZ_MC_COMPARISON_CARD_REUSED"),
        ("pz_preview", "preview_blob_sha1", "source_preview", "PZ_COMPLETE_FURNITURE_PREVIEW_REUSED"),
    ]:
        p = pathlib.PurePosixPath(row[pathkey])
        f = ROOT / p
        assert f.is_file(), f
        b = f.read_bytes()
        git_hash = hashlib.sha1(b"blob " + str(len(b)).encode() + b"\0" + b).hexdigest()
        assert git_hash == row[hashkey], (p, git_hash, row[hashkey])
        assets.append(dict(path=str(p), source_repo_path=row[sourcekey],
                           source_type=kind, git_blob_sha1=git_hash,
                           sha256=hashlib.sha256(b).hexdigest(), size_bytes=len(b)))
assert len(assets) == 20
with (ROOT / "SOURCE_SHA256.csv").open("w", encoding="utf-8", newline="") as f:
    w = csv.DictWriter(f, fieldnames=["path", "source_repo_path", "source_type",
                                       "git_blob_sha1", "sha256", "size_bytes"])
    w.writeheader()
    w.writerows(assets)
texts = ["REVIEW_DATA.json", "BATCH_241_250_MANUAL_VISUAL_REVIEW.csv",
         "BATCH_241_250_DEFERRED_OTHER_MODS.csv", "README_KO.md",
         "INDEX.html", "verify_batch.py"]
names = sorted([x["path"] for x in assets] + texts + ["SOURCE_SHA256.csv", "MANIFEST.json"])
manifest = dict(schema_version=1, range=[241,250], lane="C",
                reviewed_count=10, conditional_count=0, deferred_count=10,
                game_certified_count=0, review_date="2026-11-02",
                source_branch=DATA["source_branch"],
                target_branch="work/rosewood-manual-batch25-241-250-20261102",
                source_image_count=20, comparison_jpg_count=10, pz_preview_png_count=10,
                new_blockbench_renders=0,
                review_method="Individual visual reinspection of existing PZ/MC comparison images; incomplete source JSON imports are not accepted as complete models",
                zip_entries=names, source_asset_sha1=[{"path":a["path"],"sha1":a["git_blob_sha1"]} for a in assets])
(ROOT / "MANIFEST.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")
zpath = ROOT / "ROSEWOOD_BATCH_241_250_REVIEW.zip"
with zipfile.ZipFile(zpath, "w") as z:
    for name in names:
        zi = zipfile.ZipInfo(name, (2026,11,2,12,0,0))
        zi.compress_type = zipfile.ZIP_DEFLATED
        zi.external_attr = (0o644 << 16)
        z.writestr(zi, (ROOT / name).read_bytes(), compresslevel=6)
digest = hashlib.sha256(zpath.read_bytes()).hexdigest()
(ROOT / "ZIP_SHA256.txt").write_text(f"{digest}  {zpath.name}\n", encoding="utf-8")
with zipfile.ZipFile(zpath) as z:
    assert z.testzip() is None
    assert sorted(z.namelist()) == names
print(f"Packaged {len(assets)} images, {len(names)} ZIP entries, ZIP SHA-256 {digest}")
