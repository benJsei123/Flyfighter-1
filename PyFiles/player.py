# from flyfighter_game import Game
from vector import Vector
import pygame as pg
from guns import Guns
from timer import Timer
import math 
from sound import Sound

class Player(pg.sprite.Sprite):

    key_velocity = {pg.K_RIGHT: Vector(1, 0), pg.K_LEFT: Vector(-1,  0),
                  pg.K_UP: Vector(0, -1), pg.K_DOWN: Vector(0, 1)}
    

    def __init__(self, game, group) -> None:
        super().__init__(group)
        self.game = game

        self.direction = Vector(0,0)
        self.player_stats = PlayerStats(game = self.game)
        
        self.guns = Guns(game=self.game,owner=self)
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
        self.bullet_start_rect = None
        self.game_settings = None
        self.timer = None
        self.map = None
        self.screen_rect = None
        self.screen = None
        self.background_surface = None
        self.mask = None
        self.firerate_timer = None
        

    def init_missing_attributes(self):
        self.game_settings = self.game.game_settings
        self.original_image = pg.image.load(self.game_settings.image_paths["player"]).convert_alpha() #stays the same (no rotation)
        self.image = self.original_image #this image will be a rotated version of original image
        self.rect = self.image.get_rect()
        self.rect.center = (600,600)
        self.bullet_start_rect = self.rect #TODO maybe adjust this
        self.dying_timer = Timer(
            image_list = [pg.image.load(img).convert_alpha() for img in self.game_settings.animation_sequences["player_dying"]],
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
        self.mask = pg.mask.from_surface(self.original_image) #TODO Consider resetting self.mask = pg.mask.from_surface(self.original_image) after each rotation or movement 
        self.firerate_timer = Timer(list(range(30)), start_index=0, delta=30, looponce=False)


    def reset(self):
        # Setze die Spielereigenschaften zurück
        self.player_stats.reset()  # Oder was auch immer der Startwert sein soll
       
        # Setze den Spieler zurück in die Mitte oder einen anderen Startpunkt
        self.rect.center = (600, 600)  # Oder eine andere spezifische Startposition
        
        # Setze die Richtung und den Winkel des Spielers zurück
        self.direction = Vector(0, 0)
        self.angle = 0  # Rückkehr zur Ausgangsausrichtung
        
        # Stelle das Ursprungsbild und die Maske wieder her
        self.image = self.original_image
        self.mask = pg.mask.from_surface(self.original_image)
        
        # Wenn es eine Animation oder einen Zustand gibt, der zurückgesetzt werden muss
        self.isdying = False
        
        # Stoppe jegliches Feuern, falls aktiv
        self.firing = False
        
        # Setze Waffen und andere Komponenten zurück, wenn nötig
        self.guns.reset()  
        
        self.dying_timer = Timer(
            image_list = [pg.image.load(img).convert_alpha() for img in self.game_settings.animation_sequences["player_dying"]],
            start_index=0, 
            delta=6, 
            looponce=True 
            )
        self.firerate_timer = Timer(list(range(30)), start_index=0, delta=30, looponce=False)
        # Positioniere das Schiff im Zentrum des Bildschirms oder an einem anderen Startpunkt
        self.center_ship()


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
        if(self.player_stats.hp <= 0):
            self.explode()

        self.input()

        if self.direction.magnitude() > 0 and self.direction!=self.last_set_direction:
            #adjusting angle
            self.angle = math.degrees(math.atan2(-self.direction.y, -self.direction.x))
            self.rotate() #rotates considering the newly set angle
            self.last_set_direction = self.direction # to make sure to only rotate if really necessary

        # Aktualisiere die Position des Schiffs
        self.bullet_start_rect = self.rect
        self.rect.x += self.direction.x * (self.player_stats.speed+2)
        self.rect.y += self.direction.y * (self.player_stats.speed+2)


        #Firing and firerate
        
        self.firerate_timer.delta = 20 - (self.player_stats.firerate//0.2)
        if self.firerate_timer.delta < 2: self.firerate_timer.delta = 2
        if self.firing:
            # Prüfen Sie, ob der Timer abgelaufen ist
            if self.firerate_timer.current_image() == 0:
                self.fire()
                # Timer zurücksetzen
                self.firerate_timer.index = int(self.firerate_timer.delta)

        # Aktualisieren des Timers
        if self.firerate_timer.index > 0:
            self.firerate_timer.index -= 1

        #Bullet movement
        self.guns.update()

        if(self.isdying ==True):
            print("isdying")
            self.image= self.dying_timer.current_image()
            print(self.image)

    

    def fire(self):
        # Feuerlogik, die abgefeuerte Geschosse hinzufügt
        if self.last_set_direction.magnitude() > 0:  # avoids shooting "standing" bullets that don't move
            self.guns.add(owner=self, direction=self.last_set_direction)
            self.sound.play_bullet_sound()


    def explode(self):

        if self.isdying==False: 
            self.isdying = True
            self.sound.play_player_explosion_sound()

        if(self.dying_timer.finished()):
            self.sound.play_gameover()
            self.game_stats.save_highscore()
            self.game.game_over()


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
        self.sound = Sound()

        self.hp = 20
        self.speed = 1
        self.firerate = 1
        self.damage = 1
        
    def reset(self):
        self.hp = 20
        self.speed = 1
        self.firerate = 1 
        self.damage = 1
        
    def hp_levelup(self, amnt):
        if(self.hp <= 100): self.hp += amnt

    def firerate_levelup(self, amnt):
        self.firerate += amnt #limit already set in update() method (checks delta value of fire_timer)

    def speed_levelup(self, amnt):
        if(self.speed <= 5): self.speed += amnt

    def damage_levelup(self, amnt):
        if(self.damage <= 10): self.damage += amnt

    def take_damage(self,amnt):
        if(self.hp>=0):
            self.hp -= amnt
            self.sound.play_player_hit_sound()