import os
import json


from views import match_view


class MatchController:

    def __init__(self):
        pass

    def winner(self):
        '''Permet de mettre à jour les scores des joueurs'''
        list_result_match = []
        file_path = os.path.join("data", "tournament_pending.json")
        with open(file_path,  "r") as file:
            data_tournament = json.load(file)
        data = data_tournament[-1]
        list_match = data.get("Liste des paires: ")
        for match in list_match:
            for i in range(0, len(match), 2):
                player1 = match[0]
                player2 = match[1]
                ID_player1 = player1.get("Identifiant National d'Echecs: ")
                ID_player2 = player2.get("Identifiant National d'Echecs: ")
                player1_score = player1.get("Score global du joueur: ")
                player2_score = player2.get("Score global du joueur: ")
                print(player1, player2)
                winner_ID = match_view.MatchView().match_view()
                if str(winner_ID) == str(ID_player1):
                    player1_score_match = 1
                    player1_score += 1
                    player2_score_match = 0
                    player2_score += 0
                    match_result = [(ID_player1, player1_score_match), (ID_player2, player2_score_match)]

                if str(winner_ID) == str(ID_player2):
                    player2_score_match = 1
                    player2_score += 1
                    player1_score_match = 0
                    player1_score += 0
                    match_result = [(ID_player1, player1_score_match), (ID_player2, player2_score_match)]

                if str(winner_ID) == "nul":
                    player2_score_match = 0.5
                    player1_score += 0.5
                    player1_score_match = 0.5
                    player1_score += 0.5
                    match_result = [(ID_player1, player1_score_match), (ID_player2, player2_score_match)]

            player1.update(str(player1_score))
            player2.update(str(player2_score))
            print(player1, player2)
            list_result_match.append(match_result)

        result_match = {"Liste des scores des matchs: ": list_result_match}
        data_tournament.append(result_match)
        with open(file_path, "w") as file:
            json.dump(data_tournament, file, ensure_ascii=False, indent=1)


test = MatchController()
test.winner()
