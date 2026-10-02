import pygame
import random

from ..entity import Entity

class Snow_Ball_Projectile(Entity):
    def initialize_drawing_vars(self):
        self.main_surface = pygame.Surface((self.BLOCK_WIDTH // 2, self.BLOCK_WIDTH // 2), pygame.SRCALPHA)
        self.main_surface.fill((225, 235, 245))

    def initialize_unique_entity_attrs(self):
        self.x_size = self.BLOCK_WIDTH // 2
        self.y_size = self.BLOCK_WIDTH // 2
        self.contact_made = False

        self.immunity_ticks = 1

        self.x_acceleration = 1
        self.friction_coeficient = abs(6 / (self.BLOCK_WIDTH * 2.05))

        self.interact_in_pointer_interaction = False

        self.damage_on_impact = 10
        self.check_collisions_against_all: bool = True
        self.interact_width_projectiles: bool = False

        self.apply_x_friction_in_air: bool = False
        

    def set_initial_velocity(self, init_vel_x, init_vel_y):
        self.x_vel = init_vel_x
        self.y_vel = init_vel_y

    def execute_collide_with_player(self, player, player_inventory):
        """is executed when a player is touching an entity"""
        if self.ticks > self.immunity_ticks and player.interact_width_projectiles:
            self.contact_made = True
            player.take_damage(self.damage_on_impact)

    def is_dead(self):
        return self.contact_made

    def draw(self, screen_x=0, screen_y=0):
        draw_hit_box = self.main_surface.get_rect(
            topleft=(self.x - screen_x, self.y - screen_y)
        )
        # cur_surface = pygame.transform.rotate(self.main_surface, -self.ticks)
        # self.screen.blit(cur_surface, draw_hit_box)
        # self.ticks += 1
        self.screen.blit(self.main_surface, draw_hit_box)
        
    def process_grid_collisions(self, collide_x: bool, collide_y: bool):
        if collide_x or collide_y: self.contact_made = True

    def initialize_temp_movement_vars(self, physics):
        dx = 0
        dy = 0
        applied_acceleration_x = 0
        cur_y_acceleration = physics.Y_ACCELERATION // 4
        cur_player_speed_x = self.player_speed
        cur_y_acceleration, cur_player_speed_x, cur_player_speed_y, jump_is_possible = self.get_player_physics(physics.Y_ACCELERATION)
        if cur_player_speed_y > 0: water_movement = True
        else: water_movement = False

        return dx, dy, applied_acceleration_x, cur_y_acceleration, cur_player_speed_x, cur_player_speed_y, jump_is_possible, water_movement

    def pathfind(self, input, physics, dx, dy, applied_acceleration_x, cur_y_acceleration, cur_player_speed_x, cur_player_speed_y, jump_is_possible, water_movement, player=None):
        if player is None: return dx, dy, applied_acceleration_x, cur_y_acceleration, cur_player_speed_y, water_movement                
        return dx, dy, applied_acceleration_x, cur_y_acceleration, cur_player_speed_y, water_movement

    # ---------------------------------------------- loading and saving methods ---------------------------------------------- #
    def to_dict(self):
        return {
            "entity_type": type(self).__name__,
            "x_pixel": self.x,
            "y_pixel": self.y,
            "x_vel": self.x_vel,
            "y_vel": self.y_vel,
            "ticks_falling": self.ticks_falling,
            "ticks_inc": self.ticks_inc,
            "is_left_facing": self.is_left_facing,
            "ticks": self.ticks,
        }
    
    @classmethod
    def fill_entity_object(cls, entity_dict, grid, screen, block_width):
        x_pixel = entity_dict["x_pixel"]
        y_pixel = entity_dict["y_pixel"]
        x_vel = entity_dict["x_vel"]
        y_vel = entity_dict["y_vel"]
        ticks = entity_dict["ticks"]
        
        entity_obj = Snow_Ball_Projectile(grid, screen, player_x_pixel=x_pixel, player_y_pixel=y_pixel, x_vel=x_vel, y_vel=y_vel, BLOCK_WIDTH=block_width, ticks=ticks)
        return entity_obj
