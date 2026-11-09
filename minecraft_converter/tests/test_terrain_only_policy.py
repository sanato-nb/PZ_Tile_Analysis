"""Terrain-only whitelist and synthetic object exclusion regression tests."""
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from converter import (
    TERRAIN_ONLY_MATERIALS, enforce_terrain_only_world,
    terrain_only_material, surface_block,
)

class TerrainOnlyPolicyTests(unittest.TestCase):
    def test_allowed_solid_ground_and_floor_states(self):
        expected=[
            "minecraft:grass_block","minecraft:stone","minecraft:dirt",
            "minecraft:farmland[moisture=7]",
            "minecraft:oak_planks","minecraft:light_gray_concrete",
            "minecraft:spruce_leaves[persistent=true]",
            "minecraft:oak_leaves[persistent=true]",
            "minecraft:spruce_log",
            "minecraft:grass","minecraft:wheat[age=7]",
            "minecraft:dead_bush",
            "minecraft:yellow_concrete","minecraft:yellow_terracotta",
        ]
        for state in expected:
            with self.subTest(state=state):
                self.assertTrue(terrain_only_material(state))
        self.assertEqual(len(TERRAIN_ONLY_MATERIALS),len(set(TERRAIN_ONLY_MATERIALS)))

    def test_reject_all_furniture_walls_poles_and_unverified_objects(self):
        prohibited=[
            "minecraft:light_blue_stained_glass", "minecraft:light_blue_carpet",
            "minecraft:oak_fence", "minecraft:oak_door", "minecraft:glass_pane",
            "minecraft:iron_bars", "minecraft:lantern", "minecraft:stone_wall",
            "minecraft:lightning_rod", "minecraft:oak_stairs[facing=north]",
            "minecraft:magenta_concrete", "minecraft:chest",
            "minecraft:beacon", "minecraft:iron_block", "minecraft:pink_wool",
            "minecraft:aircraft",
        ]
        for block in prohibited:
            with self.subTest(block=block):
                self.assertFalse(terrain_only_material(block))
                with self.assertRaisesRegex(ValueError, "non-terrain blocks"):
                    enforce_terrain_only_world({(0,0):{(0,64,0):block}})

    def test_mixed_valid_terrain_palette(self):
        world={
            (0,0):{
                (0,64,0):"minecraft:gray_concrete",
                (0,65,0):"minecraft:grass",
                (1,64,0):"minecraft:farmland[moisture=7]",
                (1,65,0):"minecraft:wheat[age=7]",
            },
            (1,0):{
                (16,64,0):"minecraft:polished_andesite",
                (16,65,0):"minecraft:spruce_log",
            },
        }
        self.assertTrue(enforce_terrain_only_world(world))

    def test_known_original_surface_mappings_are_allowed(self):
        fixtures={
            "blends_natural_01":[16,22,32,48,64,80,88],
            "blends_street_01":[16,32,48,64,80],
            "floors_exterior_street_01":[16],
            "floors_interior_tilesandwood_01":[5,12,41,42,43,50],
            "floors_interior_carpet_01":[2,47],
            "floors_exterior_tilesandstone_01":[0,1,3,5,7,80],
            "floor_carpet_motif":[0,1,2,3,7,12,13,15],
            "blends_natural_02":[0,7],
        }
        for family, indices in fixtures.items():
            for index in indices:
                with self.subTest(family=family,index=index):
                    block=surface_block(f"{family}/{index}",family)
                    self.assertTrue(terrain_only_material(block),block)
        self.assertEqual(surface_block("location_shop_mall_01/22",
                                       "location_shop_mall_01"),
                         "minecraft:polished_andesite")

if __name__=="__main__":
    unittest.main()
