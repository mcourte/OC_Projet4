"""Define the Tournament."""

import os
import datetime
import json


import random

from controllers import player_controller
from views import tournament_view
from views import main_view
from views import player_view

class TournamentController:

    def __init__(self):
        
        pass

    def start_tournament(self):  
        self.tournament_data_view=tournament_view.TournamentView().start_tournament_view()
        self.number_of_player=tournament_view.TournamentView().number_of_player()
        self.score_tournoi = 0
        for i in self.number_of_player:
            self.number_of_player=str(i)
        self.list_of_players = []
        number_of_player=int(self.number_of_player)
        file_path = open(os.path.join("data","players_data.json"))
        data_players = json.load(file_path)

        self.choose_player=tournament_view.TournamentView().choose_players()      
        if self.choose_player == "oui":
                index=number_of_player+1
                random_player=random.sample(data_players,index)
                self.list_of_players.append(random_player)

        elif self.choose_player == "non":
            list_player=[]
            player_list=player_controller.PlayerController().choose_player()
            print(player_list)
            for i in range(0, (number_of_player)):
                choose_player=player_view.PlayerView().choose_player()
                choice=int(choose_player)
                choice_player=player_list.loc[choice]
                choice_player=choice_player.to_dict()
                list_player.append(choice_player) 
            self.list_of_players=list_player
                
        else :
                self.choose_player=tournament_view.TournamentView().choose_players()         
        date_of_begin = datetime.date.today()
        self.date_of_begin= date_of_begin.strftime("%d-%m-%Y")
        self.tournament_data=[{"Nombre de joueurs inscrits: " : self.number_of_player,
                        "Liste des joueurs inscrits: " : self.list_of_players,
                        "Date de début: " : self.date_of_begin,
                        }]
                        
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

        return self.tournament_data, self.number_of_player
    
    def end_tournament(self):
        file_path=os.path.join("data","tournament_data.json")
        with open(file_path, "r") as file:
            data = json.load(file)
        date_of_end = datetime.date.today()
        self.date_of_end = date_of_end.strftime("%d-%m-%Y")
        tournament_end={"Date de fin: " : self.date_of_end}
        data.append(tournament_end)
        with open(file_path,  "w") as file:
            json.dump(data, file, ensure_ascii=False, indent=4)

    def display_tournament(self):
        dict_tournament = {}
        one_tournament = {}
        sorted_tournament = []
        list_dict_tournament = []
        file_path = os.path.join("data","tournament_data.json")
        with open(file_path, "r") as file:
            data = json.load(file)
        for i in range(0, len(data)):
            dict_tournament= data[i]
            list_dict_tournament.append(dict_tournament)          
        for i in range(0, len(list_dict_tournament)):
            for dict in list_dict_tournament :
                sorted_tournament = sorted(dict.items(),
                                        key=lambda x: (x[0])) 
                sorted_tournament.append(sorted_tournament)
            print(sorted_tournament) 

    def close_tournament(self):
        close = {}
        list_close = []
        file_path = os.path.join("data","tournament_data.json")
        with open(file_path, "r") as file:
            data = json.load(file)
        for i in range(0,len(data)):
            close.update(data[i])
            list_close.append(close)
        print(list_close)

      


    def tournament_menu(self):
        while True:
            choice = player_view.PlayerView().display_player_menu()
            if choice == "1":
                self.start_tournament()
            elif choice == "2":
                self.display_tournament()
            elif choice == "3":
                break
            else:
                error = main_view.MainView().display_invalid_option_message()
        


tournament1=TournamentController()
#ournament1.start_tournament()
#tournament1.end_tournament()
tournament1.display_tournament()
#tournament1.close_tournament()
