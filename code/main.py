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
        self.ecran = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Lost Soul")
        self.clock = pygame.time.Clock()
        self.niveau_en_cours = 0
        self.niveau = [Niveau_1(self), Niveau_2(self)]

        # Initialisation des boutons
        self.resume_button, self.exit_button = init_buttons()

        # Initialisation de l'état du menu
        self.show_menu = False
        self.show_opening = True
        self.accueil_img = pygame.image.load("../graphics/accueil.png").convert_alpha()
        self.accueil_img = pygame.transform.scale(self.accueil_img, (1300, 720))
    
    def afficher_accueil(self):
        self.ecran.blit(self.accueil_img, (0, 0))
        pygame.display.update()



    def run(self):
        affichage = True
        while affichage:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.show_menu = not self.show_menu  # Basculer l'état du menu
                    elif event.key == pygame.K_p:  # Pour quitter le jeu avec la touche P
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

            if self.show_opening:
                self.afficher_accueil()
                pygame.display.update()
                pygame.time.delay(100)  # Ajout d'une pause de 100 millisecondes

                for event in pygame.event.get():  # Attente de la touche 'Entrée'
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN: 
                        self.show_opening = False

            if not self.show_opening:
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