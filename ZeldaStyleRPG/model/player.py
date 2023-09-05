from utils.support import importFolder
import pygame
from settings import *

class Player(pygame.sprite.Sprite):
    def __init__(self, position, groups, obstacleSprites):
        super().__init__(groups)
        self.image = pygame.image.load(r'ZeldaStyleRPG\graphics\levelGraphics\test\player.png').convert_alpha()

        # recebe a posicao do tile
        self.rect = self.image.get_rect(topleft = position)
        self.hitbox = self.rect.inflate(0, -26)

        # importa os assets do player
        self.importPlayerAssets()
        self.status = 'down'
        self.frameIndex = 0
        self.animationSpeed = 0.15

        # movimentos do player
        self.direction = pygame.math.Vector2()
        self.speed = 5
        self.attacking = False
        self.attackCooldown = 400
        self.attackTime = None


        self.obstacleSprites = obstacleSprites

    def importPlayerAssets(self):
        # pasta que contem os assets do player
        characterPath = 'projeto4-RPG\\ZeldaStyleRPG\\graphics\\levelGraphics\\player\\'

        #salva os states de animaçoes
        self.animations = {
            'up' : [],
            'down' : [],
            'left' : [],
            'right' : [],
            'right_idle' : [],
            'left_idle' : [],
            'up_idle' : [],
            'down_idle' : [],
            'right_attack' : [],
            'left_attack' : [],
            'up_attack' : [],
            'down_attack' : [],
        }

        for animation in self.animations.keys():
            fullPath = characterPath + animation
            self.animations[animation] = importFolder(fullPath)


    def input(self):
        if not self.attacking:
            keys = pygame.key.get_pressed()

            # keys de movimento
            if keys[pygame.K_UP]:
                self.direction.y = -1
                self.status = 'up'
            elif keys[pygame.K_DOWN]:
                self.direction.y = 1
                self.status = 'down'
            else:
                self.direction.y = 0

            
            if keys[pygame.K_RIGHT]:
                self.direction.x = 1
                self.status = 'right'
            elif keys[pygame.K_LEFT]:
                self.direction.x = -1
                self.status = 'left'
            else:
                self.direction.x = 0

            # ataque
            if keys[pygame.K_SPACE] and not self.attacking:
                self.attacking = True
                self.attackTime = pygame.time.get_ticks()
                print("attack")

            # magia
            if keys[pygame.K_LCTRL] and not self.attacking:
                self.attacking = True
                self.attackTime = pygame.time.get_ticks()
                print("magic")

    def getStatus(self):
        # idle status
        if self.direction.x == 0 and self.direction.y == 0:
            if not 'idle' in self.status and not 'attack' in self.status:
                self.status = self.status + '_idle'

        if self.attacking:
                self.direction.x = 0
                self.direction.y = 0

                if not 'attack' in self.status:
                    if 'idle' in self.status:
                        #overite idl    e
                        self.status = self.status.replace('_idle', '_attack')
                    else:   
                        self.status = self.status + '_attack'
        else:
            if 'attack' in self.status:
                self.status = self.status.replace('_attack', '')


    def move(self, speed):
        # normaliza o vetor de direcao
        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize()
    
        self.hitbox.x += self.direction.x * speed
        self.collision('horizontal')

        self.hitbox.y += self.direction.y * speed
        self.collision('vertical')

        self.rect.center = self.hitbox.center

    def collision(self, direction):
        if direction == 'horizontal':
            for sprite in self.obstacleSprites:
                if sprite.hitbox.colliderect(self.hitbox):
                    if self.direction.x > 0:
                        self.hitbox.right = sprite.hitbox.left

                    if self.direction.x < 0:
                        self.hitbox.left = sprite.hitbox.right

        if direction == 'vertical':
            for sprite in self.obstacleSprites:
                if sprite.hitbox.colliderect(self.hitbox):
                    if self.direction.y > 0:
                        self.hitbox.bottom = sprite.hitbox.top

                    if self.direction.y < 0:
                        self.hitbox.top = sprite.hitbox.bottom

    def cooldowns(self):
        currentTime = pygame.time.get_ticks()

        if self.attacking:
            if currentTime - self.attackTime >= self.attackCooldown:
                self.attacking = False

    def animate(self):
        animation = self.animations[self.status]

        #loop over the frames
        self.frameIndex += self.animationSpeed

        if self.frameIndex >= len(animation):
            self.frameIndex = 0

        # seta a imagem
        self.image = animation[int(self.frameIndex)]
        self.rect = self.image.get_rect(center = self.hitbox.center)




    def update(self):
        self.input()
        self.cooldowns()
        self.getStatus()
        self.animate()
        self.move(self.speed)