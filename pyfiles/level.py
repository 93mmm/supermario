import pygame
from pyfiles.support_level import import_csv_layout, import_cut_graphics
import json
from pyfiles.tiles import StaticTile, Tree
from pyfiles.player import Player

with open("json_files/settings.json", "r") as file:
    data = json.load(file)

tile_size = data["settings_window"]["tile_size"]
screen_width = data["settings_window"]["screen_width"]


class Level:
    def __init__(self, level_data, surface):
        # главные настройки
        self.display_surface = surface
        self.world_shift = 0

        # настройки блоков камня(stone)
        stone_layout = import_csv_layout(level_data["stone"])
        self.stone_sprites = self.create_tile_group(stone_layout, "stone")

        #настройка травы(grass)
        grass_layout = import_csv_layout(level_data["grass"])
        self.grass_sprites = self.create_tile_group(grass_layout, "grass")

        # настройка деревьев(trees)
        trees_layout = import_csv_layout(level_data["bg trees"])
        self.trees_sprites = self.create_tile_group(trees_layout, "bg trees")

        # игрок
        player_layout = import_csv_layout(level_data["player"])
        self.player = pygame.sprite.GroupSingle()
        self.end = pygame.sprite.GroupSingle()
        self.player_setup(player_layout)

    def create_tile_group(self, layout, type):
        sprite_group = pygame.sprite.Group()

        for row_index, row in enumerate(layout):
            for col_index, val in enumerate(row):
                if val != "-1":
                    x = col_index * tile_size
                    y = row_index * tile_size

                    if type == "stone":
                        stone_tile_list = import_cut_graphics("presets/graphics/dungeon_decoration/stone_tiles_light.png")
                        tile_surface = stone_tile_list[int(val)]
                        sprite = StaticTile(tile_size, x, y, tile_surface)
                        sprite_group.add(sprite)

                    if type == "grass":
                        grass_tile_list = import_cut_graphics("presets/graphics/decoration/grass/grass.png")
                        tile_surface = grass_tile_list[int(val)]
                        sprite = StaticTile(tile_size, x, y, tile_surface)
                        sprite_group.add(sprite)

                    if type == "bg trees":
                        sprite = Tree(tile_size, x, y, "presets/graphics/dungeon_decoration/palm_bg", 64)
                        sprite_group.add(sprite)

        return sprite_group

    def player_setup(self, layout):
        for row_index, row in enumerate(layout):
            for col_index, val in enumerate(row):
                x = col_index * tile_size
                y = row_index * tile_size
                if val == "0":
                    sprite = Player((x, y))
                    self.player.add(sprite)
                if val == "1":
                    pass
                    #добавить кубок как конец уровня"

    def horizontal_movement_collision(self):
        player = self.player.sprite
        player.rect.x += player.direction.x * player.speed

        collidable_sprites = self.stone_sprites.sprites()
        for sprite in collidable_sprites:
            if sprite.rect.colliderect(player.rect):
                if player.direction.x < 0:
                    player.rect.left = sprite.rect.right
                    player.on_left = True
                    self.current_x = player.rect.left
                elif player.direction.x > 0:
                    player.rect.right = sprite.rect.left
                    player.on_right = True
                    self.current_x = player.rect.right

        if player.on_left and (player.rect.left < self.current_x or player.direction.x >= 0):
            player.on_left = False
        if player.on_right and (player.rect.right > self.current_x or player.direction.x <= 0):
            player.on_right = False

    def vertical_movement_collision(self):
        player = self.player.sprite
        player.apply_gravity()
        collidable_sprites = self.stone_sprites.sprites()

        for sprite in collidable_sprites:
            if sprite.rect.colliderect(player.rect):
                if player.direction.y > 0:
                    player.rect.bottom = sprite.rect.top
                    player.direction.y = 0
                    player.on_ground = True
                elif player.direction.y < 0:
                    player.rect.top = sprite.rect.bottom
                    player.direction.y = 0
                    player.on_ceiling = True

        if player.on_ground and player.direction.y < 0 or player.direction.y > 1:
            player.on_ground = False
        if player.on_ceiling and player.direction.y > 0.1:
            player.on_ceiling = False

    def scroll_x(self):
        player = self.player.sprite
        player_x = player.rect.centerx
        direction_x = player.direction.x

        if player_x < screen_width / 4 and direction_x < 0:
            self.world_shift = 8
            player.speed = 0
        elif player_x > screen_width - (screen_width / 4) and direction_x > 0:
            self.world_shift = -8
            player.speed = 0
        else:
            self.world_shift = 0
            player.speed = 8

    def run(self):

        # блоки камня
        self.stone_sprites.draw(self.display_surface)
        self.stone_sprites.update(self.world_shift)

        # трава
        self.grass_sprites.draw(self.display_surface)
        self.grass_sprites.update(self.world_shift)

        # деревья
        self.trees_sprites.update(self.world_shift)
        self.trees_sprites.draw(self.display_surface)

        # игрок
        self.player.update()
        self.horizontal_movement_collision()
        self.vertical_movement_collision()
        self.scroll_x()
        self.player.draw(self.display_surface)

# В будущем добавить остальные детали декора, как вода, небо, облака и т.д