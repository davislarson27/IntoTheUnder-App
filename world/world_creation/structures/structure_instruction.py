class Structure_Instruction:
    def __init__(self, x, y, block, blockIsInitialized=False):
        """takes x, y, and block"""
        self.x = x
        self.y = y
        self.block = block
        self.blockIsInitialized = blockIsInitialized
    
    def getCoordinates(self):
        return self.x, self.y
        
    def setBlock(self, grid):
        if self.blockIsInitialized:
            grid.set_manual(self.x, self.y, self.block)
        else:
            grid.set(self.x, self.y, self.block)
