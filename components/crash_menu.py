import pygame

class Crash_Menu:
    def __init__(self, screen, goToState, comeFromState, message="Sorry... Your Game Crashed", button_message="Return to Menu"):
        # general variables
        self.screen = screen

        # return menu
        self.goToState = goToState

        # coming from menu
        self.comeFromState = comeFromState

        # click variables
        self.is_clicked = False
        self.quitValue = False

        # colors
        self.background_color = (50, 50, 55)
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
        self.button_font = pygame.font.Font(None, 25)
        self.title_font = pygame.font.Font(None, 45)

        # title
        title_column_width = 16
        title_column_margin_x = (self.blocks_width - title_column_width) // 2
        self.title_space = pygame.Rect(
            self.menu_block_width * title_column_margin_x,
            self.menu_block_height * 5,
            self.menu_block_width * title_column_width,
            self.menu_block_height * 4
        )
        self.title_surf = self.title_font.render(message, True, self.title_text_color)

        # base buttons 1–3
        center_column_width = 12
        center_column_margin_x = (self.blocks_width - center_column_width) // 2

        self.btn_1 = pygame.Rect(
            self.menu_block_width * center_column_margin_x,
            self.menu_block_height * 10,
            self.menu_block_width * center_column_width,
            self.menu_block_height * 2
        )
        self.btn_2 = pygame.Rect(
            self.menu_block_width * center_column_margin_x,
            self.menu_block_height * 13,
            self.menu_block_width * center_column_width,
            self.menu_block_height * 2
        )
        self.btn_3 = pygame.Rect(
            self.menu_block_width * center_column_margin_x,
            self.menu_block_height * 16,
            self.menu_block_width * center_column_width,
            self.menu_block_height * 2
        )

        self.buttons = [
            (self.btn_1, button_message),
        ]

    # ------------------------------------------------------------------ #
    #  click check                                                       #
    # ------------------------------------------------------------------ #

    def check_click(self, mouse, mx, my):
        if not self.is_clicked and mouse.get_pressed()[0]:
            self.is_clicked = True
        elif self.is_clicked and not mouse.get_pressed()[0]:
            self.is_clicked = False
            return self.execute_clicked((mx, my))
        return self

    def execute_clicked(self, pos):
        if self.btn_1.collidepoint(pos):
            return self.goToState
        return self


    # ------------------------------------------------------------------ #
    #  drawing                                                           #
    # ------------------------------------------------------------------ #

    def draw(self, mx=0, my=0):
        self.screen.fill(self.background_color)

        title_rect = self.title_surf.get_rect(center=self.title_space.center)
        self.screen.blit(self.title_surf, title_rect)

        self._draw_buttons(mx, my)

    def _draw_buttons(self, mx, my):
        for rect, label in self.buttons:
            color = self.button_hover_color if rect.collidepoint((mx, my)) else self.button_color
            pygame.draw.rect(self.screen, color, rect)

            text_surf = self.button_font.render(label, True, self.button_text_color)
            text_rect = text_surf.get_rect(center=rect.center)
            self.screen.blit(text_surf, text_rect)


    # ------------------------------------------------------------------ #
    # interacting with the main loop
    # ------------------------------------------------------------------ #


    def catch_exception(self): # this is like bad if this breaks lol
        return self.goToState

    def run(self, input):
        returnClass = self.check_click(input.mouse, input.virtual_mouse_x, input.virtual_mouse_y)
        self.draw(input.virtual_mouse_x, input.virtual_mouse_y)
        if returnClass is not self:
            self.comeFromState.finalExceptionHandle()
        return returnClass

    def on_quit(self):
        pass
    