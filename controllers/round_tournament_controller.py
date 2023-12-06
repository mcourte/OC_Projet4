"""Define the Round."""
import os
import json

import datetime
import random

from views import round_view


class RoundTournamentController:
    def __init__(self):
        pass

    def paires_of_player(self):
        dict_player = {}
        b = []
        file_path = os.path.join("data", "tournament_data.json")
        with open(file_path, "r") as file:
            data = json.load(file)
        players = data[1]
        list_player = players.get("Liste des joueurs inscrits: ")
        list_player = list_player[0]
        for i in range(0, len(data)):
            for i in list_player:
                dict_player.update(i)
                a = list(dict_player.items())
                b.append(a)
        data_round = data[-1]
        data_round = data_round[0]
        tournament_round = data_round.get("Numéro de round: ")
        if tournament_round == 1:
            random.shuffle(list_player)
            pairings = [(list_player[i], list_player[i + 1]) for i in range(0, len(list_player), 2)]
            pairings_round = {"Liste des paires: ": pairings}
            data_round.update(pairings_round)
            data.append(data_round)
            with open(file_path, "w") as file:
                json.dump(data, file, ensure_ascii=False, indent=4)
        else:
            with open(file_path, "r") as file:
                data_round = json.load(file)
            pairing_data = data_round.get("Liste des paires: ")
            pairings = []
            sorted_b = sorted(b,
                              key=lambda x: (x[-1]), reverse=True)
            sorted_b.append(sorted_b)
            sorted_b.pop()
            for i in range(0, len(sorted_b), 2):
                player1 = sorted_b[i]
                player2 = sorted_b[i + 1] if i + 1 < len(sorted_b) else None
                if (player1, player2) not in pairing_data and (player2, player1) not in pairing_data:
                    pairings.append((player1, player2))
            data_round.update(pairings)
            data.append(data_round)
            with open(file_path, "w") as file:
                json.dump(data, file, ensure_ascii=False, indent=4)
        return pairings

    def start_round(self):
        start_date = datetime.datetime.today()
        start_date = start_date.strftime("%d-%m-%Y")
        round_number = 1
        file_path = os.path.join("data", "tournament_data.json")
        with open(file_path, "r") as file:
            data = json.load(file)
        data_round = [{"Date de début: ": start_date,
                       "Numéro de round: ": round_number}]
        data.append(data_round)
        with open(file_path, "w") as file:
            json.dump(data, file, ensure_ascii=False, indent=4)
        data_players = RoundTournamentController().paires_of_player()
        data.extend(data_players)
        with open(file_path,  "w") as file:
            json.dump(data, file, ensure_ascii=False, indent=4)

    def new_round(self):
        file_path = os.path.join("data", "tournament_data.json")
        with open(file_path, "r") as file:
            data = json.load(file)
        data_round = data[-3]
        data_round = data_round[0]
        round_number = data_round.get("Numéro de round: ")
        start_date = datetime.datetime.today()
        start_date = start_date.strftime("%d-%m-%Y")
        new_round_number = round_number + 1
        data_round = [{"Date de début: ": start_date,
                       "Numéro de round: ": new_round_number}]
        data.append(data_round)
        with open(file_path,  "w") as file:
            json.dump(data, file, ensure_ascii=False, indent=4)
        data_players = RoundTournamentController().paires_of_player()
        data.append(data_players)
        with open(file_path,  "w") as file:
            json.dump(data, file, ensure_ascii=False, indent=4)
        return new_round_number

    def end_round(self):
        file_path = os.path.join("data", "tournament_data.json")
        with open(file_path, "r") as file:
            data = json.load(file)
        end_date = datetime.datetime.today()
        self.end_date = end_date.strftime("%d-%m-%Y")
        end = [{"Date de fin du round : ": self.end_date}]
        data.append(end)
        with open(file_path,  "w") as file:
            json.dump(data, file, ensure_ascii=False, indent=4)

    def round_menu(self):
        '''Permet de lancer les fonctions suivant les choix de l'utilisateur'''
        while True:
            choice = round_view.RoundView().display_round_menu()

            if choice == "1":
                RoundTournamentController().start_round()
            elif choice == "3":
                RoundTournamentController().end_round()
            elif choice == "4":
                break
            else:
                print("Option invalide. Veuillez choisir une option valide.")


test = RoundTournamentController()
test.start_round()
