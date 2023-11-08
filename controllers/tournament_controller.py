"""Define the Tournament."""

import os
import datetime
import json

import random

from models import tournament_model
from views import tournament_view

class TournamentController:

    def __init__(self):
        pass

    def start_tournament(self):  
        self.number_of_player=tournament_view.TournamentView().start_tournament_view()
        for i in self.number_of_player:
            self.number_of_player=str(i)
        self.list_of_players = []
        number_of_player=int(self.number_of_player)
        file_path = open(os.path.join("data","players_data.json"))
        data_players = json.load(file_path)
        for i in range(0, number_of_player):
            random_players = random.sample(data_players, k=1)
            self.list_of_players.append(random_players)
        date_of_begin = datetime.date.today()
        self.date_of_begin = date_of_begin.strftime("%d-%m-%Y")
        self.tournament_data=[{
                        "Liste des joueurs inscrits: " : self.list_of_players,
                        "Date de début: " : self.date_of_begin,
                        }
                        ]
        file_path=os.path.join("data","tournament_data.json")
        try:
            with open(file_path, "r") as file:
                data = json.load(file)
        except FileNotFoundError:
            data = []
        except json.JSONDecodeError:
            data = []
        data.extend(self.tournament_data)
        with open(file_path,  "w") as file:
            json.dump(data, file, ensure_ascii=False, indent=4)

        return self.tournament_data
    
    def end_tournament(self):
        file_path=os.path.join("data","tournament_data.json")
        with open(file_path, "r") as file:
            data = json.load(file)
        date_of_end = datetime.date.today()
        self.date_of_end = date_of_end.strftime("%d-%m-%Y")
        tournament_end=[{"Date de fin: " : self.date_of_end}]
        data.extend(tournament_end)
        with open(file_path,  "w") as file:
            json.dump(data, file, ensure_ascii=False, indent=4)

tournament1=tournament_model.Tournament()
tournament1=TournamentController()
tournament1.start_tournament()
tournament1.end_tournament()