import pygame
import json
import sys

from pyfiles.game import Game

def check_event(event):
    pass

with open("json_files/settings.json", "r") as file:
    data = json.load(file)

pygame.init()
screen_width, screen_height = data["window_size"]
screen = pygame.display.set_mode((screen_width,screen_height))
clock = pygame.time.Clock()
game = Game()

while True:
    for e in pygame.event.get():
        check_event(e)
    screen.fill('grey')
    pygame.display.update()
    clock.tick(60)
