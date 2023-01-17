import random
from os import walk
import pygame
from scripts.support_function import import_folder
from random import choice


class Tile(pygame.sprite.Sprite):
    def __init__(self, size, x, y):
        super().__init__()
        self.image = pygame.Surface((size, size))
        self.rect = self.image.get_rect(topleft=(x, y))

    def update(self, shift):
        self.rect.x += shift


class StaticTile(Tile):
    def __init__(self, size, x, y, image):
        super().__init__(size, x, y)
        self.image = image


class AnimatedTile(Tile):
    def __init__(self, size, x, y, path):
        super().__init__(size, x, y)
        self.frames = import_folder(path)
        self.frame_index = 0
        self.image = self.frames[self.frame_index]

    def animate(self):
        self.frame_index += 0.15
        if self.frame_index >= len(self.frames):
            self.frame_index = 0
        self.image = self.frames[int(self.frame_index)]

    def update(self, shift):
        self.animate()
        self.rect.x += shift


class EnemyTile(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.import_character_assets()
        self.frame_index = 0
        self.image = self.animations["run"][self.frame_index]
        self.speed = random.randint(1, 2)
        self.animation_speed = 0.05
        self.direction = pygame.math.Vector2(0, 0)
        self.status = 'run'
        self.rect = self.image.get_rect(topleft=pos)
        self.facing_right = True
        self.on_ground = False
        self.on_ceiling = False
        self.on_left = False
        self.on_right = False

    def import_character_assets(self):
        entitie = random.choice(["dark_tortoise", "mushroom", "tortoise"])
        character_path = f"assets/entities/{entitie}/"
        self.animations = {"run": [], "death": []}

        for animation in self.animations.keys():
            full_path = character_path + animation
            self.animations[animation] = import_folder(full_path)

    def animate(self):
        animation = self.animations[self.status]
        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation):
            self.frame_index = 0

        self.image = animation[int(self.frame_index)]

    def move(self):
        self.rect.x += self.speed

    def reverse(self):
        self.speed *= -1

    def reversed_image(self):
        if self.speed > 0:
            self.image = pygame.transform.flip(self.image, True, False)

    def update(self):
        self.animate()
        self.move()
        self.reversed_image()

class Cup(StaticTile):
    def __init__(self, size, x, y, image):
        super().__init__(size, x, y)
        self.image = image
        
