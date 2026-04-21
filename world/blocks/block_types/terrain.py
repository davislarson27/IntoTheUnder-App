import pygame
from world.blocks.block_types._base import Block

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

        # new warmer and lighter colors
        primary_background_color = (95, 100, 102)
        detail_color = (115, 120, 122)

        pygame.draw.rect(
            screen,
            (primary_background_color[0] + added_color, primary_background_color[1] + added_color, primary_background_color[2] + added_color),
            (x, y, block_width, block_width)
        )
        pygame.draw.rect(
            screen,
            (detail_color[0] + added_color, detail_color[1] + added_color, detail_color[2] + added_color),
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
        
        base_color = (150, 130, 110)
        secondary_color = (140, 120, 110)
        
        pygame.draw.rect( # draw base color
            screen,
            (base_color[0] + added_color, base_color[1] + added_color, base_color[2] + added_color),
            (x, y, block_width, block_width)
        )
        pygame.draw.rect(
            screen,
            (secondary_color[0] + added_color, secondary_color[1] + added_color, secondary_color[2] + added_color),
            ((x) + (block_width // 10) , y + (block_width // 10), block_width // 4, block_width // 4)
        )

class Packed_Dirt(Block):

    # remember to update the blocks_list for loading when you add a new type of block :)

    str_name = "Packed Dirt"
    ticks_to_mine = 40

    @staticmethod
    def draw_manual(screen, x, y, block_width, being_mined=False, is_grid_coordinates=True, use_alt_drawing=False):
        if being_mined:
            added_color = 20
        else:
            added_color = 0

        if is_grid_coordinates:
            x *= block_width
            y *= block_width

        base_color = (121, 101, 81)
        secondary_color = (135, 115, 95)
        
        pygame.draw.rect( # draw base color
            screen,
            (base_color[0] + added_color, base_color[1] + added_color, base_color[2] + added_color),
            (x, y, block_width, block_width)
        )
        pygame.draw.rect(
            screen,
            (secondary_color[0] + added_color, secondary_color[1] + added_color, secondary_color[2] + added_color),
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
            (150 + added_color, 130 + added_color, 110 + added_color),
            (x, y, block_width, block_width)
        )
        pygame.draw.rect( # draw rectangle for grass
            screen,
            (120 + added_color, 135 + added_color, 110 + added_color),
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


        pygame.draw.rect( # draw base color
            screen,
            (215 + added_color, 200 + added_color, 155 + added_color),
            (x, y, block_width, block_width)
        )

        spec_width = 1
        for sub_y in range(y + 1, y+block_width, spec_width * 3):
            for sub_x in range(x + 1, x+block_width , spec_width * 3):
                pygame.draw.rect(
                    screen,
                    (170 + added_color, 168 + added_color, 158 + added_color),
                    (sub_x , sub_y, spec_width, spec_width)
                )

class Sand_Stone(Block):

    # remember to update the blocks_list for loading when you add a new type of block :)

    str_name = "Sand Stone"
    ticks_to_mine = 40

    @staticmethod
    def draw_manual(screen, x, y, block_width, being_mined=False, is_grid_coordinates=True, use_alt_drawing=False):
        if being_mined:
            added_color = 20
        else:
            added_color = 0

        if is_grid_coordinates:
            x *= block_width
            y *= block_width

        base_color = (215, 200, 155)
        secondary_color = (220, 215, 170)
        
        pygame.draw.rect( # draw base color
            screen,
            (base_color[0] + added_color, base_color[1] + added_color, base_color[2] + added_color),
            (x, y, block_width, block_width)
        )
        pygame.draw.rect(
            screen,
            (secondary_color[0] + added_color, secondary_color[1] + added_color, secondary_color[2] + added_color),
            ((x) + (block_width // 10) , y + (block_width // 10), block_width // 4, block_width // 4)
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
        
        color = (180, 230, 245)
        
        pygame.draw.rect( # draw base color
            screen,
            (color[0] + added_color, color[1] + added_color, color[2] + added_color),           # color
            (x, y, block_width, block_width)
        )

class Packed_Ice(Block):
    
    # remember to update the blocks_list for loading when you add a new type of block :)

    str_name = "Packed Ice"
    ticks_to_mine = 50

    @staticmethod
    def draw_manual(screen, x, y, block_width, being_mined=False, is_grid_coordinates=True, use_alt_drawing=False):
        if being_mined:
            added_color = 10
        else:
            added_color = 0

        if is_grid_coordinates:
            x *= block_width
            y *= block_width

        color = (160, 210, 235)
        
        #(180, 230, 255)
        pygame.draw.rect( # draw base color
            screen,
            (color[0] + added_color, color[1] + added_color, color[2] + added_color),           # color
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

        # new warmer and lighter colors
        primary_background_color = (95, 100, 102)
        detail_color = (145, 155, 165)

        pygame.draw.rect(
            screen,
            (primary_background_color[0] + added_color, primary_background_color[1] + added_color, primary_background_color[2] + added_color),
            (x, y, block_width, block_width)
        )
        pygame.draw.rect(
            screen,
            (detail_color[0] + added_color, detail_color[1] + added_color, detail_color[2] + added_color),
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
            (225 + added_color, 235 + added_color, 245 + added_color),
            (x, y, block_width, block_width)
        )

class Border_Block(Block):

    # remember to update the blocks_list for loading when you add a new type of block :)

    str_name = "Border Block"
    ticks_to_mine = 100

    can_break = False

    def onDestroy(self, inventory=None):
        return None

    @staticmethod # alt brick version
    def draw_manual(screen, x, y, block_width, being_mined=False, is_grid_coordinates=True, use_alt_drawing=False):
        if is_grid_coordinates:
            x *= block_width
            y *= block_width

        base  = (70, 75, 80)
        dark  = (40, 47, 55)
        light = (100, 105, 110)

        if being_mined:
            addedColor = 20
            base = (base[0]+addedColor, base[1]+addedColor, base[2]+addedColor)
            dark = (dark[0]+addedColor, dark[1]+addedColor, dark[2]+addedColor)
            light = (light[0]+addedColor, light[1]+addedColor, light[2]+addedColor)

        # background fill
        pygame.draw.rect(screen, dark, (x, y, block_width, block_width))

        # chunk 1 — top left
        c1 = [
            (x + int(block_width * 0.05), y + int(block_width * 0.05)),
            (x + int(block_width * 0.55), y + int(block_width * 0.05)),
            (x + int(block_width * 0.55), y + int(block_width * 0.48)),
            (x + int(block_width * 0.05), y + int(block_width * 0.48)),
        ]

        # chunk 2 — top right
        c2 = [
            (x + int(block_width * 0.60), y + int(block_width * 0.05)),
            (x + int(block_width * 0.95), y + int(block_width * 0.05)),
            (x + int(block_width * 0.95), y + int(block_width * 0.48)),
            (x + int(block_width * 0.60), y + int(block_width * 0.48)),
        ]

        # chunk 3 — bottom left
        c3 = [
            (x + int(block_width * 0.05), y + int(block_width * 0.53)),
            (x + int(block_width * 0.38), y + int(block_width * 0.53)),
            (x + int(block_width * 0.38), y + int(block_width * 0.95)),
            (x + int(block_width * 0.05), y + int(block_width * 0.95)),
        ]

        # chunk 4 — bottom right
        c4 = [
            (x + int(block_width * 0.43), y + int(block_width * 0.53)),
            (x + int(block_width * 0.95), y + int(block_width * 0.53)),
            (x + int(block_width * 0.95), y + int(block_width * 0.95)),
            (x + int(block_width * 0.43), y + int(block_width * 0.95)),
        ]

        for chunk in [c1, c2, c3, c4]:
            pygame.draw.polygon(screen, base, chunk)

        # light edge along top of each chunk
        for chunk in [c1, c2, c3, c4]:
            pygame.draw.line(screen, light, chunk[0], chunk[1], max(1, int(block_width * 0.04)))

        # dark outline on each chunk
        for chunk in [c1, c2, c3, c4]:
            pygame.draw.polygon(screen, dark, chunk, max(1, int(block_width * 0.04)))
