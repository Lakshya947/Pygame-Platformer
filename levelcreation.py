import pygame
import os
pygame.init()

from settings import *
from World import World
from functions import read_level_from_csv

amount_of_levels = len(os.listdir("levels"))#gets the number of text files in a folder,
#each file is a level



for i in range(amount_of_levels):
    level_data = read_level_from_csv(f"levels/level_{i}.txt")
    levels.append(World(level_data))

test_level = World(read_level_from_csv("Test Level/test_level.txt"))
