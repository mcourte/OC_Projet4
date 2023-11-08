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
        #Transformer la date de naissance en âge :
        #td = datetime.date.today()
        date_of_birth = datetime.datetime.strftime(date_of_birth, '%d-%m-%Y')
        #self.age = td.year-date_of_birth.year-((td.month,td.day)<(date_of_birth.month,date_of_birth.day))
        self.date_of_birth = date_of_birth
        #Création d'un dictionnaire pour stocker les informations du joueur :
        #Enregistrement des informations dans un fichier JSON :   

        self.player_information=[
            {
                            "Nom: ": self.name, 
                            "Prénom: ": self.surname, 
                            "Date de naissance: ": self.date_of_birth, 
                            #"Age: ": self.age, 
                            "Identifiant National d'Echecs: ": self.ID
                            }
                            ]
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


