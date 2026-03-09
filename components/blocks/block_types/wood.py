import pygame
from math import floor
from components.blocks.block_types._base import Block

class Log(Block):

    # remember to update the blocks_list for loading when you add a new type of block :)

    str_name = "Log"
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
        
        pygame.draw.rect( # draw base color
            screen,
            (85 + added_color, 70 + added_color, 55 + added_color),
            (x, y, block_width, block_width)
        )
        pygame.draw.rect(
            screen,
            (40 + added_color, 25 + added_color, 10 + added_color),
            ((x) + floor(block_width * 0.15) , y + floor(block_width * 0.25), block_width // 25, block_width // 1.75)
        )
        pygame.draw.rect(
            screen,
            (40 + added_color, 25 + added_color, 10 + added_color),
            ((x) + (block_width // 2) , y + (block_width // 3), block_width // 25, block_width // 1.75)
        )
        pygame.draw.rect(
            screen,
            (40 + added_color, 25 + added_color, 10 + added_color),
            ((x) + floor(block_width * 0.8) , y + floor(block_width * 0.2), block_width // 25, block_width // 1.75)
        )

class Leaves(Block):
    str_name = "Leaves"
    ticks_to_mine = 18

    # Fixed speck pattern in normalized tile space (0..1).
    # (u, v, r_frac, is_light)
    _SPECK_PATTERN = [
        (0.22, 0.28, 0.07, True),
        (0.62, 0.24, 0.06, False),
        (0.76, 0.55, 0.06, True),
        (0.36, 0.68, 0.05, False),
        (0.55, 0.78, 0.04, True),
    ]

    @staticmethod
    def draw_manual(screen, x, y, block_width, being_mined=False, is_grid_coordinates=True, use_alt_drawing=False):
        added_color = 20 if being_mined else 0

        # IMPORTANT:
        # If is_grid_coordinates=True, x/y must be WORLD TILE coords (not screen coords).
        if is_grid_coordinates:
            px = x * block_width
            py = y * block_width
        else:
            px = x
            py = y

        base = (120 + added_color, 155 + added_color, 110 + added_color)
        pygame.draw.rect(screen, base, (px, py, block_width, block_width))

        # Two close-to-base colors (subtle)
        dark  = (max(base[0] - 8, 0),  max(base[1] - 8, 0),  max(base[2] - 8, 0))
        light = (min(base[0] + 6, 255), min(base[1] + 6, 255), min(base[2] + 6, 255))

        # Keep dots away from edges so tiles blend
        pad = max(1, block_width // 8)

        # Scale radii gently with tile size, clamp small
        def scale_r(r_frac: float) -> int:
            return max(1, min(block_width // 10, int(block_width * r_frac)))

        # Use fewer specks on small tiles (optional)
        specks = Leaves._SPECK_PATTERN
        if block_width < 24:
            specks = specks[:4]

        for (u, v, r_frac, is_light) in specks:
            r = scale_r(r_frac)
            cx = int(px + pad + u * (block_width - 2 * pad))
            cy = int(py + pad + v * (block_width - 2 * pad))
            col = light if is_light else dark
            pygame.draw.circle(screen, col, (cx, cy), r)

        # Optional tiny “cluster dot” that is ALWAYS in the same place (still not random)
        # (This mimics your occasional extra dot without RNG.)
        cx = int(px + pad + 0.48 * (block_width - 2 * pad))
        cy = int(py + pad + 0.46 * (block_width - 2 * pad))
        pygame.draw.circle(screen, dark, (cx, cy), 1)

class Wood_Planks(Block):
    str_name = "Wood Planks"
    ticks_to_mine = 38

    @staticmethod
    def draw_manual(screen, x, y, block_width, being_mined=False, is_grid_coordinates=True, use_alt_drawing=False):
        added = 20 if being_mined else 0
        if is_grid_coordinates:
            x *= block_width
            y *= block_width

        # --- palette (match your door vibe) ---
        base = (168 + added, 138 + added, 108 + added)
        seam = (140 + added, 112 + added,  86 + added)   # darker separator
        grain = (150 + added, 122 + added,  95 + added)  # subtle grain line
        highlight = (182 + added, 152 + added, 120 + added)

        # Fill background
        pygame.draw.rect(screen, base, (x, y, block_width, block_width))

        # Choose plank count (4 reads best at small sizes)
        planks = 4
        plank_h = block_width // planks
        remainder = block_width - plank_h * planks  # distribute leftover pixels

        # Deterministic offsets so blocks look consistent and tile nicely
        # (uses tile position only if you're passing grid coords in; otherwise it's still stable)
        gx = (x // block_width) if is_grid_coordinates else 0
        gy = (y // block_width) if is_grid_coordinates else 0
        seed = (gx * 73856093) ^ (gy * 19349663)

        cur_y = y
        for i in range(planks):
            h = plank_h + (1 if i < remainder else 0)

            # Slight alternating tone per plank
            tone = 6 if (i % 2 == 0) else -6
            plank_color = (min(255, base[0] + tone), min(255, base[1] + tone), min(255, base[2] + tone))
            pygame.draw.rect(screen, plank_color, (x, cur_y, block_width, h))

            # Seam line at the top of each plank (except first)
            if i != 0:
                pygame.draw.rect(screen, seam, (x, cur_y, block_width, 1))

            # Grain line (one per plank) with varying offset/length
            # offsets are deterministic but "random-ish"
            off = ((seed >> (i * 3)) & 0x7)  # 0..7
            start_x = x + max(2, block_width // 10) + off
            length = int(block_width * 0.65) - off
            grain_y = cur_y + h // 2

            # Keep grain line inside plank bounds
            length = max(6, min(length, block_width - (start_x - x) - 2))
            pygame.draw.rect(screen, grain, (start_x, grain_y, length, 1))

            # Small highlight notch near left edge (subtle “wood sheen”)
            notch_w = max(3, block_width // 8)
            notch_x = x + max(2, block_width // 14) + (off // 2)
            notch_y = cur_y + max(1, h // 3)
            pygame.draw.rect(screen, highlight, (notch_x, notch_y, notch_w, 1))

            cur_y += h

        # Bottom seam to frame the tile slightly (optional but helps readability)
        pygame.draw.rect(screen, seam, (x, y + block_width - 1, block_width, 1))

