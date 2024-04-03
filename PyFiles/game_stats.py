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
        """Loads highscore and returns"""
        try:
            with open('highscore.txt', 'r') as file:
                highscore = file.read().strip()
                return int(highscore)
        except (IOError, ValueError):
            return 0


    def save_highscore(self):
        """COmpares current score with highscore and if required writes highscore to highsocre.txt"""
        current_score = self.score 
        highscore = self.load_highscore() 
        if current_score > highscore:
            
            try:
                with open('highscore.txt', 'w') as file:
                    file.write(str(current_score))
                print("New highscore saved successfully")
            except IOError as e:
                print(f"Error saving highscore {e}")


    def update(self):
        """Called by scoreboard's update to make sure the level increases every 5 tiles"""
        last_level = self.level
        self.level = self.score//1
        self.difficulty_level = self.level


        #If level was increased in this update call:
        if last_level-self.level!=0: 
            #reinitialize with the updated difficulty level (make game harder) 
            self.game.game_settings.initialize_dynamic_settings()

