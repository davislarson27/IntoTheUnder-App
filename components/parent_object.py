"""not yet in use -> idea code for the future"""

# use during world generation and .physics() for leaves (have generation tie each Leave object to the logs (either base of the tree or a list of these objects))
# when you run physics make sure that if this object in the object is None it doesn't try to run this
#       for the leave example, make the leaves count 
# this will need to be saved and regenerated in the .json grid file so it doens't get lost on reload (not all objects of the same type will have a parent object)

from components.grid import Grid

class Parent_Object: # holds objects that 
    def __init__(self, parent_object_type, parent_object_x, parent_object_y, ticks_parent_object_missing = 0):
        self.parent_object_type = parent_object_type
        self.parent_object_x = parent_object_x
        self.parent_object_y = parent_object_y
        self.ticks_parent_object_missing = ticks_parent_object_missing

    def parent_object_exists(self, grid):
        if type(grid.get(self.parent_object_x, self.parent_object_y)) == self.parent_object_type:
            self.ticks_parent_object_missing += 1
            return True
        else:
            self.ticks_parent_object_missing = 0
            return False