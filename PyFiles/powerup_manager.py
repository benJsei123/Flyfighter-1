from player import Player
import random
from abc import ABC, abstractmethod
from flyfighter_game import Game

class PowerUpManager:
    def __init__(self, game:Game,tiles:list, player:Player) -> None:
        self.game = game
        self.settings = game.settings
        self.tiles = tiles #holds all tiles of Map 
        self.player = player
        self.powerups = [] #holds all active powerups
        
    def update_tiles(self):
        for t in self.tiles:
            if not t.visited and not t.enemies_spawned:
                t.place_entities()

    def get_random_powerup(self,position=(0,0)):
        """ used to retrieve a random powerup to let it spawn on MapTile"""
        pass


class PowerUp(ABC):
    def __init__(self, powerup_mgr:PowerUpManager, position:tuple) -> None:
        self.settings= powerup_mgr.settings
        self.image_path = ""
        self.amount = 0 # 100 fo HP means +100 HP, 10 for SPEED meand +10 speed (see inheriting classes)
        self.position = position

    @abstractmethod
    def apply(self):
        pass

    @abstractmethod
    def scale_powerup(self):
        pass


class HeartPointPowerUp(PowerUp):
    def __init__(self) -> None:
        super().__init__()
        #start with self.image_path = ...
        #and intialize self.amount 

        self.amount = int(10 * self.settings.get_difficulty_multiplier())

    #TODO implement abstract methods


class DamagePowerUp(PowerUp):
    def __init__(self) -> None:
        super().__init__()
        self.amount = int(10 * self.settings.get_difficulty_multiplier())


class SpeedPowerUp(PowerUp):
    def __init__(self) -> None:
        super().__init__()
        self.amount = int(10 * self.settings.get_difficulty_multiplier())


class FireRatePowerUp(PowerUp):
    def __init__(self) -> None:
        super().__init__()
        self.amount = int(10 * self.settings.get_difficulty_multiplier())

