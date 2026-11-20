import pygame
from settings import *

class flag(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.x = x
        self.y = y
        self.image = pygame.image.load("assets/flag.png")
        self.image = pygame.transform.scale(self.image, (tile_size, tile_size))
        self.rect = self.image.get_rect(topleft=(x, y))

        self.rect.x = self.x 
        self.rect.y = self.y
 

    def draw(self, scroll):
        
        self.rect.x = self.x - scroll
        screen.blit(self.image, (self.rect.x, self.rect.y))
         