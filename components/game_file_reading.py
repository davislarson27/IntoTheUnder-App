import json
from pathlib import Path

from .world_details import World_Details

def save_game(directory, player, inventory, grid, background_grid, world_details, start_percent=0, end_percent=100):

    inSavePercent = (end_percent - start_percent) / 100

    for grid_save_percent in grid.save_show_loading():
        yield start_percent + int(inSavePercent * 50 * grid_save_percent), 'Saving Foreground'

    for grid_save_percent in background_grid.save_show_loading():
        yield start_percent + int(inSavePercent * (50 + 46 * grid_save_percent)), 'Saving Background'

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

    yield start_percent + int(inSavePercent * 100), 'Finishing Up'


def get_user_worlds_list(game_files_directory, IMAGES_FILE_NAME, VERSION):
    def convert_file_to_class(wd_file_path): #converts file to class
        try:
            with open(wd_file_path, "r") as world_details_file:
                return World_Details.fill_from_dict(json.load(world_details_file))
        except: # prevents crash on launch with a bad details file by adding dummy file
            cur_timestamp = World_Details.get_corrupted_timestamp()
            file_name = Path(wd_file_path).parent.name
            return World_Details(f"{file_name} (CORRUPTED)", VERSION, cur_timestamp, cur_timestamp, True)

    # gets the file names for all user worlds and sorts them in order of last opened
    game_files_folder = Path(game_files_directory)

    world_details_class_list = [convert_file_to_class(f"{file}/world_details.json") for file in game_files_folder.iterdir() if file.is_dir() and file.name != IMAGES_FILE_NAME]
    world_details_class_list.sort(key=lambda world:world.last_modified_date, reverse=True)

    return [world.world_name for world in world_details_class_list if not world.version > VERSION]
