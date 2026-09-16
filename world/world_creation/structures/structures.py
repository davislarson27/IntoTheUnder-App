import hashlib

from world.blocks.block_export import *
from .structure_instruction import Structure_Instruction, Var_Structure_Instruction
from play.inventory.submenus.crafting_recipes import User_Crafting_Recipes_List
from .chest_loot import Chest_Loot, Loot_Odds


class Mahogany_Tree_Rand_Width:
    width = 6
    start_x_diff = 1 # distance from the origin x that the y elevation should be set to
    height = 8 # distance above ground
    depth = 0 # distance below ground

    def __init__(self):
        pass

    @classmethod
    def get_width(cls):
        return cls.width
    
    @classmethod
    def get_x_difference_for_y(cls):
        """returns the value to add to x to get the corect elevation this object is calcualated for (i.e., for a tree it would be +1)"""
        return cls.start_x_diff

    @classmethod
    def get_height(cls):
        """gets height above the start point"""
        return cls.height

    @classmethod
    def get_depth(cls):
        """gets depth below the start point"""
        return cls.depth

    @classmethod
    def getStructureInstructions(cls, ground_x, ground_y, grid, random_factor=0, biome_name=None):
        """takes top left block coordinates and returns list of coordinates and a list of blocks to access in the same order"""
        # initialize list
        structureInstructionsList = []

        tree_style_chance = int(hashlib.sha256(f"{random_factor}_tree_type".encode()).hexdigest(), 16) / (2**256 - 1)
        if tree_style_chance > 0.8: # 2 wide style
            structureInstructionsList, var_structure_instructions = Mahogany_Tree_Double.getStructureInstructions(ground_x, ground_y, grid, random_factor, biome_name)
        else:
            structureInstructionsList, var_structure_instructions = Mahogany_Tree.getStructureInstructions(ground_x, ground_y, grid, random_factor, biome_name)

        # return list
        return structureInstructionsList, var_structure_instructions

    @classmethod
    def getBgStructureInstructions(cls, ground_x, ground_y, grid, random_factor=0, biome_name=None): # needs to actually reflect the background
        """takes top left block coordinates and returns list of coordinates and a list of blocks to access in the same order"""
        return [], [] # trees don't have backgrounds


class Mahogany_Tree_Double:
    width = 6
    start_x_diff = 1 # distance from the origin x that the y elevation should be set to
    height = 7 # distance above ground
    depth = 0 # distance below ground

    def __init__(self):
        pass

    @classmethod
    def get_width(cls):
        return cls.width
    
    @classmethod
    def get_x_difference_for_y(cls):
        """returns the value to add to x to get the corect elevation this object is calcualated for (i.e., for a tree it would be +1)"""
        return cls.start_x_diff

    @classmethod
    def get_height(cls):
        """gets height above the start point"""
        return cls.height

    @classmethod
    def get_depth(cls):
        """gets depth below the start point"""
        return cls.depth

    @classmethod
    def getStructureInstructions(cls, ground_x, ground_y, grid, random_factor=0, biome_name=None):
        """takes top left block coordinates and returns list of coordinates and a list of blocks to access in the same order"""
        # initialize list
        structureInstructionsList = []

        # leaves disappearing time thresholds
        def get_ticks(x, y):
            value = int(hashlib.sha256(f"{random_factor}_{x}_{y}".encode()).hexdigest(), 16)
            normalized = value / (2**256)
            return int(normalized * 1000) + 200 # ticks will be between 200 and 1200

        # determine the height of the tree
        if random_factor < 0.1:
            tree_height = 6
        elif random_factor < 0.4:
            tree_height = 4
        else:
            tree_height = 5

        # trunk
        start_y = ground_y-1
        for y in range(tree_height):
            for x in range(2):
                structureInstructionsList.append(Structure_Instruction(ground_x+x+2, start_y-y, Mahogany_Log))
        
        # add the leaves to the structure instructions
        y = ground_y - tree_height - 1
        for x in range(6):
            ticks = get_ticks(x, y)
            structureInstructionsList.append(Structure_Instruction(ground_x+x, y, Mahogany_Leaves(grid, grid.screen, ground_x+x, y, grid.BLOCK_WIDTH, pass_through=True, anchor_x=ground_x+2, anchor_y=start_y, tick_threshold=ticks), blockIsInitialized=True))

        y = ground_y - tree_height - 2
        for x in range(1, 5):
            ticks = get_ticks(x, y)
            structureInstructionsList.append(Structure_Instruction(ground_x+x, y, Mahogany_Leaves(grid, grid.screen, ground_x+x, y, grid.BLOCK_WIDTH, pass_through=True, anchor_x=ground_x+2, anchor_y=start_y, tick_threshold=ticks), blockIsInitialized=True))

        y = ground_y - tree_height - 3
        for x in range(2, 4):
            ticks = get_ticks(x, y)
            structureInstructionsList.append(Structure_Instruction(ground_x+x, y, Mahogany_Leaves(grid, grid.screen, ground_x+x, y, grid.BLOCK_WIDTH, pass_through=True, anchor_x=ground_x+2, anchor_y=start_y, tick_threshold=ticks), blockIsInitialized=True))

        # add a branched off leaf
        extra_leaf_odds = int(hashlib.sha256(f"{random_factor}_extra_leaf_odds".encode()).hexdigest(), 16) / (2**256 - 1)
        add_branched_leaf = True
        if extra_leaf_odds < 0.35:
            x = 1
            y_diff = 1
        elif extra_leaf_odds < 0.7:
            x = 1
            y_diff = 1
        elif extra_leaf_odds < 0.84:
            x = 4
            y_diff = 2
        elif extra_leaf_odds < 0.98:
            x = 4
            y_diff = 2
        else:
            add_branched_leaf = False

        if add_branched_leaf:
            y = ground_y - tree_height + y_diff
            ticks = get_ticks(x, y)
            structureInstructionsList.append(Structure_Instruction(ground_x+x, y, Mahogany_Leaves(grid, grid.screen, ground_x+x, y, grid.BLOCK_WIDTH, pass_through=True, anchor_x=ground_x+2, anchor_y=start_y, tick_threshold=ticks), blockIsInitialized=True))

        # return list
        return structureInstructionsList, [Var_Structure_Instruction(ground_x + 2, ground_y, Mahogany_Log, None, 1), Var_Structure_Instruction(ground_x + 3, ground_y, Mahogany_Log, None, 1)]

    @classmethod
    def getBgStructureInstructions(cls, ground_x, ground_y, grid, random_factor=0, biome_name=None): # needs to actually reflect the background
        """takes top left block coordinates and returns list of coordinates and a list of blocks to access in the same order"""
        return [], [] # trees don't have backgrounds


class Mahogany_Tree:
    width = 3
    start_x_diff = 1 # distance from the origin x that the y elevation should be set to
    height = 8 # distance above ground
    depth = 0 # distance below ground

    def __init__(self):
        pass

    @classmethod
    def get_width(cls):
        return cls.width
    
    @classmethod
    def get_x_difference_for_y(cls):
        """returns the value to add to x to get the corect elevation this object is calcualated for (i.e., for a tree it would be +1)"""
        return cls.start_x_diff

    @classmethod
    def get_height(cls):
        """gets height above the start point"""
        return cls.height

    @classmethod
    def get_depth(cls):
        """gets depth below the start point"""
        return cls.depth

    @classmethod
    def getStructureInstructions(cls, ground_x, ground_y, grid, random_factor=0, biome_name=None):
        """takes top left block coordinates and returns list of coordinates and a list of blocks to access in the same order"""
        # initialize list
        structureInstructionsList = []

        # leaves disappearing time thresholds
        def get_ticks(x, y):
            value = int(hashlib.sha256(f"{random_factor}_{x}_{y}".encode()).hexdigest(), 16)
            normalized = value / (2**256)
            return int(normalized * 1000) + 200 # ticks will be between 200 and 1200

        # determine the height of the tree
        if random_factor < 0.1:
            tree_height = 3
        elif random_factor < 0.35:
            tree_height = 5
        else:
            tree_height = 4

        # trunk
        start_y = ground_y-1
        for y in range(tree_height):
            structureInstructionsList.append(Structure_Instruction(ground_x+2, start_y-y, Mahogany_Log))
        
        # add the leaves to the structure instructions
        y = ground_y - tree_height - 1
        for x in range(5):
            ticks = get_ticks(x, y)
            structureInstructionsList.append(Structure_Instruction(ground_x+x, y, Mahogany_Leaves(grid, grid.screen, ground_x+x, y, grid.BLOCK_WIDTH, pass_through=True, anchor_x=ground_x+2, anchor_y=start_y, tick_threshold=ticks), blockIsInitialized=True))

        y = ground_y - tree_height - 2
        for x in range(1, 4):
            ticks = get_ticks(x, y)
            structureInstructionsList.append(Structure_Instruction(ground_x+x, y, Mahogany_Leaves(grid, grid.screen, ground_x+x, y, grid.BLOCK_WIDTH, pass_through=True, anchor_x=ground_x+2, anchor_y=start_y, tick_threshold=ticks), blockIsInitialized=True))

        # add a branched off leaf
        extra_leaf_odds = int(hashlib.sha256(f"{random_factor}_extra_leaf_odds".encode()).hexdigest(), 16) / (2**256 - 1)
        add_branched_leaf = True
        if extra_leaf_odds < 0.35:
            x = 1
        elif extra_leaf_odds < 0.7:
            x = 3
        else:
            add_branched_leaf = False
        
        if add_branched_leaf:
            y = ground_y - tree_height + 1
            ticks = get_ticks(x, y)
            structureInstructionsList.append(Structure_Instruction(ground_x+x, y, Mahogany_Leaves(grid, grid.screen, ground_x+x, y, grid.BLOCK_WIDTH, pass_through=True, anchor_x=ground_x+2, anchor_y=start_y, tick_threshold=ticks), blockIsInitialized=True))

        # return list
        return structureInstructionsList, [Var_Structure_Instruction(ground_x + 2, ground_y, Mahogany_Log, None, 1)]

    @classmethod
    def getBgStructureInstructions(cls, ground_x, ground_y, grid, random_factor=0, biome_name=None): # needs to actually reflect the background
        """takes top left block coordinates and returns list of coordinates and a list of blocks to access in the same order"""
        return [], [] # trees don't have backgrounds


# ------------------------------------ start column/chunk based structures ------------------------------------ #

class Structure_Region_Container:
    def __init__(self, structure_type, col_num):
        self.structure_type = structure_type
        self.col_num = col_num


class Col_Structures:
    def __init__(self, structure_odds, start_x, start_y, end_y, grid, chunk, x_offset):
        self.start_x = start_x
        self.end_y = end_y
        self.struct_seed = structure_odds
        self.grid = grid
        self.chunk = chunk
        self.x_offset = x_offset

    def set_to_chunk(self, x, y, block_type, pass_through=None, stored_inventory_items=None, anchor_x=None, anchor_y=None, tick_threshold=None):
        self.chunk.set(x, y, block_type, x_offset=self.x_offset, pass_through=pass_through, stored_inventory_items=stored_inventory_items, grid=self.grid, anchor_x=anchor_x, anchor_y=anchor_y, tick_threshold=tick_threshold)

    def set_to_grid(self, x, y, block_type, pass_through=None, stored_inventory_items=None, anchor_x=None, anchor_y=None, tick_threshold=None):
        self.grid.set(x, y, block_type, pass_through=pass_through, stored_inventory_items=stored_inventory_items, anchor_x=anchor_x, anchor_y=anchor_y, tick_threshold=tick_threshold)

    def get_random_float(self, hash_string: str) -> float:
        return int(hashlib.sha256(f"{self.struct_seed}_{hash_string}".encode()).hexdigest(), 16) / (2**256)
    
    def get_random_int(self, min: int, max: int, hash_string: str) -> int:
        if min > max: raise ValueError("Incorrect max/min for random ints with structures")
        rand_flt = self.get_random_float(hash_string)
        int_range = max - min + 1
        return int(rand_flt * int_range) + min

    def set_fg_col(self, col_num, ground_y, biome):
        self._set_fg_col(col_num, ground_y, biome, self.set_to_chunk)

    def set_fg_col_to_grid_directly(self, col_num, ground_y, biome):
        self._set_fg_col(col_num, ground_y, biome, self.set_to_grid)

    def _set_fg_col(self, col_num, ground_y, biome, set_to_func):
        return

    def set_bg_col(self, col_num, fg_ground_y, biome):
        self._set_bg_col(col_num, fg_ground_y, biome, self.set_to_chunk)

    def set_bg_col_to_grid_directly(self, col_num, fg_ground_y, biome):
        self._set_bg_col(col_num, fg_ground_y, biome, self.set_to_grid)

    def _set_bg_col(self, col_num, fg_ground_y, biome, set_to_func):
        return


class Col_Cactus_Structure(Col_Structures):
    width = 1
    def __init__(self, structure_odds, start_x, start_y, end_y, grid, chunk, x_offset):
        self.start_x = start_x
        self.end_y = end_y
        self.struct_seed = structure_odds
        self.grid = grid
        self.chunk = chunk
        self.x_offset = x_offset

        # determine the height of the tree
        height_chance = self.get_random_float(f'{self.start_x}_cactus_height')
        if height_chance < 0.0001:
            self.cactus_height = 4
        elif height_chance < 0.2:
            self.cactus_height = 1
        elif height_chance < 0.4:
            self.cactus_height = 3
        else:
            self.cactus_height = 2

    def _set_fg_col(self, col_num, ground_y, biome, set_to_func):
        if col_num == 0:
            for y in range(ground_y-self.cactus_height, ground_y):
                set_to_func(self.start_x, y, Cactus)

    @classmethod
    def get_x_for_start_y(cls, start_x: int, structure_odds: float) -> int:
        return start_x

    @classmethod
    def get_width(cls, structure_odds):
        return cls.width


class Col_Snow_Man_Structure(Col_Structures):
    width = 1
    def __init__(self, structure_odds, start_x, start_y, end_y, grid, chunk, x_offset):
        self.start_x = start_x
        self.end_y = end_y
        self.struct_seed = structure_odds
        self.grid = grid
        self.chunk = chunk
        self.x_offset = x_offset

        self.height = 2

    def _set_fg_col(self, col_num, ground_y, biome, set_to_func):
        set_to_func(self.start_x, ground_y-1, Snow_Block)
        set_to_func(self.start_x, ground_y-2, Snow_Man_Head)

    @classmethod
    def get_x_for_start_y(cls, start_x: int, structure_odds: float) -> int:
        return start_x

    @classmethod
    def get_width(cls, structure_odds):
        return cls.width


class Col_Tree(Col_Structures):
    width = 3
    distance_to_stump_x = 1
    def __init__(self, structure_odds, start_x, start_y, end_y, grid, chunk, x_offset):
        self.start_x = start_x
        self.global_start_x = x_offset + start_x
        self.start_y = start_y
        self.end_y = end_y
        self.struct_seed = structure_odds
        self.grid = grid
        self.chunk = chunk
        self.x_offset = x_offset

        tree_height_chance = self.get_random_float(f'{self.global_start_x}_tree_height')
        if tree_height_chance < 0.0001: self.tree_height = 4
        elif tree_height_chance < 0.2: self.tree_height = 1
        elif tree_height_chance < 0.4: self.tree_height = 3
        else: self.tree_height = 2

        self.leaves_start_elev = start_y - self.tree_height - 1

        self.anchor_x = self.start_x + self.distance_to_stump_x
        self.anchor_y = self.start_y - 1

    def get_ticks(self, x, y):
        value = int(hashlib.sha256(f"{self.struct_seed}_{x}_{y}".encode()).hexdigest(), 16)
        normalized = value / (2**256)
        return int(normalized * 1000) + 200 # ticks will be between 200 and 1200

    def _set_fg_col(self, col_num, ground_y, biome, set_to_func):
        x = self.start_x + col_num
        if col_num == 0 or col_num == self.width - 1:
            for y in range(self.leaves_start_elev-2, self.leaves_start_elev+1):
                ticks = self.get_ticks(x, y)
                set_to_func(x, y, Leaves, pass_through=True, anchor_x=self.anchor_x, anchor_y=self.anchor_y, tick_threshold=ticks)
        elif col_num == self.distance_to_stump_x:
            for y in range(self.leaves_start_elev-2, self.leaves_start_elev+1):
                ticks = self.get_ticks(x, y)
                set_to_func(x, y, Leaves, pass_through=True, anchor_x=self.anchor_x, anchor_y=self.anchor_y, tick_threshold=ticks)
            
            for y in range(self.start_y-self.tree_height, ground_y):
                set_to_func(x, y, Log)

    @classmethod
    def get_x_for_start_y(cls, start_x: int, structure_odds: float) -> int:
        return start_x + cls.distance_to_stump_x
    
    @classmethod
    def get_width(cls, structure_odds):
        return cls.width


class Col_Snow_Tree(Col_Structures):
    width = 3
    distance_to_stump_x = 1
    def __init__(self, structure_odds, start_x, start_y, end_y, grid, chunk, x_offset):
        self.start_x = start_x
        self.global_start_x = x_offset + start_x
        self.start_y = start_y
        self.end_y = end_y
        self.struct_seed = structure_odds
        self.grid = grid
        self.chunk = chunk
        self.x_offset = x_offset

        tree_height_chance = self.get_random_float(f'{self.global_start_x}_tree_height')
        if tree_height_chance < 0.0001: self.tree_height = 4
        elif tree_height_chance < 0.2: self.tree_height = 1
        elif tree_height_chance < 0.4: self.tree_height = 3
        else: self.tree_height = 2

        self.leaves_start_elev = start_y - self.tree_height - 1

        self.anchor_x = self.start_x + self.distance_to_stump_x
        self.anchor_y = self.start_y - 1

    def get_ticks(self, x, y):
        value = int(hashlib.sha256(f"{self.struct_seed}_{x}_{y}".encode()).hexdigest(), 16)
        normalized = value / (2**256)
        return int(normalized * 1000) + 200 # ticks will be between 200 and 1200

    def _set_fg_col(self, col_num, ground_y, biome, set_to_func):
        # add leaves
        x = self.start_x + col_num
        if col_num == 0 or col_num == self.width - 1:
            for y in range(self.leaves_start_elev-1, self.leaves_start_elev+1):
                ticks = self.get_ticks(x, y)
                set_to_func(x, y, Snow_Leaves, pass_through=True, anchor_x=self.anchor_x, anchor_y=self.anchor_y, tick_threshold=ticks)
            y = self.leaves_start_elev-2
            ticks = self.get_ticks(x, y)
            set_to_func(x, y, Snow_Leaves_Top, pass_through=True, anchor_x=self.anchor_x, anchor_y=self.anchor_y, tick_threshold=ticks)
        elif col_num == self.distance_to_stump_x:
            for y in range(self.leaves_start_elev-1, self.leaves_start_elev+1):
                ticks = self.get_ticks(x, ground_y)
                set_to_func(x, y, Snow_Leaves, pass_through=True, anchor_x=self.anchor_x, anchor_y=self.anchor_y, tick_threshold=ticks)
            y = self.leaves_start_elev-2
            ticks = self.get_ticks(x, y)
            set_to_func(x, y, Snow_Leaves_Top, pass_through=True, anchor_x=self.anchor_x, anchor_y=self.anchor_y, tick_threshold=ticks)

            for y in range(self.start_y-self.tree_height, ground_y):
                set_to_func(x, y, Log)


    @classmethod
    def get_x_for_start_y(cls, start_x: int, structure_odds: float) -> int:
        return start_x + cls.distance_to_stump_x
    
    @classmethod
    def get_width(cls, structure_odds):
        return cls.width


class Col_Spruce_Tree(Col_Structures):
    width = 3
    distance_to_stump_x = 1
    def __init__(self, structure_odds, start_x, start_y, end_y, grid, chunk, x_offset):
        self.start_x = start_x
        self.global_start_x = x_offset + start_x
        self.start_y = start_y
        self.end_y = end_y
        self.struct_seed = structure_odds
        self.grid = grid
        self.chunk = chunk
        self.x_offset = x_offset


        tree_height_chance = self.get_random_float(f'{self.global_start_x}_spruce_tree_height')
        if tree_height_chance < 0.1: self.tree_height = 5
        elif tree_height_chance < 0.4: self.tree_height = 3
        else: self.tree_height = 4

        self.leaves_start_elev = start_y - self.tree_height - 1

        self.anchor_x = self.start_x + self.distance_to_stump_x
        self.anchor_y = self.start_y - 1

    def get_ticks(self, x, y):
        value = int(hashlib.sha256(f"{self.struct_seed}_{x}_{y}".encode()).hexdigest(), 16)
        normalized = value / (2**256)
        return int(normalized * 1000) + 200 # ticks will be between 200 and 1200

    def _set_fg_col(self, col_num, ground_y, biome, set_to_func):
        # add leaves
        if col_num == 0 or col_num == self.width - 1:
            x = self.start_x + col_num

            y = self.leaves_start_elev-2
            ticks = self.get_ticks(x, y)
            set_to_func(x, y, Spruce_Leaves, pass_through=True, anchor_x=self.anchor_x, anchor_y=self.anchor_y, tick_threshold=ticks)

            y = self.leaves_start_elev
            ticks = self.get_ticks(x, y)
            set_to_func(x, y, Spruce_Leaves, pass_through=True, anchor_x=self.anchor_x, anchor_y=self.anchor_y, tick_threshold=ticks)

        elif col_num == self.distance_to_stump_x:
            x = self.start_x + col_num
            for y in range(self.leaves_start_elev-3, self.leaves_start_elev-1):
                ticks = self.get_ticks(x, ground_y)
                set_to_func(x, y, Spruce_Leaves, pass_through=True, anchor_x=self.anchor_x, anchor_y=self.anchor_y, tick_threshold=ticks)

            for y in range(self.start_y-self.tree_height, ground_y):
                set_to_func(x, y, Spruce_Log)

            y = self.leaves_start_elev
            ticks = self.get_ticks(x, y)
            set_to_func(x, y, Spruce_Leaves, pass_through=True, anchor_x=self.anchor_x, anchor_y=self.anchor_y, tick_threshold=ticks)

            set_to_func(x, self.leaves_start_elev-1, Spruce_Log, pass_through=True) # adding the extra log


    @classmethod
    def get_x_for_start_y(cls, start_x: int, structure_odds: float) -> int:
        return start_x + cls.distance_to_stump_x
    
    @classmethod
    def get_width(cls, structure_odds):
        return cls.width


class Col_Mahogany_Tree(Col_Structures):
    width = 5
    distance_to_stump_x = 2
    def __init__(self, structure_odds, start_x, start_y, end_y, grid, chunk, x_offset):
        self.start_x = start_x
        self.global_start_x = x_offset + start_x
        self.start_y = start_y
        self.end_y = end_y
        self.struct_seed = structure_odds
        self.grid = grid
        self.chunk = chunk
        self.x_offset = x_offset

        tree_height_chance = self.get_random_float(f'{self.global_start_x}_mahogany_tree_height')
        if tree_height_chance < 0.15: self.tree_height = 3
        elif tree_height_chance < 0.35: self.tree_height = 5
        else: self.tree_height = 4

        self.leaves_start_elev = start_y - self.tree_height - 1

        self.anchor_x = self.start_x + self.distance_to_stump_x
        self.anchor_y = self.start_y - 1

    def get_ticks(self, x, y):
        value = int(hashlib.sha256(f"{self.struct_seed}_{x}_{y}".encode()).hexdigest(), 16)
        normalized = value / (2**256)
        return int(normalized * 1000) + 200 # ticks will be between 200 and 1200

    def _set_fg_col(self, col_num, ground_y, biome, set_to_func):
        # add leaves
        if col_num == 0 or col_num == self.width - 1:
            x = self.start_x + col_num
            y = self.leaves_start_elev
            ticks = self.get_ticks(x, ground_y)
            set_to_func(x, y, Mahogany_Leaves, pass_through=True, anchor_x=self.anchor_x, anchor_y=self.anchor_y, tick_threshold=ticks)
        elif col_num > 0 and col_num - 1 < self.width:
            x = self.start_x + col_num
            for y in range(self.leaves_start_elev-1, self.leaves_start_elev+1):
                ticks = self.get_ticks(x, ground_y)
                set_to_func(x, y, Mahogany_Leaves, pass_through=True, anchor_x=self.anchor_x, anchor_y=self.anchor_y, tick_threshold=ticks)

        # add stump
        if col_num == self.distance_to_stump_x:
            x = self.start_x + col_num
            for y in range(self.start_y-self.tree_height, ground_y):
                set_to_func(x, y, Mahogany_Log)

        # add side leaves
        if col_num == 1 or col_num == self.width - 2:
            side_leaf_odds = self.get_random_float(f'{self.global_start_x}_mahogany_leaves_side_chance')
            y = self.leaves_start_elev + 2
            x = self.start_x + col_num
            if side_leaf_odds < 0.35: # put left
                if col_num == 1:
                    ticks = self.get_ticks(x, y)
                    set_to_func(x, y, Mahogany_Leaves, pass_through=True, anchor_x=self.anchor_x, anchor_y=self.anchor_y, tick_threshold=ticks)
            if side_leaf_odds > 0.65: # put right
                if col_num == self.width - 2:
                    ticks = self.get_ticks(x, y)
                    set_to_func(x, y, Mahogany_Leaves, pass_through=True, anchor_x=self.anchor_x, anchor_y=self.anchor_y, tick_threshold=ticks)


    @classmethod
    def get_x_for_start_y(cls, start_x: int, structure_odds: float) -> int:
        return start_x + cls.distance_to_stump_x
    
    @classmethod
    def get_width(cls, structure_odds):
        return cls.width


class Col_Puddle(Col_Structures):
    width = 1
    def __init__(self, structure_odds, start_x, start_y, end_y, grid, chunk, x_offset):
        self.start_x = start_x
        self.end_y = end_y
        self.struct_seed = structure_odds
        self.grid = grid
        self.chunk = chunk
        self.x_offset = x_offset

    def _set_fg_col(self, col_num, ground_y, biome, set_to_func):
        set_to_func(self.start_x, ground_y, Water)

    @classmethod
    def get_x_for_start_y(cls, start_x: int, structure_odds: float) -> int:
        return start_x

    @classmethod
    def get_width(cls, structure_odds):
        return cls.width


class Col_Wild_Flower_Struct(Col_Structures):
    width = 1
    def __init__(self, structure_odds, start_x, start_y, end_y, grid, chunk, x_offset):
        self.start_x = start_x
        self.end_y = end_y
        self.struct_seed = structure_odds
        self.grid = grid
        self.chunk = chunk
        self.x_offset = x_offset

    def _set_fg_col(self, col_num, ground_y, biome, set_to_func):
        set_to_func(self.start_x, ground_y-1, Wild_Flower)

    @classmethod
    def get_x_for_start_y(cls, start_x: int, structure_odds: float) -> int:
        return start_x

    @classmethod
    def get_width(cls, structure_odds):
        return cls.width


class Col_White_Lily_Struct(Col_Structures):
    width = 1
    def __init__(self, structure_odds, start_x, start_y, end_y, grid, chunk, x_offset):
        self.start_x = start_x
        self.end_y = end_y
        self.struct_seed = structure_odds
        self.grid = grid
        self.chunk = chunk
        self.x_offset = x_offset

    def _set_fg_col(self, col_num, ground_y, biome, set_to_func):
        set_to_func(self.start_x, ground_y-1, White_Lily)

    @classmethod
    def get_x_for_start_y(cls, start_x: int, structure_odds: float) -> int:
        return start_x

    @classmethod
    def get_width(cls, structure_odds):
        return cls.width


class Col_Forget_Me_Not_Struct(Col_Structures):
    width = 1
    def __init__(self, structure_odds, start_x, start_y, end_y, grid, chunk, x_offset):
        self.start_x = start_x
        self.end_y = end_y
        self.struct_seed = structure_odds
        self.grid = grid
        self.chunk = chunk
        self.x_offset = x_offset

    def _set_fg_col(self, col_num, ground_y, biome, set_to_func):
        set_to_func(self.start_x, ground_y-1, Forget_Me_Not)

    @classmethod
    def get_x_for_start_y(cls, start_x: int, structure_odds: float) -> int:
        return start_x

    @classmethod
    def get_width(cls, structure_odds):
        return cls.width


class Col_Rose_Struct(Col_Structures):
    width = 1
    def __init__(self, structure_odds, start_x, start_y, end_y, grid, chunk, x_offset):
        self.start_x = start_x
        self.end_y = end_y
        self.struct_seed = structure_odds
        self.grid = grid
        self.chunk = chunk
        self.x_offset = x_offset

    def _set_fg_col(self, col_num, ground_y, biome, set_to_func):
        set_to_func(self.start_x, ground_y-1, Rose)

    @classmethod
    def get_x_for_start_y(cls, start_x: int, structure_odds: float) -> int:
        return start_x

    @classmethod
    def get_width(cls, structure_odds):
        return cls.width


class Col_Watermellon_Patch(Col_Structures):
    width = 1
    def __init__(self, structure_odds, start_x, start_y, end_y, grid, chunk, x_offset):
        self.start_x = start_x
        self.end_y = end_y
        self.struct_seed = structure_odds
        self.grid = grid
        self.chunk = chunk
        self.x_offset = x_offset

    def _set_fg_col(self, col_num, ground_y, biome, set_to_func):
        set_to_func(self.start_x, ground_y-1, Watermellon)

    @classmethod
    def get_x_for_start_y(cls, start_x: int, structure_odds: float) -> int:
        return start_x

    @classmethod
    def get_width(cls, structure_odds):
        return cls.width


class Col_Small_Bush(Col_Structures):
    width = 1
    def __init__(self, structure_odds, start_x, start_y, end_y, grid, chunk, x_offset):
        self.start_x = start_x
        self.end_y = end_y
        self.struct_seed = structure_odds
        self.grid = grid
        self.chunk = chunk
        self.x_offset = x_offset

    def _set_fg_col(self, col_num, ground_y, biome, set_to_func):
        set_to_func(self.start_x, ground_y-1, Leaves, pass_through=True)
    
    @classmethod
    def get_x_for_start_y(cls, start_x: int, structure_odds: float) -> int:
        return start_x

    @classmethod
    def get_width(cls, structure_odds):
        return cls.width


class Col_Recipe_Burrow(Col_Structures):
    width = 9
    def __init__(self, structure_odds, start_x, start_y, end_y, grid, chunk, x_offset):
        self.start_x = start_x
        self.global_x = start_x + x_offset
        self.start_y = start_y
        self.end_y = end_y
        self.struct_seed = structure_odds
        self.grid = grid
        self.chunk = chunk
        self.x_offset = x_offset

        self.height = 3

        self.is_reversed = False
        self.use_start_y = start_y
        if self.start_y < self.end_y:
            self.is_reversed = True
            self.use_start_y = end_y

    def _set_fg_col(self, col_num, ground_y, biome, set_to_func):
        x = self.start_x + col_num
        adjusted_col_num = self.get_adjusted_col_num(col_num)
        if adjusted_col_num >= 0 and adjusted_col_num < 2: # add the floor & ceiling
            set_to_func(x, self.use_start_y-self.height, Wood_Planks)
            for y in range(self.use_start_y-self.height+1, self.use_start_y):
                set_to_func(x, y, None)
            set_to_func(x, self.use_start_y, Wood_Planks)
        elif adjusted_col_num == 2:
            set_to_func(x, self.use_start_y-self.height, Wood_Planks)
            for y in range(self.use_start_y-self.height+1, self.use_start_y):
                set_to_func(x, y, None)
            set_to_func(x, self.use_start_y, Wood_Planks)
            set_to_func(x, self.use_start_y+1, Wood_Planks)
        elif adjusted_col_num == 3:
            set_to_func(x, self.use_start_y-self.height, Wood_Planks)
            for y in range(self.use_start_y-self.height+1, self.use_start_y+1):
                set_to_func(x, y, None)
            set_to_func(x, self.use_start_y+1, Wood_Planks)
            set_to_func(x, self.use_start_y+2, Wood_Planks)
        elif adjusted_col_num == 4:
            set_to_func(x, self.use_start_y-self.height, Wood_Planks)
            set_to_func(x, self.use_start_y-self.height+1, Wood_Planks)
            for y in range(self.use_start_y-self.height+2, self.use_start_y+2):
                set_to_func(x, y, None)
            set_to_func(x, self.use_start_y+2, Wood_Planks)
        elif adjusted_col_num == 5:
            set_to_func(x, self.use_start_y-self.height+1, Wood_Planks)
            set_to_func(x, self.use_start_y-self.height+2, Wood_Planks)
            for y in range(self.use_start_y-self.height+3, self.use_start_y+2):
                set_to_func(x, y, None)
            set_to_func(x, self.use_start_y+2, Wood_Planks)
        elif adjusted_col_num == 6 or adjusted_col_num == 7:
            set_to_func(x, self.use_start_y-self.height+2, Wood_Planks)
            for y in range(self.use_start_y-self.height+3, self.use_start_y+2):
                set_to_func(x, y, None)
            set_to_func(x, self.use_start_y+2, Wood_Planks)
        elif adjusted_col_num == 8:
            for y in range(self.use_start_y-self.height+2, self.use_start_y+3):
                set_to_func(x, y, Wood_Planks)

        if adjusted_col_num == 0: # add the doors
            set_to_func(x, self.use_start_y-self.height+1, Door_Top)
            set_to_func(x, self.use_start_y-1, Door_Bottom)

        if adjusted_col_num == 6:
            biome_name = biome.__name__
            recipeList = User_Crafting_Recipes_List.getBiomeWeightedFindableRecipesList(biome_name)
            index = int(self.get_random_float(f'{self.global_x}_recipe') * len(recipeList)) % len(recipeList)
            randomRecipe = recipeList[index]
            set_to_func(x, self.use_start_y+1, Recipe_Frame, stored_inventory_items=[randomRecipe])

    def _set_bg_col(self, col_num, fg_ground_y, biome, set_to_func):
        adjusted_col_num = col_num
        x = self.start_x + col_num
        adjusted_col_num = self.get_adjusted_col_num(col_num)
        if adjusted_col_num >= 0 and adjusted_col_num < 2: # add the floor & ceiling
            for y in range(self.use_start_y-self.height, self.use_start_y+1):
                set_to_func(x, y, Wood_Planks)
        elif adjusted_col_num == 2:
            for y in range(self.use_start_y-self.height, self.use_start_y+2):
                set_to_func(x, y, Wood_Planks)
        elif adjusted_col_num == 3:
            for y in range(self.use_start_y-self.height, self.use_start_y+3):
                set_to_func(x, y, Wood_Planks)
        elif adjusted_col_num == 4:
            for y in range(self.use_start_y-self.height+1, self.use_start_y+3):
                set_to_func(x, y, Wood_Planks)
        elif adjusted_col_num == 5:
            for y in range(self.use_start_y-self.height+2, self.use_start_y+3):
                set_to_func(x, y, Wood_Planks)
        elif adjusted_col_num == 6 or adjusted_col_num == 7:
            for y in range(self.use_start_y-self.height+2, self.use_start_y+3):
                set_to_func(x, y, Wood_Planks)
        elif adjusted_col_num == 8:
            for y in range(self.use_start_y-self.height+2, self.use_start_y+3):
                set_to_func(x, y, Wood_Planks)

    def get_adjusted_col_num(self, col_num):
        if self.is_reversed:
            return self.width - col_num - 1
        return col_num
    
    @classmethod
    def get_x_for_start_y(cls, start_x: int, structure_odds: float) -> int:
        return start_x

    @classmethod
    def get_width(cls, structure_odds):
        return cls.width


class Col_Recipe_Cave(Col_Structures):
    width = 6
    def __init__(self, structure_odds, start_x, start_y, end_y, grid, chunk, x_offset):
        self.start_x = start_x
        self.global_x = start_x + x_offset
        self.start_y = start_y
        self.end_y = end_y
        self.struct_seed = structure_odds
        self.grid = grid
        self.chunk = chunk
        self.x_offset = x_offset

        self.height = 6
        min_depth = start_y + 10
        if min_depth + self.height >= grid.height: self.depth = start_y + 3
        else: self.depth = self.get_random_int(min_depth, grid.height - 7, f'{self.global_x}_recipe_cave_depth')
        self.chest_loot = Chest_Loot([
            Loot_Odds(Rose, 3, 0.025),
            Loot_Odds(White_Lily, 3, 0.025),
            Loot_Odds(Packed_Ice, 15, 0.06),
            Loot_Odds(Spruce_Planks, 15, 0.06),
            Loot_Odds(Spruce_Log, 4, 0.02),
            Loot_Odds(Gravel, 15, 0.06),
            Loot_Odds(Gold_Ingot, 4, 0.0008),
            Loot_Odds(Iron_Ingot, 4, 0.0008),
            Loot_Odds(Diamond, 2, 0.00045),
        ])

    def _set_fg_col(self, col_num, ground_y, biome, set_to_func):
        x = col_num + self.start_x
        if col_num == 0 or col_num == self.width - 1: # left or right side
            for y in range(self.depth, self.depth+self.height):
                set_to_func(x, y, Stone_Bricks)
        else:
            set_to_func(x, self.depth, Stone_Bricks)
            set_to_func(x, self.depth+self.height-1, Stone_Bricks)
            for y in range(self.depth+1, self.depth+self.height-1):
                set_to_func(x, y, None)

        if col_num == 2:
            recipeFrame_y = self.depth + 4
            recipeList = User_Crafting_Recipes_List.getBiomeWeightedFindableRecipesList(biome.__name__)
            randomRecipe = recipeList[int(self.struct_seed * len(recipeList)) % len(recipeList)]
            set_to_func(x, recipeFrame_y, Recipe_Frame, stored_inventory_items=[randomRecipe])

        if col_num == 3:
            chest_y = self.depth + 4
            set_to_func(x, chest_y, Spruce_Chest)
            chest_block = self.chunk.get(x, chest_y)
            if chest_block is not None:
                for chest_slot_num in range(chest_block.chest_slots_count):
                    chest_loot_random_factor = self.get_random_float(f'{self.struct_seed}_{chest_slot_num}')
                    chest_block.stored_inventory_items.append(self.chest_loot.get_slot(chest_loot_random_factor))

    def _set_bg_col(self, col_num, fg_ground_y, biome, set_to_func):
        x = col_num + self.start_x
        for y in range(self.depth, self.depth+self.height):
            set_to_func(x, y, Spruce_Planks)
    
    @classmethod
    def get_x_for_start_y(cls, start_x: int, structure_odds: float) -> int:
        return start_x

    @classmethod
    def get_width(cls, structure_odds):
        return cls.width
