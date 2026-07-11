import hashlib

from play.inventory.inventory_item import Inventory_Item


class Loot_Odds:
    def __init__(self, item, max_count, odds_of_appearing):
        self.item = item
        self.max_count = max_count
        self.odds_of_appearing = odds_of_appearing

class Chest_Loot:
    def __init__(self, loot_list):
        self.loot_list = loot_list

    def get_slot(self, random_factor):
        appear_odds = int(hashlib.sha256(f"{random_factor}_appear".encode()).hexdigest(), 16) / (2**256 - 1)
        rolling_odds = 0
        for loot_list_spot in self.loot_list:
            if loot_list_spot.odds_of_appearing + rolling_odds > appear_odds:
                count = max(1, int(int(hashlib.sha256(f"{random_factor}_count".encode()).hexdigest(), 16) / (2**256 - 1) * loot_list_spot.max_count))
                return Inventory_Item(loot_list_spot.item, count)
            rolling_odds += loot_list_spot.odds_of_appearing
        return None
