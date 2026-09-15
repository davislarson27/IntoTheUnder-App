from pathlib import Path

from world.world_creation.structures.structures import *
from world.world_creation.biomes import *
from world.chunk import Chunk

class Region:
    chunks_in_region = 4
    region_width: int = Chunk.chunk_width *  chunks_in_region # gives the number of blocks across a region
    def __init__(self, directory, region_id, chunk_width, biomes, elevations, structures, bg_structures_for_fg, underground_structures):
        self.directory = directory
        self.region_id = region_id
        self.chunk_width = chunk_width
        self.biomes = biomes
        self.elevations = elevations
        self.structures = structures
        self.bg_structures_for_fg = bg_structures_for_fg
        self.underground_structures = underground_structures

    def __str__(self):
        return_str = f'region {self.region_id} saving to directory {self.directory}'
        return_str += '\nbiomes'
        i = 0
        for biome in self.biomes:
            return_str += f'\n  {i}: {biome.__name__}'
            i+=1
        return_str += '\nelevations'
        for elevation in self.elevations:
            return_str += f'\n  {elevation}'
        return_str += '\nstructures'
        for structure in self.structures:
            if structure is None: struct_str = 'none'
            else: struct_str = f'({structure.structure_type.__name__}, {structure.col_num})'
            return_str += f'\n  {struct_str}'
        return return_str
    
    def get_region_x_from_chunk_x(self, chunk_x: int, chunk_id: int) -> int:
        return chunk_id % self.chunks_in_region * Chunk.chunk_width + chunk_x
    
    def get_biome(self, chunk_x: int, chunk_id: int):
        return self.biomes[self.get_region_x_from_chunk_x(chunk_x, chunk_id)]

    def get_elevation(self, chunk_x: int, chunk_id: int) -> int:
        return self.elevations[self.get_region_x_from_chunk_x(chunk_x, chunk_id)]
    
    def get_structure(self, chunk_x: int, chunk_id: int) -> int:
        return self.structures[self.get_region_x_from_chunk_x(chunk_x, chunk_id)]

    def get_bg_structure_for_fg(self, chunk_x: int, chunk_id: int) -> int:
        return self.bg_structures_for_fg[self.get_region_x_from_chunk_x(chunk_x, chunk_id)]

    @classmethod
    def get_x_offset(cls, region_id: int) -> int:
        return region_id * cls.region_width
    
    @classmethod
    def get_region_id_from_global_x(cls, global_x: int) -> int:
        return global_x // cls.region_width

    @classmethod
    def get_region_width(cls) -> int:
        return cls.region_width

    @staticmethod
    def is_region_loaded(directory, region_id, loaded_regions):
        chunk_file_name = Path(directory) / 'region' / f'region_{region_id}.json'
        return not chunk_file_name.is_file() and region_id not in loaded_regions
    
    @classmethod
    def get_fg_region(cls, directory, region_id, seed) -> Region:
        """generates and returns a new region for the given id"""
        return 