"""Define the Player."""

import json

import pandas as pd
import os

from views.player_view import PlayerView
from models.player_model import Player

class PlayerController:
    def __init__(self):
        pass

    def CreatePlayer(self):
        surname=PlayerView().PlayerSurname()
        name=PlayerView().PlayerLastName()
        date_of_birth=PlayerView().PlayerDateOfBirth()
        chess_ID=Player.random_ID()
        self.score_global = 0
        self.name = name
        self.surname = surname
        self.ID = chess_ID
        self.date_of_birth = date_of_birth
        self.player_information=[{
            
                            "Nom: ": self.surname, 
                            "Prénom: ": self.name, 
                            "Date de naissance: ": self.date_of_birth,  
                            "Identifiant National d'Echecs: ": self.ID,
                            "Score global du joueur: " : self.score_global
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

    def list_of_player_keys(self):
        list_keys=[]
        file_path=os.path.join("data","players_data.json")
        with open(file_path, "r") as file:
            data = json.load(file)  
        for data_dict in data :
            # Accessing key-value pairs
            for key, value in data_dict.items():
                players = (f"{key} : {value}")
                keys = players.split(":")[0]
                values = players.split(":")[2].lstrip()
                for i in range(0,1) :
                    list_keys.append(''.join([keys]))
        list_keys=list_keys[0:5]

        return list_keys
    
    def choose_player(self):
        file_path=os.path.join("data","players_data.json")
        with open(file_path, "r") as file:
            data = json.load(file)  
            df=pd.json_normalize(data)
        player_list=df
        return player_list
        
        
        #for data_dict in data :
            # Accessing key-value pairs
        #    for key, value in data_dict.items():
        #        players = (f"{key} : {value}")
        #        IDs_player=players.split(":")[2].lstrip()
        #    list_ID.append(''.join([IDs_player]))
        #choose_players_ID=list_ID
        #for i, indice_ID  in enumerate(choose_players_ID, start=1) : 
        #    list_player_ID = (f"{i}.{indice_ID}")
        #return choose_players_ID
        #sorted_list_surname=sorted(list_surname)
        #print(sorted_list_surname)
