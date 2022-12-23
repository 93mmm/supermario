import pygame
import json

with open("json_files/settings.json", "r") as file:
    data = json.load(file)



class Player:
    def __init__(self, level):
        self.level = level
        self.speed = data["player_charecteristics"]["speed"]
    
    def spawn(self): # в зависимости от уровня решает, где заспавнить игрока
        pass
    
    def update(self):
        pass