import pygame as pg
from game_settings import GameSettings
from player import Player
from game_stats import GameStats
from map import Map
from vector import Vector
import sys
import time
from sound import Sound
from camera import CameraGroup
from launchscreen import Launchscreen
from scoreboard import Scoreboard

class Game:

    def __init__(self) -> None:
        pg.init()
        self.clock = pg.time.Clock()
        pg.event.set_grab(True)

        self.game_stats = GameStats(game=self)
        self.game_settings = GameSettings(game=self)
        

        sw,sh = self.game_settings.screen_width,self.game_settings.screen_height
        self.screen = pg.display.set_mode((sw,sh))
        pg.display.set_caption("FlyFighter")
        
        
        #Requires Player
        self.map = Map(game=self)
        self.background_surface = self.map.background_surface
        #Requires background surface
        self.camera_group = CameraGroup(game=self)
        #Requires camera group
        self.player = Player(game=self, group=self.camera_group)
        
        self.sound = Sound()
        self.score_board = Scoreboard(game=self)
        self.launchscreen = Launchscreen(game=self)


        self.map.set_player(self.player)
        self.map.enemy_mgr.set_player(self.player)
        self.map.powerup_mgr.set_player(self.player)

        self.player.init_missing_attributes()
        self.map.initialize_map()

     
        self.game_active = False
        self.first = True


    def check_events(self): 
        for event in pg.event.get():
            type = event.type
            if type == pg.KEYUP: 
                key = event.key 
                if key == pg.K_SPACE: 
                    self.player.firing=False
                    #self.ship.all_stop()
                elif key in Player.key_velocity.keys():
                    self.player.handle_input(event) #stop ship?
            elif type == pg.KEYDOWN:
                key = event.key
                
                if key == pg.K_SPACE: 
                    self.player.firing=True
                elif key in Player.key_velocity: 
                
                    self.player.handle_input(event)
            elif type == pg.QUIT: 
                print("QUIT GAME")
                pg.quit()
                sys.exit()

    def activate(self): 
        self.game_active = True
        self.first = False

    def restart(self):
        print("Restart called")
        self.screen.fill(self.game_settings.bg_color)
        self.player.reset()
        self.map.reset()
        #if(self.first == False): self.launchscreen.show()
            
    
    def game_over(self):
        self.reset()

    def play(self):
        self.launchscreen.show()
        
        finished = False
        # self.screen.fill(self.game_settings.bg_color)

        while not finished:
            self.check_events()    # exits if Cmd-Q on macOS or Ctrl-Q on other OS
            #Use self.game_active = False to interrupt the actual game
            if self.game_active or self.first:
                self.screen.fill("#ffffff")
                self.camera_group.update()
                self.camera_group.custom_draw(self.player)
                
                self.map.update()
                self.player.update()
                self.score_board.update()
                
                self.first = False
                
        
            pg.display.update()
            self.clock.tick(60)

if __name__ == '__main__':
  g = Game()
  g.play()

