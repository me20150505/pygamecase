import os;
import pygame;
from pygame.sprite import Sprite;

class Ship(Sprite):
    def __init__(self, al_game, ship_width=120, ship_height=96):
        super().__init__();
        self.settings = al_game.settings;
        self.screen = al_game.screen;
        self.screen_rect = al_game.screen.get_rect();

        self.image = pygame.image.load(os.path.join(os.path.dirname(__file__), 'images/ship.png'));
        self.image = pygame.transform.scale(self.image, (ship_width, ship_height));
        self.rect = self.image.get_rect();

        self.rect.midbottom = self.screen_rect.midbottom;
        self.x = float(self.rect.x);

        self.move_right = False;
        self.move_left = False;

    def blitme(self):
        self.screen.blit(self.image, self.rect);

    def update(self):
        if self.move_right and self.rect.right < self.screen_rect.right:
            self.x += self.settings.ship_speed;
        if self.move_left and self.rect.left > 0:
            self.x -= self.settings.ship_speed;

        self.rect.x = self.x;

    def center_ship(self):
        self.rect.midbottom = self.screen_rect.midbottom;
        self.x = float(self.rect.x);