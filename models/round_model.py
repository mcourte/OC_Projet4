"""Define the Round."""
import json
import random
import os


class Round:
    def __init__(self, name_of_tournoi="", start_date="", end_date="",
                 round_number=0):

        self.name_of_tournoi = name_of_tournoi
        self.start_date = start_date
        self.end_date = end_date
        self.round_number = round_number

    def load_data(self, file_path):
        try:
            with open(file_path, "r") as file:
                return json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def save_data(self, file_path, data):
        with open(file_path, "w") as file:
            json.dump(data, file, ensure_ascii=False, indent=4)

    def create_pairs_round_one(self):
        ''' Permet de créer les paires de joueurs lors du premier round d'un tournoi'''
        file_path = os.path.join("data", "tournament_data.json")
        with open(file_path, "r") as file:
            data = json.load(file)
        players = data[-1]
        list_player = players.get("Liste des joueurs inscrits: ")
        list_player = list_player[0]
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

        return {"Liste des paires: ": list_pairs}

    def update_matches(self, updated_matches):
        '''Met à jour les matchs du round avec de nouvelles valeurs.'''
        for match_index, match in enumerate(self.matches):
            # Mets à jour les valeurs du match
            if match_index < len(updated_matches):
                match_data = updated_matches[match_index]
                for key, value in match_data.items():
                    setattr(match, key, value)
