import os
import json


from views import match_view


class MatchController:

    def __init__(self):
        pass

    def winner(self):
        '''Permet de mettre à jour les scores des joueurs'''
        list_match_result = []
        players = []
        file_path = os.path.join("data", "tournament_pending.json")
        with open(file_path,  "r") as file:
            data_tournament = json.load(file)
        data = data_tournament[-1]
        list_match = data.get("Liste des paires: ")
        for match in list_match:
            match_choice = match_view.MatchView().choose_match()
            if match_choice == "oui":
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
                        player2_score_match = 0
                        match_result = ((ID_player1, player1_score_match), (ID_player2, player2_score_match))

                    if str(winner_ID) == str(ID_player2):
                        player2_score_match = 1
                        player1_score_match = 0
                        match_result = ((ID_player1, player1_score_match), (ID_player2, player2_score_match))

                    if str(winner_ID) == "nul":
                        player2_score_match = 0.5
                        player1_score_match = 0.5
                        match_result = ((ID_player1, player1_score_match), (ID_player2, player2_score_match))
                    list_match_result.append(match_result)
                    player1["Score global du joueur: "] = player1_score + player1_score_match
                    player2["Score global du joueur: "] = player2_score + player2_score_match
                    result_match = {"Liste des scores des matchs: ": list_match_result}
                    players.append(player1)
                    players.append(player2)
            elif match_choice == "non":
                break
            else:
                print("Réponse non valide.")
        data_tournament.append(result_match)
        with open(file_path, "w") as file:
            json.dump(data_tournament, file, ensure_ascii=False, indent=1)

    def update_matches(self, updated_matches):
        """Met à jour les matchs du round avec de nouvelles valeurs."""
        for match_index, match in enumerate(self.matches):
            if match_index < len(updated_matches):
                match_data = updated_matches[match_index]
                for key, value in match_data.items():
                    setattr(match, key, value)


test = MatchController()
test.winner()
