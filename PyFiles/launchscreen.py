import pygame as pg
import sys
from button import Button
import time


class Launchscreen:
    def __init__(self, game) -> None:
        self.font = pg.font.Font(None, 36)
        self.game = game
        self.screen = game.screen
        #self.sound = game.sound
        self.game_settings = self.game.game_settings
        self.in_launch_screen = True
        self.screen_rect = self.game.screen.get_rect() 
        self.colors = {"white":(255,255,255),
                    "green": (0,244,0),
                    "red": (255,0,0),
                    "light_grey" : (180,180,180),
                    "black": (0,0,0)
                    } 


        #fonts
        font_path = 'Resources/font.ttf'  
        self.title_font = pg.font.Font(font_path, 100)
        self.hs_font = pg.font.Font(font_path, 40)
        self.info_font = pg.font.Font(font_path, 25)

        #title text
        title_text_first_line = "   F L Y   "
        self.title_surface_1stline = self.title_font.render(title_text_first_line, True, self.colors["white"])
        self.title_rect_1stline = self.title_surface_1stline.get_rect(center=(self.game_settings.screen_width // 2, self.game_settings.screen_height - 600))
        title_text_second_line = "F I G H T E R"
        self.title_surface_2ndline = self.title_font.render(title_text_second_line, True, self.colors["white"])
        self.title_rect_2ndline = self.title_surface_2ndline.get_rect(center=(self.game_settings.screen_width // 2, self.game_settings.screen_height - 490 ))

        #Buttons
        play_button_pos = (self.screen_rect.center[0], self.screen_rect.center[1] -20)
        hs_button_pos = (self.screen_rect.center[0], self.screen_rect.center[1] + 40)
        self.play_button = Button(game=self.game, text='Play', pos=play_button_pos)
        self.highscore_button = Button(game=self.game, text="View Highscore", pos=hs_button_pos, bg_color= self.colors["white"], selected_color=self.colors["light_grey"], text_color=self.colors["black"])


        #alien pictures
        self.points = [10,20,30]
        


        #flags
        self.high_score_surface = None
        self.current_highscore_rect = None
        self.showing_highscore = False

    def show(self):  
        pg.event.set_grab(False)
        pg.mouse.set_visible(True)
        self.play_button.show()
        #self.sound.stop_music()
        self.highscore_button.show()  
        self.in_launch_screen = True
        while self.in_launch_screen:
            self.screen.fill((0, 0, 0))
                    
            self.check_events()
            

            if(self.showing_highscore): 
                current_highsscore = str(self.game.game_stats.high_score)
                self.high_score_surface = self.hs_font.render(current_highsscore, True, self.colors["white"])
                self.current_highscore_rect = self.high_score_surface.get_rect(center=(self.game_settings.screen_width // 2, self.game_settings.screen_height - 230 ))
                self.screen.blit(self.high_score_surface, self.current_highscore_rect)

            self.screen.blit(self.title_surface_1stline,self.title_rect_1stline)
            self.screen.blit(self.title_surface_2ndline,self.title_rect_2ndline)
            #self.display_aliens(self.screen)
            self.play_button.update()  
            self.highscore_button.update()
            pg.display.flip()
            time.sleep(0.02)
            #print("self.in_launch_screen is ",self.in_launch_screen )
        print("Launchscreen Loop ended")

    def draw_alien_info(self, screen, x, y, image, name, points):
        # Alien-Bild laden und zeichnen
        alien_image = image
        alien_rect = alien_image.get_rect()
        alien_rect.x = x
        alien_rect.y = y
        screen.blit(alien_image, alien_rect)

        # Name und Punkte unter dem Bild zeichnen
        name_surface = self.info_font.render(name, True, self.colors["white"])
        points_surface = self.info_font.render(f"Points: {points}", True, self.colors["white"])
        
        # Positionen für Name und Punkte berechnen und zeichnen
        screen.blit(name_surface, (x, y + alien_rect.height + 5))
        screen.blit(points_surface, (x, y + alien_rect.height + 5 + 25 + 5)) #25 is font size of self.info_font

    def display_aliens(self,screen):
        margin = 90
        alien_width = 90 
        start_x = (self.game_settings.screen_width - (len(Alien.images) * alien_width + (len(Alien.images) - 1) * margin)) // 2
        y = self.game_settings.screen_height - 200 

        for i, (image, name, points) in enumerate(zip(Alien.images, Alien.names, Alien.points)):
            x = start_x + i * (alien_width + margin)
            self.draw_alien_info(screen, x, y, image, name, points)      

    def check_events(self):
         for event in pg.event.get():
                type = event.type
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()
                elif type == pg.KEYDOWN:
                    key = event.key
                    if key == pg.K_p: 
                    
                        self.play_button.select(True)
                        self.play_button.press()
                        self.exit_launch_screen()
                        pg.event.clear() #no old events in events
                elif type == pg.MOUSEBUTTONDOWN:

                    x, y = pg.mouse.get_pos()
                    #print(f"mouse_button down at {x}, {y}")
                    #Checking for play button
                    b = self.play_button
                    
                    if b.rect.collidepoint(x, y):

                        print("PLAY Button pressed")
                        b.press()
                        self.game.activate() # HAS TO BE AFTER self.game.restart if statemen !!
                        self.exit_launch_screen()
                        pg.event.clear() #no old events in events
                        pg.mouse.set_visible(False)
                    
                    #Checking for highscore button
                    b = self.highscore_button
                    if b.rect.collidepoint(x, y):
                        self.showing_highscore= not self.showing_highscore
                        

                elif type == pg.MOUSEMOTION:
                    x, y = pg.mouse.get_pos()
                    
                    #For playbutton
                    b = self.play_button
                    b.select(b.rect.collidepoint(x, y))

                    #For hs button
                    b = self.highscore_button
                    b.select(b.rect.collidepoint(x, y))
                    


    def exit_launch_screen(self):
        print("Exit launchscreen called")
        self.in_launch_screen = False
        pg.event.clear() #no old events in events

  