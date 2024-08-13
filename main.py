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
    
    if dist >= (r1 + r2 - (((r1+r2)/2)*0.2)):
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
    def draw(self,window):
        window.blit(self.scaled_img,(self.x,self.y))
class Zombie:
    def __init__(self,x,y,dx,dy):
        self.x = x
        self.y = y
        self.dx = dx
        self.dy = dy
        self.scale = 1.6
        self.sprite_img = pygame.image.load('idle.png')
        self.width = self.sprite_img.get_width()*self.scale
        self.height = self.sprite_img.get_height()*self.scale
    def draw(self,window):
        pass
k1 = Knight(100,500,0,0)
screen = 0
while True:
    window.fill("Blue")
    keys = pygame.key.get_pressed()
    events = pygame.event.get()
    mouseState = pygame.mouse.get_pressed()
    mousePos = pygame.mouse.get_pos()
    for event in events:
        if event.type == pygame.QUIT:
            #ens()
            exit()
    if keys[pygame.K_ESCAPE]:
        #ens()
        exit()
    
    k1.draw(window)
    pygame.display.update()
    clock.tick(60)
    