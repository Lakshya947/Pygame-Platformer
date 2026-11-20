import pygame
pygame.init()
from bars import bar
from button import Button

#Main game settings
HEIGHT = 768
WIDTH = 1600
tile_size = 64
FPS = 60
GRAVITY = 1

money = 0
pause = False
BLACK = (0, 0, 0)
RED = (255, 0, 0)
WHITE = (255, 255, 255)
death_height = HEIGHT +500
show_grid = False
#Fonts
font = pygame.font.Font(None, 36)
font2 = pygame.font.Font("assets/daydream.ttf",18)
font3 = pygame.font.Font("assets/daydream.ttf",10)
# Initialize Pygame and create a screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Platformer")
clock = pygame.time.Clock()

#assets
fireball = pygame.image.load("assets/fireball.png")

pearl = pygame.image.load("assets/shell enemy/pearl.png")

camera_box = pygame.Rect(
    WIDTH//2 - 200,  # left
    HEIGHT//2 - 150, # top
    640,             # width
    480              # height
)

#default
charactertype = "virtual guy"
#Button images
start_button_image = pygame.image.load("assets/buttons/start_btn.png")
exit_button_image = pygame.image.load("assets/buttons/exit_btn.png")
settings_button_image = pygame.image.load("assets/buttons/settings_btn.png")
running = True

#cooldowns
blobcooldown = 0
flagcooldown = 0
spikecooldown = 0

main_menu = True
settings = False
character_selection = False

scroll = 0
levels = []
backup_levels = []

levelindex = 0

completed = False

#Bullet group for the player
bullet_group = pygame.sprite.Group()

#Buttons
start_button = Button(WIDTH/2-279/2, HEIGHT/2-200,start_button_image)
exit_button = Button(WIDTH/2-240/2, HEIGHT/2-126+100,exit_button_image)

#Audio
volume = True
volumebuttoncooldown = 0
pygame.mixer.music.load("audio/bg music.mp3")
pygame.mixer.music.set_volume(0.4)  # Set initial volume

pygame.mixer.music.play(-1)
game_over_audio = pygame.mixer.Sound("audio/game over arcade.mp3")
game_over_voice = pygame.mixer.Sound("audio/game over voice.mp3")

jumpfx = pygame.mixer.Sound("audio/jump.mp3")
jumpfx.set_volume(0.8)
shootfx = pygame.mixer.Sound("audio/shoot.mp3")
shootfx.set_volume(0.5)
levelcompletefx = pygame.mixer.Sound("audio/levelcomplete.wav")
levelcompletefx.set_volume(0.5)

characterbutton = Button(100,100,pygame.image.load(f"assets/buttons/player_btn.png "))
volume_btn = Button(100, 250, pygame.image.load("assets/buttons/volume_btn.png"))
back_button = Button(100, 400, pygame.image.load("assets/buttons/back_btn.png"))


mute_icon  = pygame.image.load("assets/volume/mute.png")
unmute_icon = pygame.image.load("assets/volume/unmute.png")
mute_icon = pygame.transform.scale(mute_icon, (30, 30))
unmute_icon = pygame.transform.scale(unmute_icon, (30, 30))

#Load stock images
masked_dude_image = pygame.image.load("assets/$masked dude/fall.png")
masked_dude_image = pygame.transform.scale(masked_dude_image, (150, 150))
pinkman_image = pygame.image.load("assets/$pinkman/fall.png")
pinkman_image = pygame.transform.scale(pinkman_image, (150, 150))
ninja_frog_image = pygame.image.load("assets/$ninja frog/fall.png")
ninja_frog_image = pygame.transform.scale(ninja_frog_image, (150, 150))
virtual_guy_image = pygame.image.load("assets/$virtual guy/fall.png")
virtual_guy_image = pygame.transform.scale(virtual_guy_image, (150, 150))
#reset button image
reset_img = pygame.image.load("assets/buttons/reset_button.png")
#exit image
exit_img2 = pygame.image.load("assets/buttons/exit_btn2.png")
#game over button
game_over_image = pygame.image.load("assets/buttons/game over.png")
#game images
game_image = pygame.image.load("assets/buttons/game.png")
completed_image = pygame.image.load("assets/buttons/complete.png")
reset_button2  = Button(WIDTH/2 - reset_img.get_width()/2,HEIGHT/2+100,pygame.image.load("assets/buttons/reset_button2.png"))
exit_button3 = Button(WIDTH/2 - pygame.image.load("assets/buttons/exit_btn3.png").get_width()/2,HEIGHT/2-50,pygame.image.load("assets/buttons/exit_btn3.png"))
trophyimage = pygame.image.load("assets/buttons/trophy.png")
trophyimage = pygame.transform.scale(trophyimage, (trophyimage.get_height()*0.5, trophyimage.get_width()*0.5))

#create stock image buttons so that the player can click on who they want to play as
masked_dude_button = Button(150, 100, masked_dude_image)
pinkman_button = Button(300, 100, pinkman_image)
ninja_frog_button = Button(450, 100, ninja_frog_image)
virtual_guy_button = Button(0, 100, virtual_guy_image)
back_button_player = Button(0, 300, pygame.image.load("assets/buttons/back_btn.png"))
leaderboard_button = Button(10,10,trophyimage)
#reset button
reset_button = Button(WIDTH/2 - reset_img.get_width()/2 ,HEIGHT/2-50,reset_img)

#exit button
exit_btn2 = Button(WIDTH/2 - exit_img2.get_width()/2 ,HEIGHT/2+100,exit_img2)
#shell bullet group
shell_bullet_group = pygame.sprite.Group()

images = []
for i in range(3):
    image = pygame.image.load(f"assets/background/{i}.png").convert_alpha()
    scaled_image = pygame.transform.scale(image,(WIDTH,HEIGHT))
    images.append(scaled_image)

health_bar = bar(10,10,200,20,(255,0,0),(0,255,0))
mana_bar = bar(10,40,200,20,(222,38,191),(65,44,201))


