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


class Emerald_Block(Block):

    # remember to update the blocks_list for loading when you add a new type of block :)

    str_name = "Emerald Block"
    ticks_to_mine = 80

    @staticmethod
    def draw_manual(screen, x, y, block_width, being_mined=False, is_grid_coordinates=True, use_alt_drawing=False):
        base_color = (90, 210, 130)
        secondary_color = (160, 240, 185)


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


class Diamond_Block(Block):

    # remember to update the blocks_list for loading when you add a new type of block :)

    str_name = "Diamond Block"
    ticks_to_mine = 100

    @staticmethod
    def draw_manual(screen, x, y, block_width, being_mined=False, is_grid_coordinates=True, use_alt_drawing=False):
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


class Coal_Block(Block):

    # remember to update the blocks_list for loading when you add a new type of block :)

    str_name = "Coal Block"
    ticks_to_mine = 80

    @staticmethod
    def draw_manual(screen, x, y, block_width, being_mined=False, is_grid_coordinates=True, use_alt_drawing=False):
        base_color = (22, 21, 22)
        secondary_color = (42, 40, 42)


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


class Gold_Block(Block):

    str_name = "Gold Block"
    ticks_to_mine = 70

    @staticmethod
    def draw_manual(screen, x, y, block_width, being_mined=False, is_grid_coordinates=True, use_alt_drawing=False):
        # cooler, less orange gold
        base_color = (186, 170, 70)
        light_color = (210, 195, 100)   # lighter inset
        highlight_color = (225, 215, 130)

        added_color = 20 if being_mined else 0

        if is_grid_coordinates:
            x *= block_width
            y *= block_width

        # full gold base
        pygame.draw.rect(
            screen,
            (
                min(base_color[0] + added_color, 255),
                min(base_color[1] + added_color, 255),
                min(base_color[2] + added_color, 255)
            ),
            (x, y, block_width, block_width)
        )

        # lighter inset (feels like shine instead of a hole)
        pygame.draw.rect(
            screen,
            (
                min(light_color[0] + added_color, 255),
                min(light_color[1] + added_color, 255),
                min(light_color[2] + added_color, 255)
            ),
            (x + block_width // 10, y + block_width // 10, block_width // 4, block_width // 4)
        )

        # subtle top highlight
        pygame.draw.line(
            screen,
            (
                min(highlight_color[0] + added_color, 255),
                min(highlight_color[1] + added_color, 255),
                min(highlight_color[2] + added_color, 255)
            ),
            (x, y),
            (x + block_width - 1, y)
        )        

# idea: make a metal gate!