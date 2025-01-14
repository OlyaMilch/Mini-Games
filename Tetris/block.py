from colors import Colors
import pygame as pg
from position import Position


# Create a Block class and use inheritance to rotate the blocks as they fall

class Block:
    def __init__(self, id):
        self.id = id
        self.cells = {}  # Dictionary of cells for rotating blocks
        self.cell_size = 30
        self.row_offset = 0
        self.column_offset = 0
        self.rotation_state = 0  # Block rotation state
        self.colors = Colors.get_cell_colors()  # List of all colors for drawing blocks on the screen

    # Block offset on the game grid
    def move(self, rows, columns):
        self.row_offset += rows
        self.column_offset += columns

    # Returns the positions of occupied cells
    def get_cell_positions(self):
        tiles = self.cells[self.rotation_state]  # Getting the default cell position
        moved_tiles = []  # List for storing moved tiles
        for position in tiles:
            position = Position(position.row + self.row_offset, position.column + self.column_offset)
            moved_tiles.append(position)
        return moved_tiles

    # Rotate blocks
    def rotate(self):
        self.rotation_state += 1
        if self.rotation_state == len(self.cells):  # Checking the number of block revolutions (4 in total)
            self.rotation_state = 0

    # So that during rotation the block does not go beyond the window frame
    def undo_rotation(self):
        self.rotation_state -= 1
        if self.rotation_state == 0:
            self.rotation_state = len(self.cells) - 1

    def draw(self, screen):
        tiles = self.get_cell_positions()
        for tile in tiles:
            title_rect = pg.Rect(tile.column * self.cell_size + 11, tile.row * self.cell_size + 11,
                                 self.cell_size - 1, self.cell_size - 1)
            pg.draw.rect(screen, self.colors[self.id], title_rect)