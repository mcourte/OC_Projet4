"""Define the Tournament."""

import datetime
import json

from models import player_model


class TournamentView:

    def __init__(self):
        pass

    def start_tournament_view(self):  
        self.name = input("Quel est le nom du tournoi?")
        self.location = input("Quelle est la location du tournoi?")
        
        nb_round = input("Combien il y aura-t-il de round?(par défaut :4)")
        if nb_round == "" or "4":
           self.number_of_round = 4
        else :
            self.number_of_round = nb_round



        self.description = input("Entrez les remarques générales du tournoi : ")
        self.tournament_data_view={
                        "Nom du tournoi: " : self.name,
                        "Lieu: ": self.location,
                        "Nombre de round: " : self.number_of_round,
                        "Description: " : self.description
                        }
        
        data=json.dumps(self.tournament_data_view, indent=2)
        with open("tournament_data_data.json", "w") as f:
            f.write(data)
        return self.tournament_data_view
    
    def end_tournament_view(self):
        self.date_of_end = datetime.date.today()
        
        #self.tournament_data.update("Date de fin: " : self.date_of_end)
        data=json.dumps(self.tournament_data_view, indent=2)
        with open("tournament_data_data.json", "w") as f:
            f.write(data)


