"""Define the Tournament."""

import datetime
import json
import os



class TournamentView:

    def __init__(self):
        pass


    def start_tournament_view(self):  
        self.name = input("Quel est le nom du tournoi?")
        self.location = input("Quelle est la localisation du tournoi?")
        
        nb_round = input("Combien il y aura-t-il de round?(par défaut :4)")
        if nb_round == "" or "4":
           self.number_of_round = 4
        else :
            self.number_of_round = nb_round

        self.description = input("Entrez les remarques générales du tournoi : ")
                
        self.tournament_data_view=[
            {
                        "Nom du tournoi: " : self.name,
                        "Lieu: ": self.location,
                        "Nombre de round: " : self.number_of_round,
                        "Description: " : self.description
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
        data.extend(self.tournament_data_view)
        with open(file_path,  "w") as file:
            json.dump(data, file, ensure_ascii=False, indent=4)
        return self.tournament_data_view
    
    def number_of_player(self):  
        self.number_of_players = input("Combien y aura-t-il de joueurs dans le tournoi ? (au moins 1 joueur de plus que le nombre de round): ")
        return  self.number_of_players

    def choose_players(self):  
        self.choose_player = input("Voulez-vous créer une liste aléatoire de joueurs ? Oui/Non ").lower()
        return self.choose_player
    
    def choose_players_ID(self):  
        self.choose_ID = input("Veuillez rentrer l'ID du joueur que vous souhaitez rajouter : ").upper()
        return self.choose_ID

    def end_tournament_view(self):
        self.date_of_end = datetime.date.today()
        date_of_end={"Date de fin: ", self.date_of_end}
        self.tournament_data_view.extend(date_of_end)
        file_path=os.path.join("data","tournament_data.json")
        try:
            with open(file_path, "r") as file:
                data = json.load(file)
        except FileNotFoundError:
            data = []
        except json.JSONDecodeError:
            data = []
        data.extend(self.tournament_data_view)
        with open(file_path,  "w") as file:
            json.dump(data, file, ensure_ascii=False, indent=4)
        return self.tournament_data_view

    def choose_tournament_print(self):
        self.choose_tournament=input("Création rapport : choisir le tournoi: ")
        return self.choose_tournament
