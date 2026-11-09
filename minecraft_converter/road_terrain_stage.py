#!/usr/bin/env python3
"""Source-indexed road/low-vegetation preview stage for the 31_46 Java world.

The identities below were checked against original B42 sprite PNGs and the
actual TMX key occurrences. Minecraft blocks/textures are visual PROXIES.
No guessed water, walls, stairs, upper floors or jumbo trees are added.
"""
import collections
import json
import struct
import zipfile
import zlib

# Original 2x/street_trafficlines_01.png: these four tiles contain thin
# YELLOW paint; other atlas indices have different forms and are excluded.
# Orientation is a deliberately provisional Minecraft top-down approximation.
ROAD_LANE = {
    16: "minecraft:yellow_concrete",
    18: "minecraft:yellow_terracotta",
    20: "minecraft:orange_concrete",
    22: "minecraft:orange_terracotta",
}
# 2x/street_trafficlines_curb_yellow_faded.png: only IDs present in 31_46.
# Multiple source pieces can share one road cell: emit one flush surface block,
# while preserving ALL raw source entries in source_placements.jsonl.gz.
CURB_IDS = frozenset((3, 4, 5, 24, 60, 101, 136, 137, 138, 145, 146))
CURB_VERTICAL = frozenset((60, 101, 24, 145, 146))
GRASS_LIVE = frozenset(
    i for start in (0, 8, 16, 24, 32, 40) for i in range(start, start + 6)
)
GRASS_DRY = frozenset(
    i for start in (48, 56, 64) for i in range(start, start + 6)
)
GROUND_COVER = frozenset((18, 19, 21, 22, 23))
ALLOWED_GREEN_SOIL = frozenset((
    "minecraft:grass_block", "minecraft:moss_block",
    "minecraft:podzol", "minecraft:coarse_dirt",
))
ALLOWED_DRY_SOIL = frozenset((
    "minecraft:coarse_dirt", "minecraft:podzol", "minecraft:dirt",
))
# Unused vanilla blocks are reused ONLY for the road-marked surface.
# World-local resources.zip replaces their block textures, leaving road Y=64
# and other block textures in Minecraft unchanged. Without resource pack these
# blocks appear as solid colored vanilla placeholders.
ROAD_PACK_TEXTURES = {
    "yellow_concrete": ("vertical", False),
    "yellow_terracotta": ("vertical", True),
    "orange_concrete": ("horizontal", False),
    "orange_terracotta": ("horizontal", True),
    "brown_concrete": ("curb_vertical", True),
    "brown_terracotta": ("curb_horizontal", True),
}

def _split_key(source_key):
    family, sep, raw = source_key.partition("/")
    if not sep or not raw.isdigit():
        return "", -1
    return family, int(raw)

def road_overlay(source_key):
    """(category, blockstate) for photo-checked road paint candidates."""
    family, index = _split_key(source_key)
    if family == "street_trafficlines_01":
        block = ROAD_LANE.get(index)
        if block:
            return "lane", block
    if family == "street_trafficlines_curb_yellow_faded" and index in CURB_IDS:
        block = "minecraft:brown_concrete" if index in CURB_VERTICAL else "minecraft:brown_terracotta"
        return "faded_yellow_curb", block
    return None

def ground_detail(source_key):
    """Vanilla low-profile approximations, not certified exact sprite models."""
    family, index = _split_key(source_key)
    if family == "blends_grassoverlays_01":
        if index in GRASS_LIVE:
            return "green_grass", "minecraft:grass"
        if index in GRASS_DRY:
            return "dry_grass", "minecraft:dead_bush"
    if family == "vegetation_groundcover_01" and index in GROUND_COVER:
        return "groundcover", "minecraft:grass"
    return None

def collect_surface_overlays(records, floor, surface_block):
    """Return source-backed road map, small plant map and provenance counters.

    Only Level 0, original overlay layers, and correct original floor families
    are accepted. The caller checks Y65 occupied positions AFTER placing
    furniture, trees, shrubs, and wheat, so vegetation cannot overwrite them.
    """
    road, plants = {}, {}
    counts = collections.Counter()
    road_kinds = {}
    for item in records:
        if item["level"] != 0 or item["layer"] == "Floor":
            continue
        key = item["source_key"]
        pos = (item["local_x"], item["local_y"])
        ground = floor.get(pos)
        paint = road_overlay(key)
        if paint:
            counts["road_source_records"] += 1
            if ground is None or ground[1] != "blends_street_01":
                counts["road_rejected_floor"] += 1
                continue
            kind, block = paint
            # Prefer a lane over curb if such source pieces ever overlap.
            if pos not in road or (kind == "lane" and road_kinds[pos] != "lane"):
                road[pos] = (block, key)
                road_kinds[pos] = kind
            continue
        plant = ground_detail(key)
        if plant:
            counts["low_vegetation_source_records"] += 1
            if ground is None or ground[1] != "blends_natural_01":
                counts["low_vegetation_rejected_floor"] += 1
                continue
            kind, block = plant
            allowed = ALLOWED_DRY_SOIL if kind == "dry_grass" else ALLOWED_GREEN_SOIL
            if surface_block(*ground) not in allowed:
                counts["low_vegetation_rejected_soil"] += 1
                continue
            if pos not in plants:
                plants[pos] = (block, key, kind)
            else:
                counts["low_vegetation_duplicate_cell"] += 1
    counts["road_unique_cells"] = len(road)
    counts["lane_cells"] = sum(road_kinds[p] == "lane" for p in road)
    counts["curb_cells"] = sum(road_kinds[p] == "faded_yellow_curb" for p in road)
    counts["low_vegetation_eligible_cells"] = len(plants)
    return road, plants, dict(sorted(counts.items()))

def _png_chunk(kind, body):
    return (struct.pack(">I", len(body)) + kind + body
            + struct.pack(">I", zlib.crc32(kind + body) & 0xffffffff))

def road_texture_png(orientation, faded):
    """Produce a deterministic 16x16 RGB PNG (asphalt and thin yellow paint)."""
    scanlines = []
    for z in range(16):
        pixels = bytearray()
        for x in range(16):
            # A little deterministic asphalt variation, no randomness.
            gray = 79 + ((x * 7 + z * 3) % 5) - 2
            rgb = (gray, gray + 2, gray + 3)
            if orientation == "vertical":
                mark = x in (7, 8)
            elif orientation == "horizontal":
                mark = z in (7, 8)
            elif orientation == "curb_vertical":
                mark = x in (1, 2)
            elif orientation == "curb_horizontal":
                mark = z in (1, 2)
            else:
                raise ValueError("Invalid road texture orientation")
            if mark:
                if faded and (x * 3 + z * 5) % 7 < 3:
                    rgb = (163, 153, 77)
                else:
                    rgb = (236, 200, 42)
            pixels.extend(rgb)
        scanlines.append(b"\x00" + bytes(pixels))
    ihdr = struct.pack(">IIBBBBB", 16, 16, 8, 2, 0, 0, 0)
    return (b"\x89PNG\r\n\x1a\n" + _png_chunk(b"IHDR", ihdr)
            + _png_chunk(b"IDAT", zlib.compress(b"".join(scanlines), 9))
            + _png_chunk(b"IEND", b""))

def write_world_road_resource_pack(world):
    """Add a WORLD-LOCAL resource pack; no global texture pack modification."""
    path = world / "resources.zip"
    path.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(path, "w", zipfile.ZIP_DEFLATED) as archive:
        archive.writestr("pack.mcmeta", json.dumps({
            "pack": {
                "pack_format": 15,
                "description": "PZ B42 31_46 preview: flush yellow-road-line proxies"
            }
        }, sort_keys=True))
        for name, (orientation, faded) in sorted(ROAD_PACK_TEXTURES.items()):
            archive.writestr(
                "assets/minecraft/textures/block/" + name + ".png",
                road_texture_png(orientation, faded)
            )
    with zipfile.ZipFile(path) as archive:
        assert archive.testzip() is None
    return path
