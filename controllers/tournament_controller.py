"""Define the Tournament."""

import os
import datetime
import json


import random

from controllers import player_controller
from views import tournament_view
from views import player_view
from views import report_view

class TournamentController:

    def __init__(self):
        
        pass

    def start_tournament(self):  
        '''Crée un tournoi : infos + liste joueurs +  date de début'''
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
        '''Permet de terminer un tournoi et de l'enregistrer dans le fichier tournament_closed'''
        file_path=os.path.join("data","tournament_data.json")
        with open(file_path, "r") as file:
            data = json.load(file)
        date_of_end = datetime.date.today()
        self.date_of_end = date_of_end.strftime("%d-%m-%Y")
        tournament_end={"Date de fin: " : self.date_of_end}
        data.append(tournament_end)
        with open(file_path,  "w") as file:
            json.dump(data, file, ensure_ascii=False, indent=4)
        file_path2=os.path.join("data","tournament_closed.json")
        with open(file_path2,  "w") as file:
            json.dump(data, file, ensure_ascii=False, indent=4)


    def close_tournament(self):
        '''Permet de lister les tournois terminés'''
        close = {}
        list_close = []
        file_path = os.path.join("data","tournament_closed.json")
        with open(file_path, "r") as file:
            data = json.load(file)
        for i in range(0,len(data)):
            close.update(data[i])
            list_close.append(close)
        print(list_close)
      
    def display_tournament(self):
        ''' Permet d'afficher la liste des tournois'''
        list_tournament = []
        file_path = os.path.join("data","tournament_data.json")
        with open(file_path, "r") as file:
            data = json.load(file)
        for i in range(0,len(data),3):
            tournament = data[i]
            list_tournament.append(tournament)
        return list_tournament

    def choose_tournament_detail(self):
        '''Permet de choisir le tournoi dont on veut les détails'''
        list_tournament = []
        data_tournament = []
        tournament_data = []
        tournament_name = []
        file_path = os.path.join("data","tournament_data.json")
        with open(file_path, "r") as file:
            data = json.load(file)
        for i in range(0,len(data)):
            tournament = data[i]
            data_tournament.append(tournament)
            tournament_name = tournament.get("Nom du tournoi: ")
            if tournament_name != None : 
                list_tournament.append(tournament_name)
                tournament_data.append(tournament_name)
        for i , list_tournament in enumerate(list_tournament, start=1) : 
            print(f"{i}.{list_tournament}")
        
        choice = tournament_view.TournamentView().choose_tournament()
        user_choice=int(choice) -1
        if 1<= user_choice <= len(tournament_data):
            tournament_choice=tournament_data[user_choice]
            print(f"Vous avez choisi le tournoi : {tournament_choice}")
        else:
            print("Numéro de tournoi invalide.")
        return tournament_choice

    def display_tournament_detail(self):
        '''Permet d'afficher les détails d'un tournoi'''
        tournament_choice = TournamentController().choose_tournament_detail()
        file_path = os.path.join("data","tournament_data.json")
        with open(file_path, "r") as file:
            data = json.load(file)
        list_tournament = []
        for i in range(0,len(data),3):
                one_tournament=data[i:(i+3)]
                list_tournament.append(one_tournament)
        for i in range(0,len(list_tournament)):
            for l in list_tournament:
                a = l.get("Nom du tournoi: ")
                if tournament_choice == a :
                    display_tournament = l
                    print(display_tournament)
        #return tournament_select
        
        


    def display_tournament_alphabetically(self):
        '''Permet de ranger la liste des joueurs du tournoi par ordre alphabétique'''
        file_path = os.path.join("data","tournament_data.json")
        with open(file_path, "r") as file:
            data = json.load(file)
        data = data[1]
        list_player=data.get("Liste des joueurs inscrits: ")
        for i in range(0, len(list_player)):
            sorted_name = sorted(list_player,
                                    key=lambda x: (x[0], x[1])) 
            sorted_name.append(sorted_name)
        return sorted_name

    def tournament_menu(self):
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
    
    def tournament_report_menu(self):
        '''Permet de choisir les rapports suivant les choix de l'utilisateur'''
        while True:
            choice = report_view.ReportView().display_report_menu()
            if choice == "2":
                TournamentController().display_tournament()
            elif choice == "3":
                TournamentController().display_tournament_detail()
            elif choice == "4":
                TournamentController().display_tournament_alphabetically()
            elif choice == "5":
                pass
            elif choice == "6":
                break
            else:
                print("Option invalide. Veuillez choisir une option valide.") 


test = TournamentController()
test.display_tournament_detail()