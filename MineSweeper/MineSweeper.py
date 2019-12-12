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
        self.flagged = False
        self.image = pg.image.load("images\\Tile_hidden.png").convert()
        self.update()

    def update(self):
        self.image = pg.transform.scale(self.image, (self.size, self.size))
        self.rect = self.image.get_rect()
        self.rect = self.rect.move((self.col * self.size, self.row * self.size))
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
        global tiles
        if not self.flagged:
            if self.bomb:
                self.image = pg.image.load("images\\Tile_mine.png").convert()
            else:
                image_name = "images\\Tile_revealed_" + str(self.count_near_bombs()) + ".png"
                self.image = pg.image.load(image_name).convert()

            self.update()
            self.revealed = True

        if self.count_near_bombs() == 0:
            for neighbour in self.get_neighbours():
                if not neighbour.revealed and not neighbour.bomb: neighbour.reveal()

    def toggle_flag(self):
        if self.flagged:
            self.flagged = False
            self.image = pg.image.load("images\\Tile_hidden.png").convert()
        else:
            self.flagged = True
            self.image = pg.image.load("images\\Tile_flagged.png").convert()

        self.update()


def create_tiles(rows, cols):
    tile_array = []
    for row in range(rows):
        tile_row = []
        for col in range(cols):
            tile_row.append(Tile(col, row, int(600 / max(cols, rows))))
        tile_array.append(tile_row)

    return tile_array


def spread_bombs(count, excluded_tile):
    global tiles
    excluded_tiles = excluded_tile.get_neighbours()
    excluded_tiles.append(excluded_tile)

    while count > 0:
        chosen_tile = tiles[randint(0, rows - 1)][randint(0, cols - 1)]
        if not chosen_tile.bomb and chosen_tile not in excluded_tiles:
            chosen_tile.bomb = True
            count -= 1


def tiles_left():
    global tiles
    #  count number of remaining hidden tiles
    remaining = 0
    for row in tiles:
        for tile in row:
            if not tile.revealed: remaining += 1

    return remaining


def game_over(set_state, text):
    global state
    for row in tiles:
        for tile in row:
            if tile.flagged: tile.toggle_flag()
            tile.reveal()

    font = pg.font.Font("Gotham_Black.ttf", 100)
    title = font.render(text, True, (200, 255, 200))
    title_rect = title.get_rect()
    title_rect.center = (300, 300)
    screen.blit(title, title_rect)

    state = set_state


def restart():
    global state, first_click
    global tiles
    tiles.clear()
    first_click = True
    tiles = create_tiles(rows, cols)

    state = "PLAYING"


pg.init()

screen_size = width, height = 600, 600
screen = pg.display.set_mode(screen_size)
pg.display.set_caption("Minesweeper")

rows = 20
cols = 20
bomb_count = 60
first_click = True
playing = True
tiles = create_tiles(rows, cols)
state = "PLAYING"

while True:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            exit()

        if event.type == pg.MOUSEBUTTONDOWN:
            mouse_pos = pg.mouse.get_pos()

            for row in tiles:
                for tile in row:
                    if tile.rect.collidepoint(mouse_pos):

                        #  left click
                        if event.button == 1:
                            if first_click:
                                spread_bombs(bomb_count, tile)
                                tile.reveal()
                                first_click = False
                            elif not tile.revealed:
                                tile.reveal()
                                if tile.bomb: game_over("LOSE", "LOSE!")

                        #  right click
                        elif event.button == 3:
                            if not tile.revealed: tile.toggle_flag()

        if event.type == pg.KEYDOWN:
            #  Enter
            if event.key == 13 and not state == "PLAYING":
                restart()

    if tiles_left() == bomb_count:
        game_over("WIN", "WIN!")

    pg.display.flip()
