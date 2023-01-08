import pygame
from pygame.locals import *
import sys

from scripts.button import Button
from scripts.level import Level
from scripts.game_data import levels


def exit_check(event):
    if event.type == QUIT:
        pygame.quit()
        sys.exit()
    if event.type == KEYDOWN:
        if event.key == K_ESCAPE:
            pygame.quit()
            sys.exit()


class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Mario")
        self.screen = pygame.display.set_mode((0, 0), FULLSCREEN)
        self.clock = pygame.time.Clock()

        self.background = "#9290ff"
        self.level = Level("level_1", self.screen)

    def setup_buttons(self):
        exit = [pygame.image.load('assets/buttons/exit_up.png'), pygame.image.load('assets/buttons/exit_down.png')]
        load = [pygame.image.load('assets/buttons/load_up.png'), pygame.image.load('assets/buttons/load_down.png')]
        play = [pygame.image.load('assets/buttons/play_up.png'), pygame.image.load('assets/buttons/play_down.png')]
        self.buttons = []
        images = [play, load, exit]
        for idx, img in enumerate(images):
            self.buttons.append(Button(img, (960, 400 + 200 * idx)))

    def run(self):
        def check_buttons():
            if self.buttons[0].check_for_input(menu_mouse_pos):
                self.play()
            if self.buttons[1].check_for_input(menu_mouse_pos):
                self.load_game()
            if self.buttons[2].check_for_input(menu_mouse_pos):
                pygame.quit()
                sys.exit()
        while True:
            self.screen.fill(self.background)
            menu_mouse_pos = pygame.mouse.get_pos()
            menu_text = self.get_font(100).render("ГЛАВНОЕ МЕНЮ", True, "#000000")
            menu_rect = menu_text.get_rect(center=(960, 200))
            self.setup_buttons()

            self.screen.blit(menu_text, menu_rect)

            for button in self.buttons:
                button.change_image(menu_mouse_pos)
                button.update(self.screen)

            for event in pygame.event.get():
                exit_check(event)
                if event.type == MOUSEBUTTONDOWN:
                    check_buttons()
            self.clock.tick(60)
            pygame.display.update()
    
    def load_game(self):
        while True:
            self.screen.fill("grey")
            play_text = self.get_font(30).render("Загрузка игры... Backspace вернуться назад", True, "black")
            play_rect = play_text.get_rect(center=(960, 150))
            self.screen.blit(play_text, play_rect)

            for event in pygame.event.get():
                keys = pygame.key.get_pressed()
                exit_check(event)
                if keys[K_BACKSPACE]:
                    self.run()
            self.clock.tick(60)
            pygame.display.update()

    def play(self):
        while True:
            for event in pygame.event.get():
                keys = pygame.key.get_pressed()
                exit_check(event)
                if keys[K_BACKSPACE]:
                    self.run()

            self.screen.fill(self.background)
            self.level.run()
            self.clock.tick(60)
            pygame.display.update()

    def get_font(self, size): # Returns Press-Start-2P in the desired size
        return pygame.font.Font("assets/fonts/font.ttf", size)
