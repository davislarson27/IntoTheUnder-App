import pygame

from ..entity import Entity

class Blob(Entity):
    """basically a green thing that moves for testing"""

    def initialize_drawing_vars(self):
        self.main_surface = pygame.Surface((self.BLOCK_WIDTH, self.BLOCK_WIDTH), pygame.SRCALPHA)
        color = (200, 200, 200)
        self.main_surface.fill(color)

    def draw(self, screen_x=0, screen_y=0):
        hit_box = self.main_surface.get_rect(
            topleft=(self.x - screen_x, self.y - screen_y)
        )
        self.screen.blit(self.main_surface, hit_box)

    def pathfind(self, input, physics, dx, dy, cur_y_acceleration, cur_player_speed_x, cur_player_speed_y, jump_is_possible, water_movement):

        return dx, dy, cur_y_acceleration, cur_player_speed_y, water_movement
