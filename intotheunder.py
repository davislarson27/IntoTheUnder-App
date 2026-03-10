import pygame
from math import floor
import json
import os, sys
from pathlib import Path

from grid import Grid
from player import Player
from blocks import *
from full_inventory import Inventory
from menu import Menu
from world_generation import *
from world_details import World_Details
from images import Images


# python location
# "/Library/Frameworks/Python.framework/Versions/3.12/bin/python3"

# pyinstaller command line
"""
python3 -m PyInstaller --clean --noconfirm --windowed \--name "IntoTheUnder" \--icon "game_files/image_files/icon.icns" \--add-data "game_files:game_files" \intotheunder.py
"""

# additional helpful command line args
# cp -a intotheunder1.3 intotheunder1.3.1 (copies a folder to a new version)


# update notes:
# added a new scren for creating a new world
# patched bug with automatically generated world names


# path based functions
def resource_path(relative_path: str) -> str:
    # When bundled by PyInstaller, files are unpacked to a temp folder: sys._MEIPASS
    base_path = getattr(sys, "_MEIPASS", os.path.abspath("."))
    return os.path.join(base_path, relative_path)

def user_data_dir(app_name="Into The Under"):
    base = os.path.expanduser("~/Library/Application Support")
    path = os.path.join(base, app_name)
    os.makedirs(path, exist_ok=True)
    return path

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

def save_game(directory, player, inventory, grid, world_details):
    grid_dictionary = grid.to_dict()
    with open(f"{directory}/grid.json", "w") as grid_file:
        json.dump(grid_dictionary, grid_file, indent=3)

    player_dictionary = player.to_dict()
    with open(f"{directory}/player_attributes.json", "w") as player_attr_file:
        json.dump(player_dictionary, player_attr_file, indent=3)
    
    inventory_dict = inventory.to_dict()
    with open(f"{directory}/inventory.json", "w") as inventory_file:
        json.dump(inventory_dict, inventory_file, indent=3)

    world_details_dict = world_details.to_dict()
    with open(f"{directory}/world_details.json", "w") as world_details_file:
        json.dump(world_details_dict, world_details_file, indent=3)

def load_world(directory, screen, window, width, height, INVENTORY_HEIGHT, BLOCK_WIDTH):
    with open(f"{directory}/grid.json", "r") as grid_file:
        grid_dict = json.load(grid_file)
        grid = Grid.fill_from_dict(grid_dict, screen, BLOCK_WIDTH)

    with open(f"{directory}/inventory.json", "r") as inventory_file:
        inventory_dict = json.load(inventory_file)
        inventory = Inventory.fill_from_dict(inventory_dict, screen, window, INVENTORY_HEIGHT, HEALTH_BAR_HEIGHT)

    with open(f"{directory}/player_attributes.json", "r") as player_attr_file:
        player_attr_dict = json.load(player_attr_file)
        player_attr_dict["screen"] = screen
        player_attr_dict["grid"] = grid
        player_attr_dict["inventory_bar_height"] = INVENTORY_HEIGHT
        player_attr_dict["health_bar_height"] = HEALTH_BAR_HEIGHT
        player = Player(**player_attr_dict)

    with open(f"{directory}/world_details.json", "r") as world_details_file:
        world_details_dict = json.load(world_details_file)
        # world_details = World_Details(**world_details_dict)
        world_details = World_Details.fill_from_dict(world_details_dict)

    return grid, inventory, player, world_details

def generate_world(screen, window, grid_width, grid_depth, world_name):
    # initialize grid
    grid = Grid(grid_width, grid_depth, BLOCK_WIDTH, screen) #sets width at 200 blocks

    # generate world terrain
    generate_world_blocks(grid, grid_width, grid_depth)

    # initialize inventory
    inventory = Inventory(screen, window, INVENTORY_HEIGHT, HEALTH_BAR_HEIGHT)

    # initialize player in grid
    player = Player(grid, screen, ((grid_width * BLOCK_WIDTH) // 2), 0, BLOCK_WIDTH, x_size=23, y_size = 23, inventory_bar_height=INVENTORY_HEIGHT, health_bar_height = HEALTH_BAR_HEIGHT)

    # initialize world details
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
INVENTORY_HEIGHT = 120
HEALTH_BAR_HEIGHT = 20 # included in INVENTORY_HEIGHT
screen_height_px = 620
screen_width_px = floor(screen_height_px / 0.625) + 100

# cur_seed = 12
# random.seed(cur_seed)

APP_NAME = "Into The Under"
APP_DISPLAY_NAME = "Into The Under 1.3.2"
VERSION_NAME = "intotheunder1.3.2"
VERSION = 1.3 # primary version - ex 1.3.1 becomes 1.3
GAME_FILE_FOLDER_NAME = "game_files"
IMAGES_FILE_NAME = "image_files"
pygame_icon_file = "icon.png"

# game_files_location = VERSION_NAME + '/' + GAME_FILE_FOLDER_NAME + '/' + world_name
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
images = Images(f"game_files/{IMAGES_FILE_NAME}", BLOCK_WIDTH)


true_height = screen_height_px - INVENTORY_HEIGHT
MOVEMENT_ALTITUDE_PX = (true_height * 13) // 16

# set grid size
grid_width = 5000
grid_height = 100


# clock features
clock = pygame.time.Clock()
TICKS = 60

# set gravity variables
Y_ACCELERATION = 1
WATER_UPWARD_ACCEL = -0.05
JUMP_VELOCITY = -15


# arrow key press variables
held_time = 0 # holds count of frames held
DESTROY_HOLD_THRESHOLD = 15 # count of frames held before destroyed motion happens
BUILD_HOLD_THRESHOLD = 3 # count of frames held before destroyed motion happens
block_selected = (None, None) # block coordinates of which block will be affected
game_is_loaded = False

build_mode = True #true for build, false for destroy

# counters of frames with key pressed
return_key_state = 0

# run details
running = True
menu = Menu(screen, images, screen_width_px, screen_height_px, BLOCK_WIDTH, get_user_worlds_list(directory, IMAGES_FILE_NAME), directory)

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

                save_game(f"{directory}/{menu.world_name}", player, inventory, grid, world_details)
        
        if event.type == pygame.TEXTINPUT: 
            typing_key = event.text

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                if game_is_loaded: 
                    menu.draw_saving_world_screen()
                    blit_letterboxed(screen, window, background_color)
                    pygame.display.flip()
                    pygame.event.pump()
                    save_game(f"{directory}/{menu.world_name}", player, inventory, grid, world_details)
                    # temp_world_name = menu.world_name
                    menu.world_names_list.remove(menu.world_name)
                    menu.world_names_list.insert(0, menu.world_name)
                game_is_loaded = False
                # menu = Menu(screen, screen_width_px, screen_height_px, BLOCK_WIDTH, menu.world_names_list) # generates new menu
                menu.return_to_main()
            if event.key == pygame.K_e:
                if game_is_loaded:
                    if inventory.show_full_inventory:
                        inventory.clear_selected_slot_full_inventory()
                        inventory.show_full_inventory = False
                    else:
                        inventory.show_full_inventory = True
            if event.key == pygame.K_BACKSPACE and menu.new_world_name_text_box.is_typing:
                typing_key = "backspace"

        if game_is_loaded and inventory.show_full_inventory and event.type == pygame.MOUSEBUTTONUP and event.button == 1: # only processes if inventory is on
            unscaled_x, unscaled_y = event.pos
            inventory_click_x, inventory_click_y = get_scaled_mouse_click(scale, unscaled_x, unscaled_y, offx, offy)
            inventory.process_click_full_inventory(inventory_click_x, inventory_click_y)


    # run game
    if menu.run_game:
        # initialize run variables
        dx = 0
        dy = 0

        # find out if player is touching a block that slows down movement
        cur_y_acceleration = Y_ACCELERATION
        cur_player_speed_x = player.player_speed
        cur_y_acceleration, cur_player_speed_x, cur_player_speed_y, jump_is_possible = player.get_player_physics(Y_ACCELERATION)
        if cur_player_speed_y > 0: water_movement = True
        else: water_movement = False
        
        # get clicks for switching inventory
        if pygame.mouse.get_pressed()[0]: # Get the state of left click
            tx, ty = pygame.mouse.get_pos()
            x, y = get_scaled_mouse_click(scale, tx, ty, offx, offy)
            if y > screen_height_px - INVENTORY_HEIGHT:
                # now send it to the part of inventory that checks what part was pressed
                new_index = inventory.select_click(x,y)
                if new_index is not None: inventory.set_cur_position(new_index)
        # if pygame.mouse.get_pressed()[2]: # check right click


        # input (held keys)
        keys = pygame.key.get_pressed()

        if not inventory.show_full_inventory: # right now if this is active, it stops the whole game

            if keys[pygame.K_RETURN]:
                return_key_state += 1
            else:
                return_key_state = 0

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

            # check for pointers
            if keys[pygame.K_LSHIFT]: build_mode = True
            else: build_mode = False

            if keys[pygame.K_LEFT]:
                dir_x, dir_y = -1, 0
            elif keys[pygame.K_RIGHT]:
                dir_x, dir_y = 1, 0
            elif keys[pygame.K_UP]:
                dir_x, dir_y = 0, -1
            elif keys[pygame.K_DOWN]:
                dir_x, dir_y = 0, 1
            else:
                dir_x, dir_y = 0, 0
                affected_x, affected_y = None, None


            # process return key data (alt inventory selection method)
            if return_key_state == 1:
                if keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]:
                    inventory.increment_cur_position(False)
                else:
                    inventory.increment_cur_position(True)


            # process selector data
            if dir_x != 0 or dir_y != 0:
                affected_x, affected_y = get_affected_block(player, grid, dir_x, dir_y, build_mode)
                if build_mode and affected_x != None:
                    affected_x += dir_x * -1
                    affected_y += dir_y * -1
                    if player.reject_block_placement(affected_x, affected_y):
                        affected_x, affected_y = None, None


                if affected_x is None: affected_block = None
                else: affected_block = grid.get(affected_x, affected_y)
            else:
                affected_block = None


            if affected_x == None:
                held_time = 0
            else:
                if block_selected == (affected_x, affected_y):
                    held_time += 1
                else:
                    held_time = 1
                    block_selected = (affected_x, affected_y)
            
            if build_mode and held_time > BUILD_HOLD_THRESHOLD:
                Block_Type = inventory.build_from_current()
                if Block_Type is not None: 
                    grid.set(affected_x, affected_y, Block_Type)

            else:
                # grid_spot = grid.get(affected_x, affected_y)
                if affected_block is not None and held_time > affected_block.ticks_to_mine:
                    if affected_block.can_move_to_inventory():
                        inventory.add_item(type(grid.get(affected_x, affected_y)))
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



        # drawing
        screen.fill(background_color)

        grid.draw(camera_x, cur_camera_y, INVENTORY_HEIGHT)

        player.draw(camera_x, cur_camera_y)

        if affected_x != None and not build_mode:
            if grid.get(affected_x, affected_y) != None:
                grid.get(affected_x, affected_y).draw(True, camera_x = camera_x, camera_y = cur_camera_y)

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

            if menu.load_world:
                grid, inventory, player, world_details = load_world(f"{directory}/{menu.world_name}", screen, window, screen_width_px, screen_height_px, INVENTORY_HEIGHT, BLOCK_WIDTH)
                camera_x = player.x + (player.x_size // 2) - (screen_width_px // 2)
                camera_y = player.y + (player.y_size // 2) - (screen_height_px // 2)
                cur_camera_y = camera_y
                game_is_loaded = True
            elif menu.generate_new_world:
                menu.world_names_list.insert(0, menu.world_name)
                grid, inventory, player, world_details = generate_world(screen, window, grid_width, grid_height, menu.world_name)
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


pygame.quit()