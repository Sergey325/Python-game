import pygame
import time
from gun import Gun
#from Settings import *
from pygame.sprite import Sprite

class Bullet(Sprite):
    """Класс для управления снарядами, выпущенными кораблем."""
    def __init__(self, game):
        """Создает объект снарядов в текущей позиции корабля."""
        super().__init__()
        self.screen = game.screen
        self.screen_rect = game.screen.get_rect()
        self.settings = game.settings
        #self.color = self.settings.bullet_color
        self.file = game.file
        #self.gun = Gun(self)
        self.shots = pygame.image.load(self.file.resource_path('images/shot1.png'))
        self.rect_shot = self.shots.get_rect()
        self.rect_shot.topleft = game.gun.rect.topleft
        self.rect_shot.x -= 40
        self.rect_shot.y += self.settings.gun_y
        self.recty = 0
        self.array_bullets = [pygame.image.load(self.file.resource_path('images/guns/BulletC.png')), pygame.image.load(self.file.resource_path('images/guns/BulletG.png'))]

        # Создание снаряда в позиции (0,0) и назначение правильной позиции.
        if self.file.stats['gun'][self.file.g-1].endswith('G'):
            self.image = self.array_bullets[1]
        else : self.image = self.array_bullets[0]
        if self.image == self.array_bullets[1]:
            self.settings.through_shot = True
        self.rect = self.image.get_rect()
        self.rect.topleft = game.gun.rect.topleft
        self.rect.x -= 40
        self.rect.y += self.settings.gun_y
        self.x = float(self.rect.x)
        self.y = float(self.rect.x)

        self.shotting = False

    def shot(self):
        if self.shotting:
            return True

    def update(self, y):
        # Обновление позиции снаряда в вещественном формате.
        self.x -= self.file.gun['bullet_speed']+6
        self.rect.x = self.x
        self.rect_shot.y = y+self.settings.shots_y

    def blitme(self):
        """Вывод снаряда на экран."""
        self.screen.blit(self.image, self.rect)
        self.recty = self.rect.y
        if self.rect.x>940:
            self.screen.blit(self.shots, self.rect_shot)
