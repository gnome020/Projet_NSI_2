import pygame,sys

from paramètre import *
from niveau_1 import Niveau_1
from niveau_2 import Niveau_2
from affichage import debug
pygame.init()

class Game:
    def __init__(self):

        # paramètre genérale
        pygame.init()
        self.ecran=pygame.display.set_mode((WIDTH,HEIGTH))
        pygame.display.set_caption("Lost soul")
        self.clock = pygame.time.Clock()
        self.niveau_en_cours = 0

        self.niveau = [Niveau_1(self),  Niveau_2(self)]


    def run(self):
        while True:
            
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()
            self.ecran.fill('black')
            self.niveau[self.niveau_en_cours].run()
            pygame.display.update()
            self.clock.tick(FPS)
    
if __name__ == '__main__':
    game = Game()
    game.run()