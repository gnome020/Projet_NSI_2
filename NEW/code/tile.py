import pygame
from paramètre import *

class Tile(pygame.sprite.Sprite):
    def __init__(self,pos,groupes,type,surface = pygame.Surface((TILESIZE,TILESIZE))):
        super().__init__(groupes)
        self.type = type
        self.image = surface
        if type  == 'objet':
            self.rect = self.image.get_rect(topleft = pos)
        else:
            self.rect = self.image.get_rect(topleft = pos)
        self.hitbox = self.rect.inflate(0,-5)

