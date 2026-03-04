import pygame
from blocks import *

class Inventory:
    MAX_ITEMS = 8

    def __init__(self, screen, SCREEN_HEIGHT, SCREEN_WIDTH, INVENTORY_HEIGHT):
        self.screen = screen
        self.SCREEN_HEIGHT = SCREEN_HEIGHT
        self.SCREEN_WIDTH = SCREEN_WIDTH
        self.INVENTORY_HEIGHT = INVENTORY_HEIGHT

        self.full_inventory = [None for x in range(8)]
        self.cur_position_index = 0

        self.show_full_inventory = False

        # object sizes
        self.tot_columns = 24
        self.tot_rows = 24
        
        self.row_width = self.SCREEN_WIDTH // self.tot_columns
        self.column_height = (self.SCREEN_HEIGHT  - self.INVENTORY_HEIGHT) // self.tot_rows

        self.boxes_per_row = 8
        self.boxes_high = 4
        self.box_side_length = 3 * self.column_height # boxes are 2 columns high and 2 columns wide

        self.margin_x = 3 * self.row_width
        self.margin_y = 3 * self.column_height

        self.margin_between_boxes_x = (self.SCREEN_WIDTH - (2 * self.margin_x) - (self.boxes_per_row * self.box_side_length)) // (self.boxes_per_row - 1)
        self.margin_between_boxes_y = (self.SCREEN_HEIGHT  - self.INVENTORY_HEIGHT - (2 * self.margin_y) - (self.boxes_high * self.box_side_length)) // (self. boxes_high - 1)
    


    def run_full(self, mouse):
        if mouse.get_pressed()[0]:
            m_x, m_y = mouse.get_pos()

    def add_item(self, item):
        empty_slot = None
        for i in range(len(self.full_inventory)):
            if self.full_inventory[i] != None and item == self.full_inventory[i].Block_Type:
                self.full_inventory[i].add_block()
                return
            if empty_slot == None and self.full_inventory[i] == None: empty_slot = i

        if empty_slot == None:
            if len(self.full_inventory) < self.MAX_ITEMS:
                self.full_inventory.append(Inventory_Position(item))
        else:
            self.full_inventory[empty_slot] = Inventory_Position(item)

    def build_from_current(self):
        cur_inventory_slot = self.full_inventory[self.cur_position_index]
        if cur_inventory_slot != None:
            block_type = cur_inventory_slot.Block_Type
            if cur_inventory_slot.remove_block():
                if cur_inventory_slot.count_of_items == 0:
                    self.full_inventory[self.cur_position_index] = None
            return block_type
        return None
    
    def set_cur_position(self, index):
        self.cur_position_index = index

    def select_click(self, x, y):
        spacing_x = self.SCREEN_WIDTH // 10
        spacing_y = self.INVENTORY_HEIGHT // 12
        INVENTORY_BLOCK_WIDTH = (spacing_x // 12) * 8

        if y > self.SCREEN_HEIGHT - self.INVENTORY_HEIGHT + (spacing_y * 2) and y < self.SCREEN_HEIGHT - (spacing_y * 2):
            x_margin = spacing_x + (spacing_x // 12)
            if x > x_margin and x + x_margin < self.SCREEN_WIDTH:
                return (x // spacing_x) - 1
        return None

    def increment_cur_position(self, is_positive = True):
        if is_positive:
            if self.cur_position_index == self.MAX_ITEMS - 1:
                self.cur_position_index = 0
            else:
                self.cur_position_index += 1
        else:
            if self.cur_position_index == 0:
                self.cur_position_index = self.MAX_ITEMS - 1
            else:
                self.cur_position_index -= 1

    def get_x_start_for_box(self, box_number): # box 0 should be the first box
        return self.margin_x + (box_number * (self.box_side_length + self.margin_between_boxes_x))
    
    def get_y_start_for_box(self, box_number):
        return self.margin_y + (box_number * (self.box_side_length + self.margin_between_boxes_y))

    def draw(self):
        font = pygame.font.Font(None, 36)  # None = default font, 36 = size

        pygame.draw.rect( # draw base color
            self.screen,
            (50, 50, 50),           # color
            (0, self.SCREEN_HEIGHT - self.INVENTORY_HEIGHT, self.SCREEN_WIDTH, self.INVENTORY_HEIGHT)
        )
        spacing_x = self.SCREEN_WIDTH // 10
        margin_x = 2 * spacing_x // 12
        INVENTORY_BLOCK_WIDTH = (spacing_x // 12) * 8 # this means that there is 2 / 12 of margins on each side
        spacing_y = self.INVENTORY_HEIGHT // 12

        
        for i in range(1, 9):
            background_color = 200
            if i - 1 == self.cur_position_index:
                background_color += 50
            pygame.draw.rect(
                self.screen,
                (background_color, background_color, background_color),
                ((i * spacing_x) + margin_x, self.SCREEN_HEIGHT - self.INVENTORY_HEIGHT + (spacing_y * 2), INVENTORY_BLOCK_WIDTH, spacing_y * 8)
            )
            inventory_index = i - 1
            if inventory_index < len(self.full_inventory):
                tenth_of_width = INVENTORY_BLOCK_WIDTH // 10

                x = (i * spacing_x) + (2 * spacing_x // 12) + tenth_of_width
                y = (spacing_y * 2) + tenth_of_width
                width = tenth_of_width * 8

                if self.full_inventory[inventory_index] != None: 
                    self.full_inventory[inventory_index].Block_Type.draw_manual(self.screen, x, self.SCREEN_HEIGHT - self.INVENTORY_HEIGHT + y, width, is_grid_coordinates = False)

                    text_surface = font.render(f"x{self.full_inventory[inventory_index].count_of_items}", True, (255, 255, 255))
                    self.screen.blit(text_surface, (x, self.SCREEN_HEIGHT - self.INVENTORY_HEIGHT + y) )


        if self.show_full_inventory:
            # draw background for inventory (maybe)
            # background_inventory_color = 

            # draw boxes
            base_box_color = (200, 200, 200)
            selected_box_color = (15, 15, 15)
            for box_number in range(self.boxes_per_row):
                for box_height in range(self.boxes_high):
                    box_dimentions = (
                        self.get_x_start_for_box(box_number),
                        self.get_y_start_for_box(box_height),
                        self.box_side_length,
                        self.box_side_length
                    )
                    pygame.draw.rect(
                        self.screen,
                        base_box_color,
                        box_dimentions
                    )

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
    def fill_from_dict(inventory_dict, screen, SCREEN_HEIGHT, SCREEN_WIDTH, INVENTORY_HEIGHT):
        # create new inventory
        inventory = Inventory(screen, SCREEN_HEIGHT, SCREEN_WIDTH, INVENTORY_HEIGHT)

        # get block conversion dictionary and list of slots
        str_to_block = get_str_to_block()
        inventory_items = inventory_dict["inventory_items"]

        # get position
        inventory.cur_position_index = inventory_dict["cur_position_index"]

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
        self.Block_Type = Block_Type
        self.count_of_items = count_of_items

    def add_block(self):
        self.count_of_items += 1

    def remove_block(self):
        if self.count_of_items > 0:
            self.count_of_items -= 1
            return True
        return False