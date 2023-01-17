import pygame
import sys
from scripts.tiles import StaticTile, EnemyTile
from scripts.player import Player
from scripts.game_data import tile_size, screen_width, levels
from scripts.support_function import get_font, import_csv_layout
from scripts.enemy import Enemy


class Level:
    def __init__(self, level, surface):
        # главные настройки
        self.surface = surface
        self.world_shift = 0
        self.player_is_dead = False

        # настройки карты
        self.map_design = import_csv_layout(levels[level])

        self.stones = pygame.image.load('assets/blocks/stones.png')
        self.bricks = pygame.image.load('assets/blocks/bricks.png')
        self.block = pygame.image.load('assets/blocks/block.png')

        self.invicible_block = pygame.image.load('assets/blocks/invicible_collider.png')

        self.bush0 = pygame.image.load('assets/decor/bush0.png')
        self.bush1 = pygame.image.load('assets/decor/bush1.png')
        self.bush2 = pygame.image.load('assets/decor/bush2.png')
        self.bush3 = pygame.image.load('assets/decor/bush3.png')
        self.flower = pygame.image.load('assets/decor/flower.png')

        self.create_tile_group()

        self.score = 1
        self.level_number = level
        self.time = 0
    
    def create_tile_group(self):
        self.colliders = pygame.sprite.Group()
        self.not_colliders = pygame.sprite.Group()
        self.enemies_colliders = []
        for row in range(len(self.map_design)):
            for col in range(len(self.map_design[0])):
                if self.map_design[row][col] != "0":
                    if self.map_design[row][col] == '1':
                        img = pygame.transform.scale(
                            self.stones, (tile_size, tile_size))
                        new_surface = pygame.Surface((tile_size, tile_size), flags=pygame.SRCALPHA)
                        new_surface.blit(img, (0, 0))
                        self.colliders.add(StaticTile(tile_size, col * tile_size, row * tile_size, img))

                    elif self.map_design[row][col] == '2':
                        img = pygame.transform.scale(
                            self.bricks, (tile_size, tile_size))
                        new_surface = pygame.Surface((tile_size, tile_size), flags=pygame.SRCALPHA)
                        new_surface.blit(img, (0, 0))
                        self.colliders.add(StaticTile(tile_size, col * tile_size, row * tile_size, img))

                    elif self.map_design[row][col] == '3':
                        img = pygame.transform.scale(self.block, (tile_size, tile_size))
                        new_surface = pygame.Surface((tile_size, tile_size), flags=pygame.SRCALPHA)
                        new_surface.blit(img, (0, 0))
                        self.colliders.add(StaticTile(tile_size, col * tile_size, row * tile_size, img))

                    elif self.map_design[row][col] == '4':
                        img = pygame.transform.scale(
                            self.bush0, (tile_size * 4, tile_size))
                        new_surface = pygame.Surface((tile_size, tile_size), flags=pygame.SRCALPHA)
                        new_surface.blit(img, (0, 0))
                        self.not_colliders.add(StaticTile(tile_size, col * tile_size, row * tile_size, img))

                    elif self.map_design[row][col] == '5':
                        img = pygame.transform.scale(
                            self.bush1, (tile_size * 2, tile_size))
                        new_surface = pygame.Surface((tile_size, tile_size), flags=pygame.SRCALPHA)
                        new_surface.blit(img, (0, 0))
                        self.not_colliders.add(StaticTile(tile_size, col * tile_size, row * tile_size, img))

                    elif self.map_design[row][col] == '6':
                        img = pygame.transform.scale(self.bush2, (tile_size, tile_size))
                        new_surface = pygame.Surface((tile_size, tile_size), flags=pygame.SRCALPHA)
                        new_surface.blit(img, (0, 0))
                        self.not_colliders.add(StaticTile(tile_size, col * tile_size, row * tile_size, img))

                    elif self.map_design[row][col] == '7':
                        img = pygame.transform.scale(self.bush3, (tile_size, tile_size))
                        new_surface = pygame.Surface((tile_size, tile_size), flags=pygame.SRCALPHA)
                        new_surface.blit(img, (0, 0))
                        self.not_colliders.add(StaticTile(tile_size, col * tile_size, row * tile_size, img))

                    elif self.map_design[row][col] == '8':
                        img = pygame.transform.scale(
                            self.flower, (tile_size, tile_size))
                        new_surface = pygame.Surface((tile_size, tile_size), flags=pygame.SRCALPHA)
                        new_surface.blit(img, (0, 0))
                        self.not_colliders.add(StaticTile(tile_size, col * tile_size, row * tile_size, img))

                    elif self.map_design[row][col] == "-1":
                        self.player = pygame.sprite.GroupSingle()
                        sprite = Player((col * tile_size, row * tile_size))
                        self.player.add(sprite)

                    elif self.map_design[row][col] == "-2":
                        img = pygame.transform.scale(
                            self.invicible_block, (tile_size, tile_size))
                        new_surface = pygame.Surface((tile_size, tile_size), flags=pygame.SRCALPHA)
                        new_surface.blit(img, (0, 0))
                        self.colliders.add(StaticTile(tile_size, col * tile_size, row * tile_size, img))

                    elif self.map_design[row][col] == "-3":
                        enemy = pygame.sprite.GroupSingle()
                        sprite = EnemyTile((col * tile_size, row * tile_size))
                        enemy.add(sprite)

                        self.enemies_colliders.append(enemy)
    
    def horizontal_movement_collision(self):
        player = self.player.sprite
        player.rect.x += player.direction.x * player.speed

        collidable_sprites = self.colliders.sprites()
        if not player.collision_off:
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
        collidable_sprites = self.colliders.sprites()

        if not player.collision_off:
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

    def enemies_collision_person(self):
        player = self.player.sprite
        for sprite in self.enemies_colliders:
            sprite = sprite.sprites()
            if not player.collision_off:
                for i in sprite:
                    if i.rect.colliderect(player.rect):
                        if player.direction.y > 0:
                            player.kill_player()
                        elif player.direction.y < 0:
                            player.kill_player()
                            self.player_is_dead = True

    def enemies_collision_blocks(self):
        collidable_sprites = self.colliders
        for enemy in self.enemies_colliders:
            enemy = enemy.sprites()
            for entity in enemy:
                if pygame.sprite.spritecollide(entity, collidable_sprites, False):
                    entity.reverse()

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
    
    def draw_score(self):
        color = "#ffffff"

        time = get_font(40).render("TIME", True, color)
        time_rect = time.get_rect(center=(100, 30))
        self.surface.blit(time, time_rect)

        time = get_font(40).render(f"{self.time}", True, color)
        time_rect = time.get_rect(center=(100, 71))
        self.surface.blit(time, time_rect)

        world = get_font(40).render("WORLD", True, color)
        level_rect = world.get_rect(center=(960, 30))
        self.surface.blit(world, level_rect)

        level = self.level_number.split("_")[-1]
        level = get_font(40).render(f"{level}", True, color)
        level_rect = level.get_rect(center=(960, 71))
        self.surface.blit(level, level_rect)
        
        score = get_font(40).render("MARIO", True, color)
        score_rect = score.get_rect(center=(1800, 30))
        self.surface.blit(score, score_rect)

        score_text = get_font(40).render(f"{self.score:06}", True, color)
        score_text_rect = score_text.get_rect(center=(1800, 71))
        self.surface.blit(score_text, score_text_rect)

    def run(self):
        # коллайдеры
        self.colliders.draw(self.surface)
        self.colliders.update(self.world_shift)
        self.not_colliders.draw(self.surface)
        self.not_colliders.update(self.world_shift)

        # счётчики
        self.draw_score()

        # игрок
        self.player.update()
        self.horizontal_movement_collision()
        self.vertical_movement_collision()
        self.scroll_x()
        self.player.draw(self.surface)
        self.enemies_collision_person()

        # противники
        self.enemies_collision_blocks()
        for entity in self.enemies_colliders:
            entity.draw(self.surface)
            entity.update()
            entity.sprite.rect.x += self.world_shift