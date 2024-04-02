import pygame as pg
from pygame.sprite import Sprite
from sound import Sound
import math

# Import Vector, Timer, Sound nach Bedarf, falls verwendet

class Bullet(Sprite):


    def __init__(self, game, v, owner, camera_group, sort='default'):
        super().__init__(camera_group)
        self.game = game
        self.screen = game.screen
        self.game_settings = game.game_settings

        #or sort choose from default, shotgun, laser, freezer
        self.v = v * self.game_settings.bullet_speed #TODO give this thing a certain multiplyer depending on sort of bullet
        self.angle = 0

        self.owner = owner
        self.original_image = pg.image.load(self.game_settings.image_paths[f'{sort}_bullet']).convert_alpha() 
        
        self.angle = math.degrees(math.atan2(-self.v.y, -self.v.x))
        self.image = pg.transform.rotate(self.original_image, -self.angle)  # Negativer Winkel für die Pygame-Koordinaten
        self.rect = self.image.get_rect(center=owner.rect.center)
        
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)


        #For collisions with tiles
        self.mask = pg.mask.from_surface(self. original_image)
    

    def update(self):
        self.x += self.v.x
        self.y += self.v.y
        
        self.rect.x = self.x
        self.rect.y = self.y


class Guns():  # Analog zu Lasers, aber für Bullets
    def __init__(self, game, owner):
        self.game = game
        self.screen = game.screen
        self.settings = game.game_settings
        self.camera_group = game.camera_group
        
        #self.v = v  # bullet velocity, can be up or down
        self.owner = owner  # the object shooting the bullet
        self.bullet_group = pg.sprite.Group()
        
        self.sound = Sound()  # assuming you have a Sound class for playing bullet sounds

    def bulletgroup(self): 
        return self.bullet_group

    def add(self, owner, direction, sort='default'):
        new_bullet = Bullet(game=self.game, v=direction, owner=owner, camera_group=self.camera_group, sort='default')
        self.bullet_group.add(new_bullet)

    def empty(self): 
        self.bullet_group.empty()

    def update(self):
        for bullet in self.bullet_group.sprites():
            bullet.update()

    def reset(self):
        for bullet in self.bullet_group:
            bullet.kill()
        self.bullet_group.empty()