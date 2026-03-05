import warnings
import traceback

warnings.filterwarnings( # you should probably delete this at some point but deprecation warnings were getting annoying
    "ignore",
    message="pkg_resources is deprecated as an API.*",
    category=UserWarning,
)

import os
os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "1"

import pygame
from math import floor, sqrt
import json
from pathlib import Path

from grid import Grid
from player import Player
from blocks import *
from items_management import Inventory
from menu import Menu
from world_generation import *
from world_details import World_Details
from images import Images
from game_file_reading import *
from mining_sprite import Mining_Sprite

# from windows_path_resources import *
from mac_path_resources import *


# pyinstaller command line
r"""
mac: python3 -m PyInstaller --clean --noconfirm --windowed --name "IntoTheUnder" --icon "game_files/image_files/ITU-Icon.icns" --add-data "game_files:game_files" intotheunder.py

windows: py -m PyInstaller --clean --noconfirm --windowed --name "IntoTheUnder" --icon "game_files\image_files\ITU-Icon.ico" --add-data "game_files;game_files" intotheunder.py

"""

# converting .png to ico (windows) https://convertico.com/

# to zip without metadata for windows on mac -> zip -r -X IntoTheUnder.zip IntoTheUnder


# update notes:
# - improved inventory UI
# - added crafting new items
# - added chests to store items
# - added functioning doors
# - let left shift key ignore item interactions
# - added items
# - added new blocks
# - fixed incorrect exit screen



# functions
def pixel_to_grid(pixel_coordinates, BLOCK_WIDTH):
    grid_coordinates = floor(pixel_coordinates / BLOCK_WIDTH)
    return grid_coordinates

def get_affected_block(player, grid, pointer_x, pointer_y, build_mode = True): #pointers (expected as 1, 0, or -1) give direction of arrow
    # get center of origin
    x = pixel_to_grid(player.x + (0.5 * player.x_size), BLOCK_WIDTH)
    y = pixel_to_grid(player.y + (0.5 * player.y_size), BLOCK_WIDTH)

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
        
    if not build_mode:
        return None, None
    return out_of_bounds_x, out_of_bounds_y

def get_affected_block_pointer(player, grid, pointer_x, pointer_y, build_mode = True): #pointers (expected as 1, 0, or -1) give direction of arrow
    # using vector raycasting
    start_x = player.x + floor(0.5 * player.x_size)
    start_y = player.y + floor(0.5 * player.y_size)

    # calculate vector step
    dx, dy = pointer_x - start_x, pointer_y - start_y        
    length = sqrt(dx*dx + dy*dy)
    if length == 0: # if the player's cursor is exactly in their center it will just return the player's center's block
        if grid.get(pixel_to_grid(start_x, grid.BLOCK_WIDTH), pixel_to_grid(start_y, grid.BLOCK_WIDTH)) is None:
            return None, None
        else:
            return pixel_to_grid(start_x, grid.BLOCK_WIDTH), pixel_to_grid(start_y, grid.BLOCK_WIDTH)
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

def get_affected_block_pointer_build(player, grid, pointer_x, pointer_y, inventory, build_mode = True, acknowledge_interactions=True): #pointers (expected as 1, 0, or -1) give direction of arrow
    # using vector raycasting
    start_x = player.x + floor(0.5 * player.x_size)
    start_y = player.y + floor(0.5 * player.y_size)

    # calculate vector step
    dx, dy = pointer_x - start_x, pointer_y - start_y
    length = sqrt(dx*dx + dy*dy)
    if length == 0: # if the player's cursor is exactly in their center it will just return the player's center's block
        if grid.get(pixel_to_grid(start_x, grid.BLOCK_WIDTH), pixel_to_grid(start_y, grid.BLOCK_WIDTH)) is None:
            return None, None
        else:
            return pixel_to_grid(start_x, grid.BLOCK_WIDTH), pixel_to_grid(start_y, grid.BLOCK_WIDTH)
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

def generate_world(screen, window, grid_width, grid_depth, world_name):
    # initialize grid and terrain
    grid = Grid(grid_width, grid_depth, BLOCK_WIDTH, screen) #sets width at 200 blocks
    generate_world_blocks(grid, grid_width, grid_depth)

    # initialize inventory, player, and world
    inventory = Inventory(screen, window, INVENTORY_HEIGHT, HEALTH_BAR_HEIGHT)
    player = Player(grid, screen, ((grid_width * BLOCK_WIDTH) // 2), 0, BLOCK_WIDTH, x_size=22, y_size = 40, inventory_bar_height=INVENTORY_HEIGHT, health_bar_height = HEALTH_BAR_HEIGHT, images=images)
    world_details = World_Details.create_new_world(world_name, VERSION)

    return grid, inventory, player, world_details

def blit_letterboxed(src, dst, color):
    sw, sh = src.get_size()
    dw, dh = dst.get_size()
    scale = min(dw / sw, dh / sh)
    new_size = (int(sw * scale), int(sh * scale))
    x = (dw - new_size[0]) // 2
    y = (dh - new_size[1]) // 2
    scaled = pygame.transform.smoothscale(src, new_size)
    dst.fill(color)
    dst.blit(scaled, (x, y))
    return scale, x, y  # useful for mouse coordinate mapping

def get_scaled_mouse_click(scale, mx, my, offx, offy):
    if scale == 0: #forcefully stops divide by 0, may cause different errors but this should not happen
        return None, None
    
    gx = (mx - offx) / scale
    gy = (my - offy) / scale

    return gx, gy

def get_user_worlds_list(game_files_directory, IMAGES_FILE_NAME):
    def convert_file_to_class(wd_file_path): #converts file to class
        try:
            with open(wd_file_path, "r") as world_details_file:
                return World_Details.fill_from_dict(json.load(world_details_file))
        except: # prevents crash on launch with a bad details file by adding dummy file
            cur_timestamp = World_Details.get_corrupted_timestamp()
            file_name = Path(wd_file_path).parent.name
            return World_Details(f"{file_name} (CORRUPTED)", VERSION, cur_timestamp, cur_timestamp, True)

    # gets the file names for all user worlds and sorts them in order of last opened
    game_files_folder = Path(game_files_directory)

    world_details_class_list = [convert_file_to_class(f"{file}/world_details.json") for file in game_files_folder.rglob("*") if file.is_dir() and file.name != IMAGES_FILE_NAME]
    world_details_class_list.sort(key=lambda world:world.last_modified_date, reverse=True)

    return [world.world_name for world in world_details_class_list if not world.version > VERSION]


# implementation details
BLOCK_WIDTH = 25

screen_height_px = 620
screen_width_px = floor(screen_height_px / 0.625) + 100

HEALTH_BAR_HEIGHT = 20 # included in INVENTORY_HEIGHT
grid_height_px = screen_height_px // 48
INVENTORY_HEIGHT = HEALTH_BAR_HEIGHT + (grid_height_px * 7) # this is so hard coded. please change this at some point.


# cur_seed = 12
# random.seed(cur_seed)

APP_NAME = "Into The Under"
APP_DISPLAY_NAME = "Into The Under 1.5.0"
VERSION_NAME = "intotheunder1.5.0"
VERSION = 1.5 # primary version - ex 1.3.1 becomes 1.3
GAME_FILE_FOLDER_NAME = "game_files"
IMAGES_FILE_NAME = "image_files"
pygame_icon_file = "ITU-Icon.png"

game_files_location = VERSION_NAME + '/' + GAME_FILE_FOLDER_NAME

save_path = user_data_dir(APP_NAME)
directory = os.path.join(save_path, game_files_location)
os.makedirs(directory, exist_ok=True)

# initalize pygame
pygame.init()
pygame.font.init()

icon_surface = pygame.image.load(resource_path(f"game_files/{IMAGES_FILE_NAME}/{pygame_icon_file}"))
pygame.display.set_icon(icon_surface)

# create the screen
background_color = (30,30,30)
window = pygame.display.set_mode((screen_width_px, screen_height_px), pygame.RESIZABLE)
screen = pygame.Surface((screen_width_px, screen_height_px))
pygame.display.set_caption(APP_DISPLAY_NAME)

# load in images
images = Images(resource_path(f"game_files/{IMAGES_FILE_NAME}"), BLOCK_WIDTH)

# initialize mining sprite
mining_sprite = Mining_Sprite(screen, BLOCK_WIDTH)


true_height = screen_height_px - INVENTORY_HEIGHT
MOVEMENT_ALTITUDE_PX = (true_height * 13) // 16

# set grid size
grid_width = 5000
grid_height = 100


# clock features
clock = pygame.time.Clock()
TICKS = 60

# set gravity variables
Y_ACCELERATION = 0.7
WATER_UPWARD_ACCEL = -0.05
JUMP_VELOCITY = -14


# arrow key press variables
destroy_held_time = 0 # holds count of frames held
build_held_time = 0
BUILD_HOLD_THRESHOLD = 10 # count of frames held before destroyed motion happens
block_selected = (None, None) # block coordinates of which block will be affected
game_is_loaded = False

build_mode = False #true for build, false for destroy
prevent_block_interaction = False

# counters of frames with key pressed
return_key_state = 0

# run details
running = True
menu = Menu(screen, images, screen_width_px, screen_height_px, BLOCK_WIDTH, get_user_worlds_list(directory, IMAGES_FILE_NAME), directory)
scroll_change = 0


# ----------------------------------------------- run loop ------------------------------------------------ #
try:
    while running and menu.menu_running:

        scale, offx, offy = blit_letterboxed(screen, window, background_color)

        typing_key = None
        if menu.new_world_name_text_box.is_typing:
            pygame.key.start_text_input()
        else:
            pygame.key.stop_text_input()

        # event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                if game_is_loaded: 
                    menu.draw_saving_world_screen()
                    blit_letterboxed(screen, window, background_color)
                    pygame.display.flip()
                    pygame.event.pump()

                    if inventory.is_open(): inventory.close()
                    save_game(f"{directory}/{menu.world_name}", player, inventory, grid, world_details)
            
            if event.type == pygame.TEXTINPUT: 
                typing_key = event.text

            if event.type == pygame.MOUSEWHEEL:
                scroll_change += event.y

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if game_is_loaded:
                        menu.draw_saving_world_screen()
                        if inventory.is_open(): inventory.close()
                        blit_letterboxed(screen, window, background_color)
                        pygame.display.flip()
                        pygame.event.pump()
                        save_game(f"{directory}/{menu.world_name}", player, inventory, grid, world_details)
                        menu.world_names_list.remove(menu.world_name)
                        menu.world_names_list.insert(0, menu.world_name)
                    game_is_loaded = False
                    menu.run_game = False
                    # menu = Menu(screen, screen_width_px, screen_height_px, BLOCK_WIDTH, menu.world_names_list) # generates new menu
                    menu.return_to_main()
                if event.key == pygame.K_e:
                    if game_is_loaded:
                        if inventory.show_full_item_management:
                            inventory.close()
                        else:
                            inventory.open()
                if event.key == pygame.K_BACKSPACE and menu.new_world_name_text_box.is_typing:
                    typing_key = "backspace"


        # run game
        if menu.run_game:
            # initialize run variables
            dx = 0
            dy = 0

            tx, ty = pygame.mouse.get_pos()
            scaled_mouse_pos_x, scaled_mouse_pos_y = get_scaled_mouse_click(scale, tx, ty, offx, offy)
            world_mx, world_my = scaled_mouse_pos_x + camera_x, scaled_mouse_pos_y + cur_camera_y

            inventory.check_click(pygame.mouse, scaled_mouse_pos_x, scaled_mouse_pos_y)


            # find out if player is touching a block that slows down movement
            cur_y_acceleration = Y_ACCELERATION
            cur_player_speed_x = player.player_speed
            cur_y_acceleration, cur_player_speed_x, cur_player_speed_y, jump_is_possible = player.get_player_physics(Y_ACCELERATION)
            if cur_player_speed_y > 0: water_movement = True
            else: water_movement = False
            

            # get scrolling for switching inventory
            if abs(scroll_change) > 0:
                inventory.scroll_change_inventory_position(scroll_change)
                scroll_change = 0

            # input (held keys)
            keys = pygame.key.get_pressed()

            if not inventory.show_full_item_management: # right now if this is active, it pauses the whole game

                if keys[pygame.K_RETURN]:
                    return_key_state += 1
                else:
                    return_key_state = 0
                if keys[pygame.K_LSHIFT]:
                    prevent_block_interaction = True
                else:
                    prevent_block_interaction = False

                if keys[pygame.K_a]:
                    dx -= cur_player_speed_x
                if keys[pygame.K_d]:
                    dx += cur_player_speed_x 
                keys = pygame.key.get_pressed()
                if keys[pygame.K_w] or keys[pygame.K_SPACE]:
                    if not player.is_not_block_below() and jump_is_possible:
                        player.y_vel = JUMP_VELOCITY
                        player.ticks_falling = 1
                        player.ticks_inc = False
                    if water_movement:
                        cur_y_acceleration = WATER_UPWARD_ACCEL
                if keys[pygame.K_s]:
                    if water_movement: 
                        player.y_vel = cur_player_speed_y




                # process return key data (alt inventory selection method)
                if return_key_state == 1:
                    if keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]:
                        inventory.increment_cur_position(False)
                    else:
                        inventory.increment_cur_position(True)


                # process block interaction data
                dir_x, dir_y = scaled_mouse_pos_x + camera_x, scaled_mouse_pos_y + cur_camera_y

                affected_x, affected_y = get_affected_block_pointer(player, grid, world_mx, world_my)

                if pygame.mouse.get_pressed()[0] and affected_x is not None:
                    destroy_held_time+=1
                    mining_sprite.set(affected_x, affected_y)
                else:
                    destroy_held_time = 0
                    mining_sprite.reset()

                if pygame.mouse.get_pressed()[2]:
                    build_mode = True
                    build_held_time+=1
                else:
                    build_held_time = 0
                    build_mode = False


                if affected_x is not None:
                    if pygame.mouse.get_pressed()[2]:
                        if (build_held_time - 1) % BUILD_HOLD_THRESHOLD == 0 and build_held_time - 1 != BUILD_HOLD_THRESHOLD:
                            build_affected_x, build_affected_y = get_affected_block_pointer_build(player, grid, world_mx, world_my, inventory, acknowledge_interactions=not prevent_block_interaction)
                            # check to see if the block can be built
                            # right here you could check for if the block has a special attribute when it's selected -also bypass it with shift
                            if build_affected_x is not None and not player.reject_block_placement(build_affected_x, build_affected_y):
                                # now build the block
                                Block_Type = inventory.get_current()
                                if Block_Type is not None:
                                    if issubclass(Block_Type, MutliBlock):
                                        if Block_Type.BuildMulti(grid, build_affected_x, build_affected_y) == True:
                                            inventory.build_from_current()
                                    else:
                                        grid.set(build_affected_x, build_affected_y, Block_Type)
                                        inventory.build_from_current()
                    
                    elif pygame.mouse.get_pressed()[0]:
                        if grid.get(affected_x, affected_y) is not None and destroy_held_time > grid.get(affected_x, affected_y).ticks_to_mine:
                            # affected_block.interaction()
                            destroy_held_time = 0
                            selected_block = grid.get(affected_x, affected_y)
                            if issubclass(type(selected_block), SubMultiBlock):
                                inventory_block_type = selected_block.onDestroy()
                                if inventory_block_type is not None:
                                    inventory.add_item(inventory_block_type)
                            else:
                                if selected_block.can_move_to_inventory():
                                    selected_block.onDestruction(inventory) # run any onDestruction methods
                                    inventory.add_item(type(selected_block))
                                grid.set(affected_x, affected_y, None)


                # apply gravity and jumping
                if player.y_vel + (cur_y_acceleration * player.ticks_falling) < BLOCK_WIDTH: #limits gravity at 1 block per tick
                    dy += player.y_vel + (cur_y_acceleration * player.ticks_falling)


                # check if motion is legal
                if water_movement: dy *= 0.4
                collided = player.is_move_ok_y(dy)

                # if collided and dy > 0 and abs(player.y_vel) > player.take_damage_threshold_velocity:
                #     print("executed")
                #     if player.health_bar.health > 0: player.health_bar.health -= player.loss_per_velocity * (abs(player.y_vel) - player.take_damage_threshold_velocity )

                x_move = abs(dx)
                if dx < 0: x_direction = -1
                else: x_direction = 1
                while x_move >= 0:
                    if player.is_move_ok_x(x_move * x_direction):
                        player.x += (x_move * x_direction)
                        break
                    x_move -= 1

                # increment gravity
                if dy == 0:
                    player.y_vel = 0
                    player.ticks_falling = 1
                else:
                    player.y_vel += cur_y_acceleration
                    if player.ticks_inc:
                        player.ticks_falling += 1
                    else:
                        player.ticks_inc = True


                # x camera movement
                left_bound = camera_x + (screen_width_px // 4)
                right_bound = camera_x + ((screen_width_px * 3) // 4)

                if player.x < left_bound:
                    camera_x = player.x - screen_width_px // 4

                elif player.x + player.x_size > right_bound:
                    camera_x = player.x + player.x_size - ((3 * screen_width_px) // 4)


                # y camera movement     # this still has some funky moments but mostly works at this point   
                camera_y = cur_camera_y
                if player.y + player.y_size > MOVEMENT_ALTITUDE_PX:
                    camera_y = player.y + player.y_size - MOVEMENT_ALTITUDE_PX

                SMOOTH = 0.4
                cur_camera_y = int(cur_camera_y + (camera_y - cur_camera_y) * SMOOTH)


                world_h_px = grid.height * BLOCK_WIDTH
                cur_camera_y = max(0, min(cur_camera_y, world_h_px - true_height))


                # execute physics
                grid.physics(camera_x, cur_camera_y, INVENTORY_HEIGHT)

                # # get player icon direction using movement direction UNLESS they are actively interacting with a block
                if pygame.mouse.get_pressed()[0] or pygame.mouse.get_pressed()[2]: is_interacting = True
                else: is_interacting = False
                screen_x = player.x - camera_x
                player.get_direction(dx, screen_x, scaled_mouse_pos_x, is_interacting)
                

            # drawing
            screen.fill(background_color)

            grid.draw(camera_x, cur_camera_y, INVENTORY_HEIGHT)

            if affected_x != None and not build_mode and grid.get(affected_x, affected_y) != None:
                if destroy_held_time > 0:
                    grid.get(affected_x, affected_y).draw(True, camera_x = camera_x, camera_y = cur_camera_y)
                    mining_sprite.draw(camera_x, cur_camera_y)
                else:
                    grid.get(affected_x, affected_y).draw(True, camera_x = camera_x, camera_y = cur_camera_y)
                    
            player.draw(camera_x, cur_camera_y)

            inventory.draw()


        # run menu
        else: #this is for the menu screens
            tx, ty = pygame.mouse.get_pos()
            scaled_mouse_pos_x, scaled_mouse_pos_y = get_scaled_mouse_click(scale, tx, ty, offx, offy)
            menu.check_click(pygame.mouse, scaled_mouse_pos_x, scaled_mouse_pos_y)
            menu.move_background()
            menu.draw(scaled_mouse_pos_x, scaled_mouse_pos_y, typing_key)

            if menu.run_game: # check for if it's time to move on and generate world before launch
                menu.draw_loading_world_screen()
                scale, offx, offy = blit_letterboxed(screen, window, background_color)
                pygame.display.flip()
                pygame.event.pump()

                # functions for loading or generating a world!
                if menu.load_world:
                    grid, inventory, player, world_details = load_world(f"{directory}/{menu.world_name}", screen, window, INVENTORY_HEIGHT, HEALTH_BAR_HEIGHT, BLOCK_WIDTH, images)
                    mining_sprite.set_grid(grid)
                    camera_x = player.x + (player.x_size // 2) - (screen_width_px // 2)
                    camera_y = player.y + (player.y_size // 2) - (screen_height_px // 2)
                    cur_camera_y = camera_y
                    game_is_loaded = True
                elif menu.generate_new_world:
                    menu.world_names_list.insert(0, menu.world_name)
                    grid, inventory, player, world_details = generate_world(screen, window, grid_width, grid_height, menu.world_name)
                    mining_sprite.set_grid(grid)
                    new_directory_path = Path(f"{directory}/{menu.world_name}")
                    new_directory_path.mkdir()
                    save_game(new_directory_path, player, inventory, grid, world_details)
                    camera_x = player.x + (player.x_size // 2) - (screen_width_px // 2)
                    camera_y = player.y + (player.y_size // 2) - (screen_height_px // 2)
                    cur_camera_y = camera_y
                    game_is_loaded = True

        # update screen
        pygame.display.flip()


        # update clock
        clock.tick(TICKS)

except Exception as e:
    print("CRASH DETECTED")
    traceback.print_exc()

    running = False
    if game_is_loaded: 
        menu.draw_saving_world_screen()
        blit_letterboxed(screen, window, background_color)
        pygame.display.flip()
        pygame.event.pump()

        if inventory.is_open(): inventory.close()
        save_game(f"{directory}/{menu.world_name}", player, inventory, grid, world_details)


pygame.quit()