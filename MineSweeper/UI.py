import pygame as pg
import Globals as g
from time import time

timer = None
menu = None
menu_buttons = []
menu_choose = []


def init():
    global timer, menu, menu_buttons, menu_choose
    pg.draw.rect(g.screen, g.menu_colour, (0, 0, g.width, g.controls_height))
    timer = Timer()
    g.flags_remaining = Flags()
    menu = MenuButton("IMAGE", "menu.png", (int(g.controls_height // 1.25), g.controls_height // 2), int(g.controls_height // 1.25))
    menu.draw()

    menu_buttons.append(CloseMenuButton("IMAGE", "close.png", (g.width // 2 - int(g.width // 5.5), g.height // 2 - g.height // 10), 30))
    menu_buttons.append(ResetButton("TEXT", "Reset", (g.width // 2, g.height // 2 + 20), 40))
    menu_buttons.append(AssistButton("TEXT", "Assist", (g.width // 2, g.height // 2 + 70), 40))

    menu_choose.append(ChooseBombCount("Bombs", 5, g.rows * g.cols // 2, g.bomb_count, 5, (g.width // 2 - g.width // 16, g.height // 2 - 80), 40))
    menu_choose.append(ChooseBoardSize("Size", 10, 30, 20, 5, (g.width // 2 - g.width // 16, g.height // 2 - 30), 40))


class Timer:
    def __init__(self):
        self.bg_rect = pg.Rect(0, 0, int(g.controls_height * 2.5), int(g.controls_height * 0.8))
        self.bg_rect.center = (g.width // 2, g.controls_height // 2)
        self.font = pg.font.Font(g.font, int(g.controls_height * 0.7))
        self.start_time = time()
        self.update()

    def update(self):
        #  draw background
        pg.draw.rect(g.screen, (50, 50, 75), self.bg_rect)
        #  get time
        current_time = int(time() - self.start_time)

        #  convert to mm:ss if time > 60 seconds
        if current_time > 60:
            minutes = str(current_time // 60)
            seconds = str(current_time % 60)
            current_time = minutes + ":" + seconds.zfill(2)  # zfill 0 pads a number (01, 02 etc.)
        else:
            current_time = str(current_time)

        timer_text = self.font.render(current_time, True, (200, 200, 200))
        timer_rect = timer_text.get_rect()
        timer_rect.center = (g.width // 2, (g.controls_height // 2) + 1)
        g.screen.blit(timer_text, timer_rect)


class Flags:
    def __init__(self):
        self.bg_rect = pg.Rect(0, 0, g.controls_height * 1.5, int(g.controls_height * 0.8))
        self.bg_rect.center = (g.width - 50, g.controls_height // 2)
        self.font = pg.font.Font(g.font, int(g.controls_height * 0.7))
        self.update()

    def update(self):
        #  draw background
        pg.draw.rect(g.screen, (50, 50, 75), self.bg_rect)

        remaining_flags = str(g.bomb_count - g.flag_count)

        text = self.font.render(remaining_flags, True, (200, 200, 200))
        text_rect = text.get_rect()
        text_rect.center = self.bg_rect.center
        g.screen.blit(text, text_rect)


class Title:
    def __init__(self, text, height, center, has_bg = False, colour = (255, 255, 255), background = (0, 0, 0)):
        text = str(text)

        self.font = pg.font.Font(g.font, height)
        self.display = self.font.render(text, True, colour)
        self.rect = self.display.get_rect()
        self.rect.center = center
        self.center, self.colour, self.has_bg = center, colour, has_bg

        if has_bg:
            self.background = background

    def draw(self):
        if self.has_bg:
            pg.draw.rect(g.screen, self.background, self.rect)
        g.screen.blit(self.display, self. rect)

    def update(self, text):
        text = str(text)

        self.display = self.font.render(text, True, self.colour)
        self.rect = self.display.get_rect()
        self.rect.center = self.center


class Button:
    def __init__(self, button_type, text, center, height, width = -1, colour=(255, 255, 255)):
        self.type, self.center, self.height = button_type, center, height

        if width == -1:
            width = height

        if button_type == "TEXT":
            self.font = pg.font.Font(g.font, height)
            self.display = self.font.render(text, True, colour)
        elif button_type == "IMAGE":
            self.display = pg.image.load("images\\" + text).convert_alpha()
            self.display = pg.transform.scale(self.display, (width, height))
        else:
            raise ValueError

        self.rect = self.display.get_rect()
        self.rect.center = center

    def draw(self):
        if self.type == "TEXT":
            pg.draw.rect(g.screen, (50, 50, 75), self.rect)
        g.screen.blit(self.display, self.rect)

    def action(self):
        pass


class ChooseValue:
    def __init__(self, text, min_val, max_val, start_val, step, center, size):
        self.title = Title(text, size, center)
        title_width = self.title.display.get_size()[0]
        self.up = Button("IMAGE", "arrow.png", (center[0] + title_width // 2 + size // 2 + 10, center[1] - size // 4), size // 2, width = size)
        self.down = Button("IMAGE", "arrow.png", (center[0] + title_width // 2 + size // 2 + 10, center[1] + size // 4), size // 2, width = size)
        self.down.display = pg.transform.flip(self.down.display, False, True)

        self.min, self.max, self.step = min_val, max_val, step

        self.value = Title(str(start_val), size // 2, (center[0] + title_width // 2 + size * 2, center[1]), has_bg = True, background = g.menu_colour)

    def draw(self):
        self.title.draw()
        self.up.draw()
        self.down.draw()
        self.value.draw()

    def increase(self):
        self.value.update("N/A")

    def decrease(self):
        self.value.update("N/A")


class MenuButton(Button):
    def __init__(self, button_type, text, center, size):
        super().__init__(button_type, text, center, size)

    def action(self):
        if g.menu_open:
            g.close_menu()
        else:
            g.menu()

# Menu buttons


class CloseMenuButton(Button):
    def __init__(self, button_type, text, center, size):
        super().__init__(button_type, text, center, size)

    def action(self):
        g.close_menu()


class ResetButton(Button):
    def __init__(self, button_type, text, center, size):
        super().__init__(button_type, text, center, size)

    def action(self):
        if g.state == "PAUSED" or g.state == "GAME_OVER":
            g.restart()


class AssistButton(Button):
    def __init__(self, button_type, text, center, size):
        super().__init__(button_type, text, center, size)

    def action(self):
        if g.assist:
            g.assist = False
        else:
            g.assist = True


class ChooseBombCount(ChooseValue):
    def __init__(self, text, min_val, max_val, start_val, step, center, size):
        super().__init__(text, min_val, max_val, start_val, step, center, size)

    def increase(self):
        g.bomb_count += self.step

        if g.bomb_count > self.max:
            g.bomb_count = self.max

        self.value.update(g.bomb_count)
        self.value.draw()

    def decrease(self):
        g.bomb_count -= self.step

        if g.bomb_count < self.min:
            g.bomb_count = self.min

        self.value.update(g.bomb_count)
        self.value.draw()


class ChooseBoardSize(ChooseValue):
    def __init__(self, text, min_val, max_val, start_val, step, center, size):
        super().__init__(text, min_val, max_val, start_val, step, center, size)

    def increase(self):
        g.rows += self.step
        g.cols += self.step

        if g.rows > self.max:
            g.rows = self.max
            g.cols = self.max

        self.value.update(g.rows)
        self.value.draw()

    def decrease(self):
        g.rows -= self.step
        g.cols -= self.step

        if g.rows < self.min:
            g.rows = self.min
            g.cols = self.min

        self.value.update(g.rows)
        self.value.draw()
