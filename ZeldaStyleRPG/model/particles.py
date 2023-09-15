from random import choice
import pygame
from utils.support import importFolder

class AnimationPlayer:
    def __init__(self):
        self.frames = {
            'flame': importFolder('projeto4-RPG\\ZeldaStyleRPG\\graphics\\levelGraphics\\particles\\flame\\frames'),
            'aura': importFolder('projeto4-RPG\\ZeldaStyleRPG\\graphics\\levelGraphics\\particles\\aura'),
            'heal': importFolder('projeto4-RPG\\ZeldaStyleRPG\\graphics\\levelGraphics\\particles\\heal\\frames'),

            # ataques
            'claw': importFolder('projeto4-RPG\\ZeldaStyleRPG\\graphics\\levelGraphics\\particles\\claw'),
            'slash': importFolder('projeto4-RPG\\ZeldaStyleRPG\\graphics\\levelGraphics\\particles\\slash'),
            'sparkle': importFolder('projeto4-RPG\\ZeldaStyleRPG\\graphics\\levelGraphics\\particles\\sparkle'),
            'leaf_attack': importFolder('projeto4-RPG\\ZeldaStyleRPG\\graphics\\levelGraphics\\particles\\leaf_attack'),
            'thunder': importFolder('projeto4-RPG\\ZeldaStyleRPG\\graphics\\levelGraphics\\particles\\thunder'),

            # morte dos monstros
            'squid': importFolder('projeto4-RPG\\ZeldaStyleRPG\\graphics\\levelGraphics\\particles\\smoke_orange'),
            'raccoon': importFolder('projeto4-RPG\\ZeldaStyleRPG\\graphics\\levelGraphics\\particles\\raccoon'),
            'spirit': importFolder('projeto4-RPG\\ZeldaStyleRPG\\graphics\\levelGraphics\\particles\\nova'),
            'bamboo': importFolder('projeto4-RPG\\ZeldaStyleRPG\\graphics\\levelGraphics\\particles\\bamboo'),

            # folhas
            'leaf': (
                importFolder('projeto4-RPG\\ZeldaStyleRPG\\graphics\\levelGraphics\\particles\\leaf1'),
                importFolder('projeto4-RPG\\ZeldaStyleRPG\\graphics\\levelGraphics\\particles\\leaf2'),
                importFolder('projeto4-RPG\\ZeldaStyleRPG\\graphics\\levelGraphics\\particles\\leaf3'),
                importFolder('projeto4-RPG\\ZeldaStyleRPG\\graphics\\levelGraphics\\particles\\leaf4'),
                importFolder('projeto4-RPG\\ZeldaStyleRPG\\graphics\\levelGraphics\\particles\\leaf5'),
                importFolder('projeto4-RPG\\ZeldaStyleRPG\\graphics\\levelGraphics\\particles\\leaf6'),
                self.reflectImages(importFolder('projeto4-RPG\\ZeldaStyleRPG\\graphics\\levelGraphics\\particles\\leaf1')),
                self.reflectImages(importFolder('projeto4-RPG\\ZeldaStyleRPG\\graphics\\levelGraphics\\particles\\leaf2')),
                self.reflectImages(importFolder('projeto4-RPG\\ZeldaStyleRPG\\graphics\\levelGraphics\\particles\\leaf3')),
                self.reflectImages(importFolder('projeto4-RPG\\ZeldaStyleRPG\\graphics\\levelGraphics\\particles\\leaf4')),
                self.reflectImages(importFolder('projeto4-RPG\\ZeldaStyleRPG\\graphics\\levelGraphics\\particles\\leaf5')),
                self.reflectImages(importFolder('projeto4-RPG\\ZeldaStyleRPG\\graphics\\levelGraphics\\particles\\leaf6')),
            )

        }

    def reflectImages(self, frames):
        newFrames = []
        
        for frame in frames:

            flippedFrame = pygame.transform.flip(frame, True, False)

            newFrames.append(flippedFrame)

        return newFrames
    
    def createGrassParticles(self, pos, groups):
        animationFrames = choice(self.frames['leaf'])
        ParticleEffect(pos, animationFrames, groups)

    def createParticles(self, animationType, pos, groups):
        animationFrames = self.frames[animationType]
        ParticleEffect(pos, animationFrames, groups)


class ParticleEffect(pygame.sprite.Sprite):
    def __init__(self, pos, animationFrames, groups):
        super().__init__(groups)
        self.frameIndex = 0
        self.animationSpeed = 0.15
        self.frames = animationFrames
        self.image = self.frames[self.frameIndex]
        self.rect = self.image.get_rect(center = pos)


    def animate(self):
        self.frameIndex += self.animationSpeed

        if self.frameIndex >= len(self.frames):
            self.kill()

        else:
            self.image = self.frames[int(self.frameIndex)]

    def update(self):
        self.animate()