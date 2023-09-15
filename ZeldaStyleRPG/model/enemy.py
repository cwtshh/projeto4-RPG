import pygame
from settings import *
from model.entity import Entity
from utils.support import importFolder


class Enemy(Entity):
    def __init__(self, monsterName, pos, groups, obstacleSprites):

        # geral
        super().__init__(groups)
        self.spriteType = 'enemy'

        # graficos
        self.importGraphics(monsterName)
        self.status = 'idle'
        self.image = self.animations[self.status][self.frameIndex]
        self.rect = self.image.get_rect(topleft = pos)

        # movimentos
        self.rect = self.image.get_rect(topleft = pos)
        self.hitbox = self.rect.inflate(0, -10)
        self.obstacleSprites = obstacleSprites

        # status
        self.mosnterName = monsterName
        monsterInfo = monster_data[monsterName]
        self.health = monsterInfo['health']
        self.speed = monsterInfo['speed']
        self.attackDamage = monsterInfo['damage']
        self.exp = monsterInfo['exp']
        self.resistance = monsterInfo['resistance']
        self.attackRadius = monsterInfo['attack_radius']
        self.noticeRadius = monsterInfo['notice_radius']
        self.attackType = monsterInfo['attack_type']

        # interacao com o player
        self.canAttack = True
        self.attackTime = None
        self.attackCooldown = 400



    def importGraphics(self, name):
        self.animations = {
            'idle': [],
            'move': [],
            'attack': [],
        }

        main_path = f'projeto4-RPG\\ZeldaStyleRPG\\graphics\\levelGraphics\\monsters\\{name}\\'

        for animation in self.animations.keys():
            self.animations[animation] = importFolder(main_path + animation)

    def getPlayerDistanceDirection(self, player):
        enemyVector = pygame.math.Vector2(self.rect.center)
        playerVector = pygame.math.Vector2(player.rect.center)
        distance = (playerVector - enemyVector).magnitude()


        if distance > 0:
            direction = (playerVector - enemyVector).normalize()

        else:
            direction = pygame.math.Vector2()

        return (distance, direction)

    def getStatus(self, player):
        distance = self.getPlayerDistanceDirection(player)[0]

        if distance <= self.attackRadius and self.canAttack:
            if self.status != 'attack':
                self.frameIndex = 0
    
            self.status = 'attack'
        elif distance <= self.noticeRadius:
            self.status = 'move'
        else:
            self.status = 'idle'
    
    def actions(self, player):
        if self.status == 'attack':
            self.attackTime = pygame.time.get_ticks()
            print('atacou')

        if self.status == 'move':
            self.direction = self.getPlayerDistanceDirection(player)[1]
    
        else:
            self.direction = pygame.math.Vector2()

    def animate(self):
        animation = self.animations[self.status]

        self.frameIndex += self.animationSpeed

        if self.frameIndex >= len(animation):
            if self.status == 'attack':
                self.canAttack = False

            self.frameIndex = 0

        self.image = animation[int(self.frameIndex)]
        self.rect = self.image.get_rect(center = self.hitbox.center)

    def cooldown(self):
        if not self.canAttack:
            currentTime = pygame.time.get_ticks()

            if currentTime - self.attackTime >= self.attackCooldown:
                self.canAttack = True
    
    def update(self):
        self.move(self.speed)
        self.animate()
        self.cooldown()

    def enemyUpdate(self, player):
        self.getStatus(player)
        self.actions(player)
    