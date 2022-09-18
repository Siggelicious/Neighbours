from cell import Cell, COLOR
import settings
import random

# The bread and butter of the program.
class World:
    # Defines what a 'neighbour' is in relation to itself (a cell).
    neighbour_offsets = [
        (-1, -1),
        (-1, 0),
        (-1, 1),
        (0, -1),
        (0, 1),
        (1, -1),
        (1, 0),
        (1, 1)
    ]

    # This init does a few things (in order):
    #   It creates a world, and populates it with empty cells.
    #   It distributes red, blue and vacant cells according to 'settings'.
    #   It gives each cell an initial state.
    def __init__(self):
        self.cell_size = (settings.WINDOW_SIZE[0] // settings.COLS, settings.WINDOW_SIZE[1] // settings.ROWS) # For rendering.
        self.grid = [[Cell() for col in range(settings.COLS)] for row in range(settings.ROWS)]
        for row in range(settings.ROWS):
            for col in range(settings.COLS):
                cell = self.grid[row][col]
                if random.random() > settings.VACANT_INCIDENCE:
                    if random.random() <= settings.RED_INCIDENCE:
                        cell.type = Cell.Type.RED
                    else:
                        cell.type = Cell.Type.BLUE

                for (offset_row, offset_col) in self.neighbour_offsets:
                    if self.is_valid(row + offset_row, col + offset_col):
                        cell.neighbours.append(self.grid[row + offset_row][col + offset_col])
        
        for row in self.grid:
            for cell in row:
                cell.refresh_state()
        
    # To make sure a cell isn't out of scope.
    def is_valid(self, row, col):
        return 0 <= row < settings.ROWS and 0 <= col < settings.COLS

    # Resolves the world one round.
    def resolve(self):
        unsatisfied = []
        vacant = []
        # Gathers all the unsatisfied and vacant cells. This probably could be optimized a bit but what the hell.
        for row in self.grid:
            for agent in row:
                if agent.type == Cell.Type.VACANT:
                    vacant.append(agent)
                else:
                    if agent.state == Cell.State.UNSATISFIED:
                        unsatisfied.append(agent)

        num_unsatisfied = len(unsatisfied) # We save the number of unsatisfied cells for the return statement.
        # Basically:
        #   Takes a random unsatisfied cell and a random vacant cell and swaps them.
        #   Refreshes the state of both cells.
        #   Broadcasts to all neighbouring cells that we did something.
        while len(unsatisfied) > 0 and len(vacant) > 0:
            origin = unsatisfied.pop(random.randint(0, len(unsatisfied) - 1))
            dest = vacant.pop(random.randint(0, len(vacant) - 1))
            dest.type = origin.type
            origin.type = Cell.Type.VACANT
            origin.refresh_state()
            dest.refresh_state()
            origin.broadcast_type_change()
            dest.broadcast_type_change()
        
        return 1 - num_unsatisfied / (settings.ROWS * settings.COLS) # To let the loop now how satisfied the world is.

    # Renders all the things. PySDL2 docs explains this.
    def render(self, graphics):
        graphics.fill_rect((0, 0, settings.WINDOW_SIZE[0], settings.WINDOW_SIZE[1]), (0, 0, 0, 255))
        for row in range(settings.ROWS):
            for col in range(settings.COLS):
                cell = self.grid[row][col]
                graphics.fill_rect(
                    (col * self.cell_size[0], row * self.cell_size[1], *self.cell_size),
                    COLOR[cell.type]
                    )
