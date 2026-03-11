import pygame
from math import floor, sqrt

from world.blocks.block_export import *
from play.mining_sprite import Mining_Sprite
from components.blit_letterboxed import blit_letterboxed
from components.game_file_reading import save_game


class Play:
    def __init__(self, screen, BLOCK_WIDTH, grid, inventory, player, world_details, menu):
        # set details
        self.grid, self.inventory, self.player, self.world_details = grid, inventory, player, world_details
        self.menu = menu
        self.screen = screen
        self.BLOCK_WIDTH = BLOCK_WIDTH

        # prep the world to work
        self.mining_sprite = Mining_Sprite(screen, BLOCK_WIDTH)
        self.destroy_held_time = 0
        self.build_held_time = 0
        self.affected_x, self.affected_y = None, None
        self.build_mode = False

        self.mining_sprite.set_grid(grid)
        self.camera_x = player.x + (player.x_size // 2) - (screen.get_width() // 2)
        self.camera_y = player.y + (player.y_size // 2) - (screen.get_height() // 2)
        self.cur_camera_y = self.camera_y

        # this is some predefined constants that are used at runtime
        self.physics_rules = Physics_Rules(screen, inventory.inventory_height)
        self.background_color = (30, 30, 30)


    # ------------------------------ helper functions ------------------------------ #

    @staticmethod
    def pixel_to_grid(pixel_coordinates, BLOCK_WIDTH):
        grid_coordinates = floor(pixel_coordinates / BLOCK_WIDTH)
        return grid_coordinates

    def get_affected_block(self, player, grid, pointer_x, pointer_y, build_mode = True): #pointers (expected as 1, 0, or -1) give direction of arrow
        # get center of origin
        x = self.pixel_to_grid(player.x + (0.5 * player.x_size), self.BLOCK_WIDTH)
        y = self.pixel_to_grid(player.y + (0.5 * player.y_size), self.BLOCK_WIDTH)

        # set out of bounds savers
        out_of_bounds_x, out_of_bounds_y = None, None

        # run through the first 3 blocks away to see when you hit a block
        for i in range(1, 4):
            x += pointer_x
            y += pointer_y
            if grid.in_bounds(x,y):
                if grid.get(x,y) != None:
                    return x, y
            else:
                out_of_bounds_x, out_of_bounds_y = x, y
            
        if not self.build_mode:
            return None, None
        return out_of_bounds_x, out_of_bounds_y

    def get_affected_block_pointer(self, player, grid, pointer_x, pointer_y, build_mode = True): #pointers (expected as 1, 0, or -1) give direction of arrow
        # using vector raycasting
        start_x = player.x + floor(0.5 * player.x_size)
        start_y = player.y + floor(0.5 * player.y_size)

        # calculate vector step
        dx, dy = pointer_x - start_x, pointer_y - start_y        
        length = sqrt(dx*dx + dy*dy)
        if length == 0: # if the player's cursor is exactly in their center it will just return the player's center's block
            if grid.get(self.pixel_to_grid(start_x, grid.BLOCK_WIDTH), self.pixel_to_grid(start_y, grid.BLOCK_WIDTH)) is None:
                return None, None
            else:
                return self.pixel_to_grid(start_x, grid.BLOCK_WIDTH), self.pixel_to_grid(start_y, grid.BLOCK_WIDTH)
        else:
            ux, uy = dx / length, dy / length

        # now step outward
        reach_sq = 4 * grid.BLOCK_WIDTH * 4 * grid.BLOCK_WIDTH # reach of 4 blocks squared
        distrance_stepped_sq = 0
        step = 0
        while distrance_stepped_sq < reach_sq:
            grid_x = floor((start_x + ux * step) / grid.BLOCK_WIDTH)
            grid_y = floor((start_y + uy * step) / grid.BLOCK_WIDTH)

            if grid.get(grid_x, grid_y) is not None:
                return grid_x, grid_y
            
            distrance_stepped_sq = ((ux * step) * (ux * step)) + ((uy * step) * (uy * step))
            step += 0.025

        return None, None

    def get_affected_block_pointer_build(self, player, grid, pointer_x, pointer_y, inventory, build_mode = True, acknowledge_interactions=True): #pointers (expected as 1, 0, or -1) give direction of arrow
        # using vector raycasting
        start_x = player.x + floor(0.5 * player.x_size)
        start_y = player.y + floor(0.5 * player.y_size)

        # calculate vector step
        dx, dy = pointer_x - start_x, pointer_y - start_y
        length = sqrt(dx*dx + dy*dy)
        if length == 0: # if the player's cursor is exactly in their center it will just return the player's center's block
            if grid.get(self.pixel_to_grid(start_x, grid.BLOCK_WIDTH), self.pixel_to_grid(start_y, grid.BLOCK_WIDTH)) is None:
                return None, None
            else:
                return self.pixel_to_grid(start_x, grid.BLOCK_WIDTH), self.pixel_to_grid(start_y, grid.BLOCK_WIDTH)
        else:
            ux, uy = dx / length, dy / length

        # now step outward
        d_step = 0.025
        reach_sq = 4 * grid.BLOCK_WIDTH * 4 * grid.BLOCK_WIDTH # reach of 4 blocks squared
        distrance_stepped_sq = 0
        step = 0
        while distrance_stepped_sq < reach_sq:
            grid_x = floor((start_x + ux * step) / grid.BLOCK_WIDTH)
            grid_y = floor((start_y + uy * step) / grid.BLOCK_WIDTH)

            if grid.get(grid_x, grid_y) is not None:
                if acknowledge_interactions:
                    if grid.get(grid_x, grid_y).interaction(inventory):
                        return None, None
                    else:
                        x_place_spot = floor((start_x + ux*(step - d_step)) / grid.BLOCK_WIDTH)
                        y_place_spot = floor((start_y + uy*(step - d_step)) / grid.BLOCK_WIDTH)

                        return x_place_spot, y_place_spot
                else:
                    x_place_spot = floor((start_x + ux*(step - d_step)) / grid.BLOCK_WIDTH)
                    y_place_spot = floor((start_y + uy*(step - d_step)) / grid.BLOCK_WIDTH)

                    return x_place_spot, y_place_spot

                
            distrance_stepped_sq = ((ux * step) * (ux * step)) + ((uy * step) * (uy * step))
            step += d_step

        return None, None

    def set_camera_offset(self):
        # x camera movement
        left_bound = self.camera_x + (self.screen.get_width() // 4)
        right_bound = self.camera_x + ((self.screen.get_width() * 3) // 4)

        if self.player.x < left_bound:
            self.camera_x = self.player.x - self.screen.get_width() // 4

        elif self.player.x + self.player.x_size > right_bound:
            self.camera_x = self.player.x + self.player.x_size - ((3 * self.screen.get_width()) // 4)


        # y camera movement     # this still has some funky moments but mostly works at this point   
        camera_y = self.cur_camera_y
        if self.player.y + self.player.y_size > self.physics_rules.MOVEMENT_ALTITUDE_PX:
            camera_y = self.player.y + self.player.y_size - self.physics_rules.MOVEMENT_ALTITUDE_PX

        SMOOTH = 0.4
        self.cur_camera_y = int(self.cur_camera_y + (camera_y - self.cur_camera_y) * SMOOTH)


        world_h_px = self.grid.height * self.BLOCK_WIDTH
        self.cur_camera_y = max(0, min(self.cur_camera_y, world_h_px - self.physics_rules.true_height))


    # ---------------------------- main actions ---------------------------- #

    def interact_with_grid(self, input):

        if input.l_shift_hold > 0: prevent_block_interaction = True
        else: prevent_block_interaction = False

        world_mouse_x = input.virtual_mouse_x + self.camera_x
        world_mouse_y = input.virtual_mouse_y + self.cur_camera_y

        # process block interaction data
        self.affected_x, self.affected_y = self.get_affected_block_pointer(self.player, self.grid, world_mouse_x, world_mouse_y)

        if input.mouse.get_pressed()[0] and self.affected_x is not None:
            self.destroy_held_time+=1
            self.mining_sprite.set(self.affected_x, self.affected_y)
        else:
            self.destroy_held_time = 0
            self.mining_sprite.reset()

        if input.mouse.get_pressed()[2]:
            self.build_held_time+=1
            self.build_mode = True
        else:
            self.build_held_time = 0
            self.build_mode = False


        if self.affected_x is not None:
            if input.mouse.get_pressed()[2]:
                if (self.build_held_time - 1) % self.physics_rules.BUILD_HOLD_THRESHOLD == 0 and self.build_held_time - 1 != self.physics_rules.BUILD_HOLD_THRESHOLD:
                    build_affected_x, build_affected_y = self.get_affected_block_pointer_build(self.player, self.grid, world_mouse_x, world_mouse_y, self.inventory, acknowledge_interactions=not prevent_block_interaction)
                    # check to see if the block can be built
                    if build_affected_x is not None and not self.player.reject_block_placement(build_affected_x, build_affected_y):
                        # now build the block
                        Block_Type = self.inventory.get_current()
                        if Block_Type is not None:
                            if issubclass(Block_Type, MutliBlock):
                                if Block_Type.BuildMulti(self.grid, build_affected_x, build_affected_y) == True:
                                    self.inventory.build_from_current()
                            else:
                                self.grid.set(build_affected_x, build_affected_y, Block_Type)
                                self.inventory.build_from_current()
            
            elif input.mouse.get_pressed()[0]:
                if self.grid.get(self.affected_x, self.affected_y) is not None and self.destroy_held_time > self.grid.get(self.affected_x, self.affected_y).ticks_to_mine:
                    self.destroy_held_time = 0
                    selected_block = self.grid.get(self.affected_x, self.affected_y)
                    if issubclass(type(selected_block), SubMultiBlock):
                        inventory_block_type = selected_block.onDestroy()
                        if inventory_block_type is not None:
                            self.inventory.add_item(inventory_block_type)
                    else:
                        if selected_block.can_move_to_inventory():
                            selected_block.onDestruction(self.inventory) # run any onDestruction methods
                            self.inventory.add_item(type(selected_block))
                        self.grid.set(self.affected_x, self.affected_y, None)

    def run_main_game(self, input):
        
        # step 1: check for if the player wants to quit BEFORE running frame logic
        if input.escape_keypress:
            self.prep_menu()
            return self.menu

        # step 2: interact with blocks
        self.interact_with_grid(input)

        # step 3: move player
        self.player.move(input, self.physics_rules)

        return self

    def prep_menu(self):
        self.menu.draw_saving_world_screen()
        if self.inventory.is_open(): self.inventory.close()
        blit_letterboxed(self.screen, self.menu.window, self.menu.loading_world_screen_background_color)
        pygame.display.flip()
        pygame.event.pump()
        save_game(f"{self.menu.game_files_directory}/{self.menu.world_name}", self.player, self.inventory, self.grid, self.world_details)
        self.menu.reopen_menu_prep()


    # ---------------------------- interacting with main loop ---------------------------- #

    def catch_exception(self):
        pass

    def run(self, input):
        # initialize return_class
        return_class = self
        
        if not self.inventory.show_full_item_management:
            return_class = self.run_main_game(input)
            if return_class is not self: return return_class

            # set camera variables
            self.set_camera_offset()

            # execute physics
            self.grid.physics(self.camera_x, self.cur_camera_y, self.inventory.inventory_height)

            # # get player icon direction using movement direction UNLESS they are actively interacting with a block
            if input.mouse.get_pressed()[0] or input.mouse.get_pressed()[2]: is_interacting = True
            else: is_interacting = False
            screen_x = self.player.x - self.camera_x
            self.player.get_direction(self.player.dx, screen_x, input.virtual_mouse_x, is_interacting)


            # ------------- draw main game ------------- #

            self.screen.fill(self.background_color)

            self.grid.draw(self.camera_x, self.cur_camera_y, self.inventory.inventory_height)

            if self.affected_x != None and not self.build_mode and self.grid.get(self.affected_x, self.affected_y) != None:
                if self.destroy_held_time > 0:
                    self.grid.get(self.affected_x, self.affected_y).draw(True, camera_x = self.camera_x, camera_y = self.cur_camera_y)
                    self.mining_sprite.draw(self.camera_x, self.cur_camera_y)
                else:
                    self.grid.get(self.affected_x, self.affected_y).draw(True, camera_x = self.camera_x, camera_y = self.cur_camera_y)
                    
            self.player.draw(self.camera_x, self.cur_camera_y)


        # ------------- run inventory ------------- #
        
        self.inventory.run(input) # this is resetting the value of self.inventory.show_full_item_mamagement BEFORE the loop runs with that! it forces exit incorrectly. fix!

        # ------------- draw inventory ------------- #

        self.inventory.draw()        

        return return_class

        
class Physics_Rules:
    def __init__(self, screen, inventory_height):
        # set physics rules
        self.Y_ACCELERATION = 0.7
        self.WATER_UPWARD_ACCEL = -0.05
        self.JUMP_VELOCITY = -14

        self.BUILD_HOLD_THRESHOLD = 10 # count of frames held before destroyed motion happens

        self.true_height = screen.get_height() - inventory_height
        self.MOVEMENT_ALTITUDE_PX = (self.true_height * 13) // 16
