class Physics_Rules:
    def __init__(self, screen, inventory_height):
        # set physics rules
        self.Y_ACCELERATION = 1.25
        self.WATER_UPWARD_ACCEL = -0.05
        self.JUMP_VELOCITY = -15

        self.BUILD_HOLD_THRESHOLD = 10 # count of frames held before destroyed motion happens

        self.true_height = screen.get_height() - inventory_height
        self.MOVEMENT_ALTITUDE_PX = (self.true_height * 11.5) // 16
