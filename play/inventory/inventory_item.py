from world.blocks.block_export import get_str_to_block

class Inventory_Item:

    def __init__(self, Block_Type, count_of_items = 1):
        self.MAX_ITEMS_IN_INVENTORY_SLOT = 99

        self.Block_Type = Block_Type
        self.count_of_items = count_of_items

    def can_add(self):
        if self.count_of_items < self.MAX_ITEMS_IN_INVENTORY_SLOT:
            return True
        else:
            return False

    def add_block(self, blocks_added=1):
        if self.count_of_items < self.MAX_ITEMS_IN_INVENTORY_SLOT:
            self.count_of_items += blocks_added
            return True
        else:
            return False

    def remove_block(self):
        if self.count_of_items > 0:
            self.count_of_items -= 1
            return True
        return False

    def rerender_as_array(self):
        return [self.Block_Type.str_name, self.count_of_items]
    
    @staticmethod
    def create_from_array(array):
        block_str_dict = get_str_to_block()
        return Inventory_Item(block_str_dict[array[0]], array[1])