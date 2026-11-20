import pygame
from settings import *
from blobclass import blob
from pickupclass import pickup
from spikeclass import spikes
from floatingplatform import FloatingPlatform
from saw import Saw
from spikeball import SpikeBall
from shellenemyclass import ShellEnemy
from Decor import decorClass

terrain = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M','N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X' ]

class World:
    def __init__(self, data):
        """
        Builds the world by reading the level data grid.
        Each tile value spawns a different object (enemies, hazards, pickups, terrain).
        Sprite groups are used so each type can update/draw itself independently.
        """
        self.tile_list = []
        self.pickups = []
        self.blobs = []
        self.spikes = []
        self.soldierslist = []
        self.data = data
        self.flags = []
        self.decor = []
        self.F_list = []
        self.boats = pygame.sprite.Group()
        self.soldiers_sprite_group = pygame.sprite.Group()
        self.blob_sprite_group = pygame.sprite.Group()
        self.spike_sprite_group = pygame.sprite.Group()
        self.flagspritegroup = pygame.sprite.Group()
        self.saws_x = pygame.sprite.Group()
        self.saws_y = pygame.sprite.Group()
        self.spikeballs = pygame.sprite.Group()
        self.shells = pygame.sprite.Group()
        self.backupshell = pygame.sprite.Group()

        for row_index, row in enumerate(self.data):
            for col_index, tile in enumerate(row):
                x = col_index * tile_size
                y = row_index * tile_size

                # Object spawning based on tile ID
                if tile == 2:
                    self.pickups.append(pickup("health potion", x, y, "health potion", 3))
                elif tile == 3:
                    self.pickups.append(pickup("mana potion", x, y, "mana potion", 3))
                elif tile == 4:
                    new_blob = blob(x, y)
                    self.blobs.append(new_blob)
                    self.blob_sprite_group.add(new_blob)
                elif tile == 5:
                    new_spike = spikes(x, y)
                    self.spikes.append(new_spike)
                    self.spike_sprite_group.add(new_spike)
                elif tile == 7:
                    platform = FloatingPlatform(x, y, 200)
                    self.boats.add(platform)
                elif tile == 8:
                    saw1 = Saw(x, y)
                    self.saws_x.add(saw1)
                elif tile == 9:
                    saw2 = Saw(x, y)
                    self.saws_y.add(saw2)
                elif tile == 10:
                    spikeball = SpikeBall(x, y, scroll)
                    self.spikeballs.add(spikeball)
                elif tile == 11:
                    shell = ShellEnemy(x, y)
                    self.shells.add(shell)
                    self.backupshell.add(shell)
                elif tile == 12:
                    tree = decorClass(x, y, "standard", 500)
                    self.decor.append(tree)
                elif tile == 13:
                    tree = decorClass(x, y, "large", 500)
                    self.decor.append(tree)
                elif tile == 14:

                    tree = decorClass(x, y, "left", 500)
                    self.decor.append(tree)
                elif tile == 15:
                    tree = decorClass(x, y, "right", 500)
                    self.decor.append(tree)
                elif tile == 17:
                    tree = decorClass(x, y, "dark left", 500)
                    self.decor.append(tree)
                elif tile == 18:
                    tree = decorClass(x, y, "dark right", 500)
                    self.decor.append(tree)
                elif tile == "Y":
                    self.xspawnpoint = x
                    self.yspawnpoint = y
                elif tile == "Z":
                    new_flag = decorClass(x, y - 18, "flag", 100)
                    self.flags.append(new_flag)
                    self.flagspritegroup.add(new_flag)

                # Terrain tiles
                for i in range(len(terrain)):
                    if tile != "F":
                        if tile == terrain[i]:
                            img = pygame.transform.scale(
                                pygame.image.load(f"assets/terrain/{terrain[i]}.png"),
                                (tile_size, tile_size)
                            )
                            rect = img.get_rect(topleft=(x, y))
                            mask = pygame.mask.from_surface(img)
                            self.tile_list.append((img, rect, mask))

                    elif tile == "F":
                        img = pygame.transform.scale(
                            pygame.image.load("assets/terrain/F.png"),
                            (tile_size, tile_size)
                        )
                        rect = img.get_rect(topleft=(x, y))
                        mask = pygame.mask.from_surface(img)
                        self.F_list.append((img, rect, mask))

    def draw(self, scroll, player, screen):
        """
        Draws every object in the world.
        Each category (terrain, enemies, hazards, pickups) is updated and drawn
        using its own logic, keeping the world modular and easy to expand.
        """

        # Terrain
        for tile in self.tile_list:
            screen.blit(tile[0], (tile[1].x - scroll, tile[1].y))

        for tile in self.F_list:
            screen.blit(tile[0], (tile[1].x - scroll, tile[1].y))

        # Decorative objects
        for item in self.decor:
            item.update_animation(scroll)
            item.draw(screen)

        # Pickups
        for item in self.pickups:
            item.update(scroll, player, screen)

        # Enemies and hazards
        for blob in self.blobs:
            blob.update(scroll)
            blob.draw(screen)

        for spike in self.spikes:
            spike.update_animation()
            spike.draw(scroll)

        for checkpoint in self.flags:
            checkpoint.update_animation(scroll)
            checkpoint.draw(screen)

        for soldier in self.soldierslist:
            soldier.update()
            soldier.draw(scroll, screen)

        for boat in self.boats:
            boat.update(scroll)
            boat.draw(scroll, screen)

        for sawx in self.saws_x:
            sawx.update_animation()
            sawx.updatex(scroll)
            sawx.draw_chain(scroll, screen)
            sawx.draw(screen, scroll)

        for sawy in self.saws_y:
            sawy.update_animation()
            sawy.updatey(scroll)
            sawy.draw_chain(scroll, screen)
            sawy.draw(screen, scroll)

        for spikeball in self.spikeballs:
            spikeball.get_position(scroll)
            spikeball.update(scroll)
            spikeball.draw_chain(screen, scroll)
            spikeball.draw(screen, scroll)

        for shell in self.shells:
            shell.update(player.rect.x, player.rect.y)
            shell.draw(screen, scroll)
