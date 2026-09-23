import pygame
import random

from ..entity import Entity
from play.player import Player
from world.blocks.block_export import Snow_Man_Head


class Snow_Man_Entity(Entity):
    def initialize_drawing_vars(self):
        self.main_surface = pygame.Surface((self.BLOCK_WIDTH, int(self.BLOCK_WIDTH * 1.9)), pygame.SRCALPHA)
        self.main_surface.fill((225, 235, 245))

        key = (Snow_Man_Head, self.BLOCK_WIDTH, False, False)
        if key not in Snow_Man_Head.surfaces:
            Snow_Man_Head.draw_to_surface(self.BLOCK_WIDTH, being_mined=False, use_alt_drawing=False)

        self.main_surface.blit(Snow_Man_Head.surfaces[key], (0, 0))

    def initialize_unique_entity_attrs(self):
        self.x_size: int = self.BLOCK_WIDTH
        self.y_size: int = int(self.BLOCK_WIDTH * 1.9)

        self.ticks_till_action: int|None = None
        self.saw_user_last_tick: bool = False

        self.survival_mode: bool = True

        self.damage_per_hit: int = 5
        self.damage_cooldown_ticks_total: int = 30

        self.damage_cooldown_ticks: int = 0

        max_natural_speed = 1.25
        self.x_acceleration = 0.25
        self.friction_coeficient = abs(self.x_acceleration / max_natural_speed)

    def set_immunity_threshold(self, threshold):
        self.immunity_ticks = threshold

    def set_logic_tick_counters(self, ticks_till_action: int|None, saw_user_last_tick: bool, damage_cooldown_ticks: int) -> None:
        self.ticks_till_action = ticks_till_action
        self.saw_user_last_tick = saw_user_last_tick

        self.damage_cooldown_ticks = damage_cooldown_ticks

    def execute_collide_with_player(self, player: Player, player_inventory):
        """is executed when a player is touching an entity"""
        if self.damage_cooldown_ticks == 0:
            player.take_damage(self.damage_per_hit)
            self.damage_cooldown_ticks = self.damage_cooldown_ticks_total

    def draw(self, screen_x=0, screen_y=0):
        draw_hit_box = self.main_surface.get_rect(
            topleft=(self.x - screen_x, self.y - screen_y)
        )
        self.screen.blit(self.main_surface, draw_hit_box)
        self.ticks += 1

    def is_player_in_reaction_distance(self, x_center, player_center_x, y_center, player_center_y, can_travel_px):
        return abs(x_center - player_center_x) < can_travel_px and abs(y_center - player_center_y) < can_travel_px

    def set_ticks_till_action(self):
        min_reaction_time = 2
        max_reaction_time = 45
        self.ticks_till_action = random.randint(min_reaction_time, max_reaction_time)

    def initialize_temp_movement_vars(self, physics):
        dx = 0
        dy = 0
        applied_acceleration_x = 0
        cur_y_acceleration = physics.Y_ACCELERATION // 4
        cur_player_speed_x = self.player_speed
        cur_y_acceleration, cur_player_speed_x, cur_player_speed_y, jump_is_possible = self.get_player_physics(physics.Y_ACCELERATION)
        if cur_player_speed_y > 0: water_movement = True
        else: water_movement = False

        if self.damage_cooldown_ticks > 0: self.damage_cooldown_ticks -= 1

        return dx, dy, applied_acceleration_x, cur_y_acceleration, cur_player_speed_x, cur_player_speed_y, jump_is_possible, water_movement

    def pathfind(self, input, physics, dx, dy, applied_acceleration_x, cur_y_acceleration, cur_player_speed_x, cur_player_speed_y, jump_is_possible, water_movement, player=None):
        if player is None: return dx, dy, applied_acceleration_x, cur_y_acceleration, cur_player_speed_y, water_movement

        can_travel_px = self.BLOCK_WIDTH * 6
        travel_speed = 1
        player_center_x, player_center_y = player.get_center_px()
        x_center, y_center = self.get_center_px()

        if self.is_player_in_reaction_distance(x_center, player_center_x, y_center, player_center_y, can_travel_px):
            if self.saw_user_last_tick:
                if self.ticks_till_action is None:
                    self.set_ticks_till_action()
                else:
                    if self.ticks_till_action == 0:
                        if self.x > player_center_x:
                            applied_acceleration_x = -self.x_acceleration
                        else:
                            applied_acceleration_x = self.x_acceleration
                    else:
                        self.ticks_till_action -= 1
            else:
                self.saw_user_last_tick = True
        else:
            self.saw_user_last_tick = False
            # now decide if it wants to move somewhere else
            self.ticks_till_action = None
                
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
            "immunity_ticks": self.immunity_ticks,
            "health": self.health_bar.get_health(),
            "ticks_till_action": self.ticks_till_action,
            "saw_user_last_tick": self.saw_user_last_tick,
            "damage_cooldown_ticks": self.damage_cooldown_ticks,
        }

    @classmethod
    def fill_entity_object(cls, entity_dict, grid, screen, block_width):
        x_pixel = entity_dict["x_pixel"]
        y_pixel = entity_dict["y_pixel"]
        x_vel = entity_dict["x_vel"]
        y_vel = entity_dict["y_vel"]
        ticks = entity_dict["ticks"]
        immunity_ticks = entity_dict['immunity_ticks']
        health = entity_dict["health"]
        ticks_till_action = entity_dict["ticks_till_action"]
        saw_user_last_tick = entity_dict["saw_user_last_tick"]
        damage_cooldown_ticks = entity_dict["damage_cooldown_ticks"]
        
        entity_obj = Snow_Man_Entity(grid, screen, player_x_pixel=x_pixel, player_y_pixel=y_pixel, x_vel=x_vel, y_vel=y_vel, BLOCK_WIDTH=block_width, health=health, ticks=ticks, immunity_ticks=immunity_ticks)
        entity_obj.set_logic_tick_counters(ticks_till_action, saw_user_last_tick, damage_cooldown_ticks)
        return entity_obj
