#!/usr/bin/env python3
"""Offline structural verification of the cross-branch Rosewood 357 review index.

Does NOT independently rehash binary JPG/ZIP evidence or certify in-game behavior.
"""
from __future__ import annotations
import csv
import json
from collections import Counter
from pathlib import Path

ROOT = Path("analysis/rosewood_furniture/2026-10-31/ten_batch_review/FINAL_QA_357_20261102")

def read_jsonl(name: str) -> list[dict]:
    return [json.loads(line) for line in (ROOT / name).read_text(encoding="utf-8").splitlines() if line.strip()]

def read_csv(name: str) -> list[dict]:
    with (ROOT / name).open(encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))

def main() -> None:
    files = ["NORMALIZED_001_120.jsonl", "NORMALIZED_121_240.jsonl", "NORMALIZED_241_357.jsonl"]
    rows = sorted((row for file in files for row in read_jsonl(file)), key=lambda x: x["index"])
    manifests = [m for file in ["MANIFEST_AUDIT_001_120.jsonl", "MANIFEST_AUDIT_121_240.jsonl", "MANIFEST_AUDIT_241_357.jsonl"] for m in read_jsonl(file)]
    summary = json.loads((ROOT / "QA_SUMMARY.json").read_text(encoding="utf-8"))
    master = read_csv("MASTER_INDEX_001_357.csv")
    deferred = read_csv("DEFERRED_BACKLOG_289.csv")
    conditional = read_csv("CONDITIONAL_RECHECK_068.csv")
    batches = read_csv("BATCH_STATUS_36.csv")
    categories = read_csv("CATEGORY_PRIORITY.csv")
    ids = [r["index"] for r in rows]
    assert ids == list(range(1, 358)), "missing, duplicate or unordered index"
    assert len(rows) == len(master) == 357
    assert len(manifests) == len(batches) == 36
    assert sum(int(c["total"]) for c in categories) == 357
    assert sum(int(c["deferred"]) for c in categories) == 289
    assert sum(int(c["conditional"]) for c in categories) == 68
    for c in categories:
        subset = [r for r in rows if r["pz_name"] == c["category"]]
        assert len(subset) == int(c["total"])
        assert sum(r["status_class"] == "DEFER" for r in subset) == int(c["deferred"])
        assert sum(r["status_class"] == "CONDITIONAL" for r in subset) == int(c["conditional"])
    assert len(set(r["pr"] for r in rows)) == 36
    assert len(set(r["source_csv_blob_sha"] for r in rows)) == 36
    assert all(len(r["source_csv_blob_sha"]) == 40 for r in rows)
    counts = Counter(r["status_class"] for r in rows)
    assert counts == Counter({"CONDITIONAL": 68, "DEFER": 289}), counts
    assert len(conditional) == 68 and len(deferred) == 289
    assert {int(x["index"]) for x in conditional} == {r["index"] for r in rows if r["status_class"] == "CONDITIONAL"}
    assert {int(x["index"]) for x in deferred} == {r["index"] for r in rows if r["status_class"] == "DEFER"}
    for r, m in zip(rows, master):
        assert int(m["index"]) == r["index"]
        assert int(m["pr"]) == r["pr"]
        assert m["status_class"] == r["status_class"]
        assert m["source_csv_blob_sha"] == r["source_csv_blob_sha"]
    assert not any(str(r.get(k, "")).strip().lower() in ("yes", "true", "1") for r in rows for k in ("exact_1_to_1_approved", "world_replacement_approved", "game_verified"))
    assert all(b["pr_state"] == "open" and b["draft"] == "true" and not b["merged_at"] for b in batches)
    assert all(b["manifest_check"] == "CONSISTENT_OR_NOT_SPECIFIED" for b in batches)
    assert sum(int(b["rows"]) for b in batches) == 357
    assert sum(int(b["conditional"]) for b in batches) == 68
    assert sum(int(b["deferred"]) for b in batches) == 289
    assert len({int(b["pr"]) for b in batches}) == 36
    assert len({m["range"] for m in manifests}) == 36
    for b in batches:
        assert any(m["range"] == b["range"] and str(m["pr"]) == b["pr"] for m in manifests)
        assert len(b["manifest_blob_sha"]) == 40
        assert len(b["review_csv_blob_sha"]) == 40
    assert summary["scope"]["unique"] == 357 and not summary["scope"]["missing"] and not summary["scope"]["duplicates"]
    assert summary["verdicts"]["conditional"] == 68 and summary["verdicts"]["deferred"] == 289
    assert summary["verdicts"]["approved"] == {"exact_1to1": 0, "world": 0, "game": 0}
    assert summary["ci"]["success"] == 32 and len(summary["ci"]["no_run"]) == 4
    print("PASS: 357 unique records, 36 PR/manifests, 68 conditional, 289 deferred, 0 approved.")
    print("NOTE: binary JPG/ZIP SHA-256 and CRC32 are not independently recomputed here.")

if __name__ == "__main__":
    main()
