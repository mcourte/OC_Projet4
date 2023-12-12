"""Define the Match."""


class Match:
    def __init__(self, couple_of_player={}, winner=bool, looser=bool, draw=bool):
        self.couple_of_player = couple_of_player
        self.winner = winner
        self.looser = looser
        self.draw = draw
