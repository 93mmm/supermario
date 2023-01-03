import pygame
from random import choice

from pyfiles.game_data import spawnpoints, enemies


class Enemy:
    def __init__(self, level, spawnpoint):
        self.level = level
        self.spawn(spawnpoint)
    
    def choice_enemy(self):
        self.name = choice(["mushroom", "tortoise"])
        self.speed = enemies[self.name]["speed"]

    def spawn(self, spawnpoint):
        pass
    
    def update(self):
        pass