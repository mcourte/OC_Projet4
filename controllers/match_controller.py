
import os
import json


from controllers import round_controller


class MatchController:

    def __init__(self):
        pass

    def match(self):
        '''Crée la liste des matchs d'un round'''
        list_match = []
        dict_player = round_controller.RoundController().paires_of_player()
        list_player = list(dict_player.values())
        for i in range(0, len(list_player)):
            match_i = list_player[i]
            list_match.append(match_i)
        print(list_match)
        return list_match

    def winner(self):
        '''Permet de mettre à jour les scores des joueurs'''
        file_path = os.path.join("data", "round_data.json")
        with open(file_path, "r") as file:
            data = json.load(file)
        # round_choice = input("Quel round souhaitez vous sélectionner ?")

        for i in range(0, len(data)):
            data = data[i]
            print(type(data))

        # list_match = list_match[0]
        # for match in list_match :
        #    player1 = match[0]
        #    player2 = match[1]
        #    ID_player1=player1.get("Identifiant National d'Echecs: ")
        #    ID_player2=player2.get("Identifiant National d'Echecs: ")
        #    player1_score = player1.get("Score global du joueur: ")
        #    player2_score = player2.get("Score global du joueur: ")
        #    print(player1, player2)
        #    winner_ID = match_view.MatchView().match_view()
        #    if str(winner_ID) == str(ID_player1) :
        #        player1_score += 1
        #        match_result = [(player1, {"Score global du tournoi: " :player1_score}),
        #                        (player2, {"Score global du tournoi: " :player2_score})]

        #    if str(winner_ID) == str(ID_player2) :
        #        player2_score +=1
        #        match_result = [(player1, {"Score global du tournoi: " :player1_score}),
        #                        (player2, {"Score global du tournoi: " :player2_score})]

        #    if str(winner_ID) == "nul" :
        #        player1_score += 0.5
        #        player2_score += 0.5
        #        match_result = [(player1, {"Score global du tournoi: " :player1_score}),
        #                        (player2, {"Score global du tournoi: " :player2_score})]

        #    data.append(match_result)
        #    with open(file_path,  "w") as file:
        #        json.dump(data, file, ensure_ascii=False, indent=4)
