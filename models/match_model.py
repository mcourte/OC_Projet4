"""Define the Match."""
import json


class Match:
    def __init__(self, player1, player2, score1=None, score2=None):
        self.player1 = player1
        self.player2 = player2
        self.score1 = score1
        self.score2 = score2

    def load_data(self, file_path):
        try:
            with open(file_path, "r") as file:
                return json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            # Si le fichier n'existe pas ou contient une erreur : création d'une liste vite
            return []

    def save_data(self, file_path, data):
        with open(file_path, "w") as file:
            json.dump(data, file, ensure_ascii=False, indent=4)

    @staticmethod
    def get_player_info_match(player1, player2):
        from models.player_model import Player
        # Your implementation to retrieve and return player information
        player1_info = Player.get_player_info(player1)
        player2_info = Player.get_player_info(player2)
        return player1_info, player2_info
