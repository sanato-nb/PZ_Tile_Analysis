# Project Zomboid B42 → Minecraft: 31_46 preview converter

**Status: photo-audited farm/vegetation preview, NOT a completed reconstruction.**
The source geometry is real. Several frequently used terrain/crop indices are now matched against the actual PNG atlas;
other floor families remain provisional, not certified per-sprite mappings. Do not merge with a playthrough save.

## Verified original

* TMX: B4220.3_MapExport_256/tmx/31_46.tmx (256×256)
* World: B4220.3_MapExport_256/Kentucky.pzw (native-256, origin 0,0, cell 31,46)
* Global Minecraft bounds: X 7936–8191, Z 11776–12031.
* Level 0 surface Y=64. Dirt Y=63–62; stone Y=61–57.
* Source: 413 tilesets, 22 layers, seven levels with data (0–6).
* 131,341 nonzero source placement records; 65,536 Level 0 Floor cells.

## Run

Requires Python 3.9+ and no external Python packages.

~~~sh
python minecraft_converter/converter.py \
  --tmx B4220.3_MapExport_256/tmx/31_46.tmx \
  --pzw B4220.3_MapExport_256/Kentucky.pzw \
  --v259-html floorplan/current/v259_floorplan.html \
  --output minecraft_converter/output \
  --preview-world --data-version 3465
~~~

DataVersion 3465 = Minecraft Java 1.20.1 **disposable testing target**.
The final game version and mod loader are still undecided.

## Files

* 31_46_preview_world.zip — real Java world directory, level.dat + Anvil region.
* report.json — generation counts and limits.
* source_placements.jsonl.gz — EVERY nonzero GID, layer, floor, position,
  candidate ID and available v259 source properties.
* furniture_parts.json — source-backed furniture/appliance tile PARTS,
  not confirmed complete object instances.
* edges.json — four boundary strips, for future neighboring TMX comparison.
* warnings.csv — unresolved ground identities and ambiguous furniture candidates.

The GitHub Actions workflow pz-minecraft-31-46-preview.yml validates
the original tile counts, 256 chunks, and ZIP contents, then uploads the result.

## Implemented in this preview

Verified global coordinates, original TMX CSV layer parsing, lossless placement
logging, v259 candidate metadata, conservative Level 0 surface preview,
2 dirt + 5 stone below surface, visually verified dirt/furrow/green terrain indices,
17,571 mature wheat plants and 7,034 dry stalks at their original source coordinates,
172 conifer sprites converted to vanilla spruce and 261 shrubs rendered with vanilla leaves,
road/field boundary leaf clipping, family-whitelisted furniture placeholders,
void world / plains biome / fixed daytime / clear weather / creative mode /
disabled natural mob spawning, and real Java Anvil chunks.

## Still deferred, NOT presented as complete

Full original sprite-level material certification; water and underwater geometry;
road textures; 45 unverified jumbo tree sprites (missing source PNG);
fully modeled trees/crops; verified upper-floor
surfaces and walkable stairs; exact full-model furniture instance matching;
collision model geometry; review-map UI; chunk checkpoints; protected world
replacement; in-game launch verification.

Important: v259 furniture candidates also match farmland plants, vegetation,
doors, windows, and external installations. They must NOT all receive furniture
placeholder blocks. Only source families starting with furniture_, appliances_,
fixtures_counters_, fixtures_bathroom_, or fixtures_sinks_ receive provisional
furniture markers. Every excluded record is still in the source archive.

This work is isolated on branch work/minecraft-31-46-preview-20261108.
Neither original TMX/PZW data nor the v259 source is modified.

## Screenshot comparison correction (2026-11-09)

The first preview had mapped the entire blends_natural_01 family to grass,
erasing large brown plowed fields and golden wheat fields seen in the TileZed
screenshot. Inspecting the repository's original 2x PNG atlases established:

* blends_natural_01/16–23: green ground; /32–39: dark green ground;
  /48–55: dried yellow/olive ground; /64–71: exposed soil;
  /80–87: cultivated furrowed soil.
* vegetation_farm_01/0–5: mature wheat, 17,571 unique Level-0 coordinates;
  /32–39: dried stalks, 7,034 unique Level-0 coordinates.
* vegetation_trees_01/8–11: conifers, 172 placements; vegetation_foliage_01/8–14:
  shrubs, 261 placements. Canopies are clipped at mapped roads/buildings/crops.
* jumbo_tree_01 has 45 occurrences but the corresponding source PNG has not
  been verified in the stored tiles, so models are intentionally deferred.

Vanilla Java crops and foliage are **visual proxies**, not exact imported
Zomboid models. randomTickSpeed is disabled to keep the preview stable.
The changes to surface mapping and world generation are automatically exercised
by the GitHub Actions workflow; a Minecraft client gameplay test is still needed.

## Stage 2 & 3: floors and stairs (2026-11-09)

The source was inspected against the actual original PNG atlases. Level 0
interior floor mapping now distinguishes individual source sprite IDs:
- `floors_interior_tilesandwood_01/5`: white checkered tiles → polished diorite proxy
- `.../12`: pale tiles → smooth sandstone
- `.../41`: dark wood → dark oak planks
- `.../42`: light wood → birch planks
- `.../43`: brown wood → spruce planks
- `.../50`: golden wood tile → oak planks
- `floors_interior_carpet_01/2`: dark gray carpet → gray wool
- `.../47`: brown carpet → brown wool

**Actual TMX audit:** this 31_46 has 65,536 ground-level Floor cells,
but **zero proven floor tiles on Level 1–6**. Level 1 primarily contains
ceilings and roofs, not a confirmed second-story floor. There are also
**zero** `fixtures_stairs_01` or escalator placements in the source TMX.
Do not fabricate upper floors from ceilings or roof pixels.

The original `Kentucky.pzw` has a **Basement** metadata region:
local rectangle (72,119), width 12 and depth 10, corresponding to global
X=8008, Z=11895; it stores StairDirection=W, StairX=1, StairY=0,
Access=ba_exterior_west_northside_06. This alone does NOT supply any
negative-level basement floor tiles or reliable 3D stair geometry.
Its reference is saved verbatim in `floor_stair_audit.json`; nothing
is carved out of the ground until the actual basement building is verified.

A safe stair builder has been added to `floor_stair_stage.py`:
it requires three actual source stair parts, a confirmed landing floor
one level above and no obstructing upper floor at the stairwell. Only then
can it write three vanilla stair blocks at Y+1, Y+2, Y+3, with the landing
at Y+4. It rejects absent or conflicting inputs; it does NOT force any
stairs onto the real 31_46 world.

For physical testing without inventing map geography, a wholly separate
`stairs_3plus1_walkability_demo.zip` world was generated. This demo is
synthetic and **not part of the Zomboid map**. Its ZIP and chunk NBT
pass automated checks, but Minecraft player movement remains to be
checked manually in-game.

Artifacts:
- `previews/31_46_preview_world.zip`: corrected real-world Level-0 flooring.
- `previews/31_46_floor_stair_audit.json`: source-backed level/roof/stair/basement report.
- `previews/stairs_3plus1_walkability_demo.zip`: separate 3+1 stair demo world.
- Automated tests: `tests/test_floor_stair_stage.py` (six cases).

Still to do: obtain original negative-level basement building geometry,
actual above-ground stair sprites and Codex models in later TMX regions,
before staircase/upper-floor placement can be validated in the real map.
