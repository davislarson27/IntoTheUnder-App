import pygame
from world.blocks.block_types._base import Block

class Iron_Block(Block):

    # remember to update the blocks_list for loading when you add a new type of block :)

    str_name = "Iron Block"
    ticks_to_mine = 85

    @staticmethod
    def draw_manual(screen, x, y, block_width, being_mined=False, is_grid_coordinates=True, use_alt_drawing=False):
        # (185, 188, 196)
        iron_base_color = (190, 193, 201)
        iron_secondary_color = (206, 209, 217)

        if being_mined: added_color = 20
        else: added_color = 0

        if is_grid_coordinates:
            x *= block_width
            y *= block_width

        pygame.draw.rect(
            screen,
            (iron_base_color[0] + added_color, iron_base_color[1] + added_color, iron_base_color[2] + added_color),
            (x, y, block_width, block_width)
        )
        pygame.draw.rect(
            screen,
            (iron_secondary_color[0] + added_color, iron_secondary_color[1] + added_color, iron_secondary_color[2] + added_color),
            ((x) + (block_width // 10) , (y) + (block_width // 10), block_width // 4, block_width // 4)
        )

class Diamond_Block(Block):

    # remember to update the blocks_list for loading when you add a new type of block :)

    str_name = "Diamond Block"
    ticks_to_mine = 100

    @staticmethod
    def draw_manual(screen, x, y, block_width, being_mined=False, is_grid_coordinates=True, use_alt_drawing=False):
        # (185, 188, 196)
        base_color = (90, 215, 235)
        secondary_color = (110, 235, 255)


        if being_mined: added_color = 20
        else: added_color = 0

        if is_grid_coordinates:
            x *= block_width
            y *= block_width

        pygame.draw.rect(
            screen,
            (min(base_color[0] + added_color, 255), min(base_color[1] + added_color, 255), min(base_color[2] + added_color, 255)),
            (x, y, block_width, block_width)
        )
        pygame.draw.rect(
            screen,
            (min(secondary_color[0] + added_color, 255), min(secondary_color[1] + added_color, 255), min(secondary_color[2] + added_color, 255)),
            ((x) + (block_width // 10) , (y) + (block_width // 10), block_width // 4, block_width // 4)
        )
