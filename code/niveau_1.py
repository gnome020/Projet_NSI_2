import pygame
from paramètre import *
from aide import *
from tile import Tile
from joueur import Joueur
from affichage import debug
from math import gcd
from time import sleep

class Niveau_1:
    def __init__(self,game):
        self.display = pygame.display.get_surface()

        # ARRANGEMENT ELEMENTS
        self.sprite_visible = GroupesCamera()
        self.obstacles = pygame.sprite.Group()
        self.objets = pygame.sprite.Group()
        self.tout = []
        self.current_joueur = []
        self.game = game

        self.creer_carte()

        

    def get_tout(self):
        #self.tout.append(self.sprite_visible.fond_rect)
        #self.tout.append(self.clone)
        for sprite in self.objets.sprites() + self.obstacles.sprites():
            if sprite not in self.tout:
                self.tout.append(sprite)


    def centrage(self):
        xA, yA = self.camera.centerx , self.camera.centery
        xB,yB = self.display.get_clip().centerx ,self.display.get_clip().centery
        vecteur = pygame.math.Vector2()
        vecteur.x = (xB - xA)
        vecteur.y = (yB - yA)

        self.sprite_visible.fond_rect.x += vecteur.x
        self.sprite_visible.fond_rect.y += vecteur.y
        for sprite in self.tout:
            sprite.hitbox.x += vecteur.x
            sprite.hitbox.y += vecteur.y
        self.current_joueur[1].hitbox.x  += vecteur.x
        self.current_joueur[1].hitbox.y  += vecteur.y
        self.current_joueur[0].hitbox.x  += vecteur.x
        self.current_joueur[0].hitbox.y  += vecteur.y
        
        check = self.joueur.check_sortie_cadre(self.sprite_visible.fond_rect) # voir la methode dans joueur
        print(check)
        liste_vecteur = []
        compte = 0
        if not check[0]:
            for side in check[1:]:

                if side == 'top':
                    yA,yB = 0 , self.sprite_visible.fond_rect.top
                    vecteur =pygame.math.Vector2()
                    vecteur.x = (0)
                    vecteur.y = (yB - yA)
                    liste_vecteur.append(vecteur)
                    compte += 1

                elif side == 'bottom':
                    yA,yB = HEIGTH , self.sprite_visible.fond_rect.bottom
                    vecteur =pygame.math.Vector2()
                    vecteur.x = (0)
                    vecteur.y = (yB - yA)
                    liste_vecteur.append(vecteur)
                    compte += 1
                elif side == 'left':
                    xA,xB =  0 , self.sprite_visible.fond_rect.left
                    vecteur =pygame.math.Vector2()
                    vecteur.x = (xB - xA)
                    vecteur.y = (0)
                    liste_vecteur.append(vecteur)
                    compte += 1
                
                elif side == 'right':
                    xA,xB = WIDTH  , self.sprite_visible.fond_rect.right
                    vecteur =pygame.math.Vector2()
                    vecteur.x = (xB - xA)
                    vecteur.y = (0)
                    liste_vecteur.append(vecteur)
                    compte += 1

            vecteur = liste_vecteur[0]
            if compte > 1:
                vecteur += liste_vecteur[1]

            self.sprite_visible.fond_rect.x -= vecteur.x
            self.sprite_visible.fond_rect.y -= vecteur.y
            for sprite in self.tout:
                sprite.hitbox.x -= vecteur.x
                sprite.hitbox.y -= vecteur.y
            self.current_joueur[1].hitbox.x  -= vecteur.x
            self.current_joueur[1].hitbox.y  -= vecteur.y
            self.current_joueur[0].hitbox.x  -= vecteur.x
            self.current_joueur[0].hitbox.y  -= vecteur.y

                









             
            
        
    def creer_carte(self):

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
                            Tile((x,y),[self.obstacles],'invisible')
                        elif type == 'joueur':
                            self.joueur = Joueur ( (x,y),[self.sprite_visible],self.obstacles,self.objets,True,self.game,self)
                            self.current_joueur.append(self.joueur)
                        elif type == 'clone' :
                            self.clone = Joueur ( (x,y),[self.sprite_visible],self.obstacles,self.objets,False,self.game,self)
                            self.current_joueur.append(self.clone)
                        elif type == 'clé' :
                            Tile((x,y),[self.objets],'clé')
                        elif type == 'sortie':
                            Tile((x,y),[self.objets],'sortie')
                        elif type == 'porte':
                            Tile((x,y),[self.objets,self.obstacles],'porte')

        

        # création caméra
        self.camera =  self.joueur.rect.inflate(500,500)
        self.camera.center = self.joueur.rect.center

        # créarion cadre
        haut = self.display.get_clip()
        haut.bottom = haut.top
        haut.inflate_ip(0,1)

        bas = self.display.get_clip()
        bas.top = bas.bottom
        bas.inflate_ip(0,1)

        gauche = self.display.get_clip()
        gauche.right = gauche.left
        gauche.inflate_ip(1,0)

        droite = self.display.get_clip()
        droite.left = droite.right
        droite.inflate_ip(1,0)

        self.cadre = {'haut': haut,'bas':bas,'gauche':gauche,'droite':droite}
        self.get_tout()
    
        self.centrage()

    def interaction_objet(self):

        for sprite in self.objets.sprites() :
            if sprite.type == 'clé':
                if sprite.hitbox.colliderect(self.current_joueur[0].hitbox) :
                    debug("press E",self.current_joueur[0].hitbox.x+80,self.current_joueur[0].hitbox.y-20)
                    if self.current_joueur[0].interaction:
                        self.current_joueur[0].inventaire.append('clé')
                        self.objets.remove(sprite)

            if sprite.type == 'porte':
                if sprite.hitbox.colliderect(self.current_joueur[0].hitbox.move(self.current_joueur[0].direction)):
                    if 'clé' in self.current_joueur[0].inventaire and self.current_joueur[0].interaction:
                        self.obstacles.remove(sprite)

            if sprite.type == 'sortie':
                if self.current_joueur[0].hitbox.colliderect(sprite.hitbox) :
                    debug("True actif")
                    if self.current_joueur[1].hitbox.colliderect(sprite.hitbox):
                        debug("True passif",10,30)
                        self.game.niveau_en_cours = 1





    def run(self):
		# update and draw the game
        self.sprite_visible.custom_draw(self.current_joueur[0])
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
