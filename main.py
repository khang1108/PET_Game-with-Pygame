import pygame as pg
import os
import math
import random

from pygame.surface import Surface
from pygame.key import ScancodeWrapper

pg.init()

IMAGE_FOLDER_PATH = os.path.join("pygame-course" , "image")
CAPTION = "Game bắn Chần Da Bẻo"
RESOLUTION = (1080 , 720)
BACKGROUND = pg.image.load(os.path.join(IMAGE_FOLDER_PATH , "bg.png"))
FONT_PATH = os.path.join("pygame-course" , "Fonts" , "Minecraft.ttf")
clock = pg.time.Clock()

class Player():
    def __init__(self , screen : Surface) -> None:
        self.player_IMG = pg.image.load(os.path.join(IMAGE_FOLDER_PATH , "rc-plane.png"))
        self.screen = screen
        self.player_posX  , self.player_posY = 1080/2 - 40 ,400

        self.player_speed = 10
    
    def resize(self , percent , img):
        img = pg.transform.scale(img , (img.get_width()*percent /100 , img.get_height()* percent / 100))
        return img

    def display(self ):
        self.screen.blit(self.player_IMG ,(self.player_posX , self.player_posY))

class Enemy():
    def __init__(self , x , y , screen : Surface) -> None:
        self.enemyX , self.enemyY = x , y
        self.enemy_IMG = pg.image.load(os.path.join(IMAGE_FOLDER_PATH , "enemy.png"))

        self.screen = screen

    def resize(self , percent , img):
        img = pg.transform.scale(img , (img.get_width()*percent /100 , img.get_height()* percent / 100))
        return img
    
    def move(self , speedX , speedY):
        self.enemyX += speedX
        
        if self.enemyX > 1080 - 40:
            self.enemyX = 0
            self.enemyY += speedY

    def display(self):
        self.screen.blit(self.enemy_IMG , (self.enemyX , self.enemyY))

class Bullet(Player):
    def __init__(self , screen : Surface) -> None:
        self.bulletImage = pg.image.load(os.path.join(IMAGE_FOLDER_PATH , "bullet.png"))
        self.bullet_posX , self.bullet_posY = 0 , 0

        self.bulletStatus = "ready"
        self.screen = screen

        self.bullet_speed = 10

    def fire(self , pos_x , pos_y):
        self.screen.blit(self.bulletImage , (self.bullet_posX + 5, self.bullet_posY))    

class Game():
    def __init__(self) -> None:

        self.speedX , self.speedY = 5 , 30
        self.score = 0

        self.icon = os.path.join(IMAGE_FOLDER_PATH , "traffic-lights.png")
        self.caption = CAPTION
        self.resolution = RESOLUTION

        self.screen = pg.display.set_mode(RESOLUTION)

        pg.display.set_caption(self.caption)
        pg.display.set_icon(pg.image.load(self.icon))

        self.player = Player(self.screen)
        self.bullet = Bullet(self.screen)
        self.enemy = Enemy(random.randint(0 , 1080) , random.randint(100 , 350) , self.screen)

        self.player.player_IMG = self.player.resize(20 , self.player.player_IMG)
        self.bullet.bulletImage = self.bullet.resize(2 , self.bullet.bulletImage)
        self.enemy.enemy_IMG = self.enemy.resize(30 , self.enemy.enemy_IMG)
        
        self.run = True
    
    def show_score(self , score):
        score = pg.font.Font(FONT_PATH , 32).render(f"Score : {score}" , True , (255 , 255 , 255))

        self.screen.blit(score , (32 , 32))
    def lose(self , enemyX , enemyY , playerX , playerY):
        distance = math.sqrt(pow(enemyX - playerX , 2) + pow(enemyY- playerY , 2))
        if distance < 55:
            return True
        return False
    
    def hit_the_target(self , enemyX , enemyY , bulletX , bulletY):
        distance = math.sqrt(pow(enemyX - bulletX , 2) + pow(enemyY-bulletY , 2))
        if distance < 55:
            return True
        return False
    
    def running(self):
        fr = open(os.path.join("pygame-course" , "src" , "high_score.txt"), "r")
        high_score = fr.read()

        fr.close()

        while self.run:
            
            self.screen.fill((0 , 0 , 0))
            clock.tick(60)

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.run = False

            self.screen.blit(BACKGROUND , (0 , 0))
            self.show_score(self.score)
            
            high_score_text = pg.font.Font(FONT_PATH , 32).render(f"High Score : {str(high_score)}" , True , (255 , 255 , 255))
            self.screen.blit(high_score_text , (1080-240 ,32))
            
            self.player.display()

            self.enemy.move(self.speedX , self.speedY)
            
            self.enemy.display()

            keys = pg.key.get_pressed()

            if(keys[pg.K_UP]):
                self.player.player_posY -= self.player.player_speed
            if(keys[pg.K_DOWN]):
                self.player.player_posY += self.player.player_speed
            if(keys[pg.K_RIGHT]):
                self.player.player_posX += self.player.player_speed
            if(keys[pg.K_LEFT]):
                self.player.player_posX -= self.player.player_speed
            if(keys[pg.K_SPACE]):
                self.bullet.bulletStatus = "fire"
                self.bullet.bullet_posX , self.bullet.bullet_posY = self.player.player_posX +41.810 , self.player.player_posY

            # print(f"Bullet ({self.bullet.bullet_posX , self.bullet.bullet_posY})")
            # print(f"Player ({self.player.player_posX , self.player.player_posY})")
            # print(f"Enemy ({self.enemy.enemyX , self.enemy.enemyY})")

            if self.bullet.bulletStatus == "fire":
                self.bullet.fire(self.player.player_posX , self.player.player_posY)
                self.bullet.bullet_posY -= self.bullet.bullet_speed
            
            if self.bullet.bullet_posY > 720 or self.bullet.bullet_posY < 0:
                self.bullet.bulletStatus = "ready"
                self.bullet.bullet_posY = self.player.player_posY
                self.bullet.bullet_posX = self.player.player_posX
            
            if self.hit_the_target(self.bullet.bullet_posX , self.bullet.bullet_posY , self.enemy.enemyX , self.enemy.enemyY):
                self.score += 1
                high_score = max(int(high_score) , self.score)
                
                if self.score % 5 ==0:
                    self.speedX += 10
                    self.speedY += 30
                self.bullet.bullet_posX , self.bullet.bullet_posY = self.player.player_posX + 5 , self.player.player_posY
                self.enemy.enemyX , self.enemy.enemyY = random.randint(0 , 1080) , random.randint(0 , 200)
                self.bullet.bulletStatus = "ready"

            self.player.player_posX = max(0 , min(1050 , self.player.player_posX))
            self.player.player_posY = max(0 , min(670 , self.player.player_posY))

            if self.lose(self.enemy.enemyX , self.enemy.enemyY , self.player.player_posX , self.player.player_posY):
                text = pg.font.Font(FONT_PATH , 100).render("NGU V** C*T" , True , (255 , 255 , 255))
                self.screen.blit(text , (1080/3 - 100 , 720 /2 - 50))
                self.enemy.X , self.enemy.enemyY , self.player.player_posX , self.player.player_posY = 0 , 0 , 0 ,0
                
                fw = open(os.path.join("pygame-course" , "src" , "high_score.txt") , "w")
                fw.write(str(high_score))
                fw.close()

                pg.display.update()
                waitting = True
                while waitting:
                    event = pg.event.wait()
                    if event.type == pg.QUIT:
                        self.run = False
                        waitting = False

            pg.display.update()
            pg.display.flip()

    
if __name__ == '__main__':
    myGame = Game()

    myGame.running()
