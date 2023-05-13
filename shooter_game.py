# Imports
from pygame import *
from random import randint
from time import time as timer    

# Music 
mixer.init()
mixer.music.load("space.ogg")
mixer.music.play()
fire_sound = mixer.Sound("fire.ogg")

# Fonts 
font.init()
font2 = font.Font(None, 36)
win = font2.render("You uh won", True, (255, 255, 255))
lose = font2.render("You Lost hehe", True, (10, 0, 0))

# Images
img_back = "galaxy.jpg"                           # Background Image
img_hero = "rocket.png"                           # Rocket
img_enemy = "ufo.png"
img_bullet = "bullet.png"

score = 0
lost = 0
max_lost = 3

# Classes
class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        sprite.Sprite.__init__(self)
        #Properties
        self.image = transform.scale(image.load(player_image), (size_x, size_y))    
        self.speed = player_speed
        #Rectangle
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
 
    def reset(self):
        #draw the character on the window
        window.blit(self.image, (self.rect.x, self.rect.y))
 
class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
 
        if keys[K_RIGHT] and self.rect.x < win_width - 80:
             self.rect.x += self.speed
 
    def fire(self):
        bullet = Bullet(img_bullet, self.rect.centerx, self.rect.top, 15, 20, 15)
        bullets.add(bullet)

class Enemy(GameSprite):
    def update(self):
        global lost
        # Automatic Movement
        self.rect.y += self.speed
        if self.rect.y > win_height:                       # Line 52-55 Once Enemy hits the bottom of the window
            self.rect.x = randint(80, win_width - 80)      # it teleports back to the top on the window
            self.rect.y = 0                                
            lost = lost + 1     

class Bullet(GameSprite):
    # Movement
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y < 0:
            self.kill()

# Window ( Screen You See )
win_width = 700                                            # Width of the Window
win_height = 500                                           # Height of the Window
display.set_caption("Shooter")                             # Caption
window = display.set_mode((win_width, win_height))
background = transform.scale(image.load(img_back), (win_width, win_height))

# Sprites
ship = Player(img_hero, 5, win_height - 100, 80, 100, 10)   # Your Player

monsters = sprite.Group()
bullets = sprite.Group()

for i in range(1,6):
    myufo = Enemy(img_enemy, randint(80, win_width - 80), -40, 80, 50, randint(1,5))
    monsters.add(myufo)

# Variables
finish = False
run = True
while run == True:                                # Loop
    for e in event.get():                         # Loop 2
        if e.type == QUIT:                        # If you close the app it stops
           run = False 
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                fire_sound.play()
                ship.fire()

    if not finish:
        window.blit(background, (0,0))

        # Score Text - Text for the score
        text_score = font2.render("Score: " + str(score), 1, (255,255,255))
        window.blit(text_score,(10,20))

        # Missed Text - Text when you miss
        text_lose = font2.render("Missed: " + str(lost), 1, (255,255,255))
        window.blit(text_lose, (10, 50))

        ship.update()
        ship.reset()

        monsters.update()
        monsters.draw(window)
        bullets.update()
        bullets.draw(window)

        #collission bullets, ufo
        collides = sprite.groupcollide(monsters, bullets, True, True)
        for c in collides:
            score += 1
            myufo = Enemy(img_enemy, randint(80, win_width - 80), -40, 80, 50, randint(1,5))
            monsters.add(myufo)
        # Win Condition
        if score >= 10:
            finish = True 
            window.blit(win, (200, 200))

        # Lose Condition
        if sprite.spritecollide(ship, monsters, False):
            finish = True
            window.blit(lose, (200, 200))

        display.update()

    time.delay(50)              # 0.05 Seconds / To Slow Down The Rocket