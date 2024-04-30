import pygame
import sys
from menu import init_buttons
from paramètre import *
from niveau_1 import Niveau_1
from niveau_2 import Niveau_2

pygame.init()

class Game:
    def __init__(self):
        # paramètres généraux
        self.ecran = pygame.display.set_mode((WIDTH, HEIGTH))
        pygame.display.set_caption("Lost Soul")
        self.clock = pygame.time.Clock()
        self.niveau_en_cours = 0
        self.niveau = [Niveau_1(self), Niveau_2(self)]

        # Initialisation des boutons
        self.resume_button, self.exit_button = init_buttons()

        # Initialisation de l'état du menu
        self.show_menu = False

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.show_menu = not self.show_menu  # Basculer l'état du menu
                    elif event.key == pygame.K_p:  # Pour quitter le jeu avec la touche Q
                        pygame.quit()
                        sys.exit()
                elif event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN and self.show_menu:
                    if self.resume_button.rect.collidepoint(pygame.mouse.get_pos()):
                        self.show_menu = False
                    elif self.exit_button.rect.collidepoint(pygame.mouse.get_pos()):
                        pygame.quit()
                        sys.exit()

            self.ecran.fill('black')

            if self.show_menu:
                # Dessiner le menu ici
                self.resume_button.draw(self.ecran)
                self.exit_button.draw(self.ecran)
            else:
                self.niveau[self.niveau_en_cours].run()

            pygame.display.update()
            self.clock.tick(FPS)

if __name__ == '__main__':
    game = Game()
    game.run()