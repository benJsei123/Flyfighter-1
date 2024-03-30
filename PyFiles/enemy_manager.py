from pygame.sprite import Group, Sprite
import pygame as pg
from abc import ABC, abstractmethod
from guns import Guns
import random

class EnemyManager:
    def __init__(self, game) -> None:
        self.game = game
        self.game_settings = game.game_settings
        self.player = None
        self.enemy_group = pg.sprite.Group()
        
    def set_player(self,player):
        self.player = player

    def get_random_enemy(self):
        """ used to get a random enemy object to let it spawn on a tile (see MapTile class)"""
        choice_pool = [
            self.get_fast_enemy(),
            self.get_smart_enemy(),
            self.get_tanky_enemy()
        ]
        random_enemy = random.choice(choice_pool)
        return random_enemy
        
    def get_fast_enemy(self):
       return FastEnemy(self.game, self.game.camera_group)

    def get_tanky_enemy(self):
        return TankyEnemy(self.game, self.game.camera_group)

    def get_smart_enemy(self):
        return SmartEnemy(self.game, self.game.camera_group)



class Enemy(Sprite, ABC):
    def __init__(self, game,camera_group) -> None:
        super().__init__(camera_group)
        self.game = game
        self.game_settings = game.game_settings
        self.screen = game.screen
        self.rect = None
        self.guns = None
        self.fire_direction = None

    @abstractmethod
    def fire(self):
        pass

    def get_fire_direction(self):
        return (1,0) #TODO (1,0) for testing purposes. Get corret direction with vector calc
        
        
class FastEnemy(Enemy):
    def __init__(self, game, camera_group) -> None:
        super().__init__(game=game,camera_group=camera_group)
        self.image = pg.image.load(self.game_settings.image_paths['fast_enemy'])
        self.rect = self.image.get_rect()
        
        self.rect.x = 0
        self.rect.y = 0

        self.guns = Guns(game=self.game,owner=self)
    
    def fire(self):
        self.fire_direction = self.get_fire_direction()
        self.guns.add(owner=self,direction=self.fire_direction,sort='default')

class SmartEnemy(Enemy):
    def __init__(self, game, camera_group) -> None:
        super().__init__(game=game,camera_group=camera_group)
        self.image = pg.image.load(self.game_settings.image_paths['smart_enemy'])
        self.rect = self.image.get_rect()
        
        self.rect.x = 0
        self.rect.y = 0

        self.guns = Guns(game=self.game,owner=self)
        
    def fire(self):
        self.fire_direction = self.get_fire_direction()
        self.guns.add(owner=self,direction=self.fire_direction,sort='default')


class TankyEnemy(Enemy):
    def __init__(self, game, camera_group) -> None:
        super().__init__(game=game,camera_group=camera_group)
        self.image = pg.image.load(self.game_settings.image_paths['tanky_enemy'])
        self.rect = self.image.get_rect()
        
        self.rect.x = 0
        self.rect.y = 0

        self.guns = Guns(game=self.game,owner=self)
    
    def fire(self):
        self.fire_direction = self.get_fire_direction()
        self.guns.add(owner=self,direction=self.fire_direction,sort='default')


