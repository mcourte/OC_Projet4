
import os
import json

import datetime
import random
import pandas as pd 

from views import match_view
from controllers import round_controller

class MatchController :
    def __init__(self):
        pass

    
    def match(self):

        list_match=[]
        dict_player = round_controller.RoundController().list_of_paires()
        list_player = list(dict_player.values())
        for i in range(0, len(list_player)) :
            match_i = list_player[i]
            list_match.append(match_i)

        return list_match
        

    def winner(self):
        file_path = os.path.join("data","round_data.json")
        with open(file_path, "r") as file:
            data = json.load(file)
        list_match = MatchController().match()
        print(list_match)
        match_choice = match_view.MatchView().choose_match()
        match_choice = int(match_choice)
        duo_player = list_match[match_choice]
        player1 = duo_player[0]
        player2 = duo_player[1]
        player1 = player1[0]
        player2 = player2[0]
        ID_player1=player1.get("Identifiant National d'Echecs: ")
        ID_player2=player2.get("Identifiant National d'Echecs: ")
        player1_score = player1.get("Score global du joueur: ")
        player2_score = player2.get("Score global du joueur: ")

        print(ID_player1, ID_player2)
        winner_ID = match_view.MatchView().match_view()
        if str(winner_ID) == str(ID_player1) :
            player1_score +=1 
            match_result = [(player1, {"Score du joueur:" :player1_score}), (player2, {"Score du joueur:" :player2_score})]



        if str(winner_ID) == str(ID_player2) :
            player2_score +=1 
            match_result = [(player1, {"Score du joueur:" :player1_score}), (player2, {"Score du joueur:" :player2_score})]


        if str(winner_ID) == "nul" :
            player1_score += 0.5 
            player2_score += 0.5
            match_result = [(player1, {"Score du joueur:" :player1_score}), (player2, {"Score du joueur:" :player2_score})]

        data.extend(match_result)
        with open(file_path,  "w") as file:
            json.dump(data, file, ensure_ascii=False, indent=4)



        



match=MatchController()
match.winner()






