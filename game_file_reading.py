import json
from grid import Grid
from full_inventory import Inventory
from player import Player
from world_details import World_Details

def save_game(directory, player, inventory, grid, world_details):
    grid_dictionary = grid.to_dict()
    with open(f"{directory}/grid.json", "w") as grid_file:
        json.dump(grid_dictionary, grid_file, indent=3)

    player_dictionary = player.to_dict()
    with open(f"{directory}/player_attributes.json", "w") as player_attr_file:
        json.dump(player_dictionary, player_attr_file, indent=3)
    
    inventory_dict = inventory.to_dict()
    with open(f"{directory}/inventory.json", "w") as inventory_file:
        json.dump(inventory_dict, inventory_file, indent=3)

    world_details_dict = world_details.to_dict()
    with open(f"{directory}/world_details.json", "w") as world_details_file:
        json.dump(world_details_dict, world_details_file, indent=3)

def load_world(directory, screen, window, INVENTORY_HEIGHT, HEALTH_BAR_HEIGHT, BLOCK_WIDTH, images):
    with open(f"{directory}/grid.json", "r") as grid_file:
        grid_dict = json.load(grid_file)
        grid = Grid.fill_from_dict(grid_dict, screen, BLOCK_WIDTH)

    with open(f"{directory}/inventory.json", "r") as inventory_file:
        inventory_dict = json.load(inventory_file)
        inventory = Inventory.fill_from_dict(inventory_dict, screen, window, INVENTORY_HEIGHT, HEALTH_BAR_HEIGHT)

    with open(f"{directory}/player_attributes.json", "r") as player_attr_file:
        player_attr_dict = json.load(player_attr_file)
        player_attr_dict["screen"] = screen
        player_attr_dict["grid"] = grid
        player_attr_dict["inventory_bar_height"] = INVENTORY_HEIGHT
        player_attr_dict["health_bar_height"] = HEALTH_BAR_HEIGHT
        player = Player(**player_attr_dict)
        player.images = images

    with open(f"{directory}/world_details.json", "r") as world_details_file:
        world_details_dict = json.load(world_details_file)
        # world_details = World_Details(**world_details_dict)
        world_details = World_Details.fill_from_dict(world_details_dict)

    return grid, inventory, player, world_details
