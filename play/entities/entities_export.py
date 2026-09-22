from .entities_files.passive_entities import *
from .entities_files.item_drop import *
from .entities_files.snow_man import *

"""this file pulls together all of the entity files into one to be exported"""

def get_entities_list():
    return [
        Item_Drop,
        Snow_Man_Entity,
    ]

def get_str_to_entity(): # uses blocks_list to generate dictionary that converts str names to their types
    entities_list = get_entities_list()

    entities_dict = {}
    for entity in entities_list:
        entities_dict[entity.__name__] = entity
    return entities_dict
