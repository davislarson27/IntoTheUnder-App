import pygame
from world.blocks.block_types._base import MutliBlock, SubMultiBlock

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

class Spruce_Door(MutliBlock):
    @staticmethod
    def BuildMulti(grid, x, y):
        y_top = y-1
        if not grid.in_bounds(x, y_top) or grid.get(x, y) is not None or grid.get(x, y_top) is not None:
            y+=1
            y_top+=1
            if not grid.in_bounds(x, y_top) or not grid.in_bounds(x, y) or grid.get(x, y) is not None or grid.get(x, y_top) is not None:
                return False
        grid.set(x, y, Spruce_Door_Bottom)
        grid.set(x, y_top, Spruce_Door_Top)
        return True

    # remember to update the blocks_list for loading when you add a new type of block :)

    str_name = "Spruce Door"
    ticks_to_mine = 45

    @staticmethod
    def draw_manual(screen, x, y, block_width, being_mined=False, is_grid_coordinates=True, use_alt_drawing=False):
        if is_grid_coordinates:
            x *= block_width
            y *= block_width

        # Create a temporary surface that can hold 2 stacked tiles
        temp_surface = pygame.Surface((block_width, block_width * 2), pygame.SRCALPHA)

        # Draw full-size door halves onto temp surface
        Spruce_Door_Top.draw_manual(
            temp_surface,
            0,
            0,
            block_width,
            being_mined=being_mined,
            is_grid_coordinates=False
        )

        Spruce_Door_Bottom.draw_manual(
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

class Mahogany_Door(MutliBlock):
    @staticmethod
    def BuildMulti(grid, x, y):
        y_top = y-1
        if not grid.in_bounds(x, y_top) or grid.get(x, y) is not None or grid.get(x, y_top) is not None:
            y+=1
            y_top+=1
            if not grid.in_bounds(x, y_top) or not grid.in_bounds(x, y) or grid.get(x, y) is not None or grid.get(x, y_top) is not None:
                return False
        grid.set(x, y, Mahogany_Door_Bottom)
        grid.set(x, y_top, Mahogany_Door_Top)
        return True

    # remember to update the blocks_list for loading when you add a new type of block :)

    str_name = "Mahogany Door"
    ticks_to_mine = 45

    @staticmethod
    def draw_manual(screen, x, y, block_width, being_mined=False, is_grid_coordinates=True, use_alt_drawing=False):
        if is_grid_coordinates:
            x *= block_width
            y *= block_width

        # Create a temporary surface that can hold 2 stacked tiles
        temp_surface = pygame.Surface((block_width, block_width * 2), pygame.SRCALPHA)

        # Draw full-size door halves onto temp surface
        Mahogany_Door_Top.draw_manual(
            temp_surface,
            0,
            0,
            block_width,
            being_mined=being_mined,
            is_grid_coordinates=False
        )

        Mahogany_Door_Bottom.draw_manual(
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


# ----------------------------------------- submultiblocks ----------------------------------------- #

class Door_Top(SubMultiBlock):
    # special_value -> True = door open, False = door closed

    # remember to update the blocks_list for loading when you add a new type of block :)

    str_name = "Door Top"
    ticks_to_mine = 45

    draw_background = True
    ignore_shading_from = {
        (0, 1): False, # coming from the top
        (0, -1): True, # coming from the bottom
        (1, 0): False, # coming from the right
        (-1, 0): False # comin from the left
    }

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

    def use_alt_drawing(self):
        return self.pass_through

    def onDestroy(self, inventory=None):
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
    
    def block_edge_shade(self, directionOfBgBlock_x, directionofBgBlock_y):
        """returns true or false if the bg block should be shaded on the corner"""
        if self.pass_through:
            temp_ignore_shading_from = {
                (0, 1): True, # coming from the top
                (0, -1): True, # coming from the bottom
                (1, 0): False, # coming from the right
                (-1, 0): True # comin from the left
            }
            return temp_ignore_shading_from[(directionOfBgBlock_x, directionofBgBlock_y)]
        else:
            return self.ignore_shading_from[(directionOfBgBlock_x, directionofBgBlock_y)]

class Door_Bottom(SubMultiBlock):
    # special_value -> True = door open, False = door closed
    
    # remember to update the blocks_list for loading when you add a new type of block :)

    str_name = "Door Bottom"
    ticks_to_mine = 45

    draw_background = True
    ignore_shading_from = {
        (0, 1): True, # coming from the top
        (0, -1): False, # coming from the bottom
        (1, 0): False, # coming from the right
        (-1, 0): False # comin from the left
    }

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

    def use_alt_drawing(self):
        return self.pass_through

    def onDestroy(self, inventory=None):
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

    def block_edge_shade(self, directionOfBgBlock_x, directionofBgBlock_y):
        """returns true or false if the bg block should be shaded on the corner"""
        if self.pass_through:
            temp_ignore_shading_from = {
                (0, 1): True, # coming from the top
                (0, -1): True, # coming from the bottom
                (1, 0): False, # coming from the right
                (-1, 0): True # comin from the left
            }
            return temp_ignore_shading_from[(directionOfBgBlock_x, directionofBgBlock_y)]
        else:
            return self.ignore_shading_from[(directionOfBgBlock_x, directionofBgBlock_y)]

class Spruce_Door_Top(SubMultiBlock):
    # special_value -> True = door open, False = door closed

    # remember to update the blocks_list for loading when you add a new type of block :)

    str_name = "Spruce Door Top"
    ticks_to_mine = 45

    draw_background = True
    ignore_shading_from = {
        (0, 1): False, # coming from the top
        (0, -1): True, # coming from the bottom
        (1, 0): False, # coming from the right
        (-1, 0): False # comin from the left
    }

    @staticmethod
    def draw_manual(screen, x, y, block_width, being_mined=False, is_grid_coordinates=True, use_alt_drawing=False):
        added = 20 if being_mined else 0
        if is_grid_coordinates:
            x *= block_width
            y *= block_width

        wood  = (105 + added,  95 + added,  88 + added)
        frame = ( 80 + added,  71 + added,  65 + added)
        panel = ( 93 + added,  84 + added,  77 + added)
        metal = ( 52 + added,  47 + added,  44 + added)

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

    def use_alt_drawing(self):
        return self.pass_through

    def onDestroy(self, inventory=None):
        # get both self and the top and set to none, return a door object
        self.grid.set(self.x, self.y, None)
        y_other_half = self.y+1
        if isinstance(self.grid.get(self.x, y_other_half), Spruce_Door_Bottom):
            self.grid.set(self.x, self.y, None)
            self.grid.set(self.x, y_other_half, None)
        return Spruce_Door

    def interaction(self, inventory):
        top_y = self.y + 1
        bottom_half = self.grid.get(self.x, top_y)
        if not isinstance(bottom_half, Spruce_Door_Bottom):
            return False
        self.pass_through = not self.pass_through
        bottom_half.pass_through = self.pass_through
        return True
    
    def block_edge_shade(self, directionOfBgBlock_x, directionofBgBlock_y):
        """returns true or false if the bg block should be shaded on the corner"""
        if self.pass_through:
            temp_ignore_shading_from = {
                (0, 1): True, # coming from the top
                (0, -1): True, # coming from the bottom
                (1, 0): False, # coming from the right
                (-1, 0): True # comin from the left
            }
            return temp_ignore_shading_from[(directionOfBgBlock_x, directionofBgBlock_y)]
        else:
            return self.ignore_shading_from[(directionOfBgBlock_x, directionofBgBlock_y)]

class Spruce_Door_Bottom(SubMultiBlock):
    # special_value -> True = door open, False = door closed
    
    # remember to update the blocks_list for loading when you add a new type of block :)

    str_name = "Spruce Door Bottom"
    ticks_to_mine = 45

    draw_background = True
    ignore_shading_from = {
        (0, 1): True, # coming from the top
        (0, -1): False, # coming from the bottom
        (1, 0): False, # coming from the right
        (-1, 0): False # comin from the left
    }

    @staticmethod
    def draw_manual(screen, x, y, block_width, being_mined=False, is_grid_coordinates=True, use_alt_drawing=False):
        added = 20 if being_mined else 0
        if is_grid_coordinates:
            x *= block_width
            y *= block_width

        wood  = (105 + added,  95 + added,  88 + added)
        frame = ( 80 + added,  71 + added,  65 + added)
        panel = ( 93 + added,  84 + added,  77 + added)
        metal = ( 52 + added,  47 + added,  44 + added)

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

    def use_alt_drawing(self):
        return self.pass_through

    def onDestroy(self, inventory=None):
        # get both self and the top and set to none, return a door object
        self.grid.set(self.x, self.y, None)
        y_other_half = self.y-1
        if isinstance(self.grid.get(self.x, y_other_half), Spruce_Door_Top):
            self.grid.set(self.x, self.y, None)
            self.grid.set(self.x, y_other_half, None)
        return Spruce_Door

    def interaction(self, inventory):
        top_y = self.y - 1
        top_half = self.grid.get(self.x, top_y)
        if not isinstance(top_half, Spruce_Door_Top):
            return False
        self.pass_through = not self.pass_through
        top_half.pass_through = self.pass_through
        return True

    def block_edge_shade(self, directionOfBgBlock_x, directionofBgBlock_y):
        """returns true or false if the bg block should be shaded on the corner"""
        if self.pass_through:
            temp_ignore_shading_from = {
                (0, 1): True, # coming from the top
                (0, -1): True, # coming from the bottom
                (1, 0): False, # coming from the right
                (-1, 0): True # comin from the left
            }
            return temp_ignore_shading_from[(directionOfBgBlock_x, directionofBgBlock_y)]
        else:
            return self.ignore_shading_from[(directionOfBgBlock_x, directionofBgBlock_y)]

class Mahogany_Door_Top(SubMultiBlock):
    # special_value -> True = door open, False = door closed

    # remember to update the blocks_list for loading when you add a new type of block :)

    str_name = "Mahogany Door Top"
    ticks_to_mine = 45

    draw_background = True
    ignore_shading_from = {
        (0, 1): False, # coming from the top
        (0, -1): True, # coming from the bottom
        (1, 0): False, # coming from the right
        (-1, 0): False # comin from the left
    }

    @staticmethod
    def draw_manual(screen, x, y, block_width, being_mined=False, is_grid_coordinates=True, use_alt_drawing=False):
        added = 20 if being_mined else 0
        if is_grid_coordinates:
            x *= block_width
            y *= block_width

        wood  = (158 + added,  86 + added,  60 + added)
        frame = (128 + added,  62 + added,  40 + added)
        panel = (143 + added,  73 + added,  50 + added)
        metal = ( 52 + added,  47 + added,  44 + added)
        
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

    def use_alt_drawing(self):
        return self.pass_through

    def onDestroy(self, inventory=None):
        # get both self and the top and set to none, return a door object
        self.grid.set(self.x, self.y, None)
        y_other_half = self.y+1
        if isinstance(self.grid.get(self.x, y_other_half), Mahogany_Door_Bottom):
            self.grid.set(self.x, self.y, None)
            self.grid.set(self.x, y_other_half, None)
        return Mahogany_Door

    def interaction(self, inventory):
        top_y = self.y + 1
        bottom_half = self.grid.get(self.x, top_y)
        if not isinstance(bottom_half, Mahogany_Door_Bottom):
            return False
        self.pass_through = not self.pass_through
        bottom_half.pass_through = self.pass_through
        return True
    
    def block_edge_shade(self, directionOfBgBlock_x, directionofBgBlock_y):
        """returns true or false if the bg block should be shaded on the corner"""
        if self.pass_through:
            temp_ignore_shading_from = {
                (0, 1): True, # coming from the top
                (0, -1): True, # coming from the bottom
                (1, 0): False, # coming from the right
                (-1, 0): True # comin from the left
            }
            return temp_ignore_shading_from[(directionOfBgBlock_x, directionofBgBlock_y)]
        else:
            return self.ignore_shading_from[(directionOfBgBlock_x, directionofBgBlock_y)]

class Mahogany_Door_Bottom(SubMultiBlock):
    # special_value -> True = door open, False = door closed
    
    # remember to update the blocks_list for loading when you add a new type of block :)

    str_name = "Mahogany Door Bottom"
    ticks_to_mine = 45

    draw_background = True
    ignore_shading_from = {
        (0, 1): True, # coming from the top
        (0, -1): False, # coming from the bottom
        (1, 0): False, # coming from the right
        (-1, 0): False # comin from the left
    }

    @staticmethod
    def draw_manual(screen, x, y, block_width, being_mined=False, is_grid_coordinates=True, use_alt_drawing=False):
        added = 20 if being_mined else 0
        if is_grid_coordinates:
            x *= block_width
            y *= block_width

        wood  = (158 + added,  86 + added,  60 + added)
        frame = (128 + added,  62 + added,  40 + added)
        panel = (143 + added,  73 + added,  50 + added)
        metal = ( 52 + added,  47 + added,  44 + added)

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

    def use_alt_drawing(self):
        return self.pass_through

    def onDestroy(self, inventory=None):
        # get both self and the top and set to none, return a door object
        self.grid.set(self.x, self.y, None)
        y_other_half = self.y-1
        if isinstance(self.grid.get(self.x, y_other_half), Mahogany_Door_Top):
            self.grid.set(self.x, self.y, None)
            self.grid.set(self.x, y_other_half, None)
        return Mahogany_Door

    def interaction(self, inventory):
        top_y = self.y - 1
        top_half = self.grid.get(self.x, top_y)
        if not isinstance(top_half, Mahogany_Door_Top):
            return False
        self.pass_through = not self.pass_through
        top_half.pass_through = self.pass_through
        return True

    def block_edge_shade(self, directionOfBgBlock_x, directionofBgBlock_y):
        """returns true or false if the bg block should be shaded on the corner"""
        if self.pass_through:
            temp_ignore_shading_from = {
                (0, 1): True, # coming from the top
                (0, -1): True, # coming from the bottom
                (1, 0): False, # coming from the right
                (-1, 0): True # comin from the left
            }
            return temp_ignore_shading_from[(directionOfBgBlock_x, directionofBgBlock_y)]
        else:
            return self.ignore_shading_from[(directionOfBgBlock_x, directionofBgBlock_y)]
