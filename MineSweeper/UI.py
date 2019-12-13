import pygame as pg
import Globals as g
from time import time


def init():
    pg.draw.rect(g.screen, (100, 100, 100), (0, 0, g.width, g.controls_height))
    g.clock = Timer()
    g.buttons.append(SettingsButton("Settings", (100, 25)))
    #g.buttons.append(ResetButton("Restart", (g.width - 100, 25)))

    g.flags_remaining = Flags()


class Timer:
    def __init__(self):
        self.bg_rect = pg.Rect(0, 0, int(g.controls_height * 2), int(g.controls_height * 0.8))
        self.bg_rect.center = (g.width // 2, g.controls_height // 2)
        self.font = pg.font.Font("Gotham_Black.ttf", int(g.controls_height * 0.7))
        self.start_time = time()
        self.update()

    def update(self):
        #  draw background
        pg.draw.rect(g.screen, (51, 51, 51), self.bg_rect)
        #  get time
        timer = int(time() - self.start_time)

        if timer > 60:
            minutes = str(timer // 60)
            seconds = str(timer % 60)
            timer = minutes + ":" + seconds.zfill(2)
        else:
            timer = str(timer)

        timer_text = self.font.render(timer, True, (200, 200, 200))
        timer_rect = timer_text.get_rect()
        timer_rect.center = (g.width // 2, (g.controls_height // 2) + 1)
        g.screen.blit(timer_text, timer_rect)


class Flags:
    def __init__(self):
        self.bg_rect = pg.Rect(0,0, g.controls_height, int(g.controls_height * 0.8))
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
    def __init__(self, text, center):
        self.name = text
        self.font = pg.font.Font("Gotham_Black.ttf", int(g.controls_height * 0.7))
        self.text = self.font.render(text, True, (255, 255, 255))
        self.rect = self.text.get_rect()
        self.rect.center = center

        pg.draw.rect(g.screen, (100, 100, 100), self.rect)
        g.screen.blit(self.text, self.rect)

    def action(self):
        pass


class SettingsButton(Button):
    def __init__(self, text, center):
        super().__init__(text, center)

    def action(self):
        settings()


class ResetButton(Button):
    def __init__(self, text, center):
        super().__init__(text, center)


def settings():
    background = pg.Rect(0,0, g.width // 3, g.height // 4)
    background.center = (g.width // 2, g.height // 2)
    pg.draw.rect(g.screen, (150, 150, 150), background)
    g.settings_open = True
    g.state = "PAUSED"
    g.pause_time = time()
