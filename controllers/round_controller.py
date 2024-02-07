from models.round_model import RoundModel
from models.tournament_model import Tournament


class RoundController:
    def __init__(self):
        pass

    def start_round(self, tournament, tournament_ID, player_ID):
        name = tournament.get("Nom_du_tournoi")
        startdate = tournament.get("Date_de_debut")
        enddate = None
        number_of_rounds = tournament.get("Nombre_de_round")
        for round_number in range(1, number_of_rounds + 1):
            new_round = RoundModel(
                name_of_tournoi=name,
                start_date=startdate,
                end_date=enddate,
                round_number=round_number
            )
            new_round.start_round_model()

            print(f"Début du round : {round_number}")

            if round_number == 1:
                pairs = new_round.create_pairs_round_one()
            else:
                pairs, _ = new_round.create_pairs_new_round(
                    player_ID
                )

            print("\nProchains matchs pour le round en cours :\n")
            for pair in pairs:
                player1 = pair[0]
                player2 = pair[1]
                player1_name = player1.get("Name")
                player1_surname = player1.get("Surname")
                player2_name = player2.get("Name")
                player2_surname = player2.get("Surname")
                print(f"Match : {player1_name}.{player1_surname} vs {player2_name}.{player2_surname}")
                print("Entrez le score")

                # Saisie des scores par les utilisateurs

                while True:
                    try:
                        score1 = float(
                            input(
                                f"Score de {player1_name}.{player1_surname} :"
                            )
                        )
                        score2 = float(
                            input(
                                f"Score de {player2_name}.{player2_surname} : "
                            )
                        )
                        player1scoreinit = player1.get("Score_tournament")
                        player2scoreinit = player2.get("Score_tournament")
                        if score1 > score2:
                            player1score = 1
                            player2score = 0
                        elif score1 < score2:
                            player1score = 0
                            player2score = 1
                        else:
                            player1score = 0.5
                            player2score = 0.5

                        player1["score_tournament "] = player1scoreinit + player1score
                        player2["score_tournament "] = player2scoreinit + player2score
                        break
                    except ValueError:
                        print("Veuillez entrer des chiffres valides pour les scores.")
            new_round.end_round()
        return tournament

    def update_player_points(self, player_points, player_ID, score):
        player_points.setdefault(player_ID, 0)
        player_points[player_ID] += score

    def resume_rounds(self, tournament_ID, player_ID, selected_tournament):
        '''Reprendre l'entrée des résultats pour les rounds d'un tournoi.'''
        print(selected_tournament)
        number_of_rounds = selected_tournament.get("Nombre_de_round")
        round_name = selected_tournament.get("Nom du round")
        print(round_name)
        round_number = round_name[-1]
        dernier_numero_round = max(round_number)
        print("le dernier round est le : ", dernier_numero_round, "\n")
        for round_number in range(dernier_numero_round + 1, number_of_rounds + 1):
            round_name = f"Round {round_number}"
            new_round = RoundModel(round_name)
            new_round.start_round()
            print(f"debut du round : {round_number}\n")
            if round_number == 1:
                new_round.create_pairs_round_one(player_ID)
            else:
                pairs, _ = new_round.create_pairs_new_round(
                    player_ID
                )
            print("\nProchains matchs pour le round en cours :\n")
            for pair in pairs:
                player1 = pair[0]
                player2 = pair[1]
                player1_name = player1.get("Name")
                player1_surname = player1.get("Surname")
                player2_name = player2.get("Name")
                player2_surname = player2.get("Surname")
                print(f"Match : {player1_name}.{player1_surname} vs {player2_name}.{player2_surname}")
                print("Entrez le score")

                # Saisie des scores par les utilisateurs

                while True:
                    try:
                        score1 = float(
                            input(
                                f"Score de {player1_name}.{player1_surname} :"
                            )
                        )
                        score2 = float(
                            input(
                                f"Score de {player2_name}.{player2_surname} : "
                            )
                        )
                        player1scoreinit = player1.get("Score_tournament")
                        player2scoreinit = player2.get("Score_tournament")
                        if score1 > score2:
                            player1score = 1
                            player2score = 0
                        elif score1 < score2:
                            player1score = 0
                            player2score = 1
                        else:
                            player1score = 0.5
                            player2score = 0.5

                        player1["score_tournament "] = player1scoreinit + player1score
                        player2["score_tournament "] = player2scoreinit + player2score
                        break
                    except ValueError:
                        print("Veuillez entrer des chiffres valides pour les scores.")
            new_round.end_round()
            Tournament.update_tournament(
                tournament_ID, {"list_of_tours": selected_tournament.list_of_round}
            )
            if round_number < number_of_rounds:
                user_choice = input("Continuez a entrer les resultats (Oui/non) : ")
                if user_choice.lower() == "non":
                    break
