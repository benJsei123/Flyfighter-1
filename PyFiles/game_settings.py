import glob
from game_stats import GameStats
import os
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
        
        self.tanky_enemy_hp = 30

        self.fast_enemy_speed = 2

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
            "player_dying": "LIST WITH ANIMATION IMAGE PATHS",
            "fast_enemy_dying": "",
            "tanky_enemy_dying": "",
            "smart_enemy_dying": "",
            "smart_enemy_idle": glob.glob("Resources/pictures/animations/smart_enemy_idle/*.png"),
            "tanky_enemy_idle": glob.glob("Resources/pictures/animations/tanky_enemy_idle/*.png")
        }

        self.tile_image_paths = {f"tile_{num}":f"Resources/pictures/tiles/tile_pic_{num}.png" for num in range(1,17)}
        

    def get_difficulty_multiplier(self):
        """returns a  multiplier that will rise with rising level"""
        multiplier = 1 + ( self.game_stats.difficulty_level / 10 )
        
        pass