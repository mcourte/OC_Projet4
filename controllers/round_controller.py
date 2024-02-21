import os

from models.round_model import RoundModel
# from models.match_model import Match
from models.player_model import Player
from models.tournament_model import Tournament
from controllers.match_controller import MatchController


class RoundController:
    def __init__(self):
        pass

    def calculate_points_for_tournament_final(tournament_ID):
        # Charger le tournoi spécifique
        player_points = {}
        new_tournament_score = 0
        file_path = os.path.join("data", "tournament_pending.json")
        tournament = Tournament.load_tournament_by_id(tournament_ID, file_path)
        list_of_rounds = tournament.list_of_round  # Access the attribute directly
        for round_data in list_of_rounds:
            for match_data in round_data.get("matches", []):
                for player_ID, score in match_data:
                    player_points.setdefault(player_ID, 0)
                    player_points[player_ID] += score
                    # Mets à jour le score du tournoi dans le modèle Player
                    player = Player.get_player_ID(player_ID)
                    if player:
                        new_tournament_score = score
                        player = Player.update_score_tournament(player_ID, new_tournament_score)
                    else:
                        print(f"Joueur avec l'ID {player_ID} non trouvé.")

        sorted_players = sorted(player_points.items(), key=lambda x: x[1], reverse=True)
        print("Classement Final du Tournoi :\n")
        for player_ID, points in sorted_players:
            player = Player.get_player_ID(player_ID)
            if player:
                print(f"{player.name} {player.surname}: {points} points")
            else:
                print(f"Player with ID {player_ID} not found.")
        print()
        return sorted_players

    def start_round(self, list_player_ID, tournament_ID, number_of_rounds, list_of_round):
        file_path = os.path.join("data", "tournament_pending.json")
        selected_tournament = Tournament.load_tournament_by_id(tournament_ID, file_path)
        tournament_ID = selected_tournament.tournament_ID
        number_of_rounds = selected_tournament.number_of_round

        print("\nLe tournoi a", number_of_rounds, "rounds\n")

        for round_number in range(1, number_of_rounds + 1):
            round_name = f"Round {round_number}"
            new_round = RoundModel(round_name)
            new_round.start_round_model()
            print(f"\nDébut du round : {round_number}\n")
            print("\nAttention, il est impératif de remplir les scores de l'ensemble des matchs du round :\n")

            if round_number == 1:
                list_pairs_one = new_round.create_pairs_round_one(list_player_ID)
                selected_tournament.add_round(new_round)
                for pair in list_pairs_one:
                    player1 = pair[0]
                    player2 = pair[1]
                    print("\nProchain match pour le round en cours :\n")
                    MatchController.play_match(new_round, player1, player2)
            new_round.end_round()
            selected_tournament.to_dict()
            print("\nTous les scores des matchs sont remplis\n")
            updates_values = {'Liste_des_rounds': selected_tournament.list_of_round}
            Tournament.update_tournament(
                tournament_ID, updates_values
                )

            if round_number < number_of_rounds:
                user_choice = input("Continuez a entrer les resultats O/N : ")
                if user_choice.lower() == "o":
                    round_controller = RoundController()
                    round_controller.resume_rounds(list_player_ID, tournament_ID,
                                                   round_number, number_of_rounds,
                                                   list_of_round)
                else:
                    break
        return selected_tournament

    def resume_rounds(self, list_player_ID, tournament_ID,
                      round_number, number_of_rounds,
                      list_of_round):
        '''Reprendre l'entrée des résultats pour les rounds d'un tournoi.'''
        file_path = os.path.join("data", "tournament_pending.json")
        selected_tournament = Tournament.load_tournament_by_id(tournament_ID, file_path)
        print("le dernier round est le : ", round_number, "\n")
        round_number = round_number + 1
        if round_number <= int(number_of_rounds):
            round_name = f"Round {round_number}"
            new_round = RoundModel(round_name)
            new_round.start_round_model()

            print(f"\nDébut du round : {round_number}\n")
            list_pairs = []
            print("\nAttention, il est impératif de remplir les scores de l'ensemble des matchs du round :\n")
            previous_result = self.get_previous_results(tournament_ID, round_number)
            print("...")
            sorted_players = self.calculate_points_for_tournament(tournament_ID)
            print("tttt")
            list_pairs = new_round.create_pairs_new_round_2(list_player_ID, previous_result)
            for pair in list_pairs:
                player1 = pair[0]
                print(player1)
                player2 = pair[1]
                print(player2)
                player1 = Player.get_player_info(player1)
                player2 = Player.get_player_info(player2)
                print("\nProchain match pour le round en cours :\n")
                MatchController.play_match_2(new_round, player1, player2)
            round_number = round_number + 1
            new_round.end_round()
            list_of_round.append(new_round)
            print("\nTous les scores des matchs sont remplis\n")
            updates_values = {'Liste_des_rounds': list_of_round}
            Tournament.update_tournament(
                    tournament_ID, updates_values
                )
            if round_number < number_of_rounds:
                user_choice = input("Continuez a entrer les resultats O/N : ")
                if user_choice.lower() == "n":
                    pass
            else:
                pass

        if not user_choice.lower() == "n":
            RoundController.calculate_points_for_tournament_final(tournament_ID)

        return selected_tournament

    def calculate_points_for_tournament(self, tournament_ID):
        # Charger le tournoi spécifique
        file_path = os.path.join("data", "tournament_pending.json")
        tournament = Tournament.load_tournament_by_id(tournament_ID, file_path)
        if not tournament:
            print(f"Tournament with ID {tournament_ID} not found.")
            return
        player_points = {}
        list_of_round = tournament.list_of_round
        for round_data in list_of_round:
            for match_data in round_data.get("matches"):
                player1 = match_data.get("player1")
                player1_score = int(match_data.get("score1"))
                player1_ID = player1[0].get("Player_ID")
                player1_point = player1[0].get("Score_tournament")
                player2 = match_data.get("player2")
                player2_score = int(match_data.get("score2"))
                player2_ID = player2[0].get("Player_ID")
                player2_point = player2[0].get("Score_tournament")
                self.update_player_points(player1_ID, player1_point, player1_score)
                self.update_player_points(player2_ID, player2_point, player2_score)
        sorted_players = sorted(player_points.items(), key=lambda x: x[1], reverse=True)
        return sorted_players

    def get_previous_results(self, tournament_ID, round_number):
        """Récupère les résultats des rounds précédents."""
        previous_results = []
        # Charge les données du tournoi depuis le fichier JSON
        file_path = os.path.join("data", "tournament_pending.json")
        selected_tournament = Tournament.load_tournament_by_id(tournament_ID, file_path)
        # Renverse la liste des tours pour parcourir du dernier au premier
        list_of_round = selected_tournament.list_of_round
        reversed_rounds = reversed(list_of_round)
        # Parcourt les rounds précédents et récupère les résultats des matchs
        for round_data in reversed_rounds:
            current_round_number = round_data.get("round_number", 0)
            if current_round_number < round_number and round_data.get("matches"):
                previous_results.extend(round_data["matches"])
                print(previous_results)
                break
        return previous_results

    def update_matches_in_round(self, round_number, tournament_ID, updated_matches):
        # Charge l'instance spécifique du tournoi à partir du fichier JSON

        selected_tournament = Tournament.load_tournament_by_id(tournament_ID)
        # Récupére le round spécifique

        round_to_update = selected_tournament.get_round_by_number(round_number)
        if round_to_update:
            # Mets à jour les matchs dans le round

            round_to_update.update_matches(updated_matches)
            # Mets à jour le tournoi avec les nouvelles valeurs

            Tournament.update_tournament(
                tournament_ID, {"list_of_tours": selected_tournament.list_of_rounds}
            )

    def update_player_points(self, player_points, player_ID, score):
        player_points = {player_ID: 0}
        player_points[player_ID] += score
