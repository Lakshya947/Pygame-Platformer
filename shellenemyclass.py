import pygame
from bullet import Bullet
from settings import *
pygame.init()

class ShellEnemy(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        
        # Starting position
        self.x = x
        self.y = y

        # Base sprite and hitbox
        self.image = pygame.image.load("assets/shell enemy/idle/0.png")
        self.rect = self.image.get_rect(center=(x, y))
        self.rect.y = self.y + 10  # slight vertical offset

        # Basic enemy stats
        self.health = 3
        self.cooldown = 0
        self.direction = 1  # 1 = right, -1 = left

        # Pixel-perfect collision
        self.mask = pygame.mask.from_surface(self.image)

    def update(self, player_x, player_y):
        # Face the player
        if player_x >= self.rect.x:
            self.direction = 1
        else:
            self.direction = -1

        # Fire when player is within a horizontal + vertical window
        if self.cooldown + 500 < pygame.time.get_ticks():
            if self.rect.centerx - 250 <= player_x <= self.rect.centerx + 250 and \
               self.rect.centery - 50 <= player_y <= self.rect.centery + 50:
                
                shell_bullet_group.add(
                    Bullet(self.rect.centerx, self.rect.centery, self.direction, pearl, 1)
                )
                self.cooldown = pygame.time.get_ticks()

        # Take damage from player bullets
        if pygame.sprite.spritecollide(self, bullet_group, True, pygame.sprite.collide_mask):
            self.health -= 1

        # kills the enemy when health runs out
        if self.health <= 0:
            self.kill()

    def draw(self, screen, scroll):
        # Flip sprite depending on direction
        flipped_image = pygame.transform.flip(self.image, self.direction == -1, False)

        self.rect.x = self.x - scroll

        # Draw to screen
        screen.blit(flipped_image, (self.rect.x, self.rect.y))
