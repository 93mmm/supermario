import pygame
from scripts.tiles import AnimatedTile
from random import randint


class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.mushroom = pygame.image.load('assets/entities/mushroom/walk_0.png')
        self.rect = self.mushroom.get_rect()
        self.rect.x = x
        self.rect.y = y
