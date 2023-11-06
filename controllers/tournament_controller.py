"""Define the Tournament."""

import datetime
import json

from models import player_model
from models import tournament_model

class TournamentController:

    def __init__(self):
        pass

    def start_tournament(self):  

        player1 = player_model.Player().CreatePlayer()
        player2 = player_model.Player().CreatePlayer()
        self.list_of_players = [player1,player2]
        self.date_of_begin = datetime.date.today()
        self.tournament_data={
                        "Liste des joueurs inscrits: " : self.list_of_players,
                        "Date de début: " : self.date_of_begin,

                        }
        
        data=json.dumps(self.tournament_data, indent=2)
        with open("tournament_data_data.json", "w") as f:
            f.write(data)
        return self.tournament_data
    
    def end_tournament(self):
        self.date_of_end = datetime.date.today()
        
        #self.tournament_data.update("Date de fin: " : self.date_of_end)
        data=json.dumps(self.tournament_data, indent=2)
        with open("tournament_data_data.json", "w") as f:
            f.write(data)


tournament1=tournament_model.Tournament()
tournament1=TournamentController
tournament1.start_tournament()