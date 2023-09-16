from utils.support import importFolder
import pygame
from settings import *
from model.entity import Entity

class Player(Entity):
    def __init__(self, position, groups, obstacleSprites, createAttack, destroyAttack, createMagic):
        super().__init__(groups)
        self.image = pygame.image.load(r'projeto4-RPG\ZeldaStyleRPG\graphics\levelGraphics\test\player.png').convert_alpha()

        # recebe a posicao do tile
        self.rect = self.image.get_rect(topleft = position)
        self.hitbox = self.rect.inflate(0, -26)

        # importa os assets do player
        self.importPlayerAssets()
        self.status = 'down'

        # movimentos do player
        self.speed = 5
        self.attacking = False
        self.attackCooldown = 400
        self.attackTime = None
        self.obstacleSprites = obstacleSprites

        
        # armas
        self.createAttack = createAttack
        self.destroyAttack = destroyAttack
        self.weapon_index = 0
        self.weapon = list(weapon_data.keys())[self.weapon_index]
        self.canSwitchWeapon = True
        self.weaponSwitchTime = None
        self.switchDurationCooldown = 200

        # magia
        self.createMagic = createMagic
        self.magic_index = 0
        self.magic = list(magic_data.keys())[self.magic_index]
        self.canSwitchMagic = True
        self.magicSwitchTime = None


        # stats
        self.stats = {'health': 100, 'energy': 60, 'attack': 10, 'magic': 4, 'speed': 6}
        self.health = self.stats['health']
        self.energy = self.stats['energy']
        self.speed = self.stats['speed']
        self.exp = 123

        # damage timer
        self.vulnerable = True
        self.hurtTime = None
        self.invunerableDuration = 500


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
                self.createAttack()

            # magia
            if keys[pygame.K_LCTRL]:
                self.attacking = True
                self.attackTime = pygame.time.get_ticks()

                style = list(magic_data.keys())[self.magic_index]
                strength = list(magic_data.values())[self.magic_index]['strenght'] + self.stats['magic']
                cost = list(magic_data.values())[self.magic_index]['cost']

                self.createMagic(style, strength, cost)

            # troca de armas
            if keys[pygame.K_q] and self.canSwitchWeapon:
                self.canSwitchWeapon = False
                self.weaponSwitchTime = pygame.time.get_ticks()

                if self.weapon_index < len(list(weapon_data.keys())) - 1:
                    self.weapon_index += 1
                else:
                    self.weapon_index = 0


                self.weapon = list(weapon_data.keys())[self.weapon_index]

            if keys[pygame.K_e] and self.canSwitchMagic:
                self.canSwitchMagic = False
                self.magicSwitchTime = pygame.time.get_ticks()

                if self.magic_index < len(list(magic_data.keys())) - 1:
                    self.magic_index += 1
                else:
                    self.magic_index = 0

                self.magic = list(magic_data.keys())[self.magic_index]

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
    
    def cooldowns(self):
        currentTime = pygame.time.get_ticks()

        if self.attacking:
            if currentTime - self.attackTime >= self.attackCooldown + weapon_data[self.weapon]['cooldown']:
                self.attacking = False
                self.destroyAttack()

        if not self.canSwitchWeapon:
            if currentTime - self.weaponSwitchTime >= self.switchDurationCooldown:
                self.canSwitchWeapon = True

        if not self.canSwitchMagic:
            if currentTime - self.magicSwitchTime >= self.switchDurationCooldown:
                self.canSwitchMagic = True

        if not self.vulnerable:
            if currentTime - self.hurtTime >= self.invunerableDuration:
                self.vulnerable = True

    def animate(self):
        animation = self.animations[self.status]

        #loop over the frames
        self.frameIndex += self.animationSpeed

        if self.frameIndex >= len(animation):
            self.frameIndex = 0

        # seta a imagem
        self.image = animation[int(self.frameIndex)]
        self.rect = self.image.get_rect(center = self.hitbox.center)

        # animaçao de dano
        if not self.vulnerable:
            alpha = self.wave_value()
            self.image.set_alpha(alpha)
        
        else:
            self.image.set_alpha(255)

    def getFullWeaponDamage(self):
        baseDamage = self.stats['attack']
        weaponDamage = weapon_data[self.weapon]['damage']

        return baseDamage + weaponDamage

    def getFullMagicDamage(self):
        baseDamage = self.stats['magic']
        spellDamage = magic_data[self.magic]['strenght']

        return baseDamage + spellDamage

    def energyRecovery(self):
        if self.energy < self.stats['energy']:
            self.energy += 0.004 * self.stats['magic']

        else:
            self.energy = self.stats['energy']

    def update(self):
        self.input()
        self.cooldowns()
        self.getStatus()
        self.animate()
        self.move(self.speed)
        self.energyRecovery()