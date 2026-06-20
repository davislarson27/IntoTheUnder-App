import pygame
from math import floor
import random

from world.blocks.block_types._base import Block
from world.blocks.block_types.terrain import Grass, Dirt

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

        primary_color = (102, 87, 72)
        secondary_color = (44, 29, 14)
        
        pygame.draw.rect( # draw base color
            screen,
            (primary_color[0] + added_color, primary_color[1] + added_color, primary_color[2] + added_color),
            (x, y, block_width, block_width)
        )
        pygame.draw.rect(
            screen,
            (secondary_color[0] + added_color, secondary_color[1] + added_color, secondary_color[2] + added_color),
            ((x) + floor(block_width * 0.15) , y + floor(block_width * 0.25), block_width // 25, block_width // 1.75)
        )
        pygame.draw.rect(
            screen,
            (secondary_color[0] + added_color, secondary_color[1] + added_color, secondary_color[2] + added_color),
            ((x) + (block_width // 2) , y + (block_width // 3), block_width // 25, block_width // 1.75)
        )
        pygame.draw.rect(
            screen,
            (secondary_color[0] + added_color, secondary_color[1] + added_color, secondary_color[2] + added_color),
            ((x) + floor(block_width * 0.8) , y + floor(block_width * 0.2), block_width // 25, block_width // 1.75)
        )

class Leaves(Block):
    str_name = "Leaves"
    ticks_to_mine = 18
    sappling_drop_chance = 0.12

    tick_threshold = 60

    def onDestroy(self, inventory=None):
        self.grid.set(self.x, self.y, None)
        if random.random() < self.sappling_drop_chance:
            for y in range(self.y, self.y + 8):
                if isinstance(self.grid.get(self.x, y), Tree_Sappling):
                    return None
            self.grid.set(self.x, self.y, Tree_Sappling, pass_through=True)
        return None

    def physics(self):
        if self.anchor_x is not None and self.anchor_y is not None:
            if self.ticks_till_physics > self.tick_threshold:
                self.onDestroy()
            else:
                if self.grid.get(self.anchor_x, self.anchor_y) is None:
                    self.ticks_till_physics += 1

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

class Iron_Ladder(Block):

    # remember to update the blocks_list for loading when you add a new type of block :)

    str_name = "Iron Ladder"
    tick_threshold = 30
    pass_through = True

    draw_background = True

    @staticmethod
    def accel_reduction(accel):
        return 0

    @staticmethod
    def velocity_reduction(velocity):
        return velocity

    @staticmethod
    def draw_manual(screen, x, y, block_width, being_mined=False, is_grid_coordinates=True, use_alt_drawing=False):
        added = 20 if being_mined else 0

        if is_grid_coordinates:
            x *= block_width
            y *= block_width

        # Darker wood rails
        rail_color = (
            min(255, 130 + added),
            min(255, 102 + added),
            min(255, 78 + added)
        )

        # Grey/silver rungs
        rung_color = (
            min(255, 155 + added),
            min(255, 155 + added),
            min(255, 155 + added)
        )
        rung_dark = (
            min(255, 120 + added),
            min(255, 120 + added),
            min(255, 120 + added)
        )

        rail_w = max(2, block_width // 7)
        rung_h = max(2, block_width // 10)
        padding = max(1, block_width // 12)

        left_x = x + padding
        right_x = x + block_width - padding - rail_w

        # Rails (full height)
        pygame.draw.rect(screen, rail_color, (left_x, y, rail_w, block_width))
        pygame.draw.rect(screen, rail_color, (right_x, y, rail_w, block_width))

        # Rungs
        rung_count = 4

        # Even spacing, but shifted slightly downward
        step = block_width / rung_count
        vertical_shift = max(1, block_width // 12)   # tweak this

        for i in range(rung_count):
            rung_y = int(y + i * step + vertical_shift)

            # keep rung inside tile
            rung_y = min(rung_y, y + block_width - rung_h)

            pygame.draw.rect(
                screen,
                rung_color,
                (left_x + rail_w, rung_y, right_x - (left_x + rail_w), rung_h)
            )

class Wood_Ladder(Block):

    # remember to update the blocks_list for loading when you add a new type of block :)

    str_name = "Wood Ladder"
    tick_threshold = 30
    pass_through = True

    draw_background = True

    @staticmethod
    def draw_manual(screen, x, y, block_width, being_mined=False, is_grid_coordinates=True, use_alt_drawing=False):
        added = 20 if being_mined else 0

        if is_grid_coordinates:
            x *= block_width
            y *= block_width

        # Slightly darker than planks
        rail_color = (
            min(255, 130 + added),
            min(255, 102 + added),
            min(255, 78 + added)
        )
        rung_color = (
            min(255, 150 + added),
            min(255, 120 + added),
            min(255, 95 + added)
        )

        # Geometry (full height, wider)
        rail_w = max(2, block_width // 7)
        rung_h = max(2, block_width // 10)

        padding = max(1, block_width // 12)

        left_x = x + padding
        right_x = x + block_width - padding - rail_w

        # FULL HEIGHT rails (key change)
        pygame.draw.rect(screen, rail_color, (left_x, y, rail_w, block_width))
        pygame.draw.rect(screen, rail_color, (right_x, y, rail_w, block_width))

        # Rungs
        rung_count = 4

        # Even spacing, but shifted slightly downward
        step = block_width / rung_count
        vertical_shift = max(1, block_width // 12)   # tweak this

        for i in range(rung_count):
            rung_y = int(y + i * step + vertical_shift)

            # keep rung inside tile
            rung_y = min(rung_y, y + block_width - rung_h)

            pygame.draw.rect(
                screen,
                rung_color,
                (left_x + rail_w, rung_y, right_x - (left_x + rail_w), rung_h)
            )

class Snow_Leaves(Leaves):
    str_name = "Snow Leaves"
    ticks_to_mine = 19

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

        base_snow_color = (225 + added_color, 245 + added_color, 215 + added_color)
        snow_color = (min(base_snow_color[0], 255), min(base_snow_color[1], 255), min(base_snow_color[2], 255))

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
            pygame.draw.circle(screen, snow_color, (cx, cy), r)

        # Optional tiny “cluster dot” that is ALWAYS in the same place (still not random)
        # (This mimics your occasional extra dot without RNG.)
        cx = int(px + pad + 0.48 * (block_width - 2 * pad))
        cy = int(py + pad + 0.46 * (block_width - 2 * pad))
        pygame.draw.circle(screen, snow_color, (cx, cy), 1)

class Snow_Leaves_Top(Leaves):
    str_name = "Snow Leaves Top"
    ticks_to_mine = 19

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

        base_snow_color = (225 + added_color, 245 + added_color, 215 + added_color)
        snow_color = (min(base_snow_color[0], 255), min(base_snow_color[1], 255), min(base_snow_color[2], 255))

        pygame.draw.rect(screen, snow_color, (px, py, block_width, int(block_width * 0.15)))

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
            pygame.draw.circle(screen, snow_color, (cx, cy), r)

        # Optional tiny “cluster dot” that is ALWAYS in the same place (still not random)
        # (This mimics your occasional extra dot without RNG.)
        cx = int(px + pad + 0.48 * (block_width - 2 * pad))
        cy = int(py + pad + 0.46 * (block_width - 2 * pad))
        pygame.draw.circle(screen, snow_color, (cx, cy), 1)

class Tree_Sappling(Block):

    str_name = "Tree Sapling"
    ticks_to_mine = 12
    pass_through = True
    draw_background = True
    ignore_shading_from = {
        (0, 1): True,
        (0, -1): True,
        (1, 0): True,
        (-1, 0): True
    }
    tick_threshold = 2
    grow_tick_threshold = 4000

    def physics(self):
        if self.grid.in_bounds(self.x, self.y + 1):
            if self.grid.get(self.x, self.y + 1) is None: # this means that the block under is empty
                if self.ticks_till_physics < self.tick_threshold:
                    self.ticks_till_physics += 1
                else: #tick count has reached go time to fall
                    self.grid.set(self.x, self.y, None)
                    self.grid.set(self.x, self.y+1, Tree_Sappling)
                    self.ticks_till_physics = 0
            else: # this means that growing can continue
                block_below = self.grid.get(self.x, self.y+1)
                if not isinstance(block_below, Grass) and not isinstance(block_below, Dirt):
                        self.ticks_till_physics = 0
                        return
                if not (self.grid.in_bounds(self.x-1, self.y-self.full_tree_height+1) and self.grid.in_bounds(self.x+1, self.y-self.full_tree_height+1)):
                    self.ticks_till_physics = 0
                    return
                for y in range(self.y - self.full_tree_height + 1, self.y):
                    for x in range(self.x - 1, self.x + 2):
                        if self.grid.get(x, y) is not None:
                            self.ticks_till_physics = 0
                            return
                    
                if self.ticks_till_physics > self.grow_tick_threshold:
                    self.grow_tree()
                else:
                    self.ticks_till_physics += 1

    def grow_tree(self):
        from world.world_creation.structures.structures import Tree
        tree_instructions = Tree.getStructureInstructions(self.x-1, self.y+1, self.grid, random.random())
        for instruct in tree_instructions:
            instruct.setBlock(self.grid)

    def special_init(self):
        max_tree_height = 4 # includes leaves
        self.tree_height = max_tree_height + 3
        self.full_tree_height = self.tree_height + 3 # includes the height of the leaves
    
    @staticmethod
    def draw_manual(screen, x, y, block_width, being_mined=False, is_grid_coordinates=True, use_alt_drawing=False):
        added = 25 if being_mined else 0

        if is_grid_coordinates:
            x *= block_width
            y *= block_width

        bw = block_width

        def c(rgb):
            return (min(255, rgb[0] + added), min(255, rgb[1] + added), min(255, rgb[2] + added))

        bark      = c((88, 65, 42))
        bark_dark = c((60, 42, 24))
        # Match the actual Leaves block palette
        leaf_base = c((120, 155, 110))
        leaf_dark = c((112, 147, 102))
        leaf_hi   = c((126, 161, 116))

        mid_x = x + bw // 2

        # Trunk — runs bottom 60% of tile
        trunk_w = max(3, int(bw * 0.13))
        trunk_x = mid_x - trunk_w // 2
        trunk_top = y + int(bw * 0.40)
        pygame.draw.rect(screen, bark, (trunk_x, trunk_top, trunk_w, bw - int(bw * 0.40)))
        pygame.draw.rect(screen, bark_dark, (trunk_x, trunk_top, max(1, trunk_w // 3), bw - int(bw * 0.40)))

        # Short side branches
        branch_y = y + int(bw * 0.44)
        branch_h = max(2, int(bw * 0.05))
        branch_len = int(bw * 0.18)
        pygame.draw.rect(screen, bark, (trunk_x - branch_len, branch_y, branch_len, branch_h))
        pygame.draw.rect(screen, bark, (trunk_x + trunk_w, branch_y, branch_len, branch_h))

        def leaf_cluster(rx, ry, rw, rh):
            pygame.draw.rect(screen, leaf_dark, (rx, ry, rw, rh))
            pygame.draw.rect(screen, leaf_base, (rx + int(bw * 0.03), ry + int(bw * 0.03), max(1, rw - int(bw * 0.06)), max(1, rh - int(bw * 0.06))))
            pygame.draw.rect(screen, leaf_hi,   (rx + int(bw * 0.05), ry + int(bw * 0.03), max(1, rw - int(bw * 0.10)), max(1, int(bw * 0.05))))

        # Leaf clusters at branch ends
        cluster_w = int(bw * 0.28)
        cluster_h = int(bw * 0.24)
        cluster_y = branch_y - int(bw * 0.16)
        for ox in (trunk_x - branch_len - cluster_w // 2, trunk_x + trunk_w + branch_len - cluster_w // 2):
            leaf_cluster(ox, cluster_y, cluster_w, cluster_h)

        # Top canopy sitting above the trunk
        top_w = int(bw * 0.40)
        top_h = int(bw * 0.24)
        top_y = y + int(bw * 0.07)
        top_x = x + (bw - top_w) // 2 + 1
        leaf_cluster(top_x, top_y, top_w, top_h)
