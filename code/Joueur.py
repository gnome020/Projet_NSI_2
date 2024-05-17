import pygame
import pygame.display
from paramètre import *
from affichage import *
from aide import *
from random import choice
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
        
        self.switching_a = False
        self.switching_tab = False
        self.cd = 500
        self.temp_statut = []
        self.temp_image = []

        self.inventaire = []

    def import_player_assets(self):
        chemin_perso = '../graphics/joueur/'
        self.animations = {'haut': [],'bas': [],'gauche': [],'droite': []
                           ,'haut_idle' : [] , 'bas_idle' : [], 'gauche_idle' : [],
                            'droite_idle' : [], 'stop': []}

        for animation in self.animations.keys():
            chemin_complet = chemin_perso + animation
            self.animations[animation] = import_folder(chemin_complet)

    def recup_status(self):

		# idle status
        if self.direction.x == 0 and self.direction.y == 0:
            if 'stop' in self.image_statut:
                pass
            elif not 'idle' in self.image_statut:
                self.image_statut = self.image_statut + '_idle'


    def input(self):
        key = pygame.key.get_pressed()
        if self.statut:
            if self.temp_image != []: # un fois au changement de personnage
                if not self.switching_tab:
                    self.niveau.current_joueur.reverse()
                    self.niveau.camera.center = self.niveau.current_joueur[0].hitbox.center
                    self.niveau.centrage()
                self.image_statut= self.temp_image[0]
                self.temp_image = []

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

        else:   
            self.direction *= 0
            self.temp_image.append(self.image_statut)
            self.temp_image = self.temp_image[:1]
            self.image_statut='stop'

            
        if key[pygame.K_a]:
            if not self.switching_a:
                self.switching_a = True
                self.switch_time = pygame.time.get_ticks()
                self.statut = not self.statut
                
        if key[pygame.K_TAB]:
            self.temp_statut.append(self.statut)
            self.temp_statut = self.temp_statut[:1]
            self.statut = True
            self.switching_tab = True
        else:
            if self.switching_tab:
                self.switching_tab = False
                self.statut=self.temp_statut[0]
                self.temp_statut = []



    
    def cooldown(self):
        if self.switching_a:
            current_time = pygame.time.get_ticks()
            if current_time - self.switch_time >= self.cd:
                self.switching_a = False


    def main_move(self,vitesse):
        if self.direction.magnitude() != 0:
                self.direction = self.direction.normalize()

        self.hitbox.x += self.direction.x * vitesse
        self.colisions('horizontale')
        self.hitbox.y += self.direction.y * vitesse
        self.colisions('verticale')
        self.rect.center = self.hitbox.center

        if self.statut:
            self.niveau.camera.center = self.hitbox.center

    def alt_move(self,vitesse):
        if self.direction.magnitude() != 0:
                    self.direction = self.direction.normalize()
        

        for sprite in self.niveau.tout:
            sprite.hitbox.x -= self.direction.x * vitesse
            self.colisions('horizontale','alt')
            sprite.hitbox.y -= self.direction.y * vitesse
            self.colisions('verticale','alt')
        self.niveau.sprite_visible.fond_rect.x -= self.direction.x * vitesse
        self.niveau.sprite_visible.fond_rect.y -= self.direction.y * vitesse
        self.niveau.current_joueur[1].hitbox.x  -= self.direction.x * vitesse
        self.niveau.current_joueur[1].hitbox.y  -= self.direction.y * vitesse
        if self.statut:
            self.niveau.camera.center = self.hitbox.center

            
    def camera_check(self):
        if self.niveau.camera.collidelist(list(self.niveau.cadre.values())) != -1:
             pass # CONTINUER ICI
        if self.niveau.camera.move(self.direction*10).collidelist(list(self.niveau.cadre.values())) != -1:
            return True
        return False
    
    
    def check_sortie_cadre(self,rect):
         L = [False]
         if rect.top >= 0:
              L.append('top')
         if rect.bottom <= HEIGTH :
              L.append('bottom')
         if rect.left  >= 0 :
              L.append('left')
         if rect.right <= WIDTH:
              L.append('right')
         if L != [False]:
              return L
         return [True]

        


    
    def colisions(self,direction,type = 'main'):
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
                            

                



    
    def animer(self):
            animation = self.animations[self.image_statut]
            
            self.indice_animation += self.vitesse_animation
            if self.indice_animation >= len(animation):
                self.indice_animation = 0

            self.image = animation[int(self.indice_animation)]
            self.image = pygame.transform.scale(self.image,(62,62))
            self.rect = self.image.get_rect(center = self.hitbox.center)
                



    def update(self):
        pygame.draw.rect(self.display,'blue',self.niveau.camera,1)
        self.niveau.interaction_objet()
        self.input()
        self.cooldown()
        self.recup_status()
        self.animer()
        debug((self.camera_check(), self.check_sortie_cadre(self.niveau.sprite_visible.fond_rect.move(-self.direction * self.vitesse))[0]))
        if self.camera_check() and not self.check_sortie_cadre(self.niveau.sprite_visible.fond_rect.move(-self.direction * self.vitesse))[0]:
            self.alt_move(self.vitesse)
        else:
            self.main_move(self.vitesse)
        