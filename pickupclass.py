import pygame

class pickup(pygame.sprite.Sprite):
    def __init__(self, path, x, y, function, scale):
        super().__init__()
        self.x = x
        self.y = y
        self.function = function
        self.image = pygame.image.load(f"assets/pickups/{path}.png")
        self.image = pygame.transform.scale(self.image, (int(self.image.get_width() * scale), int(self.image.get_height() * scale)))
        self.rect = self.image.get_rect(topleft=(x, y))
        self.used = False#This paramaeter is there so that when the pickup is used
        #this is changed to true so it doesnt stay there indefinitely
        
    def healthcrate(self,player):
        player.current_health = min(player.max_health, player.current_health + 20)#Once the player picksup the potion then 
        #the new player health is compared with the max health, so there is no overheal

        

    def energypotion(self,player):
        player.current_energy = min(player.max_energy, player.current_energy + 20)
        #Same logic is repeated here

    

    def update(self, scroll,player,screen):
        self.rect.x = self.x - scroll
        if self.rect.colliderect(player.rect) and not self.used:
            if self.function == "health potion": 
                self.healthcrate(player)#calls the method to prevent overhealing
            elif self.function == "mana potion": 
                self.energypotion(player)
            self.used = True#parameter to check is chained to true
        if not self.used:
            screen.blit(self.image, self.rect)  #if the potions are not picked up, it is blitted on the screen