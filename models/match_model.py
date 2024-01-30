"""Define the Match."""
import json

from models.player_model import Player


class Match:
    def __init__(self, player1=Player(), player2=Player(), score1=None, score2=None):
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
