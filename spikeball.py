import pygame
import math

class SpikeBall(pygame.sprite.Sprite):
    def __init__(self, x, y, scroll):
        super().__init__()

        # The fixed point the ball orbits around
        self.center = (x, y)

        # Orbit settings
        self.radius = 100
        self.orbital_speed = 0.03
        self.angle = 0

        # Images for the ball and chain
        self.ball_image = pygame.image.load("assets/spike ball/spike_ball.png").convert_alpha()
        self.chain_image = pygame.image.load("assets/spike ball/big_chain.png").convert_alpha()
        self.image = self.ball_image

        # Initial position based on angle + scroll offset
        self.rect = self.image.get_rect(center=self.get_position(scroll))

        # Pixel-perfect collision
        self.mask = pygame.mask.from_surface(self.image)

    def get_position(self, scroll):
        # Calculate orbital position using circular motion theory
        cx, cy = self.center
        x = cx + self.radius * math.cos(self.angle) - scroll
        y = cy + self.radius * math.sin(self.angle)
        return (x, y)

    def update(self, scroll):
        # Slowly rotate around the center point
        self.angle += self.orbital_speed
        self.rect.center = self.get_position(scroll)

    def draw_chain(self, screen, scroll):
        # Draw a simple line from the center to the ball
        pygame.draw.line(screen, (128, 128, 128),
                         (int(self.center[0]) - scroll, int(self.center[1])),
                         self.rect.center, 2)

    def draw(self, screen, scroll):
        # Draw the anchor point, chain, and the ball itself
        pygame.draw.circle(screen, (128, 128, 128),
                           (int(self.center[0]) - scroll, int(self.center[1])), 2)
        self.draw_chain(screen, scroll)
        screen.blit(self.image, self.rect)
