from sys import exit
from random import randint
import pygame as pg


class Tile:
    def __init__(self, col, row, size):
        self.col = col
        self.row = row
        self.size = size
        self.bomb = False
        self.revealed = False
        self.image = pg.image.load("images\\Tile_hidden.png").convert()
        self.image = pg.transform.scale(self.image, (size, size))
        self.rect = self.image.get_rect()
        self.rect = self.rect.move((col * size, row * size))
        screen.blit(self.image, self.rect)

    def get_neighbours(self):
        #  Get 8 surrounding neighbours
        #  If at an edge, ignore nonexistent neighbours
        global tiles, rows, cols
        near_tiles = []

        near_rows = tiles[self.row - 1: self.row + 2]
        if self.row == 0: near_rows = tiles[self.row : self.row + 2]
        if self.row == rows - 1: near_rows = tiles[self.row - 1: self.row + 1]

        for row in near_rows:
            near_cols = row[self.col - 1: self.col + 2]
            if self.col == 0: near_cols = row[self.col : self.col + 2]
            if self.col == cols: near_cols = row[self.col - 1: self.col + 1]
            for tile in near_cols:
                if not (tile.row == self.row and tile.col == self.col):
                    near_tiles.append(tile)

        return near_tiles

    def count_near_bombs(self):
        neighbours = self.get_neighbours()
        near = 0

        for tile in neighbours:
            if tile.bomb: near += 1

        return near

    def reveal(self):
        global tiles  # , rows, cols
        if self.bomb:
            self.image = pg.image.load("images\\Tile_mine.png").convert()
        else:
            self.image = pg.image.load("images\\Tile_revealed.png").convert()

        self.image = pg.transform.scale(self.image, (self.size, self.size))
        self.rect = self.image.get_rect()
        self.rect = self.rect.move((self.col * self.size, self.row * self.size))
        screen.blit(self.image, self.rect)

        self.revealed = True

        """neighbours = []
        if self.col > 0: neighbours.append(tiles[self.row][self.col - 1])
        if self.row > 0: neighbours.append(tiles[self.row - 1][self.col])
        if self.col < cols - 1: neighbours.append(tiles[self.row][self.col + 1])
        if self.row < rows - 1: neighbours.append(tiles[self.row + 1][self.col])"""

        if self.count_near_bombs() == 0:
            neighbours = self.get_neighbours()

            for neighbour in neighbours:
                if not neighbour.revealed and not neighbour.bomb:
                    neighbour.reveal()


def spread_bombs(count):
    global tiles
    while count > 0:
        chosen_tile = tiles[randint(0, rows - 1)][randint(0, cols - 1)]
        if not chosen_tile.bomb:
            chosen_tile.bomb = True
            count -= 1


def create_tiles(rows, cols):
    tile_array = []
    for row in range(rows):
        tile_row = []
        for col in range(cols):
            tile_row.append(Tile(col, row, int(600 / max(cols, rows))))
        tile_array.append(tile_row)

    return tile_array


pg.init()

screen_size = width, height = 600, 650
screen = pg.display.set_mode(screen_size)

rows = 10
cols = 10
bomb_count = 10

tiles = create_tiles(rows, cols)
spread_bombs(bomb_count)

while True:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            exit()

        if event.type == pg.MOUSEBUTTONDOWN:
            mouse_pos = pg.mouse.get_pos()

            for row in tiles:
                for tile in row:
                    if tile.rect.collidepoint(mouse_pos):
                        if not tile.revealed:
                            tile.reveal()
                            n = tile.get_neighbours()

    pg.display.flip()
