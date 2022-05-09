class Settings:
    def __init__(self):
        self.is_fullscreen = True;
        self.caption = 'Alien Game';
        self.screen_width = 1400;
        self.screen_height = 800;
        self.bg_color = (150, 150, 150);

        self.ship_remain = 3;

        self.score_file_path = './data/score.json';

        # 子弹设置
        self.bullet_width = 3;
        self.bullet_height = 15;
        self.bullet_color = (60, 60, 60);
        self.bullet_max_count = 10;

        self.fleet_speed_drop = 5;

        self.speed_scale = 1.1;
        self.score_scale = 1.5;

        self.initialize_dynamic_settings();

    def initialize_dynamic_settings(self):
        self.ship_speed = 1.5;
        self.bullet_speed = 5.0;
        self.alien_speed = 1.0;

        # fleet_direction 1: 右移 -1: 左移
        self.fleet_direction = 1;

        self.alien_points = 500;

    def increase_speed(self):
        self.ship_speed *= self.speed_scale;
        self.bullet_speed *= self.speed_scale;
        self.alien_speed *= self.speed_scale;

        self.alien_points = int(self.score_scale * self.alien_points);