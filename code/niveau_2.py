import pygame
from paramètre import *
from aide import *
from tile import Tile
from joueur import Joueur

class Niveau_2:
    def __init__(self,game):
        self.display = pygame.display.get_surface()

        self.sprite_visible = GroupesCamera()
        self.obstacles = pygame.sprite.Group()
        self.objets = pygame.sprite.Group()
        self.game = game



        self.créer_carte()

    def créer_carte(self):

        calques = {
            'bordure' : lire_csv("../carte/niveau_2/Carte_barrière.csv"),
            'joueur'  : lire_csv("../carte/niveau_2/Carte_joueur.csv")
        }

        for type,calque in calques.items():
            for l_indice,ligne in enumerate(calque):
                for c_indice, col in enumerate(ligne):
                    if col != '-1':
                        x = c_indice * TILESIZE
                        y = l_indice * TILESIZE

                        if type == 'bordure' :
                            Tile((x,y),[self.obstacles],'invisible')
                        elif type == 'joueur' :
                            self.joueur = Joueur (self.game, (x,y),[self.sprite_visible],self.obstacles,self.objets)


        

    def run(self):
		# update and draw the game
        self.sprite_visible.custom_draw(self.joueur)
        self.sprite_visible.update()

class GroupesCamera(pygame.sprite.Group):
    def __init__(self):

        super().__init__()

        self.display = pygame.display.get_surface()
        self.demi_width = self.display.get_size()[0] // 2
        self.demi_height = self.display.get_size()[1] // 2
        self.offset = pygame.math.Vector2()

        # création du fond
        self.fond_surface = pygame.image.load('../graphics/Carte_2.png').convert()
        self.fond_rect = self.fond_surface.get_rect(topleft = (0,0))

    def custom_draw(self,joueur):

        '''
        # recup offset
        self.offset.x = joueur.rect.centerx - self.demi_width
        self.offset.y = joueur.rect.centery - self.demi_height

        # dessin du fond
        sol_pos_offeset = self.fond_rect.topleft - self.offset
        self.display.blit(self.fond_surface,sol_pos_offeset)


        for sprite in sorted(self.sprites(), key = lambda sprite : sprite.rect.centery):
            offset_pos = sprite.rect.topleft - self.offset
            self.display.blit(sprite.image,offset_pos)
            pygame.draw.rect(self.display,'red',sprite.hitbox,1)
        '''


        self.display.blit(self.fond_surface,self.fond_rect)

        for sprite in sorted(self.sprites(),key = lambda sprite : sprite.rect.centery):
            self.display.blit(sprite.image,sprite.rect)
            pygame.draw.rect(self.display,'red',sprite.hitbox,1)

