from sys import exit, setrecursionlimit
from time import time
import pygame as pg
import Globals as g
import UI

g.rows = 20
g.cols = 20
g.bomb_count = 50
g.remaining_bombs = g.bomb_count
g.controls_height = 50
setrecursionlimit(1500)

# TODO: change board size
#   save / load
#   assist
#   make things look good

pg.init()

screen_size = g.width, g.height = 900, 950
g.screen = pg.display.set_mode(screen_size)
pg.display.set_caption("Minesweeper")

UI.init()
g.tiles = g.create_tiles(g.rows, g.cols)

playing = True

while True:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            exit()

        if event.type == pg.MOUSEBUTTONDOWN:
            mouse_pos = pg.mouse.get_pos()

            if UI.menu.rect.collidepoint(mouse_pos):
                UI.menu.action()

            if g.state == "PAUSED" or g.state == "GAME_OVER":
                for button in UI.menu_buttons:
                    if button.rect.collidepoint(mouse_pos):
                        button.action()

                for choose in UI.menu_choose:
                    if choose.up.rect.collidepoint(mouse_pos):
                        choose.increase()
                    elif choose.down.rect.collidepoint(mouse_pos):
                        choose.decrease()

            elif g.state == "PLAYING":
                for row in g.tiles:
                    for tile in row:
                        if tile.rect.collidepoint(mouse_pos):

                            #  left click
                            if event.button == 1:
                                if g.first_click:
                                    g.spread_bombs(g.remaining_bombs, tile)
                                    tile.reveal()
                                    UI.timer.start_time = time()
                                    g.first_click = False
                                elif not tile.revealed:
                                    tile.reveal()
                                    if tile.bomb and not tile.flagged: g.game_over("LOSE!", colour = (255, 100, 100))

                            #  right click
                            elif event.button == 3:
                                if not tile.revealed and not g.first_click: tile.toggle_flag()
                                g.flags_remaining.update()

        if event.type == pg.KEYDOWN:
            #  Enter
            if event.key == 13 and not g.state == "PLAYING": g.restart()

            #  Escape
            if event.key == 27: UI.menu.action()

    if g.state == "PLAYING" and not g.first_click:
        UI.timer.update()

    if g.tiles_left() == g.remaining_bombs:
        g.game_over("WIN!", colour = (100, 255, 150))

    pg.display.flip()
