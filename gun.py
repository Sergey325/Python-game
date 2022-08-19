import pygame
 
class Gun:
    """A class to manage the gun."""
    def __init__(self, game):
        """Initialize the gun and set its starting position."""
        self.screen = game.screen
        self.screen_rect = game.screen.get_rect()
        self.settings = game.settings
        self.file = game.file


        self.image = pygame.image.load(self.file.resource_path(f'images/guns/{self.file.stats["gun"][self.file.g-1]}.png'))
        if self.file.stats['gun'][self.file.g-1] == 'VSS':
            self.settings.gun_y = 11
        #self.image.set_colorkey((25, 255, 230))
        self.rect = self.image.get_rect(
            midright = (self.screen_rect.midright))
        self.y = float(self.rect.y)

        self.moving_up = False
        self.moving_down = False

    def update_location(self, endless):
        if self.moving_up and self.rect.top > self.screen_rect.top:
            if not endless:
                self.y -= self.file.level['gun_speed']
            else:
                self.y -= 5
        if self.moving_down and self.rect.bottom < self.screen_rect.bottom:
            if not endless:
                self.y += self.file.level['gun_speed']
            else:
                self.y += 5
        self.rect.y = self.y
    def blitme(self):
        """Draw the gun at its current location."""
        self.screen.blit(self.image, self.rect)

