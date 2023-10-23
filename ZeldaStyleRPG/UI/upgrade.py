import pygame
from settings import *

class Upgrade:
    def __init__(self, player):

        self.displaySurface = pygame.display.get_surface()
        self.player = player
        self.attributeNumber = len(self.player.stats)
        self.attributeNames = list(self.player.stats.keys())
        #self.maxValues = list(player.max.values())
        self.font = pygame.font.Font(UI_FONT, UI_FONT_SIZE)

        # dimensao dos itens
        self.height = self.displaySurface.get_size()[1] * 0.8
        self.width = self.displaySurface.get_size()[0] // 6
        self.createItems()

        # sistema de seleção
        self.selectionIndex = 0
        self.selectionTime = None
        self.canMove = True

        

    def input(self):
        keys = pygame.key.get_pressed()


        if self.canMove:

            if keys[pygame.K_RIGHT] and self.selectionIndex < self.attributeNumber - 1:
                self.selectionIndex += 1
                self.canMove = False
                self.selectionTime = pygame.time.get_ticks()

            if keys[pygame.K_LEFT] and self.selectionIndex >= 1:
                self.selectionIndex -= 1
                self.canMove = False
                self.selectionTime = pygame.time.get_ticks()

            if keys[pygame.K_SPACE]:
                self.canMove = False
                self.selectionTime = pygame.time.get_ticks()
                print(self.selectionIndex)

    def createItems(self):
        self.itemList = []

        for item, index in enumerate(range(self.attributeNumber)):

            fullWidth = self.displaySurface.get_size()[0]

            increment = fullWidth // self.attributeNumber

            left = (item * increment) + (increment - self.width) // 2

            top = self.displaySurface.get_size()[1] * 0.1

            # cria o objeto
            item = Item(left, top, self.width, self.height, index, self.font)
            
            self.itemList.append(item)

    def selectionCooldown(self):
        if not self.canMove:
            currentTime = pygame.time.get_ticks()

            if currentTime - self.selectionTime >= 300:
                self.canMove = True


    def display(self):
        self.input()
        self.selectionCooldown()
        for index, item in enumerate(self.itemList):
            name = self.attributeNames[index]
            value = self.player.getValueByIndex(index)
            #maxValue = self.maxValues[index]
            maxValue = 0
            cost = self.player.getCostByIndex(index)
            item.display(self.displaySurface, self.selectionIndex, name, value, maxValue, cost)


class Item:
    def __init__(self, left, top, width, height, index, font):
        self.rect = pygame.Rect(left, top, width, height)
        self.index = index
        self.font = font

    def display(self, surface, selectionNum, name, value, maxValue, cost):
        pygame.draw.rect(surface, UI_BG_COLOR, self.rect)