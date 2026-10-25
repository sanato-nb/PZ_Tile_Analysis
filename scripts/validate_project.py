#!/usr/bin/env python3
"""Validate the canonical handoff state without touching source assets."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STATE = ROOT / "PROJECT_STATE.json"

def validate(state):
    errors = []
    if state.get("schema_version") != 1:
        errors.append("Unsupported PROJECT_STATE schema_version")
    if state.get("repository") != "sanato-nb/PZ_Tile_Analysis":
        errors.append("Unexpected repository")
    scope = state.get("scope", {})
    total = scope.get("unique_tiles")
    if not isinstance(total, int) or total <= 0:
        errors.append("scope.unique_tiles must be a positive integer")
        total = 0
    base = state.get("baselines", {})
    for name in ("v36", "v37_to_v46"):
        block = base.get(name, {})
        observed = block.get("observation_records")
        candidate = block.get("provisional_identity_candidates")
        if not isinstance(observed, int) or not 0 <= observed <= total:
            errors.append(f"{name}: invalid observation_records")
        if not isinstance(candidate, int) or not 0 <= candidate <= total:
            errors.append(f"{name}: invalid provisional_identity_candidates")
        if isinstance(observed, int) and isinstance(candidate, int) and candidate > observed:
            errors.append(f"{name}: candidates cannot exceed observations")
    reconciliation = state.get("reconciliation", {})
    merged = reconciliation.get("merged_unique_observed")
    verified = reconciliation.get("status") == "VERIFIED"
    if not verified and (merged is not None or reconciliation.get("merged_unique_candidates") is not None):
        errors.append("Unverified merged totals must stay null")
    if verified:
        candidates = reconciliation.get("merged_unique_candidates")
        overlap = reconciliation.get("v36_v46_overlap_count")
        if not all(isinstance(v, int) for v in (merged, candidates, overlap)):
            errors.append("VERIFIED merge requires integer overlap, observed and candidate totals")
        elif not (0 <= candidates <= merged <= total):
            errors.append("Invalid verified merged totals")
        elif merged != sum(base[n]["observation_records"] for n in ("v36", "v37_to_v46")) - overlap:
            errors.append("Merged total does not agree with overlap")
        if not reconciliation.get("merged_db_repo_path"):
            errors.append("VERIFIED merge requires a DB repository path (or change the schema with provenance)")
    if state.get("repository_visibility") != "public":
        errors.append("Repository expected to remain public")
    return errors

def main():
    data = json.loads(STATE.read_text(encoding="utf-8"))
    problems = validate(data)
    if problems:
        for problem in problems:
            print("ERROR:", problem)
        raise SystemExit(1)
    print("PROJECT_STATE.json validated. Reconciliation:", data["reconciliation"]["status"])

if __name__ == "__main__":
    main()
