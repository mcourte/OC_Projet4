"""Define the Player."""


import string
import random
import json
import os


class Player:
    def __init__(self, score=0, name="", surname="", date_of_birth="", ID=""):
        self.name = name
        self.score = score
        self.surname = surname
        self.date_of_birth = date_of_birth
        self.ID = ID

    def random_ID(self):
        ''' Cette fonction permet de générer aléatoirement des ID
        Elle sera supprimer une fois les tests finis'''
        nb_letters = 2
        nb_numbers = 5
        letters = ''.join((random.choice(string.ascii_uppercase))
                          for x in range(nb_letters))
        numbers = ''.join((random.choice(string.digits))
                          for x in range(nb_numbers))
        ID_list = list(letters + numbers)
        ID = ''.join(ID_list)
        return ID

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

    def to_dict(self):
        '''Convertit l'objet Player en un dictionnaire.'''

        return {
            "last_name": self.name,
            "first_name": self.surname,
            "birth_date": self.date_of_birth,
            "player_id": self.player_ID,
            "score_tournament": self.score_tournament,
        }

    def update_score_tournament(self, player_ID, new_score):
        '''Met à jour le score du tournoi'''
        players = self.load_data()
        for player in players:
            if player.player_ID == player_ID:
                player.score_tournament += new_score
        file_path = os.path.join("data", "players_data.json")
        for p in players:
            with open(file_path, "w") as file:
                players_data = [
                    {
                        "last_name": p.name,
                        "first_name": p.surname,
                        "birth_date": p.date_of_birth,
                        "player_id": p.player_ID,
                        "score_tournament": p.score_tournament,
                    }
                ]
            json.dump(players_data, file, indent=4)
