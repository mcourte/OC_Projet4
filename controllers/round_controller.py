"""Define the Round."""

import os
import json

import datetime

from models import round_model

class RoundController :
    def __init__(self):
        pass

    def duo_player(self):  
        f = open(os.path.join("data","tournament_data.json"))
        data = json.load(f)
        player1 = data["Liste des joueurs inscrits: "][0]
        player2 = data["Liste des joueurs inscrits: "][1]
        self.couple_of_player = [player1,player2]

    def start_round(self):
        self.star_date = datetime.datetime.today()
        self.round_number +=1

    def end_round(self):
        self.star_date = datetime.datetime()

round=round_model.Round()
round=RoundController()
round.duo_player()
round.start_round()
round.end_round()