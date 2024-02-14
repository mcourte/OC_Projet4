import os

from models.round_model import RoundModel
from models.match_model import Match
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

    def start_round(self, tournament_ID, player_ID):
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
            list_pairs = []
            print("\nAttention, il est impératif de remplir les scores de l'ensemble des matchs du round :\n")
            if round_number == 1:
                list_pairs_one = new_round.create_pairs_round_one()
                for pair in list_pairs_one:
                    player1_dict, player2_dict = pair[0], pair[1]
                    player1 = Match(player1_dict, {})
                    player2 = Match(player2_dict, {})
                    print("\nProchain match pour le round en cours :\n")
                    MatchController.play_match_round_one(new_round, player1, player2)
                round_number = round_number + 1
                new_round.end_round()
                selected_tournament.add_round(new_round)
                print("\nTous les scores des matchs sont remplis\n")
                updated_values = {"Liste_des_rounds": selected_tournament.list_of_round}
                Tournament.update_tournament(
                    tournament_ID, updated_values
                 )
            else:
                list_pairs = new_round.create_pairs_new_round(player_ID)
                for pair in list_pairs:
                    player1 = Player.get_player_info(pair[0])
                    player2 = Player.get_player_info(pair[1])
                    print("\nProchain match pour le round en cours :\n")
                    MatchController.play_match(new_round, player1, player2)
                round_number = round_number + 1
                new_round.end_round()
                selected_tournament.add_round(new_round)
                print("\nTous les scores des matchs sont remplis\n")
                updated_values = {"Liste_des_rounds": selected_tournament.list_of_round}
                # Tournament.update_tournament(
                #    tournament_ID, updated_values
                # )
            if round_number < number_of_rounds:
                user_choice = input("Continuez a entrer les resultats O/N : ")
                if user_choice.lower() == "n":
                    break
            else:
                break

        if not user_choice.lower() == "n":
            RoundController.calculate_points_for_tournament_final(tournament_ID)

        return selected_tournament

    def update_player_points(self, player_points, player_ID, score):
        player_points.setdefault(player_ID, 0)
        player_points[player_ID] += score

    def resume_rounds(self, player_ID, tournament_ID, round_number, number_of_rounds):
        '''Reprendre l'entrée des résultats pour les rounds d'un tournoi.'''
        file_path = os.path.join("data", "tournament_pending.json")
        selected_tournament = Tournament.load_tournament_by_id(tournament_ID, file_path)
        print(type(selected_tournament))
        tournament_ID = selected_tournament.tournament_ID
        print("le dernier round est le : ", round_number, "\n")
        for round_number in range(round_number + 1, number_of_rounds + 1):
            round_name = f"Round {round_number}"
            new_round = RoundModel(round_name)
            new_round.start_round_model()
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
                player1_ID = player1.get("Player_ID")
                player2_ID = player2.get("Player_ID")
                player2_name = player2.get("Name")
                player2_surname = player2.get("Surname")
                print(f"Match : {player1_name}.{player1_surname} vs {player2_name}.{player2_surname}")
                Tournament.add_round(new_round)
                MatchController.play_match(new_round)
                for item in selected_tournament:
                    if "Player_ID" in item and item["Player_ID"] == player1_ID:
                        item["score_tournament"] = player1["score_tournament"]
                    if "Player_ID" in item and item["Player_ID"] == player2_ID:
                        item["score_tournament"] = player2["score_tournament"]
            new_round.end_round()
            Tournament.update_tournament(tournament_ID, {"List_of_rounds": selected_tournament.list_of_rounds})
            if round_number < number_of_rounds:
                user_choice = input("Continuez a entrer les resultats O/N : ")
                if user_choice.lower() == "n":
                    break
            else:
                break
        if not (user_choice.lower()) == "n":
            self.calculate_points_for_tournament_final(tournament_ID)

    def calculate_points_for_tournament(self, tournament_ID):
        # Charger le tournoi spécifique

        tournament = Tournament.load_tournament_by_id(tournament_ID)
        if not tournament:
            print(f"Tournament with ID {tournament_ID} not found.")
            return
        player_points = {}
        list_of_round = tournament.get("Liste_of_rounds")
        for round_data in list_of_round:
            for match_data in round_data.get("matches", []):
                for player_id, score in match_data:
                    self.update_player_points(player_points, player_id, score)
        sorted_players = sorted(player_points.items(), key=lambda x: x[1], reverse=True)
        return sorted_players

    def get_previous_results(self, tournament_ID, round_number):
        """Récupère les résultats des rounds précédents."""
        previous_results = []
        # Charge les données du tournoi depuis le fichier JSON

        selected_tournament = Tournament.load_tournament_by_id(tournament_ID)
        # Renverse la liste des tours pour parcourir du dernier au premier
        list_of_round = selected_tournament.get("Liste_of_rounds")
        reversed_rounds = reversed(list_of_round)
        # Parcourt les rounds précédents et récupère les résultats des matchs

        for round_data in reversed_rounds:
            current_round_number = round_data.get("round_number", 0)
            if current_round_number < round_number and round_data.get("matches"):
                previous_results.extend(round_data["matches"])
                break
        return previous_results
