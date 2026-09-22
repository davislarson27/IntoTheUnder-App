import json
from pathlib import Path

from .chunk import Chunk
from components.block_queue import Block_Queue
import components.settings as settings
from world.world_creation.chunk_generator import Chunk_Generator
from world.region import Region


class Grid:
    
    chunk_width = Chunk.chunk_width

    def __init__(self, world_width, world_height, BLOCK_WIDTH, screen, save_directory=None, save_as_you_go=False, initialize_empty_chunks=True, world_details=None, is_menu_grid=False):
        self.settings = settings.get()

        chunks = (world_width + self.chunk_width - 1) // self.chunk_width
        self.positive_chunks = chunks
        self.negative_chunks = 0
        self.chunks_per_region = Region.get_region_width() // self.chunk_width

        self.BLOCK_WIDTH = BLOCK_WIDTH
        self.screen = screen
        self.save_directory = save_directory
        self.height = world_height

        self.MAX_WORLD_CHUNKS = 50000

        self.chunks_modified = {}
        self.chunks_loading = set()

        self.regions = {}
        self.regions_loading = set()

        # fill in self.chunks
        self.chunks = { }
        if initialize_empty_chunks:
            for chunk in range(-self.negative_chunks, self.positive_chunks):
                self.chunks[chunk] = Chunk(self.chunk_width, world_height, BLOCK_WIDTH, screen)

        self.width = len(self.chunks) * self.chunk_width

        self.world_details = world_details
        if world_details is not None and world_details.world_height is not None:
            self.chunk_generator = Chunk_Generator(screen, self.chunk_width, world_details, save_directory)
        else:
            self.chunk_generator = None

        self.max_chunks_right = self.world_details.max_chunks_right
        self.max_chunks_left = self.world_details.max_chunks_left

        self.is_menu_grid = is_menu_grid

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
    
    @classmethod
    def get_global_x_from_chunk_x(cls, chunk_x: int, chunk_id: int) -> int:
        return chunk_id * Chunk.chunk_width + chunk_x
    
    @classmethod
    def get_chunk_id(cls, global_x):
        """returns chunk_id"""
        chunk_id, _ = cls.get_chunk_x(global_x)
        return chunk_id

    def get_chunk(self, global_x, y):
        if not self.in_bounds(global_x, y):
            return None
        chunk_id, x = self.get_chunk_x(global_x)
        return self.chunks[chunk_id]

    def get_region_id(self, global_x):
        return global_x // Region.get_region_width()
    
    def get_region_from_chunk_id(self, chunk_id):
        return chunk_id // self.chunks_per_region
        
    def get(self, global_x, y):
        if not self.in_bounds(global_x, y):
            return None
        chunk_id, x = self.get_chunk_x(global_x)
        return self.chunks[chunk_id].get(x, y)
    
    def set(self, global_x, y, block, pass_through=None, stored_inventory_items=None, anchor_x=None, anchor_y=None, tick_threshold=None):
        if not self.in_bounds(global_x, y):
            return
        chunk_id, x = self.get_chunk_x(global_x)
        if not self.is_chunk_loaded(chunk_id):
            return
        chunk = self.chunks[chunk_id]
        x_offset = chunk.get_x_offset(chunk_id)
        anchor_x_local = anchor_x - x_offset if anchor_x is not None else None
        chunk.set(x, y, block, pass_through=pass_through, stored_inventory_items=stored_inventory_items, x_offset=x_offset, grid=self, anchor_x=anchor_x_local, anchor_y=anchor_y, tick_threshold=tick_threshold)

        self.chunks_modified[chunk_id] = True
    
    def set_manual(self, global_x, y, block):
        if not self.in_bounds(global_x, y):
            return
        chunk_id, x = self.get_chunk_x(global_x)
        self.chunks[chunk_id].set_manual(x, y, block)
        self.chunks_modified[chunk_id] = True

    def is_chunk_loaded(self, chunk_id):
        return chunk_id in self.chunks

    def in_bounds(self, global_x, y):
        chunk_id, x = self.get_chunk_x(global_x)
        if self.max_chunks_right is not None and chunk_id > self.max_chunks_right:
            return False
        if self.max_chunks_left is not None and chunk_id < self.max_chunks_left:
            return False
        if not self.is_chunk_loaded(chunk_id):
            return False
        if self.chunks[chunk_id].in_bounds(x,y):
            return True
        return False

    def is_filled(self, x, y):
        return self.get(x, y) is not None

    def get_block_to_px(self, block_x):
        return block_x * self.BLOCK_WIDTH

    def mark_modified(self, global_x, y):
        """block methods should use this when changing things like block.pass_through to let the chunk know that it needs to be saved"""
        if not self.in_bounds(global_x, y):
            return
        chunk_id, _ = self.get_chunk_x(global_x)
        self.chunks_modified[chunk_id] = True

    def debug_block_counts(self):
        for chunk_id, chunk in self.chunks.items():
            count = 0
            for y in range(self.height):
                for x in range(self.chunk_width):
                    if chunk.get(x, y) is not None:
                        count += 1
            print(f"Chunk {chunk_id}: {count} blocks")

    def get_chunks_to_save(self):
        """chunks that were explicitly marked dirty, plus any loaded chunk still holding live entities
        (entities mutate state like rotation/position without marking the chunk dirty on every change,
        so a chunk that still has entities in it always needs a fresh snapshot)"""
        chunk_ids = set(self.chunks_modified.keys())
        for chunk_id, chunk in self.chunks.items():
            if len(chunk.entity_set) > 0:
                chunk_ids.add(chunk_id)
        return chunk_ids

    def save(self):
        for chunk_id in self.get_chunks_to_save():
            chunk = self.chunks[chunk_id]
            chunk_data = chunk.to_dict()

            chunk_dictionary = {
                'chunk_id': chunk_id,
                'chunk_data': chunk_data
            }

            # grid_dictionary = grid.to_dict()
            with open(f"{self.save_directory}/chunk_{chunk_id}.json", "w") as grid_file:
                json.dump(chunk_dictionary, grid_file, indent=3)

    def save_show_loading(self):
        chunks_per_update = 20
        i = 0
        chunks_to_save = self.get_chunks_to_save()
        chunks_updated_count = len(chunks_to_save)
        chunks_loaded = 0
        for chunk_id in chunks_to_save:
            chunk = self.chunks[chunk_id]
            chunk_data = chunk.to_dict()

            chunk_dictionary = {
                'chunk_id': chunk_id,
                'chunk_data': chunk_data
            }

            with open(f"{self.save_directory}/chunk_{chunk_id}.json", "w") as grid_file:
                json.dump(chunk_dictionary, grid_file, indent=3)

            if chunks_loaded % chunks_per_update == 0:
                if chunks_loaded == 0:
                    yield 0
                else:
                    yield chunks_loaded / chunks_updated_count

            chunks_loaded += 1

    def generate_save_files(self):
        Path(f'{self.save_directory}').mkdir()

    def manage_chunks(self, camera_x, is_background=False):
        chunks_off_screen = self.settings.physics_chunks_beyond_screen + 2

        x_draw_grid_min = camera_x // self.BLOCK_WIDTH
        x_draw_grid_max = (camera_x + self.screen.get_width()) // self.BLOCK_WIDTH

        cur_screen_min_chunk = self.get_chunk_id(x_draw_grid_min)
        cur_screen_max_chunk = self.get_chunk_id(x_draw_grid_max)

        min_chunk = cur_screen_min_chunk - chunks_off_screen
        if self.max_chunks_left is not None: min_chunk = max(self.max_chunks_left, min_chunk)
        max_chunk = cur_screen_max_chunk + chunks_off_screen
        if self.max_chunks_right is not None: max_chunk = min(self.max_chunks_right + 1, max_chunk)
        for chunk_id in range(min_chunk, max_chunk):
            if not self.is_chunk_loaded(chunk_id): self.load_chunk(chunk_id, is_background)
                
    def chunked_physics(self, camera_x, camera_y, INVENTORY_HEIGHT=0):
        chunks_off_screen = self.settings.physics_chunks_beyond_screen

        true_height = self.screen.get_height() - INVENTORY_HEIGHT
        y_grid_min = max(0, (camera_y // self.BLOCK_WIDTH) - 7)
        y_grid_max = min(self.height, (camera_y + true_height) // self.BLOCK_WIDTH) + 8

        # x_draw_grid_min = max(0, camera_x // self.BLOCK_WIDTH)
        x_draw_grid_min = camera_x // self.BLOCK_WIDTH
        x_draw_grid_max = min(self.width - 1, (camera_x + self.screen.get_width()) // self.BLOCK_WIDTH)

        cur_screen_min_chunk = self.get_chunk_id(x_draw_grid_min)
        cur_screen_max_chunk = self.get_chunk_id(x_draw_grid_max)

        # min_chunk = max(cur_screen_min_chunk - chunks_off_screen, 0)
        min_chunk = cur_screen_min_chunk - chunks_off_screen
        max_chunk = min(cur_screen_max_chunk + chunks_off_screen + 1, self.width // self.chunk_width) # is used in range so uses a + 1 (len function gets a - 1 + 1)
        for chunk_id in range(min_chunk, max_chunk):
            if chunk_id in self.chunks: self.chunks[chunk_id].chunked_physics(y_grid_min, y_grid_max)

    def load_chunk(self, chunk_id, is_background):
        if self.is_menu_grid:
            if chunk_id not in self.chunks_loading:
                self.generate_individual_chunk(chunk_id, is_background)
            return
        else:
            chunk_file_name = Path(self.save_directory) / f'chunk_{chunk_id}.json'
            if not chunk_file_name.is_file() and chunk_id not in self.chunks_loading:
                self.generate_individual_chunk(chunk_id, is_background) # as of now this just declines to load
                return
        self.chunks_loading.add(chunk_id)
        with open(chunk_file_name, 'r') as f:
                chunk_data = json.load(f)
                global_x_offset = self.chunk_width * chunk_id
                self.chunks[chunk_id] = Chunk.fill_from_dict(chunk_data['chunk_data'], self.screen, self.BLOCK_WIDTH, global_x_offset, self)
                self.chunks_loading.remove(chunk_id)
        self.width = (max(self.chunks) + 1) * self.chunk_width

    def insert_new_chunk(self, chunk_id, chunk):
        self.chunks[chunk_id] = chunk
        self.width = max((chunk_id + 1) * self.chunk_width, self.width)

    def generate_individual_chunk(self, chunk_id, is_background):
        region_id = self.get_region_from_chunk_id(chunk_id)
        if self.chunk_generator is not None:
            if region_id not in self.regions: region = self.generate_region(region_id, is_background)
            else: region = self.regions[region_id]

            if is_background: self.insert_new_chunk(chunk_id, self.chunk_generator.generate_bg_chunk_using_region(self, region, chunk_id))
            else: self.insert_new_chunk(chunk_id, self.chunk_generator.generate_fg_chunk_using_region(self, region, chunk_id))

    def generate_region(self, region_id, is_background):
        if is_background: region = self.chunk_generator.generate_bg_region(region_id)
        else: region = self.chunk_generator.generate_fg_region(region_id)
        self.regions[region_id] = region
        return region
            
    def draw(self, camera_x, camera_y, INVENTORY_HEIGHT=0):
        """draws the grid on the screen and returns blocks that need to get drawn later"""
        # x_draw_grid_min = max(0, camera_x // self.BLOCK_WIDTH)
        x_draw_grid_min = camera_x // self.BLOCK_WIDTH
        x_draw_grid_max = min(self.width - 1, (camera_x + self.screen.get_width()) // self.BLOCK_WIDTH)

        min_chunk_id, _ = self.get_chunk_x(x_draw_grid_min)
        max_chunk_id, _ = self.get_chunk_x(x_draw_grid_max)

        block_queue = Block_Queue()
        
        for chunk_id in range(min_chunk_id, max_chunk_id+1):
            global_x_offset = chunk_id * self.chunk_width
            if not self.is_chunk_loaded(chunk_id): continue
            chunk_block_queue = self.chunks[chunk_id].draw(camera_x, camera_y, INVENTORY_HEIGHT, global_x_offset=global_x_offset)
            block_queue = block_queue + chunk_block_queue

        return block_queue

    def set_chunks(self, chunks):
        self.chunks = chunks

    def reset_save_cache(self):
        self.chunks_modified = {}

    # methods for interacting with entities
    def insert_entity(self, new_entity):
        global_grid_x, grid_y = new_entity.get_player_block_coordinates()
        chunk_id, _ = self.get_chunk_x(global_grid_x)
        chunk = self.get_chunk(global_grid_x, grid_y)
        chunk.insert_entity(new_entity)
        new_entity.entity_chunk = chunk_id
        self.chunks_modified[chunk_id] = True

    def get_entities(self, camera_x):
        """returns a set of entities on the screen"""
        x_draw_grid_min = camera_x // self.BLOCK_WIDTH
        x_draw_grid_max = min(self.width - 1, (camera_x + self.screen.get_width()) // self.BLOCK_WIDTH)

        min_chunk_id, _ = self.get_chunk_x(x_draw_grid_min)
        max_chunk_id, _ = self.get_chunk_x(x_draw_grid_max)
        
        entities_set = set()
        for chunk_id in range(min_chunk_id, max_chunk_id+1):
            entities_set.update(self.chunks[chunk_id].get_entities())

        return entities_set

    def check_entity_chunks(self, rendered_entities):
        for entity in rendered_entities:
            if entity.is_dead(): # already removed from its chunk's entity_set this frame
                continue
            cur_chunk_id = entity.compute_chunk_id()
            if entity.entity_chunk != cur_chunk_id:
                self.reasign_entity_chunk(entity, cur_chunk_id)

    def reasign_entity_chunk(self, entity, new_chunk_id):
        self.chunks_modified[entity.entity_chunk] = True
        self.chunks[entity.entity_chunk].entity_set.remove(entity)
        self.chunks[new_chunk_id].entity_set.add(entity)
        entity.entity_chunk = new_chunk_id
        self.chunks_modified[new_chunk_id] = True

    def remove_entity(self, entity):
        self.chunks_modified[entity.entity_chunk] = True
        self.chunks[entity.entity_chunk].entity_set.remove(entity)

    def drop_block(self, drop_block_type, x_px, y_px):
        if drop_block_type is None:
            return
        
        from play.entities.entities_export import Item_Drop

        item_drop = Item_Drop(self, self.screen, x_px, y_px, self.BLOCK_WIDTH, world_details=self.world_details)
        item_drop.set_block(drop_block_type)
        item_drop.set_random_subblock_location()
        self.insert_entity(item_drop)

    @classmethod
    def preinitialize_local_grid(cls, directory, screen, block_width, player, is_background=False):
        "fills the grid from a file but uses a generator and required to be run in a loop -> yields grid, percent done (if percent done < 1 then grid = None)"
        # initialize the grid
        world_width = (player.compute_chunk_id() + 1) * cls.chunk_width # assumes only positive chunks
        world_height = player.world_details.world_height or 150 # falls back for saves made before world_details carried generation data
        return_grid = Grid(world_width, world_height, block_width, screen, directory, initialize_empty_chunks=False, world_details=player.world_details)

        return_grid.manage_chunks(player.x, is_background=is_background)
        yield return_grid, 1
