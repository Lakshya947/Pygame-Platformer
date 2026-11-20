import pygame
from settings import *

class spikes(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()

        # Starting position and animation setup
        self.x = x
        self.frame_index = 0
        self.animation = []

        # Load and scale the animation
        for i in range(3):
            img = pygame.image.load(f"assets/spikes/{i}.png")
            img = pygame.transform.scale(img, (64, 32))
            self.animation.append(img)

        # Initial frame + collision mask
        self.image = self.animation[self.frame_index]
        self.mask = pygame.mask.from_surface(self.image)

        # Position on the map
        self.rect = self.image.get_rect(topleft=(x, y))

        # Track when the last frame update happened
        self.update_time = pygame.time.get_ticks()

    def update_animation(self):
        # Basic looping animation with a small delay
        cooldown = 100
        self.image = self.animation[self.frame_index]
        self.mask = pygame.mask.from_surface(self.image)

        if pygame.time.get_ticks() - self.update_time > cooldown:
            self.update_time = pygame.time.get_ticks()
            self.frame_index += 1

        # Loop back to the first frame
        if self.frame_index >= len(self.animation):
            self.frame_index = 0

    def draw(self, scroll):
        # Apply camera scroll and draw to screen
        self.rect.x = self.x - scroll
        screen.blit(self.image, (self.rect.x, self.rect.y))
