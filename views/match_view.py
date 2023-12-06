"""Define the Match."""


class MatchView:

    def __init__(self):
        pass

    def choose_match(self):
        match_choice = input("Choississez le match dont vous souhaitez indiquer le score :")
        self.match_choice = match_choice
        return self.match_choice

    def match_view(self):
        winner_ID = input("Indiquez l'ID du joueur gagnant ou <nul> en cas d'égalité :")
        self.winner_ID = winner_ID
        return self.winner_ID
