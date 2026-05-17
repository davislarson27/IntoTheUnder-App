import pygame

from ..inventory_position import Inventory_Position
from ..inventory_item import Inventory_Item


class Fuel_Slots:
    def __init__(self, screen=None):
        self.fuel_slots = [Inventory_Position(None, None), Inventory_Position(None, None)]

        self.title_label_text_surface = None
        self.section_label_rect       = None

        self.pipe_rects          = []
        self.pipe_color_inactive = (115, 115, 130)
        self.pipe_color_active   = (135, 170, 145)

        self.refuel_label_surface = None
        self.refuel_label_rect    = None
        self.repair_label_surface = None
        self.repair_label_rect    = None

        action_color = (75, 75, 85)
        self.pause_slot_0 = Inventory_Position(None, None, False, None, special_color=action_color)
        self.use_slot_0   = Inventory_Position(None, None, False, None, special_color=action_color)
        self.pause_slot_1 = Inventory_Position(None, None, False, None, special_color=action_color)
        self.use_slot_1   = Inventory_Position(None, None, False, None, special_color=action_color)

    def get_slots(self):
        return self.fuel_slots + [
            self.pause_slot_0, self.use_slot_0,
            self.pause_slot_1, self.use_slot_1,
        ]

    def check_on_click(self, inventory_object):
        pass

    def draw(self, inventory_object):
        screen = inventory_object.screen

        for i, rect in enumerate(self.pipe_rects):
            has_item = self.fuel_slots[i].inventory_item is not None
            color = self.pipe_color_active if has_item else self.pipe_color_inactive
            pygame.draw.rect(screen, color, rect)

        if self.refuel_label_surface and self.refuel_label_rect:
            screen.blit(self.refuel_label_surface, self.refuel_label_rect)
        if self.repair_label_surface and self.repair_label_rect:
            screen.blit(self.repair_label_surface, self.repair_label_rect)

    def close(self, inventory_object):
        for slot in self.fuel_slots:
            if slot.inventory_item is not None:
                for _ in range(slot.inventory_item.count_of_items):
                    inventory_object.add_item(slot.inventory_item.Block_Type)
                slot.inventory_item = None
    