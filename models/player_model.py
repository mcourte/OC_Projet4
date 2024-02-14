"""Define the Player."""

import string
import random
import json
import os


class Player:
    def __init__(self, name, surname, date_of_birth, player_ID, score_tournament):
        self.name = name
        self.surname = surname
        self.date_of_birth = date_of_birth
        self.player_ID = player_ID
        self.score_tournament = score_tournament

    def random_ID(self):
        ''' Cette fonction permet de générer aléatoirement des ID'''
        nb_letters = 2
        nb_numbers = 5
        letters = ''.join((random.choice(string.ascii_uppercase))
                          for x in range(nb_letters))
        numbers = ''.join((random.choice(string.digits))
                          for x in range(nb_numbers))
        ID_list = list(letters + numbers)
        player_ID = ''.join(ID_list)
        return player_ID

    def load_data(self):
        file_path = os.path.join("data", "players_data.json")
        try:
            with open(file_path, "r") as file:
                return json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            # Si le fichier n'existe pas ou contient une erreur : création d'une liste vite
            return []

    def save_data(self, data):
        file_path = os.path.join("data", "players_data.json")
        with open(file_path, "w") as file:
            json.dump(data, file, ensure_ascii=False, indent=4)

    def update_score_tournament(self, player_ID, new_score):
        '''Met à jour le score du tournoi'''
        players = self.load_data()
        for player in players:
            if player.player_ID == player_ID:
                player.score_tournament += new_score
        file_path = os.path.join("data", "players_data.json")
        for player in players:
            with open(file_path, "w") as file:
                players_data = [
                    {
                        "Surname": player.name,
                        "Name": player.surname,
                        "Date_of_birth": player.date_of_birth,
                        "Player_ID": player.player_ID,
                        "Score_tournament": player.score_tournament,
                    }
                ]
            json.dump(players_data, file, indent=4)

    def load_players_ID(cls, players_ids):
        # Charge tous les joueurs
        all_players = cls.load_data()
        selected_players = [
            player for player in all_players if player.player_ID in players_ids
        ]
        return selected_players

    @classmethod
    def get_player_ID(cls, player_ID):
        players = cls.load_data()
        for player in players:
            if player.player_ID == player_ID:
                return player
        return None  # Retourne None si le joueur n'est pas trouvé

    @classmethod
    def get_player_by_name(cls, player_name):
        players = cls.load_data()
        for player in players:
            if player.name == player_name:
                return player
        return None  # Returns None if the player is not found

    @staticmethod
    def get_player_info(player):
        if isinstance(player, dict):
            return {
                'Surname': player.get('Surname'),
                'Name': player.get('Name'),
                'Player_ID': player.get('Player_ID'),
                'Score_tournament': player.get('Score_tournament')
            }
        else:
            return (
                player.player1.get("Name"),
                player.player1.get("Surname"),
                player.player1.get("Player_ID"),
                player.player1.get("Score_tournament")
            )
