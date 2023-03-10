import pygame
from csv import reader
from pygame.locals import QUIT, KEYDOWN, K_ESCAPE
import sys
from os import walk


def get_font(size):
    return pygame.font.Font("assets/fonts/font.ttf", size)


def exit_check(event):
    if event.type == QUIT:
        pygame.quit()
        sys.exit()
    if event.type == KEYDOWN:
        if event.key == K_ESCAPE:
            pygame.quit()
            sys.exit()


def import_csv_layout(path):
    design = []
    with open(path, "r") as file:
        level = reader(file, delimiter=",")
        for row in level:
            design.append(list(row))

    return design


def import_folder(path):
    surface_list = []
    for _, __, image_files in walk(path):
        for image in image_files:
            full_path = path + "/" + image
            image_surface = pygame.image.load(full_path).convert_alpha()
            surface_list.append(image_surface)

    return surface_list


def import_folder(path):
    surface_list = []

    for _, __, image_files in walk(path):
        for image in image_files:
            full_path = path + "/" + image
            image_surface = pygame.image.load(full_path).convert_alpha()
            surface_list.append(image_surface)

    return surface_list
