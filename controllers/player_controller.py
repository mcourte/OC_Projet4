"""Define the Player."""

import json

import datetime

from views.player_view import PlayerView
from models.player_model import Player

class PlayerController:
    def __init__(self):
        pass

    def CreatePlayer(self):
        name=PlayerView.PlayerLastName()
        surname=PlayerView.PlayerSurname()
        date_of_birth=PlayerView.PlayerDateOfBirth()
        chess_ID=Player.random_ID()
        self.name = name
        self.surname = surname
        self.ID = chess_ID
        #Transformer la date de naissance en âge :
        td = datetime.date.today()
        dob = datetime.datetime.strptime(date_of_birth, '%d-%m-%Y')
        self.age = td.year-dob.year-((td.month,td.day)<(dob.month,dob.day))
        self.date_of_birth = dob
        #Création d'un dictionnaire pour stocker les informations du joueur :
        player_information={
                            "Nom: ": self.name, 
                            "Prénom: ": self.surname, 
                            "Date de naissance: ": self.date_of_birth, 
                            "Age: ":self.age, 
                            "Identifiant National d'Echecs: ": self.ID
                            }
        #Enregistrement des informations dans un fichier JSON :   
        player_data=json.dumps(player_information, indent=2)
        with open("players_data.json", "w") as f:
            f.write(player_data)
        

    def MatchResult(self):
        pass

player1=PlayerView()
player1=PlayerController()
player1.CreatePlayer()
