import pygame
from world.blocks.block_types._base import Block

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

        # # original color
        # primary_background_color = (70, 75, 80)
        # detail_color = (90, 95, 100)

        # new warmer and lighter colors
        primary_background_color = (95, 100, 102)
        detail_color = (115, 120, 122)

        pygame.draw.rect(
            screen,
            (primary_background_color[0] + added_color, primary_background_color[1] + added_color, primary_background_color[2] + added_color),
            (x, y, block_width, block_width)
        )
        pygame.draw.rect(
            screen,
            (detail_color[0] + added_color, detail_color[1] + added_color, detail_color[2] + added_color),
            ((x) + (block_width // 10) , (y) + (block_width // 10), block_width // 4, block_width // 4)
        )

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
        
        base_color = (150, 130, 110)
        secondary_color = (140, 120, 110)
        
        pygame.draw.rect( # draw base color
            screen,
            (base_color[0] + added_color, base_color[1] + added_color, base_color[2] + added_color),
            (x, y, block_width, block_width)
        )
        pygame.draw.rect(
            screen,
            (secondary_color[0] + added_color, secondary_color[1] + added_color, secondary_color[2] + added_color),
            ((x) + (block_width // 10) , y + (block_width // 10), block_width // 4, block_width // 4)
        )

class Packed_Dirt(Block):

    # remember to update the blocks_list for loading when you add a new type of block :)

    str_name = "Packed Dirt"
    ticks_to_mine = 40

    @staticmethod
    def draw_manual(screen, x, y, block_width, being_mined=False, is_grid_coordinates=True, use_alt_drawing=False):
        if being_mined:
            added_color = 20
        else:
            added_color = 0

        if is_grid_coordinates:
            x *= block_width
            y *= block_width

        base_color = (121, 101, 81)
        secondary_color = (135, 115, 95)
        
        pygame.draw.rect( # draw base color
            screen,
            (base_color[0] + added_color, base_color[1] + added_color, base_color[2] + added_color),
            (x, y, block_width, block_width)
        )
        pygame.draw.rect(
            screen,
            (secondary_color[0] + added_color, secondary_color[1] + added_color, secondary_color[2] + added_color),
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
            (150 + added_color, 130 + added_color, 110 + added_color),
            (x, y, block_width, block_width)
        )
        pygame.draw.rect( # draw rectangle for grass
            screen,
            (120 + added_color, 135 + added_color, 110 + added_color),
            ((x), (y), block_width, block_width // 3)
        )

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


        pygame.draw.rect( # draw base color
            screen,
            (215 + added_color, 200 + added_color, 155 + added_color),
            (x, y, block_width, block_width)
        )

        spec_width = 1
        for sub_y in range(y + 1, y+block_width, spec_width * 3):
            for sub_x in range(x + 1, x+block_width , spec_width * 3):
                pygame.draw.rect(
                    screen,
                    (170 + added_color, 168 + added_color, 158 + added_color),
                    (sub_x , sub_y, spec_width, spec_width)
                )

class Sand_Stone(Block):

    # remember to update the blocks_list for loading when you add a new type of block :)

    str_name = "Sand Stone"
    ticks_to_mine = 40

    @staticmethod
    def draw_manual(screen, x, y, block_width, being_mined=False, is_grid_coordinates=True, use_alt_drawing=False):
        if being_mined:
            added_color = 20
        else:
            added_color = 0

        if is_grid_coordinates:
            x *= block_width
            y *= block_width

        base_color = (215, 200, 155)
        secondary_color = (220, 215, 170)
        
        pygame.draw.rect( # draw base color
            screen,
            (base_color[0] + added_color, base_color[1] + added_color, base_color[2] + added_color),
            (x, y, block_width, block_width)
        )
        pygame.draw.rect(
            screen,
            (secondary_color[0] + added_color, secondary_color[1] + added_color, secondary_color[2] + added_color),
            ((x) + (block_width // 10) , y + (block_width // 10), block_width // 4, block_width // 4)
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
        
        color = (180, 230, 245)
        
        pygame.draw.rect( # draw base color
            screen,
            (color[0] + added_color, color[1] + added_color, color[2] + added_color),           # color
            (x, y, block_width, block_width)
        )

class Packed_Ice(Block):
    
    # remember to update the blocks_list for loading when you add a new type of block :)

    str_name = "Packed Ice"
    ticks_to_mine = 50

    @staticmethod
    def draw_manual(screen, x, y, block_width, being_mined=False, is_grid_coordinates=True, use_alt_drawing=False):
        if being_mined:
            added_color = 10
        else:
            added_color = 0

        if is_grid_coordinates:
            x *= block_width
            y *= block_width

        color = (160, 210, 235)
        
        #(180, 230, 255)
        pygame.draw.rect( # draw base color
            screen,
            (color[0] + added_color, color[1] + added_color, color[2] + added_color),           # color
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
            (70 + added_color, 75 + added_color, 80 + added_color),
            (x, y, block_width, block_width)
            
        )
        #(145, 155, 165)
        pygame.draw.rect(
            screen,
            (145 + added_color, 155 + added_color, 165 + added_color),
            ((x) + (block_width // 10) , (y) + (block_width // 10), block_width // 4, block_width // 4)
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
            (225 + added_color, 235 + added_color, 245 + added_color),
            (x, y, block_width, block_width)
        )


### test
class Background_Planks(Block):
    str_name = "Wood Planks Background"
    ticks_to_mine = 38

    @staticmethod
    def draw_manual(screen, x, y, block_width, being_mined=False, is_grid_coordinates=True, use_alt_drawing=False):
        added = 20 if being_mined else 0

        if is_grid_coordinates:
            x *= block_width
            y *= block_width

        # --- palette ---
        base = (168 + added, 138 + added, 108 + added)
        seam = (140 + added, 112 + added, 86 + added)
        grain = (150 + added, 122 + added, 95 + added)
        highlight = (182 + added, 152 + added, 120 + added)

        # Fill background
        pygame.draw.rect(screen, base, (x, y, block_width, block_width))

        # 4 planks
        planks = 4
        plank_h = block_width // planks
        remainder = block_width - plank_h * planks

        cur_y = y
        for i in range(planks):
            h = plank_h + (1 if i < remainder else 0)

            tone = 6 if (i % 2 == 0) else -6
            plank_color = (
                min(255, base[0] + tone),
                min(255, base[1] + tone),
                min(255, base[2] + tone),
            )
            pygame.draw.rect(screen, plank_color, (x, cur_y, block_width, h))

            if i != 0:
                pygame.draw.rect(screen, seam, (x, cur_y, block_width, 1))

            off = (i * 2 + 3) % 8
            start_x = x + max(2, block_width // 10) + off
            length = int(block_width * 0.65) - off
            grain_y = cur_y + h // 2
            length = max(6, min(length, block_width - (start_x - x) - 2))
            pygame.draw.rect(screen, grain, (start_x, grain_y, length, 1))

            notch_w = max(3, block_width // 8)
            notch_x = x + max(2, block_width // 14) + (off // 2)
            notch_y = cur_y + max(1, h // 3)
            pygame.draw.rect(screen, highlight, (notch_x, notch_y, notch_w, 1))

            cur_y += h

        pygame.draw.rect(screen, seam, (x, y + block_width - 1, block_width, 1))

    def draw(self, being_mined=False, camera_x=0, camera_y=0):
            draw_x = self.x * self.block_width - camera_x
            draw_y = self.y * self.block_width - camera_y

            self.draw_manual(
                self.screen,
                draw_x,
                draw_y,
                self.block_width,
                being_mined=being_mined,
                is_grid_coordinates=False
            )

            bw = self.block_width
            technique = "gradient"  # "flat", "scanline", "checkerboard", "gradient", "vignette"
            this_type = type(self)

            top_block = self.grid.get(self.x, self.y - 1) if self.grid.in_bounds(self.x, self.y - 1) else None
            bottom_block = self.grid.get(self.x, self.y + 1) if self.grid.in_bounds(self.x, self.y + 1) else None
            left_block = self.grid.get(self.x - 1, self.y) if self.grid.in_bounds(self.x - 1, self.y) else None
            right_block = self.grid.get(self.x + 1, self.y) if self.grid.in_bounds(self.x + 1, self.y) else None

            exposed_top = not isinstance(top_block, this_type)
            exposed_bottom = not isinstance(bottom_block, this_type)
            exposed_left = not isinstance(left_block, this_type)
            exposed_right = not isinstance(right_block, this_type)

            # Always-on base desaturation overlay
            base_overlay = pygame.Surface((bw, bw), pygame.SRCALPHA)
            base_overlay.fill((71, 71, 71, 62))
            self.screen.blit(base_overlay, (draw_x, draw_y))

            def edge_strength(px, py, max_alpha=80, falloff_portion=0.3):
                falloff = max(1, int(bw * falloff_portion))
                strength = 0.0
                if exposed_top:
                    strength += max(0.0, 1.0 - (py / falloff))
                if exposed_bottom:
                    strength += max(0.0, 1.0 - ((bw - 1 - py) / falloff))
                if exposed_left:
                    strength += max(0.0, 1.0 - (px / falloff))
                if exposed_right:
                    strength += max(0.0, 1.0 - ((bw - 1 - px) / falloff))
                strength = min(strength, 1.0)
                return int(strength * max_alpha)

            if technique == "flat":
                pass  # base overlay is enough

            elif technique == "scanline":
                for row in range(0, bw, 2):
                    alpha = edge_strength(bw // 2, row, max_alpha=65, falloff_portion=0.5)
                    if alpha > 0:
                        line = pygame.Surface((bw, 1), pygame.SRCALPHA)
                        line.fill((100, 95, 110, alpha))
                        self.screen.blit(line, (draw_x, draw_y + row))

            elif technique == "checkerboard":
                dot = pygame.Surface((1, 1), pygame.SRCALPHA)
                for row in range(bw):
                    for col in range(row % 2, bw, 2):
                        alpha = edge_strength(col, row, max_alpha=75, falloff_portion=0.45)
                        if alpha > 0:
                            dot.fill((100, 95, 110, alpha))
                            self.screen.blit(dot, (draw_x + col, draw_y + row))

            elif technique == "gradient":
                overlay = pygame.Surface((bw, bw), pygame.SRCALPHA)
                for row in range(bw):
                    for col in range(bw):
                        alpha = edge_strength(col, row, max_alpha=95, falloff_portion=0.45)
                        if alpha > 0:
                            overlay.set_at((col, row), (80, 75, 90, alpha))
                self.screen.blit(overlay, (draw_x, draw_y))

            elif technique == "vignette":
                overlay = pygame.Surface((bw, bw), pygame.SRCALPHA)
                for row in range(bw):
                    for col in range(bw):
                        alpha = edge_strength(col, row, max_alpha=70, falloff_portion=0.65)
                        if alpha > 0:
                            overlay.set_at((col, row), (80, 75, 90, alpha))
                self.screen.blit(overlay, (draw_x, draw_y))

            self.draw_self_edges(draw_x, draw_y)

    def draw_self_edges(self, draw_x, draw_y, edge_color=(30, 30, 30, 55), edge_width=2):
        this_type = type(self)
        bw = self.block_width

        top_block = self.grid.get(self.x, self.y - 1) if self.grid.in_bounds(self.x, self.y - 1) else None
        bottom_block = self.grid.get(self.x, self.y + 1) if self.grid.in_bounds(self.x, self.y + 1) else None
        left_block = self.grid.get(self.x - 1, self.y) if self.grid.in_bounds(self.x - 1, self.y) else None
        right_block = self.grid.get(self.x + 1, self.y) if self.grid.in_bounds(self.x + 1, self.y) else None

        if not isinstance(top_block, this_type):
            top_edge = pygame.Surface((bw, edge_width), pygame.SRCALPHA)
            top_edge.fill(edge_color)
            self.screen.blit(top_edge, (draw_x, draw_y))

        if not isinstance(bottom_block, this_type):
            bottom_edge = pygame.Surface((bw, edge_width), pygame.SRCALPHA)
            bottom_edge.fill(edge_color)
            self.screen.blit(bottom_edge, (draw_x, draw_y + bw - edge_width))

        if not isinstance(left_block, this_type):
            left_edge = pygame.Surface((edge_width, bw), pygame.SRCALPHA)
            left_edge.fill(edge_color)
            self.screen.blit(left_edge, (draw_x, draw_y))

        if not isinstance(right_block, this_type):
            right_edge = pygame.Surface((edge_width, bw), pygame.SRCALPHA)
            right_edge.fill(edge_color)
            self.screen.blit(right_edge, (draw_x + bw - edge_width, draw_y))

    def physics(self):
        self.pass_through = True