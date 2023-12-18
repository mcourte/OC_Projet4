"""Define the Round."""
import os
import json

import datetime
import random

from views import round_view
from controllers import match_controller


class RoundController:
    def __init__(self):
        pass

    def paires_of_player_round_one(self):
        ''' Permet de créer les paires de joueurs lors du premier round d'un tournoi'''
        file_path = os.path.join("data", "tournament_data.json")
        with open(file_path, "r") as file:
            data = json.load(file)
        players = data[-1]
        list_player = players.get("Liste des joueurs inscrits: ")
        list_player = list_player[0]
        random.shuffle(list_player)
        pairings = [(list_player[i], list_player[i + 1]) for i in range(0, len(list_player), 2)]
        pairings_round = {"Liste des paires: ": pairings}
        return pairings_round

    def paires_of_player_new_round(self):
        ''' Permet de créer des paires de joueurs à partir du Round 2'''
        dict_player = {}
        b = []
        list_paires = []
        list_round_number = []
        pairing_data = []
        file_path = os.path.join("data", "tournament_pending.json")
        with open(file_path, "r") as file:
            data = json.load(file)
            for data_dict in data:
                if isinstance(data_dict, dict):
                    round_number = data_dict.get("Numéro de round: ")
                    if round_number is not None:
                        list_round_number.append(round_number)
            last_round_number = max(list_round_number)
            key_to_search = "Numéro de round: "
            value_to_search = last_round_number
            for index, item in enumerate(data):
                if item.get(key_to_search) == value_to_search:
                    result = index
            players_data = data[result + 1]
            pairing_data = players_data.get("Liste des paires: ")
            for match in pairing_data:
                for player in match:
                    dict_player.update(player)
                    a = list(dict_player.items())
                    b.append(a)
        sorted_b = sorted(b,
                          key=lambda x: (x[-1]), reverse=True)
        sorted_b.append(sorted_b)
        sorted_b.pop()
        for i in range(0, len(sorted_b), 2):
            player1 = sorted_b[i]
            player2 = sorted_b[i + 1] if i + 1 < len(sorted_b) else None
            if (player1, player2) not in pairing_data and (player2, player1) not in pairing_data:
                dict_player1 = {}
                dict_player2 = {}
                for key, value in player1:
                    dict_player1.setdefault(key, value)
                for key, value in player2:
                    dict_player2.setdefault(key, value)
                pairings_player = [dict_player1, dict_player2]
                list_paires.append(pairings_player)
        pairings_round = {"Liste des paires: ": list_paires}
        return pairings_round

    def start_round(self):
        ''' Permet de créer un premier round d'un tournoi'''
        start_date = datetime.datetime.today()
        start_date = start_date.strftime("%d-%m-%Y")
        round_number = 1
        file_path = os.path.join("data", "tournament_data.json")
        with open(file_path, "r") as file:
            data = json.load(file)
        data_round = {"Nom du Round: ": "Round "+str(round_number),
                                        "Date de début: ": start_date,
                                        "Numéro de round: ": round_number}
        data_players = RoundController().paires_of_player_round_one()
        data.append(data_round)
        data.append(data_players)
        file_path = os.path.join("data", "tournament_pending.json")
        with open(file_path,  "w") as file:
            json.dump(data, file, ensure_ascii=False, indent=4)

    def new_round(self):
        '''Permet de lancer un deuxième round & les suivants'''
        list_round_number = []
        file_path = os.path.join("data", "tournament_pending.json")
        with open(file_path, "r") as file:
            data = json.load(file)
        for round in data:
            if isinstance(round, dict):
                number_of_round = round.get("Nombre de round: ")
                round_number = round.get("Numéro de round: ")
                if round_number is not None:
                    list_round_number.append(round_number)
        last_round_number = max(list_round_number)
        start_date = datetime.datetime.today()
        start_date = start_date.strftime("%d-%m-%Y")
        new_round_number = last_round_number + 1
        if new_round_number <= number_of_round:
            data_new_round = {"Nom du Round: ": "Round "+str(new_round_number),
                              "Date de début: ": start_date,
                              "Numéro de round: ": new_round_number}
            data.append(data_new_round)
            data_players = RoundController().paires_of_player_new_round()
            data.append(data_players)
            with open(file_path,  "w") as file:
                json.dump(data, file, ensure_ascii=False, indent=4)
        else:
            print("Tous les rounds du tournoi ont été joués")
        return new_round_number

    def end_round(self):
        '''Permet de terminer un round'''
        file_path = os.path.join("data", "tournament_pending.json")
        with open(file_path, "r") as file:
            data = json.load(file)
        end_date = datetime.datetime.today()
        self.end_date = end_date.strftime("%d-%m-%Y")
        end = {"Date de fin du round : ": self.end_date}
        data.append(end)
        file_path2 = os.path.join("data", "tournament_pending.json")
        with open(file_path2,  "w") as file:
            json.dump(data, file, ensure_ascii=False, indent=4)

    def round_menu(self):
        '''Permet de lancer les fonctions suivant les choix de l'utilisateur'''
        while True:
            choice = round_view.RoundView().display_round_menu()

            if choice == "1":
                RoundController().start_round()
            elif choice == "2":
                match_controller.MatchController().winner()
            elif choice == "3":
                RoundController().new_round()
            elif choice == "4":
                RoundController().end_round()
            elif choice == "5":
                break
            else:
                print("Option invalide. Veuillez choisir une option valide.")
