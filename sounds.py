import pygame
from level import Level

class Sounds:
    def __init__(self):
        #pygame.mixer.music.set_volume(0.3)
    
        self.file = Level()
        self.file.load()
        pygame.mixer.music.load(self.file.resource_path('sounds/mortalbackground.mp3'))
        #self.menu = pygame.mixer.Sound('sounds/menu.mp3')
        self.game_over = pygame.mixer.Sound(self.file.resource_path('sounds/gameoverShao.mp3'))
        self.flowless_victory = pygame.mixer.Sound(self.file.resource_path('sounds/flowlessvictory.mp3'))
        self.finish_him = pygame.mixer.Sound(self.file.resource_path('sounds/finish_him.mp3'))
        self.button_press = pygame.mixer.Sound(self.file.resource_path('sounds/button_press.mp3'))
        self.l = self.file.stats['level']
        self.round1 = pygame.mixer.Sound(self.file.resource_path(f'sounds/round{self.l}.mp3'))

    def bg_play(self):
        pygame.mixer.music.play()

    def bg_pause(self):
        pygame.mixer.music.pause()
    def bg_unpause(self):
        pygame.mixer.music.unpause()
    def bg_stop(self):
        pygame.mixer.music.stop()

    def menu_play(self):
        pygame.mixer.music.load(self.file.resource_path('sounds/menu.mp3'))
        pygame.mixer.music.set_volume(1)
        pygame.mixer.music.play()

    def play_sounds(self, sound):
        pygame.mixer.Sound.play(sound)

    def stop_sounds(self, sound):
        pygame.mixer.Sound.stop(sound)