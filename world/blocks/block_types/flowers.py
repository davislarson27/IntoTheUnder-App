import pygame
from world.blocks.block_types._base import Block

class Rose(Block):

    # remember to update the blocks_list for loading when you add a new type of block :)

    str_name = "Rose"
    ticks_to_mine = 4
    pass_through = True

    draw_background = True
    ignore_shading_from = {
        (0, 1): True,
        (0, -1): True,
        (1, 0): True,
        (-1, 0): True
    }

    @staticmethod
    def draw_manual(screen, x, y, block_width, being_mined=False, is_grid_coordinates=True, use_alt_drawing=False):
        added = 25 if being_mined else 0

        if is_grid_coordinates:
            x *= block_width
            y *= block_width

        bw = block_width

        def c(rgb):
            return (min(255, rgb[0] + added), min(255, rgb[1] + added), min(255, rgb[2] + added))

        stem_green    = c((55, 115, 45))
        leaf_green    = c((75, 140, 55))
        sepal_green   = c((40, 90, 30))
        petal_dark    = c((135, 30, 40))
        petal_main    = c((190, 50, 60))
        petal_hi      = c((220, 88, 88))

        cx = x + bw // 2

        # --- Stem ---
        stem_w = max(2, int(bw * 0.10))
        stem_x = cx - stem_w // 2
        stem_top_y = y + int(bw * 0.46)
        pygame.draw.rect(screen, stem_green, (stem_x, stem_top_y, stem_w, bw - int(bw * 0.46)))

        # --- Leaf (left side, midway up stem) ---
        leaf_w = int(bw * 0.17)
        leaf_h = max(2, int(bw * 0.07))
        leaf_x = stem_x - leaf_w
        leaf_y = y + int(bw * 0.63)
        pygame.draw.rect(screen, leaf_green, (leaf_x, leaf_y, leaf_w, leaf_h))
        # taper the far end of the leaf slightly darker
        pygame.draw.rect(screen, sepal_green, (leaf_x, leaf_y, max(1, leaf_w // 3), leaf_h))

        # --- Sepal (base of flower, dark green) ---
        sepal_w = int(bw * 0.30)
        sepal_h = max(2, int(bw * 0.07))
        sepal_y = y + int(bw * 0.40)
        pygame.draw.rect(screen, sepal_green, (cx - sepal_w // 2, sepal_y, sepal_w, sepal_h))

        # --- Lower petal row (widest, dark red — gives depth/base) ---
        low_w = int(bw * 0.42)
        low_h = int(bw * 0.08)
        low_y = y + int(bw * 0.33)
        pygame.draw.rect(screen, petal_dark, (cx - low_w // 2, low_y, low_w, low_h))

        # --- Mid petal row (main red) ---
        mid_w = int(bw * 0.36)
        mid_h = int(bw * 0.09)
        mid_y = y + int(bw * 0.25)
        pygame.draw.rect(screen, petal_main, (cx - mid_w // 2, mid_y, mid_w, mid_h))

        # --- Top petal row (highlight, narrow — the bud tip) ---
        top_w = int(bw * 0.22)
        top_h = int(bw * 0.07)
        top_y = y + int(bw * 0.20)
        pygame.draw.rect(screen, petal_hi, (cx - top_w // 2, top_y, top_w, top_h))

        # --- Left-edge shadow on mid and lower rows for a subtle bud depth ---
        shadow_w = max(1, int(bw * 0.04))
        pygame.draw.rect(screen, petal_dark, (cx - low_w // 2, low_y, shadow_w, low_h))
        pygame.draw.rect(screen, petal_dark, (cx - mid_w // 2, mid_y, shadow_w, mid_h))
    
class Wild_Flower(Block):

    # remember to update the blocks_list for loading when you add a new type of block :)

    str_name = "Wild Flower"
    ticks_to_mine = 4
    pass_through = True

    draw_background = True
    ignore_shading_from = {
        (0, 1): True,
        (0, -1): True,
        (1, 0): True,
        (-1, 0): True
    }

    @staticmethod
    def draw_manual(screen, x, y, block_width, being_mined=False, is_grid_coordinates=True, use_alt_drawing=False):
        added = 25 if being_mined else 0

        if is_grid_coordinates:
            x *= block_width
            y *= block_width

        bw = block_width

        def c(rgb):
            return (min(255, rgb[0] + added), min(255, rgb[1] + added), min(255, rgb[2] + added))

        stem_green    = c((55, 115, 45))
        leaf_green    = c((75, 140, 55))
        sepal_green   = c((40, 90, 30))
        petal_dark  = c((148, 118, 18))
        petal_main  = c((196, 168, 48))
        petal_hi    = c((220, 200, 98))

        cx = x + bw // 2

        # --- Stem ---
        stem_w = max(2, int(bw * 0.10))
        stem_x = cx - stem_w // 2
        stem_top_y = y + int(bw * 0.46)
        pygame.draw.rect(screen, stem_green, (stem_x, stem_top_y, stem_w, bw - int(bw * 0.46)))

        # --- Leaf (left side, midway up stem) ---
        leaf_w = int(bw * 0.17)
        leaf_h = max(2, int(bw * 0.07))
        leaf_x = stem_x - leaf_w
        leaf_y = y + int(bw * 0.63)
        pygame.draw.rect(screen, leaf_green, (leaf_x, leaf_y, leaf_w, leaf_h))
        # taper the far end of the leaf slightly darker
        pygame.draw.rect(screen, sepal_green, (leaf_x, leaf_y, max(1, leaf_w // 3), leaf_h))

        # --- Sepal (base of flower, dark green) ---
        sepal_w = int(bw * 0.30)
        sepal_h = max(2, int(bw * 0.07))
        sepal_y = y + int(bw * 0.40)
        pygame.draw.rect(screen, sepal_green, (cx - sepal_w // 2, sepal_y, sepal_w, sepal_h))

        # --- Lower petal row (widest, dark red — gives depth/base) ---
        low_w = int(bw * 0.42)
        low_h = int(bw * 0.08)
        low_y = y + int(bw * 0.33)
        pygame.draw.rect(screen, petal_dark, (cx - low_w // 2, low_y, low_w, low_h))

        # --- Mid petal row (main red) ---
        mid_w = int(bw * 0.36)
        mid_h = int(bw * 0.09)
        mid_y = y + int(bw * 0.25)
        pygame.draw.rect(screen, petal_main, (cx - mid_w // 2, mid_y, mid_w, mid_h))

        # --- Top petal row (highlight, narrow — the bud tip) ---
        top_w = int(bw * 0.22)
        top_h = int(bw * 0.07)
        top_y = y + int(bw * 0.20)
        pygame.draw.rect(screen, petal_hi, (cx - top_w // 2, top_y, top_w, top_h))

        # --- Left-edge shadow on mid and lower rows for a subtle bud depth ---
        shadow_w = max(1, int(bw * 0.04))
        pygame.draw.rect(screen, petal_dark, (cx - low_w // 2, low_y, shadow_w, low_h))
        pygame.draw.rect(screen, petal_dark, (cx - mid_w // 2, mid_y, shadow_w, mid_h))

class White_Lily(Block): # Moonflower?

    # remember to update the blocks_list for loading when you add a new type of block :)

    str_name = "White_Lily"
    ticks_to_mine = 4
    pass_through = True

    draw_background = True
    ignore_shading_from = {
        (0, 1): True,
        (0, -1): True,
        (1, 0): True,
        (-1, 0): True
    }

    @staticmethod
    def draw_manual(screen, x, y, block_width, being_mined=False, is_grid_coordinates=True, use_alt_drawing=False):
        added = 25 if being_mined else 0

        if is_grid_coordinates:
            x *= block_width
            y *= block_width

        bw = block_width

        def c(rgb):
            return (min(255, rgb[0] + added), min(255, rgb[1] + added), min(255, rgb[2] + added))

        stem_green    = c((55, 115, 45))
        leaf_green    = c((75, 140, 55))
        sepal_green   = c((40, 90, 30))
        petal_dark  = c((210, 205, 180))
        petal_main  = c((238, 238, 222))
        petal_hi    = c((255, 254, 245))

        cx = x + bw // 2

        # --- Stem ---
        stem_w = max(2, int(bw * 0.10))
        stem_x = cx - stem_w // 2
        stem_top_y = y + int(bw * 0.46)
        pygame.draw.rect(screen, stem_green, (stem_x, stem_top_y, stem_w, bw - int(bw * 0.46)))

        # --- Leaf (left side, midway up stem) ---
        leaf_w = int(bw * 0.17)
        leaf_h = max(2, int(bw * 0.07))
        leaf_x = stem_x - leaf_w
        leaf_y = y + int(bw * 0.63)
        pygame.draw.rect(screen, leaf_green, (leaf_x, leaf_y, leaf_w, leaf_h))
        # taper the far end of the leaf slightly darker
        pygame.draw.rect(screen, sepal_green, (leaf_x, leaf_y, max(1, leaf_w // 3), leaf_h))

        # --- Sepal (base of flower, dark green) ---
        sepal_w = int(bw * 0.30)
        sepal_h = max(2, int(bw * 0.07))
        sepal_y = y + int(bw * 0.40)
        pygame.draw.rect(screen, sepal_green, (cx - sepal_w // 2, sepal_y, sepal_w, sepal_h))

        # --- Lower petal row (widest, dark red — gives depth/base) ---
        low_w = int(bw * 0.42)
        low_h = int(bw * 0.08)
        low_y = y + int(bw * 0.33)
        pygame.draw.rect(screen, petal_dark, (cx - low_w // 2, low_y, low_w, low_h))

        # --- Mid petal row (main red) ---
        mid_w = int(bw * 0.36)
        mid_h = int(bw * 0.09)
        mid_y = y + int(bw * 0.25)
        pygame.draw.rect(screen, petal_main, (cx - mid_w // 2, mid_y, mid_w, mid_h))

        # --- Top petal row (highlight, narrow — the bud tip) ---
        top_w = int(bw * 0.22)
        top_h = int(bw * 0.07)
        top_y = y + int(bw * 0.20)
        pygame.draw.rect(screen, petal_hi, (cx - top_w // 2, top_y, top_w, top_h))

        # --- Left-edge shadow on mid and lower rows for a subtle bud depth ---
        shadow_w = max(1, int(bw * 0.04))
        pygame.draw.rect(screen, petal_dark, (cx - low_w // 2, low_y, shadow_w, low_h))
        pygame.draw.rect(screen, petal_dark, (cx - mid_w // 2, mid_y, shadow_w, mid_h))
    