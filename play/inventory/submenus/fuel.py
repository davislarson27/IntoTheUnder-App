import pygame

from ..inventory_position import Inventory_Position
from ..inventory_item import Inventory_Item
from world.blocks.block_export import *


class Fuel_Slots:
    def __init__(self, screen=None):
        self.health_bar = None

        self.refuel_bar_remaining = 0
        self.repair_bar_remaining = 0

        self.refuel_bar_max = 0
        self.repair_bar_max = 0

        self.refuel_is_paused = False
        self.repair_is_paused = False

        self.fuel_slots = [
            Inventory_Position(None, None, allowed_items_list=[block_type for block_type in get_block_refuel_dict().keys()]),
            Inventory_Position(None, None, allowed_items_list=[block_type for block_type in get_block_repair_dict().keys()])
        ]

        self.title_label_text_surface = None
        self.section_label_rect       = None

        self.pipe_rects          = []
        self.pipe_color_inactive = (115, 115, 130)
        self.pipe_color_active   = (135, 170, 145)

        self.refuel_label_surface = None
        self.refuel_label_rect    = None
        self.repair_label_surface = None
        self.repair_label_rect    = None

        def pause_refuel(inventory_object):
            self.refuel_is_paused = True

        def start_refuel(inventory_object):
            self.refuel_is_paused = False
            if self.refuel_bar_remaining <= 0:
                fuel_inventory_item_obj = self.fuel_slots[0].inventory_item
                if fuel_inventory_item_obj is not None:
                    fuel_value = get_block_refuel_values(fuel_inventory_item_obj.Block_Type)
                    self.refuel_bar_remaining = fuel_value
                    self.refuel_bar_max = fuel_value
                    fuel_inventory_item_obj.remove_block()
                    if fuel_inventory_item_obj.count_of_items <= 0:
                        self.fuel_slots[0].inventory_item = None

        def pause_repair(inventory_object):
            self.repair_is_paused = True

        def start_repair(inventory_object):
            self.repair_is_paused = False
            if self.repair_bar_remaining <= 0:
                repair_inventory_item_obj = self.fuel_slots[1].inventory_item
                if repair_inventory_item_obj is not None:
                    repair_value = get_block_repair_values(repair_inventory_item_obj.Block_Type)
                    self.repair_bar_remaining = repair_value
                    self.repair_bar_max = repair_value
                    repair_inventory_item_obj.remove_block()
                    if repair_inventory_item_obj.count_of_items <= 0:
                        self.fuel_slots[1].inventory_item = None

        action_color = (75, 75, 85)
        self.pause_slot_0 = Inventory_Position(None, None, False, pause_refuel, special_color=action_color)
        self.use_slot_0   = Inventory_Position(None, None, False, start_refuel, special_color=action_color)
        self.pause_slot_1 = Inventory_Position(None, None, False, pause_repair, special_color=action_color)
        self.use_slot_1   = Inventory_Position(None, None, False, start_repair, special_color=action_color)

        self.refuel_speed = 0.05
        self.repair_speed = 0.05

    # ------------------------------------------------------------------ #

    def set_health_bar(self, health_bar_obj):
        self.health_bar = health_bar_obj

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
            pygame.draw.rect(screen, self.pipe_color_inactive, rect)

            if i == 0 and self.refuel_bar_max > 0:
                percent = self.refuel_bar_remaining / self.refuel_bar_max
                fill_w  = int(rect.width * percent)
                if fill_w > 0:
                    fill_rect = pygame.Rect(rect.x, rect.y, fill_w, rect.height)
                    pygame.draw.rect(screen, self.pipe_color_active, fill_rect)

            elif i == 1 and self.repair_bar_max > 0:
                percent = self.repair_bar_remaining / self.repair_bar_max
                fill_w  = int(rect.width * percent)
                if fill_w > 0:
                    fill_rect = pygame.Rect(rect.x, rect.y, fill_w, rect.height)
                    pygame.draw.rect(screen, self.pipe_color_active, fill_rect)

        if self.refuel_label_surface and self.refuel_label_rect:
            screen.blit(self.refuel_label_surface, self.refuel_label_rect)
        if self.repair_label_surface and self.repair_label_rect:
            screen.blit(self.repair_label_surface, self.repair_label_rect)

        # ---- button highlight logic ---- #
        color_dim = (95, 95, 105)
        color_lit = (175, 175, 185)

        for i, (pause_slot, use_slot, is_paused) in enumerate([
            (self.pause_slot_0, self.use_slot_0, self.refuel_is_paused),
            (self.pause_slot_1, self.use_slot_1, self.repair_is_paused),
        ]):
            has_anything = (
                self.fuel_slots[i].inventory_item is not None or
                (self.refuel_bar_remaining if i == 0 else self.repair_bar_remaining) > 0
            )

            if pause_slot.inventory_item is not None:
                pause_slot.inventory_item.color = color_lit if (has_anything and not is_paused) else color_dim
            if use_slot.inventory_item is not None:
                use_slot.inventory_item.color   = color_lit if (has_anything and is_paused) else color_dim

    def close(self, inventory_object):
        pass

    # ------------------------------------------------------------------ #

    def run_passive(self):
        if self.health_bar is None:
            return

        self._run_refuel()
        self._run_repair()

    def _run_refuel(self):
        if self.refuel_is_paused:
            return
        if self.health_bar.is_energy_full():
            return

        if self.refuel_bar_remaining <= 0:
            fuel_inventory_item_obj = self.fuel_slots[0].inventory_item
            if fuel_inventory_item_obj is None:
                return
            fuel_value = get_block_refuel_values(fuel_inventory_item_obj.Block_Type)
            self.refuel_bar_remaining = fuel_value
            self.refuel_bar_max = fuel_value
            fuel_inventory_item_obj.remove_block()
            if fuel_inventory_item_obj.count_of_items <= 0:
                self.fuel_slots[0].inventory_item = None

        if self.refuel_bar_remaining > 0:
            amount = min(self.refuel_speed, self.refuel_bar_remaining)
            amount = min(amount, self.health_bar.get_energy_missing())
            if amount > 0:
                self.refuel_bar_remaining -= amount
                self.health_bar.change_energy(amount)
            if self.refuel_bar_remaining <= 0:
                self.refuel_bar_remaining = 0
                self.refuel_bar_max = 0

    def _run_repair(self):
        if self.repair_is_paused:
            return
        if self.health_bar.is_health_full():
            return

        if self.repair_bar_remaining <= 0:
            repair_inventory_item_obj = self.fuel_slots[1].inventory_item
            if repair_inventory_item_obj is None:
                return
            repair_value = get_block_repair_values(repair_inventory_item_obj.Block_Type)
            self.repair_bar_remaining = repair_value
            self.repair_bar_max = repair_value
            repair_inventory_item_obj.remove_block()
            if repair_inventory_item_obj.count_of_items <= 0:
                self.fuel_slots[1].inventory_item = None

        if self.repair_bar_remaining > 0:
            amount = min(self.repair_speed, self.repair_bar_remaining)
            amount = min(amount, self.health_bar.get_health_missing())
            if amount > 0:
                self.repair_bar_remaining -= amount
                self.health_bar.change_health(amount)
            if self.repair_bar_remaining <= 0:
                self.repair_bar_remaining = 0
                self.repair_bar_max = 0
    