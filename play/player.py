from play.entities.entity import Entity


class Player(Entity):

    def draw(self, screen_x=0, screen_y=0):

        if self.is_left_facing:
            player_rect = self.images.player_left.get_rect(
                topleft=(self.x - screen_x, self.y - screen_y)
            )
            self.screen.blit(self.images.player_left, player_rect)
        else:
            player_rect = self.images.player_right.get_rect(
                topleft=(self.x - screen_x, self.y - screen_y)
            )
            self.screen.blit(self.images.player_right, player_rect)

    def pathfind(self, input, physics, dx, dy, applied_acceleration_x, cur_y_acceleration, cur_player_speed_x, cur_player_speed_y, jump_is_possible, water_movement, player=None):
        applied_acceleration_x = 0
        if input.a_hold > 0:
            self.wants_to_move_left = True
            applied_acceleration_x = (-self.x_acceleration * self.health_bar.get_low_energy_speed_reduction_factor())
            self.apply_movement_cost_x()
        if input.d_hold > 0:
            self.wants_to_move_left = False
            applied_acceleration_x = (self.x_acceleration * self.health_bar.get_low_energy_speed_reduction_factor())
            self.apply_movement_cost_x()
        if input.w_hold > 0 or input.space_hold > 0:
            if not self.is_not_block_below() and jump_is_possible:
                self.y_vel = physics.JUMP_VELOCITY
                self.ticks_falling = 1
                self.apply_movement_cost_jump()
            if water_movement:
                self.y_vel = -cur_player_speed_y
                self.apply_movement_cost_y()
        if input.s_hold > 0:
            if water_movement:
                self.y_vel = cur_player_speed_y
                self.apply_movement_cost_y()

        return dx, dy, applied_acceleration_x, cur_y_acceleration, cur_player_speed_y, water_movement

    def to_dict(self):
        return {
            "player_x_pixel": self.x,
            "player_y_pixel": self.y,
            "player_speed": self.player_speed,
            "x_vel": self.x_vel,
            "y_vel": self.y_vel,
            "x_size": self.x_size,
            "y_size": self.y_size,
            "ticks_falling": self.ticks_falling,
            "ticks_inc": self.ticks_inc,
            "BLOCK_WIDTH": self.BLOCK_WIDTH,
            "health": self.health_bar.get_health(),
            "energy": self.health_bar.get_energy(),
            "is_left_facing": self.is_left_facing,
            "player_spawn_x": self.player_spawn_x,
            "player_spawn_y": self.player_spawn_y,
            "can_take_fall_damage": self.can_take_fall_damage
        }

    def get_position_for_dropping_inventory_items(self):
        x, y = self.get_center_top_px()
        if self.is_left_facing:
            x -= self.BLOCK_WIDTH * 2
        else:
            x += self.BLOCK_WIDTH * 1.8
        return x, y
