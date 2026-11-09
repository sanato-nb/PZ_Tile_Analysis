"""Source-ID, guardrail, deterministic road-pack tests. No TMX fixture needed."""
import io
import json
import struct
import sys
import unittest
import zipfile
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from road_terrain_stage import (
    road_overlay, ground_detail, collect_surface_overlays,
    road_texture_png, write_world_road_resource_pack, ROAD_PACK_TEXTURES
)

def rec(key, x=3, z=5, layer="FloorOverlay", level=0):
    return {"source_key": key, "local_x": x, "local_y": z,
            "level": level, "layer": layer}

def surface(key, family):
    return {
        "blends_natural_01": "minecraft:grass_block",
        "blends_street_01": "minecraft:gray_concrete",
    }[family]

class SourceMappingTests(unittest.TestCase):
    def test_only_four_road_lane_ids(self):
        self.assertEqual([n for n in range(128)
                          if road_overlay(f"street_trafficlines_01/{n}")],
                         [16, 18, 20, 22])
        self.assertIsNone(road_overlay("street_trafficlines_01/0"))
        self.assertIsNone(road_overlay("fixtures_doors_01/16"))

    def test_grass_and_groundcover_are_positively_whitelisted(self):
        self.assertEqual(ground_detail("blends_grassoverlays_01/0"),
                         ("green_grass", "minecraft:grass"))
        self.assertEqual(ground_detail("blends_grassoverlays_01/69"),
                         ("dry_grass", "minecraft:dead_bush"))
        self.assertEqual(ground_detail("vegetation_groundcover_01/23"),
                         ("groundcover", "minecraft:grass"))
        self.assertIsNone(ground_detail("vegetation_groundcover_01/0"))
        self.assertIsNone(ground_detail("blends_grassoverlays_01/6"))

    def test_floor_level_and_road_priority(self):
        records = [
            rec("street_trafficlines_curb_yellow_faded/60"),
            rec("street_trafficlines_curb_yellow_faded/101", layer="FloorOverlay2"),
            rec("street_trafficlines_01/16"),
            rec("street_trafficlines_01/18", x=1),
            rec("street_trafficlines_01/20", x=9, level=1),
            rec("blends_grassoverlays_01/0", x=1, z=1),
            rec("vegetation_groundcover_01/18", x=1, z=1),
        ]
        floors = {(3,5):("blends_street_01/80","blends_street_01"),
                  (1,5):("blends_natural_01/16","blends_natural_01"),
                  (1,1):("blends_natural_01/16","blends_natural_01")}
        roads, plants, audit = collect_surface_overlays(records, floors, surface)
        self.assertEqual(roads[(3,5)][0], "minecraft:yellow_concrete")
        self.assertNotIn((1,5), roads)
        self.assertEqual(len(roads), 1)
        self.assertEqual(len(plants), 1)
        self.assertEqual(audit["road_source_records"], 4)
        self.assertEqual(audit["road_rejected_floor"], 1)
        self.assertEqual(audit["low_vegetation_duplicate_cell"], 1)

    def test_pack_is_valid_and_deterministic(self):
        import tempfile
        with tempfile.TemporaryDirectory() as folder:
            target=Path(folder)
            path=write_world_road_resource_pack(target)
            first=path.read_bytes()
            write_world_road_resource_pack(target)
            self.assertEqual(first, path.read_bytes())
            with zipfile.ZipFile(io.BytesIO(first)) as z:
                self.assertIsNone(z.testzip())
                self.assertEqual(json.loads(z.read("pack.mcmeta"))["pack"]["pack_format"],15)
                self.assertEqual(len(z.namelist()),len(ROAD_PACK_TEXTURES)+1)
                for name in ROAD_PACK_TEXTURES:
                    data=z.read("assets/minecraft/textures/block/"+name+".png")
                    self.assertEqual(data[:8], b"\x89PNG\r\n\x1a\n")
                    self.assertEqual(struct.unpack(">II",data[16:24]),(16,16))
                self.assertNotEqual(road_texture_png("vertical",False),
                                    road_texture_png("horizontal",False))
if __name__=="__main__":
    unittest.main()
