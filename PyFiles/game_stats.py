from flyfighter_game import Game

class GameStats:
    def __init__(self,game:Game) -> None:
        self.game = game
        self.player = game.player

        self.difficulty_level = 1

        self.current_score = 0
        self.high_score = self.load_highscore()

    
    def load_highscore(self):
        pass
        #TODO implement
    
    def save_highscore(self):
        pass

