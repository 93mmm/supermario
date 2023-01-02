# imports from external libraries
import pygame
import sys

# imports from files
from pyfiles.game import Game
from pyfiles.button import Button
from pyfiles.level import Level, level_map


def check_event(event):
    if event.type == pygame.QUIT:
        pygame.quit()
        sys.exit()
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_ESCAPE:
            pygame.quit()
            sys.exit()


pygame.init()
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
#game = Game() сделал специально, чтобы пока ошибку не ловил
running = True
BG = pygame.image.load("presets/main_menu/BG.png")
FPS = 60
clock = pygame.time.Clock()
level = Level(level_map, screen)


def get_font(size):  # Returns Press-Start-2P in the desired size
    return pygame.font.Font("presets/main_menu/font.ttf", size)


def play():
    while True:
        for event in pygame.event.get():
            keys = pygame.key.get_pressed()
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if keys[pygame.K_BACKSPACE]:
                main_menu()

        screen.fill("black")
        level.run()
        pygame.display.update()
        clock.tick(60)


def load_game():
    while True:
        screen.fill("grey")
        play_text = get_font(30).render("Загрузка игры... Backspace вернуться назад", True, "black")
        play_rect = play_text.get_rect(center=(960, 150))
        screen.blit(play_text, play_rect)

        for event in pygame.event.get():
            keys = pygame.key.get_pressed()
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if keys[pygame.K_BACKSPACE]:
                main_menu()
        pygame.display.update()


def main_menu():
    while running:
        screen.blit(BG, (0, 0))
        menu_mouse_pos = pygame.mouse.get_pos()
        menu_text = get_font(100).render("ГЛАВНОЕ МЕНЮ", True, "#000000")
        menu_rect = menu_text.get_rect(center=(960, 200))

        play_button = Button(image=None, pos=(960, 400),
                             text_input="Играть", font=get_font(70), base_color="#000000", hovering_color="Orange")
        load_button = Button(image=None, pos=(960, 600),
                             text_input="Загрузить игру", font=get_font(70), base_color="#000000", hovering_color="Orange")

        quit_button = Button(image=None, pos=(960, 800),
                             text_input="Выйти", font=get_font(70), base_color="#000000", hovering_color="Orange")

        screen.blit(menu_text, menu_rect)

        for button in [play_button, load_button, quit_button]:
            button.changeColor(menu_mouse_pos)
            button.update(screen)

        for event in pygame.event.get():
            check_event(event)
            if event.type == pygame.MOUSEBUTTONDOWN:
                if play_button.checkForInput(menu_mouse_pos):
                    play()
                if load_button.checkForInput(menu_mouse_pos):
                    load_game()
                if quit_button.checkForInput(menu_mouse_pos):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()


main_menu()
