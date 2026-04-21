from copy import deepcopy

from .blocks.block_export import *
from .world_creation.biomes import *
from play.inventory.inventory_item import Inventory_Item
from play.inventory.crafting_recipes import *
from .world_creation.structures.structures import *


class Chunk:
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
    
    def in_bounds(self, x, y):
        if x < self.width and x >= 0 and y < self.height and y >= 0:
            return True
        else:
            return False

    def get(self, x, y):
        if self.in_bounds(x, y):
            return self.array[y][x]
        else:
            return None

    def set_manual(self, x, y, value):
        self.array[y][x] = value
        
    def set(self, x, y, block, pass_through=None, stored_inventory_items=None):
            if block is None:
                self.array[y][x] = None
            else:
                if pass_through is None:
                    pass_through = block.pass_through
                self.array[y][x] = block(self, self.screen, x, y, self.BLOCK_WIDTH, pass_through, stored_inventory_items=stored_inventory_items)

    def is_filled(self, x, y):
        return self.array[y, x] != None
            
    def __str__(self):
        return f'Chunk({self.height}, {self.width}, first = {self.array[0][0]})'

    def __repr__(self):
        return f'Chunk.build({self.array})'
    
    def __eq__(self, other):
        if isinstance(other, Chunk):
            return self.array == other.array
        elif isinstance(other, list):
            return self.array == other
        
    def to_dict(self):
        blocks_in_grid = []
        for y in range(self.height):
            for x in range(self.width):
                cur_block = self.get(x, y)
                if cur_block is not None:
                    blocks_in_grid.append([cur_block.str_name, x, y, cur_block.pass_through, cur_block.get_stored_inventory_items(), cur_block.ticks_till_physics, cur_block.tick_threshold, cur_block.anchor_x, cur_block.anchor_y])
        return { #returns dictionary for grid
            "grid_width": self.width,
            "grid_height": self.height,
            "grid_array": blocks_in_grid
        }
    
    def physics(self, camera_x, camera_y, INVENTORY_HEIGHT=0, global_x_offset=0):
        x_grid_min = max(0, (camera_x // self.BLOCK_WIDTH) - global_x_offset)
        x_grid_max = min(self.width, (camera_x + self.screen.get_width()) // self.BLOCK_WIDTH - global_x_offset) + 1

        true_height = self.screen.get_height() - INVENTORY_HEIGHT
        y_grid_min = max(0, (camera_y // self.BLOCK_WIDTH) - 5)
        y_grid_max = min(self.height, (camera_y + true_height) // self.BLOCK_WIDTH) + 6

        for y in range(y_grid_min, y_grid_max):
            for x in range(x_grid_min, x_grid_max):
                obj = self.get(x, y)
                if(obj != None):
                    obj.physics()

    def draw(self, camera_x, camera_y, INVENTORY_HEIGHT=0, global_x_offset=0):
        x_draw_grid_min = max(0, (camera_x // self.BLOCK_WIDTH) - global_x_offset)
        x_draw_grid_max = min(self.width, (camera_x + self.screen.get_width()) // self.BLOCK_WIDTH - global_x_offset) + 1

        true_height = self.screen.get_height() - INVENTORY_HEIGHT
        y_draw_grid_min = max(0, camera_y // self.BLOCK_WIDTH)
        y_draw_grid_max = min(self.height, (camera_y + true_height) // self.BLOCK_WIDTH) + 1

        for y in range(y_draw_grid_min, y_draw_grid_max):
            for x in range(x_draw_grid_min, x_draw_grid_max):
                obj = self.get(x, y)
                if(obj != None):
                    obj.draw(camera_x=camera_x, camera_y=camera_y)

    @staticmethod
    def fill_from_dict(grid_dict, screen, BLOCK_WIDTH, global_x_offset, return_grid):
        #create grid
        width = grid_dict["grid_width"]
        height = grid_dict["grid_height"]
        grid = Chunk(width, height, BLOCK_WIDTH, screen)

        #fill grid
        str_to_block = get_str_to_block()
        block_locations = grid_dict["grid_array"]
        for block in block_locations:
            try:
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
                        elif len(item) == 2 and item[0] == "Crafting Recipe":
                            stored_inventory_items.append(User_Crafting_Recipes_List.getRecipeFromString(item[1]))
                        elif len(item) == 2 and item[0] == "Inventory Item":
                            stored_inventory_items.append(Inventory_Item.create_from_array(item[1]))
                else:
                    stored_inventory_items = None
                ticks_till_physics = block[5]
                tick_threshold = block[6]
                anchor_x = block[7]
                anchor_y = block[8]

                grid.set_manual(x, y, block_type(
                    return_grid,
                    screen,
                    x + global_x_offset,
                    y,
                    BLOCK_WIDTH,
                    pass_through=pass_through,
                    stored_inventory_items=stored_inventory_items,
                    ticks_till_physics=ticks_till_physics,
                    tick_threshold=tick_threshold,
                    anchor_x=anchor_x,
                    anchor_y=anchor_y)
                )
            
            except (KeyError):
                print(f'error (probable): {block_type_str} is not a valid block type in this version')
                
        return grid
        
    def copy (self):
        return deepcopy(self)
    