import os
import pygame
import random
import math
import time
import json
from cryptography.fernet import Fernet
pygame.init()
pygame.mixer.init()
keyE = b'nL5cTPi0324Gk2zgRDR6E4Y2iVHfWnrKu4kGzcB1ZnU='
f=Fernet(keyE)
def ens():
    f=Fernet(keyE)
    with open("test.json", "rb") as file:
        file_data = file.read()
    encrypted_data = f.encrypt(file_data)
    with open("test.json", "wb") as file:
        file.write(encrypted_data)
def end():
    f=Fernet(keyE)
    with open("test.json", "rb") as file:
        encrypted_data = file.read()
    decrypted_data = f.decrypt(encrypted_data)
    with open("test.json", "wb") as file:
        file.write(decrypted_data)
#end()

def collison(x1,y1,r1,x2,y2,r2):
    dx = x2 - x1
    dy = y2 - y1
    dist  = dx * dx + dy * dy
    dist = math.sqrt(dist)
    
    if dist >= r1 + r2:
        return False
    else:
        return True
def colision1(rect1 : pygame.Rect,rect2):
    if rect1.colliderect(rect2):
        return True
    return False

clock = pygame.time.Clock()
WIDTH,HEIGHT = 1200,765
window = pygame.display.set_mode((WIDTH,HEIGHT))
def button_colision(width,height,x,y,mousePos,mouseState):
    if mousePos[0] > x and mousePos[0] < x + width and mousePos[1] > y and mousePos[1] < y + height and mouseState[0] == True:
        return True
    else:
        return False

fd = 0

class pozadina:
    def __init__(self):
        self.img = pygame.image.load('haunt.png')
        self.scale = 0.9
        self.width = self.img.get_width()*self.scale
        self.height = self.img.get_height()*self.scale
        self.scaled_img = pygame.transform.scale(self.img, (self.width, self.height))
    def draw(self):
        global window
        window.blit(self.scaled_img,(0,0))
p1 = pozadina()
class Knight:
    def __init__(self,x,y,dx,dy):
        self.x = x
        self.y = y
        self.dx = dx
        self.dy = dy
        self.scale = 1.6
        self.sprite_img = pygame.image.load('idle.png')
        self.width = self.sprite_img.get_width()*self.scale
        self.height = self.sprite_img.get_height()*self.scale
        self.scaled_img = pygame.transform.scale(self.sprite_img, (self.width, self.height))
        self.width = self.scaled_img.get_width()
        self.height = self.scaled_img.get_height()
        self.immobilis = 0
        self.last_direction = 1
        self.state = 3
        self.jump = 0
        self.cooldown = 0
        self.airattack = 0
    def draw(self,window):
        if self.last_direction == 1:
            self.sprite_img = pygame.image.load('idle.png')
        else:
            self.sprite_img = pygame.image.load('idle_l.png')
        if self.move_l:
            if self.state <= 180 and self.state > 135:
                self.sprite_img = pygame.image.load('run_1_l.png')
            if self.state > 90 and self.state <= 135:
                self.sprite_img = pygame.image.load('run_2_l.png')
            if self.state <= 90 and self.state > 45:
                self.sprite_img = pygame.image.load('run_3_l.png')
            if self.state > 0 and self.state <= 45:
                self.sprite_img = pygame.image.load('run_4_l.png')
        if self.move_r:
            if self.state <= 180 and self.state > 135:
                self.sprite_img = pygame.image.load('run_1.png')
            if self.state > 90 and self.state <= 135:
                self.sprite_img = pygame.image.load('run_2.png')
            if self.state <= 90 and self.state > 45:
                self.sprite_img = pygame.image.load('run_3.png')
            if self.state > 0 and self.state <= 45:
                self.sprite_img = pygame.image.load('run_4.png')
        
        
        
        if self.immobilis<=120 and self.immobilis>= 90:
            self.y -= 40
            if self.last_direction <0:
                self.sprite_img = pygame.image.load('attack_1_l.png')
            else:
                self.sprite_img = pygame.image.load('attack_1.png')
                
        if self.immobilis>=60 and self.immobilis< 90:
            if self.last_direction <0:
                self.sprite_img = pygame.image.load('attack_2_l.png')
            else:
                self.sprite_img = pygame.image.load('attack_2.png')
        if self.immobilis<60 and self.immobilis> 0:
            if self.last_direction <0:
                self.sprite_img = pygame.image.load('attack_3_l.png')
            else:
                self.sprite_img = pygame.image.load('attack_3.png')
        if self.jump != 0:
            if self.airattack != 0:
                if self.last_direction == 1:
                    self.sprite_img = pygame.image.load('attack_2.png')
                else:
                    self.sprite_img = pygame.image.load('attack_2_l.png')
            else:
                if self.last_direction == 1:
                    self.sprite_img = pygame.image.load('run_2.png')
                else:
                    self.sprite_img = pygame.image.load('run_2_l.png')
        
        
        
        if self.sprite_img == pygame.image.load('idle.png'):
            self.state =3
            
            
        self.width = self.sprite_img.get_width()*self.scale
        self.height = self.sprite_img.get_height()*self.scale
        self.scaled_img = pygame.transform.scale(self.sprite_img, (self.width, self.height))
        window.blit(self.scaled_img,(self.x,self.y))
        if self.immobilis<=120 and self.immobilis>= 90:
            self.y += 40        
    def move(self):
        global WIDTH
        global HEIGHT
        global mouseState
        global keys
        self.dx = 0
        self.dy = 0
        self.move_l = False
        self.move_r = False
        if self.immobilis==0:
            if self.x >=27.5:
                if keys[pygame.K_a] or keys[pygame.K_LEFT]:
                    self.dx = -2.5
                    self.move_l =True
                    self.move_r = False
                    self.last_direction = -1
                    if self.state == 3:
                        self.state = 180
                    
            if self.x <= WIDTH-230-27.5:
                if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
                    self.dx = 2.5
                    self.move_l =False
                    self.move_r = True
                    self.last_direction = 1
                    if self.state == 3:
                        self.state = 180
        if self.jump == 0:
            self.y = 550
            if self.cooldown == 0:
                if self.immobilis == 0:
                    if keys[pygame.K_SPACE]:
                        self.jump = 50
        
        if self.immobilis == 0:
            if mouseState[0] == True:
                if self.jump == 0:
                    self.immobilis = 120
                else:
                    self.airattack = 30
                    
                    
        if self.jump>=26:
            self.jump-=1
            self.dy=-3

        
        if self.jump==1:
            self.cooldown = 30
        
        if self.jump>0 and self.jump<=25:
            self.jump-=1
            self.dy=3
        
        if self.state != 0:
            if self.immobilis == 0:
                self.x+=self.dx
                self.y+=self.dy
                
        
        if self.airattack > 0:
            self.airattack -= 1
        
        if self.immobilis >0:
            self.immobilis -=1
        
        if self.cooldown >0:
            self.cooldown-=1
        
        if self.state >= 6:
            self.state-=3
class Goblin:
    def __init__(self,x,y,dx,dy,last_direction):
        self.x = x
        self.y = y
        self.dx = dx
        self.dy = dy
        self.last_direction = last_direction
        self.scale = 2
        self.state = 0
        self.attack = 0
        sprite_img = pygame.image.load('run_g1.png')
        self.width = sprite_img.get_width()*self.scale
        self.height = sprite_img.get_height()*self.scale
    def draw(self,window):
        sprite_img = 0
        if self.state <= 180 and self.state > 135:
            if self.last_direction == 1:
                sprite_img = pygame.image.load('run_g1.png')
            else:
                sprite_img = pygame.image.load('run_g1l.png')
        if self.state <= 135 and self.state > 90:
            if self.last_direction == 1:
                sprite_img = pygame.image.load('run_g2.png')
            else:
                sprite_img = pygame.image.load('run_g2l.png')
        if self.state <= 90 and self.state > 45:
            if self.last_direction == 1:
                sprite_img = pygame.image.load('run_g3.png')
            else:
                sprite_img = pygame.image.load('run_g3l.png')
        if self.state <= 45 and self.state > 0:
            if self.last_direction == 1:
                sprite_img = pygame.image.load('run_g4.png')
            else:
                sprite_img = pygame.image.load('run_g4l.png')
                
        if self.attack <= 205 and self.attack > 180:
            if self.last_direction == 1:
                sprite_img = pygame.image.load('attack_g1.png')
            else:
                sprite_img = pygame.image.load('attack_g1l.png')
        if self.attack <= 180 and self.attack > 90:
            if self.last_direction == 1:
                sprite_img = pygame.image.load('attack_g2.png')
            else:
                sprite_img = pygame.image.load('attack_g2l.png')
        if self.attack <= 90 and self.attack > 45:
            if self.last_direction == 1:
                sprite_img = pygame.image.load('attack_g3.png')
            else:
                sprite_img = pygame.image.load('attack_g3l.png')
        if self.attack <= 45 and self.attack > 0:
            if self.last_direction == 1:
                sprite_img = pygame.image.load('attack_g4.png')
            else:
                sprite_img = pygame.image.load('attack_g4l.png')
                
                
        self.width = sprite_img.get_width()*self.scale
        self.height = sprite_img.get_height()*self.scale
        scaled_img = pygame.transform.scale(sprite_img, (self.width, self.height))
        window.blit(scaled_img,(self.x,self.y))
    def move(self,kx,kwidth):
        self.dx = 0
        if self.attack==0:
            if kx>self.x:
                self.last_direction = 1
                self.dx = 1.5
            else:
                self.last_direction = -1
                self.dx = -1.5
        if self.state >= 3:
            self.state -= 3
        if self.state == 0:
            self.state = 180
        if self.attack > 0:
            self.attack-=1
        if self.attack == 0:
            if self.x+self.width>= kx and self.x<kx and self.last_direction == 1 or self.x <= kx+kwidth and self.x>kx and self.last_direction == -1:
                self.attack = 205
        self.x += self.dx
l_g = []
g1 = Goblin(900,610,0,0,0)
l_g.append(g1)
k1 = Knight(100,550,0,0)
screen = 0
while True:
    window.fill("Blue")
    p1.draw()
    keys = pygame.key.get_pressed()
    events = pygame.event.get()
    mouseState = pygame.mouse.get_pressed()
    mousePos = pygame.mouse.get_pos()
    for event in events:
        if event.type == pygame.QUIT:
            exit()
    if keys[pygame.K_ESCAPE]:
        exit()
    for i in range(len(l_g)):
        l_g[i].move(k1.x,k1.width)
    k1.move()
    for i in range(len(l_g)):
        l_g[i].draw(window)
    k1.draw(window)
    pygame.display.update()
    clock.tick(60)
    