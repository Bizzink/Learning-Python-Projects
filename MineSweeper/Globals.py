from time import time, sleep
from Tile import Tile
from random import randint
import UI
import pygame as pg
from Assist import update_potentials

#  Variables


font = "Retro_Gaming.ttf"
width = 0
height = 0
controls_height = 0
rows = 0
cols = 0
tiles = []
assist = False
screen = None
first_click = True
menu_open = False
state = "PLAYING"
flags_remaining = 0
pause_time = 0
flag_count = 0
remaining_bombs = 0
bomb_count = 0
menu_colour = (75, 75, 100)

slowdown = False

#  Functions


def create_tiles(rows, cols):
    """Creates array of tiles of size rows x cols"""
    tile_array = []

    for row in range(rows):
        tile_row = []
        for col in range(cols):
            tile_row.append(Tile(col, row, int(width / max(cols, rows)), controls_height))
        tile_array.append(tile_row)

    return tile_array


def spread_bombs(count, excluded_tile):
    """Randomly spreads (count) bombs on the board, excluded_tile and the 8 surrounding tiles will not contain bombs"""
    excluded_tiles = excluded_tile.get_neighbours()
    excluded_tiles.append(excluded_tile)

    while count > 0:
        chosen_tile = tiles[randint(0, rows - 1)][randint(0, cols - 1)]
        if not chosen_tile.bomb and chosen_tile not in excluded_tiles:
            chosen_tile.bomb = True
            count -= 1

        if slowdown:
            chosen_tile.highlight((255, 50, 50))
            sleep(0.01)
            pg.display.flip()


def tiles_left():
    """Counts the number of un-revealed tiles left"""
    remaining = 0

    for row in tiles:
        for tile in row:
            if not tile.revealed: remaining += 1

    return remaining


def game_over(text, colour = (255, 255, 255)):
    """Displays a game over title on the screen and sets the game state to paused"""
    global state

    for row in tiles:
        for tile in row:
            if tile.flagged: tile.toggle_flag()
            tile.reveal()

    overlay = pg.Surface((width, height - controls_height))
    overlay.set_alpha(200)
    overlay.fill((0, 0, 0))
    screen.blit(overlay, (0, controls_height))

    UI.Title(text, width // 5, (width //2, height // 2), colour = colour).draw()
    UI.Title("PRESS ENTER TO RESTART", width // 20, (width // 2, height // 2 + width // 10)).draw()

    state = "GAME_OVER"


def restart():
    """Resets the board and game state"""
    global first_click, tiles, state, bomb_count, remaining_bombs, flag_count, menu_open, rows, cols

    if bomb_count > rows * cols // 4:
        bomb_count = rows * cols // 4

    remaining_bombs = bomb_count
    flag_count = 0
    tiles.clear()
    tiles = create_tiles(rows, cols)
    first_click = True
    menu_open = False
    state = "PLAYING"
    UI.init()


def menu():
    """Displays the menu"""
    global state, pause_time, menu_open, menu_colour

    background = pg.Rect(0, 0, int(width // 2.5), height // 4)
    background.center = (width // 2, height // 2)
    pg.draw.rect(screen, menu_colour, background)

    for button in UI.menu_buttons:
        button.draw()

    for choose in UI.menu_choose:
        choose.draw()

    pause_time = time()

    if state != "GAME_OVER":
        state = "PAUSED"
    menu_open = True


def close_menu():
    global state, menu_open
    for row in tiles:
        for tile in row:
            tile.update()

    if assist:
        update_potentials()

    UI.timer.start_time += (time() - pause_time)

    if state != "GAME_OVER":
        state = "PLAYING"

    menu_open = False
