import pygame
from sounds import Sounds

class Buttons:
    def __init__(self, game, width, height):
        self.sound = Sounds()
        self.width = width
        self.height = height
        self.screen = game.screen
        self.settings = game.settings
        self.file = game.file
        self.check = False

    def draw_buttons(self, x, y, message, size_text, action = None, color_innactive = (128,128,128)):
        self.mouse = pygame.mouse.get_pos()
        self.click = pygame.mouse.get_pressed()
        self.rect = (x, y, self.width, self.height)
        self.font_text = pygame.font.Font(self.file.resource_path('files/PingPong.ttf'), size_text)
        if x < self.mouse[0] < x + self.width and y < self.mouse[1] < y + self.height:
            self.check = True
            self.text = self.font_text.render(message, True, color_innactive)
            #pygame.draw.rect(self.screen, (69,69,69), self.rect)
            if self.click [0] == 1:
                self.sound.play_sounds(self.sound.button_press)
                pygame.time.delay(300)
                if action is not None:
                    action()
        else:
            self.check = False
            #pygame.draw.rect(self.screen, (69,69,69), self.rect)
            self.text = self.font_text.render(message, True, (255, 255, 255))
        self.rect_text = self.rect

        self.screen.blit(self.text, self.rect_text)

    def draw_gun(self, x, y, gun, action = None):
        self.mouse = pygame.mouse.get_pos()
        self.click = pygame.mouse.get_pressed()
        self.rect = (x, y, self.width, self.height)