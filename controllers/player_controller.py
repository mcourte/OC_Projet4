import os
import json

from models.player_model import Player
from views.player_view import PlayerView


class PlayerController:
    def __init__(self):
        pass

    def create_player(self):
        '''Permet de créer un nouveau joueur'''
        surname = PlayerView().player_surname()
        name = PlayerView().player_name()
        date_of_birth = PlayerView().player_date_of_birth()
        player_ID = PlayerView().player_ID()
        chess_ID = Player().random_ID()
        score_tournament = 0

        if player_ID == "":
            player_ID = chess_ID

        player_information = [{
            "last_name": name,
            "first_name": surname,
            "birth_date": date_of_birth,
            "player_id": player_ID,
            "score_tournament": score_tournament,
        }]

        # Enregistrement des informations dans un fichier JSON :
        file_path = os.path.join("data", "players_data.json")
        data = Player.load_data(file_path)
        data.extend(player_information)

        with open(file_path, "w") as file:
            json.dump(data, file, ensure_ascii=False, indent=4)

    def display_players(self):
        '''Permet de trier les joueurs par ordre alphabétique'''
        list_dict_player = []
        dict_player = {}
        sorted_player = []
        file_path = os.path.join("data", "players_data.json")
        try:
            with open(file_path, "r") as file:
                data = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            data = []

        for i in range(len(data)):
            player = data[i]
            list_dict_player.append(player)

        for i in list_dict_player:
            dict_player.update(i)
            a = list(dict_player.items())
            sorted_player.append(a)

        sorted_name = sorted(sorted_player, key=lambda x: (x[0], x[1]))
        for name in sorted_name:
            print(name)
        return sorted_name

    def player_menu(self):
        '''Permet de lancer les fonctions suivant les choix de l'utilisateur'''
        while True:
            choice = PlayerView().display_player_menu()
            if choice == "1":
                self.create_player()
            elif choice == "2":
                self.display_players()
            elif choice == "3":
                break
            else:
                print("Option invalide. Veuillez choisir une option valide.")
