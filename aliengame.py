import sys;
import os;
import json;
import pygame;
from time import sleep;

from settings import Settings;
from game_status import GameStatus;
from scoreboard import Scoreboard;
from button import Button;
from ship import Ship;
from bullet import Bullet;
from alien import Alien;

class AlienGame:
    '''
    管理游戏资源和行为的类
    '''

    def __init__(self):
        pygame.init();
        self.settings = Settings();

        if self.settings.is_fullscreen:
            self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN);
            self.settings.screen_width = self.screen.get_rect().width;
            self.settings.screen_height = self.screen.get_rect().height;
        else:
            self.screen = pygame.display.set_mode(
                (self.settings.screen_width, self.settings.screen_height)
            );
        pygame.display.set_caption(self.settings.caption);

        self.game_status = GameStatus(self);
        self.scoreboard = Scoreboard(self);

        self.ship = Ship(self);
        self.bullets = pygame.sprite.Group();
        self.aliens = pygame.sprite.Group();

        self._create_fleet();

        self.play_button = Button(self, 'Play');

    def _check_events(self):
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self._save_score_to_file();
                    sys.exit();
                elif event.type == pygame.KEYDOWN:
                    self._check_keydown_events(event);
                elif event.type == pygame.KEYUP:
                    self._check_keyup_events(event);
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos();
                    self._check_play_button(mouse_pos);

    def _save_score_to_file(self):
        high_score_data = {'high_score': self.game_status.high_score};
        with open(os.path.join(os.path.dirname(__file__), self.settings.score_file_path), 'w') as f:
            json.dump(high_score_data, f);

    def _check_play_button(self, pos):
        if self.play_button.rect.collidepoint(pos) and not self.game_status.game_active:
            self._start_game();

    def _start_game(self):
        self.settings.initialize_dynamic_settings();
        self.game_status.reset_status();
        pygame.mouse.set_visible(False);
        self.game_status.game_active = True;
        # 开始一轮游戏时初始化当前得分和等级
        self.scoreboard.prep_score();
        self.scoreboard.prep_level();
        self.scoreboard.prep_ships();

        self.aliens.empty();
        self.bullets.empty();
        self._create_fleet();
        self.ship.center_ship();

    def _check_keydown_events(self, event):
        if event.key == pygame.K_RIGHT:
            self.ship.move_right = True;
        elif event.key == pygame.K_LEFT:
            self.ship.move_left = True;
        elif event.key == pygame.K_q or event.key == pygame.K_ESCAPE:
            self._save_score_to_file();
            sys.exit();
        elif event.key == pygame.K_SPACE:
            if self.game_status.game_active:
                self._fire_bullet();
            else:
                self._start_game();

    def _check_keyup_events(self, event):
        if event.key == pygame.K_RIGHT:
            self.ship.move_right = False;
        elif event.key == pygame.K_LEFT:
            self.ship.move_left = False;

    def _fire_bullet(self):
        if len(self.bullets) < self.settings.bullet_max_count:
            new_bullet = Bullet(self);
            self.bullets.add(new_bullet);

    def _update_bullets(self):
        # 同时性 更新子弹位置
        self.bullets.update();

        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet);

        self._check_bullets_aliens_collisions();

    def _check_bullets_aliens_collisions(self):
        collisions = pygame.sprite.groupcollide(self.bullets, self.aliens, True, True);
        if collisions:
            for aliens in collisions.values():
                self.game_status.score += self.settings.alien_points * len(aliens);
            self.scoreboard.prep_score();
            self.scoreboard.check_high_score();

        if not self.aliens:
            self.bullets.empty();
            self._create_fleet();
            self.settings.increase_speed();

            self.game_status.level += 1;
            self.scoreboard.prep_level();

    def _update_aliens(self):
        self._check_fleet_edges();
        self.aliens.update();

        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit();

        self._check_aliens_bottom();

    def _check_aliens_bottom(self):
        screen_rect = self.screen.get_rect();
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= screen_rect.bottom:
                self._ship_hit();
                break;

    def _create_fleet(self):
        alien = Alien(self);
        alien_width, alien_height = alien.rect.size;
        available_space_x = self.settings.screen_width - 2 * alien_width;
        number_aliens_x = available_space_x // (alien_width * 2);

        ship_height = self.ship.rect.height;
        available_space_y = self.settings.screen_height - 5 * alien_height - ship_height;
        number_rows = available_space_y // (2 * alien_height);

        for row_number in range(number_rows):
            for alien_number in range(number_aliens_x):
                self._create_alien(alien_number, row_number);

    def _create_alien(self, alien_number, row_number):
            alien = Alien(self);
            alien_width, alien_height = alien.rect.size;
            alien.x = alien_width * (2 * alien_number + 1);
            alien.rect.x = alien.x;
            alien.rect.y = alien_height * (2 * row_number + 2);
            self.aliens.add(alien);

    def _check_fleet_edges(self):
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction();
                break;

    def _change_fleet_direction(self):
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_speed_drop;
        self.settings.fleet_direction *= -1;

    def _ship_hit(self):
        if self.game_status.ship_count > 0:
            self.game_status.ship_count -= 1;
            self.scoreboard.prep_ships();
        # 不能合并
        if self.game_status.ship_count > 0:
            self.aliens.empty();
            self.bullets.empty();

            self._create_fleet();
            self.ship.center_ship();

            sleep(1);
        else:
            pygame.mouse.set_visible(True);
            self.game_status.game_active = False;

    def _update_screen(self):
        self.screen.fill(self.settings.bg_color);
        self.ship.blitme();

        for bullet in self.bullets.sprites():
            bullet.draw_bullet();
        # 同时性 绘制一群外星人
        self.aliens.draw(self.screen);

        self.scoreboard.show_score();

        if not self.game_status.game_active:
            self.play_button.draw_button();

        pygame.display.flip();

    def run_game(self):
        while(True):
            self._check_events();
            if self.game_status.game_active:
                self.ship.update();
                self._update_bullets();
                self._update_aliens();
            self._update_screen();

if __name__ == '__main__':
    al = AlienGame();
    al.run_game();
