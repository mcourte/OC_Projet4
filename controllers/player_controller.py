import os
import json

from models.player_model import Player
from views.player_view import PlayerView


class PlayerController:
    def __init__(self):
        '''Contrôleur pour gérer les joueurs.'''
        pass

    def player_menu(self):
        '''Permet de lancer les fonctions suivant les choix de l'utilisateur'''
        while True:
            choice = PlayerView().display_player_menu()
            print(f"User choice: {choice}")
            if choice == "1":
                self.create_player()
            elif choice == "0":
                break
            else:
                print("Option invalide. Veuillez choisir une option valide.")

    def create_player(self):
        '''Permet de créer un nouveau joueur'''
        # Récuperer les informations fournies par l'utilisateur
        surname = PlayerView.player_surname(self).capitalize()
        name = PlayerView.player_name(self).capitalize()
        date_of_birth = PlayerView.player_date_of_birth(self)
        player_ID = PlayerView.player_ID(self).upper()
        score_tournament = 0
        chess_ID = Player.random_ID(self)
        # Si l'utilisateur ne rentre pas l'ID d'un joueur, création d'un ID aléatoire
        if player_ID == "":
            player_ID = chess_ID
        # Transformation des informations en dictionnaire
        player_information = [{
            "Surname": surname,
            "Name": name,
            "Date_of_birth": date_of_birth,
            "Player_ID": player_ID,
            "Score_tournament": score_tournament,
        }]

        # Enregistrement des informations dans un fichier JSON :
        file_path = os.path.join("data", "players_data.json")
        data = Player.load_data(self)
        data.extend(player_information)
        with open(file_path, "w") as file:
            json.dump(data, file, ensure_ascii=False, indent=4)
        print("Le joueur a bien été ajouté")

    def display_players(self):
        '''Permet de trier les joueurs par ordre alphabétique'''

        file_path = os.path.join("data", "players_data.json")

        # Charge les données des joueurs
        try:
            with open(file_path, "r") as file:
                data = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            data = []

        sorted_player = [list(player.items()) for player in data]

        # Trie la liste des joueurs par Surname x[0] et Name x[1]
        sorted_name = sorted(sorted_player, key=lambda x: (x[0], x[1]))

        return sorted_name
