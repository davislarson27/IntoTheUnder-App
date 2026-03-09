import pygame
from components.blocks.block_types._base import Block

class Rock(Block):

    # remember to update the blocks_list for loading when you add a new type of block :)

    str_name = "Rock"
    ticks_to_mine = 50

    @staticmethod
    def draw_manual(screen, x, y, block_width, being_mined=False, is_grid_coordinates=True, use_alt_drawing=False):
        if being_mined:
            added_color = 20
        else:
            added_color = 0

        if is_grid_coordinates:
            x *= block_width
            y *= block_width

        pygame.draw.rect(
            screen,
            (70 + added_color, 75 + added_color, 80 + added_color),
            (x, y, block_width, block_width)
        )
        pygame.draw.rect(
            screen,
            (90 + added_color, 95 + added_color, 100 + added_color),
            ((x) + (block_width // 10) , (y) + (block_width // 10), block_width // 4, block_width // 4)
        )

class Dirt(Block):

    # remember to update the blocks_list for loading when you add a new type of block :)

    str_name = "Dirt"

    @staticmethod
    def draw_manual(screen, x, y, block_width, being_mined=False, is_grid_coordinates=True, use_alt_drawing=False):
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
    def draw_manual(screen, x, y, block_width, being_mined=False, is_grid_coordinates=True, use_alt_drawing=False):
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
    def draw_manual(screen, x, y, block_width, being_mined=False, is_grid_coordinates=True, use_alt_drawing=False):
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
    def draw_manual(screen, x, y, block_width, being_mined=False, is_grid_coordinates=True, use_alt_drawing=False):
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

class Ice(Block):
    
    # remember to update the blocks_list for loading when you add a new type of block :)

    str_name = "Ice"
    ticks_to_mine = 36

    @staticmethod
    def draw_manual(screen, x, y, block_width, being_mined=False, is_grid_coordinates=True, use_alt_drawing=False):
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

    str_name = "Frozen Rock"
    ticks_to_mine = 55

    @staticmethod
    def draw_manual(screen, x, y, block_width, being_mined=False, is_grid_coordinates=True, use_alt_drawing=False):
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

class Snow_Block(Block):
    
    # remember to update the blocks_list for loading when you add a new type of block :)

    str_name = "Snow Block"
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
    def draw_manual(screen, x, y, block_width, being_mined=False, is_grid_coordinates=True, use_alt_drawing=False):
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

