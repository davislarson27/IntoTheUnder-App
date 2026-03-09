import pygame

from components.blocks.blocks import *
from play.inventory.crafting_recipe import *
from play.inventory.inventory_item import Inventory_Item


class Inventory:

    def __init__(self, screen, window, INVENTORY_HEIGHT, HEALTH_BAR_HEIGHT = 25, cur_position_index = 0):
        self.screen = screen
        
        self.expanded_inventory = []
        self.active_slots = []

        # ----------------------------------- toggle variables ----------------------------------- #

        self.show_full_item_management = False


        # ----------------------------------- helper functions ----------------------------------- #

        def triangle_points_in_rect(rect: pygame.Rect, direction: str, pad_px: int = 2):
            r = rect.inflate(-2*pad_px, -2*pad_px)

            if direction == "up":
                return [(r.centerx, r.top), (r.left, r.bottom), (r.right, r.bottom)]
            elif direction == "down":
                return [(r.left, r.top), (r.right, r.top), (r.centerx, r.bottom)]
            else:
                raise ValueError("direction must be 'up' or 'down'")


        # -------------------------------- click & selection variables-------------------------------- #

        # click positions
        self.is_clicked = False
        self.position_on_click = None

        # inventory nav attributes
        self.selected_inventory_slot = None

        # position in inventory variables
        self.cur_position_index = cur_position_index

        # -------------------------------------- scrolling data -------------------------------------- #

        self.scrolls_per_inventory_slot = 1
        self.cur_scroll_position = self.cur_position_index * self.scrolls_per_inventory_slot


        # -------------------------------------- general blocks -------------------------------------- #

        # grid sizes
        self.tot_columns = 48
        self.tot_rows = 48
        self.grid_width_px = self.screen.get_width() // self.tot_columns
        self.grid_height_px = self.screen.get_height() // self.tot_rows

        # box dimentions
        self.box_width = self.grid_height_px * 4

        # label (textbox) sizing/spacing
        self.label_gap_y = int(self.grid_height_px * 0.5)
        self.label_height = max(12, int(self.grid_height_px * 1.0))

        section_label_height = floor(2.4 * self.grid_height_px)


        # item frame box details
        item_percent_of_box = 0.75
        full_inventory_item_size = floor(self.box_width * item_percent_of_box) # item is 75% as long as its box is
        full_inventory_item_margin = floor((self.box_width - full_inventory_item_size) / 2)

        # initalize fonts
        self.hot_bar_font = pygame.font.Font(None, 36)  # None = default font, 36 = size
        self.percent_font_of_block_full_inventory = 0.75
        self.full_inventory_font = pygame.font.Font(None, floor(full_inventory_item_size * self.percent_font_of_block_full_inventory))

        self.inventory_item_name_font = pygame.font.Font(None, 16)
        self.hot_bar_name_font = pygame.font.Font(None, 15)
        
        self.section_label = pygame.font.Font(None, section_label_height)

        # colors
        self.base_box_color = (200, 200, 200)
        self.selected_box_color = (246, 246, 246)
        self.inventory_text_color = (255, 255, 255)
        self.hot_bar_background_color = (50, 50, 50)
        self.item_mng_background_color = (77, 77, 87)
        self.side_pannel_background_color = (85, 85, 95)

        self.section_title_color = (160, 160, 160)
        self.slot_label_color = (200, 200, 200)


        # -------------------------------------- hot bar -------------------------------------- #
        # inventory details
        self.items_in_hot_bar = 9

        # inventory hot bar dimentions
        self.inventory_height = self.grid_height_px * 7
        self.inventory_start_height = self.screen.get_height() - self.inventory_height
        self.hot_bar_margin_x = 7 * self.grid_width_px
        hot_bar_width = self.screen.get_width() - (self.hot_bar_margin_x * 2)
        margin_between_hot_bar_boxes = (hot_bar_width - (self.items_in_hot_bar * self.box_width)) // (self.items_in_hot_bar - 1)
        hot_bar_margin_y = (self.inventory_height - self.box_width) // 2
        hot_bar_start_height = self.screen.get_height() - hot_bar_margin_y - self.box_width

        # pygame objects
        self.inventory_background = pygame.Rect(
            0,
            self.inventory_start_height,
            self.screen.get_width(),
            self.inventory_height
        )

        for i in range(self.items_in_hot_bar): # fills hot bar with positions
            hit_box = pygame.Rect(
                (i * (self.box_width + margin_between_hot_bar_boxes)) + self.hot_bar_margin_x,
                hot_bar_start_height,
                self.box_width,
                self.box_width
            )
            item_frame = pygame.Rect(
                (i * (self.box_width + margin_between_hot_bar_boxes)) + self.hot_bar_margin_x + full_inventory_item_margin,
                hot_bar_start_height + full_inventory_item_margin,
                full_inventory_item_size,
                full_inventory_item_size
            )
            label_rect = pygame.Rect(
                hit_box.x,
                hit_box.bottom + self.label_gap_y - 2, # gets it a hair close and centers it
                hit_box.width,
                self.label_height
            )

            self.expanded_inventory.append(Inventory_Position(hit_box, item_frame, label_rect=label_rect))


        # --------------------------------- expanded item management --------------------------------- #

        item_mng_start_height = 0
        item_mng_height = self.inventory_start_height # may want to change to an exact number independent of this

        self.item_mng_background = pygame.Rect(
            0,
            item_mng_start_height,
            self.screen.get_width(),
            item_mng_height
        )


        # ----------------------------- expanded inventory ------------------------------ #

        exp_inventory_width = (self.screen.get_width() // 3) * 2

        boxes_per_row = 8
        boxes_high = 4
        self.exp_inventory_size = boxes_high * boxes_per_row

        exp_inventory_margin_x = 2 * self.grid_width_px
        exp_inventory_margin_y = 7 * self.grid_height_px

        margin_between_exp_inventory_boxes_x = (exp_inventory_width - (2 * exp_inventory_margin_x) - (boxes_per_row * self.box_width)) // (boxes_per_row - 1)
        margin_between_exp_inventory_boxes_y = (item_mng_height - (2 * exp_inventory_margin_y) - (boxes_high * self.box_width)) // (boxes_high - 1)

        section_label_start_height = (exp_inventory_margin_y - section_label_height) // 3

        inventory_label_box = pygame.Rect(
            0,
            section_label_start_height,
            exp_inventory_width,
            section_label_height
        )
        
        self.inventory_label_text_surface = self.section_label.render(  # optional: bigger font
            "Inventory",
            True,
            self.section_title_color
        )

        self.inventory_label_rect = self.inventory_label_text_surface.get_rect(
            center=inventory_label_box.center
        )


        for y in range(boxes_high):
            for x in range(boxes_per_row):
                hit_box = pygame.Rect(
                    (x * (margin_between_exp_inventory_boxes_x + self.box_width)) + exp_inventory_margin_x,
                    (y * (margin_between_exp_inventory_boxes_y + self.box_width)) + exp_inventory_margin_y,
                    self.box_width,
                    self.box_width
                )
                item_frame = pygame.Rect(
                    (x * (margin_between_exp_inventory_boxes_x + self.box_width)) + exp_inventory_margin_x + full_inventory_item_margin,
                    (y * (margin_between_exp_inventory_boxes_y + self.box_width)) + exp_inventory_margin_y + full_inventory_item_margin,
                    full_inventory_item_size,
                    full_inventory_item_size
                )
                label_rect = pygame.Rect(
                    hit_box.x,
                    hit_box.bottom + self.label_gap_y,
                    hit_box.width,
                    self.label_height
                )
                self.expanded_inventory.append(Inventory_Position(hit_box, item_frame, label_rect=label_rect))
        

        # ----------------------------------- crafting ----------------------------------- #

        crafting_start_x = ((boxes_per_row - 1) * margin_between_exp_inventory_boxes_x) + (boxes_per_row * self.box_width) + (2 * exp_inventory_margin_x)  # calculates where inventory ended
        crafting_width = self.screen.get_width() - crafting_start_x

        distance_between_boxes_x = 2 * self.grid_width_px
        count_crafting_input_slots = 3  # everything else is assumed to be 1

        crafting_margin_y = exp_inventory_margin_y  # keep as-is

        self.side_pannel_background = pygame.Rect(
            crafting_start_x,
            0,
            crafting_width,
            item_mng_height
        )

        self.crafting_object = Crafting_Slots(count_crafting_input_slots)

        # ----------------------------- get title ----------------------------- #

        side_pannel_label_box = pygame.Rect(
            crafting_start_x,
            section_label_start_height,
            crafting_width,
            section_label_height
        )
        
        crafting_section_label_text_surface = self.section_label.render(  # optional: bigger font
            "Crafting",
            True,
            self.section_title_color
        )

        crafting_section_label_rect = crafting_section_label_text_surface.get_rect(
            center=side_pannel_label_box.center
        )

        self.crafting_object.title_label_text_surface = crafting_section_label_text_surface
        self.crafting_object.section_label_rect = crafting_section_label_rect


        # -------------------- ALIGN WITH TOP 3 INVENTORY ROWS -------------------- #
        row_step_y = self.box_width + margin_between_exp_inventory_boxes_y

        # Top-aligned: rows 0, 1, 2
        input_top_y = exp_inventory_margin_y + 0 * row_step_y
        input_mid_y = exp_inventory_margin_y + 1 * row_step_y
        input_bot_y = exp_inventory_margin_y + 2 * row_step_y

        # -------------------- HORIZONTAL "SPINE" LAYOUT -------------------- #
        spine_group_width = (3 * self.box_width) + (2 * distance_between_boxes_x)

        # center the group in the crafting panel (horizontally)
        crafting_margin_x = (crafting_width - spine_group_width) // 2

        input_col_x = crafting_start_x + crafting_margin_x
        recipe_x = input_col_x + self.box_width + distance_between_boxes_x
        output_x = recipe_x + self.box_width + distance_between_boxes_x

        # -------------------- PLACE INPUTS (STACKED) -------------------- #
        input_ys = [input_top_y, input_mid_y, input_bot_y]

        for i in range(count_crafting_input_slots):
            y = input_ys[i]

            self.crafting_object.crafting_input_slots[i].hit_box = pygame.Rect(
                input_col_x,
                y,
                self.box_width,
                self.box_width
            )
            self.crafting_object.crafting_input_slots[i].item_frame = pygame.Rect(
                input_col_x + full_inventory_item_margin,
                y + full_inventory_item_margin,
                full_inventory_item_size,
                full_inventory_item_size
            )

        # -------------------- RECIPE + OUTPUT ALIGNED WITH MIDDLE INPUT -------------------- #
        self.crafting_object.recipe_slot.hit_box = pygame.Rect(
            recipe_x,
            input_mid_y,
            self.box_width,
            self.box_width
        )
        self.crafting_object.recipe_slot.item_frame = pygame.Rect(
            recipe_x + full_inventory_item_margin,
            input_mid_y + full_inventory_item_margin,
            full_inventory_item_size,
            full_inventory_item_size
        )

        self.crafting_object.output_slot.hit_box = pygame.Rect(
            output_x,
            input_mid_y,
            self.box_width,
            self.box_width
        )
        self.crafting_object.output_slot.item_frame = pygame.Rect(
            output_x + full_inventory_item_margin,
            input_mid_y + full_inventory_item_margin,
            full_inventory_item_size,
            full_inventory_item_size
        )
        

        # -------------------- create recipe object to be shown -------------------- #

        # Outline styling (tweak to taste)
        recipe_outline_w = 3
        recipe_outline_valid   = (135, 170, 145)   # green-ish (valid)
        recipe_outline_invalid = (110, 110, 125)   # muted pipe-ish (invalid)

        # Hook a UI renderer object into the recipe slot
        # main_rect: where outline is drawn
        # block_rect: where the output block icon is drawn
        self.crafting_object.recipe_slot.inventory_item = Recipe_Slot_Contents(
            main_rect=self.crafting_object.recipe_slot.hit_box,
            block_rect=self.crafting_object.recipe_slot.item_frame,
            recipe=None,  # will be filled in dynamically by Crafting_Slots.draw()
            outline_width=recipe_outline_w,
            valid_recipe_color=recipe_outline_valid,
            invalid_recipe_color=recipe_outline_invalid
        )

        # -------------------- STRAIGHT PIPE RECTS (WITH GAP FROM BOXES) -------------------- #

        self.crafting_flow_rects = []

        self.pipe_color_inactive = (115, 115, 130)
        self.pipe_color_active = (135, 170, 145)
        pipe_thickness = 3
        pipe_gap = max(4, self.grid_width_px // 2)  # gap between pipe and box

        top_box = self.crafting_object.crafting_input_slots[0].hit_box
        mid_box = self.crafting_object.crafting_input_slots[1].hit_box
        bot_box = self.crafting_object.crafting_input_slots[2].hit_box

        recipe_box = self.crafting_object.recipe_slot.hit_box
        output_box = self.crafting_object.output_slot.hit_box


        def _make_hpipe(x1, x2, y):
            """Horizontal pipe rect from x1 to x2 at y (handles direction)."""
            if x2 < x1:
                x1, x2 = x2, x1
            w = x2 - x1
            if w <= 0:
                return None
            return pygame.Rect(x1, y - pipe_thickness // 2, w, pipe_thickness)


        def _make_vpipe(y1, y2, x):
            """Vertical pipe rect from y1 to y2 at x (handles direction)."""
            if y2 < y1:
                y1, y2 = y2, y1
            h = y2 - y1
            if h <= 0:
                return None
            return pygame.Rect(x - pipe_thickness // 2, y1, pipe_thickness, h)


        # Centers for alignment of pipes
        top_cx, top_cy = top_box.center
        mid_cx, mid_cy = mid_box.center
        bot_cx, bot_cy = bot_box.center
        rec_cx, rec_cy = recipe_box.center
        out_cx, out_cy = output_box.center

        # 1) Vertical pipe: between top and middle (gap from boxes)
        v1 = _make_vpipe(top_box.bottom + pipe_gap, mid_box.top - pipe_gap, mid_cx)
        if v1:
            self.crafting_flow_rects.append(v1)

        # 2) Vertical pipe: between middle and bottom (gap from boxes)
        v2 = _make_vpipe(mid_box.bottom + pipe_gap, bot_box.top - pipe_gap, mid_cx)
        if v2:
            self.crafting_flow_rects.append(v2)

        # 3) Horizontal pipe: middle -> recipe (gap from boxes)
        h1 = _make_hpipe(mid_box.right + pipe_gap, recipe_box.left - pipe_gap, mid_cy)
        if h1:
            self.crafting_flow_rects.append(h1)

        # 4) Horizontal pipe: recipe -> output (gap from boxes)
        h2 = _make_hpipe(recipe_box.right + pipe_gap, output_box.left - pipe_gap, rec_cy)
        if h2:
            self.crafting_flow_rects.append(h2)

        # --------------------------------- up and down arrow slots --------------------------------- #

        # --- Tunables ---
        arrow_height_scale = 5 / 12          # one third of normal slot height
        arrow_width_scale  = 1            # almost full width
        arrow_padding_y    = max(6, self.grid_height_px * 1)

        recipe_rect = self.crafting_object.recipe_slot.hit_box

        # Arrow dimensions
        arrow_w = int(self.box_width * arrow_width_scale)
        arrow_h = int(self.box_width * arrow_height_scale)

        # Center horizontally with recipe slot
        arrow_x = recipe_rect.centerx - arrow_w // 2

        # Vertical positions
        up_y   = recipe_rect.top - arrow_padding_y - arrow_h
        down_y = recipe_rect.bottom + arrow_padding_y

        # Optional safety clamp to crafting panel bounds
        top_limit = 0
        bottom_limit = item_mng_height

        if up_y < top_limit:
            up_y = top_limit

        if down_y + arrow_h > bottom_limit:
            down_y = bottom_limit - arrow_h

        # Build rects
        up_rect = pygame.Rect(arrow_x, up_y, arrow_w, arrow_h)
        down_rect = pygame.Rect(arrow_x, down_y, arrow_w, arrow_h)

        # Assign to crafting slots
        self.crafting_object.point_up_slot.hit_box = up_rect
        self.crafting_object.point_up_slot.item_frame = up_rect.inflate(-4, -4)

        self.crafting_object.point_down_slot.hit_box = down_rect
        self.crafting_object.point_down_slot.item_frame = down_rect.inflate(-4, -4)

        arrow_color = (70, 80, 90)
        arrow_sel   = (90, 90, 105)

        up_pts = triangle_points_in_rect(self.crafting_object.point_up_slot.item_frame, "up", pad_px=2)
        dn_pts = triangle_points_in_rect(self.crafting_object.point_down_slot.item_frame, "down", pad_px=2)

        self.crafting_object.point_up_slot.inventory_item = Special_Slot_Polygon(up_pts, arrow_color, arrow_sel)
        self.crafting_object.point_down_slot.inventory_item = Special_Slot_Polygon(dn_pts, arrow_color, arrow_sel)

        # ----------------------------- crafting labels (relative to arrow buttons) ----------------------------- #

        label_h = self.label_height
        gap = self.label_gap_y + (self.grid_height_px * 0.3)
        stacked_label_h = (self.label_height * 2) + (gap // 2)

        up_rect = self.crafting_object.point_up_slot.hit_box
        down_rect = self.crafting_object.point_down_slot.hit_box

        # --- Recipe name (above UP arrow) ---
        recipe_name_box = pygame.Rect(
            up_rect.x,
            up_rect.top - gap - stacked_label_h,
            up_rect.width,
            stacked_label_h
        )

        # (surface rendered dynamically in Crafting_Slots.draw())
        self.crafting_object.recipe_name_rect = recipe_name_box

        # --- Craft label (below DOWN arrow) ---
        craft_label_box = pygame.Rect(
            down_rect.x,
            down_rect.bottom + gap,
            down_rect.width,
            label_h
        )

        self.crafting_object.craft_label_text_surface = self.inventory_item_name_font.render(
            "(Craft)",
            True,
            self.slot_label_color
        )

        self.crafting_object.craft_label_rect = self.crafting_object.craft_label_text_surface.get_rect(
            center=craft_label_box.center
        )

        # --- Collect label (below output slot) ---
        output_hb = self.crafting_object.output_slot.hit_box

        collect_label_box = pygame.Rect(
            output_hb.x,
            output_hb.bottom + gap,
            output_hb.width,
            label_h
        )

        self.crafting_object.collect_label_text_surface = self.inventory_item_name_font.render(
            "(Collect)",
            True,
            self.slot_label_color
        )

        self.crafting_object.collect_label_rect = self.crafting_object.collect_label_text_surface.get_rect(
            center=collect_label_box.center
        )


        # --------------------------------------- chest side pannel logic --------------------------------------- #

        chest_cols = 3
        chest_rows = 4
        count_chest_slots = chest_cols * chest_rows

        self.chest_side_pannel = Chest_Slots(count_chest_slots)

        # Match the main inventory's vertical spacing so rows align visually
        row_step_y = self.box_width + margin_between_exp_inventory_boxes_y

        # We'll also match the general horizontal feel (use same distance_between_boxes_x as crafting)
        chest_gap_x = distance_between_boxes_x

        # Total grid size
        grid_w = (chest_cols * self.box_width) + ((chest_cols - 1) * chest_gap_x)
        grid_h = (chest_rows * self.box_width) + ((chest_rows - 1) * margin_between_exp_inventory_boxes_y)

        # Center inside the side panel rect
        panel = self.side_pannel_background
        start_x = panel.x + (panel.width - grid_w) // 2
        start_y = panel.y + (panel.height - grid_h) // 2

        # item frame sizing matches inventory slots
        for r in range(chest_rows):
            for c in range(chest_cols):
                idx = r * chest_cols + c

                x = start_x + c * (self.box_width + chest_gap_x)
                y = start_y + r * (self.box_width + margin_between_exp_inventory_boxes_y)

                hit_box = pygame.Rect(x, y, self.box_width, self.box_width)
                item_frame = pygame.Rect(
                    x + full_inventory_item_margin,
                    y + full_inventory_item_margin,
                    full_inventory_item_size,
                    full_inventory_item_size
                )
                label_rect = pygame.Rect(
                    hit_box.x,
                    hit_box.bottom + self.label_gap_y,
                    hit_box.width,
                    self.label_height
                )


                self.chest_side_pannel.chest_slots[idx].hit_box = hit_box
                self.chest_side_pannel.chest_slots[idx].item_frame = item_frame
                self.chest_side_pannel.chest_slots[idx].label_rect = label_rect


                # ----------------------------- chest section label ----------------------------- #

                chest_section_label_text_surface = self.section_label.render(  # optional: bigger font
                    "Chest",
                    True,
                    self.section_title_color
                )

                chest_section_label_rect = chest_section_label_text_surface.get_rect(
                    center=side_pannel_label_box.center
                )

                self.chest_side_pannel.title_label_text_surface = chest_section_label_text_surface
                self.chest_side_pannel.section_label_rect = chest_section_label_rect



                # --------------------------------------- general side pannel logic --------------------------------------- #
                self.default_side_pannel = self.crafting_object
                self.side_pannel = None

                self.side_pannel_slots = 0



        # --------------------------------------- end __init__() --------------------------------------- #


    def __str__(self):
        returnString = ""
        i = 0
        for slot in self.expanded_inventory:
            if slot.inventory_item is None:
                returnString += f"position {i}: None"
            else:
                returnString += f"position {i}: {slot.inventory_item.Block_Type.str_name} (x{slot.inventory_item.count_of_items})"
            returnString += "\n"
            i+=1
        return returnString

# -------------------------------------------- saving and reloading methods -------------------------------------------- #
    
    def to_dict(self):
        inventory_items = []
        # for slot in self.hot_bar:
        #     cur_item = slot.inventory_item
        #     if cur_item is not None: inventory_items.append([cur_item.Block_Type.str_name, cur_item.count_of_items])
        #     else: inventory_items.append(None)
        for slot in self.expanded_inventory:
            cur_item = slot.inventory_item            
            if cur_item is not None: inventory_items.append([cur_item.Block_Type.str_name, cur_item.count_of_items])
            else: inventory_items.append(None)


        return {
            "cur_position_index": self.cur_position_index,
            "inventory_items": inventory_items
        }
    
    @staticmethod
    def fill_from_dict(inventory_dict, screen, window, INVENTORY_HEIGHT, HEALTH_BAR_HEIGHT):
        # get position
        cur_position_index = inventory_dict["cur_position_index"]

        # create new inventory
        inventory = Inventory(screen, window, INVENTORY_HEIGHT, HEALTH_BAR_HEIGHT, cur_position_index)

        # get block conversion dictionary and list of slots
        str_to_block = get_str_to_block()
        inventory_items = inventory_dict["inventory_items"]

        # get inventory contents
        for i in range(len(inventory_items)):
            slot = inventory_items[i]
            if slot is not None:
                block_type = str_to_block[slot[0]]
                block_count = slot[1]
                inventory.expanded_inventory[i].inventory_item = Inventory_Item(block_type, block_count)

        return inventory


# -------------------------------------------- interacting with blocks methods -------------------------------------------- #

    def add_item(self, item):
        empty_slot = None
        for i in range(self.exp_inventory_size + self.items_in_hot_bar):
            if self.expanded_inventory[i].inventory_item != None and item == self.expanded_inventory[i].inventory_item.Block_Type and self.expanded_inventory[i].inventory_item.can_add():
                self.expanded_inventory[i].inventory_item.add_block()
                return
            if empty_slot == None and self.expanded_inventory[i].inventory_item == None: empty_slot = i

        if empty_slot is not None:
            self.expanded_inventory[empty_slot].inventory_item = Inventory_Item(item)

    def build_from_current(self):
        cur_inventory_slot = self.expanded_inventory[floor(self.cur_position_index)].inventory_item
        if cur_inventory_slot is not None and not issubclass((cur_inventory_slot.Block_Type), Item):
            block_type = cur_inventory_slot.Block_Type
            if cur_inventory_slot.remove_block():
                if cur_inventory_slot.count_of_items == 0:
                    self.expanded_inventory[self.cur_position_index].inventory_item = None
            return block_type
        return None
    
    def get_current(self):
        cur_inventory_slot = self.expanded_inventory[floor(self.cur_position_index)].inventory_item
        if cur_inventory_slot is None:
            return None
        return cur_inventory_slot.Block_Type
        
    def set_cur_position(self, index):
        self.cur_position_index = floor(index)


# ------------------------------------------------ mouse imput methods ------------------------------------------------ #

    def check_click(self, mouse, mx, my):
        if not self.is_clicked and mouse.get_pressed()[0]: # detect click
            self.is_clicked = True

        elif self.is_clicked and not mouse.get_pressed()[0]: # detect release and run execute_clicked()
            self.is_clicked = False
            self.execute_clicked((mx, my))
        
    def execute_clicked(self, position_on_release):
        if self.show_full_item_management: # whether to even run at all
            swap_index = self.get_slot_from_mouse(position_on_release)
            if swap_index is None or (self.active_slots[swap_index].allow_swap()): # allows None to be passed in and dealt with in self.full_swap()
                self.full_swap(swap_index)
            
            if swap_index is not None and not self.active_slots[swap_index].block_check_on_click:
                self.side_pannel.check_on_click(self)

            if swap_index is not None: # now check for special actions
                special_action = self.active_slots[swap_index].execute_special_action
                if special_action is not None: 
                    special_action(self)

    def full_swap(self, swap_index): # merges if possible
        if self.position_on_click is not None:
            if swap_index is not None:
                if self.active_slots[swap_index].inventory_item is None and self.active_slots[self.position_on_click].inventory_item is None:
                    if self.position_on_click == swap_index:
                        self.position_on_click = None
                    else:
                        self.position_on_click = swap_index
                else:
                    # if (
                    #     self.active_slots[swap_index].inventory_item is not None
                    #     and 
                    #     self.active_slots[self.position_on_click].inventory_item is not None
                    #     and
                    #     self.active_slots[swap_index].inventory_item.Block_Type == self.active_slots[self.position_on_click].inventory_item.Block_Type 
                    #     and 
                    #     self.active_slots[self.position_on_click].inventory_item.count_of_items < self.active_slots[self.position_on_click].inventory_item.MAX_ITEMS_IN_INVENTORY_SLOT
                    # ):
                    #     self.fill_swap_slots(swap_index)
                    # else:
                    self.swap_inventory_slots(swap_index)
            else: # if they click an invalid option it deselects
                self.position_on_click = None
        else:
            if swap_index is not None:
                self.position_on_click = swap_index

    def swap_inventory_slots(self, swap_index):
        self.active_slots[self.position_on_click].inventory_item, self.active_slots[swap_index].inventory_item = self.active_slots[swap_index].inventory_item, self.active_slots[self.position_on_click].inventory_item
        self.position_on_click = None
    
    def fill_swap_slots(self, swap_index): # not working properly right now -> needs reconnected and repaired
        available_space = self.active_slots[swap_index].inventory_item.MAX_ITEMS_IN_INVENTORY_SLOT - self.active_slots[swap_index].inventory_item.count_of_items
        if self.active_slots[self.position_on_click].inventory_item.count_of_items > available_space:
            # needs split
            count_to_send = min(self.active_slots[self.position_on_click].inventory_item.count_of_items, available_space - self.active_slots[self.position_on_click].inventory_item.count_of_items)
            self.active_slots[swap_index].inventory_item.count_of_items += count_to_send
            if count_to_send >= available_space:
                self.active_slots[self.position_on_click].inventory_item = None
            else:
                self.active_slots[self.position_on_click].inventory_item.count_of_items -= count_to_send
        else:
            # can just fill and empty
            self.active_slots[swap_index].inventory_item.count_of_items += self.active_slots[self.position_on_click].inventory_item.count_of_items
            self.active_slots[self.position_on_click].inventory_item = None
        
        self.position_on_click = None

    def get_slot_from_mouse(self, mouse_position):
        for i in range(len(self.active_slots)):
            if self.active_slots[i].isClicked(mouse_position):
                return i
        return None


# -------------------------------------------- item management moving items -------------------------------------------- #

    def set_active_slots(self):
        self.active_slots = []
        for slot in self.expanded_inventory: 
            self.active_slots.append(slot)
        if self.side_pannel is None: return
        for slot in self.side_pannel.get_slots():
            self.active_slots.append(slot)


# -------------------------------------------------- drawing methods -------------------------------------------------- #

    def draw_item_in_slot(self, slot):
        # now draw the item into the slot
        item = slot.inventory_item

        if item is not None:
            if isinstance(item, Inventory_Item):
                item.Block_Type.draw_manual(
                    self.screen, 
                    slot.item_frame.x,
                    slot.item_frame.y,
                    slot.item_frame.width,
                    is_grid_coordinates = False # set to draw by pixel
                )

                text_surface = self.full_inventory_font.render(f"x{item.count_of_items}", True, self.inventory_text_color)
                self.screen.blit(
                    text_surface, 
                    (
                        slot.item_frame.x, 
                        slot.item_frame.y
                    ) 
                )
            elif isinstance(item, Special_Slot_Polygon):
                item.draw(self.screen, False)
            elif isinstance(item, Recipe_Slot_Contents):
                item.draw(self.screen)

    def draw_item_label(self, slot, is_hot_bar=False):
        # draw labels
        if slot.label_rect is None or slot.inventory_item is None:
            return
        
        # 1. Render the text surface
        if is_hot_bar:
            font = self.hot_bar_name_font
        else:
            font = self.inventory_item_name_font
        text_surface = font.render(
            slot.inventory_item.Block_Type.str_name,
            True,
            self.slot_label_color
        )
        

        # 2. Get text rect
        text_rect = text_surface.get_rect()

        # 3. Center it inside label box
        text_rect.center = slot.label_rect.center

        # 4. Blit
        self.screen.blit(text_surface, text_rect)



    def draw_hot_bar(self):
        # draw background
        pygame.draw.rect(self.screen, self.hot_bar_background_color, self.inventory_background)

        # draw inventory
        for i in range(self.items_in_hot_bar):
            
            if self.show_full_item_management:
                if i == self.position_on_click: cur_color = self.selected_box_color
                else: cur_color = self.base_box_color
            else:
                if i == self.cur_position_index: cur_color = self.selected_box_color
                else: cur_color = self.base_box_color

            pygame.draw.rect(
                self.screen,
                cur_color,
                self.expanded_inventory[i].hit_box 
            )

            self.draw_item_in_slot(self.expanded_inventory[i])

            if self.show_full_item_management:
                self.draw_item_label(self.expanded_inventory[i], True)

    def draw_expanded_item_management(self):
        # draw background
        pygame.draw.rect(
            self.screen,
            self.item_mng_background_color,
            self.item_mng_background
        )

        # draw label
        self.screen.blit(self.inventory_label_text_surface, self.inventory_label_rect)

        self.draw_side_pannel()

        self.draw_slots()

    def draw_slots(self): # draws all slots EXCEPT those in the hot bar
        # draw expanded inventory
        for i in range(self.items_in_hot_bar, len(self.active_slots)):
            if i == self.position_on_click: cur_color = self.selected_box_color
            else: cur_color = self.base_box_color

            if self.active_slots[i].get_special_color() is not None:
                cur_color = self.active_slots[i].get_special_color()

            pygame.draw.rect(
                self.screen,
                cur_color,
                self.active_slots[i].hit_box
            )
            self.draw_item_in_slot(self.active_slots[i])
            self.draw_item_label(self.active_slots[i])

    def draw_side_pannel(self):
        pygame.draw.rect(
            self.screen,
            self.side_pannel_background_color,
            self.side_pannel_background
        )

        if self.side_pannel.title_label_text_surface is not None and self.side_pannel.section_label_rect is not None:
            # draw the label here
            self.screen.blit(self.side_pannel.title_label_text_surface, self.side_pannel.section_label_rect)

        self.side_pannel.draw(self) # draws all special things that don't work in the normal context of what I'm doing

    def draw(self):
        self.draw_hot_bar()
        if self.show_full_item_management: self.draw_expanded_item_management()


# extra functions to be added (misc)

    def clear_selected_slot_full_inventory(self):
        self.selected_coordinates = None

    def scroll_change_inventory_position(self, scroll_change):
        scroll_change *= -1 # reverses order to make it feel more natural
        self.cur_scroll_position += scroll_change
        position = self.cur_scroll_position // self.scrolls_per_inventory_slot
        position %= self.items_in_hot_bar
        self.cur_position_index = position

    def increment_cur_position(self, is_positive=True):
        if is_positive:
            if self.cur_position_index == self.items_in_hot_bar - 1:
                self.cur_position_index = 0
            else:
                self.cur_position_index += 1
        else:
            if self.cur_position_index == 0:
                self.cur_position_index = self.items_in_hot_bar - 1
            else:
                self.cur_position_index -= 1


# --------------------------------------------- open and close functions --------------------------------------------- #

    def open(self, side_pannel_use=None):
        self.show_full_item_management = True
        if side_pannel_use is None:
            self.side_pannel = self.default_side_pannel
        self.set_active_slots()

    def open_chest(self, chest_items):
        self.show_full_item_management = True
        self.side_pannel = self.chest_side_pannel
        self.side_pannel.fill_on_open(chest_items)
        self.set_active_slots()

    def is_open(self):
        return self.show_full_item_management

    def close(self):
        self.show_full_item_management = False
        self.clear_selected_slot_full_inventory()
        self.side_pannel.close(self)
        self.position_on_click = None


# -------------------------------------------------- run functions -------------------------------------------------- #

    def run(self, input):
        # process clicks
        self.check_click(input.mouse, input.virtual_mouse_x, input.virtual_mouse_y)

        # get scrolling for switching inventory
        if self.show_full_item_management: # don't run if items management is operating            
            # close inventory
            if input.e_keypress or input.escape_keypress:
                self.close()


        else:
            if abs(input.scroll_change) > 0:
                self.scroll_change_inventory_position(input.scroll_change)
                input.scroll_change = 0

            # allow rotating inventory using keyboard
            if input.return_keypress:
                if input.l_shift_hold > 0 or input.r_shift_hold > 0:
                    self.increment_cur_position(False)
                else:
                    self.increment_cur_position(True)
            # open the full inventory
            if input.e_keypress:
                self.open()



class Inventory_Position:
    def __init__(self, hit_box, item_frame, can_allow_swap=True, execute_special_action=None, label_rect=None, inventory_item = None, special_color=None, special_color_2=None, block_check_on_click=False):
        self.hit_box = hit_box
        self.item_frame = item_frame
        self.label_rect = label_rect
        self.inventory_item = inventory_item

        self.can_allow_swap = can_allow_swap

        self.execute_special_action = execute_special_action

        self.special_color = special_color
        self.special_color_2 = special_color_2

        self.block_check_on_click = block_check_on_click

    def isClicked(self, position_on_release):
        if self.hit_box is None: return False
        return self.hit_box.collidepoint(position_on_release)
    
    def get_special_color(self):
        return self.special_color
    
    def allow_swap(self):
        return self.can_allow_swap
    
class Recipe_Slot_Contents:
    def __init__(self, main_rect, block_rect, recipe, outline_width, valid_recipe_color, invalid_recipe_color):
        self.main_rect = main_rect
        self.block_rect = block_rect
        self.recipe = recipe
        self.is_recipe_valid = False
        self.outline_width = outline_width
        self.valid_recipe_color = valid_recipe_color
        self.invalid_recipe_color = invalid_recipe_color

    def set_recipe(self, cur_recipe):
        self.recipe = cur_recipe
        if cur_recipe is not None:
            self.is_recipe_valid = True
        else:
            self.is_recipe_valid = False

    def draw(self, screen):
        if self.is_recipe_valid:
            color = self.valid_recipe_color
        else:
            color = self.invalid_recipe_color

        pygame.draw.rect(
            screen,
            color,
            self.main_rect,
            self.outline_width
        )

        if self.recipe is not None:
            block_type = self.recipe.output.block_type
            block_type.draw_manual(
                    screen, 
                    self.block_rect.x,
                    self.block_rect.y,
                    self.block_rect.width,
                    is_grid_coordinates = False # set to draw by pixel
                )
            
class Special_Slot_Polygon:
    def __init__(self, special_img_polygon, color, selected_color=None, outline_width=0):
        self.special_img_polygon = special_img_polygon
        self.color = color
        self.selected_color = selected_color
        self.outline_width = outline_width

    def draw(self, screen, invalid_color=False): # all borrowed so it draws like a block
        if invalid_color:
            cur_color = self.selected_color
        else:
            cur_color = self.color

        pygame.draw.polygon(
            screen,
            cur_color,
            self.special_img_polygon,
            width=self.outline_width
        )

class Crafting_Slots:
    def __init__(self, input_slots):

        def can_craft_more(inventory_object):

            req_list = inventory_object.crafting_object.possible_crafting_recipes[inventory_object.crafting_object.cur_recipe_index].requirement_list
            crafting_slots = inventory_object.crafting_object.crafting_input_slots

            passed_requirement = False
            for requirement in req_list:
                for input_item in crafting_slots:
                    if input_item.inventory_item is not None and input_item.inventory_item.Block_Type == requirement.block_type:
                        if input_item.inventory_item.count_of_items >= requirement.count:
                            passed_requirement = True
                            break
                if not passed_requirement:
                    inventory_object.crafting_object.check_on_click(inventory_object)

        def recipe_on_click(inventory_object):
            # step 1: make sure there is a recipe selected
            if len(inventory_object.crafting_object.possible_crafting_recipes) == 0: return

            # step 2: remove materials from slots based on recipe
            if self.cur_recipe_index >= len(inventory_object.crafting_object.possible_crafting_recipes): self.cur_recipe_index = 0  # protects against a bad index
            
            selected_recipe = inventory_object.crafting_object.possible_crafting_recipes[self.cur_recipe_index]
            output_object = inventory_object.crafting_object.output_slot.inventory_item
            if output_object is not None and (selected_recipe.output.block_type != output_object.Block_Type or output_object.count_of_items + selected_recipe.output.count > output_object.MAX_ITEMS_IN_INVENTORY_SLOT):
                return
            for recipe_item in selected_recipe.requirement_list:
                removed_item = False
                for slot in self.crafting_input_slots:
                    if isinstance(slot.inventory_item, Inventory_Item) and slot.inventory_item.Block_Type == recipe_item.block_type:
                        if slot.inventory_item.count_of_items >= recipe_item.count:
                            slot.inventory_item.count_of_items -= recipe_item.count
                            if slot.inventory_item.count_of_items == 0:
                                slot.inventory_item = None
                            removed_item = True
                            break
                if not removed_item:
                    return
                
            if inventory_object.crafting_object.output_slot.inventory_item is None:
                inventory_object.crafting_object.output_slot.inventory_item = Inventory_Item(selected_recipe.output.block_type, selected_recipe.output.count)
            else:
                inventory_object.crafting_object.output_slot.inventory_item.add_block(selected_recipe.output.count)

            # runs on click if the recipe is not longer valid
            can_craft_more(inventory_object)

        def output_onclick(inventory_object):
            # stop selection if empty
            if inventory_object.crafting_object.output_slot.inventory_item is None: return

            # step 2: use the inventory_object's add_item object to throw it in to the inventory!
            for i in range(inventory_object.crafting_object.output_slot.inventory_item.count_of_items):
                inventory_object.add_item(inventory_object.crafting_object.output_slot.inventory_item.Block_Type)
            inventory_object.crafting_object.output_slot.inventory_item = None

        def inc_recipe_up(inventory_object):
            if len(self.possible_crafting_recipes) > 0:
                if self.cur_recipe_index == 0:
                    self.cur_recipe_index = len(self.possible_crafting_recipes) - 1
                else:
                    self.cur_recipe_index -= 1

            if len(self.possible_crafting_recipes) > 0:
                self.recipe_slot.inventory_item.set_recipe(self.possible_crafting_recipes[self.cur_recipe_index])
            else:
                self.recipe_slot.inventory_item.set_recipe(None)

        def inc_recipe_down(inventory_object):
            if len(self.possible_crafting_recipes) > 0:
                if self.cur_recipe_index == len(self.possible_crafting_recipes) - 1:
                    self.cur_recipe_index = 0
                else:
                    self.cur_recipe_index += 1

            if len(self.possible_crafting_recipes) > 0:
                self.recipe_slot.inventory_item.set_recipe(self.possible_crafting_recipes[self.cur_recipe_index])
            else:
                self.recipe_slot.inventory_item.set_recipe(None)

        self.crafting_input_slots = []
        for i in range(input_slots):
            self.crafting_input_slots.append(Inventory_Position(None, None))
        self.recipe_slot = Inventory_Position(None, None, False, recipe_on_click)
        self.output_slot = Inventory_Position(None, None, False, output_onclick)
        self.point_up_slot = Inventory_Position(None, None, False, inc_recipe_up, special_color=(145, 150, 155), block_check_on_click=True)
        self.point_down_slot = Inventory_Position(None, None, False, inc_recipe_down, special_color=(145, 150, 155), block_check_on_click=True)

        self.title_label_text_surface = None
        self.section_label_rect = None

        self.craft_label_text_surface = None
        self.craft_label_rect = None

        self.collect_label_text_surface = None
        self.collect_label_rect = None

        self.recipe_name_text_surface = None
        self.recipe_name_rect = None

        self.needed_slots = 5

        self.possible_crafting_recipes = []

        self.cur_recipe_index = 0

        self.crafting_recipes = [
            Crafting_Recipe(
                "Dirt",
                [
                    Ingredient(Grass, 1)
                ],
                output=Ingredient(Dirt, 1)
            ),
            Crafting_Recipe(
                "Chest",
                [
                    Ingredient(Wood_Planks, 6), 
                    Ingredient(Iron_Ingot, 1)
                ],
                output=Ingredient(Chest, 1)
            ),
            Crafting_Recipe(
                "Iron Ore Ingot",
                [
                    Ingredient(Iron_Ore_Block, 1),
                ],
                output=Ingredient(Iron_Ingot, 1)
            ),
            Crafting_Recipe(
                "Gold Ore Ingot",
                [
                    Ingredient(Gold_Ore_Block, 1),
                ],
                output=Ingredient(Gold_Ingot, 1)
            ),
            Crafting_Recipe(
                "Gravel",
                [
                    Ingredient(Rock, 1),
                ],
                output=Ingredient(Gravel, 2)
            ),
            Crafting_Recipe(
                "Door",
                [
                    Ingredient(Wood_Planks, 3),
                ],
                output=Ingredient(Door, 2)
            ),
            Crafting_Recipe(
                "Wood Planks",
                [
                    Ingredient(Log, 1),
                ],
                output=Ingredient(Wood_Planks, 3)
            ),
            Crafting_Recipe(
                "Sulfur Powder",
                [
                    Ingredient(Sulfur_Flakes_Block, 3),
                ],
                output=Ingredient(Sulfur_Powder, 1)
            ),
            Crafting_Recipe(
                "Saltpeter Powder",
                [
                    Ingredient(Saltpeter, 1),
                ],
                output=Ingredient(Saltpeter_Powder, 5)
            ),
            Crafting_Recipe(
                "Coal",
                [
                    Ingredient(Coal_Ore_Block, 1),
                ],
                output=Ingredient(Coal, 1)
            ),
            Crafting_Recipe(
                "Gun Powder",
                [
                    Ingredient(Saltpeter_Powder, 7),
                    Ingredient(Coal, 2),
                    Ingredient(Sulfur_Powder, 1),
                ],
                output=Ingredient(Gunpowder, 1)
            ),
            Crafting_Recipe(
                "TNT",
                [
                    Ingredient(Gunpowder, 4),
                    Ingredient(Gravel, 1),
                ],
                output=Ingredient(TNT, 1)
            ),
        ]

    def close(self, inventory_object):
        for slot in self.crafting_input_slots:
            if slot.inventory_item is not None:
                for i in range(slot.inventory_item.count_of_items):
                    inventory_object.add_item(slot.inventory_item.Block_Type)
                slot.inventory_item = None
            
        self.possible_crafting_recipes = []
        self.recipe_slot.inventory_item.set_recipe(None) 
        self.cur_recipe_index = 0

        if self.output_slot.inventory_item is not None:
            for i in range(self.output_slot.inventory_item.count_of_items):
                inventory_object.add_item(self.output_slot.inventory_item.Block_Type)
            self.output_slot.inventory_item = None

    def get_cur_recipe(self):
        if self.cur_recipe_index is None or len(self.possible_crafting_recipes) == 0:
            return None
        else:
            return self.possible_crafting_recipes[self.cur_recipe_index]

    def has_enough_blocks(self, block_type, count_required, only_check_slot_index = None):
        if only_check_slot_index is None:
            for slot in self.crafting_input_slots:
                if slot.inventory_item is not None:
                    if block_type == slot.inventory_item.Block_Type and slot.inventory_item.count_of_items >= count_required:
                        return True
            return False
        else:
            slot = self.crafting_input_slots[only_check_slot_index]
            if slot.inventory_item is not None:
                if block_type == slot.inventory_item.Block_Type and slot.inventory_item.count_of_items >= count_required:
                    return True
            return False

    def get_possible_recipes(self):
        possible_crafting_recipes = []
        for recipe in self.crafting_recipes:
            has_all_ingredients = True
            for required_ingredient in recipe.requirement_list:
                # seach through slots in self.crafting_input_slots
                if not self.has_enough_blocks(required_ingredient.block_type, required_ingredient.count):
                    has_all_ingredients = False
                    break
            if has_all_ingredients: possible_crafting_recipes.append(recipe)

        return possible_crafting_recipes

    def check_on_click(self, inventory_object): # this figures out what recipes apply on each click
        
        self.possible_crafting_recipes = self.get_possible_recipes()

        # reset the active index if it is out of range (otherwise don't touch it)
        if self.cur_recipe_index >= len(self.possible_crafting_recipes): self.cur_recipe_index = 0

        if len(self.possible_crafting_recipes) > 0:
            self.recipe_slot.inventory_item.set_recipe(self.possible_crafting_recipes[self.cur_recipe_index])
        else:
            self.recipe_slot.inventory_item.set_recipe(None)
        

        # for recipe in self.possible_crafting_recipes:
        #     print(recipe.name)
        # print("")

    def get_slots(self):
        i = 0
        return_slots = []
        for i in range(len(self.crafting_input_slots)):
            return_slots.append(self.crafting_input_slots[i])
        return_slots.append(self.recipe_slot)
        return_slots.append(self.output_slot)
        return_slots.append(self.point_up_slot)
        return_slots.append(self.point_down_slot)

        return return_slots

    def draw(self, inventory_object):
        pipe_color = {}

        if len(self.possible_crafting_recipes) > 0:

            cur_slot_index = 0
            input0_active = False
            if self.crafting_input_slots[cur_slot_index].inventory_item is not None:
                found_block = False
                for req in self.possible_crafting_recipes[inventory_object.crafting_object.cur_recipe_index].requirement_list:
                    if req.block_type == self.crafting_input_slots[cur_slot_index].inventory_item.Block_Type:
                        found_block = True
                        input0_active = self.crafting_input_slots[cur_slot_index].inventory_item is not None and self.has_enough_blocks(req.block_type, req.count, cur_slot_index)
                if not found_block:
                    input0_active = False
            else:
                input0_active = False

            cur_slot_index = 2
            input2_active = False
            if self.crafting_input_slots[cur_slot_index].inventory_item is not None:
                found_block = False
                for req in self.possible_crafting_recipes[inventory_object.crafting_object.cur_recipe_index].requirement_list:
                    if req.block_type == self.crafting_input_slots[cur_slot_index].inventory_item.Block_Type:
                        found_block = True
                        input2_active = self.crafting_input_slots[cur_slot_index].inventory_item is not None and self.has_enough_blocks(req.block_type, req.count, cur_slot_index)
                if not found_block:
                    input2_active = False
            else:
                input2_active = False
            
            cur_slot_index = 1
            input_1_active = False
            if self.crafting_input_slots[cur_slot_index].inventory_item is not None:
                found_block = False
                for req in self.possible_crafting_recipes[inventory_object.crafting_object.cur_recipe_index].requirement_list:
                    if req.block_type == self.crafting_input_slots[cur_slot_index].inventory_item.Block_Type:
                        found_block = True
                        input_1_active = self.crafting_input_slots[cur_slot_index].inventory_item is not None and self.has_enough_blocks(req.block_type, req.count, cur_slot_index)
                if not found_block:
                    input_1_active = False
            else:
                input_1_active = False


            if input0_active:
                pipe_color[0] = inventory_object.pipe_color_active

            if input2_active:
                pipe_color[1] = inventory_object.pipe_color_active

            if input0_active or input2_active or input_1_active:
                pipe_color[2] = inventory_object.pipe_color_active

                if self.output_slot.inventory_item is not None:
                    pipe_color[3] = inventory_object.pipe_color_active

        cur_recipes = inventory_object.crafting_object.get_possible_recipes()
        cur_index = inventory_object.crafting_object.cur_recipe_index
        if cur_index is not None and len(cur_recipes) > 0:
            cur_recipe = cur_recipes[cur_index]
            output_object = inventory_object.crafting_object.output_slot.inventory_item
            if output_object is not None and (cur_recipe.output.block_type != output_object.Block_Type or output_object.count_of_items + cur_recipe.output.count > output_object.MAX_ITEMS_IN_INVENTORY_SLOT):
                pipe_color[3] = inventory_object.pipe_color_inactive
             
        
        for i in range(len(inventory_object.crafting_flow_rects)):
            pipe_color[i] = pipe_color.get(i, inventory_object.pipe_color_inactive)

        i = 0
        for rect in inventory_object.crafting_flow_rects:
            pygame.draw.rect(inventory_object.screen, pipe_color[i], rect)
            i+=1

        # ----------------------------- custom crafting labels ----------------------------- #

        screen = inventory_object.screen

        # static labels
        if self.craft_label_text_surface is not None and self.craft_label_rect is not None:
            screen.blit(self.craft_label_text_surface, self.craft_label_rect)

        if self.collect_label_text_surface is not None and self.collect_label_rect is not None:
            screen.blit(self.collect_label_text_surface, self.collect_label_rect)

        # dynamic recipe name (above center slot up arrow)
        if self.recipe_name_rect is not None:

            cur_recipe = self.get_cur_recipe()

            if cur_recipe is not None:
                recipe_name = cur_recipe.name
            else:
                recipe_name = "None"

            # render the two lines
            recipe_label_surface = inventory_object.inventory_item_name_font.render(
                "Recipe:",
                True,
                inventory_object.slot_label_color
            )

            recipe_name_surface = inventory_object.inventory_item_name_font.render(
                recipe_name,
                True,
                inventory_object.slot_label_color
            )

            # position them
            recipe_label_rect = recipe_label_surface.get_rect(
                center=(self.recipe_name_rect.centerx, self.recipe_name_rect.centery - self.recipe_name_rect.height // 4)
            )

            recipe_name_rect = recipe_name_surface.get_rect(
                center=(self.recipe_name_rect.centerx, self.recipe_name_rect.centery + self.recipe_name_rect.height // 4)
            )

            # draw
            screen.blit(recipe_label_surface, recipe_label_rect)
            screen.blit(recipe_name_surface, recipe_name_rect)

class Chest_Slots:
    def __init__(self, count_chest_slots):
        self.chest_slots = []
        for i in range(count_chest_slots):
            self.chest_slots.append(Inventory_Position(None, None))
        self.chest_slot_items = None

        self.title_label_text_surface = None
        self.section_label_rect = None

    def fill_on_open(self, chest_slot_items):
        self.chest_slot_items = chest_slot_items
        for i in range(len(self.chest_slots)):
            if i >= len(chest_slot_items):
                chest_slot_items.append(None)
            self.chest_slots[i].inventory_item = chest_slot_items[i]

    def close(self, inventory_object):
        if self.chest_slot_items is not None:
            i = 0
            for slot in self.chest_slots:
                self.chest_slot_items[i] = slot.inventory_item
                i+=1

    def check_on_click(self, inventory_object):
        pass

    def get_slots(self):
        return self.chest_slots

    def draw(self, inventory_object):
        pass
