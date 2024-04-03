from pygame.sprite import Group, Sprite
import pygame as pg
from abc import ABC, abstractmethod
from guns import Guns
import random
from timer import Timer
from sound import Sound
from vector import Vector

class PowerupManager:
    def __init__(self, game) -> None:
        self.game = game
        self.game_settings = game.game_settings
        self.player = None
        self.pu_group = pg.sprite.Group()
        
    def update(self):
        for powerup in self.pu_group:
            powerup.update()

    def set_player(self,player):
        self.player = player

    def get_random_powerup(self, pos:tuple):
        """ used to get a random powerup object to let it spawn on a tile (see MapTile class)"""
        
        rand_num = random.randint(0,3)
        random_powerup = None
        if(rand_num==0): random_powerup = self.get_speed_powerup(pos)
        if(rand_num==1): random_powerup = self.get_hp_powerup(pos)
        if(rand_num==2): random_powerup = self.get_firerate_powerup(pos)
        if(rand_num==3): random_powerup = self.get_damage_powerup(pos)
        print("Got random powerup of type", type(random_powerup))
        self.pu_group.add(random_powerup)
        return random_powerup
        
    def get_speed_powerup(self, pos):
        image_list = [pg.image.load(path) for path in self.game_settings.animation_sequences["speed_powerup_idle"] ]
        idle_timer = Timer(image_list, start_index=0, delta=3, looponce=False)
        return SpeedPowerup(self.game, self.game.camera_group, pos_x=pos[0], pos_y=pos[1],idle_timer=idle_timer)

    def get_hp_powerup(self, pos):
        image_list = [pg.image.load(path) for path in self.game_settings.animation_sequences["hp_powerup_idle"] ]
        idle_timer = Timer(image_list, start_index=0, delta=3, looponce=False)
        return HP_Powerup(self.game, self.game.camera_group, pos_x=pos[0], pos_y=pos[1], idle_timer=idle_timer)

    def get_firerate_powerup(self, pos):
        image_list = [pg.image.load(path) for path in self.game_settings.animation_sequences["firerate_powerup_idle"] ]
        idle_timer = Timer(image_list, start_index=0, delta=3, looponce=False)
        return FireratePowerup(self.game, self.game.camera_group, pos_x=pos[0], pos_y=pos[1], idle_timer=idle_timer)

    def get_damage_powerup(self, pos):
        image_list = [pg.image.load(path) for path in self.game_settings.animation_sequences["damage_powerup_idle"] ]
        idle_timer = Timer(image_list, start_index=0, delta=3, looponce=False)
        return DamagePowerup(self.game, self.game.camera_group, pos_x=pos[0], pos_y=pos[1], idle_timer=idle_timer)

    def get_current_powerups(self):
        return self.pu_group
    
    def reset(self):
        for pu in self.pu_group:
            pu.kill()
        self.pu_group.empty()


class Powerup(Sprite, ABC):
    
    
    def __init__(self, game,camera_group, pos_x,pos_y, idle_timer) -> None:
        super().__init__(camera_group)
        self.game = game
        self.player = game.player
        self.player_rect = self.game.player.rect
        self.game_settings = game.game_settings
        self.screen = game.screen
        self.rect = None
        self.sound = Sound()

        self.start_pos_x = pos_x
        self.start_pos_y = pos_y
        self.idle_timer = idle_timer

    @abstractmethod
    def update(self):
        pass

    @abstractmethod
    def collect(self):
        pass

class SpeedPowerup(Powerup):
    def __init__(self, game, camera_group, pos_x,pos_y,idle_timer) -> None:
        super().__init__(game=game,camera_group=camera_group, pos_x=pos_x,pos_y=pos_y,idle_timer=idle_timer)
        self.image = self.idle_timer.current_image()
        self.rect = self.image.get_rect()
        self.speed_points = self.game_settings.speed_powerup_points
        
        self.rect.center=(self.start_pos_x,self.start_pos_y)
        
        self.mask = pg.mask.from_surface(self.image)
          
    def update(self):
        self.image = self.idle_timer.current_image()

    def collect(self):
        self.game.player.player_stats.speed_levelup(self.speed_points) 
        self.sound.play_powerup_sound()
        self.kill()


class FireratePowerup(Powerup):
    def __init__(self, game, camera_group, pos_x,pos_y,idle_timer) -> None:
        super().__init__(game=game,camera_group=camera_group, pos_x=pos_x,pos_y=pos_y,idle_timer=idle_timer)
        self.image = self.idle_timer.current_image()
        self.rect = self.image.get_rect()
        self.firerate_points = self.game_settings.firerate_powerup_points
        self.rect.center=(self.start_pos_x,self.start_pos_y)

        self.mask = pg.mask.from_surface(self. image)
    
    def update(self):
        self.image = self.idle_timer.current_image()

    def collect(self):
        self.game.player.player_stats.firerate_levelup(self.firerate_points) 
        self.sound.play_powerup_sound()
        self.kill()

class HP_Powerup(Powerup):

    def __init__(self, game, camera_group, pos_x,pos_y,idle_timer) -> None:
        super().__init__(game=game,camera_group=camera_group, pos_x=pos_x,pos_y=pos_y,idle_timer=idle_timer)
        self.image = self.idle_timer.current_image()
        self.rect = self.image.get_rect()
        self.hp_points = game.game_settings.hp_powerup_points
        
        self.rect.center=(self.start_pos_x,self.start_pos_y)

        self.guns = Guns(game=self.game,owner=self)
        self.mask = pg.mask.from_surface(self.image)

    def update(self):
        self.image = self.idle_timer.current_image()
    
    def collect(self):
        self.game.player.player_stats.hp_levelup(self.hp_points)
        self.sound.play_powerup_sound()
        self.kill()


class DamagePowerup(Powerup):

    def __init__(self, game, camera_group, pos_x,pos_y,idle_timer) -> None:
        super().__init__(game=game,camera_group=camera_group, pos_x=pos_x,pos_y=pos_y,idle_timer=idle_timer)
        self.image = self.idle_timer.current_image()
        self.rect = self.image.get_rect()
        self.damage_points = game.game_settings.damage_powerup_points
        
        self.rect.center=(self.start_pos_x,self.start_pos_y)

        self.mask = pg.mask.from_surface(self.image)

    def update(self):
        self.image = self.idle_timer.current_image()

    def collect(self):
        self.game.player.player_stats.damage += self.damage_points
        self.sound.play_powerup_sound()
        self.kill()

