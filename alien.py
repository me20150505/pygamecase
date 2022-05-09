import os;
import pygame;
from pygame.sprite import Sprite;

class Alien(Sprite):
    def __init__(self, al_game):
        super().__init__();
        self.screen = al_game.screen;
        self.settings = al_game.settings;

        self.image = pygame.image.load(os.path.join(os.path.dirname(__file__), 'images/alien.png'));
        self.image = pygame.transform.scale(self.image, (60, 48));
        self.rect = self.image.get_rect();

        self.rect.x = self.rect.width;
        self.rect.y = self.rect.height;

        self.x = float(self.rect.x);

    def check_edges(self):
        screen_rect = self.screen.get_rect();
        if self.rect.right >= screen_rect.right or self.rect.left <= 0:
            return True;

    def update(self):
        self.x += (self.settings.alien_speed * self.settings.fleet_direction);
        self.rect.x = self.x;