from typing import Iterable, Union
import pygame
from pygame.sprite import AbstractGroup
from settings import *
from utils.tile import Tile
from model.player import Player
from debug import debug

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
        # passa pelas linhas
        for rowIndex, row in enumerate(world_map):
            # passa pelas colunas
            for columnindex, column in enumerate(row):
                x = columnindex * tileSize
                y = rowIndex * tileSize

                if column == 'x':
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
