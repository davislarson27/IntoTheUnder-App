from blocks import *

class Biome: #generic biome made so that not every type needs to be added - basicallyl 0's for everything
    
    # layer classes
    surface_layer = Grass
    sub_surface_layer = Dirt
    deep_layer = Rock
    ultra_deep_layer = Rock

    # floor generation dtails
    start_floor_depth = 13
    max_deviation_floor_lvl = 3
    sub_surface_layer_depth = 2
    change_probability = 0.10

    #ore generation details
    iron_ore_min_depth = 22
    iron_ore_base_chance = 0.00071
    iron_ore_inc_chances_by_layer = 0.000005
    iron_ore_vein_min_size = 1
    iron_ore_vein_max_size = 6

    coal_ore_min_depth = 22
    coal_ore_base_chance = 0.00076
    coal_ore_inc_chances_by_layer = -0.000001
    coal_ore_vein_min_size = 2
    coal_ore_vein_max_size = 9

    diamond_ore_min_depth = 56
    diamond_ore_base_chance = 0.000164
    diamond_ore_inc_chances_by_layer = (diamond_ore_base_chance * 3) / (100 - diamond_ore_min_depth)
    diamond_ore_vein_min_size = 1
    diamond_ore_vein_max_size = 4

    emerald_ore_min_depth = 36
    emerald_ore_base_chance = 0.0005
    emerald_ore_inc_chances_by_layer = -1 * emerald_ore_base_chance / 28 # means that emerald only spawns between y = 36 and 64
    emerald_ore_vein_min_size = 1
    emerald_ore_vein_max_size = 3

    mabelite_ore_min_depth = 42
    mabelite_ore_base_chance = 0.00005
    mabelite_ore_inc_chances_by_layer = 0.00000045
    mabelite_ore_vein_min_size = 1
    mabelite_ore_vein_max_size = 2

    dirt_vein_min_depth = start_floor_depth + sub_surface_layer_depth + 2
    dirt_vein_base_chance = 0.00305
    dirt_vein_inc_chances_by_layer = -0.000009
    dirt_vein_min_size = 3
    dirt_vein_max_size = 8

    gravel_vein_min_depth = start_floor_depth + sub_surface_layer_depth + 4
    gravel_vein_base_chance = 0.00275
    gravel_vein_inc_chances_by_layer = -0.000009
    gravel_vein_min_size = 3
    gravel_vein_max_size = 8


    # cave generation details
    cave_start_odds = 0.0006
    max_cave_depth = 5
    water_cave_chance = 0.03


    # object generation odds
    tree_chance = 0
    cactus_chance = 0
    lake_chance = 0
    small_bushes_chance = 0
    snow_man_chance = 0



class Forest(Biome):
    max_deviation_floor_lvl = 3
    dirt_depth = 2
    small_bushes_chance = 0.01

    tree_chance = 0.35

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


class Tundra(Biome):
    # layer classes
    surface_layer = Rock
    sub_surface_layer = Rock
    deep_layer = Rock

    max_deviation_floor_lvl = 4
    dirt_depth = 2
    change_probability = 0.2

    small_bushes_chance = 0.05

    # increased iron at all depths + decreased depth requirements
    iron_ore_min_depth = 10
    iron_ore_base_chance = 0.0008
    iron_ore_inc_chances_by_layer = 0.000005


    dirt_vein_min_depth = 18
    dirt_vein_base_chance = 0.00005
    dirt_vein_inc_chances_by_layer = -0.000009



class Desert(Biome):
    # layer classes
    surface_layer = Sand
    sub_surface_layer = Sand
    deep_layer = Rock

    max_deviation_floor_lvl = 3
    dirt_depth = 6
    change_probability = 0.08

    cactus_chance = 0.12

    dirt_vein_min_depth = Biome.start_floor_depth + max_deviation_floor_lvl + 4
    dirt_vein_inc_chances_by_layer = Biome.dirt_vein_inc_chances_by_layer * 1.01 # slight decrease in deep dirt (balances late start)


class Lake(Biome):
    surface_layer = Sand
    sub_surface_layer = Sand

    start_floor_depth = 17

    max_deviation_floor_lvl = 2
    change_probability = 0.1

    lake_chance = 1

    water_cave_chance = 0.4


    iron_ore_base_chance = Biome.iron_ore_base_chance * 1.05 #slight increase of chances to get iron
    dirt_vein_min_depth = start_floor_depth + max_deviation_floor_lvl + 4
    dirt_vein_inc_chances_by_layer = Biome.dirt_vein_inc_chances_by_layer * 1.01 # slight decrease in deep dirt (balances late start)


class Glacier(Biome):
    surface_layer = Snow_Block
    sub_surface_layer = Ice
    deep_layer = Frozen_Rock
    ultra_deep_layer = Rock

    sub_surface_layer_depth = 7

    start_floor_depth = 17

    max_deviation_floor_lvl = 2
    change_probability = 0.08

    lake_chance = 0

    water_cave_chance = 0.1

    dirt_vein_base_chance = 0

    snow_man_chance = 0.008

    iron_ore_min_depth = 25
