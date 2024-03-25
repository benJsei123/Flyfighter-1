# from flyfighter_game import Game
from vector import Vector
import pygame as pg
from guns import Guns
from timer import Timer
import math 
from camera import CameraGroup

class Player(pg.sprite.Sprite):

    key_velocity = {pg.K_RIGHT: Vector(1, 0), pg.K_LEFT: Vector(-1,  0),
                  pg.K_UP: Vector(0, -1), pg.K_DOWN: Vector(0, 1)}
    

    def __init__(self, game, group) -> None:
        super().__init__(group)
        self.game = game

        self.direction = Vector(0,0)
        self.player_stats = PlayerStats(game = self.game)
        

        self.guns = Guns(game=self.game)
        self.firing = False
        
        #Animation stuff
        self.isdying = False

        #Navigation
        self.angle = 0
        self.speed = 5
        self.last_set_direction = Vector(0,0) #to check if direction has changed (for mor efficient rotation)


        #Initialized after instantiation in game class (order issues)
        self.image = None
        self.sound = None
        self.rect = None
        self.game_settings = None
        self.timer = None
        self.map = None
        self.screen_rect = None
        self.screen = None
        self.background_surface = None
        self.camera_group = None


    def init_missing_attributes(self):
        self.game_settings = self.game.game_settings
        self.original_image = pg.image.load(self.game_settings.image_paths["player"]) #stays the same (no rotation)
        self.image = self.original_image #this image will be a rotated version of original image
        self.rect = self.image.get_rect()
        self.dying_timer = Timer(
            image_list = self.game_settings.animation_sequences["player_dying"], 
            start_index=0, 
            delta=6, 
            looponce=True 
            )
        self.map = self.game.map
        self.game_stats = self.game.game_stats
        self.sound = self.game.sound
        self.screen = self.game.screen
        self.screen_rect = self.screen.get_rect()
        self.center_ship()
        self.background_surface = self.game.background_surface

    def get_tile_standing_on(self)->tuple:
        """Returns position of tile which player stands on currently"""
        return (0,0)
        #TODO implement
    

    def input(self):
        keys = pg.key.get_pressed()
        if keys[pg.K_UP]:
            self.direction.y = -1
        elif keys[pg.K_DOWN]:
            self.direction.y = 1
        else:
            self.direction.y = 0

        if keys[pg.K_RIGHT]:
            self.direction.x = 1
        elif keys[pg.K_LEFT]:
            self.direction.x = -1
        else:
            self.direction.x = 0
    

    def update(self):
        
        self.input()

        if self.direction.magnitude() > 0 and self.direction!=self.last_set_direction:
            #adjusting angle
            self.angle = math.degrees(math.atan2(-self.direction.y, -self.direction.x))
            self.rotate() #rotates considering the newly set angle
            self.last_set_direction = self.direction # to make sure to only rotate if really necessary

        # Aktualisiere die Position des Schiffs
        self.rect.x += self.direction.x * self.player_stats.speed
        self.rect.y += self.direction.y * self.player_stats.speed

        self.draw()

    def draw(self):
        self.screen.blit(self.image, self.rect)

    def handle_input(self, event):
        """handle input and set direction"""
        if event.type == pg.KEYDOWN:
            if event.key in Player.key_velocity:
                self.direction = Player.key_velocity[event.key]
                

        elif event.type == pg.KEYUP:
            if event.key in Player.key_velocity.keys():  
                # stop move
                self.direction = Vector(0, 0)

    def rotate(self):
        if self.original_image:
            # Rotiere das Originalbild um den aktuellen Winkel und erzeuge ein neues Bild
            self.image = pg.transform.rotate(self.original_image, -self.angle)  # Negativer Winkel für die Pygame-Koordinaten
            self.rect = self.image.get_rect(center=self.rect.center)  # Zentriere das neue Bild

    def center_ship(self): 
        self.rect.center = self.screen_rect.center
        

class PlayerStats:
    def __init__(self, game) -> None:
        self.game = game

        self.hp = 100
        self.fire_rate = 10 
        self.speed = 10
        
    def hp_levelup(self, amnt):
        self.hp += amnt

    def fire_rate_levelup(self, amnt):
        self.fire_rate += amnt

    def speed_levelup(self, amnt):
        self.speed += amnt