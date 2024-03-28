import pygame as pg
from pygame.sprite import Sprite
from sound import Sound

# Import Vector, Timer, Sound nach Bedarf, falls verwendet

class Bullet(Sprite):


    def __init__(self, game, v, owner, camera_group, sort='default'):
        super().__init__(camera_group)
        self.game = game
        self.screen = game.screen
        self.settings = game.game_settings


        #or sort choose from default, shotgun, laser, freezer
        self.v = v *100 #TODO give this thing a certain multiplyer depending on sort of bullet
        self.owner = owner
        self.image = pg.image.load(self.settings.image_paths[f'{sort}_bullet']) 

        self.rect = owner.bullet_start_rect
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)

    def update(self):
        self.x += self.v.x
        self.y += self.v.y
        
        self.rect.x = self.x
        self.rect.y = self.y

        self.draw()


    def draw(self): 
        self.screen.blit(self.image, self.rect)


class Guns():  # Analog zu Lasers, aber für Bullets
    def __init__(self, game, v, owner):
        self.game = game
        self.screen = game.screen
        self.settings = game.game_settings
        self.camera_group = game.camera_group
        
        self.v = v  # bullet velocity, can be up or down
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
