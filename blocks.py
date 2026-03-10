import pygame
from math import floor

# remember to update the blocks_list for loading when you add a new type of block :)

class Block:

    ticks_to_mine = 30
    tick_threshold = 0

    def __init__(self, grid, screen, grid_x, grid_y, block_width, pass_through = False, ticks_till_physics = 0):
        self.grid = grid
        self.screen = screen
        self.x = grid_x
        self.y = grid_y
        self.block_width = block_width
        self.cur_selected = False
        self.pass_through = pass_through
        self.ticks_till_physics = ticks_till_physics

    def interaction(self):
        return None

    def can_move_to_inventory(self):
        return True
    
    def draw_manual(self):
        return
    
    def draw(self, being_mined = False, camera_x = 0, camera_y = 0):
        pixel_self_x = self.x * self.block_width
        pixel_self_y = self.y * self.block_width

        draw_x = pixel_self_x - camera_x
        draw_y = pixel_self_y - camera_y

        self.draw_manual(self.screen, draw_x, draw_y, self.block_width, being_mined, False)

    def physics(self):
        return


class Rock(Block):

    # remember to update the blocks_list for loading when you add a new type of block :)

    str_name = "Rock"
    ticks_to_mine = 50

    @staticmethod
    def draw_manual(screen, x, y, block_width, being_mined = False, is_grid_coordinates = True):
        if being_mined:
            added_color = 20
        else:
            added_color = 0

        if is_grid_coordinates:
            x *= block_width
            y *= block_width

        pygame.draw.rect(
            screen,
            (70 + added_color, 75 + added_color, 80 + added_color),           # color
            (x, y, block_width, block_width)
            
        )
        pygame.draw.rect(
            screen,
            (90 + added_color, 95 + added_color, 100 + added_color),           # color
            ((x) + (block_width // 10) , (y) + (block_width // 10), block_width // 4, block_width // 4)
        )

class Iron_Ore_Block(Block):

    # remember to update the blocks_list for loading when you add a new type of block :)

    str_name = "Iron_Ore_Block"

    ticks_to_mine = 70

    @staticmethod
    def draw_manual(screen, x, y, block_width, being_mined = False, is_grid_coordinates = True):
        if being_mined:
            added_color = 20
        else:
            added_color = 0

        if is_grid_coordinates:
            x *= block_width
            y *= block_width

        pygame.draw.rect(
            screen,
            (70 + added_color, 75 + added_color, 80 + added_color),           # color
            (x, y, block_width, block_width)
            
        )
        #(215, 180, 155) (190, 155, 130)
        pygame.draw.rect(
            screen,
            (190 + added_color, 155 + added_color, 130 + added_color),           # color
            ((x) + (block_width // 10) , (y) + (block_width // 10), block_width // 4, block_width // 4)
        )
        pygame.draw.rect(
            screen,
            (190 + added_color, 155 + added_color, 130 + added_color),
            ((x) + (block_width * 6 // 10) , (y) + (block_width * 8// 10), block_width // 6, block_width // 6)
        )

class Diamond_Ore_Block(Block):

    # remember to update the blocks_list for loading when you add a new type of block :)

    str_name = "Diamond_Ore_Block"
    ticks_to_mine = 80

    @staticmethod
    def draw_manual(screen, x, y, block_width, being_mined = False, is_grid_coordinates = True):
        if being_mined:
            added_color = 20
        else:
            added_color = 0

        if is_grid_coordinates:
            x *= block_width
            y *= block_width

        pygame.draw.rect(
            screen,
            (70 + added_color, 75 + added_color, 80 + added_color),           # color
            (x, y, block_width, block_width)
            
        )
        pygame.draw.rect(
            screen,
            (90 + added_color, 215 + added_color, 235 + added_color),           # color
            ((x) + (block_width // 10) , (y) + (block_width // 10), block_width // 4, block_width // 4)
        )
        pygame.draw.rect(
            screen,
            (90 + added_color, 215 + added_color, 235 + added_color),
            ((x) + (block_width * 6 // 10) , (y) + (block_width * 8// 10), block_width // 6, block_width // 6)
        )

class Emerald_Ore_Block(Block):
    # remember to update the blocks_list for loading when you add a new type of block :)

    str_name = "Emerald_Ore_Block"
    ticks_to_mine = 70

    @staticmethod
    def draw_manual(screen, x, y, block_width, being_mined = False, is_grid_coordinates = True):
        if being_mined:
            added_color = 20
        else:
            added_color = 0

        if is_grid_coordinates:
            x *= block_width
            y *= block_width

        pygame.draw.rect(
            screen,
            (70 + added_color, 75 + added_color, 80 + added_color),           # color
            (x, y, block_width, block_width)
            
        )
        #(80, 200, 120)

        pygame.draw.rect(
            screen,
            (90 + added_color, 210 + added_color, 130 + added_color),           # color
            ((x) + (block_width // 10) , (y) + (block_width // 10), block_width // 4, block_width // 4)
        )
        pygame.draw.rect(
            screen,
            (90 + added_color, 210 + added_color, 130 + added_color),
            ((x) + (block_width * 6 // 10) , (y) + (block_width * 8// 10), block_width // 6, block_width // 6)
        )

class Mabelite_Ore_Block(Block):

    # remember to update the blocks_list for loading when you add a new type of block :)

    str_name = "Mabelite_Ore_Block"
    ticks_to_mine = 80

    @staticmethod
    def draw_manual(screen, x, y, block_width, being_mined = False, is_grid_coordinates = True):
        if being_mined:
            added_color = 20
        else:
            added_color = 0

        if is_grid_coordinates:
            x *= block_width
            y *= block_width

        pygame.draw.rect(
            screen,
            (70 + added_color, 75 + added_color, 80 + added_color),           # color
            (x, y, block_width, block_width)
            
        )
        #(80, 200, 120)

        pygame.draw.rect(
            screen,
            (30 + added_color, 155 + added_color, 90 + added_color),           # color
            ((x) + (block_width // 10) , (y) + (block_width // 10), block_width // 4, block_width // 4)
        )
        #(184, 115, 85)
        pygame.draw.rect(
            screen,
            (30 + added_color, 155 + added_color, 90 + added_color),
            ((x) + (block_width * 6 // 10) , (y) + (block_width * 8// 10), block_width // 6, block_width // 6)
        )

class Coal_Ore_Block(Block):
        
    # remember to update the blocks_list for loading when you add a new type of block :)

    str_name = "Coal_Ore_Block"

    ticks_to_mine = 64

    @staticmethod
    def draw_manual(screen, x, y, block_width, being_mined = False, is_grid_coordinates = True):
        if being_mined:
            added_color = 20
        else:
            added_color = 0

        if is_grid_coordinates:
            x *= block_width
            y *= block_width

        pygame.draw.rect(
            screen,
            (70 + added_color, 75 + added_color, 80 + added_color),           # color
            (x, y, block_width, block_width)
            
        )
        #(215, 180, 155) (190, 155, 130)
        pygame.draw.rect(
            screen,
            (22 + added_color, 21 + added_color, 22 + added_color),           # color
            ((x) + (block_width // 10) , (y) + (block_width // 10), block_width // 4, block_width // 4)
        )
        pygame.draw.rect(
            screen,
            (22 + added_color, 21 + added_color, 22 + added_color),
            ((x) + (block_width * 6 // 10) , (y) + (block_width * 8// 10), block_width // 6, block_width // 6)
        )

class Dirt(Block):

    # remember to update the blocks_list for loading when you add a new type of block :)

    str_name = "Dirt"

    @staticmethod
    def draw_manual(screen, x, y, block_width, being_mined = False, is_grid_coordinates = True):
        if being_mined:
            added_color = 20
        else:
            added_color = 0

        if is_grid_coordinates:
            x *= block_width
            y *= block_width
        
        pygame.draw.rect( # draw base color
            screen,
            (150 + added_color, 130 + added_color, 110 + added_color),           # color
            (x, y, block_width, block_width)
        )
        pygame.draw.rect(
            screen,
            (140 + added_color, 120 + added_color, 110 + added_color),           # color
            ((x) + (block_width // 10) , y + (block_width // 10), block_width // 4, block_width // 4)
        )

class Grass(Block):

    # remember to update the blocks_list for loading when you add a new type of block :)

    str_name = "Grass"

    @staticmethod
    def draw_manual(screen, x, y, block_width, being_mined = False, is_grid_coordinates = True):
        if being_mined:
            added_color = 20
        else:
            added_color = 0

        if is_grid_coordinates:
            x *= block_width
            y *= block_width
        
        pygame.draw.rect( # draw base color
            screen,
            (150 + added_color, 130 + added_color, 110 + added_color),           # color
            (x, y, block_width, block_width)
        )
        pygame.draw.rect( # draw rectangle for grass
            screen,
            (120 + added_color, 135 + added_color, 110 + added_color),           # color
            ((x), (y), block_width, block_width // 3)
        )

class Log(Block): #not yet designed

    # remember to update the blocks_list for loading when you add a new type of block :)

    str_name = "Log"
    ticks_to_mine = 50

    @staticmethod
    def draw_manual(screen, x, y, block_width, being_mined = False, is_grid_coordinates = True):
        if being_mined:
            added_color = 20
        else:
            added_color = 0

        if is_grid_coordinates:
            x *= block_width
            y *= block_width
        
        pygame.draw.rect( # draw base color
            screen,
            (85 + added_color, 70 + added_color, 55 + added_color),           # color
            (x, y, block_width, block_width)
        )
        pygame.draw.rect(
            screen,
            (40 + added_color, 25 + added_color, 10 + added_color),           # color
            ((x) + floor(block_width * 0.15) , y + floor(block_width * 0.25), block_width // 25, block_width // 1.75)
        )
        pygame.draw.rect(
            screen,
            (40 + added_color, 25 + added_color, 10 + added_color),           # color
            ((x) + (block_width // 2) , y + (block_width // 3), block_width // 25, block_width // 1.75)
        )
        pygame.draw.rect(
            screen,
            (40 + added_color, 25 + added_color, 10 + added_color),           # color
            ((x) + floor(block_width * 0.8) , y + floor(block_width * 0.2), block_width // 25, block_width // 1.75)
        )

class Leaves(Block):

    # remember to update the blocks_list for loading when you add a new type of block :)

    str_name = "Leaves"
    ticks_to_mine = 18

    @staticmethod
    def draw_manual(screen, x, y, block_width, being_mined = False, is_grid_coordinates = True):
        if being_mined:
            added_color = 20
        else:
            added_color = 0

        if is_grid_coordinates:
            x *= block_width
            y *= block_width
        
        pygame.draw.rect( # draw base color
            screen,
            (120 + added_color, 155 + added_color, 110 + added_color),           # color
            (x, y, block_width, block_width)
        )

class Sand(Block):

    # remember to update the blocks_list for loading when you add a new type of block :)

    str_name = "Sand"
    ticks_to_mine = 24
    tick_threshold = 2

    def physics(self):
        if self.grid.in_bounds(self.x, self.y + 1): #checks for block directly under the water
            if self.grid.get(self.x, self.y + 1) is None: # this means that the block under is empty!!
                if self.ticks_till_physics < self.tick_threshold:
                    self.ticks_till_physics += 1
                else: #tick count has reached go time :)
                    self.grid.set(self.x, self.y, None)
                    self.grid.set(self.x, self.y+1, Sand, False)
                    self.ticks_till_physics = 0


    @staticmethod
    def draw_manual(screen, x, y, block_width, being_mined = False, is_grid_coordinates = True):
        if being_mined:
            added_color = 20
        else:
            added_color = 0

        if is_grid_coordinates:
            x *= block_width
            y *= block_width

        # (200, 185, 150) (210, 195, 155) (205, 203, 198) (185, 182, 172) (170, 168, 158)
        
        pygame.draw.rect( # draw base color
            screen,
            (215 + added_color, 200 + added_color, 155 + added_color),           # color
            (x, y, block_width, block_width)
        )

        spec_width = 1
        for sub_y in range(y + 1, y+block_width, spec_width * 3):
            for sub_x in range(x + 1, x+block_width , spec_width * 3):
                pygame.draw.rect(
                    screen,
                    (170 + added_color, 168 + added_color, 158 + added_color),           # color
                    (sub_x , sub_y, spec_width, spec_width)
                )

class Gravel(Block):

    # remember to update the blocks_list for loading when you add a new type of block :)

    str_name = "Gravel"
    ticks_to_mine = 24
    tick_threshold = 2

    def physics(self):
        if self.grid.in_bounds(self.x, self.y + 1): #checks for block directly under the water
            if self.grid.get(self.x, self.y + 1) is None: # this means that the block under is empty!!
                if self.ticks_till_physics < self.tick_threshold:
                    self.ticks_till_physics += 1
                else: #tick count has reached go time :)
                    self.grid.set(self.x, self.y, None)
                    self.grid.set(self.x, self.y+1, Gravel, False)
                    # self.y += 1
                    self.ticks_till_physics = 0


    @staticmethod
    def draw_manual(screen, x, y, block_width, being_mined = False, is_grid_coordinates = True):
        if being_mined:
            added_color = 20
        else:
            added_color = 0

        if is_grid_coordinates:
            x *= block_width
            y *= block_width

        # (90 + added_color, 95 + added_color, 100 + added_color)
        
        pygame.draw.rect( # draw base color
            screen,
            (100 + added_color, 105 + added_color, 110 + added_color),           # color
            (x, y, block_width, block_width)
        )

        spec_width = 1
        for sub_y in range(y + 1, y+block_width, spec_width * 3):
            for sub_x in range(x + 1, x+block_width , spec_width * 3):
                pygame.draw.rect(
                    screen,
                    (140 + added_color, 135 + added_color, 140 + added_color),           # color
                    (sub_x , sub_y, spec_width, spec_width)
                )

class Cactus(Block): #not yet designed

    # remember to update the blocks_list for loading when you add a new type of block :)

    str_name = "Cactus"

    @staticmethod
    def draw_manual(screen, x, y, block_width, being_mined = False, is_grid_coordinates = True):
        if being_mined:
            added_color = 20
        else:
            added_color = 0

        if is_grid_coordinates:
            x *= block_width
            y *= block_width
        
        pygame.draw.rect( # draw base color
            screen,
            (70 + added_color, 95 + added_color, 60 + added_color),           # color
            (x, y, block_width, block_width)
        )
        pygame.draw.rect(
            screen,
            (40 + added_color, 25 + added_color, 10 + added_color),           # color
            ((x) + floor(block_width * 0.15) , y + floor(block_width * 0.25), block_width // 25, block_width // 1.75)
        )
        pygame.draw.rect(
            screen,
            (40 + added_color, 25 + added_color, 10 + added_color),           # color
            ((x) + (block_width // 2) , y + (block_width // 3), block_width // 25, block_width // 1.75)
        )
        pygame.draw.rect(
            screen,
            (40 + added_color, 25 + added_color, 10 + added_color),           # color
            ((x) + floor(block_width * 0.8) , y + floor(block_width * 0.2), block_width // 25, block_width // 1.75)
        )

class Snow_Block(Block):
    
    # remember to update the blocks_list for loading when you add a new type of block :)

    str_name = "Snow_Block"
    ticks_to_mine = 16
    tick_threshold = 2

    def physics(self):
        if self.grid.in_bounds(self.x, self.y + 1): #checks for block directly under the water
            if self.grid.get(self.x, self.y + 1) is None: # this means that the block under is empty!!
                if self.ticks_till_physics < self.tick_threshold:
                    self.ticks_till_physics += 1
                else: #tick count has reached go time :)
                    self.grid.set(self.x, self.y, None)
                    self.grid.set(self.x, self.y+1, Snow_Block, False)
                    # self.y += 1
                    self.ticks_till_physics = 0

    @staticmethod
    def draw_manual(screen, x, y, block_width, being_mined = False, is_grid_coordinates = True):
        if being_mined:
            added_color = 9
        else:
            added_color = 0

        if is_grid_coordinates:
            x *= block_width
            y *= block_width
        
        pygame.draw.rect( # draw base color
            screen,
            (225 + added_color, 235 + added_color, 245 + added_color),           # color
            (x, y, block_width, block_width)
        )

class Snow_Man_Head(Block):
    
    # remember to update the blocks_list for loading when you add a new type of block :)

    str_name = "Snow_Man_Head"
    ticks_to_mine = 16
    tick_threshold = 2

    def physics(self):
        if self.grid.in_bounds(self.x, self.y + 1): #checks for block directly under the water
            if self.grid.get(self.x, self.y + 1) is None: # this means that the block under is empty!!
                if self.ticks_till_physics < self.tick_threshold:
                    self.ticks_till_physics += 1
                else: #tick count has reached go time :)
                    self.grid.set(self.x, self.y, None)
                    self.grid.set(self.x, self.y+1, Snow_Man_Head, False)
                    # self.y += 1
                    self.ticks_till_physics = 0

    @staticmethod
    def draw_manual(screen, x, y, block_width, being_mined = False, is_grid_coordinates = True):
        if being_mined:
            added_color = 9
        else:
            added_color = 0

        if is_grid_coordinates:
            x *= block_width
            y *= block_width
        
        pygame.draw.rect( # draw base color
            screen,
            (225 + added_color, 235 + added_color, 245 + added_color),           # color
            (x, y, block_width, block_width)
        )
        pygame.draw.rect(
            screen,
            (10 + added_color, 10 + added_color, 10 + added_color),
            (
                x + (block_width // 4),
                y + (block_width // 3),
                block_width // 8,
                block_width // 8
            )
        )
        pygame.draw.rect(
            screen,
            (10 + added_color, 10 + added_color, 10 + added_color),
            (
                x + ((block_width * 3) // 4) - 1,
                y + (block_width // 3),
                block_width // 8,
                block_width // 8
            )
        )
        # (237, 145, 33)
        pygame.draw.polygon(
            screen,
            (237 + added_color, 145 + added_color, 33 + added_color),
            [
                (x + (block_width // 2), y + (block_width // 2)),
                (x + ((block_width * 3) // 5), y + ((block_width * 3) // 5)),
                (x + ((block_width * 2) // 5), y + ((block_width * 3) // 5))
            ]  
        )

class Ice(Block):
    
    # remember to update the blocks_list for loading when you add a new type of block :)

    str_name = "Ice"
    ticks_to_mine = 36

    @staticmethod
    def draw_manual(screen, x, y, block_width, being_mined = False, is_grid_coordinates = True):
        if being_mined:
            added_color = 10
        else:
            added_color = 0

        if is_grid_coordinates:
            x *= block_width
            y *= block_width
        
        #(180, 230, 255)
        pygame.draw.rect( # draw base color
            screen,
            (180 + added_color, 230 + added_color, 245 + added_color),           # color
            (x, y, block_width, block_width)
        )

class Frozen_Rock(Block):

    # remember to update the blocks_list for loading when you add a new type of block :)

    str_name = "Frozen_Rock"
    ticks_to_mine = 55

    @staticmethod
    def draw_manual(screen, x, y, block_width, being_mined = False, is_grid_coordinates = True):
        if being_mined:
            added_color = 20
        else:
            added_color = 0

        if is_grid_coordinates:
            x *= block_width
            y *= block_width

        pygame.draw.rect(
            screen,
            (70 + added_color, 75 + added_color, 80 + added_color),           # color
            (x, y, block_width, block_width)
            
        )
        #(145, 155, 165) (175, 190, 205)
        pygame.draw.rect(
            screen,
            (145 + added_color, 155 + added_color, 165 + added_color),           # color
            ((x) + (block_width // 10) , (y) + (block_width // 10), block_width // 4, block_width // 4)
        )

class Chest(Block):

    # remember to update the blocks_list for loading when you add a new type of block :)

    str_name = "Chest"
    ticks_to_mine = 60
    interaction = None # this will eventually be a function that opens the chest and lets the user interact with it
    
    def interaction(self):
        print("hit this")
        return None

    @staticmethod
    def draw_manual(screen, x, y, block_width, being_mined = False, is_grid_coordinates = True): 
        if being_mined:
            added_color = 20
        else:
            added_color = 0

        if is_grid_coordinates:
            x *= block_width
            y *= block_width
        
        pygame.draw.rect( # draw base color
            screen,
            (227 + added_color, 183 + added_color, 138 + added_color),           # color
            (x, y, block_width, block_width)
        )
        pygame.draw.rect( # draw base color
            screen,
            (85 + added_color, 70 + added_color, 55 + added_color),           # color
            (x, y, block_width, block_width),
            2
        )
        pygame.draw.rect( # draw outline
            screen,
            (85 + added_color, 70 + added_color, 55 + added_color),           # color
            (x, y, block_width, block_width),
            floor(block_width * 0.08) # width of border
        )
        pygame.draw.rect( # draw divider between top and bottom of the chest
            screen,
            (85 + added_color, 70 + added_color, 55 + added_color),           # color
            (x, y + floor(block_width * 0.3), block_width, floor(block_width * 0.08))
        )
        pygame.draw.rect(
            screen,
            (140 + added_color, 140 + added_color, 140 + added_color),
            (x + floor(block_width * 0.42), y + floor(block_width * 0.3),floor(block_width * 0.18), floor(block_width * 0.24))
        )






class Water(Block):

    # remember to update the blocks_list for loading when you add a new type of block :)
    
    str_name = "Water"
    tick_threshold = 20
    water_value = 0
    max_water_value = 4

    def convert_water_value(self, water_value):
        return self.max_water_value + water_value

    def physics(self):
        if self.grid.in_bounds(self.x, self.y + 1) and (issubclass(type(self.grid.get(self.x, self.y + 1)), Water) or self.grid.get(self.x, self.y + 1) is None): # checks for block directly under the water
            if self.ticks_till_physics < self.tick_threshold:
                self.ticks_till_physics += 1
            else: #tick count has reached go time :)
                self.grid.set(self.x, self.y+1, Water, True)
                self.ticks_till_physics = 0
        elif issubclass(type(self.grid.get(self.x, self.y - 1)), Water) and self.water_value != 0:
            if self.ticks_till_physics < self.tick_threshold:
                self.grid.set(self.x, self.y, Water, True)
                self.ticks_till_physics = 0
            else:
                self.ticks_till_physics += 1
        elif self.grid.in_bounds(self.x + 1, self.y) and ((issubclass(type(self.grid.get(self.x, self.y + 1)), Water)) or self.grid.get(self.x + 1, self.y) is None): # check to the right
            if self.ticks_till_physics < self.tick_threshold:
                self.ticks_till_physics += 1
            else: #tick count has reached go time :)
                self.grid.set(self.x + 1, self.y, self.get_right_fill(), True)
                self.ticks_till_physics = 0
        elif self.grid.in_bounds(self.x - 1, self.y) and ((issubclass(type(self.grid.get(self.x, self.y + 1)), Water)) or self.grid.get(self.x - 1, self.y) is None): # check the left
            if self.ticks_till_physics < self.tick_threshold:
                self.ticks_till_physics += 1
            else: #tick count has reached go time :)
                self.grid.set(self.x - 1, self.y, self.get_left_fill(), True)
                self.ticks_till_physics = 0


        if self.water_value > 0: # right block
            left_block = self.grid.get(self.x - 1, self.y)
            if left_block is not None and issubclass(type(left_block), Water):
                if left_block.water_value != self.water_value - 1:
                    if left_block.water_value < self.max_water_value:
                        self.grid.set(self.x, self.y, water_value_reference[self.convert_water_value(left_block.water_value + 1)], True)
            else:
                if self.grid.in_bounds(self.x - 1, self.y):
                    self.grid.set(self.x, self.y, None)
        elif self.water_value < 0: # right block
            right_block = self.grid.get(self.x + 1, self.y)
            if right_block is not None and issubclass(type(right_block), Water):
                if right_block.water_value != self.water_value + 1:
                    if abs(right_block.water_value) < self.max_water_value:
                        self.grid.set(self.x, self.y, water_value_reference[self.convert_water_value(right_block.water_value - 1)], True)
            else:
                if self.grid.in_bounds(self.x + 1, self.y):
                    self.grid.set(self.x, self.y, None)


        if self.water_value != 0:
            left_block = self.grid.get(self.x - 1, self.y)
            right_block = self.grid.get(self.x + 1, self.y)
            if issubclass(type(right_block), Water) and issubclass(type(left_block), Water):
                if abs(right_block.water_value) < 2 and abs(left_block.water_value) < 2:
                    self.grid.set(self.x, self.y, Water, True)


    @staticmethod
    def get_left_fill():
        return Water_L1
                    
    @staticmethod
    def get_right_fill():
        return Water_R1


    def can_move_to_inventory(self):
        return False
    
    @staticmethod
    def accel_reduction(accel):
        return accel // 3
    
    @staticmethod
    def velocity_reduction(velocity):
        return velocity // 2


    @staticmethod
    def draw_manual(screen, x, y, block_width, being_mined = False, is_grid_coordinates = True):
        if being_mined:
            added_color = 20
        else:
            added_color = 0

        if is_grid_coordinates:
            x *= block_width
            y *= block_width

        # (40, 110, 170) (80, 160, 200) (25, 80, 130)

        pygame.draw.rect( # draw base color
            screen,
            (40 + added_color, 110 + added_color, 170 + added_color),           # color
            (x, y, block_width, block_width)
        )

class Water_R1(Water):

    # remember to update the blocks_list for loading when you add a new type of block :)
    
    str_name = "Water_R1"
    water_value = 1

    @staticmethod
    def get_left_fill():
        return Water
                    
    @staticmethod
    def get_right_fill():
        return Water_R2

                    

    @staticmethod
    def draw_manual(screen, x, y, block_width, being_mined = False, is_grid_coordinates = True):
        if being_mined:
            added_color = 20
        else:
            added_color = 0

        if is_grid_coordinates:
            x *= block_width
            y *= block_width

        # (40, 110, 170) (80, 160, 200) (25, 80, 130)
        drop_off_px = block_width // 4
        points = [
            (x, y),             # top-left high
            (x + block_width, y + drop_off_px),  # top-right lower
            (x + block_width, y + block_width),
            (x, y + block_width)
        ]

        pygame.draw.polygon( # draw base color
            screen,
            (40 + added_color, 110 + added_color, 170 + added_color),           # color
            points
        )

class Water_L1(Water):

    # remember to update the blocks_list for loading when you add a new type of block :)
    
    str_name = "Water_L1"
    water_value = -1
                    
    @staticmethod
    def get_left_fill():
        return Water_L2
                    
    @staticmethod
    def get_right_fill():
        return Water


    @staticmethod
    def draw_manual(screen, x, y, block_width, being_mined = False, is_grid_coordinates = True):
        if being_mined:
            added_color = 20
        else:
            added_color = 0

        if is_grid_coordinates:
            x *= block_width
            y *= block_width

        drop_off_px = block_width // 4
        points = [
            (x, y + drop_off_px),                         # top-left of box
            (x + block_width, y),          # roof peak
            (x + block_width, y + block_width),              # bottom right
            (x, y + block_width)                             # bottom-left

        ]

        pygame.draw.polygon( # draw base color
            screen,
            (40 + added_color, 110 + added_color, 170 + added_color),           # color
            points
        )

class Water_R2(Water):

    # remember to update the blocks_list for loading when you add a new type of block :)
    
    str_name = "Water_R2"
    water_value = 2

    @staticmethod
    def get_left_fill():
        return Water_R1
                    
    @staticmethod
    def get_right_fill():
        return Water_R3
      

    @staticmethod
    def draw_manual(screen, x, y, block_width, being_mined = False, is_grid_coordinates = True):
        if being_mined:
            added_color = 20
        else:
            added_color = 0

        if is_grid_coordinates:
            x *= block_width
            y *= block_width

        # (40, 110, 170) (80, 160, 200) (25, 80, 130)
        drop_off_px = block_width // 4
        points = [
            (x, y + drop_off_px),
            (x + block_width, y + 2*drop_off_px),
            (x + block_width, y + block_width),
            (x, y + block_width)
        ]

        pygame.draw.polygon( # draw base color
            screen,
            (40 + added_color, 110 + added_color, 170 + added_color),           # color
            points
        )

class Water_L2(Water):

    # remember to update the blocks_list for loading when you add a new type of block :)
    
    str_name = "Water_L2"
    water_value = -2

    @staticmethod
    def get_left_fill():
        return Water_L3
                    
    @staticmethod
    def get_right_fill():
        return Water_L1
                

    @staticmethod
    def draw_manual(screen, x, y, block_width, being_mined = False, is_grid_coordinates = True):
        if being_mined:
            added_color = 20
        else:
            added_color = 0

        if is_grid_coordinates:
            x *= block_width
            y *= block_width

        # (40, 110, 170) (80, 160, 200) (25, 80, 130)
        drop_off_px = block_width // 4
        points = [
            (x, y + drop_off_px * 2),                         # top-left of box
            (x + block_width, y + drop_off_px),          # roof peak
            (x + block_width, y + block_width),              # bottom right
            (x, y + block_width)                             # bottom-left
        ]

        pygame.draw.polygon( # draw base color
            screen,
            (40 + added_color, 110 + added_color, 170 + added_color),           # color
            points
        )

class Water_R3(Water):

    # remember to update the blocks_list for loading when you add a new type of block :)
    
    str_name = "Water_R3"
    water_value = 3

    @staticmethod
    def get_left_fill():
        return Water_R2
                    
    @staticmethod
    def get_right_fill():
        return Water_R4
      

    @staticmethod
    def draw_manual(screen, x, y, block_width, being_mined = False, is_grid_coordinates = True):
        if being_mined:
            added_color = 20
        else:
            added_color = 0

        if is_grid_coordinates:
            x *= block_width
            y *= block_width

        # (40, 110, 170) (80, 160, 200) (25, 80, 130)
        drop_off_px = block_width // 4
        points = [
            (x, y + 2 * drop_off_px),
            (x + block_width, y + 3 * drop_off_px),
            (x + block_width, y + block_width),
            (x, y + block_width)
        ]

        pygame.draw.polygon( # draw base color
            screen,
            (40 + added_color, 110 + added_color, 170 + added_color),           # color
            points
        )

class Water_L3(Water):

    # remember to update the blocks_list for loading when you add a new type of block :)
    
    str_name = "Water_L3"
    water_value = -3

    @staticmethod
    def get_left_fill():
        return Water_L4
                    
    @staticmethod
    def get_right_fill():
        return Water_L2
                

    @staticmethod
    def draw_manual(screen, x, y, block_width, being_mined = False, is_grid_coordinates = True):
        if being_mined:
            added_color = 20
        else:
            added_color = 0

        if is_grid_coordinates:
            x *= block_width
            y *= block_width

        # (40, 110, 170) (80, 160, 200) (25, 80, 130)
        drop_off_px = block_width // 4
        points = [
            (x, y + drop_off_px * 3),                         # top-left of box
            (x + block_width, y + drop_off_px * 2),          # roof peak
            (x + block_width, y + block_width),              # bottom right
            (x, y + block_width)                             # bottom-left
        ]

        pygame.draw.polygon( # draw base color
            screen,
            (40 + added_color, 110 + added_color, 170 + added_color),           # color
            points
        )

class Water_R4(Water):

    # remember to update the blocks_list for loading when you add a new type of block :)
    
    str_name = "Water_R4"
    water_value = 4

    @staticmethod
    def get_left_fill():
        return Water_R3
                    
    @staticmethod
    def get_right_fill():
        return None
      

    @staticmethod
    def draw_manual(screen, x, y, block_width, being_mined = False, is_grid_coordinates = True):
        if being_mined:
            added_color = 20
        else:
            added_color = 0

        if is_grid_coordinates:
            x *= block_width
            y *= block_width

        # (40, 110, 170) (80, 160, 200) (25, 80, 130)
        drop_off_px = block_width // 4
        points = [
            (x, y + 3 * drop_off_px),
            (x + block_width, y + 4 * drop_off_px),
            (x + block_width, y + block_width),
            (x, y + block_width)
        ]

        pygame.draw.polygon( # draw base color
            screen,
            (40 + added_color, 110 + added_color, 170 + added_color),           # color
            points
        )

class Water_L4(Water):

    # remember to update the blocks_list for loading when you add a new type of block :)
    
    str_name = "Water_L4"
    water_value = -4

    @staticmethod
    def get_left_fill():
        # return Water
        return None
                    
    @staticmethod
    def get_right_fill():
        return Water_L3
                

    @staticmethod
    def draw_manual(screen, x, y, block_width, being_mined = False, is_grid_coordinates = True):
        if being_mined:
            added_color = 20
        else:
            added_color = 0

        if is_grid_coordinates:
            x *= block_width
            y *= block_width

        # (40, 110, 170) (80, 160, 200) (25, 80, 130)
        drop_off_px = block_width // 4
        points = [
            (x, y + drop_off_px * 4),                         # top-left of box
            (x + block_width, y + drop_off_px * 3),          # roof peak
            (x + block_width, y + block_width),              # bottom right
            (x, y + block_width)                             # bottom-left
        ]

        pygame.draw.polygon( # draw base color
            screen,
            (40 + added_color, 110 + added_color, 170 + added_color),           # color
            points
        )


water_value_reference = [Water_L4, Water_L3, Water_L2, Water_L1, Water, Water_R1, Water_R2, Water_R3, Water_R4]


def get_str_to_block(): # uses blocks_list to generate dictionary that converts str names to their types
    blocks_list = [
        Rock,
        Iron_Ore_Block,
        Diamond_Ore_Block,
        Emerald_Ore_Block,
        Mabelite_Ore_Block,
        Coal_Ore_Block,
        Dirt,
        Grass,
        Log,
        Leaves,
        Sand,
        Gravel,
        Cactus,
        Snow_Block,
        Snow_Man_Head,
        Ice,
        Frozen_Rock,
        Chest,
        Water, # water subclasses after this
            Water_R1,
            Water_L1,
            Water_R2,
            Water_L2,
            Water_R3,
            Water_L3,
            Water_R4,
            Water_L4
    ]

    blocks_dict = {}
    for block in blocks_list:
        blocks_dict[block.str_name] = block
    return blocks_dict