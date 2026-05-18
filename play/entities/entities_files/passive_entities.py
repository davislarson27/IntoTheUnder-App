import pygame

from ..entity import Entity

class Blob(Entity):
    """basically a green thing that moves for testing"""

    def initialize_drawing_vars(self):
        self.main_surface = pygame.Surface((self.BLOCK_WIDTH, self.BLOCK_WIDTH), pygame.SRCALPHA)
        color = (200, 200, 200)
        self.main_surface.fill(color)

    def initialize_unique_entity_attrs(self):
        self.face_right = True
        self.path = None

    def draw(self, screen_x=0, screen_y=0):
        hit_box = self.main_surface.get_rect(
            topleft=(self.x - screen_x, self.y - screen_y)
        )
        self.screen.blit(self.main_surface, hit_box)

    # def is_valid_path(self):
    #     if self.path is None:
    #         return False
    #     return True
    
    # def set_path(self):
    #     # goal: move until you hit a block
    #     return

    def pathfind(self, input, physics, dx, dy, cur_y_acceleration, cur_player_speed_x, cur_player_speed_y, jump_is_possible, water_movement):

        # idea: have two parts: is_valid_path, then set_path
        # is_valid_path returns False if the path isn't set or doesn't work anymore
        # set_path runs if is_valid_path returns true and finds a new path to a location it chooses
        block_in_view = False

        view_range = 10
        cur_block_x, cur_block_y = self.get_player_block_coordinates()
        for check_x in range(cur_block_x, cur_block_x + view_range):
            if self.grid.get(check_x, cur_block_y) is not None: # i.e., there is a block to move to
                block_in_view = True
                break
        
        if block_in_view:
            dx += cur_player_speed_x

        return dx, dy, cur_y_acceleration, cur_player_speed_y, water_movement
