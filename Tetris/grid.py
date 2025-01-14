import pygame as pg
from colors import Colors


"""
The logic of the game is that empty cells have a value of 0 and 7 different shapes have values from 1 to 7. 
These values will be filled as the pieces are placed on the bottom.
"""


class Grid:
    # Create game grid
    def __init__(self):
        self.rows = 20
        self.columns = 10
        self.cell_size = 30
        self.grid = [[0 for j in range(self.columns)] for i in range(self.rows)]
        self.colors = Colors.get_cell_colors()


# The method prevents the block from leaving the game grid.
    def is_inside(self, row, column):
        if row >= 0 and row < self.rows and column >= 0 and column < self.columns:
            return True
        return False

    # Checks whether the cells at the bottom are occupied
    def is_empty(self, row, column):
        if self.grid[row][column] == 0:
            return True
        return False

    # Checks if the row is completely filled
    def is_row_full(self, row):
        for column in range(self.columns):
            if self.grid[row][column] == 0:
                return False
        return True

    # Clears row if it is full
    def clear_row(self, row):
        for column in range(self.columns):
            self.grid[row][column] = 0  # Here 0 is the cleared row

    # Moves rows that are not completely filled to the bottom
    def move_row_down(self, row, rows):
        for column in range(self.columns):
            self.grid[row + rows][column] = self.grid[row][column]
            self.grid[row][column] = 0

    # Checks all rows from bottom to top for filed
    def clear_full_rows(self):
        completed = 0
        for row in range(self.rows -1, 0, -1):
            if self.is_row_full(row):
                self.clear_row(row)  # Clears a filled row
                completed += 1
            elif completed > 0:
                self.move_row_down(row, completed)  # If row is not filled, then move it down
        return completed

    # Clear the playing field
    def reset(self):
        for row in range(self.rows):
            for column in range(self.columns):
                self.grid[row][column] = 0

    # Coloring occupied cells
    def draw(self, screen):
        for row in range(self.rows):
            for column in range(self.columns):
                cell_value = self.grid[row][column]
                cell_rect = pg.Rect(column*self.cell_size + 11, row*self.cell_size + 11,
                self.cell_size -1, self.cell_size -1)  # Coordinates, width and height. Pygame used to work with rectangles.
                pg.draw.rect(screen, self.colors[cell_value], cell_rect)  # 3 arguments: the surface on which the object is drawn, the color and the rectangle
