class Crafting_Recipe:
    def __init__(self, recipe_name, requirement_list, output=None):
        self.name = recipe_name
        self.requirement_list = requirement_list
        self.output = output

class Ingredient:
    def __init__(self, block_type, count):
        self.block_type = block_type
        self.count = count
