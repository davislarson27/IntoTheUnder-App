
class Help_Menu:
    def __init__(self, screen, esc_menu):
        self.screen = screen
        self.esc_menu = esc_menu

        self.background_color = (50, 50, 55)
        self.button_color = (100, 100, 112)
        self.button_hover_color = (130, 130, 145)
        self.button_text_color = (240, 240, 240)
        self.title_text_color = (255, 255, 255)

    def open(self, side_pannel_use=None):
        pass

    def close(self):
        pass

    def sub_state_full_quit(self):
        return False
    
    def onEsc(self):
        return self.esc_menu

    # ------------------------------------------------------------------ #
    #  run / click                                                       #
    # ------------------------------------------------------------------ #

    def run(self, input):
        returnClass = self
        self.draw()
        return returnClass

    def check_click(self, mouse, mx, my):
        pass

    def execute_clicked(self, pos):
        pass

    # ------------------------------------------------------------------ #
    #  drawing                                                           #
    # ------------------------------------------------------------------ #

    def draw(self, mx=0, my=0):
        self.screen.fill(self.background_color)

        # title_rect = self.title_surf.get_rect(center=self.title_space.center)
        # self.screen.blit(self.title_surf, title_rect)

        # self._draw_buttons(mx, my)
