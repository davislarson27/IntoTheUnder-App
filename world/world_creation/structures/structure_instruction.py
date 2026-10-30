class Var_Structure_Instruction:
    def __init__(self, x, y_start, block, if_block=None, direction=1):
        self.x = x
        self.y_start = y_start
        self.block = block
        self.if_block = if_block
        self.direction = direction

    def modify_surrounding_grid(self, grid):        
        y = self.y_start
        if self.if_block is None:
            if_block = type(None)
        else:
            if_block = self.if_block
        while isinstance(grid.get(self.x, y), if_block):
            grid.set(self.x, y, self.block)
            y += self.direction
            if y > grid.height:
                return
