import pygame
import random
import math
from pygame import mixer

# Initialize the pygame
pygame.init()

# Set the screen size
screen = pygame.display.set_mode((800,600))

# Sound
mixer.music.load("background.wav")
mixer.music.play(-1)


# set the caption of the window title 
pygame.display.set_caption('Galatic Battle 1.0')

# set the icon of window
icon = pygame.image.load('ufo.png')
pygame.display.set_icon(icon)

#Player
playerimg = pygame.image.load('spaceship.png')
playerX = 370
playerY = 480
player_xchange = 0
speedx = 0.4

#Enemy
enemyimg = pygame.image.load('enemy.png')
enemyX = random.randint(0,800)
enemyY = random.randint(50,150)
enemy_xchange = 0.3
enemy_ychange = 40
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 6

for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load('enemy.png'))
    enemyX.append(random.randint(0, 736))
    enemyY.append(random.randint(50, 150))
    enemyX_change.append(0.4)
    enemyY_change.append(40)
#Bullet
bulletimg = pygame.image.load('bullet.png')
bulletX = 0
bulletY = 480
bullet_xchange = 0
bullet_ychange = 0.9
bullet_state = 'ready'

# Score

score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)

textX = 10
testY = 10

# Game Over
over_font = pygame.font.Font('freesansbold.ttf', 64)


def show_score(x, y):
    score = font.render("Score : " + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))


#Functions
def game_over_text():
    over_text = over_font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(over_text, (200, 250))

def player(x,y):
    screen.blit(playerimg,(x,y))

def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))


def bullet(x,y):
    global bullet_state
    bullet_state = 'fire'
    screen.blit(bulletimg,(x + 12 ,y + 9))

def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt(math.pow(enemyX - bulletX, 2) + (math.pow(enemyY - bulletY, 2)))
    if distance < 27:
        return True
    else:
        return False

# Game loop
running = True
while running:
    screen.fill((10,10,10))
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            print('Key is pressed...')
            if event.key == pygame.K_LEFT:
                player_xchange = -speedx    
            if event.key == pygame.K_RIGHT:
                player_xchange = speedx
            if event.key == pygame.K_SPACE:
                if bullet_state is "ready":
                    bulletSound = mixer.Sound("laser.wav")
                    bulletSound.play()
                    # Get the current x cordinate of the spaceship
                    bulletX = playerX
                    bullet(bulletX, bulletY)    
        
        if event.type == pygame.KEYUP:
            player_xchange = 0
            print("Key is released...")          

    
    playerX += player_xchange
    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736    
    #----------------------------------------
        # Enemy Movement
    for i in range(num_of_enemies):

        # Game Over
        if enemyY[i] > 440:
            for j in range(num_of_enemies):
                enemyY[j] = 2000
            game_over_text()
            break

        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 0:
            enemyX_change[i] = 0.3
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 736:
            enemyX_change[i] = -0.3
            enemyY[i] += enemyY_change[i]

        # Collision
        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            explosionSound = mixer.Sound("explosion.wav")
            explosionSound.play()
            bulletY = 480
            bullet_state = "ready"
            score_value += 1
            enemyX[i] = random.randint(0, 736)
            enemyY[i] = random.randint(50, 150)

        enemy(enemyX[i], enemyY[i], i)

    # Bullet Movement
    if bulletY <= 0:
        bulletY = 480
        bullet_state = "ready"

    if bullet_state is "fire":
        bullet(bulletX, bulletY)
        bulletY -= bullet_ychange

    player(playerX, playerY)
    show_score(textX, testY)
    pygame.display.update()     