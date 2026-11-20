import pygame
pygame.init()
from settings import *

class screenTransAnim:
    def __init__(self, direction, colour, speed):
        # Store the direction the transition should move in
        # (even though it's not used yet, it's ready for future expansion)
        self.direction = direction
        
        # The colour of the transition rectangle
        self.colour = colour
        
        # How fast the transition should animate each frame
        self.speed = speed
        
        # Tracks how far the animation has progressed
        self.counter = 0

    def draw(self, screen):
        # Increase the counter each frame so the rectangle grows over time
        self.counter += self.speed

        # Assume the transition is not finished yet
        transition_completed = False

        # Draw a rectangle that starts at the top of the screen
        #that goes downwards
        pygame.draw.rect(screen, self.colour, (0, 0, WIDTH, 0 + self.counter))

        # Once the rectangle has fully covered the screen width,
        # we consider the transition finished
        if self.counter >= WIDTH:
            transition_completed = True

        # Return whether the animation has completed so the game
      
        return transition_completed
