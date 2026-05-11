class Block_Queue:
    def __init__(self, preset_queue=None):
        if preset_queue is None:
            preset_queue = []
        self.queue = preset_queue # expects references to blocks WITH GRID LOCATIONS present

    def append(self, block):
        self.queue.append(block)

    def reset(self):
        self.queue = []

    def __add__(self, other):
        # confirms type is valid
        if not isinstance(other, type(self)):
            raise ValueError
        
        # does not copy lists if one or both are empty
        if len(self.queue) == 0:
            return other
        if len(other) == 0:
            return self
        
        # creates combined list
        return Block_Queue(self.queue + other.queue)
    
    def __len__(self):
        return len(self.queue)

    def draw(self, camera_x, camera_y):
        for block in self.queue:
            if block is not None: block.draw(camera_x=camera_x, camera_y=camera_y)
        self.reset()
