# imports from external libraries
import pygame
import sys

# imports from files
from pyfiles.game import Game


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
game = Game()
running = True

while running:
    for e in pygame.event.get():
        check_event(e)
    screen.fill('grey')
    pygame.display.update()
