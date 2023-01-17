import pygame
from pygame.locals import *
from os import path
import sys


pygame.init()

clock = pygame.time.Clock()
fps = 60

tile_size = 16
width = 60
heigth = 17
background_color = "#9290ff"

screen = pygame.display.set_mode((1920, 1080))

stones = pygame.image.load('assets/blocks/stones.png')
bricks = pygame.image.load('assets/blocks/bricks.png')
block = pygame.image.load('assets/blocks/block.png')

bush0 = pygame.image.load('assets/decor/bush0.png')
bush1 = pygame.image.load('assets/decor/bush1.png')
bush2 = pygame.image.load('assets/decor/bush2.png')
bush3 = pygame.image.load('assets/decor/bush3.png')
flower = pygame.image.load('assets/decor/flower.png')

invicible_block = pygame.image.load('assets/blocks/visible_collider.png')

mario = pygame.image.load('assets/entities/mario/fall/sprite_05.png')
enemy = pygame.image.load('assets/entities/mushroom/walk_0.png')

save_img = pygame.image.load('assets/buttons/play_up.png')
save_img = pygame.transform.scale(save_img, (40, 20))
load_img = pygame.image.load('assets/buttons/load_up.png')
load_img = pygame.transform.scale(load_img, (40, 20))

clicked = False
setup_tile = 0
font = pygame.font.SysFont('Futura', 24)

white = (255, 255, 255)
green = "#9290ff"

world_data = []
for row in range(heigth):
	r = [0] * width
	world_data.append(r)

for i in range(width):
	world_data[-1][i] = 1

tile = 0

def save():
	data = []
	for el in world_data:
		el = list(map(lambda x: str(x), el))
		data.append(",".join(el) + "\n")
	with open("levels/level.csv", "w", encoding="utf-8") as file:
		file.writelines(data)

def load():
	with open("levels/level.csv", "r", encoding="utf-8") as file:
		data = file.readlines()
		data = list(map(lambda x: x.replace("\n", "").split(","), data))
		rtrn = []
		for el in data:
			el = list(map(lambda x: int(x), el))
			rtrn.append(el)
	return rtrn

def draw_grid():
	for i in range(heigth + 1):
		pygame.draw.line(screen, white, (0, i * tile_size), (1920, i * tile_size))
	for i in range(width + 1):
		pygame.draw.line(screen, white, (i * tile_size, 0), (i * tile_size, 1080))

def draw_world():
	for row in range(heigth):
		for col in range(width):
			if world_data[row][col] == 1:
				img = pygame.transform.scale(stones, (tile_size, tile_size))
				screen.blit(img, (col * tile_size, row * tile_size))
			if world_data[row][col] == 2:
				img = pygame.transform.scale(bricks, (tile_size, tile_size))
				screen.blit(img, (col * tile_size, row * tile_size))
			if world_data[row][col] == 3:
				img = pygame.transform.scale(block, (tile_size, tile_size))
				screen.blit(img, (col * tile_size, row * tile_size))
			if world_data[row][col] == 4:
				img = pygame.transform.scale(bush0, (tile_size * 4, tile_size))
				screen.blit(img, (col * tile_size, row * tile_size))
			if world_data[row][col] == 5:
				img = pygame.transform.scale(bush1, (tile_size * 2, tile_size))
				screen.blit(img, (col * tile_size, row * tile_size))
			if world_data[row][col] == 6:
				img = pygame.transform.scale(bush2, (tile_size, tile_size))
				screen.blit(img, (col * tile_size, row * tile_size))
			if world_data[row][col] == 7:
				img = pygame.transform.scale(bush3, (tile_size, tile_size))
				screen.blit(img, (col * tile_size, row * tile_size))
			if world_data[row][col] == 8:
				img = pygame.transform.scale(flower, (tile_size, tile_size))
				screen.blit(img, (col * tile_size, row * tile_size))
			if world_data[row][col] == -1:
				img = pygame.transform.scale(mario, (tile_size, tile_size))
				screen.blit(img, (col * tile_size, row * tile_size))
			if world_data[row][col] == -2:
				img = pygame.transform.scale(invicible_block, (tile_size, tile_size))
				screen.blit(img, (col * tile_size, row * tile_size))
				
			if world_data[row][col] == -3:
				img = pygame.transform.scale(enemy, (tile_size, tile_size))
				screen.blit(img, (col * tile_size, row * tile_size))
				


def draw_text(text, font, text_col, x, y):
	img = font.render(text, True, text_col)
	screen.blit(img, (x, y))


class Button():
	def __init__(self, x, y, image):
		self.image = image
		self.rect = self.image.get_rect()
		self.rect.topleft = (x, y)
		self.clicked = False

	def draw(self):
		action = False

		pos = pygame.mouse.get_pos()

		if self.rect.collidepoint(pos):
			if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
				action = True
				self.clicked = True

		if pygame.mouse.get_pressed()[0] == 0:
			self.clicked = False

		screen.blit(self.image, (self.rect.x, self.rect.y), )

		return action


save_button = Button(1920 // 2 - 150, 1080 - 80, save_img)
load_button = Button(1920 // 2 + 50, 1080 - 80, load_img)


run = True
while run:
	clock.tick(fps)

	screen.fill(green)
	if save_button.draw():
		save()
	if load_button.draw():
		world_data = load()



	draw_grid()
	draw_world()
	draw_text(f'Selected tile: {tile}', font, white, tile_size, 1080 - 60)
	draw_text('Press UP or DOWN to change tile filling', font, white, tile_size, 1080 - 40)


	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			run = False
		if event.type == pygame.MOUSEBUTTONDOWN and clicked == False:
			clicked = True
		if clicked:
			pos = pygame.mouse.get_pos()
			x = pos[0] // tile_size
			y = pos[1] // tile_size
			if x < width and y < heigth:
				if pygame.mouse.get_pressed()[0] == 1:
					world_data[y][x] = tile
		if event.type == pygame.MOUSEBUTTONUP:
			clicked = False
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_UP:
				tile += 1
			elif event.key == pygame.K_DOWN:
				tile -= 1
		if event.type == KEYDOWN:
			if event.key == K_ESCAPE:
				pygame.quit()
				sys.exit()

	pygame.display.update()

pygame.quit()