import pygame
import json


with open("json_files/settings.json", "r") as file:
    data = json.load(file)


class Enemy:
    SPAWNPOINTS = data["spawnpoints"]
    def __init__(self, level):
        self.level = level
        self.spawn()
        self.type = "ENEMYTYPE"
        self.speed = "SPEED"
    
    def spawn(self): # в зависимости от уровня решает, где заспавнить вражину
        pass # выбирает рандомную сущность из доступных 
    
    def update(self):
        pass