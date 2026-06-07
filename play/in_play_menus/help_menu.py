import pygame
from math import floor
import components.fonts as font_manager


class Help_Menu:
    def __init__(self, screen, esc_menu):
        self.screen = screen
        self.esc_menu = esc_menu

        self.is_clicked = False

        # ------------------------------------------------------------------ #
        #  colors                                                            #
        # ------------------------------------------------------------------ #

        self.background_color = (50,  50,  55)
        self.title_bar_color  = (38,  38,  43)
        self.bottom_bar_color = (38,  38,  43)
        self.title_text_color = (240, 240, 240)
        self.col_title_color  = (160, 160, 160)
        self.key_chip_bg      = (74,  74,  88)
        self.key_chip_text    = (232, 232, 232)
        self.key_chip_border  = (120, 120, 140)
        self.kb_desc_color    = (200, 200, 210)
        self.hint_text_color  = (104, 104, 120)
        self.back_btn_bg      = (74,  74,  88)
        self.back_btn_border  = (120, 120, 140)
        self.back_btn_hover   = (100, 100, 118)


        # ------------------------------------------------------------------ #
        #  grid                                                              #
        # ------------------------------------------------------------------ #

        self.tot_columns = 48
        self.tot_rows    = 48
        self.gw          = screen.get_width()  // self.tot_columns
        self.gh          = screen.get_height() // self.tot_rows

        W = screen.get_width()
        H = screen.get_height()

        # ------------------------------------------------------------------ #
        #  title bar                                                         #
        # ------------------------------------------------------------------ #

        title_bar_h         = self.gh * 5
        self.title_bar_rect = pygame.Rect(0, 0, W, title_bar_h)

        _f = font_manager.get()
        self.title_font = pygame.font.Font(str(_f.PixeloidSans_Bold), max(14, floor(self.gh * 2.6)))
        self.title_surf = self.title_font.render("How to Play", True, self.title_text_color)
        self.title_rect = self.title_surf.get_rect(center=(W // 2, title_bar_h // 2))

        # ------------------------------------------------------------------ #
        #  bottom bar                                                        #
        # ------------------------------------------------------------------ #

        bottom_bar_h         = self.gh * 4
        self.bottom_bar_rect = pygame.Rect(0, H - bottom_bar_h, W, bottom_bar_h)

        self.hint_font = pygame.font.Font(str(_f.PixeloidSans), max(8, floor(self.gh * 0.95)))
        hint_y         = H - bottom_bar_h + bottom_bar_h // 2

        hint1 = self.hint_font.render("[H]  toggle this menu", True, self.hint_text_color)
        hint2 = self.hint_font.render(".", True, self.hint_text_color)
        hint3 = self.hint_font.render("left-click a slot to select - click again to place or swap", True, self.hint_text_color)

        total_hint_w = hint1.get_width() + 16 + hint2.get_width() + 16 + hint3.get_width()
        hx = (W - total_hint_w) // 2
        self.bottom_hints = [
            (hint1, hint1.get_rect(midleft=(hx, hint_y))),
            (hint2, hint2.get_rect(midleft=(hx + hint1.get_width() + 16, hint_y))),
            (hint3, hint3.get_rect(midleft=(hx + hint1.get_width() + 16 + hint2.get_width() + 16, hint_y))),
        ]

        # ------------------------------------------------------------------ #
        #  content area - 2 columns                                          #
        # ------------------------------------------------------------------ #

        content_y    = title_bar_h
        content_h    = H - title_bar_h - bottom_bar_h
        col_margin_x = self.gw * 4
        col_gap_x    = self.gw * 4
        col_count    = 2
        col_w        = (W - 2 * col_margin_x - (col_count - 1) * col_gap_x) // col_count

        self.col_rects = []
        for i in range(col_count):
            x = col_margin_x + i * (col_w + col_gap_x)
            self.col_rects.append(pygame.Rect(x, content_y, col_w, content_h))

        div_x = col_margin_x + col_w + col_gap_x // 2
        self.dividers = [(div_x, content_y, content_h)]

        # ------------------------------------------------------------------ #
        #  fonts                                                             #
        # ------------------------------------------------------------------ #

        self.col_title_font = pygame.font.Font(str(_f.PixeloidSans_Bold), max(8, floor(self.gh * 0.95)))
        self.kb_key_font    = pygame.font.Font(str(_f.PixeloidSans), max(8, floor(self.gh * 1.0)))
        self.kb_desc_font   = pygame.font.Font(str(_f.PixeloidSans), max(8, floor(self.gh * 1.0)))

        # ------------------------------------------------------------------ #
        #  pre-build columns                                                 #
        # ------------------------------------------------------------------ #

        inner_pad_x = self.gw * 2
        inner_pad_y = self.gh * 2
        row_h       = self.gh * 3
        row_gap     = self.gh // 2
        section_gap = self.gh * 2

        # --- Column 0: Movement & World ---
        self.col0_items = self._build_keybind_col(
            col_title   = "MOVEMENT & WORLD",
            keybinds    = [
                (["W", "A", "S", "D", "/", "Space"],   "Move"),
                # (["W", "/", "Space"],    "Jump"),
                (["Left Click"],         "Mine block"),
                (["Right Click"],        "Place block"),
                (["Shift"],              "Avoid interacting with blocks"),
                (["Caps Lock"],          "Mine / place in background grid"),
                (["Scroll"],             "Change inventory slot"),
                (["E"],                  "Open inventory"),
                (["F"],                  "Open Fueling & Repair"),
                (["C"],                  "Open crafting recipes"),
            ],
            col_rect    = self.col_rects[0],
            inner_pad_x = inner_pad_x,
            inner_pad_y = inner_pad_y,
            row_h       = row_h,
            row_gap     = row_gap,
            section_gap = section_gap,
        )

        # --- Column 1: Building & Crafting ---
        self.col1_items = self._build_keybind_col(
            col_title   = "BUILDING & CRAFTING",
            keybinds    = [
                (["Setting Up"],   "Put Items in the Input Slots"),
                (["Swap Recipe"],   "Click the Arrows to Scroll Through Recipes"),
                (["Crafting"],  "Select Recipe Icon to Craft"),
                (["Collect"],   "Select the Crafted Item"),
                (["F3"],                 "Show debug menu"),
            ],
            col_rect    = self.col_rects[1],
            inner_pad_x = inner_pad_x,
            inner_pad_y = inner_pad_y,
            row_h       = row_h,
            row_gap     = row_gap,
            section_gap = section_gap,
        )

        # --- Back button ---
        self.back_font = pygame.font.Font(str(_f.PixeloidSans), max(8, floor(self.gh * 1.15)))
        back_label     = self.back_font.render("Back", True, self.key_chip_text)
        btn_pad_x      = self.gw * 2
        btn_pad_y      = self.gh
        btn_w          = back_label.get_width()  + btn_pad_x * 2
        btn_h          = back_label.get_height() + btn_pad_y * 2 - 1
        btn_x          = self.gw * 2
        btn_y          = (title_bar_h - btn_h) // 2 + 1
        self.back_btn_rect  = pygame.Rect(btn_x, btn_y, btn_w, btn_h)
        self.back_label_surf = back_label
        self.back_label_rect = back_label.get_rect(center=self.back_btn_rect.center)
        self._back_hovered   = False

    # ====================================================================== #
    #  layout helpers                                                        #
    # ====================================================================== #

    def _build_keybind_col(self, col_title, keybinds, col_rect,
                           inner_pad_x, inner_pad_y, row_h, row_gap, section_gap):
        items = []
        x0    = col_rect.x + inner_pad_x
        y     = col_rect.y + inner_pad_y

        title_surf = self.col_title_font.render(col_title, True, self.col_title_color)
        items.append(("text", title_surf, (x0, y)))
        y += title_surf.get_height() + section_gap

        chip_pad_x = max(3, self.gw // 2)
        chip_pad_y = max(2, self.gh // 3)
        chip_gap   = max(2, self.gw // 2)
        desc_gap   = self.gw

        for keys, desc in keybinds:
            row_top = y
            chips   = []
            cx      = x0

            for k in keys:
                k_surf = self.kb_key_font.render(k, True, self.key_chip_text)
                k_w    = k_surf.get_width()  + chip_pad_x * 2
                k_h    = k_surf.get_height() + chip_pad_y * 2

                if k == "/":
                    txt_rect = k_surf.get_rect(midleft=(cx, row_top + row_h // 2))
                    chips.append(("sep", k_surf, txt_rect))
                    cx += k_surf.get_width() + chip_gap
                else:
                    chip_rect = pygame.Rect(cx, row_top + (row_h - k_h) // 2, k_w, k_h)
                    txt_rect  = k_surf.get_rect(center=chip_rect.center)
                    chips.append(("chip", chip_rect, k_surf, txt_rect))
                    cx += k_w + chip_gap

            d_surf = self.kb_desc_font.render(desc, True, self.kb_desc_color)
            d_rect = d_surf.get_rect(midleft=(cx + desc_gap, row_top + row_h // 2))
            items.append(("kb_row", chips, d_surf, d_rect))

            line_y = y + row_h + row_gap // 2
            items.append(("divider_h", col_rect.x + inner_pad_x, line_y,
                          col_rect.right - inner_pad_x))

            y += row_h + row_gap

        return {"items": items, "next_y": y}

    # ====================================================================== #
    #  state management                                                      #
    # ====================================================================== #

    def open(self, side_pannel_use=None):
        pass

    def close(self):
        pass

    def sub_state_full_quit(self):
        return False

    def onEsc(self):
        return self.esc_menu

    # ====================================================================== #
    #  run / click                                                           #
    # ====================================================================== #

    def run(self, input):
        self._back_hovered = self.back_btn_rect.collidepoint(input.virtual_mouse_x, input.virtual_mouse_y)
        self.draw()
        return self.check_click(input.mouse, input.virtual_mouse_x, input.virtual_mouse_y)

    def check_click(self, mouse, mx, my):
        if not self.is_clicked and mouse.get_pressed()[0]:
            self.is_clicked = True
        elif self.is_clicked and not mouse.get_pressed()[0]:
            self.is_clicked = False
            return self.execute_clicked((mx, my))
        return self

    def execute_clicked(self, pos):
        if self.back_btn_rect.collidepoint(pos):
            return self.onEsc()

    # ====================================================================== #
    #  drawing                                                               #
    # ====================================================================== #

    def draw(self, mx=0, my=0):
        self.screen.fill(self.background_color)

        # title bar
        pygame.draw.rect(self.screen, self.title_bar_color, self.title_bar_rect)
        self.screen.blit(self.title_surf, self.title_rect)

        # bottom bar
        pygame.draw.rect(self.screen, self.bottom_bar_color, self.bottom_bar_rect)
        # for surf, rect in self.bottom_hints:
        #     self.screen.blit(surf, rect)

        # vertical divider between columns
        for (x, y, h) in self.dividers:
            div_line = pygame.Surface((1, h), pygame.SRCALPHA)
            div_line.fill((255, 255, 255, 20))
            self.screen.blit(div_line, (x, y))

        self._draw_keybind_col(self.col0_items)
        self._draw_keybind_col(self.col1_items)

        btn_color = self.back_btn_hover if self._back_hovered else self.back_btn_bg
        pygame.draw.rect(self.screen, btn_color, self.back_btn_rect, border_radius=4)
        pygame.draw.rect(self.screen, self.back_btn_border, self.back_btn_rect, width=1, border_radius=4)
        self.screen.blit(self.back_label_surf, self.back_label_rect)


    # ------------------------------------------------------------------ #
    #  draw helpers                                                       #
    # ------------------------------------------------------------------ #

    def _draw_keybind_col(self, col_data):
        for item in col_data["items"]:
            kind = item[0]

            if kind == "text":
                _, surf, pos = item
                self.screen.blit(surf, pos)

            elif kind == "kb_row":
                _, chips, d_surf, d_rect = item
                for chip in chips:
                    if chip[0] == "chip":
                        _, chip_rect, k_surf, txt_rect = chip
                        pygame.draw.rect(self.screen, self.key_chip_bg, chip_rect, border_radius=3)
                        pygame.draw.rect(self.screen, self.key_chip_border, chip_rect, width=1, border_radius=3)
                        self.screen.blit(k_surf, txt_rect)
                    else:
                        _, k_surf, txt_rect = chip
                        self.screen.blit(k_surf, txt_rect)
                self.screen.blit(d_surf, d_rect)

            elif kind == "divider_h":
                _, x0, y, x1 = item
                div = pygame.Surface((x1 - x0, 1), pygame.SRCALPHA)
                div.fill((255, 255, 255, 12))
                self.screen.blit(div, (x0, y))
    