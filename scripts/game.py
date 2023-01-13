import pygame
from pygame.locals import *
import sys
import webbrowser

from scripts.button import Button
from scripts.level import Level
from scripts.support_function import exit_check, get_font


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
        play = [pygame.image.load('assets/buttons/play_up.png'), pygame.image.load('assets/buttons/play_down.png')]
        credits_of_creators = [pygame.image.load('assets/buttons/load_up.png'), pygame.image.load('assets/buttons/load_down.png')]
        self.buttons = []
        images = [play, exit, credits_of_creators]
        for idx, img in enumerate(images):
            self.buttons.append(Button(img, (960, 400 + 200 * idx)))

    def run(self):
        def check_buttons():
            if self.buttons[0].check_for_input(menu_mouse_pos):
                self.play()
            if self.buttons[2].check_for_input(menu_mouse_pos):
                url = "https://www.tinkoff.ru/sl/8UiebMfZ6fc"
                webbrowser.open(url, new=0, autoraise=True)
                sys.exit()
                #self.load_game()
            if self.buttons[1].check_for_input(menu_mouse_pos):
                pygame.quit()
                sys.exit()
        while True:
            self.screen.fill(self.background)
            menu_mouse_pos = pygame.mouse.get_pos()
            menu_text = get_font(100).render("MAIN MENU", True, "#000000")
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
            play_text = get_font(30).render("Загрузка игры... Backspace вернуться назад", True, "black")
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
                    self.reset_game_after_death()
                    self.run()

            self.screen.fill(self.background)
            self.level.run()
            if self.level.player_is_dead:
                self.dead_scene()
            self.clock.tick(60)
            pygame.display.update()

    def dead_scene(self):
        while True:
            for event in pygame.event.get():
                keys = pygame.key.get_pressed()
                if keys[K_BACKSPACE]:
                    self.run()
            self.screen.fill("black")
            self.clock.tick(60)
            pygame.display.update()

    # donate me to fix this sh*t:
    def reset_game_after_death(self):
        game = Game()
        game.run()

