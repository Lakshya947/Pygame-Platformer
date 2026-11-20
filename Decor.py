
import pygame
pygame.init()
import os

class decorClass(pygame.sprite.Sprite):
    def __init__(self,x,y,decortype,cooldown):
        super().__init__()
        self.x = x
        self.y = y
        self.cooldown = cooldown
        self.frame_index = 0#what image is 
        self.animation = []
        for i in range(len(os.listdir(f"assets/decor/{decortype}"))):#loads all the the images in a given file
            img = pygame.image.load(f"assets/decor/{decortype}/{i}.png")#image thats selected
            self.animation.append(img)#appends the image to the animation list
        self.image = self.animation[self.frame_index]#image
        self.rect = self.image.get_rect()
        self.rect.center = (x,y)
        self.update_time = pygame.time.get_ticks()#defines a pygame clock
            
        
    def update_animation(self,scroll):
      
        self.image = self.animation[self.frame_index]#changes the image to the current one in the 
        if pygame.time.get_ticks() - self.update_time > self.cooldown:
            self.update_time = pygame.time.get_ticks()
            self.frame_index += 1#adds one 
            
        if self.frame_index >= len(self.animation):# if the current frame is more than the length of all the grames
            self.frame_index = 0

        self.rect.x = self.x - scroll
    def draw(self,screen,):
        screen.blit(self.image,(self.rect.x,self.rect.y-10))



