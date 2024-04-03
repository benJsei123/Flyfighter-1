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
        
        self.fog_effect =  self.get_fog_effect()

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
        self.game_stats.reset()
        self.game_settings.reset()
        #self.score_board.reset() #probably not necessary since updates itself anyways all the time
        if not self.first:
            self.launchscreen.show()
            
    def game_over(self):
        self.restart()

    def play(self):
        self.sound.play_launchscreen_theme()
        self.launchscreen.show()
        self.sound.stop_music()
        
       
        finished = False
        # self.screen.fill(self.game_settings.bg_color)
        self.sound.play_ambience_music()

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
                
        
            self.screen.blit(self.fog_effect, (0, 0))
            pg.display.update()
            self.clock.tick(60)

        self.sound.stop_music()

    def get_fog_effect(self):
        fog = pg.Surface((self.game_settings.screen_width, self.game_settings.screen_height), pg.SRCALPHA)
    
        center_x, center_y = self.game_settings.screen_width // 2, self.game_settings.screen_height // 2
        
        rad = 100
        max_radius = max(center_x+rad, center_y+rad)
        inner_radius = 10  # Radius des komplett weißen Bereichs in der Mitte

        # Quadratische Funktion für nichtlineare Intensitätszunahme
        # Diese Funktion erreicht 255 (volle Deckkraft) am Rand des Bildschirms
        for radius in range(max_radius, 0, -1):
            if radius > inner_radius:
                alpha = ((radius - inner_radius) / (max_radius - inner_radius)) ** 7 * 255
                alpha = max(0, min(255, alpha))  # Stelle sicher, dass alpha zwischen 0 und 255 liegt
                color = (0, 0, 0, int(alpha))
                pg.draw.ellipse(fog, color, (center_x - radius, center_y - radius, radius * 2, radius * 2))
            else:
                break  # Kein Nebel innerhalb des inneren Radius
        
        return fog


if __name__ == '__main__':
  g = Game()
  g.play()

