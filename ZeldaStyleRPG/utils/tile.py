import pygame
from settings import *

class Tile(pygame.sprite.Sprite):
    def __init__(self, position, groups, spriteType, surface = pygame.Surface((tileSize, tileSize))):
        super().__init__(groups)
        self.spriteType = spriteType
        self.image = surface

        if spriteType == 'object':
            # faz um offset no tile
            self.rect = self.image.get_rect(topleft = (position[0], position[1] - tileSize))
        else: 
            # recebe a posicao do tile
            self.rect = self.image.get_rect(topleft = position)

        # cria o hitbox
        self.hitbox = self.rect.inflate(0, -10)