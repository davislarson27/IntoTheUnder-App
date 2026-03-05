from math import floor
import random

from biomes import *
from blocks import *

# helper functions for world generation

def generate_tree(grid, grid_x, grid_y, height = 2):
    # stops generation if anything is in the way of the tree
    for y in range(grid_y, grid_y + height):
        if grid.get(grid_x, y - height) is not None: return
    for y in range(3):
        for x in range(3):
            if grid.get(grid_x - 1 + x, grid_y - height - 1 - y) is not  None: return

    for y in range(grid_y, grid_y + height): # generate trunk
        grid.set(grid_x, y - height, Log, True)
    for y in range(3): # generate leaves
        for x in range(3):
            grid.set(grid_x - 1 + x, grid_y - height - 1 - y, Leaves, True)

def generate_cactus(grid, grid_x, grid_y, height = 2):
    # stops generation if anything is in the way of the cactus
    for y in range(grid_y, grid_y + height):
        if grid.get(grid_x, y - height) is not None: return

    for y in range(grid_y, grid_y + height): # generate cactus
        grid.set(grid_x, y - height, Cactus, False)

def generate_snow_man(grid, grid_x, grid_y):
    # stops generation if anything is in the way of the cactus
    if grid.get(grid_x, grid_y) is not None or grid.get(grid_x, grid_y - 1) is not None:
        if grid.get(grid_x - 1, grid_y) is not None or grid.get(grid_x + 1, grid_y) is not None:
            return
        return

    grid.set(grid_x, grid_y, Snow_Block, False)
    grid.set(grid_x, grid_y - 1, Snow_Man_Head, False)

def generate_small_bush(grid, grid_x, grid_y):
    # stops generation if anything is in the way of the bush
    if grid.get(grid_x, grid_y) is not None: return

    grid.set(grid_x, grid_y, Leaves, True)

def find_block_vein_locations(grid, x, Block_Type, ground_level, vein_chance, vein_min_depth, vein_inc_chances_by_layer, vein_min_size, vein_max_size):
    "generates a clump of specified blocks underground"
    for y in range(vein_min_depth, grid.height):
        if y > ground_level[x]:
            if random.random() < vein_chance:
                generate_block_vein(grid, Block_Type, x, y, vein_min_size, vein_max_size)

        vein_chance += vein_inc_chances_by_layer

def generate_block_vein(grid, Block_Type, center_x, center_y, min_size, max_size):
    absolute_max = 9
    if min_size > 0:
        grid.set(center_x, center_y, Block_Type)
    last_x, last_y = center_x, center_y
    direction = [-1, 0, 1]
    direction_chance = [40, 50, 40]
    inserted_coordinates = [[center_x, center_y]]
    cur_x, cur_y = center_x, center_y
    attempts = 0

    blocks_in_vein = min(random.randint(min_size, max_size), absolute_max)

    while len(inserted_coordinates) < blocks_in_vein and attempts < 200:
        if cur_x > 0 and cur_x < grid.width and cur_y > 0 and cur_y < grid.height:
            cur_x, cur_y = random.choices(direction, weights=direction_chance, k=1)[0] + last_x, random.choices(direction, weights=direction_chance, k=1)[0] + last_y
            if [cur_x, cur_y] not in inserted_coordinates:
                grid.set(cur_x, cur_y, Block_Type)
                inserted_coordinates.append([cur_x, cur_y])
                last_x, last_y = cur_x, cur_y            
        attempts += 1

def generate_cave(grid, start_x, start_y, ground_level, max_cave_depth, is_water_cave, saltpeter_chance):
    cave_elevation_change = [-2, -1, 0, 1, 2]
    cave_elevation_change_odds = [1, 4, 5, 4, 1]

    create_cave = False

    ceiling = start_y - 1
    floor = start_y + 1
    for x in range(start_x + 1, grid.width):
        # generate changes to floor & ceiling
        ceiling_change = random.choices(cave_elevation_change, weights=cave_elevation_change_odds, k=1)[0]
        floor_change = random.choices(cave_elevation_change, weights=cave_elevation_change_odds, k=1)[0]

        # apply changes in elevation
        if ceiling + ceiling_change < grid.height and ceiling + ceiling_change >= ground_level[x]:
            ceiling += ceiling_change
        if floor + floor_change < grid.height and floor + floor_change >= ground_level[x]:
            floor += floor_change

        # check for if the cave ended
        if ceiling >= floor: break
        
        while floor - ceiling > max_cave_depth:
            if random.random() < 0.5:
                ceiling += 1
            else:
                floor -= 1

        # now go and clear out the area between the floor and ceiling
        for y in range(ceiling+1 , floor):
            if is_water_cave:
                grid.set(x, y, Water, True)
            else:
                grid.set(x, y, None)
            create_cave = True
        
        # generate saltpeter
        if floor - ceiling - 1 > 1 and not is_water_cave: # requires that there be at least two spots open to generate
            if random.random() < saltpeter_chance:
                grid.set(x, ceiling+1, Saltpeter)

    # now dig out the original center block if the cave began to expand
    if create_cave: 
        if is_water_cave:
            grid.set(start_x, start_y, Water, True)
        else:
            grid.set(start_x, start_y, None)


# main function for world generation
def generate_world_blocks(grid, world_width, world_depth): #width and height are measured in grid units, not pixels
    # generation details
    MIN_LAKE_DEPTH = Biome.start_floor_depth + 2

    # biome generation details
    biomes = [Forest, Thin_Forest, Plains, Tundra, Desert, Lake, Glacier]
    biome_probabilities = [25, 25, 35, 8, 12, 5, 3]
    biome_base_size = 40
    biome_size_variability = 15

    # set first biome at x = 0
    cur_biome = random.choices(biomes, weights=biome_probabilities, k=1)[0]
    cur_biome_start = 0
    cur_biome_size = biome_base_size + floor(random.random() * biome_size_variability)

    # generation details for computer (helps computer understand what it has done at different points during generation)
    ground_level = []
    cur_biome_by_x = []
    has_above_ground_object = []
    for x in range(world_width): has_above_ground_object.append(False) #fill with False
    cur_floor_level = cur_biome.start_floor_depth

    # generate biomes, floor, and ground for the world
    for x in range(world_width):
        # determine if new biome is needed
        cur_biome_by_x.append(cur_biome)
        if x >= cur_biome_start + cur_biome_size: # determine next biome details
            cur_biome = random.choices(biomes, weights=biome_probabilities, k=1)[0]
            cur_biome_start = x
            cur_biome_size = biome_base_size + floor(random.random() * biome_size_variability)


        #determine new elevation
        elevation_change_chance = random.random()
        if cur_biome.start_floor_depth + cur_biome.max_deviation_floor_lvl <= cur_floor_level:
            if elevation_change_chance < cur_biome.change_probability * 2:
                cur_floor_level -= 1
        elif cur_biome.start_floor_depth - cur_biome.max_deviation_floor_lvl >= cur_floor_level:
            if elevation_change_chance < cur_biome.change_probability * 2:
                cur_floor_level += 1
        else: #normal procedure
            if elevation_change_chance < cur_biome.change_probability:
                cur_floor_level += 1
            elif elevation_change_chance < cur_biome.change_probability * 2:
                cur_floor_level -= 1

        # add to the array that records ground level
        ground_level.append(cur_floor_level)

        # add the surface level
        grid.set(x, cur_floor_level, cur_biome.surface_layer)

        # fill in dirt for amound under the surface
        cur_dirt_depth = cur_biome.sub_surface_layer_depth + round(random.random()) + 1
        for y in range(1, cur_dirt_depth):
            grid.set(x, cur_floor_level + y, cur_biome.sub_surface_layer)
        
        for y in range(cur_dirt_depth, world_depth):
            grid.set(x, cur_floor_level + y, cur_biome.deep_layer)

    # generate ores
    for x in range(2, world_width - 2):
        cur_biome = cur_biome_by_x[x]
        find_block_vein_locations(grid, x, Dirt, ground_level, cur_biome.dirt_vein_base_chance, cur_biome.dirt_vein_min_depth, cur_biome.dirt_vein_inc_chances_by_layer, cur_biome.dirt_vein_min_size, cur_biome.dirt_vein_max_size)
        find_block_vein_locations(grid, x, Gravel, ground_level, cur_biome.gravel_vein_base_chance, cur_biome.gravel_vein_min_depth, cur_biome.gravel_vein_inc_chances_by_layer, cur_biome.gravel_vein_min_size, cur_biome.gravel_vein_max_size)
        find_block_vein_locations(grid, x, Coal_Ore_Block, ground_level, cur_biome.coal_ore_base_chance, cur_biome.coal_ore_min_depth, cur_biome.coal_ore_inc_chances_by_layer, cur_biome.coal_ore_vein_min_size, cur_biome.coal_ore_vein_max_size)        
        find_block_vein_locations(grid, x, Iron_Ore_Block, ground_level, cur_biome.iron_ore_base_chance, cur_biome.iron_ore_min_depth, cur_biome.iron_ore_inc_chances_by_layer, cur_biome.iron_ore_vein_min_size, cur_biome.iron_ore_vein_max_size)
        find_block_vein_locations(grid, x, Diamond_Ore_Block, ground_level, cur_biome.diamond_ore_base_chance, cur_biome.diamond_ore_min_depth, cur_biome.diamond_ore_inc_chances_by_layer, cur_biome.diamond_ore_vein_min_size, cur_biome.diamond_ore_vein_max_size)
        find_block_vein_locations(grid, x, Gold_Ore_Block, ground_level, cur_biome.gold_ore_base_chance, cur_biome.gold_ore_min_depth, cur_biome.gold_ore_inc_chances_by_layer, cur_biome.gold_ore_vein_min_size, cur_biome.gold_ore_vein_max_size)        
        find_block_vein_locations(grid, x, Emerald_Ore_Block, ground_level, cur_biome.emerald_ore_base_chance, cur_biome.emerald_ore_min_depth, cur_biome.emerald_ore_inc_chances_by_layer, cur_biome.emerald_ore_vein_min_size, cur_biome.emerald_ore_vein_max_size)
        find_block_vein_locations(grid, x, Mabelite_Ore_Block, ground_level, cur_biome.mabelite_ore_base_chance, cur_biome.mabelite_ore_min_depth, cur_biome.mabelite_ore_inc_chances_by_layer, cur_biome.mabelite_ore_vein_min_size, cur_biome.mabelite_ore_vein_max_size)

    # generate caves
    for x in range(world_width):
        cur_biome = cur_biome_by_x[x]
        for y in range(ground_level[x] + 1, world_depth):
            if random.random() < cur_biome.cave_start_odds:
                if random.random() < cur_biome.water_cave_chance: water_cave = True
                else: water_cave = False
                generate_cave(grid, x, y, ground_level, cur_biome.max_cave_depth, water_cave, cur_biome.saltpeter_chance)


    lake_level = grid.height #throws in a number that should always end a lake if it ever triggered
    fill_lake = False
    for x in range(2, world_width - 2): # cuts off last 2 blocks on each end of the world
        if fill_lake: #if we are filling right now
            if ground_level[x] > lake_level:
                for water_fill_y in range(lake_level, ground_level[x]):
                    grid.set(x, water_fill_y, Water, True)
            else:
                fill_lake = False
        else:
            cur_biome = cur_biome_by_x[x]
            if cur_biome.lake_chance > 0 and ground_level[x] > MIN_LAKE_DEPTH:
                # now check for if the lake should even start
                if ground_level[x-1] < ground_level[x]: #means a drop off started and the lake can begin forming
                    if random.random() < cur_biome.lake_chance:
                        fill_lake = True
                        lake_level = ground_level[x]-1
                        grid.set(x, lake_level, Water, True)


    # generate objects throughout world
    for x in range(world_width):
        cur_biome = cur_biome_by_x[x]
        
        # trees
        if cur_biome.tree_chance > 0:
            if x + 2 < world_width and x - 2 > 0: #check for if in bounds
                if not has_above_ground_object[x - 1] and not has_above_ground_object[x] and not has_above_ground_object[x+1]:
                    if ground_level[x] == ground_level[x+1] or ground_level[x] == ground_level[x-1]:
                        if random.random() < cur_biome.tree_chance:
                            object_height = random.randint(1, 5)
                            if object_height == 4 or object_height == 5: object_height = 2 #makes it more likely for a tree to be 2 high
                            generate_tree(grid, x, ground_level[x], object_height)
                            has_above_ground_object[x] = True
                            has_above_ground_object[x+1] = True
                            has_above_ground_object[x+2] = True
                            if x + 2 < world_width: has_above_ground_object[x+2] = True

        # cactus
        if cur_biome.cactus_chance > 0:
            if x + 1 < world_width and x - 1 > 0: #check for if in bounds
                if not has_above_ground_object[x - 1] and not has_above_ground_object[x] and not has_above_ground_object[x+1]:
                    if ground_level[x] == ground_level[x+1] or ground_level[x] == ground_level[x-1]:
                        if random.random() < cur_biome.cactus_chance:
                            object_height = random.randint(1, 4)
                            if object_height == 4: object_height = 2 #makes it more likely for a tree to be 2 high
                            generate_cactus(grid, x, ground_level[x], object_height)
                            has_above_ground_object[x-1] = True
                            has_above_ground_object[x] = True
                            has_above_ground_object[x+1] = True

        # small bush
        if cur_biome.small_bushes_chance > 0:
            if x + 1 < world_width:
                if not has_above_ground_object[x]:
                    if ground_level[x] == ground_level[x+1] or ground_level[x] == ground_level[x-1]:
                        if random.random() < cur_biome.small_bushes_chance:
                            generate_small_bush(grid, x, ground_level[x]-1)
                            has_above_ground_object[x] = True
                            
        # snow man
        if cur_biome.snow_man_chance > 0:
            if x + 1 < world_width and x - 1 > 0: #check for if in bounds
                if not has_above_ground_object[x - 1] and not has_above_ground_object[x] and not has_above_ground_object[x+1]:
                    if ground_level[x] == ground_level[x+1] or ground_level[x] == ground_level[x-1]:
                        if random.random() < cur_biome.snow_man_chance:
                            generate_snow_man(grid, x, ground_level[x] - 1)
                            has_above_ground_object[x-1] = True
                            has_above_ground_object[x] = True
                            has_above_ground_object[x+1] = True
