import pygame as pg
import Globals as g
from time import time

timer = None
menu = None
menu_buttons = []


def init():
    global timer, menu, menu_buttons
    pg.draw.rect(g.screen, (100, 100, 100), (0, 0, g.width, g.controls_height))
    timer = Timer()
    g.flags_remaining = Flags()
    menu = MenuButton("TEXT", "Menu", (100, 25), 40)
    menu.draw()


class Timer:
    def __init__(self):
        self.bg_rect = pg.Rect(0, 0, int(g.controls_height * 2.5), int(g.controls_height * 0.8))
        self.bg_rect.center = (g.width // 2, g.controls_height // 2)
        self.font = pg.font.Font("Gotham_Black.ttf", int(g.controls_height * 0.7))
        self.start_time = time()
        self.update()

    def update(self):
        #  draw background
        pg.draw.rect(g.screen, (51, 51, 51), self.bg_rect)
        #  get time
        timer = int(time() - self.start_time)

        #  convert to mm:ss if time > 60 seconds
        if timer > 60:
            minutes = str(timer // 60)
            seconds = str(timer % 60)
            timer = minutes + ":" + seconds.zfill(2)  # zfill 0 pads a number (01, 02 etc.)
        else:
            timer = str(timer)

        timer_text = self.font.render(timer, True, (200, 200, 200))
        timer_rect = timer_text.get_rect()
        timer_rect.center = (g.width // 2, (g.controls_height // 2) + 1)
        g.screen.blit(timer_text, timer_rect)


class Flags:
    def __init__(self):
        self.bg_rect = pg.Rect(0, 0, g.controls_height * 1.5, int(g.controls_height * 0.8))
        self.bg_rect.center = (g.width - 50, g.controls_height // 2)
        self.font = pg.font.Font("Gotham_Black.ttf", int(g.controls_height * 0.7))
        self.update()

    def update(self):
        #  draw background
        pg.draw.rect(g.screen, (51, 51, 51), self.bg_rect)

        remaining_flags = str(g.bomb_count - g.flag_count)

        text = self.font.render(remaining_flags, True, (200, 200, 200))
        text_rect = text.get_rect()
        text_rect.center = self.bg_rect.center
        g.screen.blit(text, text_rect)


class Button:
    def __init__(self, button_type, text, center, height, width = -1, colour=(255, 255, 255)):
        self.type, self.center, self.height = button_type, center, height

        if width == -1:
            width = height

        if button_type == "TEXT":
            self.font = pg.font.Font("Gotham_Black.ttf", height)
            self.display = self.font.render(text, True, colour)
        elif button_type == "IMAGE":
            self.display = pg.image.load("images\\" + text).convert()
            self.display = pg.transform.scale(self.display, (width, height))
        else:
            raise ValueError

        self.rect = self.display.get_rect()
        self.rect.center = center

    def draw(self):
        if self.type == "TEXT":
            pg.draw.rect(g.screen, (100, 100, 100), self.rect)
        g.screen.blit(self.display, self.rect)

    def action(self):
        pass


class ChooseValue:
    def __init__(self, text, min_val, max_val, step, center, size):
        self.up = Button("IMAGE", "up.png", (center[0], center[1] + size // 4), size // 2, width = size // 2)
        self.down = Button("IMAGE", "down.png", (center[0], center[1] - size // 4), size // 2, width = size // 2)

    def draw(self):
        pass

    def increase(self):
        pass

    def decrease(self):
        pass


class MenuButton(Button):
    def __init__(self, button_type, text, center, size):
        super().__init__(button_type, text, center, size)

    def action(self):
        if g.state == "PLAYING":
            g.menu()
        else:
            g.close_menu()

# Menu buttons


class CloseMenuButton:
    def __init__(self, button_type, text, center, size):
        super().__init__(button_type, text, center, size)

    def action(self):
        g.close_menu()


class ResetButton(Button):
    def __init__(self, button_type, text, center, size):
        super().__init__(button_type, text, center, size)

    def action(self):
        g.restart()
