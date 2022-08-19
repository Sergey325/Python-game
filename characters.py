import pygame
from pygame.sprite import Sprite
#from Settings import Settings
import random

class Char(Sprite):
    """Класс, представляющий одного персонажа"""
    def __init__(self, game):
        super().__init__()
        self.settings = game.settings
        self.screen = game.screen
        self.screen_rect = game.screen.get_rect()
        self.counter = 0
        self.file = game.file

        self.array_img = [[pygame.image.load(self.file.resource_path('images/Characters/char1.png')), 
                            pygame.image.load(self.file.resource_path('images/Characters/char2.png')),
                          pygame.image.load(self.file.resource_path('images/Characters/char3.png')), 
                          pygame.image.load(self.file.resource_path('images/Characters/char4.png')),
                          pygame.image.load(self.file.resource_path('images/Characters/char5.png')), 
                          pygame.image.load(self.file.resource_path('images/Characters/char6.png'))],
                          [pygame.image.load(self.file.resource_path('images/Characters/2char1.png')), 
                          pygame.image.load(self.file.resource_path('images/Characters/2char2.png')),
                          pygame.image.load(self.file.resource_path('images/Characters/2char3.png')), 
                          pygame.image.load(self.file.resource_path('images/Characters/2char4.png')),
                          pygame.image.load(self.file.resource_path('images/Characters/2char5.png')), 
                          pygame.image.load(self.file.resource_path('images/Characters/2char6.png'))],
                          [pygame.image.load(self.file.resource_path('images/Characters/3char1.png')), 
                          pygame.image.load(self.file.resource_path('images/Characters/3char2.png')),
                          pygame.image.load(self.file.resource_path('images/Characters/3char3.png')), 
                          pygame.image.load(self.file.resource_path('images/Characters/3char4.png')),
                          pygame.image.load(self.file.resource_path('images/Characters/3char5.png')), 
                          pygame.image.load(self.file.resource_path('images/Characters/3char6.png'))]]
        self.image = self.array_img[0][0]
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = 0

        self.array_location = [0, 123, 246, 369, 492, 615]
        self.rect.y += random.choice(self.array_location)
        self.rect.x += random.choice(self.array_location)

        self.x = float(self.rect.x)
        
        self.shine = pygame.image.load(self.file.resource_path('images/shine.png'))
        self.b1 = pygame.image.load(self.file.resource_path('images/blood1.png'))
        self.b2 = pygame.image.load(self.file.resource_path('images/blood2.png'))
        self.b3 = pygame.image.load(self.file.resource_path('images/blood3.png'))

        self.arr_blood = [self.b1,self.b2,
                          self.b3]
        self.blood = random.choice(self.arr_blood)

    def update(self):
        if self.settings.endless:
            self.x += self.settings.enemy_speed
        else:
            self.x += self.file.level['enemy_speed']
        self.rect.x = self.x

    def blit_blood(self,rect):
        self.screen.blit(self.blood, rect)

    def blit_enemy(self):
        """Вывод противников на экран."""
        if self.settings.counter == 240:
            self.settings.c = False
            self.settings.counter = 0
        if self.settings.endless:
            self.screen.blit(self.array_img[self.settings.index][self.settings.counter//40], self.rect)
        else :
            self.screen.blit(self.array_img[self.file.level['char']][self.settings.counter//40], self.rect)
        self.settings.counter += 1

    def blit_shine(self, shine_rect):
        self.screen.blit(self.shine, (shine_rect.x + 80, shine_rect.y, shine_rect.w, shine_rect.h))

    def get_rect(self):
        return self.rect