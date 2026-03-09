from datetime import datetime, timezone

class World_Details():
    def __init__(self, world_name, version, creation_date, last_modified_date, is_corrupted = False):
        self.world_name = world_name
        self.version = version
        self.creation_date = creation_date or self.get_cur_timestamp()
        self.last_modified_date = last_modified_date or self.get_cur_timestamp()
        self.is_corrupted = is_corrupted

    def to_dict(self, update_last_modified_date=True):
        cur_dict = {
            "world_name": self.world_name,
            "version": self.version,
            "creation_date": self.creation_date.isoformat()
        }
        if update_last_modified_date:
            cur_dict["last_modified_date"] = self.get_cur_timestamp().isoformat()
        else:
            cur_dict["last_modified_date"] = self.last_modified_date.isoformat()

        return cur_dict
    
    @staticmethod
    def get_cur_timestamp():
        return datetime.now(timezone.utc)
    
    @staticmethod
    def get_corrupted_timestamp():
        return datetime.min.replace(tzinfo=timezone.utc)
    
    @staticmethod
    def create_new_world(world_name, game_version):
        cur_time = World_Details.get_cur_timestamp()
        return World_Details(world_name, game_version, cur_time, cur_time)
        
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

        return World_Details(world_name, version, creation_date, last_modified_date)