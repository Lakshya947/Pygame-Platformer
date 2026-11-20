import pygame
pygame.init()

from settings import *

class FloatingPlatform(pygame.sprite.Sprite):
    def __init__(self,x,y,distance):
        super().__init__()
        self.x = x
        self.y = y
        self.distance = distance
        self.start_x = x
        self.speed = 1#ajustable speed
        self.end_x = x + self.distance 
        self.image = pygame.image.load("assets/boat.png")
        self.rect = self.image.get_rect(topleft=(x, y))
        self.direction = 1
        self.mask = pygame.mask.from_surface(self.image)

        
    def update(self, scroll):
        self.x += self.direction * self.speed
        if self.x <= self.start_x or self.x >= self.end_x:
            # if the platform has completed its journey to one side it changes direction
            self.direction *= -1
         
        self.rect.x = self.x - scroll
        self.rect.y = self.y


    def draw(self, scroll,screen):
        flipped_image = pygame.transform.flip(self.image, self.direction==-1, False)
        screen.blit(flipped_image, (self.x - scroll, self.y))


