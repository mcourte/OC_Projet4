"""Define the Round."""
import json
import random
import os
import datetime


class RoundModel:
    def __init__(self, name_of_tournoi, start_date, end_date,
                 round_number):

        self.name_of_tournoi = name_of_tournoi
        self.start_date = start_date
        self.end_date = end_date
        self.round_number = round_number
        self.matches = []

    def start_round_model(self):

        start_date = datetime.datetime.today().strftime("%d-%m-%Y")
        round_number = 1
        file_path = os.path.join("data", "tournament_data.json")
        with open(file_path, "r") as file:
            data = json.load(file)
        data_round = {
            "Nom du Round: ": f"Round {round_number}",
            "Date de début: ": start_date,
        }
        data_players = RoundModel.create_pairs_round_one(self)
        data.extend([data_round, data_players])

        file_path2 = os.path.join("data", "tournament_pending.json")
        with open(file_path2, "w") as file:
            json.dump(data, file, ensure_ascii=False, indent=4)

        print(data_round)
        print(data_players)
        return data_round, data_players

    def new_round(self):
        data = RoundModel.load_data("data", "tournament_pending.json")
        list_round_numbers = [round["Numéro de round: "] for round in data if isinstance(round, dict)]
        last_round_number = max(list_round_numbers)
        start_date = datetime.datetime.today().strftime("%d-%m-%Y")
        new_round_number = last_round_number + 1

        if new_round_number <= data[0]["Nombre de round: "]:
            data_new_round = {
                "Nom du Round: ": f"Round {new_round_number}",
                "Date de début: ": start_date,
            }
            file_path2 = os.path.join("data", "tournament_data.json")
            RoundModel.save_data(file_path2, data_new_round)

            data_players = RoundModel.create_pairs_new_round(data[-1]["Liste des paires: "])
            data.extend([data_new_round, data_players])

            file_path = os.path.join("data", "tournament_pending.json")
            RoundModel.save_data(file_path, data)

            print(data_new_round)
            print(data_players)
        else:
            print("Tous les rounds du tournoi ont été joués")

        return new_round_number

    def end_round(self):
        end_date = datetime.datetime.today().strftime("%d-%m-%Y")
        end = {"Date_de_fin_round": end_date}
        file_path = os.path.join("data", "tournament_pending.json")
        with open(file_path, "r") as file:
            data = json.load(file)
        data.append(end)

        print(end)

        file_path = os.path.join("data", "tournament_pending.json")
        with open(file_path, "w") as file:
            json.dump(data, file, ensure_ascii=False, indent=4)
        file_path2 = os.path.join("data", "tournament_data.json")
        with open(file_path2, "w") as file:
            json.dump(data, file, ensure_ascii=False, indent=4)

        return end

    def create_pairs_round_one(self):
        ''' Permet de créer les paires de joueurs lors du premier round d'un tournoi'''
        file_path = os.path.join("data", "tournament_data.json")
        with open(file_path, "r") as file:
            data = json.load(file)
        data_player = data[-1]
        list_player = data_player.get("Liste_joueurs_inscrits")
        random.shuffle(list_player)
        pairings = [(list_player[i], list_player[i + 1]) for i in range(0, len(list_player), 2)]
        return pairings

    def create_pairs_new_round(self, pairing_data):
        ''' Permet de créer les paires de joueurs lors des rounds suivants'''
        dict_player = {}
        b = []
        list_players = []
        list_pairs = []

        for match in pairing_data:
            for player in match:
                dict_player.update(player)
                a = list(dict_player.items())
                b.append(a)

        sorted_b = sorted(b, key=lambda x: (x[-1]), reverse=True)
        list_players.append(sorted_b)
        list_players.pop()

        for i in range(0, len(list_players), 2):
            player1 = list_players[i]
            player2 = list_players[i + 1] if i + 1 < len(list_players) else None

            if (player1, player2) not in pairing_data and (player2, player1) not in pairing_data:
                dict_player1 = dict(player1)
                dict_player2 = dict(player2)
                pairings_player = [dict_player1, dict_player2]
                list_pairs.append(pairings_player)

        return {"Liste_des_paires": list_pairs}

    def update_matches(self, updated_matches):
        '''Met à jour les matchs du round avec de nouvelles valeurs.'''
        for match_index, match in enumerate(self.matches):
            # Mets à jour les valeurs du match
            if match_index < len(updated_matches):
                match_data = updated_matches[match_index]
                for key, value in match_data.items():
                    setattr(match, key, value)
