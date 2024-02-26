"""Define the Match."""


class Match:
    def __init__(self, player1, player2, score1=None, score2=None):
        '''Initialise une instance de match'''
        self.player1 = player1
        self.player2 = player2
        self.score1 = score1
        self.score2 = score2
