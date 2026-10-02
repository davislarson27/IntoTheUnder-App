import pygame
from math import sqrt, copysign

from play.entities.entities_export import Snow_Ball_Projectile
from world.blocks.block_types._base import Entity_Spawner

class Snow_Ball(Entity_Spawner):
    place_as_block = False
    stored_entity = Snow_Ball_Projectile

    @classmethod
    def place_entity(cls, entity, world_mouse_x, world_mouse_y, selected_grid, foreground_grid, background_grid, screen, block_width):
        x_px, y_px = entity.get_center_top_px()
        entity_init_vel_x, entity_init_vel_y = entity.get_movement_velocities()
        tot_init_velocity = 22
        snow_ball_width = block_width // 4

        dy = world_mouse_y - y_px
        dx = world_mouse_x - x_px
        x_px += (int(block_width * 1.1) * copysign(1, dx) - snow_ball_width)

        distance = sqrt((dx * dx) + (dy * dy))
        if distance == 0:
            x_init_vel, y_init_vel = 0, 0
        else:
            vel_scale = tot_init_velocity / distance
            x_init_vel = dx * vel_scale
            y_init_vel = dy * vel_scale

        x_init_vel += entity_init_vel_x
        y_init_vel += entity_init_vel_y

        snow_ball_entity = cls.stored_entity(foreground_grid, screen, x_px, y_px, block_width)
        snow_ball_entity.set_initial_velocity(x_init_vel, y_init_vel)
        foreground_grid.insert_entity(snow_ball_entity)

    @staticmethod
    def draw_manual(screen, x, y, block_width, being_mined=False, is_grid_coordinates=True, use_alt_drawing=False):
        if is_grid_coordinates:
            x *= block_width
            y *= block_width

        snow_ball_color = (225, 235, 245)

        snow_ball_diameter = block_width // 2

        # background fill
        pygame.draw.rect(screen, snow_ball_color, (x + snow_ball_diameter // 2, y + snow_ball_diameter // 2, snow_ball_diameter, snow_ball_diameter))
