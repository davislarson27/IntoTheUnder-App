"""note that this class is still largely managed by the menu code -> at some point management of a text box should be moved into its own class"""

class Text_Box():
    def __init__(self):
        # colors
        self.text_box_color = (220, 220, 220)
        self.text_box_color_active = (255, 255, 255)
        self.text_box_text_color = (40, 40, 40)
        self.text_box_outline_color = (120, 135, 150)
        self.text_box_outline_color_active = (145, 165, 210)

        # invalid characters
        self.invalid_characters = {
            "/",
            "\\",
            "{",
            "}",
            "[",
            "]",
            ".",
            ",",
            "#",
            "@",
            "^",
            "*",
            "&",
            "\"",
            "<",
            ">",
            ":",
            ";",
            "(",
            ")"
        }

        # animation details
        self.frames_active = 0
        self.is_typing = False
        self.b_space_hold_after_init_press = 0
        self.cur_string = ""

    def get_text_cursor(self):
        if self.is_typing:
            cycle_length = 60
            self.frames_active += 1
            cur_position = self.frames_active % cycle_length
            if cur_position < cycle_length // 2:
                return "|"
            else:
                return ""
        else:
            return ""
        
    def is_valid_character(self, input_char):
        if input_char in self.invalid_characters:
            return False
        return True
    
    def take_input(self, input, length_limit):
        ticks_between_backspace = 6
        if self.is_typing and input.typed_text is not None:
            if self.b_space_hold_after_init_press > 0:
                if input.backspace_hold > 0:
                    self.b_space_hold_after_init_press += 1
                    if self.b_space_hold_after_init_press % ticks_between_backspace == 1 and self.b_space_hold_after_init_press > ticks_between_backspace * 5:
                        self.cur_string = self.cur_string[:-1]
                else:
                    self.b_space_hold_after_init_press = 0
            elif input.backspace_keypress:
                self.cur_string = self.cur_string[:-1]
                self.b_space_hold_after_init_press = 1
            elif len(self.cur_string) < length_limit:
                if not input.typed_text in self.invalid_characters:
                    self.cur_string += input.typed_text
            
            # # reset text cursor to be shown when typing happens
            # self.frames_active = 0

    def get_cur_string(self):
        return self.cur_string
    
    def open_text_box(self, initial_string):
        self.frames_active = 0
        self.is_typing = False
        self.b_space_hold_after_init_press = 0
        self.cur_string = initial_string