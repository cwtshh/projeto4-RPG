from random import choice, randint
from typing import Iterable, Union
import pygame
from pygame.sprite import AbstractGroup
from settings import *
from utils.tile import Tile
from model.player import Player
from debug import debug
from utils.support import *
from model.weapon import Weapon
from UI.ui import UI
from model.enemy import Enemy
from model.particles import AnimationPlayer
from model.magic import MagicPlayer
from UI.upgrade import Upgrade

class Level:
    def __init__(self):
        # recebe o display
        self.display_surface = pygame.display.get_surface()
        self.gamePaused = False


        # inicia os sprites
        self.visible_sprites = YSortCameraGroup()
        self.obstacle_sprites = pygame.sprite.Group()

        # sprites de ataque
        self.current_attack = None
        self.attackSprites = pygame.sprite.Group()
        self.attackableSprites = pygame.sprite.Group()

        # configuracoes do mapa
        self.createMap()

        # interface de usuario
        self.ui = UI()
        self.upgrade = Upgrade(self.player)

        # particulas
        self.animationPlayer = AnimationPlayer()
        self.magicPLayer = MagicPlayer(self.animationPlayer)

    # cria o mapa
    def createMap(self):
        layouts = {
            'boundary': importCsvLayout(r'projeto4-RPG\ZeldaStyleRPG\map\map_FloorBlocks.csv'),
            'grass': importCsvLayout(r'projeto4-RPG\ZeldaStyleRPG\map\map_Grass.csv'),
            'object': importCsvLayout(r'projeto4-RPG\ZeldaStyleRPG\map\map_Objects.csv'),
            'entities': importCsvLayout(r'projeto4-RPG\ZeldaStyleRPG\map\map_Entities.csv')
        }

        graphics = {
            'grass': importFolder(r'projeto4-RPG\ZeldaStyleRPG\graphics\levelGraphics\grass'),
            'objects': importFolder(r'projeto4-RPG\ZeldaStyleRPG\graphics\levelGraphics\objects')
        }

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
                            Tile((x, y), 
                                 [self.visible_sprites, 
                                  self.obstacle_sprites, 
                                  self.attackableSprites], 
                                  'grass', 
                                  randomGrassImage)

                        if style == 'object':
                            surface = graphics['objects'][int(column)]
                            Tile((x, y), [self.visible_sprites, self.obstacle_sprites], 'object', surface)

                        if style == 'entities':
                            if column == '394':
                                self.player = Player(
                                    (x, y), 
                                    [self.visible_sprites], 
                                    self.obstacle_sprites, 
                                    self.create_attack, 
                                    self.destroy_attack, 
                                    self.create_magic)
                                
                            else:

                                if column == '390': monster_name = 'bamboo'

                                elif column == '391' : monster_name = 'spirit'

                                elif column == '392' : monster_name = 'raccoon'

                                else: monster_name = 'squid'

                                Enemy(monster_name, 
                                      (x, y), 
                                      [self.visible_sprites, 
                                       self.attackableSprites], 
                                       self.obstacle_sprites,
                                       self.damagePlayer,
                                       self.triggerDeathParticles,
                                       self.addXp)
        
    def create_attack(self):
        self.current_attack = Weapon(self.player, [self.visible_sprites, self.attackSprites])

    def create_magic(self, style, strength, cost):
        if style == 'heal':
            self.magicPLayer.heal(self.player, strength, cost, [self.visible_sprites])

        if style == 'flame':
            self.magicPLayer.flame(self.player, cost, [self.visible_sprites, self.attackSprites])

    def destroy_attack(self):
        if self.current_attack:
            self.current_attack.kill()

        self.current_attack = None
    
    def playerAttackLogic(self):
        if self.attackSprites:
            for attackSprite in self.attackSprites:
                collisionSprites = pygame.sprite.spritecollide(attackSprite, self.attackableSprites, False)

                if collisionSprites:
                    for targetSprite in collisionSprites:
                        if targetSprite.spriteType == 'grass':
                            pos = targetSprite.rect.center
                            offset = pygame.math.Vector2(0, 75)

                            for leaf in range(randint(3, 6)):
                                self.animationPlayer.createGrassParticles(pos - offset, [self.visible_sprites])


                            self.animationPlayer.createGrassParticles(pos, [self.visible_sprites])
                            targetSprite.kill()

                        else:
                            targetSprite.getDamage(self.player, attackSprite.spriteType)

    def damagePlayer(self, ammout, attackType):
        if self.player.vulnerable:
            self.player.health -= ammout
            self.player.vulnerable = False
            self.player.hurtTime = pygame.time.get_ticks()

            # spwan de sangue
            self.animationPlayer.createParticles(attackType, self.player.rect.center, [self.visible_sprites])

    def triggerDeathParticles(self, position, particleType):
        self.animationPlayer.createParticles(particleType, position, [self.visible_sprites])

    def addXp(self, ammount):
        self.player.exp += ammount

    def toggleMenu(self):
        self.gamePaused = not self.gamePaused

    def run(self):
        self.visible_sprites.customDraw(self.player)
        self.ui.display(self.player)

        if self.gamePaused:
            self.upgrade.display()


        else:
            #atualiza e desenha os sprites
            self.visible_sprites.update()
            self.visible_sprites.enemyUpdate(self.player)
            self.playerAttackLogic()




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

    def enemyUpdate(self, player):
        enemySprites = [sprite for sprite in self.sprites() if hasattr(sprite, 'spriteType') and sprite.spriteType == 'enemy']

        for enemy in enemySprites:
            enemy.enemyUpdate(player)
