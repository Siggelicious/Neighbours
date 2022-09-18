# Module containing all the code for class 'Cell'.
import settings
import enum

class Cell:
    # Enum that defines the cell's type. A cell can be red, blue or vacant.
    class Type(enum.Enum):
        VACANT = enum.auto()
        RED = enum.auto(),
        BLUE = enum.auto()

    # Enum that defines the cell's state. A cell that is not vacant be either satisfied or unsatisfied. A cell that is vacant will always have the state 'NA' (non-applicable). 
    class State(enum.Enum): # inherits from enum.Enum. Brings some nice QoL functions. 
        NA = enum.auto(), # The enum.auto() function returns a signed integer > 0.
        SATISFIED = enum.auto(),
        UNSATISFIED = enum.auto()

    # Initializes a default empty Cell. 
    def __init__(self):
        self.type = Cell.Type.VACANT
        self.state = Cell.State.NA
        self.neighbours = [] # A list containing references to all adjacent cells (north west, north, north east, west, east, south west, south, south east).

    # Evaluates the cell's current state.
    def refresh_state(self):
        if self.type == Cell.Type.VACANT:
            self.state = Cell.State.NA
        else:
            total = same = 0
            # 'total': The number of neighbor who's type isn't 'VACANT'.
            # 'same': The number of neighbor who's type is equal to 'self.type'.
            for neighbour in self.neighbours:
                if neighbour.type != Cell.Type.VACANT:
                    total += 1
            
                    if neighbour.type == self.type:
                        same += 1
            
            if total == 0 or same / total >= settings.THRESHOLD: 
                self.state = Cell.State.SATISFIED
            else: 
                self.state = Cell.State.UNSATISFIED

    # Broadcasts that the type has been changed to all neighboring cells.
    def broadcast_type_change(self):
        for neighbour in self.neighbours:
            neighbour.refresh_state()

COLOR = {
    Cell.Type.VACANT : (255, 255, 255, 255),
    Cell.Type.RED : (255, 0, 0, 255),
    Cell.Type.BLUE : (0, 0, 255, 255) 
}
