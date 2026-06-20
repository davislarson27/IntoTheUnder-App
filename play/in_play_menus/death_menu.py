import pygame
import random
import components.fonts as font_manager

class Death_Menu:
    def __init__(self, screen, play):
        self.screen = screen
        self.play = play

        self.is_clicked = False
        self.quit_to_menu = False

        possible_death_messages = [
            'Pro Tip: 10 out of 10 doctors do not recommend death.',
            'Well that\'s unfortunate. Hopefully you had some life insurance.',
            '#whyyoushouldputitemsinchests should be trending in your feed.',
            'So, you\'re dead. Probably didn\'t expect that, did you?',
            'Next time, maybe try to get healed up, eh?',
            'Well that was unexpected... try again!',
            'Better luck next time! Respawn and keep going!',
            'That was honestly kinda cool... so maybe try again?',
            'I\'m sure that [insert copyrighted superhero here] would definitely approve!',
            'Was it worth it though?',
            '[Insert ridiculous death message here]',
            'Well that was unpleasant!',
            'Maybe try to press the \'F\' key and heal up next time, alright?',
            'Hint: Don\'t try that move again!',
            'If these death messages rage bait you... then mission accomplished!'
        ]
        self.death_message = random.choice(possible_death_messages)

        self.death_overlay_color = (180,60,60)
        self.button_color = (100, 100, 112)
        self.button_hover_color = (130, 130, 145)
        self.button_text_color = (240, 240, 240)
        self.title_text_color = (255, 255, 255)

        # menu grid sizing
        self.blocks_width = 28
        self.blocks_height = 28
        self.menu_block_width = self.screen.get_width() // self.blocks_width
        self.menu_block_height = self.screen.get_height() // self.blocks_height

        # fonts
        _f = font_manager.get()
        self.button_font = pygame.font.Font(str(_f.PixeloidSans), 18)
        self.title_font  = pygame.font.Font(str(_f.PixeloidSans_Bold), 48)

        # title
        title_column_width = 16
        title_column_margin_x = (self.blocks_width - title_column_width) // 2
        self.title_space = pygame.Rect(
            self.menu_block_width * title_column_margin_x,
            self.menu_block_height * 6,
            self.menu_block_width * title_column_width,
            self.menu_block_height * 4
        )
        self.title_surf = self.title_font.render("You Died", True, self.title_text_color)

        # death message
        self.death_message_font = pygame.font.Font(str(_f.PixeloidSans), 22)
        self.death_message_surf = self.death_message_font.render(self.death_message, True, self.title_text_color)
        self.death_message_rect = self.death_message_surf.get_rect(center=(self.title_space.centerx, int(self.menu_block_height * 10.25)))

        center_column_width = 12
        center_column_margin_x = (self.blocks_width - center_column_width) // 2

        self.btn_respawn = pygame.Rect(
            self.menu_block_width * center_column_margin_x,
            self.menu_block_height * 12,
            self.menu_block_width * center_column_width,
            self.menu_block_height * 2
        )
        self.btn_quit = pygame.Rect(
            self.menu_block_width * center_column_margin_x,
            self.menu_block_height * 15,
            self.menu_block_width * center_column_width,
            self.menu_block_height * 2
        )

        self.buttons = [
            (self.btn_respawn, "Respawn"),
            (self.btn_quit, "Return to Menu")
        ]

        self.death_overlay = pygame.Surface((self.screen.get_width(), self.screen.get_height()))
        death_overlay_alpha = 150
        self.death_overlay.set_alpha(death_overlay_alpha)
        self.death_overlay.fill(self.death_overlay_color)


    def check_click(self, mouse, mx, my):
        if not self.is_clicked and mouse.get_pressed()[0]:
            self.is_clicked = True
        elif self.is_clicked and not mouse.get_pressed()[0]:
            self.is_clicked = False
            return self.execute_clicked((mx, my))
        return self
    
    def execute_clicked(self, pos):
        if self.btn_respawn.collidepoint(pos):
            self.respawn()
            return None
        elif self.btn_quit.collidepoint(pos):
            self.quit_to_menu = True
        return self
    
    def respawn(self):
        if self.play.respawn_user():
            return True
        return False


    # main loop interaction methods

    def onEsc(self): # blocks escaping using escape button
        return self

    def open(self):
        pass

    def close(self):
        self.respawn()

    def sub_state_full_quit(self):
        if self.quit_to_menu: # ensures that when the player returns they are already respawned
            self.respawn()
        return self.quit_to_menu
    
    def catch_exception(self):
        pass
    
    def run(self, input):
        return_class = self.check_click(input.mouse, input.virtual_mouse_x, input.virtual_mouse_y)
        if return_class is None:
            return return_class
        self.draw(input.virtual_mouse_x, input.virtual_mouse_y)
        return return_class

    def draw(self, mx=0, my=0):
        self.play.draw_grid()

        # self.screen.fill(self.death_overlay_color)
        self.screen.blit(self.death_overlay, (0, 0))

        title_rect = self.title_surf.get_rect(center=self.title_space.center)
        self.screen.blit(self.title_surf, title_rect)

        self.screen.blit(self.death_message_surf, self.death_message_rect)

        for rect, label in self.buttons:
            color = self.button_hover_color if rect.collidepoint((mx, my)) else self.button_color
            pygame.draw.rect(self.screen, color, rect)

            text_surf = self.button_font.render(label, True, self.button_text_color)
            text_rect = text_surf.get_rect(center=rect.center)
            self.screen.blit(text_surf, text_rect)
