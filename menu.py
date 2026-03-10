import pygame
from math import floor, ceil

from grid import Grid
from world_generation import generate_world_blocks

class Menu:
    def __init__(self, screen, width_px, height_px, BLOCK_WIDTH, world_names_list):
        # draw_function_call
        # self.draw_function = self.draw_load_menu
        self.draw_function = self.draw_main

        # most attributes
        self.screen = screen
        self.width = width_px
        self.height = height_px
        self.run_game = False
        self.button_font = pygame.font.Font(None, 25)  # None = default font
        self.small_button_font = pygame.font.Font(None, 20)
        loading_world_screen_font = pygame.font.Font(None, 30)
        self.title_font = pygame.font.Font(None, 65)
        self.small_title_font = pygame.font.Font(None, 50)
        self.camera_x = 0
        self.background_move_speed = 0.2
        self.menu_running = True
        self.button_color = (140, 140, 140)
        self.button_select_color = (165, 165, 165)

        self.world_names_list = world_names_list
        # self.world_names_list = ["my_first_world", "my_second_world", "my_third_world", "my_fourth_world", "my_fifth_world", "my_sixth_world", "my_seventh_world"] # temp placeholder
        self.WORLDS_PER_LOAD_SCREEN = 3
        self.load_screen_factor = 0
        self.world_name = None
        
        # world options
        self.load_world = False
        self.generate_new_world = False

        # click variables
        self.is_clicked = False
        self.position_on_click = None

        # menu works under 28x28 grid where it chooses which get filled - these are the dementions for the "blocks"
        self.blocks_width = 28
        self.blocks_height = 28
        self.menu_block_width = self.width // self.blocks_width
        self.menu_block_height = self.height // self.blocks_height

        # loading and saving world screen
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

        # buttons on the menu
        self.button0_dimentions = pygame.Rect(floor(self.menu_block_width * 0.5), self.menu_block_height * 1, floor(self.menu_block_width * 2.5), floor(self.menu_block_height * 1.75))
        
        center_column_width = 12
        center_column_margin_x = (self.blocks_width - center_column_width)//2
        self.button1_dimentions = pygame.Rect(self.menu_block_width * center_column_margin_x, self.menu_block_height * 10, self.menu_block_width * center_column_width, self.menu_block_height * 2)
        self.button2_dimentions = pygame.Rect(self.menu_block_width * center_column_margin_x, self.menu_block_height * 13, self.menu_block_width * center_column_width, self.menu_block_height * 2)
        self.button3_dimentions = pygame.Rect(self.menu_block_width * center_column_margin_x, self.menu_block_height * 16, self.menu_block_width * center_column_width, self.menu_block_height * 2)
        # button 4 is split right-left if present
        RL_width = 5.5
        self.button4L_dimentions = pygame.Rect(self.menu_block_width * center_column_margin_x, self.menu_block_height * 19, floor(self.menu_block_width * RL_width), self.menu_block_height * 2)
        self.button4R_dimentions = pygame.Rect(floor(self.menu_block_width * RL_width) + (self.menu_block_width * (center_column_margin_x + 1)), self.menu_block_height * 19, floor(self.menu_block_width * RL_width), self.menu_block_height * 2)

        # generate menu background world
        load_screen_block_width = floor(BLOCK_WIDTH * 1.15) #slightly enlarge the blocks
        self.width_blocks = (width_px // load_screen_block_width) * 3
        self.height_blocks = (height_px // load_screen_block_width) + 1
        self.background_world_width_px = floor(self.width_blocks * load_screen_block_width)
        self.background_grid = Grid(self.width_blocks, self.height_blocks, load_screen_block_width, screen)
        generate_world_blocks(self.background_grid, self.width_blocks, self.height_blocks)

    def get_max_load_screens(self):
        return ceil(len(self.world_names_list) / self.WORLDS_PER_LOAD_SCREEN) 

    def execute_clicked(self, position_on_release):
        if self.draw_function.__func__ is self.draw_main.__func__:
            if self.button1_dimentions.collidepoint(self.position_on_click) and self.button1_dimentions.collidepoint(position_on_release):
                self.draw_function = self.draw_load_menu
            elif self.button2_dimentions.collidepoint(self.position_on_click) and self.button2_dimentions.collidepoint(position_on_release):
                self.generate_new_world = True
                self.run_game = True
            elif self.button3_dimentions.collidepoint(self.position_on_click) and self.button3_dimentions.collidepoint(position_on_release):
                self.menu_running = False
                self.run_game = True

        elif self.draw_function.__func__ is self.draw_load_menu.__func__:
            if len(self.world_names_list) > 0:
                if self.button0_dimentions.collidepoint(self.position_on_click) and self.button0_dimentions.collidepoint(position_on_release):
                    self.draw_function = self.draw_main
                elif self.WORLDS_PER_LOAD_SCREEN * self.load_screen_factor < len(self.world_names_list) and self.button1_dimentions.collidepoint(self.position_on_click) and self.button1_dimentions.collidepoint(position_on_release):
                    self.draw_function = self.draw_main
                    self.load_world = True
                    self.run_game = True
                    self.world_name = self.world_names_list[self.WORLDS_PER_LOAD_SCREEN * self.load_screen_factor]
                elif (self.WORLDS_PER_LOAD_SCREEN * self.load_screen_factor) + 1 < len(self.world_names_list) and self.button2_dimentions.collidepoint(self.position_on_click) and self.button2_dimentions.collidepoint(position_on_release):
                    self.draw_function = self.draw_main
                    self.load_world = True
                    self.run_game = True
                    self.world_name = self.world_names_list[(self.WORLDS_PER_LOAD_SCREEN * self.load_screen_factor) + 1]
                elif (self.WORLDS_PER_LOAD_SCREEN * self.load_screen_factor) + 2 < len(self.world_names_list) and self.button3_dimentions.collidepoint(self.position_on_click) and self.button3_dimentions.collidepoint(position_on_release):
                    self.draw_function = self.draw_main
                    self.load_world = True
                    self.run_game = True
                    self.world_name = self.world_names_list[(self.WORLDS_PER_LOAD_SCREEN * self.load_screen_factor) + 2]
                elif self.button4L_dimentions.collidepoint(self.position_on_click) and self.button4L_dimentions.collidepoint(position_on_release):
                    # this is the prev button
                    self.load_screen_factor -= 1
                    if self.load_screen_factor < 0:
                        self.load_screen_factor = self.get_max_load_screens() - 1
                elif self.button4R_dimentions.collidepoint(self.position_on_click) and self.button4R_dimentions.collidepoint(position_on_release):
                    # this is the prev button
                            self.load_screen_factor += 1
                            if self.load_screen_factor > self.get_max_load_screens() - 1:
                                self.load_screen_factor = 0
            else: # lets alt return button work
                if self.button2_dimentions.collidepoint(self.position_on_click) and self.button2_dimentions.collidepoint(position_on_release):
                    self.draw_function = self.draw_main

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

    def draw_main(self, mx, my):
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

    def draw_load_menu(self, mx, my):

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
                if self.button1_dimentions.collidepoint((mx, my)): cur_button_color = self.button_select_color
                else: cur_button_color = self.button_color
                pygame.draw.rect( # menu button
                    self.screen,
                    cur_button_color,
                    self.button1_dimentions
                )
                text_surf = self.button_font.render(self.world_names_list[start_world_position], True, (255, 255, 255))
                text_rect = text_surf.get_rect(center=self.button1_dimentions.center)
                self.screen.blit(text_surf, text_rect)

            # create second option button
            if (self.WORLDS_PER_LOAD_SCREEN * self.load_screen_factor) + 1 < len(self.world_names_list):
                if self.button2_dimentions.collidepoint((mx, my)): cur_button_color = self.button_select_color
                else: cur_button_color = self.button_color
                pygame.draw.rect( # menu button
                    self.screen,
                    cur_button_color,
                    self.button2_dimentions
                )
                text_surf = self.button_font.render(self.world_names_list[start_world_position + 1], True, (255, 255, 255))
                text_rect = text_surf.get_rect(center=self.button2_dimentions.center)
                self.screen.blit(text_surf, text_rect)

            # create third option button
            if (self.WORLDS_PER_LOAD_SCREEN * self.load_screen_factor) + 2 < len(self.world_names_list):
                if self.button3_dimentions.collidepoint((mx, my)): cur_button_color = self.button_select_color
                else: cur_button_color = self.button_color
                pygame.draw.rect( # menu button
                    self.screen,
                    cur_button_color,
                    self.button3_dimentions
                )
                text_surf = self.button_font.render(self.world_names_list[start_world_position + 2], True, (255, 255, 255))
                text_rect = text_surf.get_rect(center=self.button3_dimentions.center)
                self.screen.blit(text_surf, text_rect)

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

    def draw_confirm_delete_screen(self): # eventually this will allow deleting worlds in the game UI
        pass

    def draw_loading_world_screen(self, percent_complete=1):
        self.screen.fill(self.loading_world_screen_background_color)
        self.screen.blit(self.loading_world_title_surf, self.loading_world_screen_text_rect)
    
    def draw_saving_world_screen(self, percent_complete=1):
        self.screen.fill(self.loading_world_screen_background_color)
        self.screen.blit(self.saving_world_title_surf, self.saving_world_screen_text_rect)


    def draw(self, mx, my):
        # draw background before menus
        self.screen.fill((30,30,30))
        self.background_grid.draw(floor(self.camera_x), 0)

        self.draw_function(mx, my)
