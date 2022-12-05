
import pygame
from pygame.locals import *
import random

pygame.init()

clock = pygame.time.Clock()
fps = 60

screen_width = 400
screen_height = 600
screen = pygame.display.set_mode((screen_width,screen_height))
pygame.display.set_caption("Flappy Bird")

# game variables
ground_scroll = 0
scroll_speed = 4
flying = False
game_over = False
pipe_gap = 150
pipe_frequency = 1500
last_pipe = pygame.time.get_ticks()

# loading images 
bg = pygame.image.load('Flappy Bird/img/bg.png')
ground = pygame.image.load('Flappy Bird/img/ground.png')

class Bird(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.images = []
        self.index = 0 
        self.counter = 0
        for i in range(1,4):
            img = pygame.image.load(f'Flappy Bird/img/bird{i}.png')
            self.images.append(img)

        self.image = pygame.image.load('Flappy Bird/img/bird1.png')
        self.rect = self.image.get_rect()
        self.rect.center = [x,y]
        self.vel = 0
        self.clicked = False
    
    def update(self):
        if flying == True:
            # Adding Gravity effects 
            self.vel+=0.5
            if self.vel > 8:
                self.vel = 8
            if self.rect.y < 435:
                self.rect.y += int(self.vel)
        if game_over == False:
            # Jumping of Bird 
            if pygame.mouse.get_pressed()[0] == 1:
                self.vel = -10

            
            # handle the animation
            self.counter +=1
            flap_cooldown=5

            if self.counter > flap_cooldown:
                self.counter = 0
                self.index +=1
                if self.index >= len(self.images):
                    self.index = 0
            self.image = self.images[self.index]

            self.image = pygame.transform.rotate(self.images[self.index], self.vel*-2)
        else:
            self.image = pygame.transform.rotate(self.images[self.index], -90)

class Pipe(pygame.sprite.Sprite):
    def __init__(self,x,y,position):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("Flappy Bird/img/pipe.png")
        self.rect = self.image.get_rect()
        
        if position == -1:
            self.image = pygame.transform.flip(self.image,False,True)
            self.rect.bottomleft = [x,y-int(pipe_gap/2)]
        if position == 1:
            self.rect.topleft = [x,y+int(pipe_gap/2)]


    def update(self):
        self.rect.x -=scroll_speed


# Bird Group 
bird_group = pygame.sprite.Group()
flappy = Bird(100,int(screen_height/2))
bird_group.add(flappy)

pipe_group = pygame.sprite.Group()







run = True
while run:
    clock.tick(fps)
# Background  Image
    screen.blit(bg, (0,0))
# Bird Group 
    bird_group.draw(screen)
    bird_group.update()

#Pipe Group 
    pipe_group.draw(screen)
# Ground Image 
    screen.blit(ground,(ground_scroll,470))

# check for collisions 
if pygame.sprite.groupcollide(bird_group, pipe_group, False, False):
    game_over = True

# check if bird has hit the ground 
    if flappy.rect.bottom > 470:
        game_over = True
        flying = False


    if game_over == False and flying == True:
        # Generate pipes 
        New_time = pygame.time.get_ticks()
        if New_time - last_pipe > pipe_frequency:
            pipe_height = random.randint(-100, 100)
            pipe_top = Pipe(screen_width,int(screen_height/2)+pipe_height,1)
            pipe_bottom = Pipe(screen_width,int(screen_height/2)+pipe_height,-1)
            pipe_group.add(pipe_top)
            pipe_group.add(pipe_bottom)
            last_pipe = New_time


    # Moving the ground 
        ground_scroll-=scroll_speed
        if ground_scroll < -35:
            ground_scroll = 0
        pipe_group.update()


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN and flying ==False and game_over == False:
            flying = True
        
    pygame.display.update()


pygame.quit()