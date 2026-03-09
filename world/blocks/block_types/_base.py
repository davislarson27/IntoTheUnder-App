import pygame
from math import sqrt

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
        block_type = type(self)
        self.grid.set(self.x, self.y, None)
        return block_type

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

class MutliBlock(Block):
    @staticmethod
    def BuildMulti(grid, x, y):
        return False
    
class SubMultiBlock(Block):
    def onDestroy(self):
        return

    def interaction(self):
        return False

class Explosives(Block): # this is a container for all blocks that explode (helps them find each other)
    blast_power = 0
    blast_radius = 0

    def explode(self):
        # remove self
        self.grid.set(self.x, self.y, None)

        # create blast radius
        for y in range(-self.blast_radius, self.blast_radius + 1):
            for x in range(-self.blast_radius, self.blast_radius + 1):
                if sqrt(y*y + x*x) < self.blast_radius:
                    selected_block = self.grid.get(x + self.x, y + self.y)                        
                    if selected_block is not None:
                        if issubclass(type(selected_block), Explosives):
                            selected_block.interaction(self.inventory) # triggers explosives in the blast radius
                            selected_block.ticks_till_physics = selected_block.tick_threshold - 5
                        else:
                            destroyed_block = selected_block.onDestruction(self.inventory)
                            if destroyed_block is not None:
                                self.inventory.add_item(destroyed_block)
    
    def draw(self, being_mined = False, camera_x = 0, camera_y = 0): # resets the draw function so that it can flash while about to explode
        pixel_self_x = self.x * self.block_width
        pixel_self_y = self.y * self.block_width

        draw_x = pixel_self_x - camera_x
        draw_y = pixel_self_y - camera_y

        flash_interval = self.ticks_till_physics // 20
        if flash_interval % 2 == 1:
            self.draw_manual(self.screen, draw_x, draw_y, self.block_width, True, False, self.pass_through)
        else:
            self.draw_manual(self.screen, draw_x, draw_y, self.block_width, False, False, self.pass_through)
