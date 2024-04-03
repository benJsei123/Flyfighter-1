from pygame import mixer
import time
import random

class Sound: 
    def __init__(self) -> None:
        mixer.init()
        mixer.set_num_channels(32)
        self.game_over_sound = 0.5
        self.music_volume = 0.2


        self.bullet_sound = self.make_sound("bullet_sound", 0.1)
        self.enemy_dead_sound = self.make_sound("enemy_dead", 0.2)
        # self.set_volume(self.enemy_dead_sound, 0.5)
        self.game_over_sound = self.make_sound("game_over_sound")
        self.set_sound_volume(self.game_over_sound, 1)
        self.tile_discovered_sound = self.make_sound("tile_discovered")
        self.set_sound_volume(self.tile_discovered_sound, 1)
        self.player_explosion_sound = self.make_sound("player_explosion", 0.4)
        self.powerup_sound = self.make_sound("powerup_collected")

        self.player_hit_sound = self.make_sound("player_hit", 0.4)

        self.set_music_volume(self.music_volume)

    def play_ambience_music(self):
        self.stop_music()
        mixer.music.load("Resources/sounds/AmbienceMusic.mp3")
        mixer.music.set_volume(5.0)
        mixer.music.play(-1)

    def play_launchscreen_theme(self):
        self.stop_music()
        mixer.music.load("Resources/sounds/LaunchscreenMusic.mp3")
        mixer.music.play(-1)

    def pause_music(self):
        mixer.music.pause()

    def unpause_music(self):
        mixer.music.unpause()

    def stop_music(self):
        mixer.music.stop()

    def set_music_volume(self, vol):
        mixer.music.set_volume(vol)
        
    def set_sound_volume(self,sound:mixer.Sound, new_vol):
        sound.set_volume(new_vol)


    def play_powerup_sound(self):
        channel = mixer.find_channel(True)
        if channel is not None:
            channel.play(self.powerup_sound)
    
    def play_bullet_sound(self):
        #using this channel thing cause so many sounds at once
        channel = mixer.find_channel(True)
        if channel is not None:
            channel.play(self.bullet_sound)
    
    def play_gameover(self):
        self.stop_music()
        self.game_over_sound.play()
    
    def play_player_explosion_sound(self):
        channel = mixer.find_channel(True)
        if channel is not None:
            channel.play(self.player_explosion_sound)

    def play_player_hit_sound(self):
        channel = mixer.find_channel(True)
        if channel is not None:
            channel.play(self.player_hit_sound)

    def play_enemy_dead_sound(self):
        channel = mixer.find_channel(True)
        if channel is not None:
            channel.play(self.enemy_dead_sound)
        
    def play_tile_discovered_sound(self):
        #using this channel thing cause so many sounds at once
        channel = mixer.find_channel(True)
        if channel is not None:
            channel.play(self.tile_discovered_sound)


    def make_sound(self, name, volume=1):
        sound = mixer.Sound(f"Resources/sounds/{name}.mp3")
        sound.set_volume(volume)
        return sound


