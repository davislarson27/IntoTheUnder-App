class Inventory_Position:
    def __init__(self, hit_box, item_frame, can_allow_swap=True, execute_special_action=None, label_rect=None, inventory_item=None, special_color=None, special_color_2=None, block_check_on_click=False, allowed_items_list=None):
        self.hit_box = hit_box
        self.item_frame = item_frame
        self.label_rect = label_rect
        self.inventory_item = inventory_item

        self.can_allow_swap = can_allow_swap

        self.execute_special_action = execute_special_action

        self.special_color = special_color
        self.special_color_2 = special_color_2

        self.block_check_on_click = block_check_on_click

        self.allowed_items_list = allowed_items_list # None allows any block type to be here

    def isClicked(self, position_on_release):
        if self.hit_box is None: return False
        return self.hit_box.collidepoint(position_on_release)
    
    def get_special_color(self):
        return self.special_color
    
    def allow_swap(self, inventory_item_from):
        if self.can_allow_swap == False:
            return self.can_allow_swap
        
        elif self.allowed_items_list is None or inventory_item_from is None:
            return True
        
        else:
            if inventory_item_from.Block_Type in self.allowed_items_list:
                return True
            else:
                return False
    