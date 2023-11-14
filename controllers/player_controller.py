"""Define the Player."""

import json

import datetime
import os

from views.player_view import PlayerView
from models.player_model import Player

class PlayerController:
    def __init__(self):
        pass

    def CreatePlayer(self):
        name=PlayerView().PlayerLastName()
        surname=PlayerView().PlayerSurname()
        date_of_birth=PlayerView().PlayerDateOfBirth()
        chess_ID=Player.random_ID()
        self.name = name
        self.surname = surname
        self.ID = chess_ID
        self.date_of_birth = date_of_birth
        self.player_information=[{
            
                            "Nom: ": self.name, 
                            "Prénom: ": self.surname, 
                            "Date de naissance: ": self.date_of_birth,  
                            "Identifiant National d'Echecs: ": self.ID
                            }
        ]
        #Enregistrement des informations dans un fichier JSON :   
        file_path=os.path.join("data","players_data.json")
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

    def MatchResult(self):
        pass

player=PlayerView()
player=PlayerController()
player.CreatePlayer()


