import pygame
pygame.init()
from settings import *
import os


class Saw(pygame.sprite.Sprite):
    def __init__(self,x,y,):
        super().__init__()
        self.x = x
        self.y = y
        
        self.direction = 1#1 is left, -1 is right
        self.path = "assets/saw/animation"#File location
        self.chain_img = pygame.image.load("assets/saw/saw_chain.png")#no animation to the chain, therefore only 1 image
        self.animation_list = []
        for i in range(len(os.listdir(self.path))):#adds all the images from the file path into a list
            img = pygame.image.load(f"{self.path}/{i}.png")
            self.animation_list.append(img)
        self.image = self.animation_list[0]
        self.mask = pygame.mask.from_surface(self.image)

        self.rect = self.image.get_rect()
        self.update_time = pygame.time.get_ticks()
        self.frame_index = 0
        self.vel_y = 0
        self.vel_x = 0
        self.speed = 1
        self.start_x = x
        self.end_x = x + tile_size * 3#The range is 3 tiles forwars then 3 tiles back, oscillates on a straight line
        self.start_y = y
        self.end_y = y +tile_size * 3

    def update_animation(self):
        #The same animation logic throughout the game, cycles throough each image in the animation list and then repeats back to the first index
        animation_cooldown = 100
        self.image = self.animation_list[self.frame_index]
        self.mask = pygame.mask.from_surface(self.image)

        if pygame.time.get_ticks()-self.update_time>animation_cooldown:
            self.update_time = pygame.time.get_ticks()
            self.frame_index +=1
    
        if self.frame_index == len(self.animation_list):
            self.frame_index = 0


    def updatex(self,scroll):
        #Horizontal logic                                                                        
        self.x += self.direction * self.speed#Adds the distance to the rect x
        if self.x <= self.start_x or self.x >= self.end_x:#the condition to check whether the saw is in the given range
            self.direction *= -1
         
        self.rect.x = self.x - scroll
        self.rect.y = self.y

    def updatey(self,scroll):
        self.y += self.direction * self.speed
        if self.y <= self.start_y or self.y >= self.end_y:
            self.direction *= -1

        self.rect.y = self.y
        self.rect.x = self.x - scroll
        
    def draw_chain(self, scroll, screen):
   
        chain_x = self.x + self.image.get_width() // 2 - scroll
        top_y = 0  
        current_y = self.y

        for y in range(top_y, current_y, self.chain_img.get_height()):#Adds a chain across where the saw travels to give the illusion tha tits attached
            screen.blit(self.chain_img, (chain_x - self.chain_img.get_width() // 2, y))#Draws the chain

    def draw(self,screen,scroll):
        screen.blit(self.image, (self.x-scroll , self.y))#Draws the saw