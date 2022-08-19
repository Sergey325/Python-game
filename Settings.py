import pygame
from level import Level
from random import randint

class Settings:
    """Класс для хранения всех настроек игры Alien Invasion."""
    def __init__(self):
        """Инициализирует настройки игры."""
        # Параметры экран
        self.screen_width = 1280
        self.screen_height = 720
        self.bg_color = (50, 50, 50)

        self.file = Level()
        self.file.load()
        #настройки уровня
        #self.gun_speed = 3
        #self.enemy_speed = 2
        self.quantity_enemys = self.file.level['quantity_enemys']
        self.save_quantity_enemys = self.quantity_enemys
        self.counter = randint(0,240)
        self.endless = False
        self.index = 0
        self.enemy_speed = 3
        # Параметры оружия
        self.shotting_speed = self.file.gun['shotting_speed']
        self.through_shot = self.file.gun['through_shot']
        self.ammo = self.file.gun['ammo']
        self.save_ammo = self.file.gun['ammo']
        self.reload_time = self.file.gun['reload_time']
        self.gun_x = 0
        self.gun_y = 0
        self.shots_y = self.file.gun['shots_y']
        self.bullet_speed = self.file.gun['bullet_speed']
        self.color_ammoC = (128,128,128)
        self.color_ammoG = (204,172,0)
        self.gunshot = pygame.mixer.Sound(self.file.resource_path(f'sounds/{self.file.gun["gunshot"]}.mp3'))
        self.gunreload = pygame.mixer.Sound(self.file.resource_path(f'sounds/{self.file.gun["gunreload"]}.mp3'))

        self.font_pause = pygame.font.Font(self.file.resource_path('files/PingPong.ttf'), 100)
        self.font_ammo = pygame.font.Font(self.file.resource_path('files/PingPong.ttf'), 40)
        self.font_mid = pygame.font.Font(self.file.resource_path('files/PingPong.ttf'), 70)
        
        self.progress_width = 400
        self.progress_height = 15
        self.progress_insideW = 0
        self.progress_insideH = 11

        self.bonus = 0


