import pygame, sys
from settings import *
from model.level import Level

class Game:
    def __init__(self):
        # inicia o jogo
        pygame.init()

        #configuracoes de tela e FPS
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Heloísa's Quest: Ecos of Bolo Fofos")
        self.clock = pygame.time.Clock()

        self.level = Level()
        
        # musica !
        self.mainSound = pygame.mixer.Sound(r"projeto4-RPG\ZeldaStyleRPG\audio\main.ogg")
        self.mainSound.play(loops= -1)
        self.mainSound.set_volume(0.7)


    def run(self):
        while True:
            #captura eventos 
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_m:
                        self.level.toggleMenu()

            #atualiza a tela
            self.screen.fill('black')
            self.clock.tick(fps)

            #inicializa o level
            self.level.run()
            pygame.display.update()

            if self.level.player.health <= 0:
                break

        self.screen.fill('black')
        pygame.display.update()

                

                
                
            


if __name__ == '__main__':
    game = Game()
    game.run()

        