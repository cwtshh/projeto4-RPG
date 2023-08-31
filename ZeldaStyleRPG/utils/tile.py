import pygame
from settings import *

class Tile(pygame.sprite.Sprite):
    def __init__(self, position, groups):
        super().__init__(groups)
        self.image = pygame.image.load(r'ZeldaStyleRPG\graphics\levelGraphics\test\rock.png').convert_alpha()
        # recebe a posicao do tile
        self.rect = self.image.get_rect(topleft = position)