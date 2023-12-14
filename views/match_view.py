"""Define the Match."""


class MatchView:

    def __init__(self):
        pass

    def choose_match(self):
        '''Permet de choisir le match dont on veut indiquer le score'''
        match_choice = input("Voulez-vous rentrer le score du match suivant? Oui/Non :").lower()
        self.match_choice = match_choice
        return self.match_choice

    def match_view(self):
        '''Permet d'indiquer l'ID du gagnant'''
        winner_ID = input("Indiquez l'ID du joueur gagnant ou <nul> en cas d'égalité :")
        self.winner_ID = winner_ID
        return self.winner_ID
