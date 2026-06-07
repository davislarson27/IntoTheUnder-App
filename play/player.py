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

        # also draw the health bar for the player
        self.health_bar.draw()

    def pathfind(self, input, physics, dx, dy, cur_y_acceleration, cur_player_speed_x, cur_player_speed_y, jump_is_possible, water_movement):
        if input.a_hold > 0:
            dx -= int(cur_player_speed_x * self.health_bar.get_low_energy_speed_reduction_factor())
            self.apply_movement_cost_x()
        if input.d_hold > 0:
            dx += int(cur_player_speed_x * self.health_bar.get_low_energy_speed_reduction_factor())
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

        return dx, dy, cur_y_acceleration, cur_player_speed_y, water_movement

