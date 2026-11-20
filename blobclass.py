import pygame
pygame.init()
from settings import *

class blob(pygame.sprite.Sprite):
    def __init__(self,x,y):
        super().__init__()

        self.x = x#X spawn coordinate
        self.y = y#Y spawn coordinate
        self.animation = []
        self.image = pygame.image.load("assets/blob/blob.png")
        self.rect = self.image.get_rect()#gets the dimensions of the image
        self.rect.center = (x,y)
        self.update_time = pygame.time.get_ticks()
        self.direction = 1    
        self.speed = 2
        self.start_x = x
        self.end_x = x + tile_size * 3
        self.health = 5
    def update(self, scroll):
        self.x += self.direction * self.speed#simple patrolling logic, moves 40 pixels to the left then right
        if self.x <= self.start_x or self.x >= self.end_x:
            self.direction *= -1#changes the direction 

        if pygame.sprite.spritecollide(self, bullet_group, True, pygame.sprite.collide_mask):
            self.health -= 1         
        self.rect.x = self.x - scroll
        self.rect.y = self.y+18
    def draw(self,screen):

        screen.blit(self.image,(self.rect.x,self.rect.y))

