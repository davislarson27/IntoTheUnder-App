import pygame
from math import floor
import json

from grid import Grid
from player import Player
from blocks import *
from full_inventory import Inventory
from menu import Menu
from world_generation import *

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

def save_game(directory, player, inventory, grid):
    grid_dictionary = grid.to_dict()
    with open(f"{directory}/grid.json", "w") as grid_file:
        json.dump(grid_dictionary, grid_file, indent=3)

    player_dictionary = player.to_dict()
    with open(f"{directory}/player_attributes.json", "w") as player_attr_file:
        json.dump(player_dictionary, player_attr_file, indent=3)
    
    inventory_dict = inventory.to_dict()
    with open(f"{directory}/inventory.json", "w") as inventory_file:
        json.dump(inventory_dict,inventory_file, indent=3)

def load_world(directory, screen, width, height, INVENTORY_HEIGHT, BLOCK_WIDTH):
    with open(f"{directory}/grid.json", "r") as grid_file:
        grid_dict = json.load(grid_file)
        grid = Grid.fill_from_dict(grid_dict, screen, BLOCK_WIDTH)

    with open(f"{directory}/inventory.json", "r") as inventory_file:
        inventory_dict = json.load(inventory_file)
        inventory = Inventory.fill_from_dict(inventory_dict, screen, height, width, INVENTORY_HEIGHT, HEALTH_BAR_HEIGHT)

    with open(f"{directory}/player_attributes.json", "r") as player_attr_file:
        player_attr_dict = json.load(player_attr_file)
        player_attr_dict["screen"] = screen
        player_attr_dict["grid"] = grid
        player_attr_dict["inventory_bar_height"] = INVENTORY_HEIGHT
        player_attr_dict["health_bar_height"] = HEALTH_BAR_HEIGHT
        player = Player(**player_attr_dict)

    return grid, inventory, player

def generate_world(screen, grid_width, grid_depth):
    # initialize grid
    grid = Grid(grid_width, grid_depth, BLOCK_WIDTH, screen) #sets width at 200 blocks

    # generate world terrain
    generate_world_blocks(grid, grid_width, grid_depth)

    # initialize inventory
    inventory = Inventory(screen, screen_height_px, screen_width_px, INVENTORY_HEIGHT, HEALTH_BAR_HEIGHT)

    # initialize player in grid
    player = Player(grid, screen, ((grid_width * BLOCK_WIDTH) // 2), 0, BLOCK_WIDTH, x_size=23, y_size = 23, inventory_bar_height=INVENTORY_HEIGHT, health_bar_height = HEALTH_BAR_HEIGHT)

    return grid, inventory, player


# implementation details
BLOCK_WIDTH = 25
INVENTORY_HEIGHT = 120
HEALTH_BAR_HEIGHT = 20 # included in INVENTORY_HEIGHT
# cur_seed = 12
# random.seed(cur_seed)


# initalize pygame
pygame.init()
pygame.font.init()


# create the screen
screen_width_px, screen_height_px = 1000, 620
screen = pygame.display.set_mode((screen_width_px, screen_height_px))
pygame.display.set_caption("Zombie Archeology")

true_height = screen_height_px - INVENTORY_HEIGHT
MOVEMENT_ALTITUDE_PX = (true_height * 13) // 16

# set grid size
grid_width = 5000
# grid_depth = (screen_height_px - INVENTORY_HEIGHT)//BLOCK_WIDTH + 10
grid_height = 100


# clock features
clock = pygame.time.Clock()
TICKS = 60

directory = "zombie_archeology1.2/game_files/my_first_world"

# set gravity variables
Y_ACCELERATION = 0.3
WATER_UPWARD_ACCEL = -0.05
JUMP_VELOCITY = -12


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
menu = Menu(screen, screen_width_px, screen_height_px, BLOCK_WIDTH)

while running and menu.menu_running:
    # event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            if game_is_loaded: save_game(directory, player, inventory, grid)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                if game_is_loaded: save_game(directory, player, inventory, grid)
                game_is_loaded = False
                menu = Menu(screen, screen_width_px, screen_height_px, BLOCK_WIDTH) # generates new menu
            if event.key == pygame.K_e:
                if game_is_loaded:
                    if inventory.show_full_inventory:
                        inventory.clear_selected_slot_full_inventory()
                        inventory.show_full_inventory = False
                    else:
                        inventory.show_full_inventory = True
        if game_is_loaded and inventory.show_full_inventory and event.type == pygame.MOUSEBUTTONUP and event.button == 1: # only processes if inventory is on
            inventory_click_x, inventory_click_y = event.pos
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
            x, y = pygame.mouse.get_pos()
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
            else:
                dy = player.y_vel


            # check if motion is legal
            if water_movement: dy *= 0.4
            collided = player.is_move_ok_y(dy)

            print(f"collided: {collided}, vel = {player.y_vel}, dy = {dy}")

            if collided and dy > 0 and abs(player.y_vel) > player.take_damage_threshold_velocity:
                damage = player.loss_per_velocity * (abs(player.y_vel) - player.take_damage_threshold_velocity)
                if player.health_bar.health - damage > 0: player.health_bar.health -= player.loss_per_velocity * (abs(player.y_vel) - player.take_damage_threshold_velocity )
                else: player.health_bar.health = 0
            
            print(f"health: {player.health_bar.health}")

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
                if player.y_vel + cur_y_acceleration < BLOCK_WIDTH:
                    player.y_vel += cur_y_acceleration
                player.ticks_falling += 1


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
        screen.fill((30,30,30))

        grid.draw(camera_x, cur_camera_y, INVENTORY_HEIGHT)

        player.draw(camera_x, cur_camera_y)

        if affected_x != None and not build_mode:
            if grid.get(affected_x, affected_y) != None:
                grid.get(affected_x, affected_y).draw(True, camera_x = camera_x, camera_y = cur_camera_y)

        inventory.draw()


    # run menu
    else: #this is for the menu screens
        menu.check_click(pygame.mouse)
        menu.move_background()
        menu.draw(pygame.mouse)

        if menu.run_game: # check for if it's time to move on and generate world before launch
            if menu.load_world:
                grid, inventory, player = load_world(directory, screen, screen_width_px, screen_height_px, INVENTORY_HEIGHT, BLOCK_WIDTH)
                camera_x = player.x + (player.x_size // 2) - (screen_width_px // 2)
                camera_y = player.y + (player.y_size // 2) - (screen_height_px // 2)
                cur_camera_y = camera_y
                game_is_loaded = True
            elif menu.generate_new_world:
                grid, inventory, player = generate_world(screen, grid_width, grid_height)
                camera_x = player.x + (player.x_size // 2) - (screen_width_px // 2)
                camera_y = player.y + (player.y_size // 2) - (screen_height_px // 2)
                cur_camera_y = camera_y
                game_is_loaded = True

    # update screen
    pygame.display.flip()


    # update clock
    clock.tick(TICKS)


pygame.quit()