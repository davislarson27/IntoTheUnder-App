from .chunk import Chunk
import json
from pathlib import Path


class Grid:
    
    chunk_width = 16

    def __init__(self, world_width, world_height, BLOCK_WIDTH, screen, save_directory=None, save_as_you_go=False):
        chunks = (world_width + self.chunk_width - 1) // self.chunk_width
        # self.positive_chunks = chunks // 2
        # self.negative_chunks = chunks - self.positive_chunks
        self.positive_chunks = chunks
        self.negative_chunks = 0

        self.BLOCK_WIDTH = BLOCK_WIDTH
        self.screen = screen
        self.save_directory = save_directory
        self.height = world_height

        self.chunks_modified = {}

        # fill in self.chunks
        self.chunks = { }
        for chunk in range(-self.negative_chunks, self.positive_chunks):
            self.chunks[chunk] = Chunk(self.chunk_width, world_height, BLOCK_WIDTH, screen)

        self.width = len(self.chunks) * self.chunk_width

    def __str__(self):
        string = ''
        for chunk_id in self.chunks:
            chunk = self.chunks[chunk_id]
            string += f'chunk {chunk_id}\n'
            string += str(chunk)
            string += '\n'
        return string

    @classmethod
    def get_chunk_x(cls, global_x):
        """returns chunk_id, chunk_x -> used to access chunk"""
        chunk_id = global_x // cls.chunk_width
        chunk_x = global_x % cls.chunk_width
        return chunk_id, chunk_x

    def get(self, global_x, y):
        if not self.in_bounds(global_x, y):
            return None
        chunk_id, x = self.get_chunk_x(global_x)
        return self.chunks[chunk_id].get(x, y)
    
    def set(self, global_x, y, block, pass_through=None, stored_inventory_items=None):
        # print('chunked grid in use')
        if not self.in_bounds(global_x, y):
            return
        chunk_id, x = self.get_chunk_x(global_x)
        set_block = None
        if block is not None:
            set_block = block(self, self.screen, global_x, y, self.BLOCK_WIDTH, pass_through, stored_inventory_items=stored_inventory_items)
        self.chunks[chunk_id].set_manual(x, y, set_block)
        
        self.chunks_modified[chunk_id] = True
        
    def set_manual(self, global_x, y, block):
        if not self.in_bounds(global_x, y):
            return
        chunk_id, x = self.get_chunk_x(global_x)
        self.chunks[chunk_id].set_manual(x, y, block)
        self.chunks_modified[chunk_id] = True

    def in_bounds(self, global_x, y):
        chunk_id, _ = self.get_chunk_x(global_x)
        if chunk_id > self.positive_chunks - 1 or chunk_id < -self.negative_chunks:
            return False
        return True

    def is_filled(self, x, y):
        return self.get(x, y) is not None

    def debug_block_counts(self):
        for chunk_id, chunk in self.chunks.items():
            count = 0
            for y in range(self.height):
                for x in range(self.chunk_width):
                    if chunk.get(x, y) is not None:
                        count += 1
            print(f"Chunk {chunk_id}: {count} blocks")

    def save(self):
        for chunk_id in self.chunks_modified:
            chunk = self.chunks[chunk_id]
            chunk_data = chunk.to_dict()

            chunk_dictionary = {
                'chunk_id': chunk_id,
                'chunk_data': chunk_data
            }

            # grid_dictionary = grid.to_dict()
            with open(f"{self.save_directory}/chunk_{chunk_id}.json", "w") as grid_file:
                json.dump(chunk_dictionary, grid_file, indent=3)

    def generate_save_files(self):
        Path(f'{self.save_directory}').mkdir()
    
    def physics(self, camera_x, camera_y, INVENTORY_HEIGHT = 0):
        x_draw_grid_min = max(0, camera_x // self.BLOCK_WIDTH)
        x_draw_grid_max = min(self.width, (camera_x + self.screen.get_width()) // self.BLOCK_WIDTH) + 1

        true_height = self.screen.get_height() - INVENTORY_HEIGHT
        y_draw_grid_min = max(0, camera_y // self.BLOCK_WIDTH)
        y_draw_grid_max = min(self.height, (camera_y + true_height) // self.BLOCK_WIDTH) + 1

        for y in range(y_draw_grid_min, y_draw_grid_max):
            for global_x in range(x_draw_grid_min, x_draw_grid_max):
                obj = self.get(global_x, y)
                if(obj != None):
                    obj.physics()

    def draw(self, camera_x, camera_y, INVENTORY_HEIGHT = 0):
        x_draw_grid_min = max(0, camera_x // self.BLOCK_WIDTH)
        x_draw_grid_max = min(self.width, (camera_x + self.screen.get_width()) // self.BLOCK_WIDTH) + 1

        true_height = self.screen.get_height() - INVENTORY_HEIGHT
        y_draw_grid_min = max(0, camera_y // self.BLOCK_WIDTH)
        y_draw_grid_max = min(self.height, (camera_y + true_height) // self.BLOCK_WIDTH) + 1

        for y in range(y_draw_grid_min, y_draw_grid_max):
            for global_x in range(x_draw_grid_min, x_draw_grid_max):
                obj = self.get(global_x, y)
                if(obj != None):
                    obj.draw(camera_x = camera_x, camera_y = camera_y)

    def set_chunks(self, chunks):
        self.chunks = chunks

    def reset_save_cache(self):
        self.chunks_modified = {}

    @classmethod
    def fill_from_file(cls, directory, screen, block_width):
        max_id = 0
        chunks_data = {}
        for file in Path(directory).rglob('*.json'):
            with open(file, 'r') as f:
                chunk = json.load(f)
                chunk_id = chunk['chunk_id']
                max_id = max(max_id, chunk_id)
                chunks_data[chunk_id] = chunk
        
        world_width = (max_id + 1) * cls.chunk_width # assumes only positive chunks
        world_height = chunks_data[0]['chunk_data']['grid_height']
        return_grid = Grid(world_width, world_height, block_width, screen, directory)

        chunks = {}
        for chunk_id in chunks_data:
            chunk_data = chunks_data[chunk_id]['chunk_data']
            global_x_offset = cls.chunk_width * chunk_id
            chunks[chunk_id] = Chunk.fill_from_dict(chunk_data, screen, block_width, global_x_offset, return_grid)

        return_grid.set_chunks(chunks)
        return return_grid
