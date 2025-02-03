import random
from tile import Tile
import pygame as py


class Board(object):
    def __init__(self, width, height, tile_size, screen):
        self.run = True
        self.width = width
        self.height = height
        self.tile_size = tile_size
        self.screen: py.Surface = screen
        self.rows = height // tile_size
        self.cols = width // tile_size
        self.grid = []
        self.num_mines = 2  # You can adjust this or make it a parameter
        self.debug = False
        self.flags = 0

        self.initialize_grid()
        self.place_mines()

        if self.debug is True:
            self.rev_debug()

    def draw_rect_alpha(self, color):
        screen = py.display.get_surface()
        for row in self.grid:
            for tile in row:
                shape_surf = py.Surface((tile.size, tile.size), py.SRCALPHA)
                py.draw.rect(shape_surf, color, shape_surf.get_rect())
                screen.blit(shape_surf, (tile.x, tile.y))

    def initialize_grid(self):
        for x in range(self.cols):
            row = []
            for y in range(self.rows):
                tile = Tile(x * self.tile_size,
                            y * self.tile_size,
                            self.tile_size,
                            self.screen)
                row.append(tile)
            self.grid.append(row)

    def place_mines(self):
        coordinates = [(x, y) for x in range(self.cols) for y in range(self.rows)]
        minePositions = random.sample(coordinates, self.num_mines)

        for x, y in minePositions:
            self.grid[y][x].bee = True

    def reveal_tile(self, x, y):
        tile = self.grid[x][y]
        tile.reveal()
        if tile.bee:
            print("Game Over!")

    def flag_tile(self, x, y):
        tile = self.grid[x][y]
        if not tile.revealed:
            tile.flag()

    def count_adjacent_mines(self, x, y, tile):
        count = 0
        if not tile.bee:
            for offsetX in [-1, 0, 1]:
                for offsetY in [-1, 0, 1]:
                    if offsetX == 0 and offsetY == 0:
                        continue
                    newX, newY = x + offsetX, y + offsetY
                    if 0 <= newX < self.cols and 0 <= newY < self.rows:
                        if self.grid[newX][newY].bee:
                            count += 1
            tile.count = count
        else:
            tile.count = -1

    def reveal_adjacent_tiles(self, x, y, tile):
        if tile.count == 0:
            for offsetX in [-1, 0, 1]:
                for offsetY in [-1, 0, 1]:
                    if offsetX == 0 and offsetY == 0:
                        continue
                    newX, newY = x + offsetX, y + offsetY
                    if 0 <= newX < self.cols and 0 <= newY < self.rows:
                        new_tile = self.grid[newX][newY]
                        if not new_tile.revealed:
                            self.count_adjacent_mines(newX, newY, new_tile)
                            self.reveal_tile(newX, newY)
                            self.reveal_adjacent_tiles(newX, newY, new_tile)

    def draw(self):
        for row in self.grid:
            for tile in row:
                tile.draw()

    def rev_debug(self):
        for row in self.grid:
            for tile in row:
                self.count_adjacent_mines(tile.x, tile.y, tile)
                tile.reveal()
        py.display.flip()  # Force a full screen update

    def check_game(self):
        revealed_tiles = 0
        flagged_bees = 0  # Reset flagged count each time

        for row in self.grid:
            for tile in row:
                if tile.revealed and tile.bee:
                    self.run = False
                    self.draw_rect_alpha((255, 0, 0, 58))
                    py.image.save(self.screen, "images/lost.jpg")
                if tile.revealed:
                    revealed_tiles += 1
                if tile.bee and tile.flagged:
                    flagged_bees += 1  # Only count flagged bees

        # Reset self.flags before updating to avoid accumulation issues
        self.flags = flagged_bees

        # Check winning condition *only once*
        if self.flags == self.num_mines and all(tile.flagged for row in self.grid for tile in row if tile.bee):
            print('Game Won!')

            self.run = False
            self.draw_rect_alpha((0, 255, 0, 58))
            py.image.save(self.screen, "images/won.jpg")
