import pygame as pg
import Globals as g
from time import sleep


class Tile:
    def __init__(self, col, row, size, offset):
        self.col = col
        self.row = row
        self.size = size
        self.offset = offset

        self.bomb = False
        self.revealed = False
        self.flagged = False
        self.rect = None
        self.image = pg.image.load("images\\Tile_hidden.png").convert()

        self.update()

    def update(self):
        self.image = pg.transform.scale(self.image, (self.size, self.size))
        self.rect = self.image.get_rect()
        self.rect = self.rect.move((self.col * self.size, (self.row * self.size) + self.offset))
        g.screen.blit(self.image, self.rect)

    def get_neighbours(self):
        """Get 8 surrounding neighbours. If at an edge, ignore nonexistent neighbours"""
        near_tiles = []

        near_rows = g.tiles[self.row - 1: self.row + 2]
        if self.row == 0: near_rows = g.tiles[self.row : self.row + 2]
        if self.row == g.rows - 1: near_rows = g.tiles[self.row - 1: self.row + 1]

        for row in near_rows:
            near_cols = row[self.col - 1: self.col + 2]
            if self.col == 0: near_cols = row[self.col : self.col + 2]
            if self.col == g.cols: near_cols = row[self.col - 1: self.col + 1]
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
        if not self.flagged:
            if self.bomb:
                self.image = pg.image.load("images\\Tile_mine.png").convert()
            else:
                image_name = "images\\Tile_revealed_" + str(self.count_near_bombs()) + ".png"
                self.image = pg.image.load(image_name).convert()

            self.update()
            self.revealed = True

            if g.slowdown:
                sleep(0.01)
                pg.display.flip()

        if self.count_near_bombs() == 0:
            for neighbour in self.get_neighbours():
                if not neighbour.revealed and not neighbour.bomb: neighbour.reveal()

    def toggle_flag(self):
        if self.flagged:
            self.flagged = False
            self.image = pg.image.load("images\\Tile_hidden.png").convert()
            g.flag_count -= 1
        else:
            self.flagged = True
            self.image = pg.image.load("images\\Tile_flagged.png").convert()
            g.flag_count += 1

        self.update()

    def highlight(self, colour, opacity, reset = False, b = False):
        self.update()
        if not reset:
            overlay = pg.Surface((self.size, self.size))
            overlay.set_alpha(opacity)
            overlay.fill(colour)
            g.screen.blit(overlay, (self.col * self.size, (self.row * self.size) + g.controls_height))