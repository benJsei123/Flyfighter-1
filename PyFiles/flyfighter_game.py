import pygame as pg
from game_settings import GameSettings
from player import Player
from game_stats import GameStats
from map import Map
from vector import Vector
import sys
import time
from sound import Sound

class Game:

    def __init__(self) -> None:
        pg.init()
        
        self.player = Player(game=self)
        self.game_stats = GameStats(game=self)
        self.game_settings = GameSettings(game=self)
        
        sw,sh = self.game_settings.screen_width,self.game_settings.screen_height
        self.screen = pg.display.set_mode((sw,sh))
        pg.display.set_caption("FlyFighter")
        self.map = Map(game=self)
        self.background_surface = self.map.background_surface
        
        self.sound = Sound()

        self.player.init_missing_attributes() #due to order of constructor calls

        self.game_active = False              # MUST be before Button is created
        self.first = True

    def check_events(self):
    
        for event in pg.event.get():
            type = event.type
            if type == pg.KEYUP: 
                key = event.key 
                if key == pg.K_SPACE: 
                    pass
                    #self.ship.all_stop()
                elif key in Player.key_velocity.keys():
                    self.player.handle_input(event) #stop ship?
            elif type == pg.KEYDOWN:
                key = event.key
                
                if key == pg.K_SPACE: 
                    print("Space key pressed")
                elif key in Player.key_velocity: 
                
                    self.player.handle_input(event)
            elif type == pg.QUIT: 
                print("QUIT GAME")
                pg.quit()
                sys.exit()

    def activate(self): 
        self.game_active = True
        self.first = False

    def play(self):
        #self.launchscreen.show()
        self.activate() #TODO shift this somewhere (e.g. after butotn is pressed to start game, this should be called) 
        finished = False
        # self.screen.fill(self.game_settings.bg_color)

        while not finished:
            self.check_events()    # exits if Cmd-Q on macOS or Ctrl-Q on other OS
            
            #Use self.game_active = False to interrupt the actual game
            if self.game_active or self.first:
                self.screen.blit(self.background_surface, (0, 0))
                self.first = False
                self.player.update()
                
                # self.screen.fill(self.game_settings.bg_color)
        
            
            pg.display.flip()
            time.sleep(0.02)


if __name__ == '__main__':
  g = Game()
  g.play()

