class Text_Box():
    def __init__(self):
        # colors
        self.text_box_color = (220, 220, 220)
        self.text_box_color_hover = (245, 245, 245)
        self.text_box_text_color = (40, 40, 40)
        self.text_box_outline_color = (120, 135, 150)
        self.text_box_outline_color_hover = (150, 170, 190)

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
        if self.is_typing and input.typed_text is not None:
            if input.backspace_keypress:
                self.cur_string = self.cur_string[:-1]
            elif len(self.cur_string) < length_limit:
                if not input.typed_text in self.invalid_characters:
                    self.cur_string += input.typed_text
            
            # reset text cursor to be shown when typing happens
            self.frames_active = 0

    def get_cur_string(self):
        return self.cur_string
    
    def set_init_string(self, initial_string):
        self.cur_string = initial_string