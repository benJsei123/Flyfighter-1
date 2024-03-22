from game_stats import GameStats
#from flyfighter_game import Game

class GameSettings:
    def __init__(self, game) -> None:
        self.game = game
        self.game_stats = self.game.game_stats
        self.screen_width = 32*30
        self.screen_height = 32*20
        self.bg_color = (50,50,50)
        self.map_tile_size = 32
        self.bg_line_color = (230,230,230)
        self.map_size = (20000,20000)

        self.image_paths = {
         "player" : "Resources/pictures/Player_Ship.png",
         "fast_enemy": "",
         "tanky_enemy": "",
         "smart_enemy": ""
        }

        self.animation_sequences = {
         "player_dying" : "PATH_TO_PLAYER_IMAGE",
         "fast_enemy_dying": "",
         "tanky_enemy_dying": "",
         "smart_enemy_dying": ""
        }


    def get_difficulty_multiplier(self):
        """returns a  multiplier that will rise with rising level"""
        multiplier = 1 + ( self.game_stats.difficulty_level / 10 )
        
        pass