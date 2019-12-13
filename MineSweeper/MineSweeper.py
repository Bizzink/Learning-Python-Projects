from sys import exit, setrecursionlimit
from random import randint
from time import time
import pygame as pg
from Tile import Tile
import Globals as g
import UI


def create_tiles(rows, cols):
    tile_array = []
    for row in range(rows):
        tile_row = []
        for col in range(cols):
            tile_row.append(Tile(col, row, int(g.width / max(cols, rows)), g.controls_height))
        tile_array.append(tile_row)

    return tile_array


def spread_bombs(count, excluded_tile):
    excluded_tiles = excluded_tile.get_neighbours()
    excluded_tiles.append(excluded_tile)

    while count > 0:
        chosen_tile = g.tiles[randint(0, g.rows - 1)][randint(0, g.cols - 1)]
        if not chosen_tile.bomb and chosen_tile not in excluded_tiles:
            chosen_tile.bomb = True
            count -= 1


def tiles_left():
    #  count number of remaining hidden tiles
    remaining = 0
    for row in g.tiles:
        for tile in row:
            if not tile.revealed: remaining += 1

    return remaining


def game_over(text):
    for row in g.tiles:
        for tile in row:
            if tile.flagged: tile.toggle_flag()
            tile.reveal()

    overlay = pg.Surface((g.width, g.height - g.controls_height))
    overlay.set_alpha(100)
    overlay.fill((0, 0, 0))
    g.screen.blit(overlay, (0, g.controls_height))

    font = pg.font.Font("Gotham_Black.ttf", g.width // 5)
    title = font.render(text, True, (200, 255, 200))
    title_rect = title.get_rect()
    title_rect.center = (g.width // 2, g.height // 2)
    g.screen.blit(title, title_rect)

    g.state = "PAUSED"


def restart():
    global first_click
    g.tiles.clear()
    first_click = True
    UI.init()
    g.tiles = create_tiles(g.rows, g.cols)

    g.state = "PLAYING"


setrecursionlimit(1500)
pg.init()

screen_size = g.width, g.height = 900, 950
g.screen = pg.display.set_mode(screen_size)
pg.display.set_caption("Minesweeper")


g.rows = 20
g.cols = 20
g.bomb_count = 50
g.flag_count = 0
g.controls_height = 50
first_click = True
playing = True
freeze = False
UI.init()
g.tiles = create_tiles(g.rows, g.cols)


while True:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            exit()

        if event.type == pg.MOUSEBUTTONDOWN:
            mouse_pos = pg.mouse.get_pos()

            for button in g.buttons:
                if button.rect.collidepoint(mouse_pos):
                    button.action()
                    freeze = True

            if not freeze and not g.settings_open:
                for row in g.tiles:
                    for tile in row:
                        if tile.rect.collidepoint(mouse_pos):

                            #  left click
                            if event.button == 1:
                                if first_click:
                                    spread_bombs(g.bomb_count, tile)
                                    tile.reveal()
                                    g.clock.start_time = time()
                                    first_click = False
                                elif not tile.revealed:
                                    tile.reveal()
                                    if tile.bomb and not tile.flagged: game_over("LOSE!")

                            #  right click
                            elif event.button == 3:
                                if not tile.revealed: tile.toggle_flag()
                                g.flags_remaining.update()

                freeze = False

        if event.type == pg.KEYDOWN:
            #  Enter
            if event.key == 13 and not g.state == "PLAYING": restart()

            #  Escape
            if event.key == 27:
                if g.settings_open:
                    for row in g.tiles:
                        for tile in row:
                            tile.update()
                    g.settings_open = False
                    g.state = "PLAYING"
                    g.clock.start_time += (time() - g.pause_time)
                else:
                    UI.settings()

    if g.state == "PLAYING" and not first_click:
        g.clock.update()

    if tiles_left() == g.bomb_count:
        game_over("WIN!")

    pg.display.flip()
