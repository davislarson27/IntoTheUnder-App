from .inventory_position import Inventory_Position


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
