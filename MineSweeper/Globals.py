from time import time
from Tile import Tile
from random import randint
import UI
import pygame as pg

#  Variables


width = 0
height = 0
controls_height = 0
rows = 0
cols = 0
tiles = []
screen = None
first_click = True
state = "PLAYING"
flags_remaining = 0
pause_time = 0
flag_count = 0
bomb_count = 0

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
    overlay.set_alpha(100)
    overlay.fill((0, 0, 0))
    screen.blit(overlay, (0, controls_height))

    font = pg.font.Font("Gotham_Black.ttf", width // 5)
    title = font.render(text, True, colour)
    title_rect = title.get_rect()
    title_rect.center = (width // 2, height // 2)
    screen.blit(title, title_rect)

    state = "PAUSED"


def restart():
    """Resets the board and game state"""
    global first_click, tiles, state

    tiles.clear()
    UI.init()
    tiles = create_tiles(rows, cols)
    first_click = True
    state = "PLAYING"


def menu():
    """Displays the menu"""
    global state, pause_time

    background = pg.Rect(0, 0, width // 3, height // 4)
    background.center = (width // 2, height // 2)
    pg.draw.rect(screen, (150, 150, 150), background)

    for button in UI.menu_buttons:
        button.draw()

    pause_time = time()
    state = "PAUSED"


def close_menu():
    global state
    for row in tiles:
        for tile in row:
            tile.update()

    UI.timer.start_time += (time() - pause_time)
    state = "PLAYING"
