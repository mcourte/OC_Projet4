"""Define the Tournament."""

import datetime
import json
import os



class MatchView:

    def __init__(self):
        pass

    def match_view(self):  
        winner_ID=input("Indiquez l'ID du joueur gagnant ou <nul> en cas d'égalité :")
        self.winner_ID=winner_ID

        return self.winner_ID