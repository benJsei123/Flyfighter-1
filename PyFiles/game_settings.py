from game_stats import GameStats
from flyfighter_game import Game

class GameSettings:
    def __init__(self, game:Game) -> None:
        self.game = game
        self.game_stats = self.game.game_stats
        self.screen_width = 1000
        self.screen_height = 800


    def get_difficulty_multiplier(self):
        """returns a  multiplier that will rise with rising level"""
        multiplier = 1 + ( self.game_stats.difficulty_level / 10 )
        
        pass