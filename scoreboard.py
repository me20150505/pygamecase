import pygame.font;
from pygame.sprite import Group;

from ship import Ship;

class Scoreboard:
    def __init__(self, al_game):
        self.al_game = al_game;
        self.screen = al_game.screen;
        self.screen_rect = self.screen.get_rect();
        self.settings = al_game.settings;
        self.game_status = al_game.game_status;

        self.text_color = (30, 30, 30);
        self.font = pygame.font.SysFont(None, 48);
        self.prep_score();
        self.prep_high_score();
        self.prep_level();
        self.prep_ships();

    def prep_score(self):
        round_score = round(self.game_status.score, -2);
        score_str = '{:,}'.format(round_score);
        self.score_image = self.font.render(score_str, True, self.text_color, self.settings.bg_color);

        self.score_rect = self.score_image.get_rect();
        self.score_rect.right = self.screen_rect.right - 20;
        self.score_rect.top = 20;

    def prep_high_score(self):
        high_score = round(self.game_status.high_score, -2);
        high_score_str = '{:,}'.format(high_score);
        self.high_score_image = self.font.render(high_score_str, True, self.text_color, self.settings.bg_color);

        self.high_score_rect = self.high_score_image.get_rect();
        self.high_score_rect.centerx = self.screen_rect.centerx;
        self.high_score_rect.top = self.score_rect.top;

    def prep_level(self):
        level_str = str(self.game_status.level);
        self.level_image = self.font.render(level_str, True, self.text_color, self.settings.bg_color);

        self.level_rect = self.level_image.get_rect();
        self.level_rect.right = self.score_rect.right;
        self.level_rect.top = self.score_rect.bottom + 10;

    def prep_ships(self):
        self.ships = Group();
        for ship_number in range(self.game_status.ship_count):
            ship = Ship(self.al_game, 60, 48);
            ship.rect.x = ship_number * ship.rect.width + 10;
            ship.rect.y = 10;
            self.ships.add(ship);

    def show_score(self):
        self.screen.blit(self.score_image, self.score_rect);
        self.screen.blit(self.high_score_image, self.high_score_rect);
        self.screen.blit(self.level_image, self.level_rect);
        self.ships.draw(self.screen);

    def check_high_score(self):
        if self.game_status.score > self.game_status.high_score:
            self.game_status.high_score = self.game_status.score;
            self.prep_high_score();