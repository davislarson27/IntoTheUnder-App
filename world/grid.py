from copy import deepcopy
from math import floor
import random

from .blocks.blocks import *
from .world_creation.biomes import *
from play.inventory.inventory_item import Inventory_Item

class Grid:
    """
    2D grid with (x, y) int indexed internal storage
    Has .width .height size properties
    """
    def __init__(self, width, height, BLOCK_WIDTH, screen):
        self.width = width
        self.height = height
        self.BLOCK_WIDTH = BLOCK_WIDTH
        self.screen = screen
        self.array = []
        for y in range(self.height):
            inner = []
            for x in range(self.width):
                inner.append(None)
            self.array.append(inner)

        # generation details
        self.biomes = [Forest, Thin_Forest, Plains, Tundra, Desert, Lake, Glacier]
        self.biome_probabilities = [25, 25, 35, 800, 12, 5, 3]
        self.biome_base_size = 40
        self.biome_size_variability = 15

        self.ground_level = 13

    
    def in_bounds(self, x, y):
        if x < self.width and x >= 0 and y < self.height and y >= 0:
            return True
        else:
            return False

    def get(self, x, y):
        if self.in_bounds(x, y):
            return self.array[y][x]
        else:
            # raise IndexError      
            return None

    def set_manual(self, x, y, value):
        if self.in_bounds(x, y):
            self.array[y][x] = value
        else:
            # raise IndexError
            return None
        
    def set(self, x, y, block, pass_through=False, stored_inventory_items=None):
        if self.in_bounds(x, y):
            if block == None:
                self.array[y][x] = None
            else:
                self.array[y][x] = block(self, self.screen, x, y, self.BLOCK_WIDTH, pass_through, stored_inventory_items=stored_inventory_items)
        else:
            return None

    def is_filled(self, x, y):
        return self.array[y, x] != None
            
    def __str__(self):
        return f'Grid({self.height}, {self.width}, first = {self.array[0][0]})'

    def __repr__(self):
        return f'Grid.build({self.array})'
    
    def __eq__(self, other):
        if isinstance(other, Grid):
            return self.array == other.array
        elif isinstance(other, list):
            return self.array == other
        
    def to_dict(self):
        blocks_in_grid = []
        for y in range(self.height):
            for x in range(self.width):
                cur_block = self.get(x, y)
                if cur_block is not None:
                    blocks_in_grid.append([cur_block.str_name, x, y, cur_block.pass_through, cur_block.get_stored_inventory_items()])
        return { #returns dictionary for grid
            "grid_width": self.width,
            "grid_height": self.height,
            "grid_array": blocks_in_grid
        }
    
    def physics(self, camera_x, camera_y, INVENTORY_HEIGHT = 0):
        x_grid_min = max(0, (camera_x // self.BLOCK_WIDTH) - 5)
        x_grid_max = min(self.width, (camera_x + self.screen.get_width()) // self.BLOCK_WIDTH) + 6

        true_height = self.screen.get_height() - INVENTORY_HEIGHT
        y_grid_min = max(0, (camera_y // self.BLOCK_WIDTH) - 5)
        y_grid_max = min(self.height, (camera_y + true_height) // self.BLOCK_WIDTH) + 6

        for y in range(y_grid_min, y_grid_max):
            for x in range(x_grid_min, x_grid_max):
                obj = self.get(x, y)
                if(obj != None):
                    obj.physics()

    def draw(self, camera_x, camera_y, INVENTORY_HEIGHT = 0):
        x_draw_grid_min = max(0, camera_x // self.BLOCK_WIDTH)
        x_draw_grid_max = min(self.width, (camera_x + self.screen.get_width()) // self.BLOCK_WIDTH) + 1

        true_height = self.screen.get_height() - INVENTORY_HEIGHT
        y_draw_grid_min = max(0, camera_y // self.BLOCK_WIDTH)
        y_draw_grid_max = min(self.height, (camera_y + true_height) // self.BLOCK_WIDTH) + 1

        for y in range(y_draw_grid_min, y_draw_grid_max):
            for x in range(x_draw_grid_min, x_draw_grid_max):
                obj = self.get(x, y)
                if(obj != None):
                    obj.draw(camera_x = camera_x, camera_y = camera_y)

    @staticmethod
    def fill_from_dict(grid_dict, screen, BLOCK_WIDTH):
        #create grid
        width = grid_dict["grid_width"]
        height = grid_dict["grid_height"]
        grid = Grid(width, height, BLOCK_WIDTH, screen)

        #fill grid
        str_to_block = get_str_to_block()
        block_locations = grid_dict["grid_array"]
        for block in block_locations:
            block_type_str = block[0]
            block_type = str_to_block[block_type_str]
            x = block[1]
            y = block[2]
            pass_through = block[3]
            if len(block) > 4 and block[4] is not None:
                stored_inventory_items_compressed = block[4]
                stored_inventory_items = []
                for item in stored_inventory_items_compressed:
                    if item is None:
                        stored_inventory_items.append(None)
                    else:
                        stored_inventory_items.append(Inventory_Item.create_from_array(item))
            else:
                stored_inventory_items = None
            grid.set(x, y, block_type, pass_through, stored_inventory_items)

        return grid
        
    @staticmethod
    def check_list_malformed(lst):
        if not(isinstance(lst, list)) or lst == []:
            raise ValueError('Input must be a non-empty list of lists.')
        else:
            i = 0
            for sublist in lst:
                if not(isinstance(sublist, list)):
                    raise ValueError('Input must be a list of lists.')
                elif len(sublist) != len(lst[i-1]):
                    raise ValueError('All items in list must be lists of the same length.')
                i += 1
    
    @staticmethod
    def build(lst):
        try:
            Grid.check_list_malformed(lst)
        except ValueError as e:
            print(e)
            return
        height = len(lst)
        width = len(lst[0]) #data already validated, sublists are of same length
        grid = Grid(width, height)
        grid.array = deepcopy(lst)
        return grid

    def copy (self):
        return deepcopy(self)
    

    # ------------------------------------------------- terrain generation functions ------------------------------------------------- #
    def reset_ground_level(self, ground_level):
        self.ground_level = ground_level

    def reset_biome_chance(self, Biome, weight):
        """resets biome chance to weight (expects whole integer)"""
        for i in range(len(self.biomes)):
            if isinstance(self.biomes[i], Biome):
                self.biome_probabilities[i] = weight
                return

    def set_single_biome(self, Biome):
        """sets single biome for world generation"""
        self.biomes = [Biome]
        self.biome_probabilities = [1]

    # main function for world generation
    def generate_terrain(self): #width and height are measured in grid units, not pixels

        # ------------------------------------------------- helper functions ------------------------------------------------- #

        def generate_tree(grid_x, grid_y, height = 2):
            # stops generation if anything is in the way of the tree
            for y in range(grid_y, grid_y + height):
                if self.get(grid_x, y - height) is not None: return
            for y in range(3):
                for x in range(3):
                    if self.get(grid_x - 1 + x, grid_y - height - 1 - y) is not  None: return

            for y in range(grid_y, grid_y + height): # generate trunk
                self.set(grid_x, y - height, Log, True)
            for y in range(3): # generate leaves
                for x in range(3):
                    self.set(grid_x - 1 + x, grid_y - height - 1 - y, Leaves, True)

        def generate_cactus(grid_x, grid_y, height = 2):
            # stops generation if anything is in the way of the cactus
            for y in range(grid_y, grid_y + height):
                if self.get(grid_x, y - height) is not None: return

            for y in range(grid_y, grid_y + height): # generate cactus
                self.set(grid_x, y - height, Cactus, False)

        def generate_snow_man(grid_x, grid_y):
            # stops generation if anything is in the way of the cactus
            if self.get(grid_x, grid_y) is not None or self.get(grid_x, grid_y - 1) is not None:
                if self.get(grid_x - 1, grid_y) is not None or self.get(grid_x + 1, grid_y) is not None:
                    return
                return

            self.set(grid_x, grid_y, Snow_Block, False)
            self.set(grid_x, grid_y - 1, Snow_Man_Head, False)

        def generate_small_bush(grid_x, grid_y):
            # stops generation if anything is in the way of the bush
            if self.get(grid_x, grid_y) is not None: return

            self.set(grid_x, grid_y, Leaves, True)

        def find_block_vein_locations(x, Block_Type, ground_level, vein_chance, vein_min_depth, vein_inc_chances_by_layer, vein_min_size, vein_max_size):
            "generates a clump of specified blocks underground"
            for y in range(vein_min_depth, self.height):
                if y > ground_level[x]:
                    if random.random() < vein_chance:
                        generate_block_vein(Block_Type, x, y, vein_min_size, vein_max_size)

                vein_chance += vein_inc_chances_by_layer

        def generate_block_vein(Block_Type, center_x, center_y, min_size, max_size):
            absolute_max = 9
            if min_size > 0:
                self.set(center_x, center_y, Block_Type)
            last_x, last_y = center_x, center_y
            direction = [-1, 0, 1]
            direction_chance = [40, 50, 40]
            inserted_coordinates = [[center_x, center_y]]
            cur_x, cur_y = center_x, center_y
            attempts = 0

            blocks_in_vein = min(random.randint(min_size, max_size), absolute_max)

            while len(inserted_coordinates) < blocks_in_vein and attempts < 200:
                if cur_x > 0 and cur_x < self.width and cur_y > 0 and cur_y < self.height:
                    cur_x, cur_y = random.choices(direction, weights=direction_chance, k=1)[0] + last_x, random.choices(direction, weights=direction_chance, k=1)[0] + last_y
                    if [cur_x, cur_y] not in inserted_coordinates:
                        self.set(cur_x, cur_y, Block_Type)
                        inserted_coordinates.append([cur_x, cur_y])
                        last_x, last_y = cur_x, cur_y            
                attempts += 1

        def generate_cave(start_x, start_y, ground_level, max_cave_depth, is_water_cave, saltpeter_chance):
            cave_elevation_change = [-2, -1, 0, 1, 2]
            cave_elevation_change_odds = [1, 4, 5, 4, 1]

            create_cave = False

            ceiling = start_y - 1
            floor = start_y + 1
            for x in range(start_x + 1, self.width):
                # generate changes to floor & ceiling
                ceiling_change = random.choices(cave_elevation_change, weights=cave_elevation_change_odds, k=1)[0]
                floor_change = random.choices(cave_elevation_change, weights=cave_elevation_change_odds, k=1)[0]

                # apply changes in elevation
                if ceiling + ceiling_change < self.height and ceiling + ceiling_change >= ground_level[x]:
                    ceiling += ceiling_change
                if floor + floor_change < self.height and floor + floor_change >= ground_level[x]:
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
                        self.set(x, y, Water, True)
                    else:
                        self.set(x, y, None)
                    create_cave = True
                
                # generate saltpeter
                if floor - ceiling - 1 > 1 and not is_water_cave: # requires that there be at least two spots open to generate
                    if random.random() < saltpeter_chance:
                        self.set(x, ceiling+1, Saltpeter)

            # now dig out the original center block if the cave began to expand
            if create_cave: 
                if is_water_cave:
                    self.set(start_x, start_y, Water, True)
                else:
                    self.set(start_x, start_y, None)


        # ---------------------------------------------------- main ---------------------------------------------------- #

        MIN_LAKE_DEPTH = Biome.start_floor_depth + 2

        # set first biome at x = 0
        cur_biome = random.choices(self.biomes, weights=self.biome_probabilities, k=1)[0]
        cur_biome_start = 0
        cur_biome_size = self.biome_base_size + floor(random.random() * self.biome_size_variability)

        # generation details for computer (helps computer understand what it has done at different points during generation)
        ground_level = []
        cur_biome_by_x = []
        has_above_ground_object = []
        for x in range(self.width): has_above_ground_object.append(False) #fill with False
        cur_floor_level = cur_biome.start_floor_depth

        # generate biomes, floor, and ground for the world
        for x in range(self.width):
            # determine if new biome is needed
            cur_biome_by_x.append(cur_biome)
            if x >= cur_biome_start + cur_biome_size: # determine next biome details
                cur_biome = random.choices(self.biomes, weights=self.biome_probabilities, k=1)[0]
                cur_biome_start = x
                cur_biome_size = self.biome_base_size + floor(random.random() * self.biome_size_variability)


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
            self.set(x, cur_floor_level, cur_biome.surface_layer)

            # fill in dirt for amound under the surface
            cur_dirt_depth = cur_biome.sub_surface_layer_depth + round(random.random()) + 1
            for y in range(1, cur_dirt_depth):
                self.set(x, cur_floor_level + y, cur_biome.sub_surface_layer)
            
            for y in range(cur_dirt_depth, self.height):
                self.set(x, cur_floor_level + y, cur_biome.deep_layer)

        # generate ores
        for x in range(2, self.width - 2):
            cur_biome = cur_biome_by_x[x]
            find_block_vein_locations(x, Dirt, ground_level, cur_biome.dirt_vein_base_chance, cur_biome.dirt_vein_min_depth, cur_biome.dirt_vein_inc_chances_by_layer, cur_biome.dirt_vein_min_size, cur_biome.dirt_vein_max_size)
            find_block_vein_locations(x, Gravel, ground_level, cur_biome.gravel_vein_base_chance, cur_biome.gravel_vein_min_depth, cur_biome.gravel_vein_inc_chances_by_layer, cur_biome.gravel_vein_min_size, cur_biome.gravel_vein_max_size)
            find_block_vein_locations(x, Coal_Ore_Block, ground_level, cur_biome.coal_ore_base_chance, cur_biome.coal_ore_min_depth, cur_biome.coal_ore_inc_chances_by_layer, cur_biome.coal_ore_vein_min_size, cur_biome.coal_ore_vein_max_size)        
            find_block_vein_locations(x, Sulfur_Flakes_Block, ground_level, cur_biome.sulfur_flakes_base_chance, cur_biome.sulfur_flakes_min_depth, cur_biome.sulfur_flakes_inc_chances_by_layer, cur_biome.sulfur_flakes_vein_min_size, cur_biome.sulfur_flakes_vein_max_size)
            find_block_vein_locations(x, Iron_Ore_Block, ground_level, cur_biome.iron_ore_base_chance, cur_biome.iron_ore_min_depth, cur_biome.iron_ore_inc_chances_by_layer, cur_biome.iron_ore_vein_min_size, cur_biome.iron_ore_vein_max_size)
            find_block_vein_locations(x, Diamond_Ore_Block, ground_level, cur_biome.diamond_ore_base_chance, cur_biome.diamond_ore_min_depth, cur_biome.diamond_ore_inc_chances_by_layer, cur_biome.diamond_ore_vein_min_size, cur_biome.diamond_ore_vein_max_size)
            find_block_vein_locations(x, Emerald_Ore_Block, ground_level, cur_biome.emerald_ore_base_chance, cur_biome.emerald_ore_min_depth, cur_biome.emerald_ore_inc_chances_by_layer, cur_biome.emerald_ore_vein_min_size, cur_biome.emerald_ore_vein_max_size)
            find_block_vein_locations(x, Mabelite_Ore_Block, ground_level, cur_biome.mabelite_ore_base_chance, cur_biome.mabelite_ore_min_depth, cur_biome.mabelite_ore_inc_chances_by_layer, cur_biome.mabelite_ore_vein_min_size, cur_biome.mabelite_ore_vein_max_size)

        # generate caves
        for x in range(self.width):
            cur_biome = cur_biome_by_x[x]
            for y in range(ground_level[x] + 1, self.height):
                if random.random() < cur_biome.cave_start_odds:
                    if random.random() < cur_biome.water_cave_chance: water_cave = True
                    else: water_cave = False
                    generate_cave(x, y, ground_level, cur_biome.max_cave_depth, water_cave, cur_biome.saltpeter_chance)


        lake_level = self.height #throws in a number that should always end a lake if it ever triggered
        fill_lake = False
        for x in range(2, self.width - 2): # cuts off last 2 blocks on each end of the world
            if fill_lake: #if we are filling right now
                if ground_level[x] > lake_level:
                    for water_fill_y in range(lake_level, ground_level[x]):
                        self.set(x, water_fill_y, Water, True)
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
                            self.set(x, lake_level, Water, True)


        # generate objects throughout world
        for x in range(self.width):
            cur_biome = cur_biome_by_x[x]
            
            # trees
            if cur_biome.tree_chance > 0:
                if x + 2 < self.width and x - 2 > 0: #check for if in bounds
                    if not has_above_ground_object[x - 1] and not has_above_ground_object[x] and not has_above_ground_object[x+1]:
                        if ground_level[x] == ground_level[x+1] or ground_level[x] == ground_level[x-1]:
                            if random.random() < cur_biome.tree_chance:
                                object_height = random.randint(1, 5)
                                if object_height == 4 or object_height == 5: object_height = 2 #makes it more likely for a tree to be 2 high
                                generate_tree(x, ground_level[x], object_height)
                                has_above_ground_object[x] = True
                                has_above_ground_object[x+1] = True
                                has_above_ground_object[x+2] = True
                                if x + 2 < self.width: has_above_ground_object[x+2] = True

            # cactus
            if cur_biome.cactus_chance > 0:
                if x + 1 < self.width and x - 1 > 0: #check for if in bounds
                    if not has_above_ground_object[x - 1] and not has_above_ground_object[x] and not has_above_ground_object[x+1]:
                        if ground_level[x] == ground_level[x+1] or ground_level[x] == ground_level[x-1]:
                            if random.random() < cur_biome.cactus_chance:
                                object_height = random.randint(1, 4)
                                if object_height == 4: object_height = 2 #makes it more likely for a tree to be 2 high
                                generate_cactus(x, ground_level[x], object_height)
                                has_above_ground_object[x-1] = True
                                has_above_ground_object[x] = True
                                has_above_ground_object[x+1] = True

            # small bush
            if cur_biome.small_bushes_chance > 0:
                if x + 1 < self.width:
                    if not has_above_ground_object[x]:
                        if ground_level[x] == ground_level[x+1] or ground_level[x] == ground_level[x-1]:
                            if random.random() < cur_biome.small_bushes_chance:
                                generate_small_bush(x, ground_level[x]-1)
                                has_above_ground_object[x] = True
                                
            # snow man
            if cur_biome.snow_man_chance > 0:
                if x + 1 < self.width and x - 1 > 0: #check for if in bounds
                    if not has_above_ground_object[x - 1] and not has_above_ground_object[x] and not has_above_ground_object[x+1]:
                        if ground_level[x] == ground_level[x+1] or ground_level[x] == ground_level[x-1]:
                            if random.random() < cur_biome.snow_man_chance:
                                generate_snow_man(x, ground_level[x] - 1)
                                has_above_ground_object[x-1] = True
                                has_above_ground_object[x] = True
                                has_above_ground_object[x+1] = True
