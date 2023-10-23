import pygame
from settings import *
from random import randint

class MagicPlayer:
    def __init__(self, animationPlauer):
        self.animationPlayer = animationPlauer
        self.sounds = {
            'heal': pygame.mixer.Sound(r"projeto4-RPG\ZeldaStyleRPG\audio\heal.wav"),
            'flame': pygame.mixer.Sound(r"projeto4-RPG\ZeldaStyleRPG\audio\Fire.wav")
        }
        self.sounds['heal'].set_volume(0.3)
        self.sounds['flame'].set_volume(0.3)


    def heal(self, player, strength, cost, groups):
        if player.energy >= cost:
            player.health += strength
            player.energy -= cost
            self.sounds['heal'].play()

            if player.health >= player.stats['health']:
                player.health = player.stats['health']

            self.animationPlayer.createParticles('aura', player.rect.center, groups)
            self.animationPlayer.createParticles('heal', player.rect.center + pygame.math.Vector2(0, -60), groups)



    def flame(self, player, cost, groups):
        if player.energy >= cost:
            player.energy -= cost
            self.sounds['flame'].play()

            if player.status.split('_')[0] == 'right':
                direction = pygame.math.Vector2(1, 0)

            elif player.status.split('_')[0] == 'left':
                direction = pygame.math.Vector2(-1, 0)

            elif player.status.split('_')[0] == 'up':
                direction = pygame.math.Vector2(0, -1)

            else:
                direction = pygame.math.Vector2(0, 1)


            for i in range(1, 6):
                if direction.x:
                    offsetX = (direction.x * i) * tileSize

                    x = player.rect.centerx + offsetX + randint(-tileSize//3, tileSize//3)
                    y = player.rect.centery + randint(-tileSize//3, tileSize//3)

                    self.animationPlayer.createParticles('flame', (x, y), groups)

                else:
                    offsetY = (direction.y * i) * tileSize
                    x = player.rect.centerx + randint(-tileSize//3, tileSize//3)
                    y = player.rect.centery + offsetY + randint(-tileSize//3, tileSize//3)

                    self.animationPlayer.createParticles('flame', (x, y), groups)

            