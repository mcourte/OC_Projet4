import os
import datetime
import json


import random


from controllers import player_controller
from views import round_view
from views import tournament_view
from views import player_view


class TournamentController:

    def __init__(self):
        pass

    def start_tournament(self):
        '''Crée un tournoi : infos + liste joueurs +  date de début'''
        self.tournament_data_view = tournament_view.TournamentView().start_tournament_view()
        file_path = os.path.join("data", "tournament_data.json")
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
        self.number_of_player = tournament_view.TournamentView().number_of_player()
        if int(self.number_of_player) % 2 != 0:
            self.number_of_player = tournament_view.TournamentView().number_of_player()
        self.score_tournoi = 0
        for i in self.number_of_player:
            self.number_of_player = str(i)
        self.list_of_players = []
        number_of_player = int(self.number_of_player)
        file_path = open(os.path.join("data", "players_data.json"))
        data_players = json.load(file_path)

        self.choose_player = tournament_view.TournamentView().choose_players()
        if self.choose_player == "oui":
            index = number_of_player
            random_player = random.sample(data_players, index)
            self.list_of_players.append(random_player)

        elif self.choose_player == "non":
            list_player = []
            player_list = player_controller.PlayerController().choose_player()
            print(player_list)
            for i in range(0, (number_of_player)):
                choose_player = player_view.PlayerView().choose_player()
                choice = int(choose_player)
                choice_player = player_list.loc[choice]
                choice_player = choice_player.to_dict()
                list_player.append(choice_player)
            self.list_of_players = list_player

        else:
            self.choose_player = tournament_view.TournamentView().choose_players()
        date_of_begin = datetime.date.today()
        self.date_of_begin = date_of_begin.strftime("%d-%m-%Y")
        self.tournament_data = [{"Nombre de joueurs inscrits: ": self.number_of_player,
                                 "Liste des joueurs inscrits: ": self.list_of_players,
                                 "Date de début: ": self.date_of_begin}]
        data.extend(self.tournament_data)
        with open(file_path,  "w") as file:
            json.dump(data, file, ensure_ascii=False, indent=4)
        file_path2 = os.path.join("data", "tournament_pending.json")
        with open(file_path2,  "w") as file:
            json.dump(data, file, ensure_ascii=False, indent=4)

        return self.tournament_data, self.number_of_player

    def end_tournament(self):
        '''Permet de terminer un tournoi et de l'enregistrer dans le fichier tournament_closed'''
        file_path = os.path.join("data", "tournament_pending.json")
        with open(file_path, "r") as file:
            data = json.load(file)
        date_of_end = datetime.date.today()
        self.date_of_end = date_of_end.strftime("%d-%m-%Y")
        tournament_end = {"Date de fin: ": self.date_of_end}
        data.append(tournament_end)
        with open(file_path,  "w") as file:
            json.dump(data, file, ensure_ascii=False, indent=4)
        file_path2 = os.path.join("data", "tournament_closed.json")
        with open(file_path2,  "w") as file:
            json.dump(data, file, ensure_ascii=False, indent=4)
        new_data_pending = []
        with open(file_path,  "w") as file:
            json.dump(new_data_pending, file, ensure_ascii=False, indent=4)

    def close_tournament(self):
        '''Permet de lister les tournois terminés'''
        close = {}
        list_close = []
        file_path = os.path.join("data", "tournament_closed.json")
        with open(file_path, "r") as file:
            data = json.load(file)
        for i in range(0, len(data)):
            close.update(data[i])
            list_close.append(close)
        return list_close

    def display_tournament(self):
        ''' Permet d'afficher la liste des tournois'''
        list_tournament = []
        file_path = os.path.join("data", "tournament_data.json")
        with open(file_path, "r") as file:
            data = json.load(file)
        for data_dict in data:
            if isinstance(data_dict, dict):
                tournament_data = data_dict.get("Nom du tournoi: ")
                if tournament_data is not None:
                    list_tournament.append(tournament_data)
        return list_tournament

    def choose_tournament_detail(self):
        ''' Permet de choisir le tournoi dont on veut afficher les détails'''
        list_tournament = []
        list_tournament_name = []
        list_tournament_data = []
        file_path = os.path.join("data", "tournament_data.json")
        with open(file_path, "r") as file:
            data = json.load(file)
        for i in range(0, len(data), 3):
            one_tournament = data[i:(i+3)]
            list_tournament.append(one_tournament)
        for tournament in list_tournament:
            tournament = tournament[0]
            tournament_name = tournament.get("Nom du tournoi: ")
            if tournament_name is not None:
                list_tournament_name.append(tournament_name)
                list_tournament_data.append(tournament_name)
        for i, list_tournament_name in enumerate(list_tournament_name, start=1):
            print(f"{i}.{list_tournament_name}")
        choice = tournament_view.TournamentView().choose_tournament()
        user_choice = int(choice) - 1
        if 0 <= user_choice <= len(list_tournament_name):
            tournament_choice = list_tournament_data[user_choice]
            print(f"Vous avez choisi le tournoi : {tournament_choice}")
        else:
            print("Numéro de tournoi invalide.")
        return tournament_choice

    def choose_tournament_data(self):
        ''' Permet de choisir le tournoi dont on veut afficher les détails'''
        list_tournament = []
        list_tournament_name = []
        list_tournament_data = []
        file_path = os.path.join("data", "tournament_closed.json")
        with open(file_path, "r") as file:
            data = json.load(file)
        for i in range(0, len(data), 3):
            one_tournament = data[i:(i+3)]
            list_tournament.append(one_tournament)
        for tournament in list_tournament:
            tournament = tournament[0]
            tournament_name = tournament.get("Nom du tournoi: ")
            if tournament_name is not None:
                list_tournament_name.append(tournament_name)
                list_tournament_data.append(tournament_name)
        for i, list_tournament_name in enumerate(list_tournament_name, start=1):
            print(f"{i}.{list_tournament_name}")
        choice = tournament_view.TournamentView().choose_tournament()
        user_choice = int(choice) - 1
        if 0 <= user_choice <= len(list_tournament_name):
            tournament_choice = list_tournament_data[user_choice]
            print(f"Vous avez choisi le tournoi : {tournament_choice}")
        else:
            print("Numéro de tournoi invalide.")
        return tournament_choice

    def display_tournament_detail(self):
        '''Permet d'afficher les détails d'un tournoi'''
        list_tournament = []
        user_choice = TournamentController().choose_tournament_detail()
        file_path = os.path.join("data", "tournament_data.json")
        with open(file_path, "r") as file:
            data = json.load(file)
        for i in range(0, len(data), 3):
            one_tournament = data[i:(i+3)]
            del one_tournament[1]
            list_tournament.append(one_tournament)
        for one_tournament in list_tournament:
            for tournament_dict in one_tournament:
                choice = tournament_dict.get("Nom du tournoi: ")
                if choice == user_choice:
                    print(one_tournament)
        return one_tournament

    def display_tournament_data(self):
        '''Permet d'afficher les détails d'un tournoi'''
        user_choice = TournamentController().choose_tournament_data()
        tournament_number = user_choice[-1]
        next_tournament_number = int(tournament_number) + 1
        list_tournament = []
        file_path = os.path.join("data", "tournament_closed.json")
        with open(file_path, "r") as file:
            data = json.load(file)
        for i in range(0, len(data), 3):
            one_tournament = data[i:(i+3)]
            del one_tournament[1]
            list_tournament.append(one_tournament)
        key_to_search = "Nom du tournoi: "
        value_to_search = user_choice
        value_to_search2 = "Tournoi n°" + str(next_tournament_number)
        for index, item in enumerate(data):
            if item.get(key_to_search) == value_to_search:
                result_start = index
            if item.get(key_to_search) == value_to_search2:
                result_end = index
            else:
                result_end = -1
        tournament_data = data[result_start:result_end]
        return tournament_data

    def display_tournament_alphabetically(self):
        '''Permet de ranger la liste des joueurs du tournoi par ordre alphabétique'''
        user_choice = TournamentController().choose_tournament_detail()
        print(user_choice)
        dict_player = {}
        sorted_player = []
        file_path = os.path.join("data", "tournament_data.json")
        with open(file_path, "r") as file:
            data = json.load(file)
            key_to_search = "Nom du tournoi: "
            value_to_search = user_choice
            for index, item in enumerate(data):
                if item.get(key_to_search) == value_to_search:
                    result = index
                players_data = data[result + 1]
                list_player = players_data.get("Liste des joueurs inscrits: ")
                list_player = list_player[0]
            for player in list_player:
                dict_player.update(player)
                a = list(dict_player.items())
                sorted_player.append(a)
            for i in range(0, len(sorted_player)):
                sorted_name = sorted(sorted_player,
                                     key=lambda x: (x[0], x[1]))
                sorted_name.append(sorted_name)
            sorted_name.pop()
        return sorted_name

    def tournament_menu(self):
        '''Permet de lancer les fonctions suivant les choix de l'utilisateur'''
        while True:
            choice = tournament_view.TournamentView().display_tournament_menu()
            if choice == "1":
                TournamentController().start_tournament()
            elif choice == "2":
                round_view.RoundView().display_round_menu()
            elif choice == "3":
                TournamentController().end_tournament()
            elif choice == "4":
                break
            else:
                print("Option invalide. Veuillez choisir une option valide.")
