import os;
import json;

class GameStatus:
    def __init__(self, al_game):
        self.settings = al_game.settings;
        self.reset_status();

        self.game_active = False;

        try:
            with open(os.path.join(os.path.dirname(__file__), self.settings.score_file_path)) as f:
                score_data = json.load(f);
        except FileNotFoundError:
            self.high_score = 0;
        else:
            self.high_score = score_data['high_score'];

    def reset_status(self):
        self.ship_count = self.settings.ship_remain;
        self.score = 0;
        self.level = 1;