
import os
import json

import datetime

from models import round_model


class MatchController :
    def __init__(self):
        pass

    def duo_player(self):  
        file_path=os.path.join("data","tournament_data.json")
        data = json.load(file_path)
        player1 = data["Liste des joueurs inscrits: "][0]
        player2 = data["Liste des joueurs inscrits: "][1]
        self.couple_of_player = [player1,player2]
