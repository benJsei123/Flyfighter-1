from pygame.sprite import Group, Sprite
import pygame as pg
from abc import ABC, abstractmethod
from guns import Guns
import random
from timer import Timer
from vector import Vector
from sound import Sound

class EnemyManager:
    def __init__(self, game) -> None:
        self.game = game
        self.game_settings = game.game_settings
        self.player = None
        self.enemy_group = pg.sprite.Group()
        
    def update(self):
        for enemy in self.enemy_group:
            enemy.update()

    def set_player(self,player):
        self.player = player

    def get_random_enemy(self, pos:tuple):
        """ used to get a random enemy object to let it spawn on a tile (see MapTile class)"""
        
        rand_num = random.randint(0,2)
        random_enemy = None
        if(rand_num==0): random_enemy = self.get_fast_enemy(pos)
        if(rand_num==1): random_enemy = self.get_tanky_enemy(pos)
        if(rand_num==2): random_enemy = self.get_smart_enemy(pos)

        self.enemy_group.add(random_enemy)
        return random_enemy
        
    def get_fast_enemy(self, pos):
        image_list = [pg.image.load(path) for path in self.game_settings.animation_sequences["fast_enemy_idle"] ]
        idle_timer = Timer(image_list, start_index=0, delta=15, looponce=False)
        return FastEnemy(self.game, self.game.camera_group, pos_x=pos[0], pos_y=pos[1],idle_timer=idle_timer)

    def get_tanky_enemy(self, pos):
        image_list = [pg.image.load(path) for path in self.game_settings.animation_sequences["tanky_enemy_idle"] ]
        idle_timer = Timer(image_list, start_index=0, delta=20, looponce=False)
        return TankyEnemy(self.game, self.game.camera_group, pos_x=pos[0], pos_y=pos[1], idle_timer=idle_timer)

    def get_smart_enemy(self, pos):
        image_list = [pg.image.load(path) for path in self.game_settings.animation_sequences["smart_enemy_idle"] ]
        idle_timer = Timer(image_list, start_index=0, delta=5, looponce=False)
        return SmartEnemy(self.game, self.game.camera_group, pos_x=pos[0], pos_y=pos[1], idle_timer=idle_timer)

    def get_current_enemies(self):
        return self.enemy_group
    
    def reset(self):
        for enemy in self.enemy_group:
            enemy.guns.reset()
            enemy.kill()
        self.enemy_group.empty()


class Enemy(Sprite, ABC):
    
    def __init__(self, game,camera_group, pos_x,pos_y, idle_timer) -> None:
        super().__init__(camera_group)
        self.game = game
        self.player = game.player
        self.player_rect = self.game.player.rect
        self.game_settings = game.game_settings
        self.screen = game.screen
        self.rect = None
        self.guns = None
        self.fire_direction = None
        self.hp = game.game_settings.enemy_hp
        self.last_enemy_pos_x = pos_x
        self.last_enemy_pos_y = pos_y
        self.start_pos_x = pos_x
        self.start_pos_y = pos_y
        self.slowness = 1
        self.idle_timer = idle_timer
        self.sound = Sound()

    @abstractmethod
    def update(self):
        pass

    @abstractmethod
    def fire(self):
        pass

    def get_fire_direction(self):
        """Returns vector from to player"""
        self.player_rect = self.player.rect #update player rect
        v = Vector(self.player_rect.x-self.rect.x,self.player_rect.y-self.rect.y)/1000 * self.game_settings.enemy_bullet_speed #these vectors are huge, gotta scale them down 
        return v
    
    
    def slow_down(self):
        """Function used to slow  down an enemy. Why? The way that enemy-enemy collisions work would
        make both enemies stop as soon as they collide. Therefore the enemy that isfarther away from 
        player has to be slowed down to not make the closer one get stuck"""
        if(self.slowness<10):
            self.slowness += 1

    def take_damage(self):
        self.hp-= self.player.player_stats.damage
        if(self.hp <= 0):
            #if(self.guns):self.guns.reset() #remove bulles 
            self.guns=None
            self.kill()
            self.sound.play_enemy_dead_sound()

class FastEnemy(Enemy):

    #image_list

    def __init__(self, game, camera_group, pos_x,pos_y,idle_timer) -> None:
        super().__init__(game=game,camera_group=camera_group, pos_x=pos_x,pos_y=pos_y,idle_timer=idle_timer)
        self.image = self.idle_timer.current_image()
        self.rect = self.image.get_rect()
        
        self.rect.center=(self.start_pos_x,self.start_pos_y)
        
        self.guns = Guns(game=self.game,owner=self)
        self.mask = pg.mask.from_surface(self.image)
        
    def move_to_player(self):
        dir = self.get_move_direction()
        new_pos =  (self.rect.center[0] + dir.x * self.game_settings.fast_enemy_speed, self.rect.center[1] + dir.y  * self.game_settings.fast_enemy_speed)
        self.rect.center = new_pos

    def get_move_direction(self):
        """Returns vector from to player"""
        self.player_rect = self.player.rect #update player rect
        v = Vector(self.player_rect.x-self.rect.x,self.player_rect.y-self.rect.y)/1000 * self.game_settings.enemy_bullet_speed * (1/self.slowness)#these vectors are huge, gotta scale them down 
        return v
    
    def update(self):
        self.move_to_player()
        self.image = self.idle_timer.current_image()

    def fire(self):
        self.fire_direction = self.get_fire_direction()
        self.guns.add(owner=self,direction=self.fire_direction,sort='default')

class SmartEnemy(Enemy):
    def __init__(self, game, camera_group, pos_x,pos_y,idle_timer) -> None:
        super().__init__(game=game,camera_group=camera_group, pos_x=pos_x,pos_y=pos_y,idle_timer=idle_timer)
        self.image = self.idle_timer.current_image()
        self.rect = self.image.get_rect()
        
        self.rect.center=(self.start_pos_x,self.start_pos_y)

        self.guns = Guns(game=self.game,owner=self)
        self.mask = pg.mask.from_surface(self. image)
        
    def fire(self):
        self.fire_direction = self.get_fire_direction()
        self.guns.add(owner=self,direction=self.fire_direction,sort='default')

    def update(self):
        self.image = self.idle_timer.current_image()
        pass #TODO Implement Logic


class TankyEnemy(Enemy):

    def __init__(self, game, camera_group, pos_x,pos_y,idle_timer) -> None:
        super().__init__(game=game,camera_group=camera_group, pos_x=pos_x,pos_y=pos_y,idle_timer=idle_timer)
        self.image = self.idle_timer.current_image()
        self.rect = self.image.get_rect()
        self.hp = game.game_settings.tanky_enemy_hp
        
        self.rect.center=(self.start_pos_x,self.start_pos_y)

        self.guns = Guns(game=self.game,owner=self)
        self.mask = pg.mask.from_surface(self.image)

    def fire(self):
        self.fire_direction = self.get_fire_direction()
        self.guns.add(owner=self,direction=self.fire_direction,sort='default')

    def update(self):
        self.image = self.idle_timer.current_image()



