import pygame as pg
import pygame.font 
from pygame.sprite import Group
from player import Player
from sound import Sound

class Scoreboard:
  def __init__(self, game):
      self.game = game 
      self.screen = game.screen 
      self.player = game.player
      self.player_stats = game.player.player_stats
      self.screen_rect = game.screen.get_rect() 
      self.game_settings = game.game_settings 
      self.game_stats = game.game_stats
      self.sound = Sound()
      self.text_color = (30, 30, 30)
      self.font = pygame.font.SysFont("lucida console", 24)
      self.prep()
      self.prep_high_score()

  def prep(self):
      self.prep_score()
      self.prep_stats()
      self.prep_level()

  def prep_stats(self):
     
     #Header
     header = "    STATS    "
     self.header_image = self.font.render(header, True, self.text_color, self.game_settings.bg_color)
     self.header_rect = self.score_image.get_rect()
     self.header_rect.left = self.screen_rect.left + 20
     self.header_rect.top += 0
  
     #HP
     hp = "HP        " + str(int(self.player_stats.hp)).zfill(3) # 3 digit stat
     self.hp_image = self.font.render(hp, True, self.text_color, self.game_settings.bg_color)
     self.hp_rect = self.score_image.get_rect()
     self.hp_rect.left = self.screen_rect.left + 20
     self.hp_rect.top += 30

     #Speed
     if(int(self.player_stats.speed)>=5):
        suffix = "MAX"
     else:
        suffix = str(int(self.player_stats.speed)).zfill(3)
     
     speed = "SPEED     " + suffix # 3digit stat
    

     self.speed_image = self.font.render(speed, True, self.text_color, self.game_settings.bg_color)
     self.speed_rect = self.score_image.get_rect()
     self.speed_rect.left = self.screen_rect.left + 20
     self.speed_rect.top += 60

     #Damage
     if(int(self.player_stats.damage)>=10):
        suffix = "MAX"
     else:
        suffix = str(int(self.player_stats.damage)).zfill(3)

     damage = "DAMAGE    " + suffix# 3digit stat


     self.damage_image = self.font.render(damage, True, self.text_color, self.game_settings.bg_color)
     self.damage_rect = self.score_image.get_rect()
     self.damage_rect.left = self.screen_rect.left + 20
     self.damage_rect.top += 90

     #Firerate
     firerate = "FIRERATE  " +str(int(self.player_stats.firerate)).zfill(3) # 3 digit stat
     if self.player.firerate_timer:
        if self.player.firerate_timer.delta <= 2: firerate = "FIRERATE  " + "MAX"
     self.firerate_image = self.font.render(firerate, True, self.text_color, self.game_settings.bg_color)
     self.firerate_rect = self.score_image.get_rect()
     self.firerate_rect.left = self.screen_rect.left + 20
     self.firerate_rect.top += 120


  def prep_score(self):
     tile_score = "Discovered Tiles: " + str(self.game_stats.score).zfill(5)
     self.score_image = self.font.render(tile_score, True, self.text_color, self.game_settings.bg_color)
     self.score_rect = self.score_image.get_rect()
     self.score_rect.right = self.screen_rect.right - 20
     self.score_rect.top += 20

  def prep_high_score(self):
    
    high_score = round(self.game_stats.high_score, -1)
    high_score_str = f"High: {high_score:,}"

    self.high_score_image = self.font.render(high_score_str, True, self.text_color, self.game_settings.bg_color)

    self.high_score_rect = self.high_score_image.get_rect()
    self.high_score_rect.centerx = self.screen_rect.centerx
    self.high_score_rect.top = self.score_rect.top

  def prep_level(self):
    if(self.game_stats.level>1):
       #self.sound.stop_music()
       #self.sound.play_level_up_transition()
       #self.sound.play_main_theme()
       pass

    level_str = f'L {self.game_stats.level}'
    self.level_image = self.font.render(level_str, True, self.text_color, self.game_settings.bg_color)

    self.level_rect = self.level_image.get_rect()
    self.level_rect.right = self.score_rect.right
    self.level_rect.top = self.score_rect.bottom + 10

  def check_high_score(self):
     if self.game_stats.score > self.game_stats.high_score:
        self.game_stats.high_score = self.game_stats.score
        self.prep_high_score()

  def update(self): 
    self.prep()
    self.draw()
    self.game_stats.update()

  def draw(self):
     
    self.screen.blit(self.score_image, self.score_rect)
    self.screen.blit(self.header_image,self.header_rect)
    self.screen.blit(self.hp_image,self.hp_rect)
    self.screen.blit(self.speed_image,self.speed_rect)
    self.screen.blit(self.damage_image,self.damage_rect) 
    self.screen.blit(self.firerate_image,self.firerate_rect)
    self.screen.blit(self.high_score_image, self.high_score_rect)
    self.screen.blit(self.level_image, self.level_rect)

  
    