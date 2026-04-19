import json
# from world.grid import Grid
from world.chunked_grid import Grid
from play.inventory.inventory import Inventory
from play.player import Player
from components.world_details import World_Details

def save_game(directory, player, inventory, grid, background_grid, world_details, start_percent=0, end_percent=100):

    yield start_percent, 'Saving Grid'

    inSavePercent = (end_percent - start_percent) / 100

    grid.save()

    yield start_percent + int(inSavePercent * 50), 'Saving Background'

    background_grid.save()

    yield start_percent + int(inSavePercent * 97), 'Saving Inventory'

    player_dictionary = player.to_dict()
    with open(f"{directory}/player_attributes.json", "w") as player_attr_file:
        json.dump(player_dictionary, player_attr_file, indent=3)
    
    inventory_dict = inventory.to_dict()
    with open(f"{directory}/inventory.json", "w") as inventory_file:
        json.dump(inventory_dict, inventory_file, indent=3)

    world_details_dict = world_details.to_dict()
    with open(f"{directory}/world_details.json", "w") as world_details_file:
        json.dump(world_details_dict, world_details_file, indent=3)

    return start_percent + int(inSavePercent * 100), 'Finishing Up'
