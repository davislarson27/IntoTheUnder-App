import pygame
from math import floor, ceil
import shutil
from pathlib import Path
import json
import random

from world.world_creation.generate_world import *
from components.text_box import Text_Box
from play.play import Play
from components.blit_letterboxed import blit_letterboxed
from components.game_file_reading import save_game
from world.world_creation.world_generation_settings import World_Generation_Settings
from play.player import Player
from play.inventory.inventory import Inventory
from components.world_details import World_Details
from components.crash_menu import Crash_Menu

"""
explanation:

the menu works by using a self.blocks_width by self.blocks_height grid. 
boxes are generated during initialization
the main game loops calls the menu by calling menu.draw_function
self.draw_function holds a class method that actually draws the screen and is what click selection is based on
the subclass does the drawing
self.execute_clicked() checks self.draw_function to see what is on the screen
it then checks the mouse coordinates on click and compares them against the expected hit boxes and executes a function

"""


class Menu:
    def __init__(self, screen, window, images, width_px, height_px, BLOCK_WIDTH, world_names_list, game_files_directory, world_generation_settings):
        # draw_function_call
        self.draw_function = self.draw_main

        self.return_to = None

        # most attributes
        self.screen = screen
        self.window = window
        self.images = images
        self.width = width_px
        self.height = height_px
        self.block_width = BLOCK_WIDTH
        self.run_game = False
        self.button_font = pygame.font.Font(None, 25)  # None = default font
        self.small_button_font = pygame.font.Font(None, 20)
        self.loading_world_screen_font = pygame.font.Font(None, 30)
        self.title_font = pygame.font.Font(None, 65)
        self.small_title_font = pygame.font.Font(None, 50)
        self.subscript_font = pygame.font.Font(None, 16)
        self.camera_x = 0
        self.background_move_speed = 0.2
        self.menu_running = True
        self.button_color = (140, 140, 140)
        self.button_select_color = (165, 165, 165)
        self.game_files_directory = game_files_directory
        self.world_generation_settings = world_generation_settings

        self.string_end_if_corrupted = " (CORRUPTED)" # 12 chars

        self.announce_message = None
        self.prev_draw_func = None

        self.world_names_list = world_names_list
        self.WORLDS_PER_LOAD_SCREEN = 3
        self.load_screen_factor = 0
        self.world_name = None
        self.special_world_reference_index = None
        
        # world options
        self.load_world = False
        self.generate_new_world = False
        self.world_name_length_limit = 50

        # click variables
        self.is_clicked = False
        self.position_on_click = None

        # menu works under 28x28 grid where it chooses which get filled - these are the dementions for the "blocks"
        self.blocks_width = 28
        self.blocks_height = 28
        self.menu_block_width = self.width // self.blocks_width
        self.menu_block_height = self.height // self.blocks_height

        # loading and saving world screen (gets pre initalized)
        self.loading_world_screen_background_color = (30, 30, 30)
        self.saving_world_title_surf = self.loading_world_screen_font.render("Saving World...", True, (255, 255, 255))
        loading_world_screen_column_width = 16
        loading_world_margin_x = (self.blocks_width - loading_world_screen_column_width) // 2
        self.loading_world_title_rect = pygame.Rect(self.menu_block_width * loading_world_margin_x, self.menu_block_height * 12, self.menu_block_width * loading_world_screen_column_width, self.menu_block_height * 2)
        self.saving_world_screen_text_rect = self.saving_world_title_surf.get_rect(center=self.loading_world_title_rect.center)

        # menu titles
        title_column_width = 16
        title_column_margin_x = (self.blocks_width - title_column_width)//2
        self.title_space = pygame.Rect(self.menu_block_width * title_column_margin_x, self.menu_block_height * 5, self.menu_block_width * title_column_width, self.menu_block_height * 4)
        self.small_title_space = pygame.Rect(self.menu_block_width * title_column_margin_x, self.menu_block_height * 5, self.menu_block_width * title_column_width, self.menu_block_height * 4)
        self.main_text_surf = self.title_font.render("Into the Under", True, (255, 255, 255))

        # text box details
        self.padding = 12
        self.new_world_name_text_box = Text_Box()

        # buttons on the menu
        self.button0_dimentions = pygame.Rect(floor(self.menu_block_width * 0.5), self.menu_block_height * 1, floor(self.menu_block_width * 2.5), floor(self.menu_block_height * 1.75))
        
        center_column_width = 12
        center_column_margin_x = (self.blocks_width - center_column_width)//2
        self.button1_dimentions = pygame.Rect(
            self.menu_block_width * center_column_margin_x,
            self.menu_block_height * 10,
            self.menu_block_width * center_column_width,
            self.menu_block_height * 2
        )
        self.button2_dimentions = pygame.Rect(
            self.menu_block_width * center_column_margin_x,
            self.menu_block_height * 13,
            self.menu_block_width * center_column_width,
            self.menu_block_height * 2
        )
        self.button3_dimentions = pygame.Rect(
            self.menu_block_width * center_column_margin_x,
            self.menu_block_height * 16,
            self.menu_block_width * center_column_width,
            self.menu_block_height * 2
        )
        self.button4_dimentions = pygame.Rect(
            self.menu_block_width * center_column_margin_x,
            self.menu_block_height * 19,
            self.menu_block_width * center_column_width,
            self.menu_block_height * 2
        )

        # button 4 has split right-left options
        RL_width = 5.5
        self.button4L_dimentions = pygame.Rect(
            self.menu_block_width * center_column_margin_x,
            self.menu_block_height * 19,
            floor(self.menu_block_width * RL_width),
            self.menu_block_height * 2
        )
        self.button4R_dimentions = pygame.Rect(
            floor(self.menu_block_width * RL_width) + (self.menu_block_width * (center_column_margin_x + 1)),
            self.menu_block_height * 19,
            floor(self.menu_block_width * RL_width),
            self.menu_block_height * 2
        )

        longL_column_width = 9.75
        self.button1_longL_dimentions = pygame.Rect(
            self.menu_block_width * center_column_margin_x,
            self.menu_block_height * 10,
            self.menu_block_width * longL_column_width,
            self.menu_block_height * 2
        )
        self.button2_longL_dimentions = pygame.Rect(
            self.menu_block_width * center_column_margin_x,
            self.menu_block_height * 13,
            self.menu_block_width * longL_column_width,
            self.menu_block_height * 2
        )
        self.button3_longL_dimentions = pygame.Rect(
            self.menu_block_width * center_column_margin_x,
            self.menu_block_height * 16,
            self.menu_block_width * longL_column_width,
            self.menu_block_height * 2
        )

        self.button1_shortR_dimentions = pygame.Rect(
            floor(self.menu_block_width * longL_column_width) + (self.menu_block_width * (center_column_margin_x + 0.25)),
            self.menu_block_height * 10,
            self.menu_block_width * 2,
            self.menu_block_height * 2
        )
        self.button2_shortR_dimentions = pygame.Rect(
            floor(self.menu_block_width * longL_column_width) + (self.menu_block_width * (center_column_margin_x + 0.25)),
            self.menu_block_height * 13,
            self.menu_block_width * 2,
            self.menu_block_height * 2
        )
        self.button3_shortR_dimentions = pygame.Rect(
            floor(self.menu_block_width * longL_column_width) + (self.menu_block_width * (center_column_margin_x + 0.25)),
            self.menu_block_height * 16,
            self.menu_block_width * 2,
            self.menu_block_height * 2
        )

        # subtext boxes
        self.button1_subtext_dimentions = pygame.Rect(
            self.menu_block_width * center_column_margin_x,
            (self.menu_block_height * 9) + 3,
            self.menu_block_width * center_column_width,
            self.menu_block_height
        )


        # ------------------------------- world creation options ------------------------------- #

        self.world_size_options = ["Small", "Medium", "Large"]
        self.default_selected_world_size = 1 # default to Medium
        self.selected_world_size = self.default_selected_world_size
        self.size_to_width_dict = {
            "Small": 1000,
            "Medium": 5000,
            "Large": 15000
        }
        self.world_seed_text_box = Text_Box()
        self.seed_length = 100000000000000000
        self.custom_seed = self.getRandomSeed()

        # options screen - seed input and size selector
        self.seed_label_dimentions = pygame.Rect(
            self.menu_block_width * center_column_margin_x,
            self.menu_block_height * 9,
            self.menu_block_width * center_column_width,
            self.menu_block_height
        )
        self.seed_box_dimentions = pygame.Rect(
            self.menu_block_width * center_column_margin_x,
            self.menu_block_height * 10,
            self.menu_block_width * center_column_width,
            self.menu_block_height * 2
        )

        size_button_width = center_column_width / 3  
        size_button_gap = 0
        self.size_button_dimentions = []
        for i in range(3):
            x_offset = center_column_margin_x + (i * (size_button_width + size_button_gap))
            self.size_button_dimentions.append(pygame.Rect(
                floor(self.menu_block_width * x_offset),
                self.menu_block_height * 14,
                floor(self.menu_block_width * size_button_width),
                self.menu_block_height * 2
            ))

        self.size_label_dimentions = pygame.Rect(
            self.menu_block_width * center_column_margin_x,
            self.menu_block_height * 13,
            self.menu_block_width * center_column_width,
            self.menu_block_height
        )


        # ----------------------------------------- generate menu background world ----------------------------------------- #

        load_screen_block_width = floor(BLOCK_WIDTH * 1.15) #slightly enlarge the blocks
        self.width_blocks = (width_px // load_screen_block_width) * 3
        self.height_blocks = (height_px // load_screen_block_width) + 4
        self.background_world_width_px = floor(self.width_blocks * load_screen_block_width)

        menu_world_settings = World_Generation_Settings(
            world_generation_settings.version, 
            0, 
            0, 
            self.width_blocks, 
            self.height_blocks, 
            load_screen_block_width
        )

        menu_world_seed = self.getRandomSeed()
        menu_world_settings.reset_ground_level(13)
        grid_superstructure = Grid_Superstructure(screen, menu_world_settings, world_seed=menu_world_seed)
        grid_superstructure.generate_world()
        self.background_grid, self.bg_background_grid = grid_superstructure.get_grids()

    def getRandomSeed(self):
        return str(int(random.random() * self.seed_length))

    def get_max_load_screens(self):
        return ceil(len(self.world_names_list) / self.WORLDS_PER_LOAD_SCREEN) 

    def execute_load_world(self, button_offset = 0):
        """
        loads world and resets menu to main
        button offset specifies which button got pressed (0 is the first option, 1 is the second, etc)
        """
        self.draw_function = self.draw_main
        self.load_world = True
        self.run_game = True
        self.world_name = self.world_names_list[(self.WORLDS_PER_LOAD_SCREEN * self.load_screen_factor) + button_offset]

    def execute_delete_world_confirmation(self, button_offset = 0):
        """
        runs process for when the delete button is pressed on the load page
        does not actually delete the world files
        """
        self.draw_function = self.draw_confirm_delete_screen
        self.world_name = self.world_names_list[(self.WORLDS_PER_LOAD_SCREEN * self.load_screen_factor) + button_offset]
        self.special_world_reference_index = (self.WORLDS_PER_LOAD_SCREEN * self.load_screen_factor) + button_offset

    def delete_world_files(self, world_file_name):
        # step 1: strip file name of " (CORRUPTED)" if applicable
        # World (CORRUPTED)
        if len(world_file_name) > len(self.string_end_if_corrupted) and world_file_name[len(world_file_name) - len(self.string_end_if_corrupted) : ] == self.string_end_if_corrupted[:]:
            cleaned_world_file_name = world_file_name[0 : len(world_file_name) - len(self.string_end_if_corrupted)]
        else:
            cleaned_world_file_name = world_file_name
        
        delete_file_dir = Path(self.game_files_directory) / cleaned_world_file_name
        if (delete_file_dir).is_dir():
            shutil.rmtree(delete_file_dir)
            self.world_names_list.remove(world_file_name)
            # print(delete_file_dir)
            return True
        return False

    def execute_create_new_world(self):
        self.generate_new_world = True
        self.run_game = True

    def create_world_name(self): # this function will eventually be replaced by user input -> but for now it is auto generated
        add_on_value = len(self.world_names_list) + 1
        new_world_name = f"My World {add_on_value}"

        while new_world_name in self.world_names_list or f"{new_world_name}{self.string_end_if_corrupted}" in self.world_names_list:
            add_on_value += 1
            new_world_name = f"My World {add_on_value}"
        
        return new_world_name

    def create_announce_screen(self, message):
        self.announce_message = message
        self.prev_draw_func = self.draw_create_world_menu
        self.draw_function = self.draw_announce_and_return_screen

    def return_to_main(self):
        self.draw_function = self.draw_main
        self.load_world = False
        self.run_game = False
        self.menu_running = True
        self.generate_new_world = False
        self.world_name = None

    def move_background(self):
        if self.camera_x + self.width < self.background_world_width_px: self.camera_x += self.background_move_speed

    def draw_main(self, mx, my, input):
        # draw game title
        text_rect = self.main_text_surf.get_rect(center=self.title_space.center)
        self.screen.blit(self.main_text_surf, text_rect)

        # create "load world" button
        if self.button1_dimentions.collidepoint((mx, my)): cur_button_color = self.button_select_color
        else: cur_button_color = self.button_color
        pygame.draw.rect( # menu button
            self.screen,
            cur_button_color,
            self.button1_dimentions
        )
        text_surf = self.button_font.render("Load World", True, (255, 255, 255))
        text_rect = text_surf.get_rect(center=self.button1_dimentions.center)
        self.screen.blit(text_surf, text_rect)

        # create "create new world" button
        if self.button2_dimentions.collidepoint((mx, my)): cur_button_color = self.button_select_color
        else: cur_button_color = self.button_color
        pygame.draw.rect( # menu button
            self.screen,
            cur_button_color,
            self.button2_dimentions
        )
        text_surf = self.button_font.render("Create New World", True, (255, 255, 255))
        text_rect = text_surf.get_rect(center=self.button2_dimentions.center)
        self.screen.blit(text_surf, text_rect)

        # create "exit" button
        if self.button3_dimentions.collidepoint((mx, my)): cur_button_color = self.button_select_color
        else: cur_button_color = self.button_color
        pygame.draw.rect( # menu button
            self.screen,
            cur_button_color,
            self.button3_dimentions
        )
        text_surf = self.button_font.render("Exit", True, (255, 255, 255))
        text_rect = text_surf.get_rect(center=self.button3_dimentions.center)
        self.screen.blit(text_surf, text_rect)

    def draw_load_menu(self, mx, my, input):

        if len(self.world_names_list) > 0: # checks to make sure there are actual worlds that can be loaded
            start_world_position = self.load_screen_factor * self.WORLDS_PER_LOAD_SCREEN

            # draw game title
            load_screen_text_surf = self.small_title_font.render(f"Select World ({self.load_screen_factor+1}/{self.get_max_load_screens()})", True, (255, 255, 255))

            text_rect = load_screen_text_surf.get_rect(center=self.title_space.center)
            self.screen.blit(load_screen_text_surf, text_rect)

            # draw back button
            if self.button0_dimentions.collidepoint((mx, my)): cur_button_color = self.button_select_color
            else: cur_button_color = self.button_color
            pygame.draw.rect( # menu button
                self.screen,
                cur_button_color,
                self.button0_dimentions
            )
            text_surf = self.small_button_font.render("Back", True, (255, 255, 255))
            text_rect = text_surf.get_rect(center=self.button0_dimentions.center)
            self.screen.blit(text_surf, text_rect)


            # create first option button
            if self.WORLDS_PER_LOAD_SCREEN * self.load_screen_factor < len(self.world_names_list):
                if self.button1_longL_dimentions.collidepoint((mx, my)): cur_button_color = self.button_select_color
                else: cur_button_color = self.button_color
                pygame.draw.rect( # menu button
                    self.screen,
                    cur_button_color,
                    self.button1_longL_dimentions
                )
                text_surf = self.button_font.render(self.world_names_list[start_world_position], True, (255, 255, 255))
                text_rect = text_surf.get_rect(center=self.button1_longL_dimentions.center)
                self.screen.blit(text_surf, text_rect)

                # delete button
                if self.button1_shortR_dimentions.collidepoint((mx, my)): cur_button_color = self.button_select_color
                else: cur_button_color = self.button_color
                pygame.draw.rect( # menu button
                    self.screen,
                    cur_button_color,
                    self.button1_shortR_dimentions
                )
                icon_rect = self.images.trash.get_rect(center=self.button1_shortR_dimentions.center)
                self.screen.blit(self.images.trash, icon_rect)



            # create second option button
            if (self.WORLDS_PER_LOAD_SCREEN * self.load_screen_factor) + 1 < len(self.world_names_list):
                if self.button2_longL_dimentions.collidepoint((mx, my)): cur_button_color = self.button_select_color
                else: cur_button_color = self.button_color
                pygame.draw.rect( # menu button
                    self.screen,
                    cur_button_color,
                    self.button2_longL_dimentions
                )
                text_surf = self.button_font.render(self.world_names_list[start_world_position + 1], True, (255, 255, 255))
                text_rect = text_surf.get_rect(center=self.button2_longL_dimentions.center)
                self.screen.blit(text_surf, text_rect)

                
                # draw delete
                if self.button2_shortR_dimentions.collidepoint((mx, my)): cur_button_color = self.button_select_color
                else: cur_button_color = self.button_color
                pygame.draw.rect( # menu button
                    self.screen,
                    cur_button_color,
                    self.button2_shortR_dimentions
                )
                icon_rect = self.images.trash.get_rect(center=self.button2_shortR_dimentions.center)
                self.screen.blit(self.images.trash, icon_rect)

            # create third option button
            if (self.WORLDS_PER_LOAD_SCREEN * self.load_screen_factor) + 2 < len(self.world_names_list):
                if self.button3_longL_dimentions.collidepoint((mx, my)): cur_button_color = self.button_select_color
                else: cur_button_color = self.button_color
                pygame.draw.rect( # menu button
                    self.screen,
                    cur_button_color,
                    self.button3_longL_dimentions
                )
                text_surf = self.button_font.render(self.world_names_list[start_world_position + 2], True, (255, 255, 255))
                text_rect = text_surf.get_rect(center=self.button3_longL_dimentions.center)
                self.screen.blit(text_surf, text_rect)
                
                # delete button
                if self.button3_shortR_dimentions.collidepoint((mx, my)): cur_button_color = self.button_select_color
                else: cur_button_color = self.button_color
                pygame.draw.rect( # menu button
                    self.screen,
                    cur_button_color,
                    self.button3_shortR_dimentions
                )
                icon_rect = self.images.trash.get_rect(center=self.button3_shortR_dimentions.center)
                self.screen.blit(self.images.trash, icon_rect)

            # create "Prev" option button
            if self.button4L_dimentions.collidepoint((mx, my)): cur_button_color = self.button_select_color
            else: cur_button_color = self.button_color
            pygame.draw.rect( # menu button
                self.screen,
                cur_button_color,
                self.button4L_dimentions
            )
            text_surf = self.button_font.render("Prev", True, (255, 255, 255))
            text_rect = text_surf.get_rect(center=self.button4L_dimentions.center)
            self.screen.blit(text_surf, text_rect)

            # create "Next" option button
            if self.button4R_dimentions.collidepoint((mx, my)): cur_button_color = self.button_select_color
            else: cur_button_color = self.button_color
            pygame.draw.rect( # menu button
                self.screen,
                cur_button_color,
                self.button4R_dimentions
            )
            text_surf = self.button_font.render("Next", True, (255, 255, 255))
            text_rect = text_surf.get_rect(center=self.button4R_dimentions.center)
            self.screen.blit(text_surf, text_rect)

        else: # render return button and error message

            text_surf = self.button_font.render("No World Files Found", True, (255, 255, 255))
            text_rect = text_surf.get_rect(center=self.button1_dimentions.center)
            self.screen.blit(text_surf, text_rect)

            # create return button
            if self.button2_dimentions.collidepoint((mx, my)): cur_button_color = self.button_select_color
            else: cur_button_color = self.button_color

            pygame.draw.rect( # return button button
                self.screen,
                cur_button_color,
                self.button2_dimentions
            )
            text_surf = self.button_font.render("Main Menu", True, (255, 255, 255))
            text_rect = text_surf.get_rect(center=self.button2_dimentions.center)
            self.screen.blit(text_surf, text_rect)

    def draw_confirm_delete_screen(self, mx, my, input): # eventually this will allow deleting worlds in the game UI
                
        # draw game title
        load_screen_text_surf = self.small_title_font.render(f"Are You Sure You Want to Delete \"{self.world_name}\"", True, (255, 255, 255))
        text_rect = load_screen_text_surf.get_rect(center=self.title_space.center)
        self.screen.blit(load_screen_text_surf, text_rect)

        # create return button
        if self.button1_dimentions.collidepoint((mx, my)): cur_button_color = self.button_select_color
        else: cur_button_color = self.button_color

        pygame.draw.rect( # return button button
            self.screen,
            cur_button_color,
            self.button1_dimentions
        )
        text_surf = self.button_font.render("Delete World", True, (255, 255, 255))
        text_rect = text_surf.get_rect(center=self.button1_dimentions.center)
        self.screen.blit(text_surf, text_rect)


        # create return button
        if self.button2_dimentions.collidepoint((mx, my)): cur_button_color = self.button_select_color
        else: cur_button_color = self.button_color

        pygame.draw.rect( # return button button
            self.screen,
            cur_button_color,
            self.button2_dimentions
        )
        text_surf = self.button_font.render("Cancel", True, (255, 255, 255))
        text_rect = text_surf.get_rect(center=self.button2_dimentions.center)
        self.screen.blit(text_surf, text_rect)

    def draw_loading_world_screen(self, percent_complete=0, message='Loading'):
        self.screen.fill(self.loading_world_screen_background_color)

        outline_color = (105, 110, 112)
        bar_color = (90, 140, 200)

        # --- BAR ---
        outline_width = 2
        loading_bar_outline_dimentions = pygame.Rect(
            self.button2_dimentions.left,
            self.button2_dimentions.top,
            self.button2_dimentions.width,
            self.button2_dimentions.height - 10
        )
        loading_bar_dimentions = pygame.Rect(
            loading_bar_outline_dimentions.left + outline_width,
            loading_bar_outline_dimentions.top + outline_width,
            loading_bar_outline_dimentions.width - (2 * outline_width),
            loading_bar_outline_dimentions.height - (2 * outline_width)
        )

        pygame.draw.rect(
            self.screen,
            outline_color,
            loading_bar_outline_dimentions,
            width=outline_width
        )

        percent_bar_fill = pygame.Rect(
            loading_bar_dimentions.left,
            loading_bar_dimentions.top,
            (loading_bar_dimentions.width * percent_complete) // 100,
            loading_bar_dimentions.height
        )
        pygame.draw.rect(self.screen, bar_color, percent_bar_fill)

        # --- TEXT ---
        surf = self.loading_world_screen_font.render(f'{message}...', True, (255,255,255))

        rect = surf.get_rect(
            center=(
                loading_bar_dimentions.centerx,
                loading_bar_dimentions.top - 38   # ← easy control
            )
        )

        self.screen.blit(surf, rect)

        blit_letterboxed(self.screen, self.window, self.loading_world_screen_background_color)
        pygame.display.flip()
        pygame.event.pump()

    def draw_announce_and_return_screen(self, mx, my, input):
            text_surf = self.button_font.render(self.announce_message, True, (255, 255, 255))
            text_rect = text_surf.get_rect(center=self.button1_dimentions.center)
            self.screen.blit(text_surf, text_rect)

            # create return button
            if self.button2_dimentions.collidepoint((mx, my)): cur_button_color = self.button_select_color
            else: cur_button_color = self.button_color

            pygame.draw.rect( # return button button
                self.screen,
                cur_button_color,
                self.button2_dimentions
            )
            text_surf = self.button_font.render("Return", True, (255, 255, 255))
            text_rect = text_surf.get_rect(center=self.button2_dimentions.center)
            self.screen.blit(text_surf, text_rect)

    def draw_create_world_menu(self, mx, my, input):
        # handle text input
        self.new_world_name_text_box.take_input(input, self.world_name_length_limit)
        self.world_name = self.new_world_name_text_box.get_cur_string()

        # draw game title
        load_screen_text_surf = self.small_title_font.render("Create New World", True, (255, 255, 255))

        text_rect = load_screen_text_surf.get_rect(center=self.title_space.center)
        self.screen.blit(load_screen_text_surf, text_rect)

        # draw back button
        if self.button0_dimentions.collidepoint((mx, my)): cur_button_color = self.button_select_color
        else: cur_button_color = self.button_color
        pygame.draw.rect( # menu button
            self.screen,
            cur_button_color,
            self.button0_dimentions
        )
        text_surf = self.small_button_font.render("Back", True, (255, 255, 255))
        text_rect = text_surf.get_rect(center=self.button0_dimentions.center)
        self.screen.blit(text_surf, text_rect)


        # draw world name text box
        if self.new_world_name_text_box.is_typing:
            cur_button_color = self.new_world_name_text_box.text_box_color_active
        else:
            cur_button_color = self.new_world_name_text_box.text_box_color
        if self.button1_dimentions.collidepoint((mx, my)):
            outline_color = self.new_world_name_text_box.text_box_outline_color_active
            outline_width = 3
        else:
            outline_color = self.new_world_name_text_box.text_box_outline_color
            outline_width = 1

        pygame.draw.rect( # world name text box
            self.screen,
            cur_button_color,
            self.button1_dimentions
        )
        pygame.draw.rect( # outline
            self.screen,
            outline_color,
            self.button1_dimentions,
            width=outline_width
        )

        display_string = self.new_world_name_text_box.get_cur_string() + self.new_world_name_text_box.get_text_cursor()
        text_surf = self.button_font.render(display_string, True, self.new_world_name_text_box.text_box_text_color)
        text_rect = text_surf.get_rect(
            midleft=(
                self.button1_dimentions.left + self.padding,
                self.button1_dimentions.centery
            )
        )
        self.screen.blit(text_surf, text_rect)
        
        
        # draw text box subtext
        text_surf = self.subscript_font.render("world name", True, (160, 165, 170))
        text_rect = text_surf.get_rect(
            midleft=(
                self.button1_subtext_dimentions.left,
                self.button1_subtext_dimentions.centery
            )
        )
        self.screen.blit(text_surf, text_rect)


        # draw options button
        if self.button2_dimentions.collidepoint((mx, my)): cur_button_color = self.button_select_color
        else: cur_button_color = self.button_color
        pygame.draw.rect(
            self.screen,
            cur_button_color,
            self.button2_dimentions
        )
        text_surf = self.button_font.render("Options", True, (255, 255, 255))
        text_rect = text_surf.get_rect(center=self.button2_dimentions.center)
        self.screen.blit(text_surf, text_rect)

        # draw create new world button
        if self.button3_dimentions.collidepoint((mx, my)): cur_button_color = self.button_select_color
        else: cur_button_color = self.button_color
        pygame.draw.rect( # menu button
            self.screen,
            cur_button_color,
            self.button3_dimentions
        )
        text_surf = self.button_font.render("Create New World", True, (255, 255, 255))
        text_rect = text_surf.get_rect(center=self.button3_dimentions.center)
        self.screen.blit(text_surf, text_rect)

    def draw_world_options_menu(self, mx, my, input):
        # handle seed text input
        self.world_seed_text_box.take_input(input, 20)
        self.custom_seed = self.world_seed_text_box.get_cur_string()

        # --- card background ---
        card_margin_x = self.menu_block_width * 6
        card_top = self.menu_block_height * 5
        card_bottom = self.menu_block_height * 22
        card_rect = pygame.Rect(card_margin_x, card_top, self.width - (card_margin_x * 2), card_bottom - card_top)
        pygame.draw.rect(self.screen, (50, 50, 50), card_rect, border_radius=8)
        pygame.draw.rect(self.screen, (80, 80, 80), card_rect, width=1, border_radius=8)

        card_padding = self.menu_block_width * 1

        # --- small subtitle at top ---
        title_surf = self.button_font.render("World Options", True, (180, 180, 180))
        title_rect = title_surf.get_rect(center=(card_rect.centerx, card_top - self.menu_block_height))
        text_rect = title_surf.get_rect(center=title_rect.center)
        self.screen.blit(title_surf, text_rect)

        # --- seed section ---
        seed_section_top = card_top + self.menu_block_height * 1

        label_surf = self.button_font.render("World Seed", True, (220, 220, 220))
        self.screen.blit(label_surf, label_surf.get_rect(midleft=(
            card_rect.left + card_padding,
            seed_section_top + self.menu_block_height // 2
        )))

        self.seed_box_dimentions = pygame.Rect(
            card_rect.left + card_padding,
            seed_section_top + self.menu_block_height * 1,
            card_rect.width - (card_padding * 2),
            self.menu_block_height * 2
        )

        if self.world_seed_text_box.is_typing:
            fill_color = self.world_seed_text_box.text_box_color_active
            outline_color = self.world_seed_text_box.text_box_outline_color_active
            outline_width = 3
        else:
            fill_color = self.world_seed_text_box.text_box_color
            outline_color = self.world_seed_text_box.text_box_outline_color_active if self.seed_box_dimentions.collidepoint((mx, my)) else self.world_seed_text_box.text_box_outline_color
            outline_width = 3 if self.seed_box_dimentions.collidepoint((mx, my)) else 1

        pygame.draw.rect(self.screen, fill_color, self.seed_box_dimentions, border_radius=4)
        pygame.draw.rect(self.screen, outline_color, self.seed_box_dimentions, width=outline_width, border_radius=4)

        display_string = self.world_seed_text_box.get_cur_string() + self.world_seed_text_box.get_text_cursor()
        text_surf = self.button_font.render(display_string, True, self.world_seed_text_box.text_box_text_color)
        self.screen.blit(text_surf, text_surf.get_rect(midleft=(
            self.seed_box_dimentions.left + self.padding,
            self.seed_box_dimentions.centery
        )))

        # --- size section ---
        size_section_top = seed_section_top + self.menu_block_height * 4

        label_surf = self.button_font.render("World Size", True, (220, 220, 220))
        self.screen.blit(label_surf, label_surf.get_rect(midleft=(
            card_rect.left + card_padding,
            size_section_top + self.menu_block_height // 2
        )))

        size_button_width = (card_rect.width - (card_padding * 2)) // 3
        size_button_top = size_section_top + self.menu_block_height * 1
        size_button_height = self.menu_block_height * 2

        selected_color = (90, 140, 200)
        unselected_color = self.button_color
        hover_color = self.button_select_color

        # rebuild size rects inline so they fit the card
        self.size_button_dimentions = []
        for i, label in enumerate(self.world_size_options):
            rect = pygame.Rect(
                card_rect.left + card_padding + (i * size_button_width),
                size_button_top,
                size_button_width,
                size_button_height
            )
            self.size_button_dimentions.append(rect)

            if i == self.selected_world_size:
                color = selected_color
            elif rect.collidepoint((mx, my)):
                color = hover_color
            else:
                color = unselected_color

            pygame.draw.rect(self.screen, color, rect)
            if i == self.selected_world_size:
                pygame.draw.rect(self.screen, (140, 190, 255), rect, width=2)

            text_surf = self.button_font.render(label, True, (255, 255, 255))
            self.screen.blit(text_surf, text_surf.get_rect(center=rect.center))

        # --- bottom buttons: Return (left) and Create World (right) ---
        btn_width = (card_rect.width - self.menu_block_width) // 2 - card_padding
        btn_height = self.menu_block_height * 2
        btn_top = card_bottom - self.menu_block_height * 1 - btn_height

        gap_below = card_bottom - (btn_top + btn_height)
        line_y = btn_top - gap_below
        pygame.draw.line(self.screen, (80, 80, 80), (card_rect.left + card_padding, line_y), (card_rect.right - card_padding, line_y), 1)

        self.options_return_btn = pygame.Rect(card_rect.left + card_padding, btn_top, btn_width, btn_height)
        self.options_create_btn = pygame.Rect(card_rect.right - btn_width - card_padding, btn_top, btn_width, btn_height)

        if self.options_return_btn.collidepoint((mx, my)): cur_button_color = self.button_select_color
        else: cur_button_color = self.button_color
        pygame.draw.rect(self.screen, cur_button_color, self.options_return_btn, border_radius=4)
        text_surf = self.button_font.render("Return", True, (255, 255, 255))
        self.screen.blit(text_surf, text_surf.get_rect(center=self.options_return_btn.center))

        if self.options_create_btn.collidepoint((mx, my)): cur_button_color = self.button_select_color
        else: cur_button_color = self.button_color
        pygame.draw.rect(self.screen, cur_button_color, self.options_create_btn, border_radius=4)
        text_surf = self.button_font.render("Create World", True, (255, 255, 255))
        self.screen.blit(text_surf, text_surf.get_rect(center=self.options_create_btn.center))

    def returnToLast(self):
        if self.return_to is None:
            self.return_to_main()
        else:
            self.draw_function = self.return_to
            self.return_to = None

    # main functions

    def draw(self, mx, my, input):
        # draw background before menus
        self.screen.fill((30,30,30))
        self.background_grid.draw(floor(self.camera_x), 0)

        self.draw_function(mx, my, input)
    
    def execute_clicked(self, position_on_release): # may need to add in self.

        # main menu
        if self.draw_function.__func__ is self.draw_main.__func__:
            if self.button1_dimentions.collidepoint(self.position_on_click) and self.button1_dimentions.collidepoint(position_on_release):
                self.draw_function = self.draw_load_menu
            elif self.button2_dimentions.collidepoint(self.position_on_click) and self.button2_dimentions.collidepoint(position_on_release):
                self.world_name = self.create_world_name()
                self.new_world_name_text_box.open_text_box(self.world_name)
                self.draw_function = self.draw_create_world_menu
            elif self.button3_dimentions.collidepoint(self.position_on_click) and self.button3_dimentions.collidepoint(position_on_release):
                pygame.event.post(pygame.event.Event(pygame.QUIT))
                
        # if load world menu is active
        elif self.draw_function.__func__ is self.draw_load_menu.__func__:
            if len(self.world_names_list) > 0:
                # check the return button
                if self.button0_dimentions.collidepoint(self.position_on_click) and self.button0_dimentions.collidepoint(position_on_release):
                    self.returnToLast()
                
                # now check the launch world buttons
                elif self.button1_longL_dimentions.collidepoint(self.position_on_click) and self.button1_longL_dimentions.collidepoint(position_on_release):
                    if self.WORLDS_PER_LOAD_SCREEN * self.load_screen_factor < len(self.world_names_list):
                        self.execute_load_world(0)
                elif self.button2_longL_dimentions.collidepoint(self.position_on_click) and self.button2_longL_dimentions.collidepoint(position_on_release):                    
                    if (self.WORLDS_PER_LOAD_SCREEN * self.load_screen_factor) + 1 < len(self.world_names_list):
                        self.execute_load_world(1)
                elif self.button3_longL_dimentions.collidepoint(self.position_on_click) and self.button3_longL_dimentions.collidepoint(position_on_release):                    
                    if (self.WORLDS_PER_LOAD_SCREEN * self.load_screen_factor) + 2 < len(self.world_names_list):
                        self.execute_load_world(2)
                
                # check the delete world buttons
                elif self.button1_shortR_dimentions.collidepoint(self.position_on_click) and self.button1_shortR_dimentions.collidepoint(position_on_release):
                    if self.WORLDS_PER_LOAD_SCREEN * self.load_screen_factor < len(self.world_names_list):
                        self.execute_delete_world_confirmation(0)
                elif self.button2_shortR_dimentions.collidepoint(self.position_on_click) and self.button2_shortR_dimentions.collidepoint(position_on_release):
                    if (self.WORLDS_PER_LOAD_SCREEN * self.load_screen_factor) + 1 < len(self.world_names_list):
                        self.execute_delete_world_confirmation(1)
                elif self.button3_shortR_dimentions.collidepoint(self.position_on_click) and self.button3_shortR_dimentions.collidepoint(position_on_release):
                    if (self.WORLDS_PER_LOAD_SCREEN * self.load_screen_factor) + 2 < len(self.world_names_list):
                        self.execute_delete_world_confirmation(2)

                # check the load menu navigation buttons
                elif self.button4L_dimentions.collidepoint(self.position_on_click) and self.button4L_dimentions.collidepoint(position_on_release):
                    # prev button
                    self.load_screen_factor -= 1
                    if self.load_screen_factor < 0:
                        self.load_screen_factor = self.get_max_load_screens() - 1
                elif self.button4R_dimentions.collidepoint(self.position_on_click) and self.button4R_dimentions.collidepoint(position_on_release):
                    # next button
                    self.load_screen_factor += 1
                    if self.load_screen_factor > self.get_max_load_screens() - 1:
                        self.load_screen_factor = 0
            
            else: # allows alt return button to work
                if self.button2_dimentions.collidepoint(self.position_on_click) and self.button2_dimentions.collidepoint(position_on_release):
                    self.draw_function = self.draw_main

        # confirm world deletion menu
        elif self.draw_function.__func__ is self.draw_confirm_delete_screen.__func__:
            # selected yes
            if self.button1_dimentions.collidepoint(self.position_on_click) and self.button1_dimentions.collidepoint(position_on_release):
                # self.announce_message = "successfully deleted f{}"  
                if self.delete_world_files(self.world_names_list[self.special_world_reference_index]):
                    self.announce_message = f"Successfully Deleted \"{self.world_name}\""
                else:
                    self.announce_message = f"Failed to Delete \"{self.world_name}\""
                self.draw_function = self.draw_announce_and_return_screen
                self.special_world_reference_index = None
                self.world_name = None
                self.load_screen_factor = 0 # ensures that when the user clicks back in it doesn't throw an index error
                self.prev_draw_func = self.draw_load_menu
            # selected no
            elif self.button2_dimentions.collidepoint(self.position_on_click) and self.button2_dimentions.collidepoint(position_on_release):
                self.draw_function = self.draw_load_menu
                self.special_world_reference_index = None
                self.world_name = None

        # print alert system and return to last
        elif self.draw_function.__func__ is self.draw_announce_and_return_screen.__func__:
            if self.button2_dimentions.collidepoint(self.position_on_click) and self.button2_dimentions.collidepoint(position_on_release):
                self.draw_function = self.prev_draw_func

        # create new world menu
        elif self.draw_function.__func__ is self.draw_create_world_menu.__func__:
            # check the return button
            if self.button0_dimentions.collidepoint(self.position_on_click) and self.button0_dimentions.collidepoint(position_on_release):
                self.returnToLast()
            elif self.button1_dimentions.collidepoint(self.position_on_click) and self.button1_dimentions.collidepoint(position_on_release):
                self.new_world_name_text_box.is_typing = True
            elif self.button2_dimentions.collidepoint(self.position_on_click) and self.button2_dimentions.collidepoint(position_on_release):
                self.world_seed_text_box.open_text_box(self.custom_seed)
                self.draw_function = self.draw_world_options_menu
                self.return_to = self.draw_create_world_menu
            elif self.button3_dimentions.collidepoint(self.position_on_click) and self.button3_dimentions.collidepoint(position_on_release):
                if self.world_name in self.world_names_list or f"{self.world_name}{self.string_end_if_corrupted}" in self.world_names_list:
                    self.create_announce_screen(f"World Name \"{self.world_name}\" is Already in Use")
                else:
                    self.execute_create_new_world()
            # now deactivate the text box if something else if clicked
            if not self.button1_dimentions.collidepoint(self.position_on_click) and not self.button1_dimentions.collidepoint(position_on_release):
                self.new_world_name_text_box.is_typing = False

        # draw the world options
        elif self.draw_function.__func__ is self.draw_world_options_menu.__func__:
            # back to create world screen
            if self.options_return_btn.collidepoint(self.position_on_click) and self.options_return_btn.collidepoint(position_on_release):
                self.world_seed_text_box.is_typing = False
                self.returnToLast()
            elif self.options_create_btn.collidepoint(self.position_on_click) and self.options_create_btn.collidepoint(position_on_release):
                if self.world_name in self.world_names_list or f"{self.world_name}{self.string_end_if_corrupted}" in self.world_names_list:
                    self.create_announce_screen(f"World Name \"{self.world_name}\" is Already in Use")
                else:
                    self.execute_create_new_world()

            # size selector buttons
            for i, rect in enumerate(self.size_button_dimentions):
                if rect.collidepoint(self.position_on_click) and rect.collidepoint(position_on_release):
                    self.selected_world_size = i

            # seed text box focus
            if self.seed_box_dimentions.collidepoint(self.position_on_click):
                self.world_seed_text_box.is_typing = True
            else:
                self.world_seed_text_box.is_typing = False

    def check_click(self, mouse, mx, my):
        if not self.is_clicked and mouse.get_pressed()[0]: # detect click
            self.is_clicked = True
            self.position_on_click = (mx, my)

        elif self.is_clicked and not mouse.get_pressed()[0]: # detect release
            self.execute_clicked((mx, my))
            self.is_clicked = False

    # helper functions
    def create_new_world(self):
        # initialize the loading screen
        # initialize grid and terrain
        self.world_generation_settings.reset_ground_level(50)
        grid_superstructure = Grid_Superstructure(self.screen, self.world_generation_settings)
        for GenerationText, percentComplete in grid_superstructure._generate_world():
            pass
        grid, background_grid = grid_superstructure.get_grids()
        grid.reset_save_cache()
        background_grid.reset_save_cache()

        # initialize inventory, player, and world
        inventory = Inventory(self.screen, self.window, self.world_generation_settings.inventory_height, self.world_generation_settings.health_bar_height)
        player = Player(grid, self.screen, ((self.world_generation_settings.grid_width * self.block_width) // 2), 0, self.block_width, x_size=22, y_size=40, inventory_bar_height=self.world_generation_settings.inventory_height, health_bar_height = self.world_generation_settings.health_bar_height, images=self.images)
        world_details = World_Details.create_new_world(self.world_name, self.world_generation_settings.version)

        return grid, background_grid, inventory, player, world_details
    
    def create_new_world_with_loading(self):
        # initialize the loading screen
        self.draw_loading_world_screen(0, 'Prepping World Generator')

        def resolve_seed():
            seed_string = self.custom_seed.strip()
            try:
                seedValue = int(seed_string)
                return seedValue
            except ValueError:
                value = 0
                for char in seed_string:
                    value = value * 31 + ord(char)
                return value % self.seed_length

        # create directory name
        new_directory_path = Path(f"{self.game_files_directory}/{self.world_name}")

        # initialize inventory, player, and world
        self.world_generation_settings.reset_ground_level(50)
        world_seed = resolve_seed()

        self.world_generation_settings.set_grid_width(self.size_to_width_dict[self.world_size_options[self.selected_world_size]])

        inventory = Inventory(self.screen, self.window, self.world_generation_settings.inventory_height, self.world_generation_settings.health_bar_height)
        world_spawn_x = ((self.world_generation_settings.grid_width * self.block_width) // 2)
        world_spawn_y = 0
        world_details = World_Details.create_new_world(self.world_name, self.world_generation_settings.version, world_spawn_x=world_spawn_x, world_spawn_y=world_spawn_y, world_seed=world_seed)

        # initialize grid and terrain
        grid_superstructure = Grid_Superstructure(self.screen, self.world_generation_settings, new_directory_path, world_seed, world_spawn_x)
        for GenerationText, percentComplete in grid_superstructure._generate_world():
            self.draw_loading_world_screen(percentComplete, GenerationText)
        grid, background_grid = grid_superstructure.get_grids()

        # create world save directory
        new_directory_path.mkdir()
        grid.generate_save_files()
        background_grid.generate_save_files()
        
        player = Player(grid, self.screen, world_spawn_x, world_spawn_y, self.block_width, x_size=22, y_size=40, inventory_bar_height=self.world_generation_settings.inventory_height, health_bar_height=self.world_generation_settings.health_bar_height, images=self.images)

        save_start_percent = 55
        save_end_percent = 99
        for percent, save_message in save_game(new_directory_path, player, inventory, grid, background_grid, world_details, save_start_percent, save_end_percent):
            self.draw_loading_world_screen(percent, save_message)

        # reset the grid caches to speed up saving
        grid.reset_save_cache()
        background_grid.reset_save_cache()

        self.custom_seed = self.getRandomSeed()

        return grid, background_grid, inventory, player, world_details
    
    def load_world_from_file(self):
        self.draw_loading_world_screen(0, 'Loading Grid')

        worlds_directory = f"{self.game_files_directory}/{self.world_name}"
        grid = Grid.fill_from_file(f"{self.game_files_directory}/{self.world_name}/foreground_grid", self.screen, self.block_width)
        
        self.draw_loading_world_screen(50, 'Loading Background')

        bg_grid = Grid.fill_from_file(f"{self.game_files_directory}/{self.world_name}/background_grid", self.screen, self.block_width)

        self.draw_loading_world_screen(90, 'Loading Inventory')

        with open(f"{worlds_directory}/inventory.json", "r") as inventory_file:
            inventory_dict = json.load(inventory_file)
            inventory = Inventory.fill_from_dict(inventory_dict, self.screen, self.window, self.world_generation_settings.inventory_height, self.world_generation_settings.health_bar_height)

        self.draw_loading_world_screen(95, 'Loading World Details')

        with open(f"{worlds_directory}/player_attributes.json", "r") as player_attr_file:
            player_attr_dict = json.load(player_attr_file)
            player_attr_dict["screen"] = self.screen
            player_attr_dict["grid"] = grid
            player_attr_dict["inventory_bar_height"] = self.world_generation_settings.inventory_height
            player_attr_dict["health_bar_height"] = self.world_generation_settings.health_bar_height
            player = Player(**player_attr_dict)
            player.images = self.images

        with open(f"{worlds_directory}/world_details.json", "r") as world_details_file:
            world_details_dict = json.load(world_details_file)
            world_details = World_Details.fill_from_dict(world_details_dict)

        self.draw_loading_world_screen(99, 'Finishing Up')

        return grid, bg_grid, inventory, player, world_details
    
    def reopen_menu_prep(self):
        self.world_names_list.remove(self.world_name)
        self.world_names_list.insert(0, self.world_name)
        self.run_game = False
        self.return_to_main()
        self.custom_seed = self.getRandomSeed()
        self.selected_world_size = self.default_selected_world_size

    # ------------------------ functions interacting with the main loop ------------------------ #

    def catch_exception(self): # reboots the menu
        new_menu = Menu(self.screen, self.window, self.images, self.width, self.height, self.block_width, self.world_names_list, self.game_files_directory, self.world_generation_settings)
        return Crash_Menu(self.screen, new_menu, self, "Sorry... The Menu Crashed", "Attempt to Reload")

    def finalExceptionHandle(self):
        pass

    def run(self, input):
        """runs the menu and returns function of class that will run next (normally itself)"""

        self.check_click(pygame.mouse, input.virtual_mouse_x, input.virtual_mouse_y)
        self.move_background()
        self.draw(input.virtual_mouse_x, input.virtual_mouse_y, input)

        # register keyboard inputs
        if input.escape_keypress:
            self.returnToLast()

        if self.run_game: # creates the play object that will be returned
            
            play_object = None

            if self.load_world:
                grid, background_grid, inventory, player, world_details = self.load_world_from_file()
                play_object = Play(self.screen, self.block_width, grid, background_grid, inventory, player, world_details, self)

            elif self.generate_new_world:
                self.world_names_list.insert(0, self.world_name)
                grid, background_grid, inventory, player, world_details = self.create_new_world_with_loading()
                play_object = Play(self.screen, self.block_width, grid, background_grid, inventory, player, world_details, self)

            if play_object is None: return self

            return play_object

        else:
            return self
    
    def on_quit(self):
        pass
    