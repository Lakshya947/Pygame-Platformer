import pygame
from settings import *

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, direction,image,scale):
        super().__init__()
        self.image = image#image
        self.scale = scale#scale
        self.rect = self.image.get_rect(center=(x, y))#gets the dimesnions of the image
        self.image = pygame.transform.scale(self.image, (int(self.image.get_width() * scale), int(self.image.get_height() * scale)))#scales the image
        self.speed = 10#speed of the bullet
        self.direction = direction#direction the bullet is going
        self.mask = pygame.mask.from_surface(self.image)# pixel perfect c0ollions, stores the image exluding the transparent parts
        
    def update(self):
        self.rect.x += self.speed * self.direction#bullet goes in the direction it is shot in

        if self.rect.right < 0 or self.rect.left > WIDTH:
            self.kill()#bullet is killed when it goes off the screen

 
            

    def draw(self, screen):
        self.image = pygame.transform.flip(self.image, self.direction==-1, False)
        screen.blit(self.image, (self.rect.x, self.rect.y))#blits the screen
