import pygame

class Debug_Overlay:
    def __init__(self, screen, player):
        self.screen = screen
        self.player = player
        self.is_active = False
        self.player_coordinates = player.get_player_block_coordinates()
        self.fps = 0

        allow_start_y = player.get_health_bar_height()

        self.font_height = 22
        self.font = pygame.font.Font(None, self.font_height)
        self.margin_left = 30
        self.margin_top = 12 + allow_start_y


    def run(self, input, clock):
        if input.f3_keypress:
            self.is_active = not self.is_active
        
        if self.is_active:
            self.player_coordinates = self.player.get_player_block_coordinates()
            self.fps = round(clock.get_fps(), 1)

    def draw(self):
        if not self.is_active:
            return
        
        x, y = self.player_coordinates
        text = f'X: {x}  Y: {y}'
        surface = self.font.render(text, True, (255, 255, 255))
        self.screen.blit(surface, (self.margin_left, self.margin_top))

        text = f'FPS: {self.fps}'
        surface = self.font.render(text, True, (255, 255, 255))
        self.screen.blit(surface, (self.margin_left, self.margin_top + self.font_height))

