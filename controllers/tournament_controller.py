import os
import datetime
import random
import json


from views.tournament_view import TournamentView
from views.player_view import PlayerView
from controllers.round_controller import RoundController


class TournamentController:

    def __init__(self):
        self.tournament_data_view = None
        self.number_of_player = None
        self.score_tournoi = 0
        self.list_of_players = []

    def start_tournament(self):
        '''Crée un tournoi'''
        self.tournament_data_view = TournamentView().start_tournament_view()
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
        self.number_of_player = TournamentView().number_of_player()
        if int(self.number_of_player) % 2 != 0:
            self.number_of_player = TournamentView().number_of_player()
        self.score_tournoi = 0
        for i in self.number_of_player:
            self.number_of_player = str(i)
        self.list_of_players = []
        number_of_player = int(self.number_of_player)
        file_path = open(os.path.join("data", "players_data.json"))
        data_players = json.load(file_path)

        self.choose_player = TournamentView().choose_players()
        if self.choose_player == "oui":
            index = number_of_player
            random_player = random.sample(data_players, index)
            self.list_of_players.append(random_player)

        elif self.choose_player == "non":
            list_player = []
            for i in index:
                player_list = TournamentView().choose_players_ID()
                print(player_list)
                for i in range(0, (number_of_player)):
                    choose_player = PlayerView().choose_player()
                    choice = int(choose_player)
                    choice_player = player_list.loc[choice]
                    choice_player = choice_player.to_dict()
                    list_player.append(choice_player)
                self.list_of_players = list_player

        else:
            self.choose_player = TournamentView().choose_players()
        self.tournament_data = [{"Nombre_joueurs_inscrits": self.number_of_player,
                                 "Liste_joueurs_inscrits": self.list_of_players,
                                 }]
        data.extend(self.tournament_data)
        file_path = os.path.join("data", "tournament_data.json")
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

        tournament_end = {"Date_de_fin": self.date_of_end}
        data.append(tournament_end)
        print(data)

        with open(file_path, "w") as file:
            json.dump([], file, ensure_ascii=False, indent=4)

        file_path2 = os.path.join("data", "tournament_closed.json")
        with open(file_path2, "w") as file:
            json.dump(data, file, ensure_ascii=False, indent=4)

    def close_tournament(self):
        '''Permet de lister les tournois terminés'''
        file_path = os.path.join("data", "tournament_closed.json")
        with open(file_path, "r") as file:
            data = json.load(file)

        close = {}
        list_close = []

        for i in range(len(data)):
            close.update(data[i])
            list_close.append(close)

        return list_close

    def select_players(self):
        number_of_player = int(self.number_of_player)
        file_path = os.path.join("data", "players_data.json")
        with open(file_path, "r") as file:
            data_players = json.load(file)

        self.choose_player = TournamentView().choose_players()

        if self.choose_player == "oui":
            index = number_of_player
            return random.sample(data_players, index)
        elif self.choose_player == "non":
            list_player = []
            player_list = PlayerView().choose_player_ID()

            for _ in range(number_of_player):
                choose_player = PlayerView().choose_player()
                choice = int(choose_player)
                choice_player = player_list.loc[choice].to_dict()
                list_player.append(choice_player)

            return list_player
        else:
            return TournamentView().choose_players()

    def load_tournament_data(self, file_path):
        with open(file_path, "r") as file:
            return json.load(file)

    def choose_tournament(self, file_path):
        with open(file_path, "r") as file:
            data = json.load(file)
        list_tournament = []
        for i in range(0, len(data), 3):
            one_tournament = data[i:(i + 3)]
            if one_tournament[0].get("Nom_du_tournoi") is not None:
                list_tournament.append(one_tournament[0].get("Nom_du_tournoi"))

        for i, tournament_name in enumerate(list_tournament, start=1):
            print(f"{i}.{tournament_name}")

        choice = int(input("Choisissez le numéro du tournoi : ")) - 1

        if 0 <= choice < len(list_tournament):
            tournament_choice = list_tournament[choice]
            print(f"Vous avez choisi le tournoi : {tournament_choice}")

        else:
            print("Numéro de tournoi invalide.")

        return tournament_choice

    def display_tournament_details(self):
        '''Permet d'afficher les détails d'un tournoi'''
        file_path = os.path.join("data", "tournament_data.json")
        user_choice = TournamentController().choose_tournament(file_path)
        print(user_choice)
        list_tournament = []
        with open(file_path, "r") as file:
            data = json.load(file)
        for i in range(0, len(data), 3):
            one_tournament = data[i:(i + 3)]
            del one_tournament[1]
            list_tournament.append(one_tournament)
        for one_tournament in list_tournament:
            for tournament_dict in one_tournament:
                choice = tournament_dict.get("Nom_du_tournoi")
                if choice == user_choice:
                    print(one_tournament)
        return one_tournament

    def display_tournament_alphabetically(self):
        '''Permet de ranger la liste des joueurs du tournoi par ordre alphabétique'''
        file_path = os.path.join("data", "tournament_data.json")
        user_choice = TournamentController().choose_tournament(file_path)
        print(user_choice)
        dict_player = {}
        sorted_player = []
        with open(file_path, "r") as file:
            data = json.load(file)
        for index, item in enumerate(data):
            if item.get("Nom_du_tournoi") == user_choice:
                players_data = data[index + 1]
                list_player = players_data.get("Liste_joueurs_inscrits")[0]
                for player in list_player:
                    dict_player.update(player)
                    a = list(dict_player.items())
                    sorted_player.append(a)
                sorted_name = sorted(sorted_player, key=lambda x: (x[0], x[1]))
                sorted_name.append(sorted_name)
                sorted_name.pop()
        return sorted_name

    def display_tournament_data(self):
        '''Permet d'afficher les détails d'un tournoi'''
        file_path = os.path.join("data", "tournament_closed.json")
        user_choice = TournamentController().choose_tournament(file_path)
        tournament_number = user_choice[-1]
        next_tournament_number = int(tournament_number) + 1
        list_tournament = []
        with open(file_path, "r") as file:
            data = json.load(file)
        for i in range(0, len(data), 3):
            one_tournament = data[i:(i+3)]
            del one_tournament[1]
            list_tournament.append(one_tournament)
        key_to_search = "Nom_du_tournoi"
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

    def display_tournament(self):
        ''' Permet d'afficher la liste des tournois'''
        list_tournament = []
        file_path = os.path.join("data", "tournament_data.json")
        with open(file_path, "r") as file:
            data = json.load(file)
        for data_dict in data:
            if isinstance(data_dict, dict):
                tournament_data = data_dict.get("Nom_du_tournoi")
                if tournament_data is not None:
                    list_tournament.append(tournament_data)
        return list_tournament

    def tournament_menu(self):
        '''Permet de lancer les fonctions suivant les choix de l'utilisateur'''
        while True:
            choice = TournamentView().display_tournament_menu()
            if choice == "1":
                TournamentController().start_tournament()
            elif choice == "2":
                RoundController().round_menu()
            elif choice == "3":
                TournamentController().end_tournament()
            elif choice == "4":
                break
            else:
                print("Option invalide. Veuillez choisir une option valide.")
