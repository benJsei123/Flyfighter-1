class GameStats:
    def __init__(self,game) -> None:
        self.game = game

        #CAUTION DONT ADD PLAYER 

        self.difficulty_level = 1

        self.score = 0
        self.level = 1
        self.high_score = self.load_highscore()

    
    def load_highscore(self):
        return 143543500
        #TODO implement
    
    def save_highscore(self):
        pass

