import math
from numpy import mat
import pygame
import random
from pygame import mixer
#Initialize pygame
pygame.init()

#Creating window
screen = pygame.display.set_mode((800,600))

#Title and Icon
pygame.display.set_caption("Space Invaders")
Icon = pygame.image.load("ufo.png")
pygame.display.set_icon(Icon)

#Player
player_image = pygame.image.load("space-invaders.png")
playerx = 370
playery = 480
playerx_change = 0

def player(x,y):
    screen.blit(player_image,(x,y))

#Enemy
enemy_image = []
enemyx = []
enemyy = []
enemyx_change = []
enemyy_change = []

num_of_enemies = 10 
for i in range(num_of_enemies):
    enemy_image.append(pygame.image.load("alien.png"))
    enemyx.append(random.randint(0,735))
    enemyy.append(random.randint(50,150))
    enemyx_change.append(3)
    enemyy_change.append(40)

def enemy(x,y, i ):
    screen.blit(enemy_image[i],(x,y))

#projectile
projectile_img = pygame.image.load("bullet.png")
projectilex = 0
projectiley = 480
projectilex_change = 0
projectiley_change = 10
projectile_state = "ready"

def fire_bullet(x,y):
    global projectile_state
    projectile_state = "fire"
    screen.blit(projectile_img,(x+16,y+10))

def is_colision(enemyy,enemyx,projectiley,projectilex):
    distance = math.sqrt((math.pow(enemyx-projectilex,2) + math.pow(enemyy-projectiley,2)))
    if distance < 27:
        colision_sound = mixer.Sound("explosion.wav")
        colision_sound.play()
        return True
    else:
        return False

#score
score_value = 0
font = pygame.font.Font("freesansbold.ttf",32)
textx = 10
texty = 10
def show_score(x,y):
    score = font.render("Score:"+ str(score_value),True,(255,255,255))
    screen.blit(score,(x,y))
#Background
background = pygame.image.load("background.png")

#Background m usic
mixer.music.load("background.wav")
mixer.music.play(-1)
#Game loop
running = True

while running:
#RGB Background color
    screen.fill((0,0,0))
#Background image
    screen.blit(background,(0,0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
#if key is pressed check left or right
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerx_change = -4
            if event.key == pygame.K_RIGHT:
                playerx_change = 4
            if event.key == pygame.K_SPACE:
                if projectile_state is "ready":
                    bullet_sound = mixer.Sound("laser.wav")
                    bullet_sound.play()
                    projectilex = playerx
                    fire_bullet(playerx,projectiley)

        
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerx_change = 0
    

#spaceship boundaries
    playerx += playerx_change
    
    if playerx <= 0:
        playerx =0
    elif playerx >= 736:
        playerx = 736
#enemy boundaries
    for i in range(num_of_enemies):
        enemyx[i] += enemyx_change[i]

        if enemyx[i] <= 0:
            enemyx_change[i] = 2.5
            enemyy[i] += enemyy_change[i]
        elif enemyx[i] >= 736:
            enemyx_change[i] = -2.5
            enemyy[i] += enemyy_change[i]
        #Colision
        colision = is_colision(enemyy[i],enemyx[i],projectiley,projectilex)
        if colision:
            projectiley = 480
            projectile_state = "ready"
            score_value += 1
            enemyx[i] = random.randint(0,735)
            enemyy[i] = random.randint(50,150)
        enemy(enemyx[i],enemyy[i],i)
#projectile movement
    if projectiley <= 0:
        projectiley = 480
        projectile_state = "ready"
    if projectile_state is "fire":
        fire_bullet(projectilex,projectiley)
        projectiley -= projectiley_change

    player(playerx,playery)
    show_score(textx,texty)
    pygame.display.update()