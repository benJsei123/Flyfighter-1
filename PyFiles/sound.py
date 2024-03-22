from pygame import mixer
import time
import random

class Sound: 
    def __init__(self) -> None:
        mixer.init()
        mixer.set_num_channels(32)
        #mixer.music.load('sounds/main_theme.mp3')
        self.game_over_sound = 0.5
        self.music_volume = 0.2


    #     self.phaser_sound = self.make_sound("laser", 0.1)


    #     self.explosion_sound = self.make_sound("explosion", 1)
    #     # self.set_sound_volume(self.explosion_sound, 0.5)

    #     self.game_over_sound = self.make_sound("gameover")
    #     self.set_sound_volume(self.game_over_sound, 1)

    #     self.levelup_sound = self.make_sound("levelup")
    #     self.set_sound_volume(self.levelup_sound, 1)

    #     self.ufo_spawn_sound = self.make_sound("ufo_spawn", 0.4)
        
    #     # self.main_theme = self.make_sound("main_theme")
        
    #     self.alien_kill_sound = self.make_sound("alien_kill")

        
    #     self.set_music_volume(self.music_volume)

    # def play_main_theme(self):
    #     self.stop_music()
    #     mixer.music.load("sounds/main_theme.mp3")
    #     mixer.music.play(-1)

    # def pause_music(self):
    #     mixer.music.pause()

    # def unpause_music(self):
    #     mixer.music.unpause()

    # def stop_music(self):
    #     mixer.music.stop()

    # def set_music_volume(self, vol):
    #     mixer.music.set_volume(vol)
        
    # def set_sound_volume(self,sound:mixer.Sound, new_vol):
    #     sound.set_volume(new_vol)

    # def play_level_up_transition(self):
    #     channel = mixer.find_channel(True)
    #     if channel is not None:
    #         channel.play(self.levelup_sound)
    
    # def play_phaser(self):
    #     #using this channel thing cause so many sounds at once
    #     channel = mixer.find_channel(True)
    #     if channel is not None:
    #         channel.play(self.phaser_sound)
    
    # def play_gameover(self):
    #     self.stop_music()
    #     self.game_over_sound.play()
    
    # def play_explosion(self):
    #     channel = mixer.find_channel(True)
    #     if channel is not None:
    #         channel.play(self.explosion_sound)

    # def play_ufo_spawn(self):
    #     channel = mixer.find_channel(True)
    #     if channel is not None:
    #         channel.play(self.ufo_spawn_sound)
        
    
    # def play_alien_kill(self):
    #     #using this channel thing cause so many sounds at once
    #     channel = mixer.find_channel(True)
    #     if channel is not None:
    #         channel.play(self.alien_kill_sound)

    # def make_sound(self, name, volume=1):
    #     sound = mixer.Sound(f"sounds/{name}.mp3")
    #     sound.set_volume(volume)
    #     return sound


