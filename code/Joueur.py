import pygame
from paramètre import *
from affichage import *

class Joueur(pygame.sprite.Sprite):
    def __init__(self,game, pos,groupes,obstacles,objets):
        super().__init__(groupes)

        self.image = pygame.image.load("../graphics/link.png").convert_alpha()
        self.image = pygame.transform.scale(self.image,(62,62))
        self.rect = self.image.get_rect(topleft = pos)
        self.hitbox = self.rect.inflate(0,-5)
        self.camera = self.rect.inflate(10,10)
        self.interaction = False
        self.objets = objets
        self.game = game

        self.direction = pygame.math.Vector2()
        self.vitesse = 5

        self.obstacles = obstacles

    def input(self):
        key = pygame.key.get_pressed()

        if key[pygame.K_z]:
            self.direction.y = -1
        elif key[pygame.K_s]:
            self.direction.y = 1
        else:
            self.direction.y = 0

        if key[pygame.K_d]:
            self.direction.x = 1
        elif key[pygame.K_q]:
            self.direction.x = -1
        else:
            self.direction.x = 0
        if key[pygame.K_e]:
            self.interaction = True
        else:
            self.interaction = False

    def move(self,vitesse):
        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize()

        self.interaction_objet()
        self.hitbox.x += self.direction.x * vitesse
        self.colisions('horizontale')
        self.hitbox.y += self.direction.y * vitesse
        self.colisions('verticale')
        self.rect.center = self.hitbox.center
    
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
    def interaction_objet(self):
        for sprite in self.objets :
            if sprite.type == 'portal':
                if sprite.hitbox.colliderect(self.hitbox.move(self.direction)) :
                    debug("press E",self.hitbox.x+80,self.hitbox.y-20)
                    if self.interaction:
                        self.game.niveau_en_cours = 1

    def update(self):
        self.input()
        self.move(self.vitesse)