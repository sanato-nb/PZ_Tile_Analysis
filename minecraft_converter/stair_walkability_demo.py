"""Tiny independent Minecraft Java 1.20.1 world to manually test 3+1 stairs.

This is deliberately NOT part of 31_46.tmx. The real map has no verified
stairs, and its PZW basement hint is not enough to build a physical stair.
"""
import argparse
from pathlib import Path
import zipfile
from converter import chunk,region_merge,level_dat
from floor_stair_stage import plan_three_step_run,write_stair_run

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--output",type=Path,required=True)
    args=p.parse_args()
    args.output.mkdir(parents=True,exist_ok=True)
    name="stairs_3plus1_walkability_demo"
    world=args.output/name
    blocks={}
    for x in range(16):
        for z in range(16):
            blocks[x,64,z]="minecraft:grass_block"
    # Walkable upper landing and open platform, no stairs under this platform.
    for x in range(5,13):
        for z in range(4,9):
            blocks[x,68,z]="minecraft:oak_planks"
            for y in range(65,68):
                blocks[x,y,z]="minecraft:stone_bricks"
    # This synthetic fixture exists only to test physical geometry,
    # NOT as a claim that 31_46 has these stair sprites.
    parts={(0,x,6) for x in (2,3,4)}
    floor={(1,5,6)}
    plan=plan_three_step_run(floor,parts,0,2,6,"E")
    assert write_stair_run(blocks,plan)==6
    region_merge(world/"region/r.0.0.mca",{(0,0):chunk(0,0,blocks,3465)})
    level_dat(world,310046,1,6,3465,level_name="STAIRS DEMO (not PZ map)")
    with zipfile.ZipFile(args.output/(name+".zip"),"w",zipfile.ZIP_DEFLATED) as archive:
        for path in sorted(world.rglob("*")):
            if path.is_file():
                archive.write(path,name+"/"+str(path.relative_to(world)))
    print("PASS demo staircase world with 3 vanilla stairs, 1 confirmed-in-fixture landing and 4 vertical blocks")

if __name__=="__main__":main()
