import pygame
import pickle
from buttons import Buttons
import time

class Win_died:
    def __init__(self, game):
        self.settings = game.settings
        self.screen = game.screen
        self.screen_rect = game.screen.get_rect()
        self.sounds = game.sounds
        self.file = game.file
        self.Shop = game.Shop
        self._update = game._update_screen

        self.coin = game.coin
        self.rect_coin = self.coin.get_rect(
            center = (self.screen_rect.center))
        self.rect_coin.x +=50
        self.pause = False
        self.process_pause = False
        self.pause_land = pygame.image.load(self.file.resource_path('images/lands/pause.jpg'))
        self.text1 = self.settings.font_pause.render('Pause', True, (0,0,0))
        self.text2 = self.settings.font_ammo.render('Press "Space" to continue', True, (255,0,0))
        self.rect_text1 = self.text1.get_rect(
            midtop = (self.screen_rect.midtop))
        self.rect_text2 = self.text1.get_rect(
            center = (self.screen_rect.center))
        self.rect_text1.y += 50
        self.rect_text2.x -= 100
        self.sec = 3
        self.start = 0 
        self.run = True
        self.shop = True

        self.win = False
        self.win_img = pygame.image.load(self.file.resource_path('images/lands/win.jpg'))
        self.rectwin = self.win_img.get_rect(
            center = (self.screen_rect.center))
        self.rectwin.y -= 200

        self.died = False
        self.died_img = pygame.image.load(self.file.resource_path('images/died.png'))
        self.rectdied = self.died_img.get_rect(
            center = (self.screen_rect.center))
        self.died_land = pygame.image.load(self.file.resource_path('images/lands/die.jpg'))
        self.button_to_menu = Buttons(self, 220, 80)

    def _pause (self):
        self.pause = True
        self.sounds.bg_pause()
        self.start = time.perf_counter()
        self.screen.blit(self.pause_land, (0,0))
        self.screen.blit(self.text1, self.rect_text1)
        self.screen.blit(self.text2, self.rect_text2)
        self.button_to_menu.draw_buttons(self.screen_rect.midbottom[0]-100, self.screen_rect.midbottom[1]-150, 'Menu', 100, self.restart_game)
        pygame.display.flip()

    def unpause(self):
        self.process_pause = True
        while self.sec > 0:
            self._update()
            self.text = self.settings.font_pause.render(str(self.sec), True, (255,0,0))
            self.rect_text = self.text.get_rect(
                center = (self.screen_rect.center))
            self.screen.blit(self.text1, self.rect_text1)
            self.screen.blit(self.text, self.rect_text)
            pygame.display.flip()
            self.sec -= 1
            time.sleep(1)
        self.sec = 3
        self.pause = False
        self.sounds.bg_unpause()


    def _you_win(self):
        self.screen.fill((0,0,0))
        self.screen.blit(self.win_img, self.rectwin)
        self.textt = self.settings.font_ammo.render(f'+{self.settings.bonus}', True, self.settings.color_ammoG)
        self.Shop.blit_text(self.textt, (self.rect_coin[0]-80, self.rect_coin[1]))
        self.screen.blit(self.coin, self.rect_coin)
        self.button_to_menu.draw_buttons(self.screen_rect.midbottom[0]-100, self.screen_rect.midbottom[1]-150, 'Menu', 100, self.restart_game)
        pygame.display.flip()

    def _you_died(self):
        self.screen.blit(self.died_land, (0,0))
        self.screen.blit(self.died_img, self.rectdied)
        self.button_to_menu.draw_buttons(self.screen_rect.midbottom[0]-100, self.screen_rect.midbottom[1]-150, 'Menu', 100, self.restart_game)
        pygame.display.flip()

    def restart_game(self):
        self.sounds.stop_sounds(self.sounds.game_over)
        self.file.save_stats()
        self.shop = False
        self.run = False
    