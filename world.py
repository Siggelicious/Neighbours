from cell import Cell, COLOR
import settings
import random

class World:
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

    def __init__(self):
        self.cell_size = (settings.WINDOW_SIZE[0] // settings.COLS, settings.WINDOW_SIZE[1] // settings.ROWS)
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
        
    def is_valid(self, row, col):
        return 0 <= row < settings.ROWS and 0 <= col < settings.COLS

    def resolve(self):
        unsatisfied = []
        vacant = []

        for row in self.grid:
            for agent in row:
                if agent.type == Cell.Type.VACANT:
                    vacant.append(agent)
                else:
                    if agent.state == Cell.State.UNSATISFIED:
                        unsatisfied.append(agent)

        while len(unsatisfied) > 0 and len(vacant) > 0:
            origin = unsatisfied.pop(random.randint(0, len(unsatisfied) - 1))
            dest = vacant.pop(random.randint(0, len(vacant) - 1))
            dest.type = origin.type
            origin.type = Cell.Type.VACANT
            origin.refresh_state()
            dest.refresh_state()
            origin.broadcast_type_change()
            dest.broadcast_type_change()

    def render(self, graphics):
        graphics.fill_rect((0, 0, settings.WINDOW_SIZE[0], settings.WINDOW_SIZE[1]), (0, 0, 0, 255))
        
        for row in range(settings.ROWS):
            for col in range(settings.COLS):
                cell = self.grid[row][col]
                graphics.fill_rect(
                    (col * self.cell_size[0], row * self.cell_size[1], *self.cell_size),
                    COLOR[cell.type]
                    )