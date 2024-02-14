from models.match_model import Match


class MatchController:
    def __init__(self):
        pass

    def play_match_round_one(round, player1, player2):
        print("Entrez le score")
        player1_info, player2_info = Match.get_player_info_match(player1, player2)

        while True:
            try:
                score1 = float(input(f"Score de {player1_info[0]}.{player1_info[1]} : "))
                score2 = float(input(f"Score de {player2_info[0]}.{player2_info[1]} : "))

                if score1 > score2:
                    player1_score = 1
                    player2_score = 0
                elif score1 < score2:
                    player1_score = 0
                    player2_score = 1
                else:
                    player1_score = 0.5
                    player2_score = 0.5
                # Update player scores
                if isinstance(player1, dict):
                    player1["Score_tournament"] = int(player1_info[-1]) + player1_score
                elif isinstance(player1, Match):
                    player1.player1["Score_tournament"] = int(player1_info[-1]) + player1_score

                if isinstance(player2, dict):
                    player2["Score_tournament"] = int(player2_info[-1]) + player2_score
                elif isinstance(player2, Match):
                    player2.player1["Score_tournament"] = int(player2_info[-1]) + player2_score

                break
            except ValueError:
                print("Veuillez entrer des chiffres valides pour les scores.")

        return (
            player1.get("Score_tournament") if isinstance(player1, dict) else player1.player1["Score_tournament"],
            player2.get("Score_tournament") if isinstance(player2, dict) else player2.player1["Score_tournament"]
        )

    def play_match(round, player1, player2):
        print("Entrez le score")
        player1_score_init = player1.get('Score_tournament')
        player2_score_init = player2.get('Score_tournament')
        while True:
            try:
                score1 = float(input(f"Score de {player1.get('Surname')}, {player1.get('Name')} : "))
                score2 = float(input(f"Score de {player2.get('Surname')}, {player2.get('Name')} : "))

                if score1 > score2:
                    player1_score = 1
                    player2_score = 0
                elif score1 < score2:
                    player1_score = 0
                    player2_score = 1
                else:
                    player1_score = 0.5
                    player2_score = 0.5
                # Update player scores
                if isinstance(player1, dict):
                    player1["Score_tournament"] = int(player1_score_init) + player1_score
                elif isinstance(player1, Match):
                    player1.player1["Score_tournament"] = int(player1_score_init) + player1_score

                if isinstance(player2, dict):
                    player2["Score_tournament"] = int(player2_score_init) + player2_score
                elif isinstance(player2, Match):
                    player2.player1["Score_tournament"] = int(player2_score_init) + player2_score

                break
            except ValueError:
                print("Veuillez entrer des chiffres valides pour les scores.")

        return (
                player1.get("Score_tournament") if isinstance(player1, dict) else player1.player1["Score_tournament"],
                player2.get("Score_tournament") if isinstance(player2, dict) else player2.player1["Score_tournament"]
            )
