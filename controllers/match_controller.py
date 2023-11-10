
import os
import json

import datetime
import random

from controllers import tournament_controller

class MatchController :
    def __init__(self):
        pass

    def duo_player(self):  
        file_path=os.path.join("data","tournament_data.json")
        with open(file_path, "r") as file:
            data = json.load(file)
        dict_of_player = data[1]
        list_of_player=list(dict_of_player.values())
        random_player=random.sample(data,2)




match=MatchController()
match.duo_player()