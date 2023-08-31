from typing import Iterable, Union
import pygame
from pygame.sprite import AbstractGroup
from settings import *
from utils.tile import Tile
from model.player import Player
from debug import debug
import random

def generate_map(width, height, wall_percentage):
    map = [[0 for _ in range(width)] for _ in range(height)]
    
    for y in range(1, height - 1):
        for x in range(1, width - 1):
            if random.random() < wall_percentage:
                map[y][x] = 395
    
    for y in range(height):
        map[y][0] = 395
        map[y][width - 1] = 395
    
    for x in range(width):
        map[0][x] = 395
        map[height - 1][x] = 395
    
    start_x = random.randint(1, width - 2)
    start_y = random.randint(1, height - 2)
    map[start_y][start_x] = "p"
    
    return map


generated_map = generate_map(24, 24, 0.4)


class Level:
    def __init__(self):
        # recebe o display
        self.display_surface = pygame.display.get_surface()


        # inicia os sprites
        self.visible_sprites = YSortCameraGroup()
        self.obstacle_sprites = pygame.sprite.Group()

        # configuracoes do mapa
        self.createMap()

    # cria o mapa
    def createMap(self):
        print(generated_map)
        # passa pelas linhas
        for rowIndex, row in enumerate(generated_map):
            # passa pelas colunas
            for columnindex, column in enumerate(row):
                x = columnindex * tileSize
                y = rowIndex * tileSize

                if column != 0:
                    # captura a posicao da tile
                    Tile((x, y), [self.visible_sprites, self.obstacle_sprites])

                if column == 'p':
                    # captura a posicao do player
                    self.player = Player((x, y), [self.visible_sprites], self.obstacle_sprites)





    def run(self):
        #atualiza e desenha os sprites
        self.visible_sprites.customDraw(self.player)
        self.visible_sprites.update()


class YSortCameraGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.display_surface = pygame.display.get_surface()

        # metade da largura e altura da tela
        self.half_width = self.display_surface.get_size()[0] // 2
        self.half_height = self.display_surface.get_size()[1] // 2

        # offset do grupo
        self.offset = pygame.math.Vector2()

    def customDraw(self, player):

        # calcula o offset
        self.offset.x = player.rect.centerx - self.half_width
        self.offset.y = player.rect.centery - self.half_height


        for sprite in sorted(self.sprites(), key= lambda sprite: sprite.rect.centery):
            offset_position = sprite.rect.topleft - self.offset
            self.display_surface.blit(sprite.image, offset_position)
