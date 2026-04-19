from world.blocks.block_export import *

GRID_HEIGHT = 150

class Biome:
    
    # layer classes
    surface_layer = Grass
    sub_surface_layer = Dirt
    deep_layer = Rock
    ultra_deep_layer = Rock

    # floor generation details
    start_floor_depth = 0
    max_deviation_floor_lvl = 3
    sub_surface_layer_depth = 2
    change_probability = 0.10

    # biome size details
    biome_base_size = 50

    # ore generation details
    iron_ore_min_depth = 9
    iron_ore_base_chance = 0.00071
    iron_ore_inc_chances_by_layer = 0.000005
    iron_ore_vein_min_size = 1
    iron_ore_vein_max_size = 6

    coal_ore_min_depth = 9
    coal_ore_base_chance = 0.00076
    coal_ore_inc_chances_by_layer = -0.000001
    coal_ore_vein_min_size = 2
    coal_ore_vein_max_size = 9

    gold_ore_min_depth = 41
    gold_ore_base_chance = 0.000169
    gold_ore_inc_chances_by_layer = (gold_ore_base_chance * 3) / (GRID_HEIGHT - gold_ore_min_depth)
    gold_ore_vein_min_size = 1
    gold_ore_vein_max_size = 6

    diamond_ore_min_depth = 43
    diamond_ore_base_chance = 0.000164
    diamond_ore_inc_chances_by_layer = (diamond_ore_base_chance * 3) / (GRID_HEIGHT - diamond_ore_min_depth)
    diamond_ore_vein_min_size = 1
    diamond_ore_vein_max_size = 4

    emerald_ore_min_depth = 23
    emerald_ore_base_chance = 0.0005
    emerald_ore_inc_chances_by_layer = -1 * emerald_ore_base_chance / 28
    emerald_ore_vein_min_size = 1
    emerald_ore_vein_max_size = 3

    mabelite_ore_min_depth = 29
    mabelite_ore_base_chance = 0.00005
    mabelite_ore_inc_chances_by_layer = 0.00000045
    mabelite_ore_vein_min_size = 1
    mabelite_ore_vein_max_size = 2

    dirt_vein_min_depth = start_floor_depth + sub_surface_layer_depth + 4
    dirt_vein_base_chance = 0.00305
    dirt_vein_inc_chances_by_layer = -0.000009
    dirt_vein_min_size = 3
    dirt_vein_max_size = 8

    gravel_vein_min_depth = start_floor_depth + sub_surface_layer_depth + 4
    gravel_vein_base_chance = 0.00275
    gravel_vein_inc_chances_by_layer = -0.000009
    gravel_vein_min_size = 3
    gravel_vein_max_size = 8

    sulfur_flakes_min_depth = start_floor_depth + sub_surface_layer_depth + 4
    sulfur_flakes_base_chance = 0.00008
    sulfur_flakes_inc_chances_by_layer = -1 * sulfur_flakes_base_chance / 20
    sulfur_flakes_vein_min_size = 1
    sulfur_flakes_vein_max_size = 3

    # cave generation details
    cave_start_odds = 0.0006
    max_cave_depth = 5
    water_cave_chance = 0.03
    saltpeter_chance = 0.018

    # object generation odds
    tree_chance = 0
    cactus_chance = 0
    lake_chance = 0
    small_bushes_chance = 0
    snow_man_chance = 0

    # structures
    recipe_burrow_chance = 0.0045

    @classmethod
    def terrainShape(cls):
        pass


class Forest(Biome):
    max_deviation_floor_lvl = 3
    dirt_depth = 2
    small_bushes_chance = 0.01
    tree_chance = 0.32
    water_cave_chance = 0.1

class Thin_Forest(Biome):
    max_deviation_floor_lvl = 3
    dirt_depth = 2
    small_bushes_chance = 0.06
    tree_chance = 0.1
    water_cave_chance = 0.05

class Plains(Biome):
    max_deviation_floor_lvl = 3
    dirt_depth = 2
    change_probability = 0.08
    small_bushes_chance = 0.03
    recipe_burrow_chance = Biome.recipe_burrow_chance * 1.25

class Tundra(Biome):
    surface_layer = Rock
    sub_surface_layer = Rock
    deep_layer = Rock

    max_deviation_floor_lvl = 4
    dirt_depth = 2
    change_probability = 0.2
    small_bushes_chance = 0.05

    iron_ore_min_depth = -3
    iron_ore_base_chance = 0.0008
    iron_ore_inc_chances_by_layer = 0.000005

    dirt_vein_min_depth = 5
    dirt_vein_base_chance = 0.00005
    dirt_vein_inc_chances_by_layer = -0.000009

    sulfur_flakes_base_chance = Biome.sulfur_flakes_base_chance * 6
    sulfur_flakes_inc_chances_by_layer = -1 * sulfur_flakes_base_chance / 20

    recipe_burrow_chance = Biome.recipe_burrow_chance * 3

class Desert(Biome):
    surface_layer = Sand
    sub_surface_layer = Sand
    deep_layer = Rock

    max_deviation_floor_lvl = 3
    dirt_depth = 6
    change_probability = 0.08
    cactus_chance = 0.12

    dirt_vein_min_depth = Biome.start_floor_depth + max_deviation_floor_lvl + 4
    dirt_vein_inc_chances_by_layer = Biome.dirt_vein_inc_chances_by_layer * 1.01

class Lake(Biome):
    surface_layer = Sand
    sub_surface_layer = Sand

    start_floor_depth = 4
    max_deviation_floor_lvl = 2
    change_probability = 0.1
    lake_chance = 1
    water_cave_chance = 0.4

    iron_ore_base_chance = Biome.iron_ore_base_chance * 1.05
    dirt_vein_min_depth = start_floor_depth + max_deviation_floor_lvl + 4
    dirt_vein_inc_chances_by_layer = Biome.dirt_vein_inc_chances_by_layer * 1.01

    recipe_burrow_chance = 0

class Glacier(Biome):
    surface_layer = Snow_Block
    sub_surface_layer = Ice
    deep_layer = Frozen_Rock
    ultra_deep_layer = Rock

    biome_base_size = Biome.biome_base_size * 2
    sub_surface_layer_depth = 7
    start_floor_depth = 4
    max_deviation_floor_lvl = 2
    change_probability = 0.08
    lake_chance = 0
    water_cave_chance = 0.1
    dirt_vein_base_chance = 0
    snow_man_chance = 0.018

    iron_ore_min_depth = 12
