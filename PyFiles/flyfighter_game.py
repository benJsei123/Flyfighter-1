import pygame as pg
from game_settings import GameSettings
from player import Player
from game_stats import GameStats


class Game:
    def __init__(self) -> None:
        pg.init()

        self.player = Player()
        self.settings = GameSettings()
        self.game_stats = GameStats()

        sw,sh = self.settings.screen_width,self.settings.screen_height
        self.screen = pg.display.set_mode((sw,sh))
