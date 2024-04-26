import pygame
from paramètre import *
from aide import *
from tile import Tile
from joueur import Joueur
from affichage import debug

class Niveau_1:
    def __init__(self,game):
        self.display = pygame.display.get_surface()

        self.sprite_visible = GroupesCamera()
        self.obstacles = pygame.sprite.Group()
        self.objets = pygame.sprite.Group()
        self.tout = pygame.sprite.Group()
        self.game = game

        self.créer_carte()

        

    def get_tout(self):
        self.tout.add(self.sprite_visible.fond_rect)
        for sprite in self.objets.sprites() + self.sprite_visible.sprites() + self.obstacles.sprites():
            if not self.tout.has(sprite):
                print(sprite,"aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa")
                self.tout.add(sprite)
        print(self.tout.sprites)


    def créer_carte(self):

        calques = {
            'barrière' : lire_csv("../carte/niveau_1/Carte_barrière.csv"),
            'joueur' : lire_csv("../carte/niveau_1/Carte_joueur.csv"),
            'clone' : lire_csv("../carte/niveau_1/Carte_clone.csv"),
            'clé'  : lire_csv("../carte/niveau_1/Carte_clé.csv"),
            'sortie' : lire_csv("../carte/niveau_1/Carte_sortie.csv"),
            'porte' : lire_csv("../carte/niveau_1/Carte_porte.csv")
        }

        for type,calque in calques.items():
            for l_indice,ligne in enumerate(calque):
                for c_indice, col in enumerate(ligne):
                    if col != '-1':
                        x = c_indice * TILESIZE
                        y = l_indice * TILESIZE

                        if type == 'barrière' :
                            Tile((x,y),[self.obstacles,self.sprite_visible,self.tout],'invisible')
                        elif type == 'joueur':
                            self.joueur = Joueur ( (x,y),[self.sprite_visible],self.obstacles,self.objets,True,self.game,self)
                        elif type == 'clone' :
                            self.clone = Joueur ( (x,y),[self.sprite_visible],self.obstacles,self.objets,False,self.game,self)
                        elif type == 'clé' :
                            Tile((x,y),[self.objets],'clé')
                        elif type == 'sortie':
                            Tile((x,y),[self.objets],'sortie')
                        elif type == 'porte':
                            Tile((x,y),[self.objets,self.obstacles],'porte')

        

        # création caméra
        self.camera =  self.joueur.rect.inflate(150,150)
        self.camera.center = self.joueur.rect.center

        # créarion cadre
        haut = self.display.get_clip()
        haut.bottom = haut.top
        haut.inflate_ip(0,5)

        bas = self.display.get_clip()
        bas.top = bas.bottom
        bas.inflate_ip(0,5)

        gauche = self.display.get_clip()
        gauche.right = gauche.left
        gauche.inflate_ip(5,0)

        droite = self.display.get_clip()
        droite.left = droite.right
        droite.inflate_ip(5,0)

        self.cadre = [haut,bas,droite,gauche]

        self.get_tout()
    


    def interaction_objet(self):
        for i in self.cadre:
            pygame.draw.rect(self.display,'green',i)
        pygame.draw.rect(self.display,'blue',self.camera,1)
        for sprite in self.objets.sprites() :
            if sprite.type == 'clé':
                if sprite.hitbox.colliderect(self.joueur.hitbox) :
                    debug("press E",self.joueur.hitbox.x+80,self.joueur.hitbox.y-20)
                    if self.joueur.interaction:
                        self.joueur.inventaire.append('clé')
                        self.objets.remove(sprite)

            if sprite.type == 'porte':
                if sprite.hitbox.colliderect(self.joueur.hitbox.move(self.joueur.direction)):
                    if 'clé' in self.joueur.inventaire and self.joueur.interaction:
                        self.obstacles.remove(sprite)

            if sprite.type == 'sortie':
                if self.joueur.hitbox.colliderect(sprite.hitbox) and self.clone.hitbox.colliderect(sprite.hitbox):
                    self.game.niveau_en_cours = 1





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
        self.fond_surface = pygame.image.load('../graphics/Carte.png').convert()
        self.fond_rect = self.fond_surface.get_rect(topleft = (0,0))



    def custom_draw(self,joueur):

        '''
        # getting the offset 
        self.offset.x = joueur.rect.centerx - self.demi_width
        self.offset.y = joueur.rect.centery - self.demi_height

		# drawing the floor
        floor_offset_pos = self.fond_rect.topleft - self.offset
        self.display.blit(self.fond_surface,floor_offset_pos)

		# for sprite in self.sprites():
        for sprite in sorted(self.sprites(),key = lambda sprite: sprite.rect.centery):
            offset_pos = sprite.rect.topleft - self.offset
            self.display.blit(sprite.image,offset_pos)
        '''
        


        
        self.display.blit(self.fond_surface,self.fond_rect)

        for sprite in sorted(self.sprites(),key = lambda sprite : sprite.rect.centery):
            self.display.blit(sprite.image,sprite.rect)
            pygame.draw.rect(self.display,'red',sprite.rect,1)
        
