
import os
import json

import datetime
import random
import pandas as pd 

from views import match_view
from controllers import player_controller

class MatchController :
    def __init__(self):
        pass

    def duo_player(self):  
        paire_player=[]
        file_path=os.path.join("data","tournament_data.json")
        with open(file_path, "r") as file:
            data = json.load(file)
        players=data[1]
        list_player=players.get("Liste des joueurs inscrits: ")
        list_player=list_player[0]
        for i in list_player :
            random_player=random.sample(list_player, 2)
            paire_player.append(random_player)

        self.paire_player=paire_player
        

        return self.paire_player
   
        

        #return random_player
    
    def match(self):
        paire_player = MatchController().duo_player()
        match = random.sample(paire_player,1)
        file_path = os.path.join("data","match_data.json")
        with open(file_path,  "w") as file:
            json.dump(match, file, ensure_ascii=False, indent=4)

    def winner(self):
        file_path = os.path.join("data","match_data.json")
        with open(file_path, "r") as file:
            data = json.load(file)
        players_match = data
        players = players_match[0]
        player1 = players[0]
        player2 = players[1]
        ID_player1=player1.get("Identifiant National d'Echecs: ")
        ID_player2=player2.get("Identifiant National d'Echecs: ")
        print(ID_player1, ID_player2)
        winner_ID = match_view.MatchView().match_view()
        if str(winner_ID) == str(ID_player1) :
            player1_score = player1.get("Score global du joueur: ")
            player1_score +=1 
            players[0].update({"Score global du joueur: " : player1_score})

        if str(winner_ID) == str(ID_player2) :
            player2_score = player1.get("Score global du joueur: ")
            player2_score +=1 
            players[1].update({"Score global du joueur: " : player2_score})

        if str(winner_ID) == "nul" :
            player1_score = player1.get("Score global du joueur: ")
            player1_score += 0.5 
            player2_score = player1.get("Score global du joueur: ")
            player2_score += 0.5
            players[0].update({"Score global du joueur: " : player1_score})
            players[1].update({"Score global du joueur: " : player2_score})
        with open(file_path,  "w") as file:
            json.dump(players, file, ensure_ascii=False, indent=4)

        



match=MatchController()
match.match()
match.winner()





