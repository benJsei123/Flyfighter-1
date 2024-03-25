from game_stats import GameStats
#from flyfighter_game import Game

class GameSettings:
    def __init__(self, game) -> None:
        self.game = game
        self.game_stats = self.game.game_stats
        self.screen_width = 32*30
        #player size is 80x80

        self.screen_height = 32*20
        self.bg_color = (50,50,50)
        self.small_tile_size = 32 #tile for background generation
        self.medium_tile_size = 32*3 #tile size for MapTile Objects
        self.large_tile_size = 32*6

        self.bg_line_color = (230,230,230)
        
        self.map_width = 20000
        self.map_height = 20000
        self.map_size = (self.map_width,self.map_height)

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

        self.tile_image_paths = {
            "tile_1" : "Resources/pictures/tiles/tile_pic_1.png",
            "tile_2" : "Resources/pictures/tiles/tile_pic_2.png",
            "tile_3" : "Resources/pictures/tiles/tile_pic_3.png",
            "tile_4" : "Resources/pictures/tiles/tile_pic_4.png",
            "tile_5" : "Resources/pictures/tiles/tile_pic_5.png",
            "tile_6" : "Resources/pictures/tiles/tile_pic_6.png",
            "tile_7" : "Resources/pictures/tiles/tile_pic_7.png",
            "tile_8" : "Resources/pictures/tiles/tile_pic_8.png",
            "tile_9" : "Resources/pictures/tiles/tile_pic_9.png",
            "tile_10" :"Resources/pictures/tiles/tile_pic_10.png",
            "tile_11" :"Resources/pictures/tiles/tile_pic_11.png",
            "tile_12" :"Resources/pictures/tiles/tile_pic_12.png",
            "tile_13" :"Resources/pictures/tiles/tile_pic_13.png",
            "tile_14" :"Resources/pictures/tiles/tile_pic_14.png",
            "tile_15" :"Resources/pictures/tiles/tile_pic_15.png",
            "tile_16" :"Resources/pictures/tiles/tile_pic_16.png"
            
        }
        

    def get_difficulty_multiplier(self):
        """returns a  multiplier that will rise with rising level"""
        multiplier = 1 + ( self.game_stats.difficulty_level / 10 )
        
        pass