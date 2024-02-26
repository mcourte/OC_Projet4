"""Define the Player."""

import string
import random
import json
import os


class Player:
    def __init__(self, name, surname, date_of_birth, player_ID, score_tournament):
        '''Initialise une instance de joueur'''
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
        '''Permet de charger l'ensemble des données des joueurs'''
        file_path = os.path.join("data", "players_data.json")
        try:
            with open(file_path, "r") as file:
                return json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            # Si le fichier n'existe pas ou contient une erreur : création d'une liste vite
            return []

    @classmethod
    def get_player_ID(cls, player_ID):
        '''Permet de récupérer les informations d'un joueur via son ID'''
        file_path = os.path.join("data", "players_data.json")
        try:
            with open(file_path, "r") as file:
                players = json.load(file)
                for player in players:
                    if player.get("Player_ID") == player_ID:
                        return player
            return None
        except (FileNotFoundError, json.JSONDecodeError):
            # Si le fichier n'existe pas ou contient une erreur : création d'une liste vite
            return []

    @staticmethod
    def get_player_info(player):
        '''Permet de récupérer les informations d'un joueur'''
        if isinstance(player, dict):
            return {
                'Surname': player.get("Surname"),
                'Name': player.get("Name"),
                'Player_ID': player.get("Player_ID"),
                'Score_tournament': player.get("Score_tournament")
            }
        else:
            return (
                player.player.get("Name"),
                player.player.get("Surname"),
                player.player.get("Player_ID"),
                player.player.get("Score_tournament")
            )

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
