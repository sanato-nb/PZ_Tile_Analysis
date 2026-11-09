"""Regression tests for source-backed level floors and three-step stairs."""
import tempfile
import unittest
from pathlib import Path
from minecraft_converter.floor_stair_stage import (
    audit_source_floors,audit_pzw_basements,plan_three_step_run,write_stair_run)

def rec(level,key,layer="FloorOverlay",x=3,z=4):
    return {"level":level,"source_key":key,"layer":layer,"x":x,"z":z,
            "local_x":x,"local_y":z,"tile_properties":{}}

class Stage23Tests(unittest.TestCase):
    def test_upper_floor_not_roof_or_ceiling(self):
        objects=[
          rec(1,"ceilings_01/0"),rec(2,"roofs_03/55"),
          rec(1,"overlay_grime_floor_01/37"),
          rec(1,"floors_rugs_01/48"),
          rec(1,"floors_interior_tilesandwood_01/42",x=5),
          rec(2,"floors_interior_carpet_01/2",x=6),
        ]
        r=audit_source_floors(objects)
        self.assertEqual(len(r["floors"]),2)
        self.assertEqual(r["audit"]["nonfloor_tiles_by_level"]["1"]["ceiling"],1)
        self.assertEqual(r["audit"]["nonfloor_tiles_by_level"]["2"]["roof"],1)
        self.assertEqual(r["audit"]["confirmed_upper_lower_floor_total"],2)

    def test_stair_four_block_rise_only_if_source_confirmed(self):
        # Three lower-floor stair sprite parts, then existing upper floor landing.
        parts={(0,i,0) for i in range(3)}
        floors={(1,3,0)}
        plan=plan_three_step_run(floors,parts,0,0,0,"E")
        self.assertEqual([a["y"] for a in plan["parts"]],[65,66,67])
        self.assertEqual(plan["landing"]["y"],68)
        blocks={(3,68,0):"minecraft:oak_planks"}
        self.assertEqual(write_stair_run(blocks,plan),6)
        self.assertIn("stairs",blocks[(0,65,0)])
        self.assertEqual(blocks[(1,65,0)],"minecraft:oak_planks")
        self.assertEqual(blocks[(2,66,0)],"minecraft:oak_planks")

    def test_stair_rejects_missing_landing(self):
        parts={(0,i,0) for i in range(3)}
        with self.assertRaisesRegex(ValueError,"upper floor landing"):
            plan_three_step_run(set(),parts,0,0,0,"E")

    def test_stair_rejects_unsupported_sprite(self):
        parts={(0,i,0) for i in range(2)}
        with self.assertRaisesRegex(ValueError,"three stair pieces"):
            plan_three_step_run({(1,3,0)},parts,0,0,0,"E")

    def test_stair_rejects_upper_floor_over_treads(self):
        with self.assertRaisesRegex(ValueError,"opening"):
            plan_three_step_run({(1,3,0),(1,1,0)},
                                {(0,i,0) for i in range(3)},0,0,0,"E")

    def test_pzw_basement_is_metadata_not_built_floor(self):
        doc='''<world cellFormat="native-256"><cell x="31" y="46">
          <object group="Basement" x="72" y="119" width="12" height="10">
           <property name="StairDirection" value="W"/>
           <property name="StairX" value="1"/>
           <property name="StairY" value="0"/>
          </object></cell></world>'''
        with tempfile.TemporaryDirectory() as tmp:
            path=Path(tmp)/"map.pzw";path.write_text(doc)
            basements=audit_pzw_basements(path,31,46,7936,11776)
        self.assertEqual(len(basements),1)
        self.assertEqual(basements[0]["world_rect"]["x"],8008)
        self.assertEqual(basements[0]["stair_hint_global"]["z"],11895)
        self.assertFalse(basements[0]["is_verified_physical_basement"])

if __name__=="__main__":unittest.main()
