"""Define the Round."""
import os
import json

import datetime
import random
import pandas as pd 

from views import match_view
from controllers import player_controller
from models import round_model

class RoundController :
    def __init__(self):
        pass
    
    def list_of_paires(self):
        list_of_pair=[]
        file_path=os.path.join("data","tournament_data.json")
        with open(file_path, "r") as file:
            data = json.load(file)
        players=data[1]
        list_player = players.get("Liste des joueurs inscrits: ")
        list_player = list_player[0]
        number_player=players.get("Nombre de joueurs inscrits: ")
        for i in range(0, int(number_player), 2):
            pairing = [list_player[i], list_player[i+1]]
            list_of_pair.append(pairing)
        dict_player = {" Liste des matchs: " : list_of_pair}
        self.dict_player = dict_player

        return self.dict_player

    def first_round(self):
        start_date = datetime.datetime.today()
        self.start_date= start_date.strftime("%d-%m-%Y")
        self.round_number = 1
        file_path2 = os.path.join("data","round_data.json")
        try:
            with open(file_path2, "r") as file:
                data = json.load(file)
        except FileNotFoundError:
            data = []
        except json.JSONDecodeError:
            data = []
        data = [{"Date de début: " : self.start_date,
                "Numéro de round: " : self.round_number
                }]

        with open(file_path2, "w") as file:
            json.dump(data, file, ensure_ascii=False, indent=4)
        

        
        
    def start_round(self):
        file_path = os.path.join("data","round_data.json")
        with open(file_path, "r") as file:
            data = json.load(file)
        start_date = datetime.datetime.today()
        self.start_date= start_date.strftime("%d-%m-%Y")
        self.round_number =self.round_number +1
        self.start = [{"Date de début du round : " : self.start_date,
                "Numéro de round: " : self.round_number}]
        data.extend(self.start)
        with open(file_path,  "w") as file:
            json.dump(data, file, ensure_ascii=False, indent=4)
        return self.round_number
        

    def end_round(self):
        file_path = os.path.join("data","round_data.json")
        with open(file_path, "r") as file:
            data = json.load(file)
        end_date = datetime.datetime.today()
        self.end_date= end_date.strftime("%d-%m-%Y")
        self.end = [{"Date de fin du round : " : self.end_date}]
        data.extend(self.end)
        file_path=os.path.join("data","round_data.json")
        with open(file_path,  "w") as file:
            json.dump(data, file, ensure_ascii=False, indent=4)



test=RoundController()
test.first_round()
