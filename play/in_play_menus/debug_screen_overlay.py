import pygame
import components.fonts as font_manager

class Debug_Overlay:
    def __init__(self, screen, grid, player):
        self.screen = screen
        self.grid = grid
        self.player = player
        self.is_active = False
        self.player_coordinates = player.get_player_block_coordinates()
        self.cur_chunk = grid.get_chunk_x(self.player_coordinates[0])
        self.fps = 0

        self.font_height = 16
        _f = font_manager.get()
        self.font = pygame.font.Font(str(_f.PixeloidMono), self.font_height)
        self.margin_left = 30

        allow_start_y = player.get_health_bar_height()
        if allow_start_y > 0:
            self.margin_top = allow_start_y + 6
        else:
            self.margin_top = player.health_bar.margin

        self.padding_between_lines = self.font_height // 3

    def get_line_start_y(self, line_num): # line num starts at 1
        return self.margin_top + ((self.font_height + self.padding_between_lines) * (line_num - 1))


    def run(self, input, clock):
        if input.f3_keypress:
            self.is_active = not self.is_active
        
        if self.is_active:
            self.player_coordinates = self.player.get_player_block_coordinates()
            self.cur_chunk = self.grid.get_chunk_id(self.player_coordinates[0])
            self.fps = round(clock.get_fps(), 1)

    def draw(self):
        if not self.is_active:
            return
        
        x, y = self.player_coordinates
        text = f'X: {x}  Y: {y}'
        surface = self.font.render(text, True, (255, 255, 255))
        self.screen.blit(surface, (self.margin_left, self.get_line_start_y(1)))

        text = f'Chunk ID: {self.cur_chunk}'
        surface = self.font.render(text, True, (255, 255, 255))
        self.screen.blit(surface, (self.margin_left, self.get_line_start_y(2)))

        text = f'FPS: {self.fps}'
        surface = self.font.render(text, True, (255, 255, 255))
        self.screen.blit(surface, (self.margin_left, self.get_line_start_y(3)))

