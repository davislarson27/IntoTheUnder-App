import pygame
from math import floor

# remember to update the blocks_list for loading when you add a new type of block :)

class Block:

    ticks_to_mine = 30
    tick_threshold = 0

    can_place = True
    can_store_items = False

    def __init__(self, grid, screen, grid_x, grid_y, block_width, pass_through = False, ticks_till_physics = 0, stored_inventory_items=None, special_value=True):
        self.grid = grid
        self.screen = screen
        self.x = grid_x
        self.y = grid_y
        self.block_width = block_width
        self.cur_selected = False
        self.pass_through = pass_through
        self.ticks_till_physics = ticks_till_physics
        self.special_value = special_value
        if stored_inventory_items is not None:
            self.stored_inventory_items = stored_inventory_items
        else:
            self.stored_inventory_items = []


    def interaction(self, inventory):
        return False
    
    def get_stored_inventory_items(self):
        return_list = []
        if len(self.stored_inventory_items) > 0:
            for item in self.stored_inventory_items:
                if item is None:
                    return_list.append(None)
                else:
                    return_list.append(item.rerender_as_array())
            return return_list
        else:
            return None

    def can_move_to_inventory(self):
        return True
    
    def draw_manual(screen, x, y, block_width, being_mined=False, is_grid_coordinates=True, use_alt_drawing=False):
        return
    
    def draw(self, being_mined = False, camera_x = 0, camera_y = 0):
        pixel_self_x = self.x * self.block_width
        pixel_self_y = self.y * self.block_width

        draw_x = pixel_self_x - camera_x
        draw_y = pixel_self_y - camera_y

        self.draw_manual(self.screen, draw_x, draw_y, self.block_width, being_mined, False, self.pass_through)

    def physics(self):
        return
    
    def onDestruction(self, inventory=None):
        return

class Item(Block):
    can_place = False

class Ingot(Item): # this is just here to help draw other ingots
    @staticmethod
    def draw_ingot_manual(screen, x, y, block_width, base_color, being_mined=False, is_grid_coordinates=True):
        added = 20 if being_mined else 0

        if is_grid_coordinates:
            x *= block_width
            y *= block_width

        # ----- helpers -----
        def clamp(c):
            return max(0, min(255, c))

        def shade(rgb, delta):
            r, g, b = rgb
            return (clamp(r + delta), clamp(g + delta), clamp(b + delta))

        base = shade(base_color, added)
        outline = shade(base, -55)
        shadow  = shade(base, -35)
        light   = shade(base, +25)
        shine   = shade(base, +45)

        # ----- geometry -----
        bar_w = int(block_width * 0.78)
        bar_h = int(block_width * 0.28)

        bx = x + (block_width - bar_w) // 2
        by = y + (block_width - bar_h) // 2

        cham = max(2, bar_h // 2)
        border = max(1, block_width // 24)

        # Main polygon (horizontal bar with diagonal ends)
        pts = [
            (bx + cham, by),
            (bx + bar_w - cham, by),
            (bx + bar_w, by + bar_h // 2),
            (bx + bar_w - cham, by + bar_h),
            (bx + cham, by + bar_h),
            (bx, by + bar_h // 2),
        ]

        pygame.draw.polygon(screen, base, pts)
        pygame.draw.polygon(screen, outline, pts, width=border)

        # Top highlight
        inset = border + 1
        top_h = max(2, bar_h // 3)

        pts_top = [
            (bx + cham + inset, by + inset),
            (bx + bar_w - cham - inset, by + inset),
            (bx + bar_w - inset, by + top_h),
            (bx + inset, by + top_h),
        ]

        pygame.draw.polygon(screen, light, pts_top)

        # Bottom shadow
        bot_h = max(2, bar_h // 3)

        pts_bot = [
            (bx + inset, by + bar_h - bot_h),
            (bx + bar_w - inset, by + bar_h - bot_h),
            (bx + bar_w - cham - inset, by + bar_h - inset),
            (bx + cham + inset, by + bar_h - inset),
        ]

        pygame.draw.polygon(screen, shadow, pts_bot)

        # Shine notch
        notch_w = max(3, bar_w // 8)
        notch_h = max(2, top_h // 2)
        pygame.draw.rect(screen, shine,
                        (bx + cham + inset + 1, by + inset + 1, notch_w, notch_h))

        # ----- subtle ITU stamp -----
        stamp_color = shade(base, -28)

        stamp_h = max(3, bar_h // 2)
        stamp_w = max(1, bar_h // 10)

        sx = bx + bar_w // 2
        sy = by + (bar_h - stamp_h) // 2

        gap = max(1, stamp_w)
        letter_w = stamp_w * 2

        # I
        pygame.draw.rect(screen, stamp_color,
                        (sx - (letter_w*3 + gap*2)//2, sy, stamp_w, stamp_h))

        # T
        tx = sx - (letter_w + gap)//2
        pygame.draw.rect(screen, stamp_color, (tx, sy, letter_w, stamp_w))
        pygame.draw.rect(screen, stamp_color,
                        (tx + letter_w//2 - stamp_w//2, sy, stamp_w, stamp_h))

        # U
        ux = sx + (letter_w + gap)//2
        pygame.draw.rect(screen, stamp_color, (ux, sy, stamp_w, stamp_h))
        pygame.draw.rect(screen, stamp_color,
                        (ux + letter_w - stamp_w, sy, stamp_w, stamp_h))
        pygame.draw.rect(screen, stamp_color,
                        (ux, sy + stamp_h - stamp_w, letter_w, stamp_w))

class PowderPile(Item):
    @staticmethod
    def draw_manual(
        screen,
        x,
        y,
        block_width,
        powder_color=(205, 205, 65),
        being_mined=False,
        is_grid_coordinates=True,
        use_alt_drawing=False
    ):
        """
        Clean, Minecraft-like powder pile (same shape for all powders, only color changes),
        but tuned to NOT read like a perfect pyramid:

        - Slight asymmetry (left-lean vs right-lean depending on use_alt_drawing)
        - Sits a tad lower so inventory count in top-left doesn't cover the peak
        - Slightly larger footprint for readability
        - Minimal highlights + minimal dust (not busy)
        """

        # ---------------- helpers ---------------- #
        def clamp(v): 
            return 0 if v < 0 else (255 if v > 255 else v)

        def shade(c, d):
            return (clamp(c[0] + d), clamp(c[1] + d), clamp(c[2] + d))

        def mix(a, b, t):
            return (
                int(a[0] + (b[0] - a[0]) * t),
                int(a[1] + (b[1] - a[1]) * t),
                int(a[2] + (b[2] - a[2]) * t),
            )

        # ---------------- position ---------------- #
        added = 18 if being_mined else 0

        if is_grid_coordinates:
            px = x * block_width
            py = y * block_width
        else:
            px, py = x, y

        # Slightly larger than before (was 0.92)
        target = int(block_width * 0.95)
        cell = max(1, target // 16)
        size = cell * 16
        ox = px + (block_width - size) // 2
        oy = py + (block_width - size) // 2

        def p(ix, iy, color):
            pygame.draw.rect(
                screen,
                color,
                (ox + ix * cell, oy + iy * cell, cell, cell)
            )

        # ---------------- palette (simple) ---------------- #
        base = shade(powder_color, added)

        # Strong outline to pop on light slot backgrounds
        outline = shade(base, -40)

        # Limited tones to keep it clean
        fill = shade(base, -18)
        highlight = shade(base, +28)

        # Dust: slightly darker than slot bg + lightly tinted
        dust_a = mix((175, 175, 182), base, 0.15)
        dust_b = mix((145, 145, 155), base, 0.12)

        # Sit lower to avoid top-left count overlap + feel grounded
        y_shift = 2
        def Y(v): return v + y_shift

        # ---------------- fixed base shape ---------------- #
        # Core silhouette (symmetrical template)
        outline_px = [
            (7, Y(2)),
            (6, Y(3)), (7, Y(3)), (8, Y(3)),
            (5, Y(4)), (6, Y(4)), (7, Y(4)), (8, Y(4)), (9, Y(4)),
            (4, Y(5)), (5, Y(5)), (6, Y(5)), (7, Y(5)), (8, Y(5)), (9, Y(5)), (10, Y(5)),
            (3, Y(6)), (4, Y(6)), (5, Y(6)), (6, Y(6)), (7, Y(6)), (8, Y(6)), (9, Y(6)), (10, Y(6)), (11, Y(6)),
            (2, Y(7)), (3, Y(7)), (4, Y(7)), (5, Y(7)), (6, Y(7)), (7, Y(7)), (8, Y(7)), (9, Y(7)), (10, Y(7)), (11, Y(7)), (12, Y(7)),

            # thick base slab
            (1, Y(8)), (2, Y(8)), (3, Y(8)), (4, Y(8)), (5, Y(8)), (6, Y(8)),
            (7, Y(8)), (8, Y(8)), (9, Y(8)), (10, Y(8)), (11, Y(8)), (12, Y(8)), (13, Y(8)),

            # base lip
            (0, Y(9)), (1, Y(9)), (13, Y(9)), (14, Y(9)),
        ]

        # ---------------- anti-pyramid asymmetry ---------------- #
        # We keep the SAME "family" shape, but slightly lean it:
        # - default: shave one pixel off upper-right shoulder + add one on lower-left
        # - alt:     shave one pixel off upper-left shoulder + add one on lower-right
        if not use_alt_drawing:
            # shave right shoulder
            if (9, Y(4)) in outline_px:
                outline_px.remove((9, Y(4)))
            # subtle left bulge
            outline_px.append((1, Y(7)))
        else:
            # shave left shoulder
            if (5, Y(4)) in outline_px:
                outline_px.remove((5, Y(4)))
            # subtle right bulge
            outline_px.append((12, Y(7)))

        # Slightly wider base feel (tiny, consistent)
        # Helps it read like a pile instead of a perfect triangle.
        outline_px.append((2, Y(9)))

        # Draw outline
        for ix, iy in outline_px:
            p(ix, iy, outline)

        # ---------------- fill (single clean tone) ---------------- #
        fill_px = [
            (7, Y(3)),
            (6, Y(4)), (7, Y(4)), (8, Y(4)),
            (5, Y(5)), (6, Y(5)), (7, Y(5)), (8, Y(5)), (9, Y(5)),
            (4, Y(6)), (5, Y(6)), (6, Y(6)), (7, Y(6)), (8, Y(6)), (9, Y(6)), (10, Y(6)),
            (3, Y(7)), (4, Y(7)), (5, Y(7)), (6, Y(7)), (7, Y(7)), (8, Y(7)), (9, Y(7)), (10, Y(7)), (11, Y(7)),
            (2, Y(8)), (3, Y(8)), (4, Y(8)), (5, Y(8)), (6, Y(8)), (7, Y(8)),
            (8, Y(8)), (9, Y(8)), (10, Y(8)), (11, Y(8)), (12, Y(8)),
        ]
        for ix, iy in fill_px:
            p(ix, iy, fill)

        # ---------------- minimal highlights ---------------- #
        # Consistent highlight placement, but shifted with the lean
        if not use_alt_drawing:
            highlight_px = [(8, Y(6)), (9, Y(7))]
        else:
            highlight_px = [(6, Y(6)), (7, Y(7))]

        for ix, iy in highlight_px:
            p(ix, iy, highlight)

        # ---------------- minimal dust ---------------- #
        # Enough to say "powder" but not noisy.
        dust_px = [
            (6, Y(9)), (7, Y(9)), (8, Y(9)),  # tiny band under base
            (2, Y(10)),                        # left stray
            (13, Y(10)),                       # right stray
        ]

        # Slight variation so stacks don't all look identical
        if use_alt_drawing:
            dust_px.append((10, Y(10)))
        else:
            dust_px.append((4, Y(10)))

        for i, (ix, iy) in enumerate(dust_px):
            p(ix, iy, dust_a if i % 2 == 0 else dust_b)

        # Optional single micro-speck for big tiles only (still subtle)
        if block_width >= 40:
            p(5, Y(7), shade(highlight, -20))


class Iron_Ingot(Item):
    str_name = "Iron Ingot"

    @staticmethod
    def draw_manual(screen, x, y, block_width, being_mined=False, is_grid_coordinates=True, use_alt_drawing=False):
        iron_base_color = (185, 188, 196)
        Ingot.draw_ingot_manual(screen, x, y, block_width, iron_base_color, being_mined, is_grid_coordinates)

class Gold_Ingot(Item):
    str_name = "Gold Ingot"

    @staticmethod
    def draw_manual(screen, x, y, block_width, being_mined=False, is_grid_coordinates=True, use_alt_drawing=False):
        ingot_gold_base = (210, 205, 95)
        Ingot.draw_ingot_manual(screen, x, y, block_width, ingot_gold_base, being_mined, is_grid_coordinates)

class Rock(Block):

    # remember to update the blocks_list for loading when you add a new type of block :)

    str_name = "Rock"
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

        pygame.draw.rect(
            screen,
            (70 + added_color, 75 + added_color, 80 + added_color),
            (x, y, block_width, block_width)
        )
        pygame.draw.rect(
            screen,
            (90 + added_color, 95 + added_color, 100 + added_color),
            ((x) + (block_width // 10) , (y) + (block_width // 10), block_width // 4, block_width // 4)
        )

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

class Dirt(Block):

    # remember to update the blocks_list for loading when you add a new type of block :)

    str_name = "Dirt"

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
            (150 + added_color, 130 + added_color, 110 + added_color),           # color
            (x, y, block_width, block_width)
        )
        pygame.draw.rect(
            screen,
            (140 + added_color, 120 + added_color, 110 + added_color),           # color
            ((x) + (block_width // 10) , y + (block_width // 10), block_width // 4, block_width // 4)
        )

class Grass(Block):

    # remember to update the blocks_list for loading when you add a new type of block :)

    str_name = "Grass"

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
            (150 + added_color, 130 + added_color, 110 + added_color),           # color
            (x, y, block_width, block_width)
        )
        pygame.draw.rect( # draw rectangle for grass
            screen,
            (120 + added_color, 135 + added_color, 110 + added_color),           # color
            ((x), (y), block_width, block_width // 3)
        )

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
            (85 + added_color, 70 + added_color, 55 + added_color),           # color
            (x, y, block_width, block_width)
        )
        pygame.draw.rect(
            screen,
            (40 + added_color, 25 + added_color, 10 + added_color),           # color
            ((x) + floor(block_width * 0.15) , y + floor(block_width * 0.25), block_width // 25, block_width // 1.75)
        )
        pygame.draw.rect(
            screen,
            (40 + added_color, 25 + added_color, 10 + added_color),           # color
            ((x) + (block_width // 2) , y + (block_width // 3), block_width // 25, block_width // 1.75)
        )
        pygame.draw.rect(
            screen,
            (40 + added_color, 25 + added_color, 10 + added_color),           # color
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

class Sand(Block):

    # remember to update the blocks_list for loading when you add a new type of block :)

    str_name = "Sand"
    ticks_to_mine = 24
    tick_threshold = 2

    def physics(self):
        if self.grid.in_bounds(self.x, self.y + 1): #checks for block directly under the water
            if self.grid.get(self.x, self.y + 1) is None: # this means that the block under is empty!!
                if self.ticks_till_physics < self.tick_threshold:
                    self.ticks_till_physics += 1
                else: #tick count has reached go time :)
                    self.grid.set(self.x, self.y, None)
                    self.grid.set(self.x, self.y+1, Sand, False)
                    self.ticks_till_physics = 0


    @staticmethod
    def draw_manual(screen, x, y, block_width, being_mined=False, is_grid_coordinates=True, use_alt_drawing=False):
        if being_mined:
            added_color = 20
        else:
            added_color = 0

        if is_grid_coordinates:
            x *= block_width
            y *= block_width

        # (200, 185, 150) (210, 195, 155) (205, 203, 198) (185, 182, 172) (170, 168, 158)
        
        pygame.draw.rect( # draw base color
            screen,
            (215 + added_color, 200 + added_color, 155 + added_color),           # color
            (x, y, block_width, block_width)
        )

        spec_width = 1
        for sub_y in range(y + 1, y+block_width, spec_width * 3):
            for sub_x in range(x + 1, x+block_width , spec_width * 3):
                pygame.draw.rect(
                    screen,
                    (170 + added_color, 168 + added_color, 158 + added_color),           # color
                    (sub_x , sub_y, spec_width, spec_width)
                )

class Gravel(Block):

    # remember to update the blocks_list for loading when you add a new type of block :)

    str_name = "Gravel"
    ticks_to_mine = 24
    tick_threshold = 2

    def physics(self):
        if self.grid.in_bounds(self.x, self.y + 1): #checks for block directly under the water
            if self.grid.get(self.x, self.y + 1) is None: # this means that the block under is empty!!
                if self.ticks_till_physics < self.tick_threshold:
                    self.ticks_till_physics += 1
                else: #tick count has reached go time :)
                    self.grid.set(self.x, self.y, None)
                    self.grid.set(self.x, self.y+1, Gravel, False)
                    # self.y += 1
                    self.ticks_till_physics = 0


    @staticmethod
    def draw_manual(screen, x, y, block_width, being_mined=False, is_grid_coordinates=True, use_alt_drawing=False):
        if being_mined:
            added_color = 20
        else:
            added_color = 0

        if is_grid_coordinates:
            x *= block_width
            y *= block_width

        # (90 + added_color, 95 + added_color, 100 + added_color)
        
        pygame.draw.rect( # draw base color
            screen,
            (100 + added_color, 105 + added_color, 110 + added_color),           # color
            (x, y, block_width, block_width)
        )

        spec_width = 1
        for sub_y in range(y + 1, y+block_width, spec_width * 3):
            for sub_x in range(x + 1, x+block_width , spec_width * 3):
                pygame.draw.rect(
                    screen,
                    (140 + added_color, 135 + added_color, 140 + added_color),           # color
                    (sub_x , sub_y, spec_width, spec_width)
                )

class Cactus(Block): #not yet designed

    # remember to update the blocks_list for loading when you add a new type of block :)

    str_name = "Cactus"

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
            (70 + added_color, 95 + added_color, 60 + added_color),           # color
            (x, y, block_width, block_width)
        )
        pygame.draw.rect(
            screen,
            (40 + added_color, 25 + added_color, 10 + added_color),           # color
            ((x) + floor(block_width * 0.15) , y + floor(block_width * 0.25), block_width // 25, block_width // 1.75)
        )
        pygame.draw.rect(
            screen,
            (40 + added_color, 25 + added_color, 10 + added_color),           # color
            ((x) + (block_width // 2) , y + (block_width // 3), block_width // 25, block_width // 1.75)
        )
        pygame.draw.rect(
            screen,
            (40 + added_color, 25 + added_color, 10 + added_color),           # color
            ((x) + floor(block_width * 0.8) , y + floor(block_width * 0.2), block_width // 25, block_width // 1.75)
        )

class Snow_Block(Block):
    
    # remember to update the blocks_list for loading when you add a new type of block :)

    str_name = "Snow Block"
    ticks_to_mine = 16
    tick_threshold = 2

    def physics(self):
        if self.grid.in_bounds(self.x, self.y + 1): #checks for block directly under the water
            if self.grid.get(self.x, self.y + 1) is None: # this means that the block under is empty!!
                if self.ticks_till_physics < self.tick_threshold:
                    self.ticks_till_physics += 1
                else: #tick count has reached go time :)
                    self.grid.set(self.x, self.y, None)
                    self.grid.set(self.x, self.y+1, Snow_Block, False)
                    # self.y += 1
                    self.ticks_till_physics = 0

    @staticmethod
    def draw_manual(screen, x, y, block_width, being_mined=False, is_grid_coordinates=True, use_alt_drawing=False):
        if being_mined:
            added_color = 9
        else:
            added_color = 0

        if is_grid_coordinates:
            x *= block_width
            y *= block_width
        
        pygame.draw.rect( # draw base color
            screen,
            (225 + added_color, 235 + added_color, 245 + added_color),           # color
            (x, y, block_width, block_width)
        )

class Snow_Man_Head(Block):
    
    # remember to update the blocks_list for loading when you add a new type of block :)

    str_name = "Snow Man Head"
    ticks_to_mine = 16
    tick_threshold = 2

    def physics(self):
        if self.grid.in_bounds(self.x, self.y + 1): #checks for block directly under the water
            if self.grid.get(self.x, self.y + 1) is None: # this means that the block under is empty!!
                if self.ticks_till_physics < self.tick_threshold:
                    self.ticks_till_physics += 1
                else: #tick count has reached go time :)
                    self.grid.set(self.x, self.y, None)
                    self.grid.set(self.x, self.y+1, Snow_Man_Head, False)
                    # self.y += 1
                    self.ticks_till_physics = 0

    @staticmethod
    def draw_manual(screen, x, y, block_width, being_mined=False, is_grid_coordinates=True, use_alt_drawing=False):
        if being_mined:
            added_color = 9
        else:
            added_color = 0

        if is_grid_coordinates:
            x *= block_width
            y *= block_width
        
        pygame.draw.rect( # draw base color
            screen,
            (225 + added_color, 235 + added_color, 245 + added_color),           # color
            (x, y, block_width, block_width)
        )
        pygame.draw.rect(
            screen,
            (10 + added_color, 10 + added_color, 10 + added_color),
            (
                x + (block_width // 4),
                y + (block_width // 3),
                block_width // 8,
                block_width // 8
            )
        )
        pygame.draw.rect(
            screen,
            (10 + added_color, 10 + added_color, 10 + added_color),
            (
                x + ((block_width * 3) // 4) - 1,
                y + (block_width // 3),
                block_width // 8,
                block_width // 8
            )
        )
        # (237, 145, 33)
        pygame.draw.polygon(
            screen,
            (237 + added_color, 145 + added_color, 33 + added_color),
            [
                (x + (block_width // 2), y + (block_width // 2)),
                (x + ((block_width * 3) // 5), y + ((block_width * 3) // 5)),
                (x + ((block_width * 2) // 5), y + ((block_width * 3) // 5))
            ]  
        )

class Ice(Block):
    
    # remember to update the blocks_list for loading when you add a new type of block :)

    str_name = "Ice"
    ticks_to_mine = 36

    @staticmethod
    def draw_manual(screen, x, y, block_width, being_mined=False, is_grid_coordinates=True, use_alt_drawing=False):
        if being_mined:
            added_color = 10
        else:
            added_color = 0

        if is_grid_coordinates:
            x *= block_width
            y *= block_width
        
        #(180, 230, 255)
        pygame.draw.rect( # draw base color
            screen,
            (180 + added_color, 230 + added_color, 245 + added_color),           # color
            (x, y, block_width, block_width)
        )

class Frozen_Rock(Block):

    # remember to update the blocks_list for loading when you add a new type of block :)

    str_name = "Frozen Rock"
    ticks_to_mine = 55

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
        #(145, 155, 165) (175, 190, 205)
        pygame.draw.rect(
            screen,
            (145 + added_color, 155 + added_color, 165 + added_color),           # color
            ((x) + (block_width // 10) , (y) + (block_width // 10), block_width // 4, block_width // 4)
        )

class Chest(Block):

    # remember to update the blocks_list for loading when you add a new type of block :)

    str_name = "Chest"
    ticks_to_mine = 60

    can_store_items = True
    
    def interaction(self, inventory):
        inventory.open_chest(self.stored_inventory_items)
        return True
    
    def onDestruction(self, inventory): # this needs to get called on each block -> needs to give each item to the inventory
        for item in self.stored_inventory_items:
            if item is not None:
                for i in range(item.count_of_items):
                    inventory.add_item(item.Block_Type)

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
            (220 + added_color, 175 + added_color, 138 + added_color),           # color
            (x, y, block_width, block_width)
        )
        pygame.draw.rect( # draw base color
            screen,
            (85 + added_color, 70 + added_color, 55 + added_color),           # color
            (x, y, block_width, block_width),
            2
        )
        pygame.draw.rect( # draw outline
            screen,
            (85 + added_color, 70 + added_color, 55 + added_color),           # color
            (x, y, block_width, block_width),
            floor(block_width * 0.08) # width of border
        )
        pygame.draw.rect( # draw divider between top and bottom of the chest
            screen,
            (85 + added_color, 70 + added_color, 55 + added_color),           # color
            (x, y + floor(block_width * 0.3), block_width, floor(block_width * 0.08))
        )
        pygame.draw.rect(
            screen,
            (140 + added_color, 140 + added_color, 140 + added_color),
            (x + floor(block_width * 0.42), y + floor(block_width * 0.3),floor(block_width * 0.18), floor(block_width * 0.24))
        )

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

class Saltpeter(Block):
    # remember to update the blocks_list for loading when you add a new type of block :)

    str_name = "Saltpeter"

    ticks_to_mine = 45

    @staticmethod
    def draw_manual(screen, x, y, block_width, being_mined=False, is_grid_coordinates=True, use_alt_drawing=False):
        if being_mined:
            added_color = 20
        else:
            added_color = 0

        if is_grid_coordinates:
            x *= block_width
            y *= block_width

        half_len = int(block_width / 2)
        quarter_len = int(block_width / 4)

        outline_w = 1

        main_left_base = (x + outline_w, y + outline_w)
        main_right_base = (x - outline_w + int(block_width * 0.6), y + outline_w)
        main_triangle_tip = (x + quarter_len, y + int(block_width * 0.9) - outline_w)

        main_left_base_outline = (x, y)
        main_right_base_outline = (x + int(block_width * 0.6), y)
        main_triangle_tip_outline = (x + quarter_len, y + int(block_width * 0.9))


        secondary_left_base_outline = (x + half_len, y)
        secondary_right_base_outline = (x + block_width, y)
        secondary_triangle_tip_outline = (x + half_len + quarter_len, y + int(block_width * 0.6))

        secondary_left_base = (x + outline_w + half_len, y + outline_w)
        secondary_right_base = (x - outline_w + block_width, y + outline_w)
        secondary_triangle_tip = (x + half_len + quarter_len, y + int(block_width * 0.6) - outline_w)


        primary_color = (
            205 + added_color, 
            205 + added_color, 
            195 + added_color
        )
        secondary_color = (
            185 + added_color, 
            185 + added_color, 
            175 + added_color
        )
        outline_color = (
            140 + added_color, 
            140 + added_color, 
            132 + added_color
        )


        # --------------- draw tall main stalactite --------------- #
        pygame.draw.polygon( # outline
            screen,
            outline_color,
            [
                main_left_base_outline,
                main_right_base_outline,
                main_triangle_tip_outline
            ]
        )
        pygame.draw.polygon( # body
            screen,
            primary_color,
            [
                main_left_base,
                main_right_base,
                main_triangle_tip
            ]
        )

        # --------------- draw short secondary stalactite --------------- #
        pygame.draw.polygon( # outline
            screen,
            outline_color,
            points = [
                secondary_left_base_outline,
                secondary_right_base_outline,
                secondary_triangle_tip_outline
            ]
        )
        pygame.draw.polygon( # body
            screen,
            secondary_color,
            points = [
                secondary_left_base,
                secondary_right_base,
                secondary_triangle_tip
            ]
        )

class Saltpeter_Powder(Item):
    str_name = "Saltpeter Powder"

    @staticmethod
    def draw_manual(screen, x, y, block_width, being_mined=False, is_grid_coordinates=True, use_alt_drawing=False):
        powder_color = (
            205, 
            205, 
            195
        )

        PowderPile.draw_manual(screen, x, y, block_width, powder_color, being_mined, is_grid_coordinates, use_alt_drawing)


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

class Sulfur_Powder(Item):

    str_name = "Sulfur Powder"

    @staticmethod
    def draw_manual(screen, x, y, block_width, being_mined=False, is_grid_coordinates=True, use_alt_drawing=False):
        powder_color = (
            160,
            170,
            60
        )

        PowderPile.draw_manual(screen, x, y, block_width, powder_color, being_mined, is_grid_coordinates, use_alt_drawing)


class MutliBlock(Block):
    @staticmethod
    def BuildMulti(grid, x, y):
        return False
    
class Door(MutliBlock):
    @staticmethod
    def BuildMulti(grid, x, y):
        y_top = y-1
        if not grid.in_bounds(x, y_top) or grid.get(x, y) is not None or grid.get(x, y_top) is not None:
            y+=1
            y_top+=1
            if not grid.in_bounds(x, y_top) or not grid.in_bounds(x, y) or grid.get(x, y) is not None or grid.get(x, y_top) is not None:
                return False
        grid.set(x, y, Door_Bottom)
        grid.set(x, y_top, Door_Top)
        return True

    # remember to update the blocks_list for loading when you add a new type of block :)

    str_name = "Door"
    ticks_to_mine = 45

    @staticmethod
    def draw_manual(screen, x, y, block_width, being_mined=False, is_grid_coordinates=True, use_alt_drawing=False):
        if is_grid_coordinates:
            x *= block_width
            y *= block_width

        # Create a temporary surface that can hold 2 stacked tiles
        temp_surface = pygame.Surface((block_width, block_width * 2), pygame.SRCALPHA)

        # Draw full-size door halves onto temp surface
        Door_Top.draw_manual(
            temp_surface,
            0,
            0,
            block_width,
            being_mined=being_mined,
            is_grid_coordinates=False
        )

        Door_Bottom.draw_manual(
            temp_surface,
            0,
            block_width,
            block_width,
            being_mined=being_mined,
            is_grid_coordinates=False
        )

        # Scale down to fit inside item slot
        scaled_height = int(block_width * 1)
        scaled_width = int(block_width * 0.5)

        scaled = pygame.transform.smoothscale(
            temp_surface,
            (scaled_width, scaled_height)
        )

        # Center in item slot
        draw_x = x + (block_width - scaled_width) // 2
        draw_y = y + (block_width - scaled_height) // 2

        screen.blit(scaled, (draw_x, draw_y))


class SubMultiBlock(Block):
    def onDestroy(self):
        return

    def interaction(self):
        return False

class Door_Top(SubMultiBlock):
    # special_value -> True = door open, False = door closed

    # remember to update the blocks_list for loading when you add a new type of block :)

    str_name = "Door Top"
    ticks_to_mine = 45

    @staticmethod
    def draw_manual(screen, x, y, block_width, being_mined=False, is_grid_coordinates=True, use_alt_drawing=False):
        added = 20 if being_mined else 0
        if is_grid_coordinates:
            x *= block_width
            y *= block_width

        wood  = (168 + added, 138 + added, 108 + added)
        frame = (140 + added, 112 + added,  86 + added)
        panel = (155 + added, 125 + added,  96 + added)
        metal = ( 60 + added,  50 + added,  40 + added)

        t = max(1, block_width // 10)
        hinge_dot = max(1, block_width // 16)

        hinge_left = True
        is_open = use_alt_drawing

        # OPEN: match bottom (thin slab)
        if is_open:
            slab_w = max(2, block_width // 4)
            slab_x = x if hinge_left else x + (block_width - slab_w)

            pygame.draw.rect(screen, wood, (slab_x, y, slab_w, block_width))

            shadow_w = max(1, t // 2)
            edge_x = slab_x + slab_w - shadow_w if hinge_left else slab_x
            pygame.draw.rect(screen, metal, (edge_x, y, shadow_w, block_width))

            hx = x + max(1, t // 2) if hinge_left else x + block_width - hinge_dot - max(1, t // 2)
            pygame.draw.rect(screen, metal, (hx, y + int(block_width * 0.20), hinge_dot, hinge_dot))
            pygame.draw.rect(screen, metal, (hx, y + int(block_width * 0.65), hinge_dot, hinge_dot))
            return

        # CLOSED: one big panel
        pygame.draw.rect(screen, wood, (x, y, block_width, block_width))
        pygame.draw.rect(screen, frame, (x + t, y + t, block_width - 2 * t, block_width - 2 * t))

        inset_x = x + 2 * t
        inset_y = y + 2 * t
        inset_w = block_width - 4 * t
        inset_h = block_width - 4 * t

        pygame.draw.rect(screen, panel, (inset_x, inset_y, inset_w, inset_h))

        gap = max(1, t)
        inner_w = max(1, t // 2)
        pygame.draw.rect(screen, frame, (inset_x + gap, inset_y + gap, inset_w - 2 * gap, inset_h - 2 * gap), width=inner_w)

        # hinges
        hx = x + max(1, t // 2) if hinge_left else x + block_width - hinge_dot - max(1, t // 2)
        pygame.draw.rect(screen, metal, (hx, y + int(block_width * 0.20), hinge_dot, hinge_dot))
        pygame.draw.rect(screen, metal, (hx, y + int(block_width * 0.65), hinge_dot, hinge_dot))


    def onDestroy(self):
        # get both self and the top and set to none, return a door object
        self.grid.set(self.x, self.y, None)
        y_other_half = self.y+1
        if isinstance(self.grid.get(self.x, y_other_half), Door_Bottom):
            self.grid.set(self.x, self.y, None)
            self.grid.set(self.x, y_other_half, None)
        return Door

    def interaction(self, inventory):
        top_y = self.y + 1
        bottom_half = self.grid.get(self.x, top_y)
        if not isinstance(bottom_half, Door_Bottom):
            return False
        self.pass_through = not self.pass_through
        bottom_half.pass_through = self.pass_through
        return True

class Door_Bottom(SubMultiBlock):
    # special_value -> True = door open, False = door closed
    
    # remember to update the blocks_list for loading when you add a new type of block :)

    str_name = "Door Bottom"
    ticks_to_mine = 45

    @staticmethod
    def draw_manual(screen, x, y, block_width, being_mined=False, is_grid_coordinates=True, use_alt_drawing=False):
        added = 20 if being_mined else 0
        if is_grid_coordinates:
            x *= block_width
            y *= block_width

        wood  = (168 + added, 138 + added, 108 + added)
        frame = (140 + added, 112 + added,  86 + added)
        panel = (155 + added, 125 + added,  96 + added)
        metal = ( 60 + added,  50 + added,  40 + added)

        t = max(1, block_width // 10)
        hinge_dot = max(1, block_width // 16)

        hinge_left = True
        is_open = use_alt_drawing

        # OPEN: match bottom (thin slab)
        if is_open:
            slab_w = max(2, block_width // 4)
            slab_x = x if hinge_left else x + (block_width - slab_w)

            pygame.draw.rect(screen, wood, (slab_x, y, slab_w, block_width))

            shadow_w = max(1, t // 2)
            edge_x = slab_x + slab_w - shadow_w if hinge_left else slab_x
            pygame.draw.rect(screen, metal, (edge_x, y, shadow_w, block_width))

            hx = x + max(1, t // 2) if hinge_left else x + block_width - hinge_dot - max(1, t // 2)
            pygame.draw.rect(screen, metal, (hx, y + int(block_width * 0.20), hinge_dot, hinge_dot))
            pygame.draw.rect(screen, metal, (hx, y + int(block_width * 0.65), hinge_dot, hinge_dot))
            return

        # CLOSED: one big panel
        pygame.draw.rect(screen, wood, (x, y, block_width, block_width))
        pygame.draw.rect(screen, frame, (x + t, y + t, block_width - 2 * t, block_width - 2 * t))

        inset_x = x + 2 * t
        inset_y = y + 2 * t
        inset_w = block_width - 4 * t
        inset_h = block_width - 4 * t

        pygame.draw.rect(screen, panel, (inset_x, inset_y, inset_w, inset_h))

        gap = max(1, t)
        inner_w = max(1, t // 2)
        pygame.draw.rect(screen, frame, (inset_x + gap, inset_y + gap, inset_w - 2 * gap, inset_h - 2 * gap), width=inner_w)

        # hinges
        hx = x + max(1, t // 2) if hinge_left else x + block_width - hinge_dot - max(1, t // 2)
        pygame.draw.rect(screen, metal, (hx, y + int(block_width * 0.20), hinge_dot, hinge_dot))
        pygame.draw.rect(screen, metal, (hx, y + int(block_width * 0.65), hinge_dot, hinge_dot))

        # ---------------- door nob logic ---------------- #
        full_door_top = y - block_width
        full_door_height = block_width * 2
        knobc = (205 + added, 190 + added, 125 + added)
        knob_sz = max(2, block_width // 8)


        # knob vertical position relative to the full door (tweak 0.45–0.50)
        knob_y = full_door_top + int(full_door_height * 0.48)

        # knob horizontal position within this tile
        knob_x = x + block_width - 2 * t - knob_sz if hinge_left else x + 2 * t

        # keep the knob fully inside the bottom tile (so it never clips)
        knob_y = max(y + t, min(knob_y, y + block_width - t - knob_sz))

        pygame.draw.rect(screen, knobc, (knob_x, knob_y, knob_sz, knob_sz))



    def onDestroy(self):
        # get both self and the top and set to none, return a door object
        self.grid.set(self.x, self.y, None)
        y_other_half = self.y-1
        if isinstance(self.grid.get(self.x, y_other_half), Door_Top):
            self.grid.set(self.x, self.y, None)
            self.grid.set(self.x, y_other_half, None)
        return Door

    def interaction(self, inventory):
        top_y = self.y - 1
        top_half = self.grid.get(self.x, top_y)
        if not isinstance(top_half, Door_Top):
            return False
        self.pass_through = not self.pass_through
        top_half.pass_through = self.pass_through
        return True






class Water(Block):

    # remember to update the blocks_list for loading when you add a new type of block :)
    
    str_name = "Water"
    tick_threshold = 20
    water_value = 0
    max_water_value = 4

    def convert_water_value(self, water_value):
        return self.max_water_value + water_value

    def physics(self):
        if self.grid.in_bounds(self.x, self.y + 1) and (issubclass(type(self.grid.get(self.x, self.y + 1)), Water) or self.grid.get(self.x, self.y + 1) is None): # checks for block directly under the water
            if self.ticks_till_physics < self.tick_threshold:
                self.ticks_till_physics += 1
            else: #tick count has reached go time :)
                self.grid.set(self.x, self.y+1, Water, True)
                self.ticks_till_physics = 0
        elif issubclass(type(self.grid.get(self.x, self.y - 1)), Water) and self.water_value != 0:
            if self.ticks_till_physics < self.tick_threshold:
                self.grid.set(self.x, self.y, Water, True)
                self.ticks_till_physics = 0
            else:
                self.ticks_till_physics += 1
        elif self.grid.in_bounds(self.x + 1, self.y) and ((issubclass(type(self.grid.get(self.x, self.y + 1)), Water)) or self.grid.get(self.x + 1, self.y) is None): # check to the right
            if self.ticks_till_physics < self.tick_threshold:
                self.ticks_till_physics += 1
            else: #tick count has reached go time :)
                self.grid.set(self.x + 1, self.y, self.get_right_fill(), True)
                self.ticks_till_physics = 0
        elif self.grid.in_bounds(self.x - 1, self.y) and ((issubclass(type(self.grid.get(self.x, self.y + 1)), Water)) or self.grid.get(self.x - 1, self.y) is None): # check the left
            if self.ticks_till_physics < self.tick_threshold:
                self.ticks_till_physics += 1
            else: #tick count has reached go time :)
                self.grid.set(self.x - 1, self.y, self.get_left_fill(), True)
                self.ticks_till_physics = 0


        if self.water_value > 0: # right block
            left_block = self.grid.get(self.x - 1, self.y)
            if left_block is not None and issubclass(type(left_block), Water):
                if left_block.water_value != self.water_value - 1:
                    if left_block.water_value < self.max_water_value:
                        self.grid.set(self.x, self.y, water_value_reference[self.convert_water_value(left_block.water_value + 1)], True)
            else:
                if self.grid.in_bounds(self.x - 1, self.y):
                    self.grid.set(self.x, self.y, None)
        elif self.water_value < 0: # right block
            right_block = self.grid.get(self.x + 1, self.y)
            if right_block is not None and issubclass(type(right_block), Water):
                if right_block.water_value != self.water_value + 1:
                    if abs(right_block.water_value) < self.max_water_value:
                        self.grid.set(self.x, self.y, water_value_reference[self.convert_water_value(right_block.water_value - 1)], True)
            else:
                if self.grid.in_bounds(self.x + 1, self.y):
                    self.grid.set(self.x, self.y, None)


        if self.water_value != 0:
            left_block = self.grid.get(self.x - 1, self.y)
            right_block = self.grid.get(self.x + 1, self.y)
            if issubclass(type(right_block), Water) and issubclass(type(left_block), Water):
                if abs(right_block.water_value) < 2 and abs(left_block.water_value) < 2:
                    self.grid.set(self.x, self.y, Water, True)


    @staticmethod
    def get_left_fill():
        return Water_L1
                    
    @staticmethod
    def get_right_fill():
        return Water_R1


    def can_move_to_inventory(self):
        return False
    
    @staticmethod
    def accel_reduction(accel):
        return accel // 3
    
    @staticmethod
    def velocity_reduction(velocity):
        return velocity // 2


    @staticmethod
    def draw_manual(screen, x, y, block_width, being_mined=False, is_grid_coordinates=True, use_alt_drawing=False):
        if being_mined:
            added_color = 20
        else:
            added_color = 0

        if is_grid_coordinates:
            x *= block_width
            y *= block_width

        # (40, 110, 170) (80, 160, 200) (25, 80, 130)

        pygame.draw.rect( # draw base color
            screen,
            (40 + added_color, 110 + added_color, 170 + added_color),           # color
            (x, y, block_width, block_width)
        )

class Water_R1(Water):

    # remember to update the blocks_list for loading when you add a new type of block :)
    
    str_name = "Water R1"
    water_value = 1

    @staticmethod
    def get_left_fill():
        return Water
                    
    @staticmethod
    def get_right_fill():
        return Water_R2

                    

    @staticmethod
    def draw_manual(screen, x, y, block_width, being_mined=False, is_grid_coordinates=True, use_alt_drawing=False):
        if being_mined:
            added_color = 20
        else:
            added_color = 0

        if is_grid_coordinates:
            x *= block_width
            y *= block_width

        # (40, 110, 170) (80, 160, 200) (25, 80, 130)
        drop_off_px = block_width // 4
        points = [
            (x, y),             # top-left high
            (x + block_width, y + drop_off_px),  # top-right lower
            (x + block_width, y + block_width),
            (x, y + block_width)
        ]

        pygame.draw.polygon( # draw base color
            screen,
            (40 + added_color, 110 + added_color, 170 + added_color),           # color
            points
        )

class Water_L1(Water):

    # remember to update the blocks_list for loading when you add a new type of block :)
    
    str_name = "Water L1"
    water_value = -1
                    
    @staticmethod
    def get_left_fill():
        return Water_L2
                    
    @staticmethod
    def get_right_fill():
        return Water


    @staticmethod
    def draw_manual(screen, x, y, block_width, being_mined=False, is_grid_coordinates=True, use_alt_drawing=False):
        if being_mined:
            added_color = 20
        else:
            added_color = 0

        if is_grid_coordinates:
            x *= block_width
            y *= block_width

        drop_off_px = block_width // 4
        points = [
            (x, y + drop_off_px),                         # top-left of box
            (x + block_width, y),          # roof peak
            (x + block_width, y + block_width),              # bottom right
            (x, y + block_width)                             # bottom-left

        ]

        pygame.draw.polygon( # draw base color
            screen,
            (40 + added_color, 110 + added_color, 170 + added_color),           # color
            points
        )

class Water_R2(Water):

    # remember to update the blocks_list for loading when you add a new type of block :)
    
    str_name = "Water R2"
    water_value = 2

    @staticmethod
    def get_left_fill():
        return Water_R1
                    
    @staticmethod
    def get_right_fill():
        return Water_R3
      

    @staticmethod
    def draw_manual(screen, x, y, block_width, being_mined=False, is_grid_coordinates=True, use_alt_drawing=False):
        if being_mined:
            added_color = 20
        else:
            added_color = 0

        if is_grid_coordinates:
            x *= block_width
            y *= block_width

        # (40, 110, 170) (80, 160, 200) (25, 80, 130)
        drop_off_px = block_width // 4
        points = [
            (x, y + drop_off_px),
            (x + block_width, y + 2*drop_off_px),
            (x + block_width, y + block_width),
            (x, y + block_width)
        ]

        pygame.draw.polygon( # draw base color
            screen,
            (40 + added_color, 110 + added_color, 170 + added_color),           # color
            points
        )

class Water_L2(Water):

    # remember to update the blocks_list for loading when you add a new type of block :)
    
    str_name = "Water L2"
    water_value = -2

    @staticmethod
    def get_left_fill():
        return Water_L3
                    
    @staticmethod
    def get_right_fill():
        return Water_L1
                

    @staticmethod
    def draw_manual(screen, x, y, block_width, being_mined=False, is_grid_coordinates=True, use_alt_drawing=False):
        if being_mined:
            added_color = 20
        else:
            added_color = 0

        if is_grid_coordinates:
            x *= block_width
            y *= block_width

        # (40, 110, 170) (80, 160, 200) (25, 80, 130)
        drop_off_px = block_width // 4
        points = [
            (x, y + drop_off_px * 2),                         # top-left of box
            (x + block_width, y + drop_off_px),          # roof peak
            (x + block_width, y + block_width),              # bottom right
            (x, y + block_width)                             # bottom-left
        ]

        pygame.draw.polygon( # draw base color
            screen,
            (40 + added_color, 110 + added_color, 170 + added_color),           # color
            points
        )

class Water_R3(Water):

    # remember to update the blocks_list for loading when you add a new type of block :)
    
    str_name = "Water R3"
    water_value = 3

    @staticmethod
    def get_left_fill():
        return Water_R2
                    
    @staticmethod
    def get_right_fill():
        return Water_R4
      

    @staticmethod
    def draw_manual(screen, x, y, block_width, being_mined=False, is_grid_coordinates=True, use_alt_drawing=False):
        if being_mined:
            added_color = 20
        else:
            added_color = 0

        if is_grid_coordinates:
            x *= block_width
            y *= block_width

        # (40, 110, 170) (80, 160, 200) (25, 80, 130)
        drop_off_px = block_width // 4
        points = [
            (x, y + 2 * drop_off_px),
            (x + block_width, y + 3 * drop_off_px),
            (x + block_width, y + block_width),
            (x, y + block_width)
        ]

        pygame.draw.polygon( # draw base color
            screen,
            (40 + added_color, 110 + added_color, 170 + added_color),           # color
            points
        )

class Water_L3(Water):

    # remember to update the blocks_list for loading when you add a new type of block :)
    
    str_name = "Water L3"
    water_value = -3

    @staticmethod
    def get_left_fill():
        return Water_L4
                    
    @staticmethod
    def get_right_fill():
        return Water_L2
                

    @staticmethod
    def draw_manual(screen, x, y, block_width, being_mined=False, is_grid_coordinates=True, use_alt_drawing=False):
        if being_mined:
            added_color = 20
        else:
            added_color = 0

        if is_grid_coordinates:
            x *= block_width
            y *= block_width

        # (40, 110, 170) (80, 160, 200) (25, 80, 130)
        drop_off_px = block_width // 4
        points = [
            (x, y + drop_off_px * 3),                         # top-left of box
            (x + block_width, y + drop_off_px * 2),          # roof peak
            (x + block_width, y + block_width),              # bottom right
            (x, y + block_width)                             # bottom-left
        ]

        pygame.draw.polygon( # draw base color
            screen,
            (40 + added_color, 110 + added_color, 170 + added_color),           # color
            points
        )

class Water_R4(Water):

    # remember to update the blocks_list for loading when you add a new type of block :)
    
    str_name = "Water R4"
    water_value = 4

    @staticmethod
    def get_left_fill():
        return Water_R3
                    
    @staticmethod
    def get_right_fill():
        return None
      

    @staticmethod
    def draw_manual(screen, x, y, block_width, being_mined=False, is_grid_coordinates=True, use_alt_drawing=False):
        if being_mined:
            added_color = 20
        else:
            added_color = 0

        if is_grid_coordinates:
            x *= block_width
            y *= block_width

        # (40, 110, 170) (80, 160, 200) (25, 80, 130)
        drop_off_px = block_width // 4
        points = [
            (x, y + 3 * drop_off_px),
            (x + block_width, y + 4 * drop_off_px),
            (x + block_width, y + block_width),
            (x, y + block_width)
        ]

        pygame.draw.polygon( # draw base color
            screen,
            (40 + added_color, 110 + added_color, 170 + added_color),           # color
            points
        )

class Water_L4(Water):

    # remember to update the blocks_list for loading when you add a new type of block :)
    
    str_name = "Water L4"
    water_value = -4

    @staticmethod
    def get_left_fill():
        # return Water
        return None
                    
    @staticmethod
    def get_right_fill():
        return Water_L3
                

    @staticmethod
    def draw_manual(screen, x, y, block_width, being_mined=False, is_grid_coordinates=True, use_alt_drawing=False):
        if being_mined:
            added_color = 20
        else:
            added_color = 0

        if is_grid_coordinates:
            x *= block_width
            y *= block_width

        # (40, 110, 170) (80, 160, 200) (25, 80, 130)
        drop_off_px = block_width // 4
        points = [
            (x, y + drop_off_px * 4),                         # top-left of box
            (x + block_width, y + drop_off_px * 3),          # roof peak
            (x + block_width, y + block_width),              # bottom right
            (x, y + block_width)                             # bottom-left
        ]

        pygame.draw.polygon( # draw base color
            screen,
            (40 + added_color, 110 + added_color, 170 + added_color),           # color
            points
        )


water_value_reference = [Water_L4, Water_L3, Water_L2, Water_L1, Water, Water_R1, Water_R2, Water_R3, Water_R4]


def get_str_to_block(): # uses blocks_list to generate dictionary that converts str names to their types
    blocks_list = [
        Iron_Ingot,
        Gold_Ingot,
        Rock,
        Iron_Ore_Block,
        Gold_Ore_Block,
        Diamond_Ore_Block,
        Emerald_Ore_Block,
        Mabelite_Ore_Block,
        Coal_Ore_Block,
        Coal,
        Dirt,
        Grass,
        Log,
        Leaves,
        Sand,
        Gravel,
        Cactus,
        Snow_Block,
        Snow_Man_Head,
        Ice,
        Frozen_Rock,
        Chest,
        Door,
        Door_Top,
        Door_Bottom,
        Wood_Planks,
        Saltpeter,
        Saltpeter_Powder,
        Sulfur_Flakes_Block,
        Sulfur_Powder,
        Water, # water subclasses after this
            Water_R1,
            Water_L1,
            Water_R2,
            Water_L2,
            Water_R3,
            Water_L3,
            Water_R4,
            Water_L4
    ]

    blocks_dict = {}
    for block in blocks_list:
        blocks_dict[block.str_name] = block
    return blocks_dict