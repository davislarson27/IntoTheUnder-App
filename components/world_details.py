from datetime import datetime, timezone
import random

class World_Details():
    def __init__(self, world_name, version, creation_date, last_modified_date, is_corrupted = False, world_spawn_x=0, world_spawn_y=0, world_seed=0, keep_inventory=True, survival_mode=True):
        self.world_name = world_name
        self.version = version
        self.creation_date = creation_date or self.get_cur_timestamp()
        self.last_modified_date = last_modified_date or self.get_cur_timestamp()
        self.is_corrupted = is_corrupted
        self.world_spawn_x = world_spawn_x
        self.world_spawn_y = world_spawn_y
        self.world_seed = world_seed
        self.keep_inventory = keep_inventory
        self.survival_mode = survival_mode

    def to_dict(self, update_last_modified_date=True):
        cur_dict = {
            "world_name": self.world_name,
            "version": self.version,
            "world_spawn_x": self.world_spawn_x,
            "world_spawn_y": self.world_spawn_y,
            "world_seed": self.world_seed,
            "creation_date": self.creation_date.isoformat(),
            "keep_inventory": self.keep_inventory,
            "survival_mode": self.survival_mode
        }
        if update_last_modified_date:
            cur_dict["last_modified_date"] = self.get_cur_timestamp().isoformat()
        else:
            cur_dict["last_modified_date"] = self.last_modified_date.isoformat()

        return cur_dict
    
    def set_spawn(self, x, y):
        self.world_spawn_x, self.world_spawn_y = x, y

    def set_seed(self, seed):
        self.world_seed = seed

    @staticmethod
    def get_cur_timestamp():
        return datetime.now(timezone.utc)
    
    @staticmethod
    def get_corrupted_timestamp():
        return datetime.min.replace(tzinfo=timezone.utc)
    
    @staticmethod
    def create_new_world(world_name, game_version, world_spawn_x=0, world_spawn_y=0, world_seed=0, keep_inventory=True, survival_mode=True):
        cur_time = World_Details.get_cur_timestamp()
        return World_Details(world_name, game_version, cur_time, cur_time, world_spawn_x=world_spawn_x, world_spawn_y=world_spawn_y, world_seed=world_seed, keep_inventory=keep_inventory, survival_mode=survival_mode)
        
    @staticmethod
    def fill_from_dict(world_details_dict):
        world_name = world_details_dict["world_name"]
        version = world_details_dict["version"]
        try:
            creation_date = datetime.fromisoformat(world_details_dict["creation_date"])
            last_modified_date = datetime.fromisoformat(world_details_dict["last_modified_date"])
        except:
            creation_date = World_Details.get_cur_timestamp()
            last_modified_date = World_Details.get_cur_timestamp()

        world_spawn_x = world_details_dict["world_spawn_x"]
        world_spawn_y = world_details_dict["world_spawn_y"]

        if "world_seed" in world_details_dict:
            world_seed = world_details_dict["world_seed"]
        else:
            world_seed = int(random.random() * 100000) # bad solution but it's quick

        if "keep_inventory" in world_details_dict:
            keep_inventory = world_details_dict["keep_inventory"]
        else:
            keep_inventory = True

        if "survival_mode" in world_details_dict:
            survival_mode = world_details_dict["survival_mode"]
        else:
            survival_mode = True

        return World_Details(world_name, version, creation_date, last_modified_date, world_spawn_x=world_spawn_x, world_spawn_y=world_spawn_y, world_seed=world_seed, keep_inventory=keep_inventory, survival_mode=survival_mode)
    