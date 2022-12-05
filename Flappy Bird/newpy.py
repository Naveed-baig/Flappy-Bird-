import pygame
from pygame.locals import *
import random

pygame.init()
clock = pygame.time.Clock()
fps = 50

# creating screen of the game 
width = 600
height = 600
screen = pygame.display.set_mode((width,height))
pygame.display.set_caption("Flappy Bird")

# define fonts
font = pygame.font.SysFont('Bauhaus 93', 60)

# define color
white = (255,255,255)

# Background images 
bg = pygame.image.load("Flappy Bird/img/bg.png")
ground = pygame.image.load("Flappy Bird/img/ground.png")
buttom_img = pygame.image.load("Flappy Bird/img/restart.png")

def draw_text(text,font,text_col,x,y):
    img = font.render(text,True,text_col)
    screen.blit(img,(x,y))

def reset_game():
    pipe_group.empty()
    floppy.rect.x = 100
    floppy.rect.y = int(height/2)
    score = 0
    return score

# Game variables 
bg_scroll = 0
scroll_speed = 4
flying = False
game_over = False
pipe_gap = 150
pipe_frequency = 1500
last_pipe = pygame.time.get_ticks() - pipe_frequency
score = 0
pass_pipe = False

# bird class 
class Bird(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.images = []
        self.index = 0
        self.counter = 0
        for i in range(1,4):
            img = pygame.image.load(f"Flappy Bird/img/bird{i}.png")
            self.images.append(img)
        self.image = pygame.image.load("Flappy Bird/img/bird1.png")
        self.rect = self.image.get_rect()
        self.rect.center = [x,y]
        self.vel = 0
        self.clicked = False
        
        

    def update(self):
        global game_over
        if flying == True:
            # Gravity Creation in game 
            self.vel+=0.3
            if self.vel > 4:
                self.vel = 4
            if self.rect.y < 460:
                self.rect.y += int(self.vel)
            else:
                game_over = True
       
        if game_over == False:
            # Jumping of Bird
            if pygame.mouse.get_pressed()[0]==True and self.clicked == False:
                self.clicked=True
                self.vel += -10
            if pygame.mouse.get_pressed()[0]==False:
                self.clicked = False
            
            
            # Bird Animation 
            self.counter+=1
            flap_cooldown = 5
            if self.counter > flap_cooldown:
                self.counter = 0
                self.index+=1
                if self.index >= len(self.images):
                    self.index = 0
                
            self.image = self.images[self.index]
            self.image = pygame.transform.rotate(self.image,self.vel*-2)
        
        
class Pipe(pygame.sprite.Sprite):
    def __init__(self,x,y,position):
        pygame.sprite.Sprite.__init__ (self)
        self.image = pygame.image.load("Flappy Bird/img/pipe.png")
        self.rect = self.image.get_rect()

        # position 1 is from top , -1 from bottom 
        if position == 1:
            self.image = pygame.transform.flip(self.image,False,True)
            self.rect.bottomleft = [x,y-int(pipe_gap/2)]
        if position == -1:
            self.rect.topleft = [x,y+int(pipe_gap/2)]
    
    def update(self):
        self.rect.x-=scroll_speed
        if self.rect.right < 0:
            self.kill()
         

class Button():
    def __init__(self,x,y,image):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x,y)
    
    def draw(self):
        action = False
        # get mouse position 
        pos = pygame.mouse.get_pos()

        # check if mouse is over the button 
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] ==1 :
                action = True
        # draw button 
        screen.blit(self.image,(self.rect.x,self.rect.y))

        return action
    
bird_group = pygame.sprite.Group()
pipe_group = pygame.sprite.Group()

floppy= Bird(100,int(height/2))
bird_group.add(floppy)


button = Button(width/2-50,height/2-50,buttom_img)





run = True
while run:
    clock.tick(fps)

    screen.blit(bg,(0,0))
    bird_group.draw(screen)
    bird_group.update()
    pipe_group.draw(screen)
    screen.blit(ground,(bg_scroll,500))

    # check the score 
    if len(pipe_group) > 0:
        if bird_group.sprites()[0].rect.left > pipe_group.sprites()[0].rect.left\
        and bird_group.sprites()[0].rect.right < pipe_group.sprites()[0].rect.right\
        and pass_pipe == False:
            pass_pipe = True
        if pass_pipe == True:
            if bird_group.sprites()[0].rect.left > pipe_group.sprites()[0].rect.right:
                score+=1
                pass_pipe = False
        
    draw_text(str(score), font, white,int(width/2), 20)

# Check if the bird has collided with the pipes 
    if pygame.sprite.groupcollide(bird_group, pipe_group, False, False) or floppy.rect.top < 0:
        game_over = True
    
    if game_over == False and flying == True:
        # Generate New pipes 
        time_now = pygame.time.get_ticks()
        if time_now - last_pipe >  pipe_frequency:
            pipe_height = random.randint(-100,100)
            btm_pipe = Pipe(width,int(height/2)+pipe_height,-1)
            top_pipe = Pipe(width,int(height/2)+pipe_height,1)
            pipe_group.add(btm_pipe,top_pipe)
            last_pipe = time_now
            
        # draw and scroll the ground 
        bg_scroll -=scroll_speed
        if bg_scroll < -35:
            bg_scroll = 0

        pipe_group.update()
    else:
        if button.draw():
            game_over = False
            score = reset_game()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN and flying == False and game_over == False:
            flying = True
    
    pygame.display.update()
        
pygame.quit()