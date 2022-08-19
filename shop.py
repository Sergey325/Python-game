import pygame
from buttons import Buttons
import time

class Shop:
    def __init__(self, game):
        self.settings = game.settings
        self.screen = game.screen
        self.screen_rect = game.screen.get_rect()
        self.sounds = game.sounds
        self.file = game.file
        self.gun = game.gun

        self.text_counter = 0
        self.shop = False
        self.text_shop1 = self.settings.font_mid.render('buy', True, (255,255,255))
        self.cost = 0
        self.text_c = False
        '''self.arr_guns = [pygame.image.load('images/guns/glock.png'), pygame.image.load('images/guns/Desert_eagle.png'),
                        pygame.image.load('images/guns/AK-47.png'), pygame.image.load('images/guns/m-16.png'), 
                        pygame.image.load('images/guns/ASval'), pygame.image.load('images/guns/VSS.png'), pygame.image.load('images/guns/ASvalG.png')]'''
        self.glock = pygame.image.load(self.file.resource_path('images/guns/glockshop.png'))
        self.rect_glock = self.glock.get_rect()
        self.desert_eagle = pygame.image.load(self.file.resource_path('images/guns/Desert_eagleshop.png'))
        self.rect_desert_eagle = self.desert_eagle.get_rect()
        self.ak47 = pygame.image.load(self.file.resource_path('images/guns/AK-47shop.png'))
        self.rect_ak47 = self.ak47.get_rect()
        self.m16 = pygame.image.load(self.file.resource_path('images/guns/m-16shop.png'))
        self.rect_m16 = self.m16.get_rect()
        self.ASval = pygame.image.load(self.file.resource_path('images/guns/ASvalshop.png'))
        self.rect_ASval = self.ASval.get_rect()
        self.VSS = pygame.image.load(self.file.resource_path('images/guns/VSSshop.png'))
        self.rect_VSS = self.VSS.get_rect()
        self.ASvalG = pygame.image.load(self.file.resource_path('images/guns/ASvalGshop.png'))
        self.rect_ASvalG = self.ASvalG.get_rect()

        self.text_false = self.settings.font_ammo.render("You don't have enough funds!", True, (255,0,0))
        self.rect_text_false = self.screen.get_rect(
            center = (self.screen_rect.center))
        self.coin = pygame.image.load(self.file.resource_path('images/coinshop.png'))
        self.rect_coin = self.coin.get_rect()

        self.button_yes = Buttons(self, 60,35)
        self.button_no = Buttons(self, 50,35)

    def blit_text(self, text, rect):
        self.screen.blit(text, rect)
        self.text_counter += 1
        if self.text_counter == 200:
                self.text_counter = 0
                self.text_c = False

    def _buying(self):
        self.file.stats['gold'] -= self.cost
        self.file.stats['gun'].append(self.name)
        self.file.save_stats()
        self.file.load()
        self._break_shop()

    def _break_shop(self):
        self.shop = False

    def _shopping(self):
        pygame.draw.rect(self.screen, (0,0,0), (490,250,300,200))
        length1 = self.text_shop1.get_rect()
        length2 = self.text_shop2.get_rect()
        x1 = (300-length1[2])/2+490
        x2 = (300-length2[2])/2+490
        self.blit_text(self.text_shop1, (x1, 250))
        self.blit_text(self.text_shop2, (x2, 330))
        self.button_yes.draw_buttons(525,400,'Yes', 40, self._buying,(255,0,0))
        self.button_no.draw_buttons(700,400,'No', 40, self._break_shop, (255,0,0))

    def blit_shop(self):
        self._blit_guns(self.glock, 200, 100, self.rect_glock, 0, 'glock')
        self._blit_guns(self.desert_eagle, 190, 240, self.rect_desert_eagle, 350, 'desert_eagle')
        self._blit_guns(self.ak47, 115, 375, self.rect_ak47, 400, 'AK-47')    
        self._blit_guns(self.m16, 900, 100, self.rect_m16, 600, 'm-16')
        self._blit_guns(self.ASval, 900, 240, self.rect_ASval, 800, 'ASval')
        self._blit_guns(self.VSS, 900,375, self.rect_VSS, 1000, 'VSS')
        self._blit_guns(self.ASvalG, 500, 530, self.rect_ASvalG, 2500, 'ASvalG')

    def _blit_guns(self, gun, x, y, rect, cost, name):
        self.mouse = pygame.mouse.get_pos()
        self.click = pygame.mouse.get_pressed()
        self.text = self.settings.font_ammo.render(f'{cost}', True, (0,0,0))
        if name == self.file.stats['gun'][self.file.g-1]:
            #Линия под  выбранным оружием
            pygame.draw.rect(self.screen, (0,255,0), (x - 5, y + rect[3], rect[2] + 5,  5), 5)
        self.screen.blit(gun, (x, y, rect[2], rect[3]))
        if name not in self.file.stats['gun']:
            #Действия с оружием, которое еще не было куплено
            self.screen.blit(self.coin, (x - 50, y + 50, self.rect_coin[2], self.rect_coin[3]))
            self.screen.blit(self.text, (x - 20, y + 42, self.rect_coin[2], self.rect_coin[3]))
            if x < self.mouse[0] < x + rect[2] and y < self.mouse[1] < y + rect[3]:
                pygame.draw.rect(self.screen, self.settings.color_ammoG, (x - 55, y, rect[2] + 60, rect[3] + 5), 5)
                if self.click [0] == 1 and not self.shop:
                    self.sounds.play_sounds(self.sounds.button_press)
                    pygame.time.delay(300)
                    if self.file.stats['gold']<=cost:  
                        self.text_counter +=1
                        self.text_c = True
                    else :
                        self.shop = True
                        self.text_shop2 = self.settings.font_ammo.render(f'{name}', True, (255,0,0))
                        self.cost = cost
                        self.name = name
                        #self._shopping(name, cost)
        else:
            #выбор имеющегося оружия
            if x < self.mouse[0] < x + rect[2] and y < self.mouse[1] < y + rect[3]:
                #pygame.draw.rect(self.screen, (0,255,0), (x - 5, y, rect[2] + 5, rect[3] + 5), 5)
                if self.click [0] == 1 and not self.shop:
                    self.sounds.play_sounds(self.sounds.button_press)
                    pygame.time.delay(300)
                    if name is not self.file.stats['gun'][self.file.g-1]:
                        index = self.file.stats['gun'].index(name)
                        self.file.stats['gun'][self.file.g-1], self.file.stats['gun'][index] = self.file.stats['gun'][index], self.file.stats['gun'][self.file.g-1]
