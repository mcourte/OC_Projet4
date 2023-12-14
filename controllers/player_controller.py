"""Define the Player."""

import json

import pandas as pd
import os

from views import player_view
from models import player_model


class PlayerController:

    def __init__(self):
        pass

    def CreatePlayer(self):
        '''Permet de créer un nouveau joueur'''
        surname = player_view.PlayerView().PlayerSurname()
        name = player_view.PlayerView().PlayerLastName()
        date_of_birth = player_view.PlayerView().PlayerDateOfBirth()
        player_ID = player_view.PlayerView().Player_ID()
        chess_ID = player_model.Player().random_ID()
        self.score_global = 0
        self.name = name
        self.surname = surname
        if player_ID == "":
            self.ID = chess_ID
        else:
            self.ID = player_ID
        self.ID = chess_ID
        self.date_of_birth = date_of_birth
        self.player_information = [{"Nom: ": self.surname,
                                    "Prénom: ": self.name,
                                    "Date de naissance: ": self.date_of_birth,
                                    "Identifiant National d'Echecs: ": self.ID,
                                    "Score global du joueur: ": self.score_global}]
        # Enregistrement des informations dans un fichier JSON :
        file_path = os.path.join("data", "players_data.json")
        try:
            with open(file_path, "r") as file:
                data = json.load(file)
        except FileNotFoundError:
            # If the file doesn't exist, create an empty list
            data = []
        except json.JSONDecodeError:
            # If the file is empty or contains invalid JSON, initialize data as an empty list
            data = []
        data.extend(self.player_information)
        with open(file_path,  "w") as file:
            json.dump(data, file, ensure_ascii=False, indent=4)

    def choose_player(self):
        '''Permet de lister les joueurs'''
        file_path = os.path.join("data", "players_data.json")
        with open(file_path, "r") as file:
            data = json.load(file)
            df = pd.json_normalize(data)
        player_list = df
        return player_list

    def display_players(self):
        '''Permet de trier les joueurs par ordre alphabétique (Nom puis prénom)'''
        list_dict_player = []
        dict_player = {}
        sorted_player = []
        file_path = os.path.join("data", "players_data.json")
        with open(file_path, "r") as file:
            data = json.load(file)
        for i in range(0, len(data)):
            dict_player = data[i]
            list_dict_player.append(dict_player)
        for i in list_dict_player:
            dict_player.update(i)
            a = list(dict_player.items())
            sorted_player.append(a)
        for i in range(0, len(sorted_player)):
            sorted_name = sorted(sorted_player,
                                 key=lambda x: (x[0], x[1]))
            sorted_name.append(sorted_name)
        sorted_name.pop()
        for name in sorted_name:
            print(name)
        return sorted_name

    def player_menu(self):
        '''Permet de lancer les fonctions suivant les choix de l'utilisateur'''
        while True:
            choice = player_view.PlayerView().display_player_menu()
            if choice == "1":
                self.CreatePlayer()
            elif choice == "2":
                self.display_players()
            elif choice == "3":
                break
            else:
                print("Option invalide. Veuillez choisir une option valide.")
