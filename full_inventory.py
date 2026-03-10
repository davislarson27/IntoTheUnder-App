import pygame
from blocks import *

class Inventory:

    def __init__(self, screen, window, INVENTORY_HEIGHT, HEALTH_BAR_HEIGHT = 25, cur_position_index = 0):
        self.screen = screen
        
        self.window = window # use for width and height when dealing with mouse clicks
        self.INVENTORY_HEIGHT = INVENTORY_HEIGHT - HEALTH_BAR_HEIGHT
        self.HEALTH_BAR_HEIGHT = HEALTH_BAR_HEIGHT

        self.show_full_inventory = False

        # object sizes
        self.tot_columns = 24
        self.tot_rows = 24
        
        self.row_width = screen.get_width() // self.tot_columns
        self.column_height = (screen.get_height()  - self.INVENTORY_HEIGHT) // self.tot_rows

        self.boxes_per_row = 8
        self.boxes_high = 4
        # possibly force this number to be even for box_size_length
        self.box_side_length = 3 * self.column_height # boxes are 2 columns high and 2 columns wide

        self.margin_x = 3 * self.row_width
        self.margin_y = 3 * self.column_height

        self.margin_between_boxes_x = (screen.get_width() - (2 * self.margin_x) - (self.boxes_per_row * self.box_side_length)) // (self.boxes_per_row - 1)
        self.margin_between_boxes_y = (screen.get_height()  - self.INVENTORY_HEIGHT - (2 * self.margin_y) - (self.boxes_high * self.box_side_length)) // (self. boxes_high - 1)
    
        self.item_percent_of_box = 0.75
        self.full_inventory_item_size = floor(self.box_side_length * self.item_percent_of_box) # item is 90% as long as its box is
        self.full_inventory_item_margin = floor((self.box_side_length - self.full_inventory_item_size) / 2)

        self.hot_bar_margin_y = (self.INVENTORY_HEIGHT - self.box_side_length) // 2
        self.hot_bar_y_start = self.screen.get_height() - self.hot_bar_margin_y - self.box_side_length

        # inventory contents
        self.max_items_in_inventory = (self.boxes_high + 1) * self.boxes_per_row + 1
        self.full_inventory = [None for x in range(self.max_items_in_inventory)]
        self.hot_bar_length = 8
        self.cur_position_index = cur_position_index
        
        self.scrolls_per_inventory_slot = 1
        self.cur_scroll_position = self.cur_position_index * self.scrolls_per_inventory_slot

        # initalize fonts
        self.hot_bar_font = pygame.font.Font(None, 36)  # None = default font, 36 = size
        self.percent_font_of_block_full_inventory = 0.8
        self.full_inventory_font = pygame.font.Font(None, floor(self.full_inventory_item_size * self.percent_font_of_block_full_inventory))

        # inventory nav attributes
        self.selected_coordinates = None

        # colors
        self.base_box_color = (200, 200, 200)
        self.selected_box_color = (240, 240, 240)
        self.inventory_text_color = (255, 255, 255)
        self.inventory_background_color = (50, 50, 50)


    def clear_selected_slot_full_inventory(self): # deselects items when inventory is open on closing
        self.selected_coordinates = None

    def get_inventory_position_from_coordinates(self, coordinates, offset = 0):
        x, y = coordinates[0], coordinates[1]
        # if y == self.boxes_high:
        #     return (self.boxes_per_row)
        # return (self.boxes_per_row * y) + x + offset
        return (self.boxes_per_row * y) + x

    def scroll_change_inventory_position(self, scroll_change):
        scroll_change *= -1 # reverses order to make it feel more natural
        self.cur_scroll_position += scroll_change
        position = self.cur_scroll_position // self.scrolls_per_inventory_slot
        position %= self.hot_bar_length
        self.cur_position_index = position


    def swap_positions(self, swap_coordinates):
        p1 = floor(self.get_inventory_position_from_coordinates(self.selected_coordinates, self.hot_bar_length))
        p2 = floor(self.get_inventory_position_from_coordinates(swap_coordinates, self.hot_bar_length))

        self.full_inventory[p1], self.full_inventory[p2] = self.full_inventory[p2], self.full_inventory[p1]

        self.selected_coordinates = None

    def process_click_full_inventory(self, m_x, m_y, scale = 1):
        if m_x > self.margin_x and m_x < self.screen.get_width() - self.margin_x:
            if m_y > self.margin_y and m_y < self.margin_y + ((self.box_side_length * self.boxes_high) + ((self.boxes_high - 1) * self.margin_between_boxes_y)):
                # now we are in range of the boxes - we can work on determining which box was selected
                box_position_x = (m_x - self.margin_x) // (self.box_side_length + self.margin_between_boxes_x) 
                box_position_y = (m_y - self.margin_y) // (self.box_side_length + self.margin_between_boxes_y) + 1

                # now check for valid positions
                if (m_x - self.margin_x) < ((box_position_x + 1) * self.box_side_length) + (box_position_x * self.margin_between_boxes_x) and (m_y - self.margin_y) < ((box_position_y + 1) * self.box_side_length) + (box_position_y * self.margin_between_boxes_y):
                    cur_coordinates = (box_position_x, box_position_y)

                    if self.selected_coordinates is None and self.selected_coordinates != cur_coordinates:
                        self.selected_coordinates = cur_coordinates
                    else:
                        self.swap_positions(cur_coordinates)
            
            elif m_y > self.screen.get_height() - self.INVENTORY_HEIGHT + self.hot_bar_margin_y and m_y < self.screen.get_height() - self.INVENTORY_HEIGHT + self.hot_bar_margin_y + self.box_side_length:
                box_position_x = (m_x - self.margin_x) // (self.box_side_length + self.margin_between_boxes_x) 
                if (m_x - self.margin_x) < ((box_position_x + 1) * self.box_side_length) + (box_position_x * self.margin_between_boxes_x):
                    # cur_coordinates =  (box_position_x, self.boxes_high)
                    cur_coordinates =  (box_position_x, 0)

                    if self.selected_coordinates is None and self.selected_coordinates != cur_coordinates:
                        self.selected_coordinates = cur_coordinates
                    else:
                        self.swap_positions(cur_coordinates)


    def add_item(self, item):
        empty_slot = None
        for i in range(len(self.full_inventory)):
            if self.full_inventory[i] != None and item == self.full_inventory[i].Block_Type and self.full_inventory[i].can_add():
                self.full_inventory[i].add_block()
                return
            if empty_slot == None and self.full_inventory[i] == None: empty_slot = i

        if empty_slot == None: # create new Inventory_Position object
            if len(self.full_inventory) < self.max_items_in_inventory:
                self.full_inventory.append(Inventory_Position(item))
        else:
            self.full_inventory[empty_slot] = Inventory_Position(item)

    def build_from_current(self):
        cur_inventory_slot = self.full_inventory[floor(self.cur_position_index)]
        if cur_inventory_slot != None:
            block_type = cur_inventory_slot.Block_Type
            if cur_inventory_slot.remove_block():
                if cur_inventory_slot.count_of_items == 0:
                    self.full_inventory[self.cur_position_index] = None
            return block_type
        return None

    def set_cur_position(self, index):
        self.cur_position_index = floor(index)

    def select_click(self, x, y): # needs to get redone for new inventory hot bar
        spacing_x = self.screen.get_width() // 10
        spacing_y = self.INVENTORY_HEIGHT // 12
        INVENTORY_BLOCK_WIDTH = (spacing_x // 12) * 8

        if y > self.screen.get_height() - self.INVENTORY_HEIGHT + (spacing_y * 2) and y < self.screen.get_height() - (spacing_y * 2):
            x_margin = spacing_x + (spacing_x // 12)
            if x > x_margin and x + x_margin < self.screen.get_width():
                return (x // spacing_x) - 1
        return None

    def increment_cur_position(self, is_positive = True):
        if is_positive:
            if self.cur_position_index == self.hot_bar_length - 1:
                self.cur_position_index = 0
            else:
                self.cur_position_index += 1
        else:
            if self.cur_position_index == 0:
                self.cur_position_index = self.hot_bar_length - 1
            else:
                self.cur_position_index -= 1

    def get_x_start_for_box(self, box_number): # box 0 should be the first box
        return self.margin_x + (box_number * (self.box_side_length + self.margin_between_boxes_x))

    def get_y_start_for_box(self, box_number):
        return self.margin_y + (box_number * (self.box_side_length + self.margin_between_boxes_y))

    def draw(self):

        # if self.show_full_inventory: # fills background as same color as inventory and covers the screen
        #     self.screen.fill(self.inventory_background_color)

        pygame.draw.rect( # draw base color
            self.screen,
            self.inventory_background_color,           # color
            (0, self.screen.get_height() - self.INVENTORY_HEIGHT, self.screen.get_width(), self.INVENTORY_HEIGHT)
        )


        box_height = 0
        for box_number in range(self.boxes_per_row):
            if self.show_full_inventory: # hilight selection for if the full inventory is open
                if (box_number, box_height) == self.selected_coordinates:
                    use_base_box_color = self.selected_box_color
                else:
                    use_base_box_color = self.base_box_color
            else: # hilight selection for if the inventory is not open (highlights the slot being used)
                if self.cur_position_index == box_number:
                    use_base_box_color = self.selected_box_color
                else:
                    use_base_box_color = self.base_box_color


            # draw background rectangle for inventory slot
            box_dimentions = (
                self.get_x_start_for_box(box_number),
                self.hot_bar_y_start,
                self.box_side_length,
                self.box_side_length
            )
            pygame.draw.rect(
                self.screen,
                use_base_box_color,
                box_dimentions
            )

            # now draw the item into the slot
            if self.full_inventory[box_number] is not None:
                self.full_inventory[box_number].Block_Type.draw_manual(
                    self.screen, 
                    self.get_x_start_for_box(box_number) + self.full_inventory_item_margin, # x position
                    self.hot_bar_y_start + self.full_inventory_item_margin, # y position
                    self.full_inventory_item_size, # set side size
                    is_grid_coordinates = False # set to draw by pixel
                )

                text_surface = self.full_inventory_font.render(f"x{self.full_inventory[box_number].count_of_items}", True, self.inventory_text_color)
                self.screen.blit(
                    text_surface, 
                    (
                        self.get_x_start_for_box(box_number) + self.full_inventory_item_margin, 
                        self.hot_bar_y_start + self.full_inventory_item_margin
                    ) 
                )


        if self.show_full_inventory:
            # draw background for inventory (maybe)
            # background_inventory_color = (50, 50, 50)

            # draw boxes
            inventory_item_num = self.hot_bar_length
            for height_calc_box_height in range(self.boxes_high):
                coordinate_box_height = height_calc_box_height + 1
                for box_number in range(self.boxes_per_row):
                    # select background color
                    if (box_number, coordinate_box_height) == self.selected_coordinates:
                        use_base_box_color = self.selected_box_color
                    else:
                        use_base_box_color = self.base_box_color

                    # draw background rectangle for inventory slot
                    box_dimentions = (
                        self.get_x_start_for_box(box_number),
                        self.get_y_start_for_box(height_calc_box_height),
                        self.box_side_length,
                        self.box_side_length
                    )
                    pygame.draw.rect(
                        self.screen,
                        use_base_box_color,
                        box_dimentions
                    )

                    # now draw the item into the slot
                    if self.full_inventory[inventory_item_num] is not None:
                        self.full_inventory[inventory_item_num].Block_Type.draw_manual(
                            self.screen, 
                            self.get_x_start_for_box(box_number) + self.full_inventory_item_margin, # x position
                            self.get_y_start_for_box(height_calc_box_height) + self.full_inventory_item_margin, # y position
                            self.full_inventory_item_size, # set side size
                            is_grid_coordinates = False # set to draw by pixel
                        )

                        text_surface = self.full_inventory_font.render(f"x{self.full_inventory[inventory_item_num].count_of_items}", True, self.inventory_text_color)
                        self.screen.blit(
                            text_surface, 
                            (
                                self.get_x_start_for_box(box_number) + self.full_inventory_item_margin, 
                                self.get_y_start_for_box(height_calc_box_height) + self.full_inventory_item_margin
                            ) 
                        )


                    inventory_item_num += 1


    # saving and reloading methods
    def to_dict(self):
        inventory_items = []
        for slot in self.full_inventory:
            if slot is not None: inventory_items.append([slot.Block_Type.str_name, slot.count_of_items])
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
                inventory.full_inventory[i] = Inventory_Position(block_type, block_count)

        return inventory


class Inventory_Position:

    def __init__(self, Block_Type, count_of_items = 1):
        self.MAX_ITEMS_IN_INVENTORY_SLOT = 99

        self.Block_Type = Block_Type
        self.count_of_items = count_of_items

    def can_add(self):
        if self.count_of_items < self.MAX_ITEMS_IN_INVENTORY_SLOT:
            return True
        else:
            return False

    def add_block(self):
        if self.count_of_items < self.MAX_ITEMS_IN_INVENTORY_SLOT:
            self.count_of_items += 1
            return True
        else:
            return False

    def remove_block(self):
        if self.count_of_items > 0:
            self.count_of_items -= 1
            return True
        return False
    