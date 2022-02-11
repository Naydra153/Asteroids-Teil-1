from math import fabs
import pygame
from pygame.draw import circle
from pygame.version import PygameVersion
from random import randint
import os
from math import sin, cos
import math

class Settings:             
    window_width = 1000
    window_height = 800
    path_file = os.path.dirname(os.path.abspath(__file__))
    path_image = os.path.join(path_file, "images")
    fps = 60
    caption = "Spaceship Animationen"
    score = 0


class Background(object):       #erstellt den Hintergrund
    def __init__(self, filename="Garfield 87.png") -> None:
        super().__init__()
        self.image = pygame.image.load(os.path.join(Settings.path_image, filename)).convert()
        self.image = pygame.transform.scale(self.image, (Settings.window_width, Settings.window_height))

    def draw(self, screen):
        screen.blit(self.image, (0, 0))

class Player(pygame.sprite.Sprite):     #erstellt den Spieler
    def __init__(self) -> None:
        super().__init__()
        self.height = 50
        self.width = 50
        self.Raumschiff = "0°Ohne Schiff.png"
        self.image_original = pygame.image.load(os.path.join(Settings.path_image, self.Raumschiff))
        self.image_scaled = pygame.transform.scale(self.image_original, (50, 50))
        self.image = pygame.transform.scale(self.image_original, (self.width, self.height))
        self.color = self.image.get_at((0,0))
        self.image.set_colorkey(self.color)
        self.rect = self.image.get_rect()
        self.rect.centerx = Settings.window_width / 2
        self.rect.centery = Settings.window_height / 2
        self.grad = 0
        self.speed_h = 0
        self.speed_v = 0
  
   

    def rotate_left(self):
        self.old_center = self.rect.center
        self.image = pygame.transform.rotate(self.image_scaled, self.grad)
        self.grad += 22.5
        self.rect = self.image.get_rect()
        self.rect.center = self.old_center

    
    def rotate_right(self):
        self.old_center = self.rect.center
        self.image = pygame.transform.rotate(self.image_scaled, self.grad)
        self.grad -= 22.5
        self.rect = self.image.get_rect()
        self.rect.center = self.old_center


    def Gas(self):
        self.rechnung()
        self.speed_h = self.speed_h - sin(self.grad_rechnung)  
        self.speed_v = self.speed_v - cos(self.grad_rechnung)

    def rechnung(self):
        self.grad_rechnung = 0
        self.grad_rechnung = (math.pi/180) * self.grad
 
    def draw(self, screen): 
        screen.blit(self.image, self.rect)

    def update(self):       
        self.rect.move_ip((self.speed_h, self.speed_v))
        if self.speed_h >= 10:
            self.speed_h = 10
        if self.speed_v >= 10:
            self.speed_v = 10
        if self.speed_h <= -10:
            self.speed_h = -10
        if self.speed_v <= -10:
            self.speed_v = -10

        if self.rect.top <= 0:
            self.rect.centery += Settings.window_height
        
        if self.rect.left <= 0:
            self.rect.centerx += Settings.window_width

        if self.rect.right >= Settings.window_width:
            self.rect.centery -= Settings.window_height

        if self.rect.bottom >= Settings.window_height:
            self.rect.centerx -= Settings.window_height

class Game(object):
    def __init__(self) -> None:
        super().__init__()
        os.environ['SDL_VIDEO_WINDOW_POS'] = "650,30"
        pygame.init()      
        pygame.display.set_caption(Settings.caption)
        self.screen = pygame.display.set_mode((Settings.window_width,Settings.window_height))
        self.clock = pygame.time.Clock()
        self.running = False
        self.players = pygame.sprite.GroupSingle()
        self.player = Player()
        self.background = Background()

    def start(self):    
            self.players.add(Player())


     
    def update(self):
        self.player.update()
        
    def draw(self):
        self.background.draw(self.screen)
        self.player.draw(self.screen)
        pygame.display.flip()

    
    def run(self):
        self.running = True
        self.start()
        self.update()
        while self.running:
            self.clock.tick(Settings.fps)
            self.watch_for_events()
            self.update()
            self.draw()
        pygame.quit()

    def watch_for_events(self):  
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                elif event.key == pygame.K_DOWN:
                    pass
                elif event.key == pygame.K_UP:
                    Player.Gas(self.player)
                elif event.key == pygame.K_LEFT:
                    Player.rotate_left(self.player)
                elif event.key == pygame.K_RIGHT:
                    Player.rotate_right(self.player)
                 

            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_DOWN:
                    pass
                elif event.key == pygame.K_UP:
                    pass
                elif event.key == pygame.K_LEFT:
                    pass
                elif event.key == pygame.K_RIGHT:
                    pass

       

if __name__ == "__main__":

    game = Game()
    game.run()
