import os
import pygame
import random
import math
import time
import json
from playsound import playsound
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

sound1 = pygame.mixer.Sound('womp-womp.mp3')

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

sound0 = pygame.mixer.Sound('tata.wav')
clock = pygame.time.Clock()
WIDTH,HEIGHT = 1200,765
window = pygame.display.set_mode((WIDTH,HEIGHT))
def highlight(width,height,x,y,mousePos):
    if mousePos[0] > x and mousePos[0] < x + width and mousePos[1] > y and mousePos[1] < y + height:
        return True
    else:
        return False

def button_colision(width,height,x,y,mousePos,mouseState):
    if mousePos[0] > x and mousePos[0] < x + width and mousePos[1] > y and mousePos[1] < y + height and mouseState[0] == True:
        return True
    else:
        return False

fd = 0
class health:
    def __init__(self):
        self.x = 20
        self.y = 20
        self.img = pygame.image.load('frame.png')
        self.scale = 0.2
        self.width = self.img.get_width()*self.scale
        self.height = self.img.get_height()*self.scale
        self.scaled_img = pygame.transform.scale(self.img, (self.width, self.height))
        
        self.img1 = pygame.image.load('ex.png')
        self.width1 = self.img1.get_width()*(self.scale+0.1)
        self.height1 = self.img1.get_height()*(self.scale+0.1)
        self.scaled_img1 = pygame.transform.scale(self.img1, (self.width1, self.height1))

        self.img2 = pygame.image.load('avatar.png')
        self.scale = 4
        self.width2 = self.img2.get_width()*self.scale
        self.height2 = self.img2.get_height()*self.scale
        self.scaled_img2 = pygame.transform.scale(self.img2, (self.width2, self.height2))
    def draw(self,hp):
        global window
        window.blit(self.scaled_img2,(self.x+30,self.y+30))
        pygame.draw.rect(window,"green",pygame.Rect(self.x+self.width-10,self.y+65,hp*55,60))
        for i in range(hp):
            pygame.draw.rect(window,"black",pygame.Rect( self.x+ self.width-20+i*55,self.y+25+40,10,60))
        window.blit(self.scaled_img1,(self.x+self.width-10,self.y+40))
        window.blit(self.scaled_img,(self.x,self.y))
h1 = health()
class pozadina:
    def __init__(self):
        self.img = pygame.image.load('main_menu.png')
        self.scale = 0.851
        self.scale = 1.3
        self.width = self.img.get_width()*self.scale
        self.height = self.img.get_height()*self.scale
        self.scaled_img = pygame.transform.scale(self.img, (self.width, self.height))
    def update(self,x,e):
        self.scale = e
        self.width = x.get_width()*self.scale
        self.height = x.get_height()*self.scale
        self.scaled_img = pygame.transform.scale(x, (self.width, self.height))
    def draw(self):
        global window
        global screen
        #if screen == 50:
        #    self.img = pygame.image.load('death.png')
        if screen == 50:
            window.blit(self.scaled_img,(-100,0))
        else:
            window.blit(self.scaled_img,(0,0))
countdown = 0
class Knight:
    def __init__(self,x,y,dx,dy,hp):
        self.x = x
        self.y = y
        self.dx = dx
        self.dy = dy
        self.scale = 1.6
        self.coldow = 0
        self.sprite_img = pygame.image.load('idle.png')
        self.width = self.sprite_img.get_width()*self.scale
        self.height = self.sprite_img.get_height()*self.scale
        self.scaled_img = pygame.transform.scale(self.sprite_img, (self.width, self.height))
        self.width = self.scaled_img.get_width()
        self.height = self.scaled_img.get_height()
        self.immobilis = 0
        self.xc1 = 0
        self.last_direction = 1
        self.state = 3
        self.jump = 0
        self.cooldown = 0
        self.airattack = 0
        self.hp = hp
    def end_(self):
        global screen
        global countdown
        screen = 50
        countdown = 300
    def checker(self,kx,kwidth):
        minus_g = 0
        if self.x+self.width>= kx and self.x<kx and self.last_direction == 1 or self.x <= kx+kwidth and self.x>kx and self.last_direction == -1:
            minus_g += 1
        return minus_g
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
        if self.xc1 == 1:
            if self.last_direction == 1:
                self.sprite_img = pygame.image.load('idle.png')
            else:
                self.sprite_img = pygame.image.load('idle_l.png')
        
        if self.sprite_img == pygame.image.load('idle.png') or self.sprite_img == pygame.image.load('idle_l.png'):
            self.state =3
            
            
        self.width = self.sprite_img.get_width()*self.scale
        self.height = self.sprite_img.get_height()*self.scale
        self.scaled_img = pygame.transform.scale(self.sprite_img, (self.width, self.height))
        window.blit(self.scaled_img,(self.x,self.y))
        if self.immobilis<=120 and self.immobilis>= 90:
            self.y += 40        
    def move(self,minus):
        global screen
        if self.coldow>0:
            self.coldow-=1
        cv = 0
        cx = 0
        if screen==2 or screen == 3:
            cv = 180
            cx = 300
        global WIDTH
        global HEIGHT
        global mouseState
        global keys
        self.hp -= minus
        if self.hp <= 0:
            self.end_()
        if self.jump == 0:
            self.dx = 0
            self.dy = 0
        self.move_l = False
        self.move_r = False
        if self.xc1 == 0:
            if self.immobilis==0 and self.jump == 0:
                if self.x >=27.5:
                    if keys[pygame.K_a] or keys[pygame.K_LEFT]:
                        self.dx = -2.5
                        self.move_l =True
                        self.move_r = False
                        if self.airattack == 0 and self.jump == 0:
                            self.last_direction = -1
                        if self.state == 3:
                            self.state = 180
                        
                if self.x <= WIDTH-230-cv-27.5:
                    if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
                        self.dx = 2.5
                        self.move_l =False
                        self.move_r = True
                        if self.airattack == 0 and self.jump == 0:
                            self.last_direction = 1
                        if self.state == 3:
                            self.state = 180
        if self.jump == 0:
            self.y = 550-cx
            if self.cooldown == 0:
                if self.immobilis == 0:
                    if keys[pygame.K_SPACE]:
                        self.jump = 50
        
        if self.immobilis == 0:
            if self.coldow == 0:
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
        
        if self.xc1 == 0:
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
        self.xc1 = 0
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
        self.hp = 1
    def draw(self,window,sc):
        if sc == 4 or sc == 0:
            if self.hp == 1:
                if self.state == 0:
                    self.state = 180
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
    def move(self,kx,kwidth,sc):
        if sc == 4 or sc == 0:
            if self.hp == 1:
                minus = 0
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
                if self.attack > 0:
                    self.attack-=1
                if self.attack == 0:
                    if self.x+self.width>= kx and self.x<kx and self.last_direction == 1 or self.x <= kx+kwidth and self.x>kx and self.last_direction == -1:
                        self.attack = 205
                if self.attack == 75:
                    if self.x+self.width>= kx and self.x<kx and self.last_direction == 1 or self.x <= kx+kwidth and self.x>kx and self.last_direction == -1:
                        minus += 1
                self.x += self.dx
                return minus
class Button:
    def __init__(s,x,y,text,scren_c):
        s.text = text
        s.x = x
        s.y = y
        s.dx = 0
        s.dy = 0
        s.sx = scren_c
        s.font = pygame.font.SysFont('The Black Knight',70)
        s.text_surface = s.font.render(f"{s.text}", True, (255, 255, 255))
        s.width,s.height = s.font.size(s.text)
    def draw(s,window):
        window.blit(s.text_surface,(s.x+s.dx,s.y+s.dy))
        s.dx=0
        s.dy=0
    def checker(s,mousePos,mouseState,scr):
        if highlight(s.width,s.height,s.x,s.y,mousePos):
            s.font = pygame.font.SysFont('The Black Knight',90)
            s.text_surface = s.font.render(f"{s.text}", True, (255, 255, 255))
            s.dx = -30
            s.dy = 0
            if mouseState[0] == True:
                scr = s.sx
                if s.sx == 0:
                    p1.update(pygame.image.load('haunt.png'),0.851)
                    k1.coldow = 10
                if s.sx == 4:
                    p1.update(pygame.image.load('level_1.png'),1.35)
                    k1.coldow = 10
        else:
            s.font = pygame.font.SysFont('The Black Knight',70)
            s.text_surface = s.font.render(f"{s.text}", True, (255, 255, 255))
        return scr
    
l_b = [Button(425,250,"---Start Over---",4),Button(425,400,"----Continue----",4)]

def scroll(window,x,y):
    img = pygame.image.load('scroll.png')
    scale = 0.3
    width = img.get_width()*scale
    height = img.get_height()*scale
    scaled_img = pygame.transform.scale(img, (width, height))
    window.blit(scaled_img,(x,y))

def wrant(window,x,y,scale):
    x_=pygame.image.load('key_up.png')
    width = x_.get_width()*scale
    height = x_.get_height()*scale
    scaled_img = pygame.transform.scale(x_, (width, height))
    window.blit(scaled_img,(x,y))
    
def check():
    hp_minus = 0
    global screen
    for i in range(len(l_g)):
        h = 0
        if k1.immobilis == 89 or k1.airattack==25:
            minus_g = k1.checker(l_g[i].x,l_g[i].width)
            l_g[i].hp -= minus_g
            minus_g = 0
        h = l_g[i].move(k1.x,k1.width,screen)
        if h == None:
            h = 0
        hp_minus+=h
    return hp_minus

def thought(text,text1,k,x,y):
    scale = 0.8
    img = pygame.image.load('thought.png')
    width = img.get_width()*scale
    height = img.get_height()*scale
    scaled_img = pygame.transform.scale(img, (width, height))
    x = x+k.width-75
    y = y-height
    
    
    font = pygame.font.SysFont('The Black Knight',25)
    text_surface = font.render(f"{text}", True, (0,0,0))
    window.blit(scaled_img,(x,y))
    window.blit(text_surface,(x+30,y+25))
    if text1 != 0:
        text_surface = font.render(f"{text1}", True, (0,0,0))
        window.blit(text_surface,(x+30,y+50))
    k1.last_direction = -1
    k.xc1 = 1
hp_minus = 0
alldead = False
cooldown = 0
l_g = []
img = pygame.image.load('cry.png')
scale = 0.4
width = img.get_width()*scale
height = img.get_height()*scale
img = pygame.transform.scale(img, (width,height))
p1 = pozadina()
sc2 = 0
k1 = Knight(100,550,0,0,5)
screen = 1
d = 0

gg = 0
bbbb = 0
qqq = 0
c = 0
minus_g = 0
while True:
    if screen == 4:
        window.fill("Blue")
        p1.draw()
        keys = pygame.key.get_pressed()
        events = pygame.event.get()
        mouseState = pygame.mouse.get_pressed()
        mousePos = pygame.mouse.get_pos()
        for event in events:
            if event.type == pygame.QUIT:
                screen=1
                l_b[1].sx = 4
                cooldown = 30
                p1.update(pygame.image.load('main_menu.png'),1.3)
        if keys[pygame.K_ESCAPE]:
            screen = 1
            cooldown = 30
            l_b[1].sx = 4
            p1.update(pygame.image.load('main_menu.png'),1.3)
        window.blit(img,(400,600))
        hp_minus = check()
        k1.move(hp_minus)
        k1.draw(window)
        if k1.x >= 300 and k1.x<= 500:
            if bbbb!=-1 and bbbb>=0:
                wrant(window,400,450,0.2)
                if keys[pygame.K_w] or keys[pygame.K_UP]:
                    bbbb =100
        if bbbb >=2:
            thought('HELP!',0,k1,300+width,600)
            if k1.x <= 400:
                k1.x = 225
                k1.last_direction = 1
            else:
                k1.x = 525
                k1.last_direction = -1
            bbbb-=1
        if qqq == 0:
            if bbbb ==1:
                l_g.append(Goblin(900,610,0,0,1))
                qqq = 1
                
        if bbbb == 1:
            if l_g[0].hp == 0:
                bbbb = -301
            
        if k1.x >= 300 and k1.x<= 500:
            if bbbb == -301:
                wrant(window,400,450,0.2)
                if keys[pygame.K_w] or keys[pygame.K_UP]:
                    bbbb =-100
                    
                    
        if bbbb <= -2 and bbbb> -301:
            thought('Find the source!',0,k1,300+width,600)
            if k1.x <= 400:
                k1.x = 225
                k1.last_direction = 1
            else:
                k1.x = 525
                k1.last_direction = -1
            bbbb+=1
            
            
        if k1.x >= 815 and k1.x<= 945:
            if bbbb == -1:
                wrant(window,875,450,0.2)
                if keys[pygame.K_w] or keys[pygame.K_UP]:
                    screen = 0
                    l_g = []
                    sc2 = 0
                    k1.hp = 5
                    k1 = Knight(100,550,0,0,5)
                    p1.update(pygame.image.load('haunt.png'),0.851)
        
        
        for i in range(len(l_g)):
            l_g[i].draw(window,screen)
        h1.draw(k1.hp)
        
    
    
    
    if screen == 3:
        window.fill("Blue")
        p1.draw()
        keys = pygame.key.get_pressed()
        events = pygame.event.get()
        mouseState = pygame.mouse.get_pressed()
        mousePos = pygame.mouse.get_pos()
        if gg<=1:
            for event in events:
                if event.type == pygame.QUIT:
                    screen=2
                    l_b[1].sx = 3
                    cooldown = 30
                    p1.update(pygame.image.load('haunted_room1.png'),4.6)
            if keys[pygame.K_ESCAPE]:
                screen =2
                cooldown = 30
                l_b[1].sx = 3
                p1.update(pygame.image.load('haunted_room1.png'),4.6)
        hp_minus = check()
        k1.move(hp_minus)
        scroll(window,650,350)
        k1.draw(window)
        if k1.x >= 750 and k1.x<=900:
            wrant(window,650,200,0.3)
            if keys[pygame.K_UP] or keys[pygame.K_w]:
                gg = 150
        if gg >=2:
            k1.last_direction = -1
            thought("The king is",'the source',k1,k1.x,k1.y)
            gg-=1
    
    
    if screen == 2:
        sound0.stop()
        window.fill("Blue")
        p1.draw()
        keys = pygame.key.get_pressed()
        events = pygame.event.get()
        mouseState = pygame.mouse.get_pressed()
        mousePos = pygame.mouse.get_pos()
        for event in events:
            if event.type == pygame.QUIT:
                if cooldown ==0:
                    k1 = Knight(100,550,0,0,5)
                    k1.coldow = 10
                    sc2 = 0
                    screen=0
                    l_b[1].sx = 2
                    cooldown
                    p1.update(pygame.image.load('haunt.png'),0.851)
        if keys[pygame.K_ESCAPE]:
            if cooldown == 0:
                screen =0
                l_b[1].sx = 2
                p1.update(pygame.image.load('haunt.png'),0.851)
                k1 = Knight(100,550,0,0,5)
                k1.coldow = 10
                sc2 = 0
                cooldown = 30
        hp_minus = check()
        k1.move(hp_minus)
        k1.draw(window)
        if d== 0:
            if k1.x>100 and k1.x<350:
                wrant(window,325,115,0.4)
                if keys[pygame.K_w] or keys[pygame.K_UP]:
                    d = 151
        if d>=2:
            thought('I will be safe',' ... I think.',k1,k1.x,k1.y)
        if d>=2:
            d-=1
        if d == 1:
            if k1.x>625 and k1.x<725:
                wrant(window,680,115,0.4)
                if keys[pygame.K_w] or keys[pygame.K_UP]:
                    screen = 3
                    k1 = Knight(100,150,0,0,5)
                    k1.scale = 3
                    p1.update(pygame.image.load('haunted_room2.png'),4.6)
        if cooldown>=1:
            cooldown-=1



    if screen == 50:
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
        if countdown == 300:
            p1.update(pygame.image.load('death.png'),2.2)
        if countdown == 0:
            screen = 1
            p1.update(pygame.image.load('main_menu.png'),1.3)
        sound0.stop()
        if countdown == 300:
            sound1.play()
        countdown-=1
        
        
    if screen == 0:
        a = random.randint(1,100)
        if sc2 <= 24:
            if k1.coldow == 0:
                if a == 1:
                    sc2+=1
                    x_a = random.randint(100,900)
                    if len(l_g) == 100:
                        l_g[0] = Goblin(x_a,610,0,0,1)
                    else:
                        g = Goblin(x_a,610,0,0,1)
                        l_g.append(g)


        sound0.play()
        h = 0
        window.fill("Blue")
        p1.draw()
        keys = pygame.key.get_pressed()
        events = pygame.event.get()
        mouseState = pygame.mouse.get_pressed()
        mousePos = pygame.mouse.get_pos()
        if cooldown == 0:
            for event in events:
                if event.type == pygame.QUIT:
                    screen=1
                    d = 0
                    gg = 0
                    bbbb = 0
                    qqq = 0
                    c = 0
                    l_b[1].sx = 0
                    cooldown = 30
                    p1.update(pygame.image.load('main_menu.png'),1.3)
            if keys[pygame.K_ESCAPE]:
                screen = 1
                l_b[1].sx = 0
                d = 0
                gg = 0
                bbbb = 0
                qqq = 0
                c = 0
                cooldown = 30
                p1.update(pygame.image.load('main_menu.png'),1.3)
            
            
        hp_minus = check()
        k1.move(hp_minus)
        for i in range(len(l_g)):
            l_g[i].draw(window,screen)
        k1.draw(window)
        h1.draw(k1.hp)
        if sc2==25:
            alldead = True
            if c == 0:
                for i in range(len(l_g)):
                    if l_g[i].hp == 1:
                        alldead==False
            if alldead == True:
                c = 1
            if k1.x>=650 and k1.x<=835:
                if c == 1:
                    wrant(window,750,425,0.2)
                    if keys[pygame.K_w] or keys[pygame.K_UP]:
                        if gg == 0:
                            screen = 2
                            p1.update(pygame.image.load('haunted_room1.png'),4.6)
                            k1 = Knight(100,150,0,0,5)
                            k1.scale = 3
                            l_g=[]
                         
                            
        if cooldown>=1:
            cooldown -= 1

            
    if screen == 1:
        sound0.stop()
        window.fill("Blue")
        p1.draw()
        keys = pygame.key.get_pressed()
        events = pygame.event.get()
        mouseState = pygame.mouse.get_pressed()
        mousePos = pygame.mouse.get_pos()
        for event in events:
            if event.type == pygame.QUIT:
                if cooldown == 0:
                    exit()
        if keys[pygame.K_ESCAPE]:
            if cooldown ==0:
                exit()
        for i in range(len(l_b)):
            screen = l_b[i].checker(mousePos,mouseState,screen)
            if screen == 0:
                    k1 = Knight(100,550,0,0,5)
                    k1.coldow = 10
                    l_g = []
                    sc2 = 0
            if screen == 2:
                p1.update(pygame.image.load('haunted_room1.png'),4.6)
                k1 = Knight(100,150,0,0,5)
                k1.scale = 3
            if cooldown>=1:
                cooldown -= 1
            l_b[i].draw(window)
    pygame.display.update()
    clock.tick(60)
    