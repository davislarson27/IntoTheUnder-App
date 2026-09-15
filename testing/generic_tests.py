import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from world.grid import Grid
from world.region import Region


# chunk negative tests
def test_get_chunk_id_from_global_x():
    global_x = -16
    chunk_id = Grid.get_chunk_id(global_x)
    print(chunk_id)

def get_chunk_x_from_global_x():
    global_x = -17
    chunk_id, chunk_x = Grid.get_chunk_x(global_x)
    print(f'global_x = {global_x} -> chunk_x = {chunk_x}, chunk_id = {chunk_id}')

def get_global_x_from_chunk_x():
    chunk_x = 15
    chunk_id = -2
    global_x = Grid.get_global_x_from_chunk_x(chunk_x, chunk_id)
    print(f'chunk_x = {chunk_x}, chunk_id = {chunk_id} -> global_x = {global_x}')

# negative region tests
def get_region_id():
    print(Region.get_region_id_from_global_x(-15))

def get_region_x_from_chunk_x():
    print(Region.get_region_x_from_chunk_x(15, -1))

if __name__ == '__main__':
    get_region_x_from_chunk_x()
