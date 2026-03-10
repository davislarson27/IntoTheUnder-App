import pygame
from math import floor, ceil
import shutil
from pathlib import Path

from grid import Grid
from world_generation import generate_world_blocks
from text_box import Text_Box

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
    def __init__(self, screen, images, width_px, height_px, BLOCK_WIDTH, world_names_list, game_files_directory):
        # draw_function_call
        # self.draw_function = self.draw_load_menu
        self.draw_function = self.draw_main

        # most attributes
        self.screen = screen
        self.images = images
        self.width = width_px
        self.height = height_px
        self.run_game = False
        self.button_font = pygame.font.Font(None, 25)  # None = default font
        self.small_button_font = pygame.font.Font(None, 20)
        loading_world_screen_font = pygame.font.Font(None, 30)
        self.title_font = pygame.font.Font(None, 65)
        self.small_title_font = pygame.font.Font(None, 50)
        self.subscript_font = pygame.font.Font(None, 16)
        self.camera_x = 0
        self.background_move_speed = 0.2
        self.menu_running = True
        self.button_color = (140, 140, 140)
        self.button_select_color = (165, 165, 165)
        self.game_files_directory = game_files_directory

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
        self.loading_world_title_surf = loading_world_screen_font.render("loading...", True, (255, 255, 255))
        self.saving_world_title_surf = loading_world_screen_font.render("saving world...", True, (255, 255, 255))
        loading_world_screen_column_width = 16
        loading_world_margin_x = (self.blocks_width - loading_world_screen_column_width) // 2
        self.loading_world_title_rect = pygame.Rect(self.menu_block_width * loading_world_margin_x, self.menu_block_height * 12, self.menu_block_width * loading_world_screen_column_width, self.menu_block_height * 2)
        self.loading_world_screen_text_rect = self.loading_world_title_surf.get_rect(center=self.loading_world_title_rect.center)
        self.saving_world_screen_text_rect = self.saving_world_title_surf.get_rect(center=self.loading_world_title_rect.center)

        # menu titles
        title_column_width = 16
        title_column_margin_x = (self.blocks_width - title_column_width)//2
        self.title_space = pygame.Rect(self.menu_block_width * title_column_margin_x, self.menu_block_height * 5, self.menu_block_width * title_column_width, self.menu_block_height * 4)
        self.small_title_space = pygame.Rect(self.menu_block_width * title_column_margin_x, self.menu_block_height * 5, self.menu_block_width * title_column_width, self.menu_block_height * 4)
        self.main_text_surf = self.title_font.render("Into the Under", True, (255, 255, 255))
        # self.load_screen_text_surf = self.small_title_font.render("Select World", True, (255, 255, 255))
        # self.load_screen_text_surf = self.small_title_font.render(f"Select World ({self.load_screen_factor+1}/{self.get_max_load_screens()})", True, (255, 255, 255))

        # text box details
        self.padding = 12
        self.new_world_name_text_box = Text_Box()
        # self.text_box_list = [self.new_world_name_text_box]

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

        # generate menu background world
        load_screen_block_width = floor(BLOCK_WIDTH * 1.15) #slightly enlarge the blocks
        self.width_blocks = (width_px // load_screen_block_width) * 3
        self.height_blocks = (height_px // load_screen_block_width) + 1
        self.background_world_width_px = floor(self.width_blocks * load_screen_block_width)
        self.background_grid = Grid(self.width_blocks, self.height_blocks, load_screen_block_width, screen)
        generate_world_blocks(self.background_grid, self.width_blocks, self.height_blocks)

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

    def execute_clicked(self, position_on_release): # may need to add in self.

        # main menu
        if self.draw_function.__func__ is self.draw_main.__func__:
            if self.button1_dimentions.collidepoint(self.position_on_click) and self.button1_dimentions.collidepoint(position_on_release):
                self.draw_function = self.draw_load_menu
            elif self.button2_dimentions.collidepoint(self.position_on_click) and self.button2_dimentions.collidepoint(position_on_release):
                self.world_name = self.create_world_name()
                self.draw_function = self.draw_create_world_menu
            elif self.button3_dimentions.collidepoint(self.position_on_click) and self.button3_dimentions.collidepoint(position_on_release):
                self.menu_running = False
                self.run_game = True

        # if load world menu is active
        elif self.draw_function.__func__ is self.draw_load_menu.__func__:
            if len(self.world_names_list) > 0:
                # check the return button
                if self.button0_dimentions.collidepoint(self.position_on_click) and self.button0_dimentions.collidepoint(position_on_release):
                    self.draw_function = self.draw_main
                
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
                self.draw_function = self.draw_main
            elif self.button1_dimentions.collidepoint(self.position_on_click) and self.button1_dimentions.collidepoint(position_on_release):
                self.new_world_name_text_box.is_typing = True
            elif self.button2_dimentions.collidepoint(self.position_on_click) and self.button2_dimentions.collidepoint(position_on_release):
                # this will be an options box - needs more logic built in
                self.create_announce_screen("Options Are Not Yet Available")
            elif self.button3_dimentions.collidepoint(self.position_on_click) and self.button3_dimentions.collidepoint(position_on_release):
                if self.world_name in self.world_names_list or f"{self.world_name}{self.string_end_if_corrupted}" in self.world_names_list:
                    self.create_announce_screen(f"World Name \"{self.world_name}\" is Already in Use")
                else:
                    self.execute_create_new_world()

            # now deactivate the text box if something else if clicked
            if not self.button1_dimentions.collidepoint(self.position_on_click) and not self.button1_dimentions.collidepoint(position_on_release):
                self.new_world_name_text_box.is_typing = False


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

    def check_click(self, mouse, mx, my):
        if not self.is_clicked and mouse.get_pressed()[0]: # detect click
            self.is_clicked = True
            self.position_on_click = (mx, my)

        elif self.is_clicked and not mouse.get_pressed()[0]: # detect release
            self.execute_clicked((mx, my))
            self.is_clicked = False

    def move_background(self):
        if self.camera_x + self.width < self.background_world_width_px: self.camera_x += self.background_move_speed

    def draw_main(self, mx, my, text_input):
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

    def draw_load_menu(self, mx, my, text_input):

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

    def draw_confirm_delete_screen(self, mx, my, text_input): # eventually this will allow deleting worlds in the game UI
                
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

    def draw_loading_world_screen(self, percent_complete=1):
        self.screen.fill(self.loading_world_screen_background_color)
        self.screen.blit(self.loading_world_title_surf, self.loading_world_screen_text_rect)
    
    def draw_saving_world_screen(self, percent_complete=1):
        self.screen.fill(self.loading_world_screen_background_color)
        self.screen.blit(self.saving_world_title_surf, self.saving_world_screen_text_rect)

    def draw_announce_and_return_screen(self, mx, my, text_input):
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

    def draw_create_world_menu(self, mx, my, text_input):
        # handle text input
        if self.new_world_name_text_box.is_typing and text_input is not None:
            if text_input == "backspace":
                self.world_name = self.world_name[:-1]
            elif len(self.world_name) < self.world_name_length_limit:
                if not text_input in self.new_world_name_text_box.invalid_characters:
                    self.world_name += text_input
            
            # reset text cursor to be shown when typing happens
            self.new_world_name_text_box.frames_active = 0
        

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
        text_box_color = (220, 220, 220)
        text_box_color_hover = (245, 245, 245)
        text_box_text_color = (40, 40, 40)
        text_box_outline_color = (120, 135, 150)
        text_box_outline_color_hover = (150, 170, 190)
        if self.button1_dimentions.collidepoint((mx, my)): 
            cur_button_color = text_box_color_hover
        else: 
            cur_button_color = text_box_color
        pygame.draw.rect( # world name text box
            self.screen,
            cur_button_color,
            self.button1_dimentions
        )
        pygame.draw.rect( # outline
            self.screen,
            text_box_outline_color,
            self.button1_dimentions,
            width=1
        )

        display_string = self.world_name + self.new_world_name_text_box.get_text_cursor()
        text_surf = self.button_font.render(display_string, True, text_box_text_color)
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



    def draw(self, mx, my, text_input):
        # draw background before menus
        self.screen.fill((30,30,30))
        self.background_grid.draw(floor(self.camera_x), 0)

        self.draw_function(mx, my, text_input)
