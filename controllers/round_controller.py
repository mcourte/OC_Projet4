"""Define the Round."""
import os
import json

import datetime
from views import tournament_view
from views import report_view
from controllers import match_controller
from controllers import tournament_controller

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

    def start_round(self):
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
        

        
        
    #def new_round(self):
    #    file_path = os.path.join("data","round_data.json")
    #    with open(file_path, "r") as file:
    #        data = json.load(file)
    #    data = data[0]
    #    round_number = data.get("Numéro de round: ")
    #    start_date = datetime.datetime.today()
    #    start_date= start_date.strftime("%d-%m-%Y")
    #    self.new_round_number = round_number +1
    #    data_round = [{"Date de début: " : start_date,
    #                 "Numéro de round: " : self.new_round_number}]
    #    data.update(data_round)
    #    with open(file_path,  "a") as file:
    #        json.dump(data, file, ensure_ascii=False, indent=4)
    #    return self.new_round_number
        

    def end_round(self):
        file_path = os.path.join("data","round_data.json")
        with open(file_path, "r") as file:
            data = json.load(file)
        end_date = datetime.datetime.today()
        self.end_date= end_date.strftime("%d-%m-%Y")
        end = [{"Date de fin du round : " : self.end_date}]
        data.append(end)
        with open(file_path,  "w") as file:
            json.dump(data, file, ensure_ascii=False, indent=4)
        
    def add_round_to_tournament(self):
        file_path = os.path.join("data","round_data.json")
        with open(file_path, "r") as file:
            data = json.load(file)

        file_path2 = os.path.join("data","tournament_data.json")
        with open(file_path2, "r") as file:
            data_tournament = json.load(file)
        
        data_tournament.append(data)

        with open(file_path, "w") as file:
            json.dump(data_tournament, file, ensure_ascii=False, indent=4)




        #file_path2 = os.path.join("data","players_data.json")
        #with open(file_path2, "r") as file:
        #    player_data = json.load(file)
        #for player_dict in player_data :
        #    data_player = data[1]
        #    player_information = data_player[-2]
        #    ID_player = player_information.get("Identifiant National d'Echecs: ")

        #    for i in range(0,len(data_player)):
        #        data_player = data_player[i]
        #        print(data_player)
        #        score = data_player[-1]
        #        score = score["Score global du tournoi: "]
        #        player_dict["Score global du joueur: "] = score
        #        print(player_dict)

    def round_menu(self):
        '''Permet de lancer les fonctions suivant les choix de l'utilisateur'''
        while True:
            choice = tournament_view.TournamentView().display_tournament_menu()
            if choice == "1":
                TournamentController().start_tournament()
            elif choice == "3":
                TournamentController().close_tournament()
            elif choice == "4":
                TournamentController().display_tournament()
            elif choice == "5":
                break
            else:
               print("Option invalide. Veuillez choisir une option valide.")