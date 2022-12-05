import pygame
from pygame.locals import *
import random

pygame.init()

# screen dimension 
s_width = 800
s_height = 400
clock = pygame.time.Clock()
fps = 60
screen = pygame.display.set_mode((s_width,s_height))

# loading images 
bg = pygame.image.load('img/bg.png')
ground = pygame.image.load('img/ground.png')

# constant variables 
bg_scroll = 0
scroll_speed = 4
GRAVITY = 0.5
pipe_gap = 150
pipe_frequency = 1500 # milliseconds
last_pipe = pygame.time.get_ticks()-pipe_frequency


class Bird(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.images = []
        self.index = 0
        self.counter = 0
        self.vel = 0
        self.fly = False
        self.btn_press = False
        for i in range(1,4):
            img = pygame.image.load(f'img/bird{i}.png')
            self.images.append(img)
        
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
    
    def update(self):
        if self.rect.y < s_height - 80:
            # animation for the bird 
            self.counter+=1 
            if self.counter > 5:
                self.counter = 0
                self.index +=1 
    
    
            if self.index >= len(self.images):
                self.index = 0

            if self.btn_press:
                # Adding gravity 
                self.vel += GRAVITY
                if self.vel > 5:
                    self.vel = 5
                
            # setting the bird to fly when player press spaceBar
            if self.fly:
                self.vel -= 11
                self.fly = False

        # game over when bird hit the ground 
        if self.rect.y > s_height - 80 :
            self.rect.y = s_height - 80
            
        
        # setting bird's vertical position 
        self.rect.y += self.vel
        

        self.image = self.images[self.index]
        

class Pipe(pygame.sprite.Sprite):
    def __init__(self,x,y,direction):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('img/pipe.png')
        self.rect = self.image.get_rect()
        rand_pipe = random.randint(-50, 50)
        if direction == 1: 
            self.rect.topleft = (x,y+int(pipe_gap/2)+rand_pipe)
        elif direction == -1:
            self.image = pygame.transform.rotate(self.image, 180)
            self.rect.bottomleft  = (x,y-int(pipe_gap//2)+rand_pipe)
    
    def update(self):
        self.rect.x-=scroll_speed
        if self.rect.right < 0:
            self.kill()
        

# sprite groups 
bird_group = pygame.sprite.Group()
pipe_group = pygame.sprite.Group()

# instances 
flappy = Bird(200, 150)


bird_group.add(flappy)


run = True
while run:
    # frame rate set to 60 fps 
    clock.tick(fps)

    # screen 
    screen.blit(bg, (0,0))

    # updating and drawing bird group 
    bird_group.update()
    bird_group.draw(screen)

    # drawing and updating pipe group 
    pipe_group.update()
    pipe_group.draw(screen)

    # bliting ground image 
    screen.blit(ground,(bg_scroll,s_height-35))

    # scrolling the ground 
    if flappy.rect.y < s_height - 80:
        # generate pipes 
        if flappy.btn_press: # when player press spaceBar only then game starts
            time_now = pygame.time.get_ticks()
            if time_now - last_pipe > pipe_frequency:
                pipe = Pipe(800, 200, 1) # downward pipe
                pipe2 = Pipe(800, 200, -1) # upward pipe
                pipe_group.add(pipe,pipe2)

                last_pipe = time_now
            # ground scroll 
            bg_scroll -= scroll_speed
            if abs(bg_scroll) > 35 :
                bg_scroll = 0
    else:
        scroll_speed = 0


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                flappy.fly = True
                flappy.btn_press = True
    
        # if event.type == pygame.KEYUP:
        #     if event.key == pygame.K_SPACE:
        #         flappy.fly = False

    pygame.display.update()

pygame.quit()