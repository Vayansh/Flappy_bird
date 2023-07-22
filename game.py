import pygame
import random

WIN_HEIGHT = 800
WIN_WIDTH = 1500

BIRD_IMG = [pygame.transform.scale2x(pygame.image.load("imgs/bird1.png")),pygame.transform.scale2x(pygame.image.load("imgs/bird2.png")),pygame.transform.scale2x(pygame.image.load("imgs/bird3.png"))]
PIPE_IMG = pygame.transform.scale2x(pygame.image.load("imgs/pipe.png"))
BASE_IMG = pygame.transform.scale2x(pygame.image.load("imgs/base.png"))
BG_IMG = pygame.transform.scale2x(pygame.image.load("imgs/bg.png"))

pygame.init()
font = pygame.font.Font('arial.ttf', 25)
class Bird:
    IMGS = BIRD_IMG
    MAX_ROT = 20 
    ROT_VEL = 10
    ANIMATION_TIME = 5 
    
    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.tilt = 0
        self.tick_count = 0
        self.vel = 0
        self.height = self.y
        self.img_count = 0
        self.img = self.IMGS[0]

    def jump(self):
        self.vel = -10 
        self.tick_count = 0
        self.height = self.y
        
    def move(self):
        self.tick_count += 1
        
        d = self.vel*self.tick_count + 1.5*self.tick_count**2
        
        if d>16:
            d = 16
        if d<0:
            d -= 2
        
        self.y += d
        if d<0 or self.y <self.height +50:
            if self.tilt < self.MAX_ROT:
                self.tilt = self.MAX_ROT
        else:
            if self.tilt > -90:
                self.tilt -= self.ROT_VEL
        
    def draw(self,win):
        self.img_count +=1
        
        if self.img_count < self.ANIMATION_TIME:
            self.img = self.IMGS[0]
        elif self.img_count < self.ANIMATION_TIME*2:
            self.img = self.IMGS[1]
        elif self.img_count < self.ANIMATION_TIME*3:
            self.img = self.IMGS[2]
        elif self.img_count < self.ANIMATION_TIME*4:
            self.img = self.IMGS[1]
        elif self.img_count == self.ANIMATION_TIME*4 +1:
            self.img = self.IMGS[0]
            self.img_count = 0
        
        if self.tilt <= -80:
            self.img = self.IMGS[1]
            self.img_count = self.ANIMATION_TIME*2
            
        rotated_img = pygame.transform.rotate(self.img,self.tilt)
        new_react = rotated_img.get_rect(center = self.img.get_rect(topleft = (self.x,self.y)).center) 
        win.blit(rotated_img,new_react.topleft)
    
    def get_mask(self):
        return pygame.mask.from_surface(self.img)
    
class Pipe:
    GAP = 200
    VEL = 5
    
    def __init__(self,x):
        self.x = x
        self.height = 0
        
        self.top = 0
        self.bottom = 0
        self.PIPE_TOP = pygame.transform.flip(PIPE_IMG,False,True)
        self.PIPE_BOTTOM = PIPE_IMG
        
        self.set_height()
        self.passed = False
        
    def set_height(self):
        self.height = random.randrange(50,450)
        self.top = self.height - self.PIPE_TOP.get_height()
        self.bottom = self.height + self.GAP
        
    def move(self):
        self.x -= self.VEL
    
    def draw(self,win):
        win.blit(self.PIPE_TOP,(self.x,self.top))
        win.blit(self.PIPE_BOTTOM,(self.x,self.bottom))
        
    def collide(self,bird):
        bird_mask = bird.get_mask()
        top_mask = pygame.mask.from_surface(self.PIPE_TOP)
        bottom_mask = pygame.mask.from_surface(self.PIPE_BOTTOM)
        
        top_offset = (self.x - bird.x, self.top - round(bird.y))
        bottom_offset = (self.x - bird.x , self.bottom - round(bird.y))
        
        b_point = bird_mask.overlap(bottom_mask,bottom_offset)
        t_point = bird_mask.overlap(top_mask,top_offset)
        
        if t_point or b_point:
            return True
        return False
                    
    
class Base:
    VEL = 5
    WIDTH = BASE_IMG.get_width()
    IMG = BASE_IMG
    
    def __init__(self,y):
        self.y = y
        self.x1 = 0
        self.x2 = self.WIDTH
        self.x3 = 2*self.WIDTH
        self.x4 = 3*self.WIDTH
        
    def move(self):
        self.x1 -= self.VEL
        self.x2 -= self.VEL
        self.x3 -= self.VEL
        self.x4 -= self.VEL  
        if self.x1 +self.WIDTH <0:
            self.x1 = self.x4+self.WIDTH
        if self.x2 +self.WIDTH <0:
            self.x2 = self.x1 + self.WIDTH
        if self.x3 + self.WIDTH <0:
            self.x3 = self.x2 + self.WIDTH
        if self.x4 + self.WIDTH <0:
            self.x4 = self.x3 + self.WIDTH
        
            
            
    def draw(self,win):
        win.blit(self.IMG,(self.x1,self.y))
        win.blit(self.IMG,(self.x2,self.y))
        win.blit(self.IMG,(self.x3,self.y))
        win.blit(self.IMG,(self.x4,self.y))
                                        
            
def draw_window(win,bird,pipes,base,score)  :
    win.blit(BG_IMG,(0,0))
    win.blit(BG_IMG,(BG_IMG.get_width(),0))
    win.blit(BG_IMG,(2*BG_IMG.get_width(),0))
    for pipe in pipes:
        pipe.draw(win)
    base.draw(win)    
    bird.draw(win)
    text = font.render("Score : " + str(score),True,(0,0,0))
    win.blit(text,[0,0])
    pygame.display.update()
    
def main():
    bird = Bird(230,350)
    base = Base(720)
    score = 0
    pipes = [Pipe(1600)]
    win = pygame.display.set_mode((WIN_WIDTH,WIN_HEIGHT))
    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(30)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.KEYDOWN:
                    bird.jump()
                    
        bird.move()    
        
        # pipe working
        add_pipe =  False
        rem = []
        for pipe in pipes:
            if pipe.collide(bird):
                run = False
                break
            
            if pipe.x + pipe.PIPE_TOP.get_width() < 0:
                rem.append(pipe)
                
            if not pipe.passed and pipe.x < bird.x:
                pipe.passed = True
                score += 1
                add_pipe = True
            
            pipe.move()
        
        if not add_pipe and pipes[-1].x < 900:
            add_pipe = True
            
        if add_pipe:
            pipes.append(Pipe(1700))
            add_pipe = False
             
                        
        for r in rem:
            pipes.remove(r)

        if bird.y+bird.img.get_height() >= 730:
            run = False
            
        base.move()
        
        draw_window(win,bird,pipes,base,score)                
    pygame.quit()
    print(score)
    quit()

if __name__ == "__main__":
    main()     
    
    
    
     