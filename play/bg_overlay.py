import pygame

class BG_Overlay:

    def __init__(self, screen, BLOCK_WIDTH, grid, background_grid):
        self.screen = screen
        self.BLOCK_WIDTH = BLOCK_WIDTH
        self.grid = grid
        self.background_grid = background_grid
        self.bg_overlay_cache = {}
        self.build_bg_overlay_cache()

    def build_bg_overlay_cache(self):
        self.bg_overlay_cache = {}
        for exposed_top in (False, True):
            for exposed_bottom in (False, True):
                for exposed_left in (False, True):
                    for exposed_right in (False, True):
                        self.get_bg_overlay_surface(
                            exposed_top, exposed_bottom, exposed_left, exposed_right
                        )

    def get_bg_overlay_surface(self, exposed_top, exposed_bottom, exposed_left, exposed_right):
        key = (exposed_top, exposed_bottom, exposed_left, exposed_right)
        if key in self.bg_overlay_cache:
            return self.bg_overlay_cache[key]

        bw = self.BLOCK_WIDTH
        base_color = (43, 48, 51, 73)
        edge_color = (55, 65, 75)

        surf = pygame.Surface((bw, bw), pygame.SRCALPHA)
        falloff = max(1, int(bw * 0.45))

        for py in range(bw):
            for px in range(bw):
                e_strength = 0.0
                if exposed_top:    e_strength += max(0.0, 1.0 - (py / falloff))
                if exposed_bottom: e_strength += max(0.0, 1.0 - ((bw - 1 - py) / falloff))
                if exposed_left:   e_strength += max(0.0, 1.0 - (px / falloff))
                if exposed_right:  e_strength += max(0.0, 1.0 - ((bw - 1 - px) / falloff))

                e_strength = min(e_strength, 1.0)
                final_alpha = min(255, 62 + int(e_strength * 95))
                surf.set_at((px, py), (*edge_color, final_alpha))

        surf = surf.convert_alpha()
        self.bg_overlay_cache[key] = surf
        return surf

    def draw_at(self, grid_x, grid_y, camera_x, camera_y):
        bg_block = self.background_grid.get(grid_x, grid_y)
        if bg_block is None:
            return

        fg_block = self.grid.get(grid_x, grid_y)
        if fg_block is not None and fg_block.draw_background == False:
            return

        exposed_top    = self.grid.get(grid_x, grid_y-1) is not None and self.grid.get(grid_x, grid_y-1).block_edge_shade(0, -1) == False
        exposed_bottom = self.grid.get(grid_x, grid_y+1) is not None and self.grid.get(grid_x, grid_y+1).block_edge_shade(0, 1) == False
        exposed_left   = self.grid.get(grid_x-1, grid_y) is not None and self.grid.get(grid_x-1, grid_y).block_edge_shade(-1, 0) == False
        exposed_right  = self.grid.get(grid_x+1, grid_y) is not None and self.grid.get(grid_x+1, grid_y).block_edge_shade(1, 0) == False

        draw_x = grid_x * self.BLOCK_WIDTH - camera_x
        draw_y = grid_y * self.BLOCK_WIDTH - camera_y

        overlay = self.get_bg_overlay_surface(
            exposed_top, exposed_bottom, exposed_left, exposed_right
        )
        self.screen.blit(overlay, (draw_x, draw_y))

    def draw(self, camera_x, camera_y, inventory_height):
        x_min = max(0, camera_x // self.BLOCK_WIDTH)
        x_max = min(self.background_grid.width, (camera_x + self.screen.get_width()) // self.BLOCK_WIDTH) + 1

        true_height = self.screen.get_height() - inventory_height
        y_min = max(0, camera_y // self.BLOCK_WIDTH)
        y_max = min(self.background_grid.height, (camera_y + true_height) // self.BLOCK_WIDTH) + 1

        for y in range(y_min, y_max):
            for x in range(x_min, x_max):
                self.draw_at(x, y, camera_x, camera_y)