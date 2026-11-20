import pygame

class bar:
    def __init__(self,x,y,w,h,colour1,colour2):
        super().__init__()

        self.x = x#x spawn coordinate
        self.y = y#y spawn coordinate
        self.w = w#width
        self.h = h#height
        self.colour1 = colour1#background
        self.colour2 = colour2#foreground

    def draw(self,attribute1,attribute2,screen):
        
        pygame.draw.rect(screen, self.colour1, (self.x, self.y, self.w, self.h))#draws the border
        pygame.draw.rect(screen, self.colour2, (self.x, self.y, self.w * attribute1 / attribute2, self.h))#draws the background
        pygame.draw.rect(screen, (0, 0, 0), (self.x, self.y, self.w, self.h), 2)#draws the bar


