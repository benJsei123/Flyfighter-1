from game_stats import GameStats
#from flyfighter_game import Game

class GameSettings:
    def __init__(self, game) -> None:
        self.game = game
        self.game_stats = self.game.game_stats
        self.screen_width = 32*45
        #player size is 80x80

        self.screen_height = 32*24
        self.bg_color = (100,100,100)
        self.small_tile_size = 32 #tile for background generation
        self.medium_tile_size = 32*3 #tile size for MapTile Objects
        self.large_tile_size = 32*6

        self.bg_line_color = (230,230,230)
        
        self.map_width = 20000
        self.map_height = 20000
        self.map_size = (self.map_width,self.map_height)

        #Enemies
        self.enemy_fire_proba_thresh = 0.1 #1 is high difficulty, 0 is no difficulty at all
        self.enemy_spawn_chance = 0.5
        self.enemy_bullet_speed = 5
        self.enemy_bullet_damage = 1
        self.enemy_hp = 10
        self.tanky_enemy_hp = 90

        #Guns
        self.bullet_speed = 5

        self.image_paths = {
         "player" : "Resources/pictures/Player_Ship.png",
         "fast_enemy": "Resources/pictures/enemies/fast_enemy.png",
         "tanky_enemy": "Resources/pictures/enemies/tanky_enemy.png",
         "smart_enemy": "Resources/pictures/enemies/smart_enemy.png",
         "default_bullet":"Resources/pictures/bullets/default_bullet.png",
         "shotgun_bullet":"",
         "laser_bullet":"",
         "freezer_bullet":"",
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