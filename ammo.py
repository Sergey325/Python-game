import pygame

class Ammo:
    def __init__(self, game):
        self.screen = game.screen
        self.screen_rect = game.screen.get_rect()
        self.settings = game.settings
        self.file = game.file
        self.color_ammo = self.settings.color_ammoC

        self.reload = pygame.image.load(self.file.resource_path('images/reload.png'))
        self.rect_reload = self.reload.get_rect(
            midbottom = (self.screen_rect.midbottom))

        self.ammo = pygame.image.load(self.file.resource_path('images/guns/ammo.png'))
        if self.file.stats['gun'][self.file.g-1].endswith('G'):
            self.ammo = pygame.image.load(self.file.resource_path('images/guns/ammoG.png'))
            self.color_ammo = self.settings.color_ammoG
        self.rect_ammo1 = self.ammo.get_rect(
            midbottom = (self.screen_rect.midbottom))
        self.rect_ammo2 = self.ammo.get_rect(
            midbottom = (self.screen_rect.midbottom))
        self.rect_ammo3 = self.ammo.get_rect(
            midbottom = (self.screen_rect.midbottom))

        self.rect_ammo2.x -= 7
        self.rect_ammo3.x -= 14
        self.rect_reload.x -= 6

        self.text = self.settings.font_ammo.render(f'{self.settings.ammo}/{self.file.gun["ammo"]}', True, self.color_ammo)
        self.rect_text = self.text.get_rect(
            midbottom = (self.screen_rect.midbottom))
        self.rect_text.x += 50

    def reload_ammo(self):
        self.settings.ammo = self.file.gun['ammo']

    def update_ammo(self):
        self.text = self.settings.font_ammo.render(f'{self.settings.ammo}/{self.file.gun["ammo"]}', True, self.color_ammo)
    
    def write_ammo(self):
        self.screen.blit(self.ammo, self.rect_ammo1)
        self.screen.blit(self.ammo, self.rect_ammo2)
        self.screen.blit(self.ammo, self.rect_ammo3)
        self.screen.blit(self.text, self.rect_text)
    
    def image_reload(self):
        self.screen.blit(self.reload, self.rect_reload)
