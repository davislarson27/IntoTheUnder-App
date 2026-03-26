import pygame

class Input:
    def __init__(self):
        # held time inputs
        self.w_hold = 0
        self.a_hold = 0
        self.s_hold = 0
        self.d_hold = 0
        self.e_hold = 0
        self.c_hold = 0
        self.l_shift_hold = 0
        self.r_shift_hold = 0
        self.space_hold = 0
        self.return_hold = 0
        self.backspace_hold = 0

        # mouse inputs
        self.mouse = None
        self.scroll_change = 0
        self.virtual_mouse_x = None
        self.virtual_mouse_y = None

        # processing typing
        self.typed_text = ""

        # keydown inputs
        self.escape_keypress = False
        self.backspace_keypress = False
        self.e_keypress = False
        self.c_keypress = False
        self.return_keypress = False

        # quit key
        self.quit = False

    def take_input(self, scale, offx, offy):

        # ------------------------------------- event handling ------------------------------------- #
        # reset values
        self.typed_text = ""
        self.scroll_change = 0
        self.escape_keypress = False
        self.e_keypress = False
        self.c_keypress = False
        self.backspace_keypress = False
        self.return_keypress = False

        # set event inputs
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.set_quit()
                
            elif event.type == pygame.TEXTINPUT:
                self.typed_text += event.text

            elif event.type == pygame.MOUSEWHEEL:
                self.scroll_change += event.y

            elif event.type == pygame.KEYDOWN:
                self.escape_keypress = (event.key == pygame.K_ESCAPE)
                self.e_keypress = (event.key == pygame.K_e)
                self.c_keypress = (event.key == pygame.K_c)
                self.backspace_keypress = (event.key == pygame.K_BACKSPACE)
                self.return_keypress = (event.key == pygame.K_RETURN)


            # get virtual mouse positions
            mx, my = pygame.mouse.get_pos()
            self.mouse = pygame.mouse
            self.virtual_mouse_x, self.virtual_mouse_y = self.get_scaled_mouse_click(scale, mx, my, offx, offy)


            # input (held keys)
            keys = pygame.key.get_pressed()

            if keys[pygame.K_RETURN]: self.return_hold += 1
            else: self.return_hold = 0

            if keys[pygame.K_LSHIFT]: self.l_shift_hold += 1
            else: self.l_shift_hold = 0

            if keys[pygame.K_RSHIFT]: self.r_shift_hold += 1
            else: self.r_shift_hold = 0

            if keys[pygame.K_a]: self.a_hold += 1
            else: self.a_hold = 0

            if keys[pygame.K_d]: self.d_hold += 1
            else: self.d_hold = 0

            if keys[pygame.K_w]: self.w_hold += 1
            else: self.w_hold = 0

            if keys[pygame.K_SPACE]: self.space_hold += 1
            else: self.space_hold = 0
            
            if keys[pygame.K_s]: self.s_hold += 1
            else: self.s_hold = 0

            if keys[pygame.K_c]: self.c_hold += 1
            else: self.c_hold = 0

            if keys[pygame.K_BACKSPACE]: self.backspace_hold += 1
            else: self.backspace_hold = 0

    @staticmethod
    def get_scaled_mouse_click(scale, mouse_x, mouse_y, offx, offy):
        if scale == 0: #forcefully stops divide by 0, may cause different errors but this should not happen
            return None, None
        
        virtual_mouse_x = (mouse_x - offx) / scale
        virtual_mouse_y = (mouse_y - offy) / scale

        return virtual_mouse_x, virtual_mouse_y

    def set_quit(self):
        self.quit = True

    def check_quit(self):
        return self.quit
    