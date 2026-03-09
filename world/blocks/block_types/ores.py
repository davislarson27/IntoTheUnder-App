import pygame
from world.blocks.block_types._base import Block

class Iron_Ore_Block(Block):

    # remember to update the blocks_list for loading when you add a new type of block :)

    str_name = "Iron Ore"

    ticks_to_mine = 75

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

class Gold_Ore_Block(Block):

    # remember to update the blocks_list for loading when you add a new type of block :)

    str_name = "Gold Ore"

    ticks_to_mine = 75

    @staticmethod
    def draw_manual(screen, x, y, block_width, being_mined=False, is_grid_coordinates=True, use_alt_drawing=False):
        added = 20 if being_mined else 0

        if is_grid_coordinates:
            x *= block_width
            y *= block_width

        # --- rock base (can brighten when mined) ---
        pygame.draw.rect(
            screen,
            (70 + added, 75 + added, 80 + added),
            (x, y, block_width, block_width)
        )

        # --- gold ore palette (DO NOT add 'added' so it doesn't shift when mining) ---
        gold_core    = (245, 235, 110)   # cool lemon / pale gold
        gold_outline = (105, 95, 25)     # olive-brown rim (cooler than orange-brown)
        gold_hi      = (255, 255, 210)   # sparkle

        def draw_ore_spec(px, py, w, h, sparkle=False):
            # 1px dark rim
            pygame.draw.rect(screen, gold_outline, (x + px, y + py, w, h))

            # inner core inset (if there's room)
            if w > 2 and h > 2:
                pygame.draw.rect(screen, gold_core, (x + px + 1, y + py + 1, w - 2, h - 2))
            else:
                pygame.draw.rect(screen, gold_core, (x + px, y + py, w, h))

            # optional 1px highlight
            if sparkle:
                pygame.draw.rect(screen, gold_hi, (x + px + 1, y + py + 1, 1, 1))

        # keep your same two specs, just render them with rim + core
        w1 = max(3, block_width // 4)
        h1 = w1
        draw_ore_spec(block_width // 10, block_width // 10, w1, h1, sparkle=True)

        w2 = max(3, block_width // 6)
        h2 = w2
        draw_ore_spec(block_width * 6 // 10, block_width * 8 // 10, w2, h2, sparkle=False)

class Diamond_Ore_Block(Block):

    # remember to update the blocks_list for loading when you add a new type of block :)

    str_name = "Diamond Ore"
    ticks_to_mine = 85

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

    str_name = "Emerald Ore"
    ticks_to_mine = 75

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

    str_name = "Mabelite Ore"
    ticks_to_mine = 85

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

    str_name = "Coal Ore"

    ticks_to_mine = 74

    @staticmethod
    def draw_manual(screen, x, y, block_width, being_mined=False, is_grid_coordinates=True, use_alt_drawing=False):
        if being_mined:
            added_color = 20
        else:
            added_color = 0

        if is_grid_coordinates:
            x *= block_width
            y *= block_width

        pygame.draw.rect( # stone background
            screen,
            (70 + added_color, 75 + added_color, 80 + added_color),
            (x, y, block_width, block_width)
            
        )
        pygame.draw.rect( # coal spot
            screen,
            (22 + added_color, 21 + added_color, 22 + added_color),
            ((x) + (block_width // 10) , (y) + (block_width // 10), block_width // 4, block_width // 4)
        )
        pygame.draw.rect( # second coal spot
            screen,
            (22 + added_color, 21 + added_color, 22 + added_color),
            ((x) + (block_width * 6 // 10) , (y) + (block_width * 8// 10), block_width // 6, block_width // 6)
        )

class Sulfur_Flakes_Block(Block):
    # remember to update the blocks_list for loading when you add a new type of block :)

    str_name = "Sulfur Flakes"

    ticks_to_mine = 70

    @staticmethod
    def draw_manual(screen, x, y, block_width, being_mined=False, is_grid_coordinates=True, use_alt_drawing=False):
        added_color = 20 if being_mined else 0

        if is_grid_coordinates:
            x *= block_width
            y *= block_width

        # base stone
        pygame.draw.rect(
            screen,
            (70 + added_color, 75 + added_color, 80 + added_color),
            (x, y, block_width, block_width)
        )

        # subtle sulfur color (muted)
        sulfur_speck = (
            min(160 + added_color, 255),
            min(170 + added_color, 255),
            min(60 + added_color, 255)
        )

        # base speck size
        base_speck = max(1, block_width // 14)

        # consistent speck layout (x, y, size multiplier)
        specks = [
            (2, 4, 1),
            (5, 3, 2),   # slightly bigger
            (8, 6, 1),
            (4, 8, 1),
            (7, 9, 2),   # slightly bigger
            (10, 5, 1),
        ]

        for sx, sy, mult in specks:
            size = base_speck * mult

            pygame.draw.rect(
                screen,
                sulfur_speck,
                (
                    x + sx * block_width // 12,
                    y + sy * block_width // 12,
                    size,
                    size
                )
            )

