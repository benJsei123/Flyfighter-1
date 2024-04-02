class GameStats:
    def __init__(self,game) -> None:
        self.game = game

        #CAUTION DONT ADD PLAYER 

        self.difficulty_level = 1

        self.score = 0
        self.level = 1
        self.high_score = self.load_highscore()

    def reset(self):
        self.save_highscore()
        self.score = 0
        self.difficulty_level = 1
        self.level = 1
        self.load_highscore()
    
    def load_highscore(self):
        """ has to load highscore from file and return it"""
        return 99999999999
        #TODO implement
    
    def save_highscore(self):
        """ Has to take current sore and compare to what is in fil, then decide if writes score to file"""
        pass

    def update(self):
        """Called by scoreboard's update to make sure the level increases every 5 tiles"""
        last_level = self.level
        self.level = self.score//1
        self.difficulty_level = self.level


        #If level was increased in this update call:
        if last_level-self.level!=0: 
            #reinitialize with the updated difficulty level (make game harder) 
            self.game.game_settings.initialize_dynamic_settings()

