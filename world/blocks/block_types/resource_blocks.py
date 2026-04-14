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
    ticks_to_mine = 100

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


# idea: make a metal gate! 30 155 90


# class Iron_Clump(Block): # used the wrong color and doesn't look good yet

#     str_name = "Iron Clump"
#     ticks_to_mine = 75

#     @staticmethod
#     def draw_manual(screen, x, y, block_width, being_mined=False, is_grid_coordinates=True, use_alt_drawing=False):
#         if is_grid_coordinates:
#             x *= block_width
#             y *= block_width

#         base    = (185, 188, 196)
#         dark    = (120, 122, 128)  # gap/shadow color between chunks
#         light   = (210, 212, 218)  # highlight on chunk faces

#         # background fill
#         pygame.draw.rect(screen, dark, (x, y, block_width, block_width))

#         # chunk 1 — top left
#         c1 = [
#             (x + int(block_width * 0.08), y + int(block_width * 0.12)),
#             (x + int(block_width * 0.48), y + int(block_width * 0.08)),
#             (x + int(block_width * 0.52), y + int(block_width * 0.28)),
#             (x + int(block_width * 0.42), y + int(block_width * 0.50)),
#             (x + int(block_width * 0.10), y + int(block_width * 0.52)),
#         ]

#         # chunk 2 — top right
#         c2 = [
#             (x + int(block_width * 0.52), y + int(block_width * 0.08)),
#             (x + int(block_width * 0.88), y + int(block_width * 0.14)),
#             (x + int(block_width * 0.90), y + int(block_width * 0.48)),
#             (x + int(block_width * 0.55), y + int(block_width * 0.50)),
#             (x + int(block_width * 0.52), y + int(block_width * 0.28)),
#         ]

#         # chunk 3 — bottom left
#         c3 = [
#             (x + int(block_width * 0.10), y + int(block_width * 0.52)),
#             (x + int(block_width * 0.42), y + int(block_width * 0.50)),
#             (x + int(block_width * 0.45), y + int(block_width * 0.88)),
#             (x + int(block_width * 0.08), y + int(block_width * 0.90)),
#         ]

#         # chunk 4 — bottom right
#         c4 = [
#             (x + int(block_width * 0.55), y + int(block_width * 0.50)),
#             (x + int(block_width * 0.90), y + int(block_width * 0.48)),
#             (x + int(block_width * 0.88), y + int(block_width * 0.90)),
#             (x + int(block_width * 0.45), y + int(block_width * 0.88)),
#         ]

#         for chunk in [c1, c2, c3, c4]:
#             pygame.draw.polygon(screen, base, chunk)

#         # light edge on top face of each chunk
#         for chunk in [c1, c2, c3, c4]:
#             top_two = chunk[:2]
#             pygame.draw.line(screen, light, top_two[0], top_two[1], max(1, int(block_width * 0.04)))

#         # outlines between chunks
#         for chunk in [c1, c2, c3, c4]:
#             pygame.draw.polygon(screen, dark, chunk, max(1, int(block_width * 0.04)))