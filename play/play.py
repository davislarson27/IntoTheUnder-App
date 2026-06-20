import pygame
from math import floor, sqrt

from world.blocks.block_export import *
from play.mining_sprite import Mining_Sprite
from components.game_file_reading import save_game
from .physics_rules import Physics_Rules
from .in_play_menus.escape_menu import Escape_Menu
from components.crash_menu import Crash_Menu
from .bg_overlay import BG_Overlay
from .bg_mining_icon import Bg_Mining_Icon
from .in_play_menus.debug_screen_overlay import Debug_Overlay
from .in_play_menus.death_menu import Death_Menu
from .inventory.inventory import Inventory
from .inventory.submenus.crafting import Crafting_Slots
from .inventory.submenus.fuel import Fuel_Slots
from .inventory.submenus.chest import Chest_Slots
from .inventory.submenus.enduring_chest import Enduring_Chest_Slots
from .entities.entities_export import *
from .star_background import Star_Background


class Play:

    def __init__(self, screen, BLOCK_WIDTH, grid, background_grid, inventory, player, world_details, menu):
        # set details
        self.grid, self.inventory, self.player, self.world_details = grid, inventory, player, world_details
        self.background_grid = background_grid
        self.menu = menu
        self.screen = screen
        self.BLOCK_WIDTH = BLOCK_WIDTH

        # set up crash menu
        self.crash_menu = Crash_Menu(screen, menu, self, button_message="Save and Return to Menu")

        # generate in play menus
        self.escape_menu = Escape_Menu(screen)

        # prep substate
        self.sub_state = None # holds the run function for submenus when applicable

        # check for if the recipes are supposed to be filled in
        if not world_details.recipe_progression:
            self.inventory.crafting_object.crafting_recipes.add_all_recipes()

        # prep the world to work
        self.mining_sprite = Mining_Sprite(screen, BLOCK_WIDTH)
        self.destroy_held_time = 0
        self.build_held_time = 0
        self.affected_x, self.affected_y = None, None
        self.build_mode = False

        self.mining_sprite.set_grid(grid)
        self.reset_camera_positions()

        # this is some predefined constants that are used at runtime
        self.physics_rules = Physics_Rules(screen, inventory.inventory_height)
        self.background_color = (30, 30, 30)

        self.active_grid = self.grid

        self.bg_overlay = BG_Overlay(screen, BLOCK_WIDTH, grid, background_grid)

        self.build_block_surfaces()
        
        # gemerate the bg_mining_active icon
        bg_mining_icon_margin = 30
        bg_mining_icon_width = 51
        self.bg_mining_icon = Bg_Mining_Icon(screen, screen.get_width() - bg_mining_icon_width - bg_mining_icon_margin, bg_mining_icon_margin, bg_mining_icon_width, bg_mining_icon_width)

        self.debug_overlay = Debug_Overlay(screen, grid, player)

        self.inventory.set_health_bar(self.player.health_bar)

        self.star_bg = Star_Background(screen)

    # ------------------------------ helper functions ------------------------------ #

    def build_block_surfaces(self):
        for block in get_blocks_list():
            block.draw_to_surface(self.BLOCK_WIDTH, being_mined=True, use_alt_drawing=False)
            block.draw_to_surface(self.BLOCK_WIDTH, being_mined=False, use_alt_drawing=False)
            block.draw_to_surface(self.BLOCK_WIDTH, being_mined=True, use_alt_drawing=True)
            block.draw_to_surface(self.BLOCK_WIDTH, being_mined=False, use_alt_drawing=True)

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

    def get_affected_block_pointer(self, player, pointer_x, pointer_y, allowBgInteract): #pointers (expected as 1, 0, or -1) give direction of arrow
        # using vector raycasting
        start_x = player.x + floor(0.5 * player.x_size)
        start_y = player.y + floor(0.5 * player.y_size)

        # calculate vector step
        dx, dy = pointer_x - start_x, pointer_y - start_y        
        length = sqrt(dx*dx + dy*dy)
        if length == 0: # if the player's cursor is exactly in their center it will just return the player's center's block
            if self.grid.get(self.pixel_to_grid(start_x, self.grid.BLOCK_WIDTH), self.pixel_to_grid(start_y, self.grid.BLOCK_WIDTH)) is None:
                return None, None, self.grid
            elif allowBgInteract and self.background_grid.get(self.pixel_to_grid(start_x, self.background_grid.BLOCK_WIDTH), self.pixel_to_grid(start_y, self.background_grid.BLOCK_WIDTH)) is None:
                return None, None, self.background_grid
            else:
                return self.pixel_to_grid(start_x, self.grid.BLOCK_WIDTH), self.pixel_to_grid(start_y, self.grid.BLOCK_WIDTH), self.grid
        else:
            ux, uy = dx / length, dy / length

        # now step outward
        reach_sq = 4.5 * self.grid.BLOCK_WIDTH * 4.5 * self.grid.BLOCK_WIDTH # reach of 4 blocks squared
        distrance_stepped_sq = 0
        step = 0
        while distrance_stepped_sq < reach_sq:
            grid_x = floor((start_x + ux * step) / self.grid.BLOCK_WIDTH)
            grid_y = floor((start_y + uy * step) / self.grid.BLOCK_WIDTH)

            if self.grid.get(grid_x, grid_y) is not None and not issubclass(type(self.grid.get(grid_x, grid_y)), Water):
                return grid_x, grid_y, self.grid
            elif allowBgInteract and self.background_grid.get(grid_x, grid_y) is not None and not issubclass(type(self.background_grid.get(grid_x, grid_y)), Water):
                return grid_x, grid_y, self.background_grid

            distrance_stepped_sq = ((ux * step) * (ux * step)) + ((uy * step) * (uy * step))
            step += 0.025

        return None, None, self.grid

    def get_affected_block_pointer_build(self, player, grid, pointer_x, pointer_y, inventory, build_mode=True, acknowledge_interactions=True): #pointers (expected as 1, 0, or -1) give direction of arrow
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
        reach_sq = 4.5 * grid.BLOCK_WIDTH * 4.5 * grid.BLOCK_WIDTH # reach of 4 blocks squared
        distrance_stepped_sq = 0
        step = 0
        while distrance_stepped_sq < reach_sq:
            grid_x = floor((start_x + ux * step) / grid.BLOCK_WIDTH)
            grid_y = floor((start_y + uy * step) / grid.BLOCK_WIDTH)

            if grid.get(grid_x, grid_y) is not None and not issubclass(type(grid.get(grid_x, grid_y)), Water):
                if acknowledge_interactions:
                    if grid.get(grid_x, grid_y).interaction(inventory):
                        return None, None
                    else:
                        x_place_spot = floor((start_x + ux*(step - d_step)) / grid.BLOCK_WIDTH)
                        y_place_spot = floor((start_y + uy*(step - d_step)) / grid.BLOCK_WIDTH)
                        
                        if grid.get(x_place_spot, y_place_spot) is not None and not issubclass(type(grid.get(x_place_spot, y_place_spot)), Water):
                            return None, None

                        return x_place_spot, y_place_spot
                else:
                    x_place_spot = floor((start_x + ux*(step - d_step)) / grid.BLOCK_WIDTH)
                    y_place_spot = floor((start_y + uy*(step - d_step)) / grid.BLOCK_WIDTH)

                    if grid.get(x_place_spot, y_place_spot) is not None and not issubclass(type(grid.get(x_place_spot, y_place_spot)), Water):
                        return None, None

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

    def draw_grid(self):
        """used when another class needs to draw the grid - does not draw player or inventory"""
        # ------------- draw main game ------------- #

        # fill screen with base color
        self.screen.fill(self.background_color)

        # draw background blocks
        self.background_grid.draw(self.camera_x, self.cur_camera_y, 0)

        # draw background overlay
        self.bg_overlay.draw(self.camera_x, self.cur_camera_y, 0)

        # draw main grid
        main_grid_queue = self.grid.draw(self.camera_x, self.cur_camera_y, 0)
        
        # now draw the rest of the queue
        main_grid_queue.draw(self.camera_x, self.cur_camera_y)

    def reset_camera_positions(self):
        self.camera_x = self.player.x + (self.player.x_size // 2) - (self.screen.get_width() // 2)
        self.camera_y = self.player.y + (self.player.y_size // 2) - (self.screen.get_height() // 2)
        self.cur_camera_y = self.camera_y

    def respawn_user(self):
        self.player.respawn()
        self.reset_camera_positions()
        if not self.world_details.keep_inventory: self.inventory.clear_inventory_contents()
        return True

    # ---------------------------- main actions ---------------------------- #

    def interact_with_grid(self, input):

        allow_bg_interactions = input.caps_lock

        if input.l_shift_hold > 0: prevent_block_interaction = True
        else: prevent_block_interaction = False

        world_mouse_x = input.virtual_mouse_x + self.camera_x
        world_mouse_y = input.virtual_mouse_y + self.cur_camera_y
        
        self.affected_x, self.affected_y, self.active_grid = self.get_affected_block_pointer(self.player, world_mouse_x, world_mouse_y, allow_bg_interactions)

        # set mining sprite grid
        self.mining_sprite.set_grid(self.active_grid)

        if input.mouse.get_pressed()[0] and self.affected_x is not None and self.active_grid.get(self.affected_x, self.affected_y).can_break:
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
                    build_affected_x, build_affected_y = self.get_affected_block_pointer_build(self.player, self.active_grid, world_mouse_x, world_mouse_y, self.inventory, acknowledge_interactions=not prevent_block_interaction)
                    
                    # reselect the grid for building AFTER identifying where to place the block if necessary
                    if self.build_mode and allow_bg_interactions:
                        self.active_grid = self.background_grid

                    # check to see if the block can be built
                    if build_affected_x is not None and not self.player.reject_block_placement(build_affected_x, build_affected_y):
                        # now build the block
                        Block_Type = self.inventory.get_current()
                        if Block_Type is not None and not issubclass(Block_Type, Item):
                            if issubclass(Block_Type, MutliBlock):
                                if Block_Type.BuildMulti(self.active_grid, build_affected_x, build_affected_y) == True:
                                    self.inventory.build_from_current()
                            else:
                                self.active_grid.set(build_affected_x, build_affected_y, Block_Type)
                                self.inventory.build_from_current()
            
            elif input.mouse.get_pressed()[0]:
                if self.active_grid.get(self.affected_x, self.affected_y) is not None and self.destroy_held_time > self.active_grid.get(self.affected_x, self.affected_y).ticks_to_mine:
                    self.destroy_held_time = 0
                    selected_block = self.active_grid.get(self.affected_x, self.affected_y)
                    inventory_block_type = selected_block.onDestroy(self.inventory)
                    if inventory_block_type is not None:
                        self.inventory.add_item(inventory_block_type)

    def run_main_game(self, input):
        # step 1: interact with blocks
        self.interact_with_grid(input)

        # step 2: move player
        self.player.move(input, self.physics_rules)

        # step 3: check for energy changes
        self.player.manage_energy(self.grid)

        # step 4: check for if the player is alive
        if not self.player.is_alive():
            self.sub_state = Death_Menu(self.screen, self)

        # step 5: return run class
        return self

    def prep_menu(self):
        self.menu.draw_loading_world_screen(0, 'Closing Active States')
        if self.sub_state is not None: self.sub_state.close()
        start_save_percent = 5
        end_save_percent = 95
        for percent, save_message in save_game(f"{self.menu.game_files_directory}/{self.menu.world_name}", self.player, self.inventory, self.grid, self.background_grid, self.world_details, start_save_percent, end_save_percent):
            self.menu.draw_loading_world_screen(percent, save_message)
        self.menu.reopen_menu_prep()

    def manage_menus(self, input):
        """manages the opening and closing of in play menus such as opening the inventory"""
        # check for off cycle inventory open first (meaning open came from a block rather than a keypress, happened on the last loop)
        if self.inventory.open_off_cycle():
            self.sub_state = self.inventory
            self.sub_state.open()
            return

        def operate_menu(menu, esc=False, side_pannel_type=None, side_pannel_open_func=None):
            if esc:
                self.sub_state.close()
                self.sub_state = self.sub_state.onEsc()
            elif self.sub_state is menu:
                same_panel = (
                    side_pannel_type is None
                    or (
                        hasattr(self.sub_state, 'side_pannel')
                        and isinstance(self.sub_state.side_pannel, side_pannel_type)
                    )
                )
                if same_panel:
                    # same menu, same mode → toggle closed
                    self.sub_state.close()
                    self.sub_state = self.sub_state.onEsc()
                else:
                    # same menu, different mode → close old panel, open new one
                    if hasattr(self.sub_state, 'side_pannel'):
                        self.sub_state.side_pannel.close(self.sub_state)
                    if side_pannel_open_func is not None:
                        side_pannel_open_func()
            else:
                if self.sub_state is not None:
                    self.sub_state.close()
                self.sub_state = menu
                if side_pannel_open_func is not None:
                    side_pannel_open_func()
                self.sub_state.open()

        if isinstance(self.inventory.side_pannel, Chest_Slots) and isinstance(self.sub_state, Inventory): # allows easier escaping from chests
            if input.e_keypress or input.c_keypress or input.f_keypress or input.escape_keypress:
                operate_menu(self.inventory, side_pannel_type=Chest_Slots, side_pannel_open_func=self.inventory.open_crafting)
        elif isinstance(self.inventory.side_pannel, Enduring_Chest_Slots) and isinstance(self.sub_state, Inventory): # allows easier escaping from chests
            if input.e_keypress or input.c_keypress or input.f_keypress or input.escape_keypress:
                operate_menu(self.inventory, side_pannel_type=Enduring_Chest_Slots, side_pannel_open_func=self.inventory.open_crafting)
        elif input.e_keypress:
            operate_menu(self.inventory, side_pannel_type=Crafting_Slots, side_pannel_open_func=self.inventory.open_crafting)
        elif input.c_keypress:
            operate_menu(self.inventory.get_recipe_menu()) # this isn't an inventory menu, but it does access it through the inventory
        elif input.f_keypress:
            operate_menu(self.inventory, side_pannel_type=Fuel_Slots, side_pannel_open_func=self.inventory.open_fuel)
        elif input.escape_keypress: # this one works differently
            if self.sub_state is not None:
                operate_menu(self.sub_state, esc=True)
            else:
                operate_menu(self.escape_menu)


    # ---------------------------- interacting with main loop ---------------------------- #

    def catch_exception(self):
        return self.crash_menu

    def finalExceptionHandle(self):
        # attempt to save the game
        try:
            self.prep_menu()
        except Exception as e:
            self.menu.reopen_menu_prep() # minimum required to prep menu
            print('CRASH WHILE ATTEMPTING SAVE')

    def run(self, input, clock):
        # initialize return_class
        return_class = self

        if self.sub_state is not None:
            # check for if a sub_state wants the the play class to quit and return to the menu
            if self.sub_state.sub_state_full_quit():
                self.prep_menu()
                return self.menu

            # run sub_state
            self.sub_state = self.sub_state.run(input) # responsible for drawing

        else:
            # run main game
            return_class = self.run_main_game(input)
            if return_class is not self: return return_class

            # set camera variables
            self.set_camera_offset()

            # execute physics
            self.grid.chunked_physics(self.camera_x, self.cur_camera_y, self.inventory.inventory_height)
            self.background_grid.chunked_physics(self.camera_x, self.cur_camera_y, self.inventory.inventory_height)

            # # get player icon direction using movement direction UNLESS they are actively interacting with a block
            if input.mouse.get_pressed()[0] or input.mouse.get_pressed()[2]: is_interacting = True
            else: is_interacting = False
            screen_x = self.player.x - self.camera_x
            self.player.get_direction(self.player.dx, screen_x, input.virtual_mouse_x, is_interacting)

            # ------------------------------------- temp spawn using enter ------------------------------------- #
            if input.return_keypress:
                Highly_Motivated_Blob.spawn_new(self.grid, self.screen, self.BLOCK_WIDTH, self.player.x, 0, self.world_details)
            # ------------------------------------- end spawn using enter ------------------------------------- #

            # process entities
            entities = self.grid.get_entities(self.camera_x)
            for entity in entities:
                entity.move(input, self.physics_rules)

            # ------------- draw main game ------------- #

            # fill bg
            self.screen.fill(self.background_color)

            # draw stars
            self.star_bg.draw(self.camera_x, self.cur_camera_y)

            # draw background blocks
            self.background_grid.draw(self.camera_x, self.cur_camera_y, self.inventory.inventory_height)
            # draw background overlay
            self.bg_overlay.draw(self.camera_x, self.cur_camera_y, self.inventory.inventory_height)

            # draw main grid
            main_grid_queue = self.grid.draw(self.camera_x, self.cur_camera_y, self.inventory.inventory_height)

            # draw selected block
            if self.affected_x != None and not self.build_mode and self.active_grid.get(self.affected_x, self.affected_y) != None:
                if self.destroy_held_time > 0:
                    self.active_grid.get(self.affected_x, self.affected_y).draw(True, camera_x = self.camera_x, camera_y = self.cur_camera_y)
                    self.mining_sprite.draw(self.camera_x, self.cur_camera_y)
                else:
                    self.active_grid.get(self.affected_x, self.affected_y).draw(True, camera_x = self.camera_x, camera_y = self.cur_camera_y)
                    
            # redraw overlay if the grid is in background mode
            if self.active_grid is self.background_grid and self.affected_x is not None:
                self.bg_overlay.draw_at(self.affected_x, self.affected_y, self.camera_x, self.cur_camera_y)

            self.player.draw(self.camera_x, self.cur_camera_y)
            for entity in entities:
                entity.draw(self.camera_x, self.cur_camera_y)

            # now draw the rest of the queue
            main_grid_queue.draw(self.camera_x, self.cur_camera_y)

            self.bg_mining_icon.draw(input)


            # ------------- run passive inventory ------------- #
            
            self.inventory.run_passive(input) # this is resetting the value of self.inventory.show_full_item_mamagement BEFORE the loop runs with that! it forces exit incorrectly. fix!


            # ------------- draw inventory ------------- #

            self.inventory.draw_passive()

            # ------------- run & draw the debug overlay ------------- #

            self.debug_overlay.run(input, clock)
            self.debug_overlay.draw()

            # ------------- check entity chunks --------------#
            self.grid.check_entity_chunks(entities)


        # check for changing menus in game
        self.manage_menus(input)

        return return_class

    def on_quit(self):
        self.prep_menu()
        