import pygame
import pygame.display
from paramètre import *
from affichage import *
from aide import *
class Joueur(pygame.sprite.Sprite):
    def __init__(self, pos,groupes,obstacles,objets,statut,game,niveau):
        super().__init__(groupes)

        ### Image
        self.import_player_assets()
        self.image_statut = 'bas'
        self.vitesse_animation = 0.05
        self.indice_animation = 0
        self.image = pygame.image.load("../graphics/joueur/bas/1.png").convert_alpha()
        self.image = pygame.transform.scale(self.image,(62,62))
        self.display = pygame.display.get_surface()

        self.rect = self.image.get_rect(topleft = pos)
        self.hitbox = self.rect.inflate(-12,-18)
        self.objets = objets
        self.game = game
        self.niveau = niveau
        self.statut = statut
        self.obstacles = obstacles

        self.direction = pygame.math.Vector2()
        self.vitesse = 5
        self.interaction = False
        
        self.inventaire = []

    def import_player_assets(self):
        chemin_perso = '../graphics/joueur/'
        self.animations = {'haut': [],'bas': [],'gauche': [],'droite': []
                           ,'haut_idle' : [] , 'bas_idle' : [], 'gauche_idle' : [],
                            'droite_idle' : []}

        for animation in self.animations.keys():
            chemin_complet = chemin_perso + animation
            self.animations[animation] = import_folder(chemin_complet)

    def recup_status(self):

		# idle status
        if self.direction.x == 0 and self.direction.y == 0:
            if not 'idle' in self.image_statut:
                self.image_statut = self.image_statut + '_idle'


    def input(self):
        key = pygame.key.get_pressed()
        if self.statut == True:

            ## Mouvement

            if key[pygame.K_z]:
                self.direction.y = -1
                self.image_statut = 'haut'
            elif key[pygame.K_s]:
                self.direction.y = 1
                self.image_statut = 'bas'
            else:
                self.direction.y = 0


            if key[pygame.K_d]:
                self.direction.x = 1
                self.image_statut = 'droite'
            elif key[pygame.K_q]:
                self.direction.x = -1
                self.image_statut = 'gauche'
            else:
                self.direction.x = 0




            if key[pygame.K_e]:
                self.interaction = True
            else:
                self.interaction = False

            if key[pygame.K_SPACE]:
                self.dupli = True
            else:
                self.dupli = False
            
        if key[pygame.K_a]:
            self.statut = not self.statut

    


    def move(self,vitesse):
        if self.statut :
            if self.niveau.camera.move(self.direction).collidelist(self.niveau.cadre) == -1:
                
                if self.direction.magnitude() != 0:
                    self.direction = self.direction.normalize()
                self.niveau.camera.center = self.hitbox.center

                self.hitbox.x += self.direction.x * vitesse
                self.colisions('horizontale')
                self.hitbox.y += self.direction.y * vitesse
                self.colisions('verticale')
                self.rect.center = self.hitbox.center
            
            else:
                pass


    def animer(self):
        if self.statut:
            animation = self.animations[self.image_statut]
            
            self.indice_animation += self.vitesse_animation
            if self.indice_animation >= len(animation):
                self.indice_animation = 0

            self.image = animation[int(self.indice_animation)]
            self.image = pygame.transform.scale(self.image,(62,62))
            self.rect = self.image.get_rect(center = self.hitbox.center)
    
    def colisions(self,direction):
        if direction == 'horizontale':
            for sprite in self.obstacles:
                    if sprite.hitbox.colliderect(self.hitbox):
                        if self.direction.x > 0 : # vers la droite
                            self.hitbox.right = sprite.hitbox.left
                        elif self.direction.x < 0 : # vers la gauche
                            self.hitbox.left = sprite.hitbox.right
                

        elif direction == 'verticale':
            for sprite in self.obstacles:
                    if sprite.hitbox.colliderect(self.hitbox):
                        if self.direction.y > 0 : # vers le bas
                            self.hitbox.bottom = sprite.hitbox.top
                        elif self.direction.y < 0 : # vers le haut
                            self.hitbox.top = sprite.hitbox.bottom

    
                



    def update(self):
        self.niveau.interaction_objet()
        self.input()
        self.recup_status()
        self.animer()
        self.move(self.vitesse)