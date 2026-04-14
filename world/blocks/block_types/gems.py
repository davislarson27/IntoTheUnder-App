import pygame
from world.blocks.block_types._base import Item, Ingot

class Coal(Item):
    str_name = "Coal"

    @staticmethod
    def draw_manual(screen, x, y, block_width, being_mined=False, is_grid_coordinates=True, use_alt_drawing=False):
        dark = (
            22,
            21,
            22
        )
        mid = (
            28,
            26,
            28
        )

        points = [
            (x + int(block_width*0.35), y + int(block_width*0.17)),
            (x + int(block_width*0.65), y + int(block_width*0.22)),
            (x + int(block_width*0.80), y + int(block_width*0.52)),
            (x + int(block_width*0.55), y + int(block_width*0.82)),
            (x + int(block_width*0.25), y + int(block_width*0.67)),
        ]

        pygame.draw.polygon(screen, mid, points)
        pygame.draw.polygon(screen, dark, points, 1)


class Diamond(Item):
    str_name = "Diamond"

    @staticmethod
    def draw_manual(screen, x, y, block_width, being_mined=False, is_grid_coordinates=True, use_alt_drawing=False):
        dark = (
            90,
            215,
            235
        )
        mid = (
            100,
            225,
            245
        )

        points = [
            (x + int(block_width*0.45), y + int(block_width*0.25)), # center left
            (x + int(block_width*0.30), y + int(block_width*0.36)), # two left
            (x + int(block_width*0.22), y + int(block_width*0.45)), # three left
            (x + int(block_width*0.5), y + int(block_width*0.8)), # center bottom
            (x + int(block_width*0.78), y + int(block_width*0.45)), # three right
            (x + int(block_width*0.70), y + int(block_width*0.36)), # two right
            (x + int(block_width*0.55), y + int(block_width*0.25)), # center right
        ]

        pygame.draw.polygon(screen, mid, points)
        pygame.draw.polygon(screen, dark, points, 1)


class Emerald(Item):
    str_name = "Emerald"

    @staticmethod
    def draw_manual(screen, x, y, block_width, being_mined=False, is_grid_coordinates=True, use_alt_drawing=False):
        if is_grid_coordinates:
            x *= block_width
            y *= block_width

        outer_dark = (35, 120, 65)
        outer_mid = (90, 210, 130)
        inner_light = (160, 240, 185)

        outer_points = [
            (x + int(block_width * 0.38), y + int(block_width * 0.18)),  # top left
            (x + int(block_width * 0.62), y + int(block_width * 0.18)),  # top right
            (x + int(block_width * 0.74), y + int(block_width * 0.32)),  # right upper
            (x + int(block_width * 0.74), y + int(block_width * 0.68)),  # right lower
            (x + int(block_width * 0.62), y + int(block_width * 0.82)),  # bottom right
            (x + int(block_width * 0.38), y + int(block_width * 0.82)),  # bottom left
            (x + int(block_width * 0.26), y + int(block_width * 0.68)),  # left lower
            (x + int(block_width * 0.26), y + int(block_width * 0.32)),  # left upper
        ]

        inner_points = [
            (x + int(block_width * 0.45), y + int(block_width * 0.33)),
            (x + int(block_width * 0.55), y + int(block_width * 0.33)),
            (x + int(block_width * 0.63), y + int(block_width * 0.43)),
            (x + int(block_width * 0.63), y + int(block_width * 0.57)),
            (x + int(block_width * 0.55), y + int(block_width * 0.67)),
            (x + int(block_width * 0.45), y + int(block_width * 0.67)),
            (x + int(block_width * 0.37), y + int(block_width * 0.57)),
            (x + int(block_width * 0.37), y + int(block_width * 0.43)),
        ]

        pygame.draw.polygon(screen, outer_mid, outer_points)
        pygame.draw.polygon(screen, inner_light, inner_points)
        pygame.draw.polygon(screen, outer_dark, outer_points, 1)

class Mabelite(Item):
    str_name = "Mabelite"

    @staticmethod
    def draw_manual(screen, x, y, block_width, being_mined=False, is_grid_coordinates=True, use_alt_drawing=False):
        if is_grid_coordinates:
            x *= block_width
            y *= block_width

        # gold core
        outer_dark  = (20, 100, 60)
        outer_mid   = (30, 155, 90)
        inner_light = (195, 155, 20)

        # # purple
        # outer_dark  = (20, 100, 60)
        # outer_mid   = (30, 155, 90)
        # inner_light = (160, 80, 210)

        # # black core
        # outer_dark  = (20, 100, 60)
        # outer_mid   = (30, 155, 90)
        # inner_light = (15, 25, 20)


        outer_points = [
            (x + int(block_width * 0.40), y + int(block_width * 0.20)),  # top left
            (x + int(block_width * 0.60), y + int(block_width * 0.20)),  # top right
            (x + int(block_width * 0.78), y + int(block_width * 0.40)),  # right upper
            (x + int(block_width * 0.78), y + int(block_width * 0.60)),  # right lower
            (x + int(block_width * 0.60), y + int(block_width * 0.80)),  # bottom right
            (x + int(block_width * 0.40), y + int(block_width * 0.80)),  # bottom left
            (x + int(block_width * 0.22), y + int(block_width * 0.60)),  # left lower
            (x + int(block_width * 0.22), y + int(block_width * 0.40)),  # left upper
        ]
        inner_points = [
            (x + int(block_width * 0.50), y + int(block_width * 0.32)),
            (x + int(block_width * 0.62), y + int(block_width * 0.42)),
            (x + int(block_width * 0.62), y + int(block_width * 0.58)),
            (x + int(block_width * 0.50), y + int(block_width * 0.68)),
            (x + int(block_width * 0.38), y + int(block_width * 0.58)),
            (x + int(block_width * 0.38), y + int(block_width * 0.42)),
        ]
        
        pygame.draw.polygon(screen, outer_mid, outer_points)
        pygame.draw.polygon(screen, inner_light, inner_points)
        pygame.draw.polygon(screen, outer_dark, outer_points, 1)
    