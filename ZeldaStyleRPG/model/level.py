from random import choice
from typing import Iterable, Union
import pygame
from pygame.sprite import AbstractGroup
from settings import *
from utils.tile import Tile
from model.player import Player
from debug import debug
from utils.support import *

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
        layouts = {
            'boundary': importCsvLayout(r'projeto4-RPG\ZeldaStyleRPG\map\map_FloorBlocks.csv'),
            'grass': importCsvLayout(r'projeto4-RPG\ZeldaStyleRPG\map\map_Grass.csv'),
            'object': importCsvLayout(r'projeto4-RPG\ZeldaStyleRPG\map\map_Objects.csv')
        }

        graphics = {
            'grass': importFolder(r'projeto4-RPG\ZeldaStyleRPG\graphics\levelGraphics\grass'),
            'objects': importFolder(r'projeto4-RPG\ZeldaStyleRPG\graphics\levelGraphics\objects')
        }

        print(graphics)

        for style, layout in layouts.items():
            for rowIndex, row in enumerate(layout):
                for columnIndex, column in enumerate(row):
                    if column != '-1':
                        x = columnIndex * tileSize
                        y = rowIndex * tileSize

                        if style == 'boundary':
                            Tile((x, y), [self.obstacle_sprites], 'invisible')

                        if style == 'grass':
                            randomGrassImage = choice(graphics['grass'])
                            Tile((x, y), [self.visible_sprites, self.obstacle_sprites], 'visible', randomGrassImage)

                        if style == 'object':
                            surface = graphics['objects'][int(column)]
                            Tile((x, y), [self.visible_sprites, self.obstacle_sprites], 'object', surface)
        
        self.player = Player((2000, 1500), [self.visible_sprites], self.obstacle_sprites)





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

        # cria o chao
        self.floorSurface = pygame.image.load(r'projeto4-RPG\ZeldaStyleRPG\graphics\levelGraphics\tilemap\ground.png').convert()
        self.floor_rect = self.floorSurface.get_rect(topleft = (0, 0))

    def customDraw(self, player):

        # calcula o offset
        self.offset.x = player.rect.centerx - self.half_width
        self.offset.y = player.rect.centery - self.half_height

        # desenha o chao
        floor_offset_position = self.floor_rect.topleft - self.offset
        self.display_surface.blit(self.floorSurface, floor_offset_position)


        for sprite in sorted(self.sprites(), key= lambda sprite: sprite.rect.centery):
            offset_position = sprite.rect.topleft - self.offset
            self.display_surface.blit(sprite.image, offset_position)
