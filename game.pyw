import sys
import pygame
import pickle
from Settings import *
from gun import Gun
from bullet import Bullet
from ammo import Ammo
from characters import Char
from game_stats import Game_stats
from sounds import Sounds
from win_died import Win_died
from buttons import Buttons
from shop import Shop
from level import Level
import time
import random

class Game:
    """Overall class to manage game assets and behavior."""
    def __init__(self):
        """Initialize the game, and create game resources."""
        pygame.init()
        self.file = Level()
        self.file.load()

        self.settings = Settings()
        #self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.screen = pygame.display.set_mode(
           (self.settings.screen_width, self.settings.screen_height))
        
        self.screen_rect = self.screen.get_rect()

        img = pygame.image.load(self.file.resource_path('images/tyan2.png'))
        pygame.display.set_icon(img)
        pygame.display.set_caption("My fucking game")
        self.clock = pygame.time.Clock()
        self.fps = 180
        self.c = False
        self.shine = False
        self.count_blood = 0
        self.count_shine = 0
        self.check = True
        self.start = -5
        self.time_shot = 0
        self.blood = pygame.image.load(self.file.resource_path('images/blood1.png'))

        self.run = True
        self.shop = False
        self.endless = False

        self.coin = pygame.image.load(self.file.resource_path('images/coin.png'))
        self.rect_coin = self.screen.get_rect(
            top = (self.screen_rect.top))
        self.coinshop = pygame.image.load(self.file.resource_path('images/coinshop.png'))
        self.text = self.settings.font_ammo.render(f'{self.file.stats["gold"]}', True, self.settings.color_ammoG)
        self.rect_text = self.text.get_rect(
            top = (self.screen_rect.top))
        self.rect_text.x += 50
        self.land = pygame.image.load(self.file.resource_path(f'images/lands/{self.file.level["land"]}'))
        self.gun = Gun(self)
        self.bullet = Bullet(self)
        self.char = Char(self)
        self.stats = Game_stats(self)
        self.sounds = Sounds()
        self.Shop = Shop(self)
        self.ammo = Ammo(self)
        self.other_bg = Win_died(self)

        self.menu = True
        self.round = self.file.stats['level']

        self.bullets = pygame.sprite.Group()
        self.squad = pygame.sprite.Group()
        self._create_squad()

        self.button1 = Buttons(self, 102, 27)
        self.button_start = Buttons(self, 250, 80)
        self.button_shop = Buttons(self, 175, 70)
        self.button_exit = Buttons(self, 136, 70)
        self.button_gun = Buttons(self, 300, 85)
        self.button_menu = Buttons(self, 175, 70)
        self.button_endless_mode = Buttons(self,307,42)
        self.kill = True
        self.shine_rect = 0
        self.kills = 0

    def show_menu(self):
        self.land_menu = pygame.image.load(self.file.resource_path('images/lands/menu.jpg'))
        self.sounds.menu_play()
        while self.menu:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.file.save_stats()
                    sys.exit()
            self.screen.blit(self.land_menu, (0,0))
            self.button_start.draw_buttons(self.screen_rect.center[0]-100, self.screen_rect.center[1]-150, 'Start', 100, self._break_menu)
            self.button_endless_mode.draw_buttons(self.screen_rect.center[0]-130, self.screen_rect.center[1]-30, 'Endless mode', 50,self._endless_game)
            self.button_shop.draw_buttons(self.screen_rect.center[0]-60, self.screen_rect.center[1]+25, 'Shop', 80, self._start_shop)
            self.button_exit.draw_buttons(self.screen_rect.center[0]-40, self.screen_rect.center[1]+100, 'Exit', 80, sys.exit)
            pygame.display.flip()
        self.round = self.sounds.round1

    def _break_menu(self):
        self.shop = False
        self.menu = False
        self.sounds.bg_stop()
    
    def _endless_game(self):
        self.shop = False
        self.menu = False
        self.endless = True
        self.settings.endless = True
        self.land = pygame.image.load(self.file.resource_path(f'images/lands/Land0.jpg'))
        self.sounds.bg_stop()

    def _start_shop(self):
        self.shop = True
        self.menu = False

    def show_shop(self):
        self.land_shop = pygame.image.load(self.file.resource_path('images/lands/shop.jpg'))
        self.text1 = self.settings.font_pause.render('  Shop  ', True, (0,0,0))
        self.rect_text1 = self.text1.get_rect(
            midtop = (self.screen_rect.midtop))
        self.rect_text1.y += 50
        while self.other_bg.shop:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.file.save_stats()
                    sys.exit()
            self.screen.blit(self.land_shop, (0,0))
            self.screen.blit(self.coin, self.rect_coin)
            self.screen.blit(self.text, self.rect_text)
            self.screen.blit(self.text1, self.rect_text1)
            self.text = self.settings.font_ammo.render(f'{self.file.stats["gold"]}', True, self.settings.color_ammoG)
            self.Shop.blit_shop()
            if self.Shop.text_counter != 0 and self.Shop.text_c:
                self.Shop.blit_text(self.Shop.text_false, (350, 300))
            if self.Shop.shop:
                self.Shop._shopping()
            else:
                self.button_menu.draw_buttons(self.screen_rect.midbottom[0]-85, self.screen_rect.midbottom[1]-350, 'Menu', 80, self.other_bg.restart_game)
            pygame.display.flip()

    def run_game(self):
        """Start the main loop for the game."""
        if self.other_bg.run:
            pygame.mixer.music.load(self.file.resource_path('sounds/mortalbackground.mp3'))
            self.sounds.bg_play()
            time.sleep(1)
            if self.endless:
                self.sounds.round1 = pygame.mixer.Sound(self.file.resource_path(f'sounds/round0.mp3'))
            self.sounds.play_sounds(self.sounds.round1)
        while self.other_bg.run:
            if self.other_bg.win:
                self.other_bg._you_win()
                self._check_events()
            elif self.other_bg.died:
                self.other_bg._you_died()
                self._check_events()
            elif self.other_bg.pause:
                self.other_bg._pause()
                self._check_events()
            elif not self.other_bg.win:
                # Watch for keyboard and mouse events.
                if self.fps == 180:
                    self._check_events()
                self.update_bullet()
                self.collision()
                self.gun.update_location(self.endless)
                self.bullets.update(self.gun.rect.y)
                self._update_enemy()
                self.update_counters()
                self.check_fatality()
                #print(self.other_bg.start)
                # Redraw the screen during each pass through the loop.
                self._update_screen()
                self.clock.tick(self.fps)

    def _check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.file.save_stats()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keyDOWN_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyUP_events(event)
            elif self.check:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self._check_mouseDOWN_events(event)
                elif event.type == pygame.MOUSEBUTTONUP:
                    self._check_mouseUP_events(event)

    def _check_keyDOWN_events(self, event):
        if event.key == pygame.K_w and not self.other_bg.pause:
            self.gun.moving_up = True
        elif event.key == pygame.K_s and not self.other_bg.pause:
            self.gun.moving_down = True
        elif (event.key == pygame.K_q) or (event.key == pygame.K_ESCAPE):
            if not self.other_bg.pause:
                self.other_bg.pause = True
                self.other_bg.process_pause = False

        elif event.key == pygame.K_r and not self.other_bg.pause and self.check:
            self.check = False
            self.sounds.play_sounds(self.settings.gunreload)
            self.start = time.perf_counter()
        
        elif event.key == pygame.K_SPACE and not self.other_bg.process_pause:
            if self.other_bg.pause == False:
                self.other_bg.pause = True
            elif self.other_bg.pause == True:
                self.other_bg.unpause()
                self.other_bg.pause = False
                

    def _check_keyUP_events(self, event):
        if event.key == pygame.K_w:
            self.gun.moving_up = False
        elif event.key == pygame.K_s:
            self.gun.moving_down = False

    def _check_mouseDOWN_events(self, event):
        self.bullet.shotting = True


    def _check_mouseUP_events(self, event):
        if event.button == 1:
            self.time_shot = 0
            self.bullet.shotting = False

    def _fire_bullet(self):
        """Создание нового снаряда и включение его в группу bullets."""
        if self.settings.ammo > 0:
            self.settings.ammo -= 1
            self.ammo.update_ammo()
            self.time_shot = time.perf_counter()
            self.sounds.play_sounds(self.settings.gunshot)
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)
        
                
    def update_bullet(self):
        if (time.perf_counter() - self.settings.reload_time > self.start) and (self.check == False):
                self.check = True
                self.time_shot = 0
                self.bullet.shotting = False
                self.ammo.reload_ammo()
                self.ammo.update_ammo()

        for i in self.bullets.copy():
                if i.rect.right < 0:
                    self.bullets.remove(i)

    def collision(self):
        self.kill = True
        for sprite in self.bullets:
            name = pygame.sprite.spritecollideany(sprite, self.squad)
            if name:
                if self.settings.counter > 120 and self.settings.counter < 200 and not self.settings.through_shot and not self.file.level['char'] and not self.endless:
                    self.kill = False
                    self.shine = True
                    self.shine_rect = name.rect
                elif self.endless and not self.settings.index and (self.settings.counter > 120 and self.settings.counter < 200 and not self.settings.through_shot):
                    self.kill = False
                    self.shine = True
                    self.shine_rect = name.rect
                else:
                    self.c = True
                    self.blood_rect = name.rect
                    self.char.blood = random.choice(self.char.arr_blood)
                    self.stats.update_progress()
                    self.file.stats['kill']+=1
                    self.kills += 1
                    self.file.stats['gold']+=5
                    self.file.save_stats()
                break
        if self.kill:
            collisions = pygame.sprite.groupcollide(
                self.bullets, self.squad, not self.settings.through_shot, True)
        if self.shine:
            collisions = pygame.sprite.groupcollide(
                self.bullets, self.squad, not self.settings.through_shot, False)
        if not self.squad:
            self._create_squad()


    def _create_squad(self):
        '''Создание тимы противника'''
        #Создание экземпляра противника
        if self.settings.quantity_enemys:
            enemy = Char(self)
            if self.endless:
                self.settings.index = random.randint(0,2)
                self.settings.enemy_speed = random.randint(2,3)
            self.squad.add(enemy)
            if not self.endless:
                self.settings.quantity_enemys -= 1
            if self.settings.quantity_enemys == 0:
                self.sounds.play_sounds(self.sounds.finish_him)
            
        elif self.settings.quantity_enemys == 0: 
            self.other_bg.win = True
            self.fps = 180
            self.file.stats['gold']+= self.file.stats['level']*100
            self.settings.bonus = self.file.stats['level']*100
            if self.file.stats['level'] < 3:
                self.file.stats['level'] += 1
            self.file.save_stats()
            self.sounds.play_sounds(self.sounds.flowless_victory)


    def _update_enemy(self):
        self.squad.update()
        '''if pygame.sprite.spritecollideany(self.gun, self.squad):
            time.sleep(0.5)
            self.died = True'''
        self._check_enemys_right()

    def _check_enemys_right(self):
        for i in self.squad.sprites():
            if i.rect.right >= self.screen_rect.right:
                self.sounds.bg_stop()
                self.sounds.play_sounds(self.sounds.game_over)
                time.sleep(0.5)
                self.other_bg.died = True
                break

    def check_fatality(self):
        if self.settings.quantity_enemys == 0 and self.bullets.sprites() and self.fps == 180:
            for enemy in self.squad:
                for bullet in self.bullets:
                    if bullet.rect.y < enemy.rect.y+enemy.rect[3]\
                        and bullet.rect.y+bullet.rect[3] > enemy.rect.y:
                        self.fps = 8
                        self.bullet.shotting = False

    def update_counters(self):
        if self.c:
            self.count_blood+=1
            if self.count_blood > 100:
                self.c = False
                self.count_blood = 0
        if self.shine:
            self.count_shine+=1
            if self.count_shine>4:
                self.shine = False
                self.count_shine = 0

    def _update_screen(self):
        self.screen.blit(self.land, (0,0))
        self.screen.blit(self.coin, self.rect_coin)
        self.text = self.settings.font_ammo.render(f'{self.file.stats["gold"]}', True, self.settings.color_ammoG)
        self.screen.blit(self.text, (self.rect_text[0]-7, \
            self.rect_text[1]-2, self.rect_text[2], self.rect_text[3]))

        if self.bullet.shotting and self.check:
            if time.perf_counter() - self.time_shot >= self.settings.shotting_speed and not self.button1.check:
                self._fire_bullet()
        #self.screen.fill(self.settings.bg_color)

        if self.c:
            self.char.blit_blood(self.blood_rect)
        self.gun.blitme()
        self.ammo.write_ammo()
        if self.check == False:
            self.ammo.image_reload()
        if self.shine:
            self.char.blit_shine(self.shine_rect)
        
        for bullet in self.bullets.sprites():
            bullet.blitme()
        for enemy in self.squad.sprites():
            enemy.blit_enemy()
        if not self.endless:
            self.stats.draw_progress()
        else:
            self.stats.numb_of_kills(self.kills)
        self.button1.draw_buttons(0, 0+40, 'Pause II', 30, self.other_bg._pause)
        #self.squad.draw(self.screen)
        # Make the most recently drawn screen visible.
        pygame.display.flip()



if __name__ == '__main__':
    while True:
        # Make a game instance, and run the game.
        gg = Game()
        gg.show_menu()
        if gg.shop:
            gg.show_shop()
        if gg.other_bg.run:
            gg.run_game()
