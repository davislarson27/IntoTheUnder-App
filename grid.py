from copy import deepcopy
from blocks import *

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
        
    def set(self, x, y, block, pass_through = False):
        if self.in_bounds(x, y):
            if block == None:
                self.array[y][x] = None
            else:
                self.array[y][x] = block(self, self.screen, x, y, self.BLOCK_WIDTH, pass_through)
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
                    blocks_in_grid.append([cur_block.str_name, x, y, cur_block.pass_through])
        
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
            grid.set(x, y, block_type, pass_through)

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

    def display_grid(self): #prints a grid for visualizing what a grid looks like
        row_string = ''
        i = 1
        for row in self.array:
            row_string += '|'
            for item in row:
                if item == None:
                    item_value = ' '
                else:
                    item_value = item
                row_string += item_value
                row_string += '|'
            if i != len(self.array):
                row_string += '\n'
            i += 1
        print(row_string)
        return row_string
