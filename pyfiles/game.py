import pygame
from pygame.locals import *
import sys

# imports from files
from pyfiles.button import Button
from pyfiles.level import Level
from pyfiles.game_data import level_0



class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Awesome solution")
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.clock = pygame.time.Clock()
        self.background = pygame.image.load("presets/main_menu/BG.png")
        self.fps = 60
        self.level = Level(level_0, self.screen)
        self.running = True
    
    def setup_buttons(self):
        font = self.get_font(70)
        self.buttons = []
        names = ["Играть", "Загрузить игру", "Выйти"]
        for idx, text in enumerate(names):
            self.buttons.append(Button(image=None, pos=(960, 400 + 200 * idx),
                            text_input=text, font=font, base_color="#000000", hovering_color="Orange"))

    def run(self):
        def check_buttons():
            if self.buttons[0].checkForInput(menu_mouse_pos):
                self.play()
            if self.buttons[1].checkForInput(menu_mouse_pos):
                self.load_game()
            if self.buttons[2].checkForInput(menu_mouse_pos):
                pygame.quit()
                sys.exit()
        while self.running:
            self.screen.blit(self.background, (0, 0))
            menu_mouse_pos = pygame.mouse.get_pos()
            menu_text = self.get_font(100).render("ГЛАВНОЕ МЕНЮ", True, "#000000")
            menu_rect = menu_text.get_rect(center=(960, 200))
            self.setup_buttons()

            self.screen.blit(menu_text, menu_rect)

            for button in self.buttons:
                button.changeColor(menu_mouse_pos)
                button.update(self.screen)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    check_buttons()

            pygame.display.update()
    
    def load_game(self):
        while True:
            self.screen.fill("grey")
            play_text = self.get_font(30).render("Загрузка игры... Backspace вернуться назад", True, "black")
            play_rect = play_text.get_rect(center=(960, 150))
            self.screen.blit(play_text, play_rect)

            for event in pygame.event.get():
                keys = pygame.key.get_pressed()
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if keys[pygame.K_BACKSPACE]:
                    self.run()
            pygame.display.update()

    def play(self):
        while True:
            for event in pygame.event.get():
                keys = pygame.key.get_pressed()
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if keys[pygame.K_BACKSPACE]:
                    self.run()

            self.screen.fill("grey")
            self.level.run()
            pygame.display.update()
            self.clock.tick(60)

    def get_font(self, size): # Returns Press-Start-2P in the desired size
        return pygame.font.Font("presets/main_menu/font.ttf", size)