from models.match_model import Match


class MatchController:
    def __init__(self):
        pass

    @staticmethod
    def play_match_round_one(round, player1_info, player2_info):
        print("Entrez le score : (0/1/0.5)")
        player1_score_init = player1_info.get('Score_tournament')
        player2_score_init = player2_info.get('Score_tournament')
        while True:
            try:
                score1 = float(input(f"Score de {player1_info.get('Name')}.{player1_info.get('Surname')} : "))
                if score1 not in {0, 0.5, 1}:
                    print("Veuillez entrez un score corect (1,0 ou 0.5)")
                    continue
                score2 = float(input(f"Score de {player2_info.get('Name')}.{player2_info.get('Surname')} : "))
                if score2 not in {0, 0.5, 1}:
                    print("Veuillez entrez un score corect (1,0 ou 0.5)")
                    continue
                elif score1 > score2:
                    player1_score = 1
                    player2_score = 0
                elif score1 < score2:
                    player1_score = 0
                    player2_score = 1
                elif score1 == score2:
                    player1_score = 0.5
                    player2_score = 0.5
                # Update player scores
                if isinstance(player1_info, dict):
                    player1_info["Score_tournament"] = player1_score_init + player1_score
                # elif isinstance(player1_info, Match):
                #    player1_info.player1["Score_tournament"] = player1_score_init + player1_score

                if isinstance(player2_info, dict):
                    player2_info["Score_tournament"] = player2_score_init + player2_score
                # elif isinstance(player2_info, Match):
                #    player2_info.player2["Score_tournament"] = player2_score_init + player2_score
                break
            except ValueError:
                print("Veuillez entrer des chiffres valides pour les scores.")

        return (
            player1_info.get("Score_tournament") if isinstance(player1_info, dict)
            else player1_info.player1["Score_tournament"],
            player2_info.get("Score_tournament") if isinstance(player2_info, dict)
            else player2_info.player2["Score_tournament"]
        )

    def play_match_2(round, player1, player2):
        print("Entrez le score : (0/1/0.5)")
        player1_score_init = player1.get('Score_tournament')
        player2_score_init = player2.get('Score_tournament')
        while True:
            try:
                score1 = float(input(f"Score de {player1.get('Surname')}, {player1.get('Name')} : "))
                if score1 not in {0, 0.5, 1}:
                    print("Veuillez entrez un score corect (1,0 ou 0.5)")
                    continue
                score2 = float(input(f"Score de {player2.get('Surname')}, {player2.get('Name')} : "))
                if score2 not in {0, 0.5, 1}:
                    print("Veuillez entrez un score corect (1,0 ou 0.5)")
                    continue
                elif score1 > score2:
                    player1_score = 1
                    player2_score = 0
                elif score1 < score2:
                    player1_score = 0
                    player2_score = 1
                elif score1 == score2:
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
                print(player1["Score_tournament"])
                print(player2["Score_tournament"])
                break
            except ValueError:
                print("Veuillez entrer des chiffres valides pour les scores.")

        return (
                player1.get("Score_tournament") if isinstance(player1, dict) else player1.player1["Score_tournament"],
                player2.get("Score_tournament") if isinstance(player2, dict) else player2.player2["Score_tournament"]
            )

    def play_match(round, player1, player2):
        """Simule le déroulement des matches pour un round."""
        match = Match(player1, player2)
        round.matches.append(match)
        # Logique pour simuler le déroulement du match
        # demande les scores aux utilisateurs
        print(
                f"Entrez le score pour "
                f"{match.player1.get('Surname')} {match.player1.get('Name')} vs "
                f"{match.player2.get('Surname')} {match.player2.get('Name')}\n"
            )

        # Saisie des scores par les utilisateurs
        while True:
            try:
                score1 = int(
                    input(
                        f"Score de {match.player1.get('Surname')} {match.player1.get('Name')}: "
                    )
                )
                score2 = int(
                    input(
                        f"Score de {match.player2.get('Surname')} {match.player2.get('Name')}: "
                    )
                )
                print()

                # Mettre à jour les scores des joueurs
                match.score1 = score1
                match.score2 = score2

                # Update player scores
                player1["Score_tournament"] += match.score1
                player2["Score_tournament"] += match.score2
                break
            except ValueError:
                print("Veuillez entrer des chiffres valides pour les scores.")

        return player1["Score_tournament"], player2["Score_tournament"]
