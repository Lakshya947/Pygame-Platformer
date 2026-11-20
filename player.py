import pygame
pygame.init()
from settings import *
from functions import *
from bullet import Bullet
import math
class Player:
    def __init__(self, x, y,scale,charactertype):
        super().__init__()
        self.charactertype = charactertype
        self.scale = scale
        self.idleanimation = get_image(load_character_images(self.charactertype)["idle"],32,32,1.25)#Loads the character sprietsheets in
        #Self created functions turn them into lists of images immediately
        self.runninganimation = get_image(load_character_images(self.charactertype)["run"],32,32,1.25)
        self.jumpinganimation = get_image(load_character_images(self.charactertype)["jump"],32,32,1.25)
        self.fallinganimation = get_image(load_character_images(self.charactertype)["fall"],32,32,1.25)
     
        self.animations = [
            self.idleanimation,    
            self.runninganimation, 
            self.jumpinganimation, 
            self.fallinganimation  
        ]
        self.show_grid = False
        self.action = 0
        self.frame_index = 0
        self.image = self.animations[self.action][self.frame_index]
        self.rect = self.image.get_rect(topleft=(x, y))
        self.showgridcooldown = 0
        
        #Character movement variables
        self.vel_y = 0
        self.jumping = False
        self.max_health = 100
        self.current_health = self.max_health
        self.max_energy = 100
        self.current_energy = self.max_energy
        self.direction = 1
        self.update_time = pygame.time.get_ticks()
        self.cooldown = 0
        self.last_hit = 0
        self.alive = True

        #Cooldowns
        self.blob_cooldown = 0
        self.sawx_cooldown = 0
        self.sawy_cooldown = 0
        self.flag_cooldown = 0
        self.spikeball_cooldown = 0
        self.shellcooldown = 0
        self.level_completed = False
        self.animcooldown = 75
        self.dash_cooldown = 0
        
        self.mask = pygame.mask.from_surface(self.image)
        self.sprint = False
        self.speed = 6.5
       
        self.jumpval = 20

    def handle_collisions(self, level):
        now = pygame.time.get_ticks()
        #The logic is basicly the same throughtout, if there is a collision there is damage inflicted
        # Blob damage
        if pygame.sprite.spritecollide(self, level.blob_sprite_group, False,pygame.sprite.collide_mask):
            if self.blob_cooldown + 100 < now:
                self.current_health -= 10
                self.blob_cooldown = now

        #Collision with spikes = instant death
        if pygame.sprite.spritecollide(self, level.spike_sprite_group, False,pygame.sprite.collide_mask):
            self.current_health = 0

        # Collision with Flags = complete level
        if pygame.sprite.spritecollide(self, level.flagspritegroup, False,pygame.sprite.collide_mask):
     
            if self.flag_cooldown + 1000 < now:
                levelcompletefx.play()
                self.flag_cooldown = now
                self.level_completed = True


        if pygame.sprite.spritecollide(self, level.saws_x, False,pygame.sprite.collide_mask):
            if self.sawx_cooldown + 10 < now:#As long as the cooldown has passed then the player takes damage
                #This is there so that the player doesnt die immediatley because there are technicly many collisions in a second
                self.current_health -= 1
                self.sawx_cooldown = now

        if pygame.sprite.spritecollide(self, level.saws_y, False,pygame.sprite.collide_mask):#Collision with a saw (vertical or horizontal ) will deal damage
            if self.sawy_cooldown + 100 < now:
                self.current_health -= 10
                self.sawy_cooldown = now

        if pygame.sprite.spritecollide(self, level.spikeballs, False, pygame.sprite.collide_mask):
            if self.spikeball_cooldown + 1000 < now:
                self.current_health -= 50
                self.spikeball_cooldown = now
                    

        if pygame.sprite.spritecollide(self,shell_bullet_group,True,pygame.sprite.collide_mask):
            self.current_health -= 15#The cooldown isnt needed here because the shell enemy shoots bullets
            self.current_energy -= 10
        
        # Check death
        if self.current_health <= 0 or self.rect.bottom > death_height:#if health <0 or the player is below the death height
            self.alive = False

        if self.rect.top <0:
            self.rect.top = 3#This is so that character doesnt go off the screen
        if self.rect.left <0:
            self.rect.left = 0

    def update(self, tiles, scroll,bullet_group,boats):
        keys = pygame.key.get_pressed()
        dx = 0
        dy = 0
        if keys[pygame.K_a]:# when a is pressed the player goes left
            dx -= self.speed
            self.direction = -1
        if keys[pygame.K_d]:#when d is pressed the player goes right
            dx += self.speed
            self.direction = 1
        if keys[pygame.K_SPACE] and not self.jumping:#Jump button
            jumpfx.play()#plays a sound effect
            self.vel_y = -self.jumpval
            self.jumping = True
            
        if keys[pygame.K_w] and self.cooldown + 500 < pygame.time.get_ticks() and self.current_energy > 0:#space is a shoot button
            shootfx.play()

            bullet_group.add(Bullet(self.rect.centerx, self.rect.centery, self.direction,fireball,1 ))#Adds a bullet to the group
            #this group gets reupdated every frame
            self.current_energy -= 5#shooting costs energy
            self.cooldown = pygame.time.get_ticks()

        if keys[pygame.K_TAB]:
            if self.showgridcooldown + 500 < pygame.time.get_ticks():#this is the show grid function for testing
                # so that people can see textboxes
                self.showgridcooldown = pygame.time.get_ticks()
                if self.show_grid == False:
                    self.show_grid = True
                elif self.show_grid == True:
                    self.show_grid = False
       

        # apply gravity
        self.vel_y += GRAVITY
        dy += self.vel_y

        # collision with tiles
        for tile in tiles:
            rect = tile[1].copy()
            rect.x -= scroll  # adjust tile position based on camera scroll

            # horizontal collision
            if rect.colliderect(self.rect.x + dx, self.rect.y, self.rect.width, self.rect.height):
                dx = 0

            # vertical collision
            if rect.colliderect(self.rect.x, self.rect.y + dy, self.rect.width, self.rect.height):
                if self.vel_y > 0:  # falling
                    dy = rect.top - self.rect.bottom
                    
                    self.vel_y = 0
                    self.jumping = False
                elif self.vel_y < 0:  # jumping upward
                    dy = rect.bottom - self.rect.top
                    self.vel_y = 0
                    dx += 12*self.direction
        # collision with moving platforms (boats)
        for platform in boats:
            # horizontal collision
            if platform.rect.colliderect(self.rect.x + dx, self.rect.y, self.rect.width, self.rect.height):
                dx = 0

            # vertical collision
            if platform.rect.colliderect(self.rect.x, self.rect.y + dy, self.rect.width, self.rect.height):
                if self.vel_y > 0:  # landing on platform
                    dy = platform.rect.top - self.rect.bottom
                    self.vel_y = 0
                    self.jumping = False
                    # move with the platform
                    dx += platform.speed * platform.direction
                    new_action = 0

                elif self.vel_y < 0:  # hitting bottom of platform
                    dy = platform.rect.bottom - self.rect.top
                    self.vel_y = 0

        # determine animation state
        if self.vel_y < 0:
            new_action = 2  # jumping
        elif self.vel_y > 1:
            new_action = 3  # falling
        elif dx != 0:
            new_action = 1  # running
        else:
            new_action = 0  # idle

        # update animation state and frames
        self.update_action(new_action)
        self.update_animation()

        # apply movement
        self.rect.x += dx
        self.rect.y += dy
        return dx

    def update_animation(self):
        # set current frame image
        self.image = self.animations[self.action][self.frame_index]
        # update mask for pixel-perfect collision
        self.mask = pygame.mask.from_surface(self.image)

        # update frame based on cooldown
        if pygame.time.get_ticks() - self.update_time > self.animcooldown:
            self.update_time = pygame.time.get_ticks()
            self.frame_index += 1

        # loop animation frames
        if self.frame_index >= len(self.animations[self.action]):
            self.frame_index = 0     

    def update_action(self, new_action):
        # change animation only if action changed
        if new_action != self.action:
            self.action = new_action
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()

    def draw(self,screen):
        # flip sprite based on direction (-1 = left)
        flipped_image = pygame.transform.flip(self.image, self.direction == -1, False)
        # draw sprite to screen
        screen.blit(flipped_image, self.rect)
