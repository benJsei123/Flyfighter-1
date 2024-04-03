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
        self.bg_color = (255,255,255)
        self.small_tile_size = 32 #tile for background generation
        self.medium_tile_size = 32*3 #tile size for MapTile Objects
        self.large_tile_size = 32*6

        self.bg_line_color = (230,230,230)
        
        self.map_width = 20000
        self.map_height = 20000
        self.map_size = (self.map_width,self.map_height)

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
            "player_dying": glob.glob("Resources/pictures/animations/player_dying/*.png"),
            "player_idle": "LIST WITH ANIMATION IMAG PATHS",
            "fast_enemy_dying": "",
            "tanky_enemy_dying": "",
            "smart_enemy_dying": "",
            "smart_enemy_idle": glob.glob("Resources/pictures/animations/smart_enemy_idle/*.png"),
            "tanky_enemy_idle": glob.glob("Resources/pictures/animations/tanky_enemy_idle/*.png"),
            "fast_enemy_idle" : glob.glob("Resources/pictures/animations/fast_enemy_idle/*.png"),
            "speed_powerup_idle":glob.glob("Resources/pictures/animations/powerups/speed/*.jpg"),
            "damage_powerup_idle":glob.glob("Resources/pictures/animations/powerups/damage/*.png"),
            "firerate_powerup_idle":glob.glob("Resources/pictures/animations/powerups/firerate/*.png"),
            "hp_powerup_idle":glob.glob("Resources/pictures/animations/powerups/hp/*.png"),
        }

        self.tile_image_paths = {f"tile_{num}":f"Resources/pictures/tiles/tile_pic_{num}.png" for num in range(1,17)}
        self.initialize_dynamic_settings()


    def initialize_dynamic_settings(self):
        """ Following are dynamic settings and change during game
        Is called with each levelup and at game start"""

        #Calculate an increasing multiplier to make the game harder (see game stats)
        difficulty_multiplier = self.get_difficulty_multiplier()
        print("Difficultz set to:", difficulty_multiplier)

        #Enemies
        self.enemy_fire_proba_thresh = 0.05 * difficulty_multiplier#1 is high difficulty, 0 is no difficulty at all
        self.entity_spawn_chance = 0.2 * difficulty_multiplier
        self.powerup_spawn_chance = 0.25
        self.enemy_bullet_speed = 5
        self.enemy_bullet_damage = int(difficulty_multiplier) 
        self.enemy_hp = int(difficulty_multiplier)
        self.tanky_enemy_hp = int(5 * difficulty_multiplier)
        self.fast_enemy_speed = 2

        #Powerups
        self.hp_powerup_points = 2 + (difficulty_multiplier//0.3)
        self.firerate_powerup_points = 1
        self.damage_powerup_points = 1
        self.speed_powerup_points = 1

        #Guns
        self.bullet_speed = 5
        self.standard_player_firerate = 20


    def get_difficulty_multiplier(self):
        """returns a  multiplier that will rise with rising level"""
        difficulty_multiplier = 1 + self.game_stats.difficulty_level/10
        
        return difficulty_multiplier

    def reset(self):
        self.initialize_dynamic_settings()
