
import pygame
pygame.init()
from settings import *
from button import Button

def read_level_from_csv(filename):
    #takes in a file as a paramter and converts it into a 
    #list so it can be fed into the world class to make levels
    grid = []
    with open(filename, 'r') as file:
        for line in file: 
            
            row = []
                        
            for x in line.strip().split(','):
                if x.isdigit():
                    row.append(int(x))
                else:
                    row.append(x)  


            grid.append(row)
    return grid

def get_image(spritesheet, frame_width, frame_height,scale):
    #Takes in a sprite sheet and splits them into
    #individual images and outs them into a list
    
    frames = []
    frame_width = int(frame_width * scale)
    frame_height = int(frame_height * scale)
    sheet_width, sheet_height = spritesheet.get_size()
    spritesheet = pygame.transform.scale(spritesheet, (int(sheet_width * scale), int(sheet_height * scale)))
    for y in range(0, sheet_height, frame_height):
        for x in range(0, sheet_width, frame_width):
            rect = pygame.Rect(x, y, frame_width, frame_height)
            frame = spritesheet.subsurface(rect).copy()
            frames.append(frame)
    
    return frames

def fps_counter():
    fps_text = font.render(f"FPS: {int(clock.get_fps())}", True, (255, 255, 255))
    screen.blit(fps_text, (10, 70))


def draw_grid():#for testing purposes i implemented a toggle grid function 
    for x in range(0, WIDTH, tile_size):
        pygame.draw.line(screen, (255,255,255), (x, 0), (x, HEIGHT))
    for y in range(0, HEIGHT, tile_size):
        pygame.draw.line(screen,(255,255,255), (0, y), (WIDTH, y))


def show_hitboxes(current_level, bullet_group,player):
    #every single enemy/pickup has a hitbox as they are saved as rects in a list, each of these lists

    for blob in current_level.blob_sprite_group:#loops through each item in the list and 
        pygame.draw.rect(screen, (255,255,255), blob.rect, 2)#draws the outline
        #the same logic is repeated for all enemies
    for bullet in bullet_group:
        pygame.draw.rect(screen, (255,255,255), bullet.rect, 2)

    for spike in current_level.spike_sprite_group:
        pygame.draw.rect(screen,(255,255,255),spike.rect,2)

    for checkpoint in current_level.flagspritegroup:
        pygame.draw.rect(screen,(255,255,255),checkpoint.rect,2)
    for pickup in current_level.pickups:
        if pickup.used == False:
            pygame.draw.rect(screen, (RED), pickup.rect, 2)
   
    for dirt in current_level.tile_list:
        if dirt[0] == 1:
            pygame.draw.rect(screen, (255, 255, 255), dirt[1], 2)

    for boat in current_level.boats:
        pygame.draw.rect(screen,(255,255,255),boat.rect,2)
    
    for saw_x in current_level.saws_x:
        pygame.draw.rect(screen, (255, 255, 255), saw_x.rect, 2)
    for saw_y in current_level.saws_y:
        pygame.draw.rect(screen, (255, 255, 255), saw_y.rect, 2)

    for spikeball in current_level.spikeballs:
        pygame.draw.rect(screen, (255, 255, 255), spikeball.rect, 2)

    for shell in current_level.shells:
        pygame.draw.rect(screen, (255, 255, 255), shell.rect, 2)

    for pearls in shell_bullet_group:
        pygame.draw.rect(screen,(255,255,255),pearls.rect)

    pygame.draw.rect(screen, (255, 255, 255), player.rect, 1) 
    
def paused():
    pauseoverlay = pygame.Surface((WIDTH, HEIGHT))#creates a surface that is the same size as the game window
    pauseoverlay.fill((0, 0, 0))# makes it black
    
    screen.blit(pauseoverlay, (0, 0))#blits it on the screen
    pause_font = pygame.font.Font(None, 74)
    text = pause_font.render("PAUSED", True, (255, 255, 255))#creates a text on the screen
    screen.blit(text, text.get_rect(center=(WIDTH // 2, HEIGHT // 2)))#blits the text

def load_character_images(charactertype):
    #Instead of loading each spirtesheeet in manually, i have this function which loads them
    # all at once as each character has the same folder location

    return {
        "run": pygame.image.load(f"assets/${charactertype}/run.png"),
        "idle": pygame.image.load(f"assets/${charactertype}/idle.png"),
        "jump": pygame.image.load(f"assets/${charactertype}/jump.png"),
        "fall": pygame.image.load(f"assets/${charactertype}/fall.png")
    }


def game_over_screen():

    screen.fill(BLACK)#fills the screen black
    game_over_audio.play()#some audio
    game_over_voice.play()
    screen.blit(game_over_image,(WIDTH/2 - game_over_image.get_width()/2,HEIGHT/2-200))#blits an image that says game over
    reset_button.draw(screen)#reset button
    exit_btn2.draw(screen)#exit button
    pygame.display.update()


def completed_screen():
    screen.fill(BLACK)#A black layer is blitted on the screen
    screen.blit(completed_image,(WIDTH/2 - game_over_image.get_width()/2,HEIGHT/2-200))#External image is used as a button
    reset_button2.draw(screen)
    exit_button3.draw(screen)

    pygame.display.update()
 
def leaderboard():
    screen.fill(WHITE)
    back_button_player.draw(screen)
    leaderboardtxt()

def create_glow(radius, color=(255, 255, 255)):#Hollow knight inspired back glow on the character, it is easier to see the character in darker settings
    
    glow_surface = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)
    for r in range(radius, 0, -1):
        alpha = int(255 * (1 - (r / radius))*0.5)#Essentialy draws many circumferences at once that increase in glow brightness
        pygame.draw.circle(glow_surface, (*color, alpha), (radius, radius), r)#draws them
    return glow_surface

times= []

def open_txt():
    with open("times.txt","r") as f:
        for line in f:
            line = line.strip()
            parts = line.strip().split(",")
            times.append(parts)


def close_txt(new_row):
    with open("times.txt","a") as f:
        f.write(",".join(new_row)+"\n")

def leaderboardtxt():
    for i in range(len(times)):
        leaderboardtxt = font2.render(f"{str(times[i][0]) +" " + str(times[i][1])}", True, (0, 0, 0))
        screen.blit(leaderboardtxt, (700, 70+30*i))

def drawtimer(currenttime):
    text = font3.render(f"{str(currenttime)}", True, (255, 255, 255))
    screen.blit(text,(1500,50))

def printcontrols():
    for i in range (3):
        print("")
    print("Shoot - W")
    print("Move Left - A")
    print("Move Right - D")
    print("Jump - Space")
    print("R - reset when dead")