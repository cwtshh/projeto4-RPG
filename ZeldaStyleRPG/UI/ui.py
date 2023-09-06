import pygame
from settings import *

class UI:
    def __init__(self):
        # geral
        self.displaySurface = pygame.display.get_surface()
        self.font = pygame.font.Font(UI_FONT, UI_FONT_SIZE)

        # barras
        self.healthBarRect = pygame.Rect(10, 10, HEALTH_BAR_WIDTH, BAR_HEIGHT)
        self.energyBarRect = pygame.Rect(10, 34, ENERGY_BAR_WIDTH, BAR_HEIGHT)


    def showBar(self, current, max_ammount, bg_rect, color):
        # desenha o bg
        pygame.draw.rect(self.displaySurface, UI_BG_COLOR, bg_rect)

        # converte os stats para pixel
        ratio = current / max_ammount
        current_width = ratio * bg_rect.width
        current_rect = bg_rect.copy()
        current_rect.width = current_width

        # desenha a barra
        pygame.draw.rect(self.displaySurface, color, current_rect)
        pygame.draw.rect(self.displaySurface, UI_BORDER_COLOR, bg_rect, 3)

        # converte armas para um dicionario
        self.weaponGraphics = []
        for weapon in weapon_data.values():
            path = weapon['graphic']
            weapon = pygame.image.load(path).convert_alpha()
            self.weaponGraphics.append(weapon)


    def showExp(self, exp):
        text_surface = self.font.render("XP: " + str(int(exp)), False, TEXT_COLOR)
        x = self.displaySurface.get_size()[0] - 20
        y = self.displaySurface.get_size()[1] - 20
        text_rect = text_surface.get_rect(bottomright = (x, y))

        pygame.draw.rect(self.displaySurface, UI_BG_COLOR, text_rect.inflate(20, 20))
        self.displaySurface.blit(text_surface, text_rect)
        pygame.draw.rect(self.displaySurface, UI_BG_COLOR, text_rect.inflate(20, 20), 3)

    def selection_box(self, left, top, has_switched):
        bg_rect = pygame.Rect(left, top, ITEM_BOX_SIZE, ITEM_BOX_SIZE)
        pygame.draw.rect(self.displaySurface, UI_BG_COLOR, bg_rect)
        if has_switched:
            pygame.draw.rect(self.displaySurface, UI_BORDER_COLOR_ACTIVE, bg_rect, 3)
        else:
            pygame.draw.rect(self.displaySurface, UI_BORDER_COLOR, bg_rect, 3)

        return bg_rect

    def weaponOverlay(self, weaponIndex, has_switched):
        bg_rect = self.selection_box(10, 600, has_switched)
        weapon_surf = self.weaponGraphics[weaponIndex]
        weapon_rect = weapon_surf.get_rect(center = bg_rect.center)

        self.displaySurface.blit(weapon_surf, weapon_rect)





    def display(self, player):
        self.showBar(player.health, player.stats['health'], self.healthBarRect, HEALTH_COLOR)
        self.showBar(player.energy, player.stats['energy'], self.energyBarRect, ENERGY_COLOR)

        self.showExp(player.exp)

        #self.selection_box(10, 600, player.canSwitchWeapon)
        self.weaponOverlay(player.weapon_index, player.canSwitchWeapon)
        #self.selection_box(85, 635)