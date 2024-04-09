import pygame,sys
from paramètre import *
from niveau import *


class Game:
    def __init__(self):

        # paramètre genérale
        pygame.init()
        self.ecran=pygame.display.set_mode((WIDTH,HEIGTH))
        pygame.display.set_caption("Nom à trouver")
        self.clock = pygame.time.Clock()

        self.niveau=Niveau()
    
    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()
            
            self.ecran.fill('black')
            self.niveau.run()
            pygame.display.update()
            self.clock.tick(FPS)
    
if __name__ == '__main__':
     game = Game()
     game.run()