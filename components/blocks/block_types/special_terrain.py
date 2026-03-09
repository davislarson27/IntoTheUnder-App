import pygame
from math import floor
from components.blocks.block_types._base import Block

class Cactus(Block):

    # remember to update the blocks_list for loading when you add a new type of block :)

    str_name = "Cactus"

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

class Snow_Man_Head(Block):
    
    # remember to update the blocks_list for loading when you add a new type of block :)

    str_name = "Snow Man Head"
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

class Saltpeter(Block):
    # remember to update the blocks_list for loading when you add a new type of block :)

    str_name = "Saltpeter"

    ticks_to_mine = 45

    @staticmethod
    def draw_manual(screen, x, y, block_width, being_mined=False, is_grid_coordinates=True, use_alt_drawing=False):
        if being_mined:
            added_color = 20
        else:
            added_color = 0

        if is_grid_coordinates:
            x *= block_width
            y *= block_width

        half_len = int(block_width / 2)
        quarter_len = int(block_width / 4)

        outline_w = 1

        main_left_base = (x + outline_w, y + outline_w)
        main_right_base = (x - outline_w + int(block_width * 0.6), y + outline_w)
        main_triangle_tip = (x + quarter_len, y + int(block_width * 0.9) - outline_w)

        main_left_base_outline = (x, y)
        main_right_base_outline = (x + int(block_width * 0.6), y)
        main_triangle_tip_outline = (x + quarter_len, y + int(block_width * 0.9))


        secondary_left_base_outline = (x + half_len, y)
        secondary_right_base_outline = (x + block_width, y)
        secondary_triangle_tip_outline = (x + half_len + quarter_len, y + int(block_width * 0.6))

        secondary_left_base = (x + outline_w + half_len, y + outline_w)
        secondary_right_base = (x - outline_w + block_width, y + outline_w)
        secondary_triangle_tip = (x + half_len + quarter_len, y + int(block_width * 0.6) - outline_w)


        primary_color = (
            205 + added_color, 
            205 + added_color, 
            195 + added_color
        )
        secondary_color = (
            185 + added_color, 
            185 + added_color, 
            175 + added_color
        )
        outline_color = (
            140 + added_color, 
            140 + added_color, 
            132 + added_color
        )


        # --------------- draw tall main stalactite --------------- #
        pygame.draw.polygon( # outline
            screen,
            outline_color,
            [
                main_left_base_outline,
                main_right_base_outline,
                main_triangle_tip_outline
            ]
        )
        pygame.draw.polygon( # body
            screen,
            primary_color,
            [
                main_left_base,
                main_right_base,
                main_triangle_tip
            ]
        )

        # --------------- draw short secondary stalactite --------------- #
        pygame.draw.polygon( # outline
            screen,
            outline_color,
            points = [
                secondary_left_base_outline,
                secondary_right_base_outline,
                secondary_triangle_tip_outline
            ]
        )
        pygame.draw.polygon( # body
            screen,
            secondary_color,
            points = [
                secondary_left_base,
                secondary_right_base,
                secondary_triangle_tip
            ]
        )
