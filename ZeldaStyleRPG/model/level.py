import pygame
from settings import *
from utils.tile import Tile
from model.player import Player
from debug import debug

class Level:
    def __init__(self):
        # recebe o display
        self.display_surface = pygame.display.get_surface()


        # inicia os sprites
        self.visible_sprites = pygame.sprite.Group()
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
        self.visible_sprites.draw(self.display_surface)
        self.visible_sprites.update()
        debug(self.player.direction)