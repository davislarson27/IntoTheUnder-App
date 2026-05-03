
class LakePreFill:
    def __init__(self, start_x, start_y):
        self.start_x = start_x
        self.start_y = start_y
        self.end_x = start_x
        self.end_y = start_y

        self.water_level = None
        self.max_depth = None
        self.ground_level_equation = None

    def extend_x(self, next_x, next_y):
        self.end_x = next_x
        self.end_y = next_y
        
    def calculate_lake(self): # this will determine where fading will happen, how it will happen, 
        self.start_x+=1
        self.end_x-=1
        width = self.end_x - self.start_x
        self.water_level = max(self.start_y, self.end_y) + 1 # drops water level below threshold (prevents overflowing)
        self.max_depth = min(width * 0.3, 40)

    def get_floor_height(self, x):
        t = (x - self.start_x) / (self.end_x - self.start_x)
        bowl = 4 * t * (1 - t)
        baseline = self.start_y + (self.end_y - self.start_y) * t  # lerp between shores
        return int(baseline + bowl * self.max_depth)  # + because y increases downward

    def is_lake(self, x):
        return self.start_x <= x <= self.end_x
    
    def is_end_of_lake(self, x):
        return x == self.end_x
    
    def get_water_level(self):
        return self.water_level
    
    def is_valid_lake(self):
        return self.start_y <= self.water_level and self.end_y <= self.water_level and self.end_x - self.start_x > 1

    def __str__(self):
        return f'range = ({self.start_x},{self.end_x})'
