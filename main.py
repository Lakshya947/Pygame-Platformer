
import pygame#pygame module 
pygame.init()
from datetime import datetime

from settings import *
from functions import *
from player import Player
from levelcreation import *
from saw import *
from screenTrans import *

player = Player(levels[levelindex].xspawnpoint, levels[levelindex].yspawnpoint,1.25,charactertype)#creating an instance of the player
game_transition = screenTransAnim(2,(0,0,0),40)# this creates a transition between pres  dd start and the first level

#This variable is used to monitor the state of the game whether its in main menu or in level stage
main_menu = True
leaderboard_menu = False

glow = create_glow(80)#This creates an instance glow behind the player
backup_levels = levels
test = False#If true, the game will load the test level instead of the first level for when im testing new features and creating new enemies or objects
open_txt()
printcontrols()
while running:
     if main_menu == True:

        
        screen.fill(WHITE)#Main menu is designd to be simple, so it is a white background with 2 buttons
  
        start_button.draw(screen)#blits the start button
        exit_button.draw(screen)#blits the exit button
        leaderboard_button.draw(screen)
        #this small section underneath is to check for a mouse click and then checks if the cursor was on the button when the click was detected
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if start_button.rect.collidepoint(event.pos):
                    start_game = True
                    main_menu = False
                    start_timer = datetime.now()
                    today = datetime.today()
                    
                    formatted = today.strftime("%d/%m/%Y")
                  
                    
                if exit_button.rect.collidepoint(event.pos):
                    running = False#when exit buttons is pressed, the "main" loop is broken and the game closes
                if leaderboard_button.rect.collidepoint(event.pos):
                    start_game = False
                    main_menu = False
                    leaderboard_menu=True
                    leaderboardtxt()
     elif leaderboard_menu == True:
         leaderboard()
         for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if back_button_player.rect.collidepoint(event.pos):
                    main_menu=True
                    start_game=False
                    leaderboard_menu=False
                
        
     elif start_game == True : #main game starts
        if test == True:# this is a small tool i built in the game so when I am creating new enemies or levels i can use the test level as a blueprint to develop in
            current_level = test_level#current level is swithched to current level
        else:
            current_level = levels[levelindex]#if test is False then level 1 is initiated
        clock.tick(FPS)#limits the FPS to 60 by not letting more frames a second pass
        
        
        if game_transition.draw(screen) == True:
            
            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    running = False

                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    pause = True
                
                    paused()
                    pygame.display.update()
                    while pause:
                        for event in pygame.event.get():
                            if event.type == pygame.QUIT:                                                                                               
                                pygame.quit()
                        
                            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                                pause = False

            
            player.handle_collisions(current_level)#pass in the level to check collisions within the player
            if player.level_completed:#player.level_completed is true when the player collides with flag
                levelindex += 1 #as the levels are stored in a list adding 1 to the list selects the next level
                bullet_group.empty()#emptys the bullet group to prevent bullets travelling across the map
                shell_bullet_group.empty()#emptys shell group 
                player.level_completed = False#  This is swithched to False to start the next level
                
                if levelindex >= len(levels):# this is a mini check to see if there are any more levels
                    completed = True
                else:
                    scroll = 0
                    current_level = levels[levelindex]#switched to the next level given there is atleast 1 more level left
                    player.rect.x = current_level.xspawnpoint#sets the players x coordinate to the start position
                    player.rect.y = current_level.yspawnpoint#sets the players x coordinate to the start position
                    player.current_health = min(player.current_health+10,player.max_health)


                    

            dx = player.update(current_level.tile_list, scroll, bullet_group,current_level.boats)# this is to see how much the player moves


            # Horizontal scrolling
            if player.rect.right > camera_box.right:
                scroll += player.rect.right - camera_box.right
                player.rect.right = camera_box.right
            elif player.rect.left < camera_box.left:
                scroll += player.rect.left - camera_box.left
                player.rect.left = camera_box.left
                #Essentialy there is an area each side of the screen where scrolling starts, this small check is to see if
                #The player is in the area either side of the screen


            bullet_group.update()#activates the update method in the bullet classes
            shell_bullet_group.update()#activates the update method in the shell classes
            screen.fill((51,50,61))
            
            
       
            if completed == False:
                current_level.draw(scroll,player,screen)#draw the current level and player
                player.draw(screen)#draw the player
                player_pos = [player.rect.centerx,player.rect.centery]#players position
                glow_rect = glow.get_rect(center=player_pos)
                screen.blit(glow, glow_rect)
      
                bullet_group.draw(screen)#draws the bullets on the screen
                shell_bullet_group.draw(screen)#draws the bullets from the shell enemy
       
                health_bar.draw(player.current_health,player.max_health,screen)#draws the health bar
                mana_bar.draw(player.current_energy,player.max_energy,screen)
                

                fps_counter()#draws the fps counter
        
            if player.show_grid == True:
                show_hitboxes(current_level, bullet_group,player)#another small tool i put in for a debug tool
                draw_grid()#draws grids onto the screen
        
            if player.current_health <= 0 or player.rect.bottom > death_height: 
                player.alive = False

            if player.alive == False:
                game_over_screen()#draws the game over screen
                pygame.time.wait(1000)
                waiting_for_input = True#This waits for a mouse click
                while waiting_for_input:
                    keys = pygame.key.get_pressed()
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            running = False
                            waiting_for_input = False
                            keys = pygame.key.get_pressed()
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            if reset_button.rect.collidepoint(event.pos) :#if the reset button is pressed
                                

                                if reset_button.rect.collidepoint(event.pos):
                                    waiting_for_input = False
                                    player.alive = True#player is reset
                                    player.current_health = player.max_health#health is reset
                                    player.current_energy = player.max_energy#energy is reset
                                     
                                    scroll = 0#scrolls is set to 0
                                    current_level = levels[levelindex]
                                    player.rect.x = current_level.xspawnpoint#player x is returned to the start of the level
                                    player.rect.y = current_level.yspawnpoint#player y is returned to the start of the level
                                    player.level_completed = False
                                    r = False
                        

                            if exit_btn2.rect.collidepoint(event.pos):
                                running = False
                                waiting_for_input = False   

                        
                        if keys[pygame.K_r]:#instead of pressing the reset button using the mouse the player can press r
                            
                            waiting_for_input = False#waits for an input
                            player.alive = True#player is alive
                            player.current_health = player.max_health#sets health back to max
                            player.current_energy = player.max_energy#sets energy back to max
                                    
                            scroll = 0
                            current_level = levels[levelindex]
                            player.rect.x = current_level.xspawnpoint#resets the characters x position to the start of the level
                            player.rect.y = current_level.yspawnpoint#resets the characters y position to the start of the level
                            player.level_completed = False


                    
            elapsed = datetime.now() - start_timer
            
            drawtimer(elapsed.total_seconds())
            if completed:#if the game is completed (levels are all complete)
                end_timer = datetime.now()
                time_difference=end_timer-start_timer
                timelist=[str(formatted),str(time_difference.total_seconds())]
                close_txt(timelist)
                completed_screen()#blits the game winner screen
                waiting_for_input2 = True
                while waiting_for_input2:
                
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            running = False
                            waiting_for_input2 = False
                        if event.type == pygame.MOUSEBUTTONDOWN:

                            if reset_button2.rect.collidepoint(event.pos):#If the button is pressed the player can replay the game 
                                if reset_button2.rect.collidepoint(event.pos):#they click the button
                                    waiting_for_input2 = False# Breaks the loop 
                                    player.alive = True
                                    player.current_health = player.max_health#resets health
                                    player.current_energy = player.max_energy#resets energy
                                    levelindex = 0# resets the level back to 0
                                    scroll = 0# resets scoll
                                    current_level.shells = current_level.backupshell#all the hazards that can despawn are reset
                                    levels[levelindex] = backup_levels[levelindex]#
                                    current_level = levels[levelindex]
                                    
                                    player.rect.x = current_level.xspawnpoint#resets the position of the character
                                    player.rect.y = current_level.yspawnpoint#resets the position of the character
                                    player.level_completed = False#lets the loop go back to the start
                                    completed = False
                                    player.sw = False
                                    

                            if exit_button3.rect.collidepoint(event.pos):
                                running = False
                                waiting_for_input2 = False   

    
            if volume:
                screen.blit(unmute_icon, (WIDTH - unmute_icon.get_width(), 10))
            else:
                screen.blit(mute_icon, (WIDTH - mute_icon.get_width(), 10))

        



     
     pygame.display.update()

pygame.quit()
