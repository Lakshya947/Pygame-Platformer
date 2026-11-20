import pygame
pygame.init()


class Button():
    def __init__(self,x,y,image):
        self.x = x
        self.y = y
    
        self.image = image
        
        self.rect = self.image.get_rect(topleft=(x, y))
        self.clicked = False

    def draw(self,screen):
        screen.blit(self.image, (self.x, self.y))
          

        