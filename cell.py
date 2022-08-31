import settings
import enum

class Cell:
    class Type(enum.Enum):
        VACANT = enum.auto()
        RED = enum.auto(),
        BLUE = enum.auto()

    class State(enum.Enum):
        NA = enum.auto(),
        SATISFIED = enum.auto(),
        UNSATISFIED = enum.auto()

    def __init__(self):
        self.type = Cell.Type.VACANT
        self.state = Cell.State.NA
        self.neighbours = []

    def refresh_state(self):
        if self.type == Cell.Type.VACANT:
            self.state = Cell.State.NA
        else:
            total = same = 0
            
            for neighbour in self.neighbours:
                if neighbour.type != Cell.Type.VACANT:
                    total += 1
            
                    if neighbour.type == self.type:
                        same += 1
            
            if total == 0 or same / total >= settings.THRESHOLD:
                self.state = Cell.State.SATISFIED
            else: 
                self.state = Cell.State.UNSATISFIED

    def broadcast_type_change(self):
        for neighbour in self.neighbours:
            neighbour.refresh_state()

COLOR = {
    Cell.Type.VACANT : (255, 255, 255, 255),
    Cell.Type.RED : (255, 0, 0, 255),
    Cell.Type.BLUE : (0, 0, 255, 255) 
}