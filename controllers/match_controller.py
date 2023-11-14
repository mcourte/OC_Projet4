
import os
import json

import datetime
import random

from views import match_view

class MatchController :
    def __init__(self):
        pass

    def duo_player(self):  
        file_path=os.path.join("data","tournament_data.json")
        with open(file_path, "r") as file:
            data = json.load(file)
        dict_of_player = data[5]
        list_of_player=list(dict_of_player.values())
        random_player=random.sample(list_of_player,1)
        print(random_player)

    def winner(self):
        winner_ID=match_view.MatchView().match_view()
        




match=MatchController()
match.duo_player()