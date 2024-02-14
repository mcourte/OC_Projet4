"""Define the Round."""
import json
import random
import os
import datetime

from models.match_model import Match


class RoundModel:
    def __init__(self, round_name, start_time=None, end_time=None):
        """Initialise une instance de Round avec un nom, une heure de début et une heure de fin optionnelles."""
        self.round_name = round_name
        self.start_time = start_time or datetime.datetime.now()
        self.end_time = end_time
        self.matches = []
        self.players = []

    def get_players(self):
        return self.players

    def start_round_model(self):

        start_date = datetime.datetime.today().strftime("%d/%m/%Y")
        round_number = 1
        file_path = os.path.join("data", "tournament_data.json")
        with open(file_path, "r") as file:
            data = json.load(file)
        data_round = {
            "Nom du Round: ": f"Round {round_number}",
            "Date de début: ": start_date,
        }
        data.extend([data_round])

        file_path2 = os.path.join("data", "tournament_pending.json")
        with open(file_path2, "w") as file:
            json.dump(data, file, ensure_ascii=False, indent=4)

        return data_round

    def end_round(self):
        end_date = datetime.datetime.today().strftime("%d/%m/%Y")
        end = {"Date_de_fin_round": end_date}
        file_path = os.path.join("data", "tournament_pending.json")
        with open(file_path, "r") as file:
            data = json.load(file)
        data.append(end)

        file_path = os.path.join("data", "tournament_pending.json")
        with open(file_path, "w") as file:
            json.dump(data, file, ensure_ascii=False, indent=4)
        file_path2 = os.path.join("data", "tournament_data.json")
        with open(file_path2, "w") as file:
            json.dump(data, file, ensure_ascii=False, indent=4)

    def create_pairs_round_one(self):
        file_path = os.path.join("data", "tournament_data.json")
        with open(file_path, "r") as file:
            data_player = json.load(file)

        list_player = data_player[-1].get("Liste_joueurs_inscrits")
        random.shuffle(list_player)

        pairings = [(list_player[i], list_player[i + 1]) for i in range(0, len(list_player), 2)]

        for pair in pairings:
            player1 = pair[0]
            player2 = pair[1]

            player1_info = {
                "Name": player1.get("Name"),
                "Surname": player1.get("Surname"),
                "Date_of_birth": player1.get("Date_of_birth"),
                "Player_ID": player1.get("Player_ID"),
                "Score_tournament": player1.get("Score_tournament", 0),  # Default to 0 if not present
            }

            player2_info = {
                "Name": player2.get("Name"),
                "Surname": player2.get("Surname"),
                "Date_of_birth": player2.get("Date_of_birth"),
                "Player_ID": player2.get("Player_ID"),
                "Score_tournament": player2.get("Score_tournament", 0),  # Default to 0 if not present
            }

            match = Match(player1_info, player2_info)
            self.matches.append(match)

        return pairings

    def create_pairs_new_round(self, pairing_data):
        list_players = []
        total_list_pairs = []
        file_path = os.path.join("data", "players_data.json")

        with open(file_path, "r") as file:
            players_info = json.load(file)

        for player_id in pairing_data:
            player_info = next((player for player in players_info if player['Player_ID'] == player_id), None)

            if player_info:
                list_players.append(player_info)

        num_players = len(list_players)

        for i in range(num_players // 2):
            player1 = list_players[i]
            player2 = list_players[num_players // 2 + i]

            pairings_round = [player1, player2]
            total_list_pairs.append(pairings_round)
        list_pairs = [[{'Surname': player['Surname'], 'Name': player['Name'],
                        'Date_of_birth': player['Date_of_birth'], 'Player_ID': player['Player_ID'],
                        'Score_tournament': 0} for player in pair] for pair in total_list_pairs]

        return list_pairs

    def update_matches(self, updated_matches):
        '''Met à jour les matchs du round avec de nouvelles valeurs.'''
        for match_index, match in enumerate(self.matches):
            # Mets à jour les valeurs du match
            if match_index < len(updated_matches):
                match_data = updated_matches[match_index]
                for key, value in match_data.items():
                    setattr(match, key, value)
