import os
import json
from views.match_view import MatchView


class MatchController:
    def update_player_scores(player, match_result):
        player_score = player.get("Score global du joueur: ")
        player_score_match = match_result.get(player["Identifiant National d'Echecs: "], 0)
        player["Score global du joueur: "] = player_score + player_score_match

    def process_match(self):
        '''Permet de mettre à jour les scores des joueurs'''
        list_match_result = []
        file_path = os.path.join("data", "tournament_pending.json")
        with open(file_path,  "r") as file:
            data_tournament = json.load(file)
        data = data_tournament[-1]
        for match in data:
            match_choice = MatchView().choose_match()
            if match_choice == "oui":
                for i in range(0, len(match), 2):
                    player1 = match[0]
                    player2 = match[1]
                    ID_player1 = player1.get("Identifiant National d'Echecs: ")
                    ID_player2 = player2.get("Identifiant National d'Echecs: ")
                    print(player1, player2)
                    winner_ID = MatchView().match_view()
                    if winner_ID == ID_player1:
                        match_result = {ID_player1: 1, ID_player2: 0}
                    elif winner_ID == ID_player2:
                        match_result = {ID_player1: 0, ID_player2: 1}
                    else:
                        match_result = {ID_player1: 0.5, ID_player2: 0.5}

                    list_match_result.append(match_result)
                    MatchController.update_player_scores(player1, match_result)
                    MatchController.update_player_scores(player2, match_result)

                    result_match = {"Liste des scores des matchs: ": list_match_result}
            elif match_choice == "non":
                break
            else:
                print("Réponse non valide.")
        data_tournament.append(result_match)
        with open(file_path, "w") as file:
            json.dump(data_tournament, file, ensure_ascii=False, indent=1)
        return data_tournament

    def update_matches(self):
        '''Met à jour les matchs du round avec de nouvelles valeurs.'''
        file_path = os.path.join("data", "tournament_pending.json")
        with open(file_path,  "r") as file:
            data = json.load(file)
        data_tournament = data[-1]
        data_matchs = data[-2]

        current_match_index = 0

        for matchs in data_matchs:
            for match in matchs:
                player_ID = match.get("Identifiant National d'Echecs: ")
                matchs_played = data_tournament.get("Liste des scores des matchs: ")
                for match_index, match in enumerate(matchs_played):
                    if match_index < len(matchs):
                        match_data = matchs[match_index]
                        player_IDs = match_data.get("Identifiant National d'Echecs: ")
                        print(player_IDs)
                        if player_ID in player_IDs:
                            index = match_index + 1
                            print(index)
                            next_match = data_matchs[index]

                len_data = len(data_matchs) - 1
                if index <= len_data:
                    match_choice = MatchView().choose_match()
                    if match_choice == "oui":
                        for i in range(0, len(match), 2):
                            player1 = next_match[0]
                            player2 = next_match[1]
                            ID_player1 = player1.get("Identifiant National d'Echecs: ")
                            ID_player2 = player2.get("Identifiant National d'Echecs: ")
                            print(player1, player2)
                            winner_ID = MatchView().match_view()
                            if winner_ID == ID_player1:
                                match_result = {ID_player1: 1, ID_player2: 0}
                            elif winner_ID == ID_player2:
                                match_result = {ID_player1: 0, ID_player2: 1}
                            else:
                                match_result = {ID_player1: 0.5, ID_player2: 0.5}
                            matchs_played.append(match_result)
                            MatchController.update_player_scores(player1, match_result)
                            MatchController.update_player_scores(player2, match_result)

                            result_match = {"Liste des scores des matchs: ": matchs_played}
                    elif match_choice == "non":
                        break
                    else:
                        print("Réponse non valide.")

                    # Increment the current match index
                    current_match_index += 1

                    # Check if all matches have been played
                    if current_match_index == len_data:
                        print("Tous les matchs ont été joués.")
                        break

                    data_tournament.update(result_match)
                    data.pop()
                    data.append(data_tournament)
                    # with open(file_path, "w") as file:
                    #    json.dump(data, file, ensure_ascii=False, indent=1)

    def play_match(round):
        '''Simule le déroulement des matches pour un round.'''
        for match in round.matches:
            print(
                f"Entrez le score pour "
                f"{match.player1.first_name} {match.player1.last_name} vs "
                f"{match.player2.first_name} {match.player2.last_name}\n"
            )
            while True:
                try:
                    score1 = int(
                        input(
                            f"Score de {match.player1.first_name} {match.player1.last_name}: "
                        )
                    )
                    score2 = int(
                        input(
                            f"Score de {match.player2.first_name} {match.player2.last_name}: "
                        )
                    )
                    print()
                    match.score1 = score1
                    match.score2 = score2
                    if score1 > score2:
                        match.score1 = 1
                        match.score2 = 0
                    elif score1 < score2:
                        match.score1 = 0
                        match.score2 = 1
                    else:
                        match.score1 = 0.5
                        match.score2 = 0.5
                    break
                except ValueError:
                    print("Veuillez entrer des chiffres valides pour les scores.")
