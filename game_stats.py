import pygame

class Game_stats:
    def __init__(self, game):
        self.screen = game.screen
        self.screen_rect = game.screen.get_rect()
        self.settings = game.settings
        self.color = (255,0,0)
        self.file = game.file

        self.rect = pygame.Rect(0, 0, self.settings.progress_width,
                                self.settings.progress_height)
        self.rect.midtop = self.screen_rect.midtop

        self.inside_color = (0,0,0)
        self.inside_rect = pygame.Rect(0, 0, self.settings.progress_insideW,
                                self.settings.progress_insideH)
        self.inside_rect.x += self.rect.x

    def draw_progress(self):
        pygame.draw.rect(self.screen, self.color, self.rect)
        pygame.draw.rect(self.screen, self.inside_color, self.inside_rect)

    def update_progress(self):
        self.settings.progress_insideW += int(self.settings.progress_width/self.settings.save_quantity_enemys)
        self.inside_color = (0,0,0)
        self.inside_rect = pygame.Rect(0, 0, self.settings.progress_insideW,
                                self.settings.progress_insideH)
        self.inside_rect.x += self.rect.x + 2
        self.inside_rect.y += 2

    def numb_of_kills(self, kills):
        text1 = self.settings.font_ammo.render(f'Kills: {kills}', True, (255,0,0))
        rect_text1 = text1.get_rect(
            midtop = (self.screen_rect.midtop))
        self.screen.blit(text1, rect_text1)
