import pygame

class Weapon(pygame.sprite.Sprite):
    def __init__(self, player, groups):
        super().__init__(groups)
        self.spriteType = 'weapon'

        # recebe a direcao do player
        direction = player.status.split('_')[0]

        # graficos
        fullPath = f'projeto4-RPG\\ZeldaStyleRPG\\graphics\\levelGraphics\\weapons\\{player.weapon}\\{direction}.png'
        self.image = pygame.image.load(fullPath).convert_alpha()

        # posicao
        if direction == 'right':
            self.rect = self.image.get_rect(midleft = player.rect.midright + pygame.math.Vector2(0, 16))

        elif direction == 'left':
            self.rect = self.image.get_rect(midright = player.rect.midleft + pygame.math.Vector2(0, 16))

        elif direction == 'down':
            self.rect = self.image.get_rect(midtop = player.rect.midbottom + pygame.math.Vector2(-10, 0))

        elif direction == 'up':
            self.rect = self.image.get_rect(midbottom = player.rect.midtop + pygame.math.Vector2(-10, 0))
        
        else:
            self.rect = self.image.get_rect(center = player.rect.center)
