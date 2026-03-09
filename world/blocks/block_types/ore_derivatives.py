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
