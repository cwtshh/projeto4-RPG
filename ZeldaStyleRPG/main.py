import pygame, sys
from settings import *
from model.level import Level

class Game:
    def __init__(self):
        # inicia o jogo
        pygame.init()

        #configuracoes de tela e FPS
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption('RPG zelda')
        self.clock = pygame.time.Clock()

        self.level = Level()

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


if __name__ == '__main__':
    game = Game()
    game.run()
        