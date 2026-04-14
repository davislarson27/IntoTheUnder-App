import pygame
from world.blocks.block_types._base import Block

class Stone_Bricks(Block): # used the wrong color and doesn't look good yet

    str_name = "Stone Bricks"
    ticks_to_mine = 55

    @staticmethod
    def draw_manual(screen, x, y, block_width, being_mined=False, is_grid_coordinates=True, use_alt_drawing=False):
        if is_grid_coordinates:
            x *= block_width
            y *= block_width

        base  = (70, 75, 80)
        dark  = (40, 47, 55)
        light = (100, 105, 110)

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

class Frozen_Stone_Bricks(Block): # used the wrong color and doesn't look good yet

    str_name = "Frozen Stone Bricks"
    ticks_to_mine = 60

    @staticmethod
    def draw_manual(screen, x, y, block_width, being_mined=False, is_grid_coordinates=True, use_alt_drawing=False):
        if is_grid_coordinates:
            x *= block_width
            y *= block_width


        base  = (70, 75, 80)     # main frozen stone color
        dark  = (93, 103, 115)   # cool mortar / cracks
        light = (100, 105, 110)  # frosty highlight


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

class Ice_Bricks(Block): # used the wrong color and doesn't look good yet

    str_name = "Ice Bricks"
    ticks_to_mine = 35

    @staticmethod
    def draw_manual(screen, x, y, block_width, being_mined=False, is_grid_coordinates=True, use_alt_drawing=False):
        if is_grid_coordinates:
            x *= block_width
            y *= block_width


        base  = (180, 230, 255)   # main ice color
        dark  = (120, 170, 200)   # cracks / separation
        light = (220, 245, 255)   # icy highlight


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

class Sand_Bricks(Block): # used the wrong color and doesn't look good yet

    str_name = "Sand Bricks"
    ticks_to_mine = 50

    @staticmethod
    def draw_manual(screen, x, y, block_width, being_mined=False, is_grid_coordinates=True, use_alt_drawing=False):
        if is_grid_coordinates:
            x *= block_width
            y *= block_width


        base  = (215, 200, 155)   # main color
        dark  = (175, 160, 120)   # cracks / separation
        light = (220, 215, 170)   # highlight


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
