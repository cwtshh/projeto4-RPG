from csv import reader
from os import walk
import pygame

def importCsvLayout(path):
    terrainMap = []
    with open(path, 'r') as levelMap:
        layout = reader(levelMap, delimiter = ',')
        for row in layout:
            terrainMap.append(list(row))

        return terrainMap


def importFolder(path):
    surface_list = []

    for _,__,img_files in walk(path):
        for image in img_files:
            full_path = path + '\\' + image
            image_surf = pygame.image.load(full_path).convert_alpha()
            surface_list.append(image_surf)

    return surface_list

